# Frangidoc

Generate markdown from reST based Python docstrings

## Installation

`pip install git+https://github.com/MrFrangipane/docgen.git`

## Usage

FrangiDoc is a command line tool

### By module

You can generate markdown files locally by giving a module name

```bash
python -m frangidoc module <module_name> [-o output_file.md]
```

### With Git

It is possible to generate markdown from a distant repository.

This repo must have a `.frangidoc.yml` file at its root, describing the modules/packages to be parsed :

It is possible to alter the environment before generation.

```yml
title: The Title
environment:
  PYTHONPATH: some/path;some/other/path
  SOME_ENV_VAR: some_value
modules:
  - path/to/module.py
  - path/to/package/__init__.py
```

```bash
python -m frangidoc git <repo_url> <output_dir>
```

Each given module will be parsed and a respective .md file will be created in the given output folder

## Syntax Examples

The following source renders as [this page](demo-output.md)

### Python source

```python
"""
Top module docstring

You can use markdown here
- A bullet
- list
- for example
"""


DISCLAIMER = """If there is a `DISCLAIMER` member in the module, it is put at the end of the Markdown document

It can be multiline and use markdown too

---

Thank you
"""


class OneClass(object):
    """
    Class level docstring
    
    You can use markdown here
    
    | A | Table |
    | --- | --- |
    | For | Example |
    """

    def __init__(self, arg_1, arg_2="default"):
        """
        Constructor docstring
        
        You can use markdown here too
        
        :param arg_1: What is argument 1
        :param arg_2: What is argument 2
        """
        pass

    def a_method(self, argument):
        """
        Some text to describe the purpose of the method
        
        You can use markdown here too
        
        :param argument: What is this argument 
        :return: What the method returns
        """
        pass
    
def some_function(one_param):
    """
    Explain what happens here 
    :param one_param: Argument one **must be** something in bold
    :return: None
    """
    pass
```

### Markdown Output

````markdown
# Demo

Top module docstring

You can use markdown here
- A bullet
- list
- for example

## Class **OneClass**

Class level docstring

You can use markdown here

| A | Table |
| --- | --- |
| For | Example |

### Constructor

```python
OneClass(arg_1, arg_2='default')
```

Constructor docstring

You can use markdown here too


| Argument | Role |
| --- | --- |
| `arg_1` |  What is argument 1 |
| `arg_2` |  What is argument 2 |

### **a_method**

```python
OneClass.a_method(argument)
```

Some text to describe the purpose of the method

You can use markdown here too


| Argument | Role |
| --- | --- |
| `argument` |  What is this argument |
| Returns |  What the method returns |

## Functions


### **some_function**

```python
demo_doc.some_function(one_param)
```

Explain what happens here

| Argument | Role |
| --- | --- |
| `one_param` |  Argument one **must be** something in bold |
| Returns |  None |

---

If there is a `DISCLAIMER` member in the module, it is put at the end of the Markdown document

It can be multiline and use markdown too

---

Thank you
````

## References

Largely inspired from

- https://medium.com/python-pandemonium/python-introspection-with-the-inspect-module-2c85d5aa5a48
- https://gist.github.com/dvirsky/30ffbd3c7d8f37d4831b30671b681c24
- https://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html

Many thanks to their respective authors
