from .explorer import File, Folder, explore, format_as_lines


def _python_and_markdown(name, type_):
    '''
    Performs a filter on files and folders names

    Excludes all files that are not `.py` or `.md`, and folders that starts with `__` or `.`

    :param name: name of the file / folder
    :param type_: File or Folder
    :return: bool
    '''
    if type_ == File and name.endswith(('.py', '.md')):
        return False

    elif type_ == Folder and not name.startswith(('.', '__')):
        return False

    return True


def discover(root):
    '''
    Discovers all python and markdown files in the file tree

    :param root: path to the root of the file tree, can be a path to a file
    :return: Folder or File object
    '''
    folder = explore(root, exclude_function=_python_and_markdown)
    return folder
