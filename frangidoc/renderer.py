from frangidoc.objects import *


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


def _render_docstring(docstring, parent, level):
    lines = docstring.content.splitlines()
    table = ['| Argument | Role |', '|---|---|']
    output = list()
    return_info = list()

    for line in lines:
        if line.startswith(':param '):
            name = line[6:].split(':')[0]
            info = ':'.join(line[6:].split(':')[1:])

            table.append('| `{}` | {} |'.format(name, info))

        elif line.startswith(':return:'):
            info = line[8:]
            if info:
                return_info.append('')
                return_info.append('**Returns** : {}'.format(info))

        else:
            output.append(line)

    if len(table) > 2:
        return '\n'.join(output + table + return_info)

    return '\n'.join(output + return_info)


def _title(level):
    """Markdown title"""
    return '#' * (level + 1) + ' '


def _render_module(module, parent, level):
    """Renders a module to Markdown"""
    title = _title(level)
    name = module.name
    docstring = render(module.docstring) if module.docstring else ''
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

    docstring = render(function.docstring) if function.docstring else ''
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

    if isinstance(item, Docstring):
        return _render_docstring(item, parent, level)
