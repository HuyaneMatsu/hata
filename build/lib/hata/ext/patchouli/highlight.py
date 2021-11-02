# -*- coding: utf-8 -*-
"""
The token types for coloring are the following:

+-----------------------------------------------+-------+-------------------------------------------+
| Respective name                               | Value | Parent's respective name                  |
+===============================================+=======+===========================================+
| TOKEN_TYPE_ALL                                |   0   | N/A                                       |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_SPACE                              |   1   | TOKEN_TYPE_ALL                            |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_LINEBREAK                          |   2   | TOKEN_TYPE_ALL                            |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_NON_SPACE                          |   3   | TOKEN_TYPE_ALL                            |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_NON_SPACE_UNIDENTIFIED             |   4   | TOKEN_TYPE_NON_SPACE                      |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_COMMENT                            |   5   | TOKEN_TYPE_ALL                            |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_LINEBREAK_ESCAPED                  |   6   | TOKEN_TYPE_LINEBREAK                      |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_CONSTANT                           | 100   | TOKEN_TYPE_NON_SPACE                      |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_NUMERIC                            | 110   | TOKEN_TYPE_CONSTANT                       |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_NUMERIC_FLOAT                      | 111   | TOKEN_TYPE_NUMERIC                        |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_NUMERIC_FLOAT_COMPLEX              | 112   | TOKEN_TYPE_NUMERIC_FLOAT                  |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_NUMERIC_INTEGER                    | 113   | TOKEN_TYPE_NUMERIC                        |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_NUMERIC_INTEGER_HEXADECIMAL        | 114   | TOKEN_TYPE_NUMERIC_INTEGER                |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_NUMERIC_INTEGER_DECIMAL            | 115   | TOKEN_TYPE_NUMERIC_INTEGER                |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_NUMERIC_INTEGER_OCTAL              | 116   | TOKEN_TYPE_NUMERIC_INTEGER                |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_NUMERIC_INTEGER_BINARY             | 117   | TOKEN_TYPE_NUMERIC_INTEGER                |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_STRING                             | 120   | TOKEN_TYPE_CONSTANT                       |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_STRING_BINARY                      | 121   | TOKEN_TYPE_STRING                         |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_STRING_UNICODE                     | 122   | TOKEN_TYPE_STRING                         |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_STRING_UNICODE_FORMAT              | 123   | TOKEN_TYPE_STRING_UNICODE                 |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_STRING_UNICODE_FORMAT_MARK         | 124   | TOKEN_TYPE_STRING_UNICODE_FORMAT          |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_STRING_UNICODE_FORMAT_CODE         | 125   | TOKEN_TYPE_STRING_UNICODE_FORMAT          |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_STRING_UNICODE_FORMAT_POSTFIX      | 126   | TOKEN_TYPE_STRING_UNICODE_FORMAT          |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_IDENTIFIER                         | 200   | TOKEN_TYPE_NON_SPACE                      |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_IDENTIFIER_VARIABLE                | 201   | TOKEN_TYPE_IDENTIFIER                     |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_IDENTIFIER_ATTRIBUTE               | 202   | TOKEN_TYPE_IDENTIFIER                     |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_IDENTIFIER_KEYWORD                 | 210   | TOKEN_TYPE_IDENTIFIER                     |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_IDENTIFIER_BUILTIN                 | 221   | TOKEN_TYPE_IDENTIFIER                     |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_IDENTIFIER_BUILTIN_VARIABLE        | 222   | TOKEN_TYPE_IDENTIFIER_BUILTIN             |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_IDENTIFIER_BUILTIN_CONSTANT        | 223   | TOKEN_TYPE_IDENTIFIER_BUILTIN             |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_IDENTIFIER_BUILTIN_EXCEPTION       | 224   | TOKEN_TYPE_IDENTIFIER_BUILTIN             |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_IDENTIFIER_MAGIC                   | 230   | TOKEN_TYPE_IDENTIFIER                     |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_IDENTIFIER_MAGIC_FUNCTION          | 231   | TOKEN_TYPE_IDENTIFIER_MAGIC               |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_IDENTIFIER_MAGIC_VARIABLE          | 232   | TOKEN_TYPE_IDENTIFIER_MAGIC               |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_SPECIAL                            | 300   | TOKEN_TYPE_NON_SPACE                      |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_SPECIAL_OPERATOR                   | 301   | TOKEN_TYPE_SPECIAL                        |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_SPECIAL_OPERATOR_ATTRIBUTE         | 302   | TOKEN_TYPE_SPECIAL_OPERATOR               |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_SPECIAL_PUNCTUATION                | 303   | TOKEN_TYPE_SPECIAL                        |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_SPECIAL_OPERATOR_WORD              | 304   | TOKEN_TYPE_SPECIAL_OPERATOR               |
+-----------------------------------------------+-------+-------------------------------------------+
| TOKEN_TYPE_SPECIAL_CONSOLE_PREFIX             | 305   | TOKEN_TYPE_SPECIAL                        |
+-----------------------------------------------+-------+-------------------------------------------+

To set a html class to a token, do:

```py
set_highlight_html_class(token_type_identifier, html_class_name)
```

Testing
-------
To check highlights set some colors down and enjoy.

```py
TUMMY_REPR_ACCURACY = 2

class CakeEater:
    __slots__ = ('tummy_size', 'type')
    
    def __init__(self, type_, tummy_size):
        self.type = type_
        self.tummy_size = tummy_size
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.type!r}, {self.tummy_size:.{TUMMY_REPR_ACCURACY}f})'
    
    async def throw(self):
        # No one would ever expect this.
        raise StopIteration()

print(CakeEater('dream eater', 2.111))
```
"""
__all__ = ('set_highlight_html_class', )

import re
from html import escape as html_escape

PYTHON_IDENTIFIERS = {'python', 'py', 'sage', 'python3', 'py3'}

COMPLEX_RP = re.compile('((?:\d(?:_?\d)*\.\d(?:_?\d)*|\d(?:_?\d)*\.|\.\d(?:_?\d)*)(?:[eE][+-]?\d(?:_?\d)*)?[jJ])')
FLOAT_RP = re.compile('((?:\d(?:_?\d)*\.\d(?:_?\d)*|\d(?:_?\d)*\.|\.\d(?:_?\d)*)(?:[eE][+-]?\d(?:_?\d)*)?)')
INTEGER_HEXADECIMAL_RP = re.compile('(0[xX](?:_?[0-9a-fA-F])+)')
INTEGER_DECIMAL_RP = re.compile('(\d(?:_?\d)*)')
INTEGER_OCTAL_RP = re.compile('(0[oO](?:_?[0-7])+)')
INTEGER_BINARY_RP = re.compile('(0[bB](?:_?[01])+)')
IDENTIFIER_RP = re.compile('([a-zA-Z_][a-zA-Z_0-9]*)')

ATTRIBUTE_ACCESS_OPERATOR = '.'
KEYWORD_ELLIPSIS = '...'
ESCAPE = '\\'

BUILTIN_CONSTANTS = {'Ellipsis', 'False', 'None', 'NotImplemented', 'True', KEYWORD_ELLIPSIS}

KEYWORDS = {'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
    'finally', 'for', 'from', 'global', 'if', 'import', 'lambda', 'nonlocal', 'pass', 'raise', 'return', 'try',
    'while', 'with', 'yield'}

