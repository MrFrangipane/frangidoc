import logging

from . import git_
from . import generator


def clone_and_generate(repository_url, output_directory, cleanup=True):
    '''
    Clones a repo and generates markdown files

    :param repository_url: str
    :param output_directory: str
    :param cleanup: bool
    :return: bool
    '''
    temp_cloned_folder = git_.clone(repository_url)
    if temp_cloned_folder is None: return False

    generator.generate(temp_cloned_folder, output_directory)

    if cleanup:
        generator.cleanup_folder(temp_cloned_folder)
        logging.info('Temp folder deleted {}'.format(temp_cloned_folder))
