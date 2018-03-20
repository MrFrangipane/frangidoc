# Frangidoc

Generate markdown from Python sources (reST based)

## Installation

`pip install git+https://github.com/MrFrangipane/docgen.git`

## Usage

```bash
python -m frangidoc -m <module_name> -o /path/to/output/file.md
```

## Example

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

Many thanks to their respective authors