BUILTIN_VARIABLES = {'__import__', 'abs', 'all', 'any', 'bin', 'bool', 'bytearray', 'bytes', 'chr', 'classmethod',
    'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'filter', 'float', 'format',
    'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass',
    'iter', 'len', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow',
    'print', 'property', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod',
    'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip', }

BUILTIN_EXCEPTIONS = {'ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BufferError',
    'BytesWarning', 'DeprecationWarning', 'EOFError', 'EnvironmentError', 'Exception', 'FloatingPointError',
    'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError',
    'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'NameError', 'NotImplementedError', 'OSError',
    'OverflowError', 'PendingDeprecationWarning', 'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning',
    'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'TypeError',
    'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError',
    'UnicodeWarning', 'UserWarning', 'ValueError', 'VMSError', 'Warning', 'WindowsError', 'ZeroDivisionError',
    'BlockingIOError', 'ChildProcessError', 'ConnectionError', 'BrokenPipeError', 'ConnectionAbortedError',
    'ConnectionRefusedError', 'ConnectionResetError', 'FileExistsError', 'FileNotFoundError', 'InterruptedError',
    'IsADirectoryError', 'NotADirectoryError', 'PermissionError', 'ProcessLookupError', 'TimeoutError',
    'StopAsyncIteration', 'ModuleNotFoundError', 'RecursionError', }

MAGIC_FUNCTIONS = {'__abs__', '__add__', '__aenter__', '__aexit__', '__aiter__', '__and__', '__anext__', '__await__',
    '__bool__', '__bytes__', '__call__', '__complex__', '__contains__', '__del__', '__delattr__', '__delete__',
    '__delitem__', '__dir__', '__divmod__', '__enter__', '__eq__', '__exit__', '__float__', '__floordiv__',
    '__format__', '__ge__', '__get__', '__getattr__', '__getattribute__', '__getitem__', '__gt__', '__hash__',
    '__iadd__', '__iand__', '__ifloordiv__', '__ilshift__', '__imatmul__', '__imod__', '__imul__', '__index__',
    '__init__', '__instancecheck__', '__int__', '__invert__', '__ior__', '__ipow__', '__irshift__', '__isub__',
    '__iter__', '__itruediv__', '__ixor__', '__le__', '__len__', '__length_hint__', '__lshift__', '__lt__',
    '__matmul__', '__missing__', '__mod__', '__mul__', '__ne__', '__neg__', '__new__', '__next__', '__or__', '__pos__',
    '__pow__', '__prepare__', '__radd__', '__rand__', '__rdivmod__', '__repr__', '__reversed__', '__rfloordiv__',
    '__rlshift__', '__rmatmul__', '__rmod__', '__rmul__', '__ror__', '__round__', '__rpow__', '__rrshift__',
    '__rshift__', '__rsub__', '__rtruediv__', '__rxor__', '__set__', '__setattr__', '__setitem__', '__str__',
    '__sub__', '__subclasscheck__', '__truediv__', '__xor__', }

MAGIC_VARIABLES = {'__annotations__', '__bases__', '__class__', '__closure__', '__code__', '__defaults__', '__dict__',
    '__doc__', '__file__', '__func__', '__globals__', '__kwdefaults__', '__module__', '__mro__', '__name__',
    '__objclass__', '__qualname__', '__self__', '__slots__', '__weakref__'}

PUNCTUATIONS = {'(', ')', ',', ':', ';', '[', ']', '{', '}'}
OPERATOR_WORDS = {'and', 'in', 'is', 'not', 'or'}

OPERATORS = {'!=', '%', '%=', '&', '&=', '*', '**', '**=', '*=', '+', '+=', '-', '-=', '->', '.', '...', '/', '//',
    '//=', '/=', '<', '<<', '<<=', '<=', '=', '==', '>', '>=', '>>', '>>=', '@', '@=', '\\', '^', '^=', '|', '|='}

STRING_STARTER_RP = re.compile('(r[fb]?|[fb]r?|b|f)?(\'{3}|\"{3}|\'|\")')
STRING_END_SINGLE_RP = re.compile('(.*?[^\\\\])\'|\'')
STRING_END_DOUBLE_RP = re.compile('(.*?[^\\\\])\"|\'')
STRING_MULTI_LINE_END_SINGLE_RP = re.compile('(.*?[^\\\\])\'\'\'|\'\'\'')
STRING_MULTI_LINE_END_DOUBLE_RP = re.compile('(.*?[^\\\\])\"\"\"|\"\"\"')

SPACE_MATCH_RP = re.compile('([ \t]+)')

TOKEN_TYPE_NODES = {}

FORMAT_STRING_MATCH_STRING = re.compile('(.*?)(\{\{|\{|\n|\}\}|\})')

CONSOLE_PREFIX_RP = re.compile('(>>>>?)( [ \t]*)')

FORMAT_STRING_POSTFIX_RP = re.compile('(![sraSRA])\}')

class WordNode:
    """
    A words's character node when building regex.
    
    Attributes
    ----------
    character : `str`
        The represented character by the node.
    is_final : `bool`
        Whether the node is the end of a word.
    nodes : `dict` of (`str`, ``WordNode``) items
        Sub nodes branching out.
    parent : `None` or ``WordNode``
        The parent node.
    """
    __slots__ = ('character', 'is_final', 'nodes', 'parent')
    def __new__(cls, character, is_final, parent):
        """
        Creates a new ``WordNode`` with the given `character`.
        
        Parameters
        ----------
        character : `str`
            The character of the node.
        is_final : `bool`
            Whether the node is the end of a word.
        """
        self = object.__new__(cls)
        self.character = character
        self.nodes = None
        self.is_final = is_final
        self.parent = parent
        return self
    
    def __repr__(self):
        """Returns the word node's representation."""
        result = ['<', self.__class__.__name__, ' of ', repr(self.character)]
        if self.is_final:
            result.append(' (final)')
        
        nodes = self.nodes
        if (nodes is not None):
            result.append(' nodes=')
            result.append(repr(nodes))
        
        result.append('>')
        
        return ''.join(result)
    
    def add_node(self, characters, character_index):
        """
        Adds a sub-node to the node.
        
        Attributes
        ----------
        characters : `list` of `str`
            A list of characters to add as nodes.
        character_index : `int`
            The character's index to use from `characters`.
        """
        character = characters[character_index]
        character_index += 1
        if len(characters) == character_index:
            is_final = True
        else:
            is_final = False
        
        nodes = self.nodes
        if (nodes is None):
            self.nodes = nodes = {}
        
        try:
            node = nodes[character]
        except KeyError:
            node = WordNode(character, is_final, self)
            self.nodes[character] = node
        else:
            if is_final:
                node.is_final = True
        
        if (not is_final):
            node.add_node(characters, character_index)
    
    def _match_index(self, string, index):
        """
        Matches the pattern from the given string.
        
        Parameters
        ----------
        string : `str`
            The string to match from.
        index : `int`
            The starter index to match since. Defaults to `0`.
        
        Returns
        -------
        matched_count : `int`
            The amount of matched characters.
            
            `-1` is returned of nothing is matched.
        """
        if len(string) > index:
            character = string[index]
            
            nodes = self.nodes
            if (nodes is not None):
                try:
                    node = nodes[character]
                except KeyError:
                    pass
                else:
                    match_index = node._match_index(string, index+1)
                    if match_index != -1:
                        return match_index+1
        
        if self.is_final:
            return 1
        
        return -1
    
    def match(self, string, index=0):
        """
        Matches pattern from the given string.
        
        Parameters
        ----------
        string : `str`
            The string to match from.
        index : `int`, Optional
            The starter index to match since. Defaults to `0`.
        
        Returns
        -------
        matched : `None` or `str`
            The matched string, if any.
        """
        if len(string) > index:
            character = string[index]
            
            nodes = self.nodes
            if (nodes is not None):
                try:
                    node = nodes[character]
                except KeyError:
                    pass
                else:
                    match_index = node._match_index(string, index+1)
                    if match_index != -1:
                        return string[index:index+match_index]
        
        if self.is_final:
            return ''
        
        return None


