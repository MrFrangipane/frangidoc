from frangidoc.objects import *
from frangidoc.parser import parse_module

_MODULE = """{title} Module `{name}`

{docstring}

{content}
"""

_CLASS = """{title} class `{name}`

```python
{signature}
```

{docstring}

{content}
"""


_FUNCTION = """{title} function `{name}`

```python
{signature}
```

{docstring}
"""


def _title(level):
    """Markdown title"""
    return '#' * (level + 1) + ' '


def _render_module(module, parent, level):
    """Renders a module to Markdown"""
    title = _title(level)
    name = module.name
    docstring = module.docstring if module.docstring else ''
    content = '\n'.join(render(item, None, level + 1) for item in module.content)

    return _MODULE.format(
        title=title,
        name=name,
        docstring=docstring,
        content=content
    ).strip()


def _render_class(class_, parent, level):
    """Renders a class to Markdown"""
    title = _title(level)
    name = class_.name
    signature = class_
    docstring = class_.docstring if class_.docstring else ''
    content = '\n'.join(render(item, class_, level + 1) for item in class_.content)

    return _CLASS.format(
        title=title,
        name=name,
        signature=signature,
        docstring=docstring,
        content=content
    ).strip()


def _render_function(function, parent, level):
    title = _title(level)

    docstring = function.docstring if function.docstring else ''
    if parent is not None:
        name = parent.name + '.' + str(function)
        signature = parent.name + '.' + str(function)
    else:
        name = function
        signature = function

    return _FUNCTION.format(
        title=title,
        name=name,
        signature=signature,
        docstring=docstring
    )


def render(item, parent=None, level=0):
    if isinstance(item, Module):
        return _render_module(item, parent, level)

    if isinstance(item, Class):
        return _render_class(item, parent, level)

    if isinstance(item, Function):
        return _render_function(item, parent, level)


if __name__ == '__main__':

    module = parse_module('R:/users/v.moriceau/blender-lab/libs/nomenclature/texture_filepath.py')
    page = render(module)

    print(page)
