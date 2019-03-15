import os

_INDENT = '    '


class File(object):
    '''
    Represents a file

    Has a `.name`
    '''
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    @property
    def fullpath(self):
        if self.parent is None:
            return self.name

        return os.path.join(self.parent.fullpath, self.name).replace('\\', '/')

    def __repr__(self):
        return "<File('{}')>".format(self.name)


class Folder(object):
    '''
    Represents a folder

    Has a `.name` and a list of files : `.files`
    '''
    def __init__(self, name, files=None, folders=None, parent=None):
        if files is None: files = list()
        if folders is None: folders = list()
        self.name = name
        self.files = files
        self.folders = folders
        self.parent = None

    @property
    def fullpath(self):
        if self.parent is None:
            return self.name

        return os.path.join(self.parent.fullpath, self.name).replace('\\', '/')

    def __repr__(self):
        return "<Folder('{}' {} file(s), {} folder(s))>".format(self.name, len(self.files), len(self.folders))


def _walk_folder(path_, exclude_function):
    '''
    Recursively explores a Folder, given its root path and an exclude function
    
    :param path_: str
    :param exclude_function: function called on each element (File or Folder)
    :return: Folder object
    '''
    name = os.path.basename(os.path.abspath(path_))
    here = Folder(name)
    if exclude_function(here.name, Folder):
        return None

    for item_name in sorted(os.listdir(path_)):
        item_path = os.path.join(path_, item_name)

        item = explore(item_path, exclude_function)
        if item is None: continue

        item.parent = here

        if isinstance(item, File):
            here.files.append(item)

        if isinstance(item, Folder):
            here.folders.append(item)

    return here


def explore(path_, exclude_function=lambda name, type_: False):
    '''
    Recursively explores given path or filepath

    :param path_: str
    :return: File or a Folder
    '''
    if os.path.isfile(path_):
        file_ = File(os.path.basename(path_))
        if not exclude_function(file_.name, File):
            return file_

    if os.path.isdir(path_):
        return _walk_folder(path_, exclude_function)


def format_as_lines(item, _indent=0):
    '''
    Pretty prints a tree of Folder / Files objects
    :param item: a File or Folder
    :return: None
    '''
    lines = list()

    if isinstance(item, Folder):
        lines.append('{}+ {}'.format(_INDENT * _indent, item.name))

        for file in item.files:
            lines += format_as_lines(file, _indent + 1)

        for folder in item.folders:
            lines += format_as_lines(folder, _indent + 1)

    if isinstance(item, File):
        lines.append('{}- {}'.format(_INDENT * _indent, item.name))

    return lines