def create_word_pattern(words):
    """
    Creates 1 regex pattern from many words.
    
    Parameters
    ----------
    words : `iterable` of `str`
        The words to create regex pattern from.
    
    Returns
    -------
    regex_pattern : ``WordNode``
        The generated pattern.
    """
    word_node = WordNode('', False, None)
    for word in words:
        if word:
            word_node.add_node(list(word), 0)
        else:
            word_node.is_final = True
    
    return word_node

PUNCTUATION_WP = create_word_pattern(PUNCTUATIONS)
OPERATOR_WP = create_word_pattern(OPERATORS)


class TokenTypeNode:
    """
    Represents a token class node for specified token types.
    
    Attributes
    ----------
    id : `int`
        The node's identifier.
    html_class : `None` or `str`
        The token node's type.
    is_class_direct : `bool`
        Whether ``.type`` is set directly or is inherited.
    nodes : `None` or `dict` of (`int`, ``TokenTypeNode``) items
        Sub-nodes branching out from the source one.
    parent : `None` or ``TokenTypeNode``
        The parent node-
    """
    __slots__ = ('html_class', 'id', 'is_class_direct', 'nodes', 'parent')
    
    def __new__(cls, id_):
        """
        Creates a new ``TokenClassNode`` instance with the given identifier.
        
        Parameters
        ----------
        id_ : `int`
            The identifier of the token.
        """
        self = object.__new__(cls)
        self.id = id_
        self.html_class = None
        self.is_class_direct = False
        self.nodes = None
        self.parent = None
        
        TOKEN_TYPE_NODES[id_] = self
        
        return self
    
    def __repr__(self):
        """Returns the token type node's representation."""
        result = ['<', self.__class__.__name__, ' id=', repr(self.id)]
        
        if self.is_class_direct:
            result.append(', html_class=')
            result.append(repr(self.html_class))
        
        nodes = self.nodes
        if (nodes is not None):
            result.append(', nodes=')
            result.append(repr(nodes))
        
        result.append('>')
        
        return ''.join(result)
    
    def add_node(self, node):
        """
        Adds a sub node.
        
        Parameters
        ----------
        node : ``TokenTypeNode``
        """
        node.parent = self
        
        nodes = self.nodes
        if nodes is None:
            self.nodes = nodes = {}
        
        nodes[node.id] = node
    
    def _set_html_class(self, html_class):
        """
        Sets the node's html class. This is an internal method called by ``.set_html_class`` or by itself recursively
        to actually modify the attributes.
        
        This method shall be called only from a parent node.
        
        Parameters
        ----------
        html_class : `None` or `str`
            the html class to set or `None` to remove.
        """
        self.html_class = html_class
        
        nodes = self.nodes
        if (nodes is not None):
            for node in nodes.values():
                if not node.is_class_direct:
                    node._set_html_class(html_class)
    
    def set_html_class(self, html_class):
        """
        Sets html class to the node.
        
        Parameters
        ----------
        html_class : `None` or `str`
            the html class to set or `None` to remove.
        """
        if html_class is None:
            if self.is_class_direct:
                self.is_class_direct = False
                parent = self.parent
                if (parent is not None):
                    html_class = parent.html_class
                    # Only continue if the html classes are different
                    if self.html_class != html_class:
                        self._set_html_class(html_class)
        
        else:
            self.is_class_direct = True
            self._set_html_class(html_class)


def build_type_token_nodes(dictionary):
    """
    Builds a token node type structure from the given dictionary.
    
    Parameters
    ----------
    dictionary : `dict` of (`int`, `None` or repeat) items
        A dictionary, which describes the node structure.
    """
    for key, value in dictionary.items():
        node = TokenTypeNode(key)
        if (value is not None):
            build_type_token_child(node, value)

def build_type_token_child(parent, dictionary):
    """
    Builds token node type structure extending the given parent.
    
    Parameters
    ----------
    parent : ``TokenTypeNode``
        The parent node.
    dictionary : `dict` of (`int`, `None` or repeat) items
        A dictionary, which describes the node structure.
    """
    for key, value in dictionary.items():
        node = TokenTypeNode(key)
        parent.add_node(node)
        if (value is not None):
            build_type_token_child(node, value)

def set_highlight_html_class(token_type_identifier, html_class):
    """
    Sets html class for the given node.
    
    Raises
    ------
    TypeError
        - If `token_type_identifier` was not given as `int` instance.
        - If `html_class` was not given neither as `None` nor as `str` instance.
    ValueError
        If `token_type_identifier` was not given as any of the predefined values. Check ``TOKEN_TYPES`` for more
            details.
    """
    if not isinstance(token_type_identifier, int):
        raise TypeError(f'`token_type_identifier` can be given as `int` instance, got: '
            f'{token_type_identifier.__class__.__name__}.')
    
    if (html_class is not None) and (not isinstance(html_class, str)):
        raise TypeError(f'`html_class` can be given as `None` or `str` instance, got {html_class.__class__.__name__}.')
    
    try:
        node = TOKEN_TYPE_NODES[token_type_identifier]
    except KeyError:
        raise ValueError(f'`token_type_identifier` was not given as any of the predefined values, got: '
            f'{token_type_identifier!r}.') from None
    
    node.set_html_class(html_class)


TOKEN_TYPE_ALL = 0
TOKEN_TYPE_SPACE = 1
TOKEN_TYPE_LINEBREAK = 2
TOKEN_TYPE_NON_SPACE = 3
TOKEN_TYPE_NON_SPACE_UNIDENTIFIED = 4
TOKEN_TYPE_COMMENT = 5
TOKEN_TYPE_LINEBREAK_ESCAPED = 6

TOKEN_TYPE_CONSTANT = 100
TOKEN_TYPE_NUMERIC = 110
TOKEN_TYPE_NUMERIC_FLOAT = 111
TOKEN_TYPE_NUMERIC_FLOAT_COMPLEX = 112
TOKEN_TYPE_NUMERIC_INTEGER = 113
TOKEN_TYPE_NUMERIC_INTEGER_HEXADECIMAL = 114
TOKEN_TYPE_NUMERIC_INTEGER_DECIMAL = 115
TOKEN_TYPE_NUMERIC_INTEGER_OCTAL = 116
TOKEN_TYPE_NUMERIC_INTEGER_BINARY = 117
TOKEN_TYPE_STRING = 120
TOKEN_TYPE_STRING_BINARY = 121
TOKEN_TYPE_STRING_UNICODE = 122
TOKEN_TYPE_STRING_UNICODE_FORMAT = 123
TOKEN_TYPE_STRING_UNICODE_FORMAT_MARK = 124
TOKEN_TYPE_STRING_UNICODE_FORMAT_CODE = 125
TOKEN_TYPE_STRING_UNICODE_FORMAT_POSTFIX = 126

