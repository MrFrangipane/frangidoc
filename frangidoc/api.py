import os
import sys
import copy
import logging
import tempfile
import generator
import git
import yaml


def generate_and_save(module_name, output_filepath=None):
    module = generator.get_module(module_name)

    if module is None: return

    if output_filepath is None:
        output_filepath = generator.make_output_filepath(module)

    content = generator.get_markdown(module)

    with open(output_filepath, "w+") as content_file:
        content_file.write(content)

    logging.info("Output file written : %s" % output_filepath)


def clone_and_generate(repository_url, output_directory):
    repo_name = os.path.basename(repository_url).replace('.git', '')
    temp_folder = tempfile.mkdtemp(prefix="frangidoc-{}.".format(repo_name))
    config_filepath = os.path.join(temp_folder, '.frangidoc.yml')

    git.Repo.clone_from(repository_url, temp_folder)

    logging.info("Cloned {repo_url} to {temp_folder}".format(repo_url=repository_url, temp_folder=temp_folder))

    if not os.path.isfile(config_filepath):
        logging.warn("Could not find .frangidoc.yml, aborting")
        return False

    with open(config_filepath, 'r') as f_config:
        config = yaml.load(f_config)

    logging.info("Loaded .frangidoc.yml")

    output_folder = os.path.join(output_directory, config['title'])

    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    sys_path_backup = copy.deepcopy(sys.path)
    environment_backup = copy.deepcopy(os.environ)

    environment = config.get('environment', dict())
    for key, value in environment.iteritems():
        value = value.replace(':', ';')
        logging.info("Adding to {} : {}".format(key, value))

        if key.upper() == 'PYTHONPATH':
            for path in value.split(';'):
                sys.path.append(path)
        else:
            os.environ[key] = value

    sys_path_inter_backup = copy.deepcopy(sys.path)

    for module_filepath in config['modules']:
        relative_path, filename = os.path.split(module_filepath)
        path = os.path.join(temp_folder, relative_path)
        name = filename.replace('.py', '')
        output_filename = os.path.join(output_folder, name + '.md')

        sys.path.append(path)
        generate_and_save(name, output_filename)

        sys.path = copy.deepcopy(sys_path_inter_backup)

    sys.path = copy.deepcopy(sys_path_backup)
    os.environ = environment_backup
