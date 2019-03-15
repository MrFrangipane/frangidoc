import os
import io
import stat
import errno
import shutil
import logging
import tempfile
from pathlib2 import Path

import git
import yaml

from . import parser
from . import discover
from . import renderer


def _handle_remove_read_only(func, path, exc):
    '''
    Removes readonly flag to force removal of files / folders by shutil
    '''
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        func(path)
    else:
        raise


def _clone(repository_url):
    '''
    Clones the given repo url to a temporary directory

    :param repository_url: A valid url
    :return: Temporary directory if cloning succeeded, `None` otherwise
    '''
    repo_name = os.path.basename(repository_url).replace('.git', '')
    temp_folder = tempfile.mkdtemp(prefix="frangidoc-{}.".format(repo_name))

    try:
        git.Repo.clone_from(repository_url, temp_folder)
    except git.GitCommandError as e:
        logging.warning("Impossible to clone {repo_url}".format(repo_url=repository_url))
        logging.warning(e)

        return

    logging.info("Cloned {repo_url} to {temp_folder}".format(repo_url=repository_url, temp_folder=temp_folder))

    return temp_folder


def _load_config(repo_root):
    '''
    Loads and parses .frangidoc.yml from repo root folder
    :param repo_root: A valid folder
    :return: parsed content, `None` otherwise
    '''
    config_filepath = os.path.join(repo_root, '.frangidoc.yml')

    if not os.path.isfile(config_filepath):
        logging.warning("Could not find .frangidoc.yml, aborting")
        return None

    with open(config_filepath, 'r') as f_config:
        config = yaml.load(f_config)

    logging.info("Loaded .frangidoc.yml")

    return config


def _cleanup_folder(folder):

    if os.path.isdir(folder):
        shutil.rmtree(folder, ignore_errors=False, onerror=_handle_remove_read_only)

    os.makedirs(folder)


def _handle_markdown(item, input_filepath, output_filepath):
    '''
    Handles a markdown file found in repo

    If reading in utf-8 raises, falls back to latin-1

    :param item: File
    :param input_filepath: str
    :param output_filepath: str
    '''
    logging.info("Copying markdown file {}".format(item.fullpath))

    try:
        with io.open(input_filepath, 'r', encoding='utf-8') as f_input:
            content = f_input.read()
    except UnicodeDecodeError as e:
        with io.open(input_filepath, 'r', encoding='cp1250') as f_input:
            content = f_input.read()

    with io.open(output_filepath, 'w', encoding='utf-8') as f_output:
        f_output.write(content)


def _handle_python(item, input_filepath, output_filepath):
    '''
    Handles a python file found in repo

    :param item: File
    :param input_filepath: str
    :param output_filepath: str
    '''
    logging.info("Generating markdown for {}".format(item.fullpath))

    content = parser.parse_module(input_filepath)
    markdown = renderer.render_full(content)
    with open(output_filepath, 'w') as f_output:
        f_output.write(markdown)


def generate(repo_root, output_folder, item):
    '''
    Generates markdown files from .py and .md files discovered in `repo_root` folder,
    given a `Folder` or `File` as a starting point

    :param repo_root: str
    :param output_folder: str
    :param item: Folder or File
    '''
    if isinstance(item, discover.File):
        relative_fullpath = Path(*Path(item.fullpath).parts[1:])

        input_filepath = str(Path(repo_root) / relative_fullpath)

        output_filepath = str(Path(output_folder) / relative_fullpath)
        output_filepath = output_filepath.replace('.py', '.md')

        if not os.path.exists(os.path.dirname(output_filepath)):
            os.makedirs(os.path.dirname(output_filepath))

        if os.path.exists(input_filepath):
            if input_filepath.endswith('.md'):
                _handle_markdown(item, input_filepath, output_filepath)

            elif input_filepath.endswith('.py'):
                _handle_python(item, input_filepath, output_filepath)

    # recurse
    if isinstance(item, discover.Folder):
        for subitem in item.files:
            generate(repo_root, output_folder, subitem)

        for subitem in item.folders:
            generate(repo_root, output_folder, subitem)

    return True


def clone_and_generate(repository_url, output_directory, cleanup=True):
    '''
    Clones a repo and generates markdown files

    :param repository_url: str
    :param output_directory: str
    :param cleanup: bool
    :return: bool
    '''
    repo_root = _clone(repository_url)
    if repo_root is None: return False

    config = _load_config(repo_root)
    if config is None: return False

    output_folder = os.path.join(output_directory, config['title'])
    _cleanup_folder(output_folder)

    root_item = discover.discover(repo_root)

    logging.info("Discovered files :")
    for line in discover.format_as_lines(root_item):
        logging.info(line)

    return generate(repo_root, output_folder, root_item)