TOKEN_TYPE_IDENTIFIER = 200
TOKEN_TYPE_IDENTIFIER_VARIABLE = 201
TOKEN_TYPE_IDENTIFIER_ATTRIBUTE = 202
TOKEN_TYPE_IDENTIFIER_KEYWORD = 210
TOKEN_TYPE_IDENTIFIER_BUILTIN = 221
TOKEN_TYPE_IDENTIFIER_BUILTIN_VARIABLE = 222
TOKEN_TYPE_IDENTIFIER_BUILTIN_CONSTANT = 223
TOKEN_TYPE_IDENTIFIER_BUILTIN_EXCEPTION = 224
TOKEN_TYPE_IDENTIFIER_MAGIC = 230
TOKEN_TYPE_IDENTIFIER_MAGIC_FUNCTION = 231
TOKEN_TYPE_IDENTIFIER_MAGIC_VARIABLE = 232

TOKEN_TYPE_SPECIAL = 300
TOKEN_TYPE_SPECIAL_OPERATOR = 301
TOKEN_TYPE_SPECIAL_OPERATOR_ATTRIBUTE = 302
TOKEN_TYPE_SPECIAL_PUNCTUATION = 303
TOKEN_TYPE_SPECIAL_OPERATOR_WORD = 304
TOKEN_TYPE_SPECIAL_CONSOLE_PREFIX = 305


build_type_token_nodes({
    TOKEN_TYPE_ALL: {
        TOKEN_TYPE_SPACE : None,
        TOKEN_TYPE_LINEBREAK : {
            TOKEN_TYPE_LINEBREAK_ESCAPED : None,
        },
        TOKEN_TYPE_NON_SPACE : {
            TOKEN_TYPE_NON_SPACE_UNIDENTIFIED : None,
            TOKEN_TYPE_CONSTANT : {
                TOKEN_TYPE_NUMERIC : {
                    TOKEN_TYPE_NUMERIC_FLOAT : {
                        TOKEN_TYPE_NUMERIC_FLOAT_COMPLEX : None,
                    },
                    TOKEN_TYPE_NUMERIC_INTEGER : {
                        TOKEN_TYPE_NUMERIC_INTEGER_HEXADECIMAL : None,
                        TOKEN_TYPE_NUMERIC_INTEGER_DECIMAL : None,
                        TOKEN_TYPE_NUMERIC_INTEGER_OCTAL : None,
                        TOKEN_TYPE_NUMERIC_INTEGER_BINARY : None,
                    },
                    TOKEN_TYPE_STRING : {
                        TOKEN_TYPE_STRING_BINARY : None,
                        TOKEN_TYPE_STRING_UNICODE : {
                            TOKEN_TYPE_STRING_UNICODE_FORMAT : {
                                TOKEN_TYPE_STRING_UNICODE_FORMAT_MARK : None,
                                TOKEN_TYPE_STRING_UNICODE_FORMAT_CODE : None,
                                TOKEN_TYPE_STRING_UNICODE_FORMAT_POSTFIX : None,
                            },
                        },
                    },
                },
            },
            TOKEN_TYPE_IDENTIFIER : {
                TOKEN_TYPE_IDENTIFIER_VARIABLE : None,
                TOKEN_TYPE_IDENTIFIER_ATTRIBUTE : None,
                TOKEN_TYPE_IDENTIFIER_KEYWORD : None,
                TOKEN_TYPE_IDENTIFIER_BUILTIN : {
                    TOKEN_TYPE_IDENTIFIER_BUILTIN_VARIABLE : None,
                    TOKEN_TYPE_IDENTIFIER_BUILTIN_CONSTANT : None,
                    TOKEN_TYPE_IDENTIFIER_BUILTIN_EXCEPTION : None,
                },
                TOKEN_TYPE_IDENTIFIER_MAGIC : {
                    TOKEN_TYPE_IDENTIFIER_MAGIC_FUNCTION : None,
                    TOKEN_TYPE_IDENTIFIER_MAGIC_VARIABLE : None,
                },
            },
            TOKEN_TYPE_SPECIAL : {
                TOKEN_TYPE_SPECIAL_OPERATOR : {
                    TOKEN_TYPE_SPECIAL_OPERATOR_ATTRIBUTE : None,
                    TOKEN_TYPE_SPECIAL_OPERATOR_WORD : None,
                },
                TOKEN_TYPE_SPECIAL_PUNCTUATION : None,
                TOKEN_TYPE_SPECIAL_CONSOLE_PREFIX : None,
            },
        },
    TOKEN_TYPE_COMMENT : None,
    },
},)


MERGE_TOKEN_TYPES = {
    # Strings are usually added as 3 parts, prefix+encapsulator | content | prefix+encapsulator
    TOKEN_TYPE_STRING,
    TOKEN_TYPE_STRING_BINARY,
    TOKEN_TYPE_STRING_UNICODE,
    TOKEN_TYPE_STRING_UNICODE_FORMAT,
    TOKEN_TYPE_STRING_UNICODE_FORMAT_MARK,
    TOKEN_TYPE_STRING_UNICODE_FORMAT_CODE,
    # At the case of special characters it not really matters
    TOKEN_TYPE_SPECIAL,
    TOKEN_TYPE_SPECIAL_OPERATOR,
    TOKEN_TYPE_SPECIAL_OPERATOR_ATTRIBUTE,
    TOKEN_TYPE_SPECIAL_PUNCTUATION,
    TOKEN_TYPE_SPECIAL_OPERATOR_WORD,
    # Yes, space may be duped as well.
    TOKEN_TYPE_SPACE,
}


class Token:
    """
    Represents a token parsed by ``HighlightContextBase``.
    
    Parameters
    ----------
    type : `int`
        The token's identifier.
    value : `None` or `str`
        The token's value.
    """
    __slots__ = ('type', 'value',)
    
    def __new__(cls, type_, value):
        """
        Creates a new ``Token`` instance.
        
        Parameters
        ----------
        type : `int`
            The token's identifier.
        value : `None` or `str`
            The token's value.
        """
        self = object.__new__(cls)
        self.type = type_
        self.value = value
        return self
    
    def __repr__(self):
        """Returns the token's representation."""
        return f'{self.__class__.__name__}({self.type}, {self.value})'


def _merge_tokens(tokens, start_index, end_index):
    """
    Merges the tokens inside of the given range.
    
    Parameters
    ----------
    tokens : `list` of ``Token``
        The tokens, which will have it's slice merged.
    start_index : `int`
        The first token's index to merge.
    end_index : `int`
        The last token's index +1 to merge.
    """
    values = []
    
    for token_index in range(start_index, end_index):
        value = tokens[token_index].value
        if (value is not None) and value:
            values.append(value)
    
    value = ''.join(values)
    
    del tokens[start_index+1:end_index]
    tokens[start_index].value = value


