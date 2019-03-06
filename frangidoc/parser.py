import os.path
import token, tokenize
from objects import *


class Token(object):
    """
    Holds Token information
    """
    def __init__(self, infos=None):
        if infos:
            self.type = infos[0]
            self.text = infos[1]
            self.s_line, self.s_col = infos[2]
            self.e_line, self.e_col = infos[3]
            self.line_text = infos[4]
            # print(self)
        else:
            self.type = None
            self.type = None
            self.text = None
            self.s_line = None
            self.s_col = None
            self.e_line = None
            self.e_col = None
            self.line_text = None

    def __str__(self):
        return "%10s %-14s %-20r %r" % (
            tokenize.tok_name.get(self.type, self.type),
            "%d.%d-%d.%d" % (self.s_line, self.s_col, self.e_line, self.e_col),
            self.text, self.line_text
        )

    def __repr__(self):
        return '<Token({})>'.format(str(self))


def _strip(text, quotes=False):
    """
    Strips indentation and quotes
    """
    text_ = ""

    for line in text.splitlines():
        line_ = line.strip()
        if quotes:
            line_ = line_.strip('"').strip("'")

        text_ += line_ + '\n'

    return text_


def _parse_class_parents(tokens):
    parents = list()
    parent = list()

    for infos in tokens:
        new_token = Token(infos)

        if new_token.type == token.NAME:
            parent.append(new_token.text)

        if new_token.type == token.OP and new_token.text in (',', ')'):
            parents.append('.'.join(parent))
            parent = list()

        if new_token.type == token.OP and new_token.text == ':':
            break

    return parents


def parse_arguments(tokens):
    arguments = list()
    argument = Argument()

    for infos in tokens: # TODO : _parse_value to deal with arg=[None, 1] for example
        new_token = Token(infos)

        if new_token.type == token.NAME and not argument.name:
            argument.name = new_token.text

        elif new_token.type in (token.NUMBER, token.STRING, token.NAME) and argument.name:
            argument.default = new_token.text

        elif new_token.type == token.OP and new_token.text in (',', ')'):
            arguments.append(argument)
            argument = Argument()

        if new_token.type == token.OP and new_token.text == ':':
            break

    return arguments


def _parse_def(tokens):
    indent = None
    previous = Token()
    function_ = Function()


    for infos in tokens:
        new_token = Token(infos)

        if new_token.type == token.STRING and previous.type == token.INDENT:
            function_.docstring = Docstring(_strip(new_token.line_text, quotes=True))

        if new_token.type == token.INDENT and indent is None:
            indent = new_token.e_col

        if new_token.type == token.NAME and not function_.name:
            function_.name = new_token.text
            function_.arguments = parse_arguments(tokens)

        if new_token.type == token.DEDENT and new_token.e_col <= indent - 4:
            return function_

        previous = new_token


def _parse_class(tokens):
    indent = None
    new_token = Token(tokens.next())
    previous = new_token

    new_class = Class()
    new_class.name = new_token.text
    new_class.parents = _parse_class_parents(tokens)

    for infos in tokens:
        new_token = Token(infos)

        if new_token.type == token.INDENT and indent is None:
            indent = new_token.e_col

        if new_token.type == token.STRING and previous.type == token.INDENT:
            new_class.docstring = Docstring(_strip(new_token.line_text, quotes=True))

        if new_token.type == token.NAME and new_token.text == 'def':
            function_ = _parse_def(tokens)
            if function_.name == '__init__':
                new_class.constructor = function_
            else:
                new_class.content.append(function_)

        if new_token.type == token.DEDENT and new_token.e_col <= indent - 4:
            return new_class

        previous = new_token


def _parse_module(tokens, module):
    previous_type = token.INDENT

    for infos in tokens:
        new_token = Token(infos)

        if previous_type == token.INDENT and new_token.type == token.STRING:
            module.docstring = Docstring(_strip(new_token.line_text, quotes=True))

        if new_token.type == token.NAME and new_token.text == 'class':
            new_class = _parse_class(tokens)
            module.content.append(new_class)

        if new_token.type == token.NAME and new_token.text == 'def':
            new_function = _parse_def(tokens)
            module.content.append(new_function)

        previous_type = new_token.type

    return module


def parse_module(filepath):
    module = Module()
    module.name = os.path.basename(filepath)

    with open(filepath, 'r') as f_source:
        tokens = tokenize.generate_tokens(f_source.readline)
        module = _parse_module(tokens, module)

    return module
