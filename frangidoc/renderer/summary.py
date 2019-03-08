from frangidoc.objects import *


_INDENT = "    "
_BULLET_MODULE = "*"
_BULLET_CLASS = "+"
_BULLET_FUNCTION = "-"


def _render_module(module, parent, level):
    """Renders a module summary to Markdown"""
    summary = ["{}{} {}".format(_INDENT *level, _BULLET_MODULE, module.name)]
    for item in module.content:
        summary.append(render(item, module, level + 1))

    return '\n'.join(summary)


def _render_class(class_, parent, level):
    """Renders a class summary to Markdown"""
    if class_.parents:
        title = '{} : {}'.format(class_, ', '.join(class_.parents))
    else:
        title = class_

    summary = ["{}{} class {}".format(_INDENT * level, _BULLET_CLASS, title)]

    for item in class_.content:
        summary.append(render(item, class_, level + 1))

    return '\n'.join(summary)

def _render_function(function, parent, level):
    return "{}{} {}".format(_INDENT * level, _BULLET_FUNCTION, function)


def render(item, parent=None, level=0):
    if isinstance(item, Module):
        return _render_module(item, parent, level)

    if isinstance(item, Class):
        return _render_class(item, parent, level)

    if isinstance(item, Function):
        return _render_function(item, parent, level)