class HighlightContextBase:
    """
    Base class for highlighting.
    
    Attributes
    ----------
    done : `bool`
        Whether processing is done.
    tokens : `list` of ``Token``
        The generated tokens.
    """
    __slots__ = ('done', 'tokens',)
    
    def __new__(cls):
        """
        Creates a new ``HighlightContextBase`` instance.
        
        > Subclasses should overwrite it.
        """
        return object.__new__(cls)
    
    def get_line_index(self):
        """
        Returns the line's index where the context is at.
        
        > Subclasses should overwrite it.
        
        Returns
        -------
        line_index : `int`
        """
        return 0

    def get_line(self):
        """
        Returns the actual line of the context.
        
        > Subclasses should overwrite it.
        
        Returns
        -------
        line : `str`
        """
        return ''
        
    def get_line_character_index(self):
        """
        Returns the character index of the context's actual line.
        
        > Subclasses should overwrite it.
        
        Returns
        -------
        line_character_index : `int`
        """
        return 0

    def set_line_character_index(self, line_character_index):
        """
        Sets the actual line's character index.
        
        > Subclasses should overwrite it.
        
        Parameters
        ----------
        line_character_index : `int`
            The index to set of the actual line.
            
            Pass it as `-1` to force end the line with linebreak or as `-2` to force it without linebreak.
        """
        pass
    
    def add_token(self, token_type, token_value):
        """
        Adds a token to the context.
        
        Parameters
        ----------
        token_type : `int`
            The token's identifier.
        token_value : `None` or `str`
            The token's value.
        """
        token = Token(token_type, token_value)
        self.tokens.append(token)

    def add_tokens(self, tokens):
        """
        Adds tokens to the context.
        
        Parameters
        ----------
        tokens : `list` of ``Token``
            The tokens to add.
        """
        self.tokens.extend(tokens)
    
    def get_last_related_token(self):
        """
        Gets the last token of the highlight context.
        
        Returns
        -------
        token : ``Token`` or `None`
            The token if there is any added.
        """
        tokens = self.tokens
        
        for token in reversed(tokens):
            token_type = token.type
            
            if token_type == TOKEN_TYPE_LINEBREAK_ESCAPED:
                continue
            
            if token_type == TOKEN_TYPE_SPACE:
                continue
            
            if token_type == TOKEN_TYPE_COMMENT:
                continue
            
            break
        else:
            token = None
        
        return token
    
    def match(self):
        """
        Matches the content of the context.
        
        > Subclasses should overwrite it.
        """
        pass
    
    def generate_highlighted(self):
        """
        Generates highlighted content.
        
        This method is a generator.
        
        > Subclasses should overwrite it.
        
        Returns
        -------
        content : `str`
            The generated content.
        """
        return
        yield
    
    def _add_linebreak_token(self):
        """
        Adds a linebreak token to the context.
        """
        tokens = self.tokens
        
        for token in reversed(tokens):
            token_type = token.type
            if token_type == TOKEN_TYPE_SPACE:
                continue
            
            if token_type == TOKEN_TYPE_COMMENT:
                continue
            
            if (token_type == TOKEN_TYPE_SPECIAL_OPERATOR) and (token.value == '\\'):
                last_token_is_escape = True
                break
            
            last_token_is_escape = False
            break
        else:
            last_token_is_escape = False
        
        if last_token_is_escape:
            token_type = TOKEN_TYPE_LINEBREAK
        else:
            token_type = TOKEN_TYPE_LINEBREAK_ESCAPED
        
        token = Token(token_type, None)
        tokens.append(token)


class HighlightContext(HighlightContextBase):
    """
    Represents a context of highlighting any content.
    
    Attributes
    ----------
    done : `bool`
        Whether processing is done.
    tokens : `list` of ``Token``
        The generated tokens.
    line_character_index : `int`
        The index of the character of the processed line.
    line_index : `int`
        The index of the line which is processed at the moment.
    lines : `list` of `str`
        The lines to highlight.
    """
    __slots__ = ('line_character_index', 'line_index', 'lines')
    def __new__(cls, lines):
        """
        Creates a new ``HighlightContext`` instance.
        
        Parameters
        ----------
        lines : `list` of `str`
            The lines what the highlight context should match.
        """
        if len(lines) == 0:
            done = True
        else:
            done = False
        
        self = object.__new__(cls)
        
        self.lines = lines
        self.line_index = 0
        self.line_character_index = 0
        self.done = done
        self.tokens = []
        
        return self
    
    def get_line_index(self):
        """
        Returns the line's index where the context is at.
        
        Returns
        -------
        line_index : `int`
        """
        return self.line_index
    
    def get_line(self):
        """
        Returns the actual line of the context.
        
        Returns
        -------
        line : `str`
        """
        lines = self.lines
        line_index = self.line_index
        if len(lines) <= line_index:
            line = ''
        else:
            line = lines[line_index]
        
        return line
    
    def get_line_character_index(self):
        """
        Returns the character index of the context's actual line.
        
        Returns
        -------
        line_character_index : `int`
        """
        return self.line_character_index
    
    def set_line_character_index(self, line_character_index):
        """
        Sets the actual line's character index.
        
        Parameters
        ----------
        line_character_index : `int`
            The index to set of the actual line.
            
            Pass it as `-1` to force end the line with linebreak or as `-2` to force it without linebreak.
        """
        lines = self.lines
        line_index = self.line_index
        line = lines[line_index]
        
        if (line_character_index > 0) and (len(line) > line_character_index):
            self.line_character_index = line_character_index
        else:
            self.line_character_index = 0
            line_index += 1
            
            if len(lines) > line_index:
                self.line_index = line_index
            else:
                self.line_index = line_index
                self.done = True
            
            if line_character_index != -2:
                self._add_linebreak_token()
    
    def match(self):
        """
        Matches the content of the context.
        """
        while not self.done:
            for parser in PYTHON_PARSERS:
                if parser(self):
                    break
        
        # Make sure the last token is not linebreak
        tokens = self.tokens
        if tokens and (tokens[-1].type == TOKEN_TYPE_LINEBREAK):
            del tokens[-1]
        
        # Optimize tokens with merging sames into each other if applicable
        same_count = 1
        last_type = TOKEN_TYPE_ALL
        token_index = len(tokens)-1
        
        while True:
            if token_index <= 0:
                if same_count > 1:
                    # Merge tokens
                    _merge_tokens(tokens, 0, same_count)
                break
            
            token = tokens[token_index]
            token_type = token.type
            
            if (token_type not in MERGE_TOKEN_TYPES):
                last_type = token_type
                same_count = 0
                token_index -= 1
                continue
            
            if (last_type == token_type):
                token_index -= 1
                same_count +=1
                continue
            
            if same_count > 1:
                # Merge tokens
                _merge_tokens(tokens, token_index+1, token_index+same_count+1)
            
            same_count = 1
            last_type = token_type
            token_index -= 1
            continue
    
    def generate_highlighted(self):
        """
        Generates highlighted content.
        
        This method is a generator.
        
        Returns
        -------
        content : `str`
            The generated content.
        """
        for token in self.tokens:
            token_type = token.type
            html_class = TOKEN_TYPE_NODES[token_type].html_class
            token_value = token.value
            if (token_value is not None):
                if (html_class is not None):
                    yield '<span class="'
                    yield html_class
                    yield '">'
                
                yield html_escape(token_value)
                
                if (html_class is not None):
                    yield '</span>'
            
            if (token_type == TOKEN_TYPE_LINEBREAK) or (token_type == TOKEN_TYPE_LINEBREAK_ESCAPED):
                yield '<br>'


