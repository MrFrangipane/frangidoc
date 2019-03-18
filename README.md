# Frangidoc

Generate markdown from reST based Python docstrings

## Installation

`pip install frangidoc`

## Usage

FrangiDoc is a command line tool

### With Git

It is possible to generate markdown from a distant repository.

The repo must have a `.frangidoc.yml` file at its root, describing the modules/packages to be parsed :

```bash
python -m frangidoc git <repo_url> <output_dir>
```

All python (.py) and markdown (.md) files are recursively discovered in the repo (given rules in configuration).

Each file will be parsed/copied to a respective .md file in the output folder. _Folders hierarchy is preserved_

for example :

```text
+ <repo root>
    + example
        - __init__.py
        - __main__.py
        - mylib.py
        + mypackage
            - __init__.py
            - module_a.py
            - module_b.py 
    - readme.md 
```

will output :

```text
+ <output folder>
    + example
        - __init__.md
        - __main__.md
        - mylib.md
        + mypackage
            - __init__.md
            - module_a.md
            - module_b.md
    - readme.md 
```

#### Configuration

The `.frangidoc.yml` file contains
- a title
- include patterns (optionnal)
- exclude patterns (optionnal)

```yml
title: The Title
include:
  - some/pattern
  - a/pattern*/with-wildcar
exclude:
  - path/to/file.md
```

If both patterns are specified : **include pattern** prevails on the exclude pattern
    
i.e : `/frangidoc/*` is included, and `tests` is excluded. 
Only files matching `/frangidoc/*` **and not** matching `tests` will be parsed

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
#  Module demo.py

Top module docstring

You can use markdown here
- A bullet
- list
- for example

###  class OneClass

```python
OneClass(self, arg_1, arg_2="default")
```

Class level docstring

You can use markdown here

| A | Table |
| --- | --- |
| For | Example |

####  OneClass.a_method

```python
OneClass.a_method(self, argument)
```

Some text to describe the purpose of the method

You can use markdown here too

| Argument | Role |
|---|---|
| ` argument` |  What is this argument |

**Returns** :  What the method returns

###  some_function

```python
some_function(one_param)
```

Explain what happens here

| Argument | Role |
|---|---|
| ` one_param` |  Argument one **must be** something in bold |

**Returns** :  None
````

## References

Largely inspired from

- https://medium.com/python-pandemonium/python-introspection-with-the-inspect-module-2c85d5aa5a48
- https://gist.github.com/dvirsky/30ffbd3c7d8f37d4831b30671b681c24
- https://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html

Many thanks to their respective authors
