import logging
from frangidoc.objects import *


_MODULE = """{title} Module {name}

{docstring}

{content}
"""

_CLASS = """{title} class {name}

```python
{signature}
```

{docstring}

{content}
"""

_METHOD = """{title} {class_name}.{name}

```python
{signature}
```

{docstring}
"""

_FUNCTION = """{title} {name}

```python
{signature}
```

{docstring}
"""


def _render_docstring(docstring, parent, level):
    logging.info('Rendering docstring : {}'.format(parent.name))
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
    logging.info('Rendering module    : {}'.format(module.name))
    title = _title(level)
    name = module.name
    docstring = render(module.docstring, module) if module.docstring else ''
    content = '\n'.join(render(item, None, level + 2) for item in module.content)

    logging.info('Rendering done      : {}'.format(module.name))

    return _MODULE.format(
        title=title,
        name=name,
        docstring=docstring,
        content=content
    ).strip()


def _render_class(class_, parent, level):
    """Renders a class to Markdown"""
    logging.info('Rendering class     : {}'.format(class_.name))
    title = _title(level)
    name = class_.name
    signature = class_
    docstring = class_.docstring if class_.docstring else ''
    content = '\n'.join(render(item, class_, level + 1) for item in class_.content)

    logging.info('Rendering done      : {}'.format(class_.name))

    return _CLASS.format(
        title=title,
        name=name,
        signature=signature,
        docstring=docstring,
        content=content
    ).strip()


def _render_function(function, parent, level):
    logging.info('Rendering function  : {}'.format(function.name))
    title = _title(level)
    docstring = render(function.docstring, function) if function.docstring else ''

    if isinstance(parent, Class):
        class_name = parent.name
        name =  function.name
        signature = parent.name + '.' + str(function)

        return _METHOD.format(
            title=title,
            class_name=class_name,
            name=name,
            signature=signature,
            docstring=docstring
        )

    name = function.name
    signature = str(function)

    return _FUNCTION.format(
        title=title,
        name=name,
        signature=signature,
        docstring=docstring
    )


def render(item, parent=None, level=0):
    if isinstance(item, Module):
        return '\n' + _render_module(item, parent, level)

    if isinstance(item, Class):
        return '\n' + _render_class(item, parent, level)

    if isinstance(item, Function):
        return '\n' + _render_function(item, parent, level)

    if isinstance(item, Docstring):
        return '\n' + _render_docstring(item, parent, level)