class FormatStringContext(HighlightContextBase):
    """
    Highlighter used to highlight format strings.
    
    Attributes
    ----------
    done : `bool`
        Whether processing is done.
    tokens : `list` of ``Token``
        The generated tokens.
    brace_level : `int`
        The internal brace level to un-match before entering a string.
    is_in_code : `bool`
        Whether we are parsing format code.
    line : `str`
        The internal content of the format string.
    line_character_index : `int`
        The index of the character of the processed line.
    """
    __slots__ = ('brace_level', 'is_in_code', 'line', 'line_character_index', )
    def __new__(cls, line):
        """
        Creates a new ``FormatStringContext`` instance.
        
        Parameters
        ----------
        line : `str`
            A format string's internal content to highlight.
        """
        if len(line) == 0:
            done = True
        else:
            done = False
        
        self = object.__new__(cls)
        
        self.line = line
        self.done = done
        self.tokens = []
        self.line_character_index = 0
        self.brace_level = 0
        self.is_in_code = False
        
        return self
    
    def get_line(self):
        """
        Returns the actual line of the context.
        
        Returns
        -------
        line_index : `str`
        """
        return self.line
    
    def get_line_character_index(self):
        """
        Returns the character index of the context's actual line.
        
        Returns
        -------
        line_character_index : `int`
        """
        return self.line_character_index
    
    def set_line_character_index(self, line_character_index):
        """
        Sets the actual line's character index.
        
        Parameters
        ----------
        line_character_index : `int`
            The index to set of the actual line.
            
            Pass it as `-1` to force end the line with linebreak or as `-2` to force it without linebreak.
        """
        line = self.line
        
        if (line_character_index > 0) and (len(line) > line_character_index):
            self.line_character_index = line_character_index
        else:
            self.line_character_index = 0
            self.done = True
    
    def add_token(self, token_type, token_value):
        """
        Adds a token to the context.
        
        Parameters
        ----------
        token_type : `int`
            The token's identifier.
        token_value : `None` or `str`
            The token's value.
        """
        if token_type == TOKEN_TYPE_LINEBREAK:
            self._add_linebreak_token()
            return
        
        # Check braces and such ~ Nya!
        if token_type == TOKEN_TYPE_STRING_UNICODE_FORMAT:
            if self.is_in_code:
                token_type = TOKEN_TYPE_STRING_UNICODE_FORMAT_CODE
        elif token_type == TOKEN_TYPE_SPECIAL_PUNCTUATION and (token_value is not None):
            brace_level = self.brace_level
            if token_value == '{':
                if brace_level == self.is_in_code:
                    token_type = TOKEN_TYPE_STRING_UNICODE_FORMAT_MARK
                
                brace_level += 1
                self.brace_level = brace_level
            
            elif token_value == '}':
                if brace_level == 0:
                    # Random `}`- may be added as well, so if we are outside of f string internal, leave it alone.
                    token_type = TOKEN_TYPE_STRING_UNICODE_FORMAT
                else:
                    is_in_code = self.is_in_code
                    if brace_level <= is_in_code+1:
                        token_type = TOKEN_TYPE_STRING_UNICODE_FORMAT_MARK
                        if (brace_level == 1) and is_in_code:
                            self.is_in_code = False
                    
                    brace_level -= 1
                    self.brace_level = brace_level
            
            elif token_value == ':':
                if (self.brace_level == 1) and (not self.is_in_code):
                    self.is_in_code = True
                    token_type = TOKEN_TYPE_STRING_UNICODE_FORMAT_MARK
        
        HighlightContextBase.add_token(self, token_type, token_value)
    
    def match(self):
        """
        Matches the content of the context.
        """
        while True:
            if self.done:
                break
            
            if (self.brace_level == self.is_in_code):
                _try_match_till_format_string_expression(self)
            else:
                while True:
                    for parser in PYTHON_PARSERS_FORMAT_STRING:
                        if parser(self):
                            break
                    
                    # Need goto!
                    if self.done:
                        break
                    
                    # Need goto!
                    if self.brace_level == self.is_in_code:
                        break



def _try_match_complex(context):
    """
    Tries to match a complex as the context's next token.
    
    Parameter
    ---------
    context : ``HighlightContextBase``
        The context to use.
    
    Returns
    -------
    success : `bool`
        Whether a complex could be matched.
    """
    line = context.get_line()
    index = context.get_line_character_index()
    
    matched = COMPLEX_RP.match(line, index)
    if matched is None:
        return False
    
    content = matched.group(0)
    
    context.add_token(TOKEN_TYPE_NUMERIC_FLOAT_COMPLEX, content)
    
    end = matched.end()
    context.set_line_character_index(end)
    return True

def _try_match_float(context):
    """
    Tries to match a float as the context's next token.
    
    Parameter
    ---------
    context : ``HighlightContextBase``
        The context to use.
    
    Returns
    -------
    success : `bool`
        Whether a float could be matched.
    """
    line = context.get_line()
    index = context.get_line_character_index()
    
    matched = FLOAT_RP.match(line, index)
    if matched is None:
        return False
    
    content = matched.group(0)
    
    context.add_token(TOKEN_TYPE_NUMERIC_FLOAT, content)
    
    end = matched.end()
    context.set_line_character_index(end)
    return True


def _try_match_integer_hexadecimal(context):
    """
    Tries to match an hexadecimal integer as the context's next token.
    
    Parameter
    ---------
    context : ``HighlightContextBase``
        The context to use.
    
    Returns
    -------
    success : `bool`
        Whether a hexadecimal integer could be matched.
    """
    line = context.get_line()
    index = context.get_line_character_index()
    
    matched = INTEGER_HEXADECIMAL_RP.match(line, index)
    if matched is None:
        return False
    
    content = matched.group(0)
    
    context.add_token(TOKEN_TYPE_NUMERIC_INTEGER_HEXADECIMAL, content)
    
    end = matched.end()
    context.set_line_character_index(end)
    return True


def _try_match_integer_decimal(context):
    """
    Tries to match an decimal integer as the context's next token.
    
    Parameter
    ---------
    context : ``HighlightContextBase``
        The context to use.
    
    Returns
    -------
    success : `bool`
        Whether a decimal integer could be matched.
    """
    line = context.get_line()
    index = context.get_line_character_index()
    
    matched = INTEGER_DECIMAL_RP.match(line, index)
    if matched is None:
        return False
    
    content = matched.group(0)
    
    context.add_token(TOKEN_TYPE_NUMERIC_INTEGER_DECIMAL, content)
    
    end = matched.end()
    context.set_line_character_index(end)
    return True

def _try_match_integer_octal(context):
    """
    Tries to match an octal integer as the context's next token.
    
    Parameter
    ---------
    context : ``HighlightContextBase``
        The context to use.
    
    Returns
    -------
    success : `bool`
        Whether an octal integer could be matched.
    """
    line = context.get_line()
    index = context.get_line_character_index()
    
    matched = INTEGER_OCTAL_RP.match(line, index)
    if matched is None:
        return False
    
    content = matched.group(0)
    
    context.add_token(TOKEN_TYPE_NUMERIC_INTEGER_OCTAL, content)
    
    end = matched.end()
    context.set_line_character_index(end)
    return True

