class Docstring(object):
    def __init__(self):
        self.content = None

    def __repr__(self):
        return "<Docstring {}>".format(self.content.splitlines()[0])


class Object(object):
    def __init__(self):
        self.name = None
        self.signature = None
        self.docstring = None
        self.content = None
        self.indentation = None

    def __repr__(self):
        return "<{} '{}'>".format(self.__class__.__name__, self.name)


class Module(Object):
    pass


class Class(Object):
    pass


class Constructor(Object):
    pass


class Function(Object):
    pass


class Method(Object):
    pass


class _Line(object):
    """Stores stripped line text, indentation as int, number as int"""
    def __init__(self, text_line):
        self.text = text_line.strip()
        self.number = 0
        self.indentation = len(text_line) - len(text_line.lstrip(' '))

    def __repr__(self):
        return "<Line({:04d}:{} indent={:02d})>".format(
            self.number,
            self.text,
            self.indentation
        )

    @staticmethod
    def from_raw_lines(text_lines):
        """
        Parses all the text lines, and determines indentation's space count
        :param text_lines: list of raw text lines
        :return:  list of _Line objects
        """
        space_count = 0
        lines = list()

        for line_number, text_line in enumerate(text_lines):
            line = _Line(text_line)
            line.number = line_number
            if line.indentation > space_count and space_count == 0:
                space_count = line.indentation

            lines.append(line)

        for line in lines:
            line.indentation = line.indentation // space_count if space_count else 0

        return lines


class Token(object):
    BEGIN = 'TOKEN_BEGIN'
    END = 'TOKEN_END'
    INDENT_BEGIN = 'TOKEN_INDENT_BEGIN'
    INDENT_END = 'TOKEN_INDENT_END'
    DOCSTRING_SIMPLE = 'TOKEN_DOCSTRING_SIMPLE'
    DOCSTRING_DOUBLE = 'TOKEN_DOCSTRING_DOUBLE'
    DECORATOR = 'TOKEN_DECORATOR'
    CLASS = 'TOKEN_CLASS'
    INIT = 'TOKEN_INIT'
    DEF = 'TOKEN_DEF'

    EXPECTED = {
        BEGIN: (DOCSTRING_SIMPLE, DOCSTRING_DOUBLE, CLASS, DEF, END)
    }


class Parser(object):

    def __init__(self, text_lines):
        self.lines = _Line.from_raw_lines(text_lines)
        if self.lines:
            self._index = 0
            self._line = self.lines[0]
            self._token = Token.BEGIN
            self._indentation = 0
        self.result = None

    #
    # Navigation
    def consume(self):
        """
        Updates indentation and line
        """
        if self._index > 0:
            self._indentation = self._line.indentation

        self._index += 1

        if self._index > len(self.lines) - 1:
            return False

        self._line = self.lines[self._index]
        return True

    #
    # Parsing
    def token(self, line, current_indentation):
        """
        Returns the corresponding token for given line at current_index
        :param line: _Line object
        :param current_indentation: level of indentation before given _Line
        :param current_index: index of given
        :return:
        """
        if line.indentation > current_indentation:
            return Token.INDENT_BEGIN

        elif line.indentation < current_indentation:
            return Token.INDENT_END

        if line.content.startswith('"""'):
            return Token.DOCSTRING_DOUBLE

        if line.content.startswith("'''"):
            return Token.DOCSTRING_SIMPLE

        if line.content.startswith('@'):
            return Token.DECORATOR

        if line.content.startswith('class '):
            return Token.CLASS

        if line.content.replace(' ', '').startswith('def__init__'):
            return Token.INIT

        if line.content.startswith('def '):
            return Token.DEF

        if line.number == len(self.lines) - 1:  # todo : ??
            return Token.END

    def next_token(self):
        while True:
            if self._line.text:
                break
            if not self.consume():
                break

        print(self._line)

    def parse(self):
        """
        Parses the given text_lines
        :return: Objects, None otherwise
        """
        if self.lines:
            self.next_token()

        return self.result
