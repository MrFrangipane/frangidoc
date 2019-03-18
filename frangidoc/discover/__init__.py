import re

from .explorer import File, Folder, explore, format_as_lines



def _config_to_regexp(config):
    include = list()
    exclude = list()

    if config is None:
        return include, exclude

    for pattern in config.get('include', list()):
        include.append(re.compile(pattern.replace('*', '.+')))

    for pattern in config.get('exclude', list()):
        exclude.append(re.compile(pattern.replace('*', '.+')))

    return include, exclude


def is_excluded_by_config(config, file):
    '''
    Applies include / exclude patterns from config
    :param config: dict
    :param file: a File object
    :return: bool
    '''
    if config is None:
        return False

    includes, excludes = _config_to_regexp(config)

    for include in includes:
        if include.findall(file.fullpath):

            for exclude in excludes:
                if exclude.findall(file.fullpath):
                    return True

            return False

    if includes:
        return True

    for pattern in excludes:
        if pattern.findall(file.fullpath):
            return True

    return False


def make_exclude_function(config):
    '''
    Makes the exclude function

    Excludes all files that are not `.py` or `.md`, and folders that starts with `__` or `.`
    Excludes / includes files according to config patterns

    :param config: dict (typically, extracted from `.frangidoc.yml`)
    :return: callable
    '''

    def exclude_function(item, type_):
        '''
        Performs a filter on files and folders names

        Excludes all files that are not `.py` or `.md`, and folders that starts with `__` or `.`

        If `True` is returned, the item will be excluded from exploration

        :param item: File or Folder instance
        :param type_: File or Folder class
        :return: bool
        '''
        excluded = True

        if type_ == File and item.name.endswith(('.py', '.md')):
            if not is_excluded_by_config(config, item):
                excluded = False

        elif type_ == Folder and not item.name.startswith(('.', '__')):
            excluded = False

        return excluded

    return exclude_function


def discover(root, config=None):
    '''
    Discovers all python and markdown files in the file tree, according to configuration (include / exclude patterns)

    :param root: path to the root of the file tree, can be a path to a file
    :param config: dict (typically, extracted from `.frangidoc.yml`)
    :return: Folder or File object
    '''
    folder = explore(root, exclude_function=make_exclude_function(config))
    return folder