def _try_match_integer_binary(context):
    """
    Tries to match a binary integer as the context's next token.
    
    Parameter
    ---------
    context : ``HighlightContextBase``
        The context to use.
    
    Returns
    -------
    success : `bool`
        Whether an octal integer could be matched.
    """
    line = context.get_line()
    index = context.get_line_character_index()
    
    matched = INTEGER_BINARY_RP.match(line, index)
    if matched is None:
        return False
    
    content = matched.group(0)
    
    context.add_token(TOKEN_TYPE_NUMERIC_INTEGER_BINARY, content)
    
    end = matched.end()
    context.set_line_character_index(end)
    return True

def _try_match_identifier(context):
    """
    Tries to match an identifier as the context's next token.
    
    Parameter
    ---------
    context : ``HighlightContextBase``
        The context to use.
    
    Returns
    -------
    success : `bool`
        Whether an identifier could be matched.
    """
    line = context.get_line()
    index = context.get_line_character_index()
    
    matched = IDENTIFIER_RP.match(line, index)
    if matched is None:
        return False
    
    content = matched.group(0)
    
    if content in BUILTIN_CONSTANTS:
        token_type = TOKEN_TYPE_IDENTIFIER_BUILTIN_CONSTANT
    elif content in KEYWORDS:
        token_type = TOKEN_TYPE_IDENTIFIER_KEYWORD
    elif content in MAGIC_FUNCTIONS:
        token_type = TOKEN_TYPE_IDENTIFIER_MAGIC_FUNCTION
    elif content in MAGIC_VARIABLES:
        token_type = TOKEN_TYPE_IDENTIFIER_MAGIC_VARIABLE
    elif content in OPERATOR_WORDS:
        token_type = TOKEN_TYPE_SPECIAL_OPERATOR_WORD
    else:
        last_token = context.get_last_related_token()
        if (last_token is not None) and (last_token.type == TOKEN_TYPE_SPECIAL_OPERATOR_ATTRIBUTE):
            token_type = TOKEN_TYPE_IDENTIFIER_ATTRIBUTE
        else:
            if content in BUILTIN_VARIABLES:
                token_type = TOKEN_TYPE_IDENTIFIER_BUILTIN_VARIABLE
            elif content in BUILTIN_EXCEPTIONS:
                token_type = TOKEN_TYPE_IDENTIFIER_BUILTIN_EXCEPTION
            else:
                token_type = TOKEN_TYPE_IDENTIFIER_VARIABLE
    
    context.add_token(token_type, content)
    
    end = matched.end()
    context.set_line_character_index(end)
    return True

def _try_match_punctuation(context):
    """
    Tries to match a punctuation as the context's next token.
    
    Parameter
    ---------
    context : ``HighlightContextBase``
        The context to use.
    
    Returns
    -------
    success : `bool`
        Whether a punctuation could be matched.
    """
    line = context.get_line()
    index = context.get_line_character_index()
    
    matched = PUNCTUATION_WP.match(line, index)
    if matched is None:
        return False
    
    context.add_token(TOKEN_TYPE_SPECIAL_PUNCTUATION, matched)
    
    end = index+len(matched)
    context.set_line_character_index(end)
    return True

def _try_match_operator(context):
    """
    Tries to match an operator as the context's next token.
    
    Parameter
    ---------
    context : ``HighlightContextBase``
        The context to use.
    
    Returns
    -------
    success : `bool`
        Whether a operator could be matched.
    """
    line = context.get_line()
    index = context.get_line_character_index()
    
    matched = OPERATOR_WP.match(line, index)
    if matched is None:
        return False
    
    if matched == ATTRIBUTE_ACCESS_OPERATOR:
        token_type = TOKEN_TYPE_SPECIAL_OPERATOR_ATTRIBUTE
    elif matched == KEYWORD_ELLIPSIS:
        token_type = TOKEN_TYPE_IDENTIFIER_BUILTIN_CONSTANT
    else:
        token_type = TOKEN_TYPE_SPECIAL_OPERATOR
    
    context.add_token(token_type, matched)
    
    end = index+len(matched)
    context.set_line_character_index(end)
    return True

def _try_match_string(context):
    """
    Tries to match a string as the context's next token.
    
    Parameter
    ---------
    context : ``HighlightContextBase``
        The context to use.
    
    Returns
    -------
    success : `bool`
        Whether a string could be matched.
    """
    line = context.get_line()
    index = context.get_line_character_index()
    
    matched = STRING_STARTER_RP.match(line, index)
    if matched is None:
        return False
    
    content = matched.group(0)
    prefix, encapsuletor = matched.groups()
    
    if prefix is None:
        token_type = TOKEN_TYPE_STRING_UNICODE
    elif 'b' in prefix:
        token_type = TOKEN_TYPE_STRING_BINARY
    elif 'f' in prefix:
        token_type = TOKEN_TYPE_STRING_UNICODE_FORMAT
    else:
        token_type = TOKEN_TYPE_STRING_UNICODE
    
    context.add_token(token_type, content)
    
    end = matched.end()
    context.set_line_character_index(end)
    
    if len(encapsuletor) == 3:
        if encapsuletor == '\'\'\'':
            end_finder = STRING_MULTI_LINE_END_SINGLE_RP
        else:
            end_finder = STRING_MULTI_LINE_END_DOUBLE_RP
        
        content_parts = []
        while True:
            line = context.get_line()
            index = context.get_line_character_index()
            
            matched = end_finder.match(line, index)
            if matched is None:
                context.set_line_character_index(-2)
                content = line[index:]
                content_parts.append(content)
                continue
            
            content = matched.group(1)
            content_parts.append(content)
            
            set_end_later = matched.end()
            break
        
        # Add content
        if token_type == TOKEN_TYPE_STRING_UNICODE_FORMAT:
            content = '\n'.join(content_parts)
            format_string_context = FormatStringContext(content)
            format_string_context.match()
            context.add_tokens(format_string_context.tokens)
        else:
            limit = len(content_parts)
            if limit:
                index = 0
                while True:
                    content = content_parts[index]
                    context.add_token(token_type, content)
                    
                    index += 1
                    if index == limit:
                        break
                    
                    context.add_token(TOKEN_TYPE_LINEBREAK, None)
                    continue
    
    else:
        if len(line) == end:
            set_end_later = -100
        else:
            if encapsuletor == '\'':
                end_finder = STRING_END_SINGLE_RP
            else:
                end_finder = STRING_END_DOUBLE_RP
            
            matched = end_finder.match(line, end)
            if matched is None:
                content = line[end:]
                set_end_later = -1
            else:
                content = matched.group(1)
                set_end_later = matched.end()
            
            if token_type == TOKEN_TYPE_STRING_UNICODE_FORMAT:
                format_string_context = FormatStringContext(content)
                format_string_context.match()
                context.add_tokens(format_string_context.tokens)
            else:
                context.add_token(token_type, content)
    
    context.add_token(token_type, encapsuletor)
    
    if set_end_later != -100:
        context.set_line_character_index(set_end_later)
    
    return True

def _try_match_space(context):
    """
    Tries to match some space as the context's next token.
    
    Parameter
    ---------
    context : ``HighlightContextBase``
        The context to use.
    
    Returns
    -------
    success : `bool`
        Whether any space could be matched.
    """
    line = context.get_line()
    index = context.get_line_character_index()
    
    matched = SPACE_MATCH_RP.match(line, index)
    if matched is None:
        return False
    
    content = matched.group(0)
    
    context.add_token(TOKEN_TYPE_SPACE, content)
    
    end = matched.end()
    context.set_line_character_index(end)
    return True

