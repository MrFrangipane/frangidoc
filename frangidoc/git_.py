import os
import logging
import tempfile

import git


def clone(repository_url):
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
