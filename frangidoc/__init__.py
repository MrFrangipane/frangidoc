"""
Largely inspired from
- https://medium.com/python-pandemonium/python-introspection-with-the-inspect-module-2c85d5aa5a48
- https://gist.github.com/dvirsky/30ffbd3c7d8f37d4831b30671b681c24
Many thanks to their respective authors
"""
import os
import sys
import pydoc


def _module_header(module):
    return [
        '# {module_name}'.format(module_name=module.__name__),
        ''
    ]


def _class_header(class_, parent):
    return [
        '',
        '## Class **{class_name}**'.format(
            parent_name=parent.__name__,
            class_name=class_.__name__
        ),
        ''
    ]


def _functions_header(parent):
    return ['', '## Functions', '']


def _function_header(function_, parent):
    return [
        '',
        '### **{function_name}**'.format(
            function_name=function_.__name__
        ),
        ''
    ]


def _method_header(method, parent):
    if method.__name__ == '__init__':
        return ['', '### Constructor', '']

    return [
        '',
        '### **{function_name}**'.format(
            function_name=method.__name__
        ),
        ''
    ]


def _function_signature(function_, parent):
    args_specs = pydoc.inspect.getargspec(function_)
    args_signature = pydoc.inspect.formatargspec(*args_specs)
    return [
        '```python',
        '{parent_name}.{function_name}{args_signature}'.format(
            parent_name=parent.__name__,
            function_name=function_.__name__,
            args_signature=args_signature
        ),
        '```',
        ''
    ]


def _method_signature(method, parent):
    args, varags, varkw, defaults = pydoc.inspect.getargspec(method)
    args_signature = pydoc.inspect.formatargspec(args[1:], varags, varkw, defaults)

    if method.__name__ == '__init__':
        name = ""
    else:
        name = "." + method.__name__

    return [
        '```python',
        '{parent_name}{function_name}{args_signature}'.format(
            parent_name=parent.__name__,
            function_name=name,
            args_signature=args_signature
        ),
        '```',
        ''
    ]


def _separator():
    return [
        '',
        '***',
        ''
    ]


def _is_function_or_method(object_):
    return pydoc.inspect.isfunction(object_) or pydoc.inspect.ismethod(object_)


def _format_docstring(docstring):
    output = list()
    lines = docstring.split('\n')

    inside_caption = True

    caption = list()
    arguments = list()

    for line in lines:
        if line.startswith(':'):
            inside_caption = False
            _, arg, role = line.split(':')

            if arg == "return":
                arg = "Returns"
            else:
                arg = "`" + arg.replace("param ", "") + "`"
            arguments.append([arg, role])

        elif not inside_caption:
            arguments[-1][1] += " " + line

        if inside_caption:
            caption.append(line)

    caption = "\n".join(caption)

    output.append(caption)
    output.append("")
    output.append("| Argument | Role |")
    output.append("| --- | --- |")

    for argument in arguments:
        output.append("| %s | %s |" % (argument[0], argument[1]))

    return output


def genereate(module_name):
    try:
        working_dir = os.getcwd()
        if working_dir not in sys.path:
            sys.path.append(working_dir)

        module = pydoc.safeimport(module_name)

        if module is None:
            print("Module not found")

        return get_markdown(module)

    except pydoc.ErrorDuringImport:
        print("Error while trying to import %s" % module_name)


def generate_and_save(module_name, output_filepath):
    content = genereate(module_name)

    if content is None: return

    with open(output_filepath, "w+") as content_file:
        content_file.write(content)


def get_markdown(module):
    output = _module_header(module)

    doc = pydoc.inspect.getdoc(module)
    if doc is not None:
        output.append(doc)

    output.extend(get_classes(module))

    functions = get_functions(module)

    if functions:
        output.extend(_functions_header(module))
        output.extend(functions)

    if hasattr(module, "DISCLAIMER"):
        output.extend([
            '',
            '---',
            '',
            module.DISCLAIMER
        ])

    return "\n".join([str(item) for item in output])


def get_functions(item):
    output = list()

    for function_name, function in pydoc.inspect.getmembers(item, _is_function_or_method):
        if function_name.startswith("_") and function_name != '__init__': continue

        output.extend(_function_header(function, parent=item))
        output.extend(_function_signature(function, parent=item))

        docstring = pydoc.inspect.getdoc(function)
        if docstring is not None:
            output.extend(_format_docstring(docstring))

    return output


def get_methods(class_):
    output = list()

    for method_name, method in pydoc.inspect.getmembers(class_, _is_function_or_method):
        if method_name.startswith("_") and method_name != '__init__': continue

        output.extend(_method_header(method, parent=class_))
        output.extend(_method_signature(method, parent=class_))

        docstring = pydoc.inspect.getdoc(method)
        if docstring is not None:
            output.extend(_format_docstring(docstring))

    return output


def get_classes(item):
    output = list()

    for class_name, class_ in pydoc.inspect.getmembers(item, pydoc.inspect.isclass):
        if class_name.startswith("_"): continue

        output.extend(_class_header(class_, parent=item))

        doc = pydoc.inspect.getdoc(class_)
        if doc is not None:
            output.append(doc)

        output.extend(get_methods(class_))
        output.extend(get_classes(class_))

    return output


if __name__ == '__main__':
    generate_and_save("tubemetadata2", os.getcwd() + "/test.md")