def _try_match_comment(context):
    """
    Tries to match a comment as the context's next token.
    
    Parameter
    ---------
    context : ``HighlightContextBase``
        The context to use.
    
    Returns
    -------
    success : `bool`
        Whether any comment could be matched.
    """
    line = context.get_line()
    index = context.get_line_character_index()
    
    if line[index] != '#':
        return False
    
    # In later joined contents we might meet line break, so check that as well!
    line_break_index = line.find('\n')
    if line_break_index == -1:
        content = line[index:]
        context.add_token(TOKEN_TYPE_COMMENT, content)
        context.set_line_character_index(-1)
    else:
        content = line[index:line_break_index]
        context.add_token(TOKEN_TYPE_COMMENT, content)
        context.add_token(TOKEN_TYPE_LINEBREAK, None)
        context.set_line_character_index(line_break_index+1)
    
    return True

def _try_match_anything(context):
    """
    Matches anything as the context's next token.
    
    Parameter
    ---------
    context : ``HighlightContextBase``
        The context to use.
    
    Returns
    -------
    success : `bool`
        Whether anything could be matched, so of course true.
    """
    line = context.get_line()
    index = context.get_line_character_index()
    content = line[index]
    context.add_token(TOKEN_TYPE_NON_SPACE_UNIDENTIFIED, content)
    context.set_line_character_index(index+1)
    return True

def _try_match_empty_line(context):
    """
    Tries to match an empty line.
    
    Parameter
    ---------
    context : ``HighlightContextBase``
        The context to use.
    
    Returns
    -------
    success : `bool`
        Whether an empty line could be matched.
    """
    line = context.get_line()
    index = context.get_line_character_index()
    
    if index < len(line):
        return False
    
    context.add_token(TOKEN_TYPE_LINEBREAK, None)
    context.set_line_character_index(-1)
    return True

def _try_match_console_prefix(context):
    """
    Tries to match a console prefix
    
    Parameter
    ---------
    context : ``HighlightContextBase``
        The context to use.
    
    Returns
    -------
    success : `bool`
        Whether console prefix could be matched.
    """
    index = context.get_line_character_index()
    if index != 0:
        return False
    
    line = context.get_line()
    
    matched = CONSOLE_PREFIX_RP.match(line)
    if matched is None:
        return False
    
    prefix, space = matched.groups()
    context.add_token(TOKEN_TYPE_SPECIAL_CONSOLE_PREFIX, prefix)
    context.add_token(TOKEN_TYPE_SPACE, space)
    
    end = matched.end()
    context.set_line_character_index(end)
    return True


PYTHON_PARSERS = (
    _try_match_empty_line,
    _try_match_space,
    _try_match_comment,
    _try_match_string,
    _try_match_complex,
    _try_match_float,
    _try_match_integer_hexadecimal,
    _try_match_integer_decimal,
    _try_match_integer_octal,
    _try_match_integer_binary,
    _try_match_identifier,
    _try_match_console_prefix,
    _try_match_punctuation,
    _try_match_operator,
    _try_match_anything,
      )

def _try_match_till_format_string_expression(context):
    """
    Tries to match a format string's internal content, till reaches the first code part.
    
    Parameters
    ----------
    context : ``FormatStringContext``
        The context to use.
    
    Returns
    -------
    success : `bool`
        Whether anything was matched.
        
        Always returns `True`.
    """
    line = context.get_line()
    line_length = len(line)
    start_index = index = context.get_line_character_index()
    
    while True:
        if index > line_length:
            break
        
        matched = FORMAT_STRING_MATCH_STRING.match(line, index)
        if matched is None:
            # We are at the end, we done, yay.
            content = line[start_index:]
            context.add_token(TOKEN_TYPE_STRING_UNICODE_FORMAT, content)
            context.set_line_character_index(-1)
            break
        
        content, ender = matched.groups()
        if ender == '{{':
            # Escaped `{`
            context.add_token(TOKEN_TYPE_STRING_UNICODE_FORMAT, content)
            context.add_token(TOKEN_TYPE_STRING_UNICODE_FORMAT, ender)
            index += len(content)+2
            continue
        
        if ender == '\n':
            # Multi-line string line break, need to add a linebreak.
            context.add_token(TOKEN_TYPE_STRING_UNICODE_FORMAT, content)
            context.add_token(TOKEN_TYPE_LINEBREAK, None)
            index += len(content)+1
            continue
        
        if ender == '{':
            context.add_token(TOKEN_TYPE_STRING_UNICODE_FORMAT, content)
            context.add_token(TOKEN_TYPE_SPECIAL_PUNCTUATION, ender)
            index += len(content)+1
            context.set_line_character_index(index)
            break
        
        if ender == '}}':
            context.add_token(TOKEN_TYPE_STRING_UNICODE_FORMAT, content)
            context.add_token(TOKEN_TYPE_STRING_UNICODE_FORMAT, ender)
            index += len(content)+2
            context.set_line_character_index(index)
            continue
        
        if ender == '}':
            context.add_token(TOKEN_TYPE_STRING_UNICODE_FORMAT, content)
            context.add_token(TOKEN_TYPE_SPECIAL_PUNCTUATION, ender)
            index += len(content)+1
            context.set_line_character_index(index)
            break
    
    return True

def _try_match_linebreak(context):
    """
    Tries to match a linebreak.
    
    Parameters
    ----------
    context : ``HighlightContextBase``
        The context to use.
    
    Returns
    -------
    success : `bool`
        Whether a linebreak was matched.
    """
    line = context.get_line()
    index = context.get_line_character_index()
    
    if line[index] != '\n':
        return False
    
    context.add_token(TOKEN_TYPE_LINEBREAK, None)
    context.set_line_character_index(index+1)
    
    return True

def _try_match_format_string_postfix(context):
    """
    Tries to match format string postfix.
    
    Parameters
    ----------
    context : ``FormatStringContext``
        The context to use.
    
    Returns
    -------
    success : `bool`
        Whether postfix was matched.
    """
    if context.is_in_code:
        return False
    
    if context.brace_level != 1:
        return False
    
    line = context.get_line()
    index = context.get_line_character_index()
    
    matched = FORMAT_STRING_POSTFIX_RP.match(line, index)
    if matched is None:
        return False
    
    postfix = matched.group(1)
    end = matched.end()
    
    context.add_token(TOKEN_TYPE_STRING_UNICODE_FORMAT_POSTFIX, postfix)
    context.add_token(TOKEN_TYPE_SPECIAL_PUNCTUATION, '}')
    context.set_line_character_index(end)
    return True
    
PYTHON_PARSERS_FORMAT_STRING = (
    _try_match_empty_line,
    _try_match_linebreak,
    _try_match_space,
    _try_match_comment,
    _try_match_string,
    _try_match_complex,
    _try_match_float,
    _try_match_integer_hexadecimal,
    _try_match_integer_decimal,
    _try_match_integer_octal,
    _try_match_integer_binary,
    _try_match_identifier,
    _try_match_punctuation,
    _try_match_operator,
    _try_match_format_string_postfix,
    _try_match_anything,
)
