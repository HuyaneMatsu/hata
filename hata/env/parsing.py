__all__ = ()

from codecs import decode

from scarletio import RichAttributeErrorBaseType


ESCAPE_MAP = {
    '\\':'\\',
    '\'': '\'',
    '"': '"',
    'a': '\a',
    'b': '\b',
    'f': '\f',
    'n': '\n',
    'r': '\r',
    't': '\t',
    'v': '\v',
}


ESCAPE_MAP_REVERSED = {value: key for key, value in ESCAPE_MAP.items()}


PARSED_STATE_SUCCESS = 1 << 0
PARSED_STATE_FAILURE = 1 << 1
PARSED_STATE_END = 1 << 2

ERROR_CODE_VALUE_ALREADY_PARSED = 1
ERROR_CODE_EXPECTED_EQUAL_SIGN = 2
ERROR_CODE_QUOTE_NOT_CLOSED = 3
ERROR_CODE_KEY_STARTER_INVALID = 4


ERROR_MESSAGES = {
    ERROR_CODE_VALUE_ALREADY_PARSED: (
        'Expected comment or end of line.\n'
        'Perhaps there are extra character(s) after the value?'
    ),
    ERROR_CODE_EXPECTED_EQUAL_SIGN: (
        'Expected equal sign, comment or end of line.\n'
        'Perhaps there are extra character(s) after the key?'
    ),
    ERROR_CODE_QUOTE_NOT_CLOSED: (
        'Expected the quote to be closed.\n'
        'If there is no quote on this line at all check them above.'
    ),
    ERROR_CODE_KEY_STARTER_INVALID: (
        'Expected alphabetical character or underscore.\n'
        'Keys cannot start with numbers, perhaps it started with one?'
    ),
}


def embed_error_code(parsed_state, error_code):
    """
    Embeds the error code into the given parsed state.
    
    Parameters
    ----------
    parsed_state : `int`
        Bitwise flag containing the state how the operation went.
    error_code : `int`
        The error code to embed.
    
    Returns
    -------
    parsed_state : `int`
    """
    return (error_code << 16) | parsed_state


def uproot_error_code(parsed_state):
    """
    Uproots the error code from the given parsed state.
    
    Parameters
    ----------
    parsed_state : `int`
        Bitwise flag containing the state how the operation went.
    
    Returns
    -------
    error_code : `int`
    """
    return (parsed_state >> 16) & 0xffff


class ParserState(RichAttributeErrorBaseType):
    """
    Represents parser's state.
    
    Attributes
    ----------
    end : `int`
        The end position of the parser.
    line_index : `int`
        The index of the current line.
    line_start : `int`
        Where the current line is started.
    position : `int`
        The current position.
    value : `list` of `str`
        The value to parse by character.
    """
    __slots__ = ('end', 'line_index', 'line_start', 'position', 'value')
    
    def __new__(cls, value):
        """
        Parameters
        ----------
        value : `str`
            The value to parse.
        """
        self = object.__new__(cls)
        self.end = len(value)
        self.line_index = 0
        self.line_start = 0
        self.position = 0
        self.value = [*value] # When using C change it to uint32 array.
        return self
    
    
    def __repr__(self):
        """Returns the parser's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' position = ')
        repr_parts.append(repr(self.position))
        repr_parts.append(' / ')
        repr_parts.append(repr(self.end))
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def get_value_in_range(self, start, end):
        """
        Returns the value of the parser state at the given range.
        
        Parameters
        ----------
        start : `int`
            Start index.
        end : `int`
            End index.
        
        Returns
        -------
        value_in_range : `str`
        """
        return ''.join(self.value[start : end])
    
        
    def set_line_break(self):
        """
        Sets the line last break of the parser to the current index.
        """
        self.line_start = self.position
        self.line_index += 1


def render_escaped_string_into(into, string):
    """
    Renders the string as escaped into the given container.
    
    Parameters
    ----------
    into : `list` of `str`
        String parts to extend.
    string : `str`
        The string to render.
    
    Returns
    -------
    into : `list` of `str`
    """
    for character in string:
        try:
            character = ESCAPE_MAP_REVERSED[character]
        except KeyError:
            pass
        else:
            into.append('\\')
        
        into.append(character)
    
    return into


def render_string_hidden_representation_into(into, string, cut_at):
    """
    Renders the string as escaped into the given container.
    
    Parameters
    ----------
    into : `list` of `str`
        String parts to extend.
    string : `str`
        The string to render.
    cut_at : `int`
        Where to cut the string.
    
    Returns
    -------
    into : `list` of `str`
    """
    string_length = len(string)
    
    into.append('\'')
    
    # Case: '' (so 0 characters)
    if string_length == 0:
        pass
    
    # Case: 'a'  to 'aaabbb' (1 to  1 - cut_at * 2 characters)
    elif string_length <= cut_at << 1:
        render_escaped_string_into(into, string)
    
    # Case: 'aaa ... (+n hidden) ... bbb' (so cut_at * 2 + 1 to n characters)
    else:
        render_escaped_string_into(into, string[:cut_at])
        into.append(' ... (+')
        into.append(repr(string_length - (cut_at << 1)))
        into.append(' hidden) ... ')
        render_escaped_string_into(into, string[-cut_at:])
    
    into.append('\'')

    return into


class ParserFailureInfo(RichAttributeErrorBaseType):
    """
    Holds additional information about parsing failure.
    
    Attributes
    ----------
    index : `int`
        The error position's index on the `line`. (0 based.)
    line : `str`
        The line where the error was found.
    line_index : `int`
        The `line`'s index inside of the file. (0 based.)
    error_code : `int`
        Error representing the reason why parsing failed.
    """
    __slots__ = ('error_code', 'index', 'line', 'line_index')
    
    def __new__(cls, index, line, line_index, error_code):
        """
        Creates a new parser failure info with the given parameters.
        
        Parameters
        ----------
        index : `int`
            The error position's index on the `line`. (0 based.)
        line : `str`
            The line where the error was found.
        line_index : `int`
            The `line`'s index inside of the file. (0 based.)
        error_code : `int`
            Error representing the reason why parsing failed.
        """
        self = object.__new__(cls)
        self.index = index
        self.line = line
        self.line_index = line_index
        self.error_code = error_code
        return self
    
    
    @classmethod
    def from_parser_state(cls, parser_state, error_code):
        """
        Creates a new parser failure info from the given parser state.
        
        Parameters
        ----------
        parser_state : ``ParserState``
            The parser state to get the error information from.
        error_code : `int`
            Error representing the reason why parsing failed.
        
        Returns
        -------
        self : `instance<cls>`
        """
        line_start_position = parser_state.line_start
        index = parser_state.position - line_start_position
        line_index = parser_state.line_index
        
        exhaust_line(parser_state)
        line = parser_state.get_value_in_range(line_start_position, parser_state.position).rstrip()
        return cls(index, line, line_index, error_code)
    
    
    def __repr__(self):
        """Returns the parser failure's representation."""
        repr_parts = ['<', self.__class__.__name__]
        repr_parts.append(' line_index = ')
        repr_parts.append(repr(self.line_index))
        repr_parts.append(', index = ')
        repr_parts.append(repr(self.index))
        repr_parts.append(', line = ')
        render_string_hidden_representation_into(repr_parts, self.line, 3)
        repr_parts.append(', error_code = ')
        repr_parts.append(repr(self.error_code))
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two parser failure infos are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.error_code != other.error_code:
            return False
        
        if self.index != other.index:
            return False
        
        if self.line != other.line:
            return False
        
        if self.line_index != other.line_index:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the hash value of the parser failure handler."""
        hash_value = 0
        
        # error_code
        hash_value ^= self.error_code
        
        # index
        hash_value ^= self.index << 8
        
        # line
        hash_value ^= hash(self.line)
        
        # line_index
        hash_value ^= self.line_index << 24
        
        return hash_value
    
    
    def get_error_message(self):
        """
        Gets the error message attached to the failure info.
        
        Returns
        -------
        error_message : `None`, `str`
        """
        return ERROR_MESSAGES.get(self.error_code, None)


def is_character_white_space(character):
    """
    Returns whether the character is a white space.
    
    Parameters
    ----------
    character : `str`
        The character to check.
    
    Returns
    -------
    is_white_space : `bool`
    """
    return character in (' ', '\t')


def is_character_per_r(character):
    """
    Returns whether the character is a `\\r`.
    
    Parameters
    ----------
    character : `str`
        The character to check.
    
    Returns
    -------
    is_per_r : `bool`
    """
    return character == '\r'


def is_character_per_n(character):
    """
    Returns whether the character is a `\\r`.
    
    Parameters
    ----------
    character : `str`
        The character to check.
    
    Returns
    -------
    is_per_n : `bool`
    """
    return character == '\n'


def is_character_comment(character):
    """
    Returns whether the character is a comment sign.
    
    Parameters
    ----------
    character : `str`
        The character to check.
    
    Returns
    -------
    is_comment : `bool`
    """
    return character == '#'


def is_character_non_comment_or_line_break(character):
    """
    Returns whether the character is NOT a comment sign or line break.
    
    Parameters
    ----------
    character : `str`
        The character to check.
    
    Returns
    -------
    is_comment : `bool`
    """
    return character not in ('#', '\n', '\r')


def is_character_equal(character):
    """
    Returns whether the character is an equal sign.
    
    Parameters
    ----------
    character : `str`
        The character to check.
    
    Returns
    -------
    is_equal : `bool`
    """
    return character == '='


def is_character_identifier_starter(character):
    """
    Returns whether the character is an identifier starter.
    
    Parameters
    ----------
    character : `str`
        The character to check.
    
    Returns
    -------
    is_character_identifier_starter : `bool`
    """
    return character.isalpha() or character == '_'


def is_character_identifier_continuous(character):
    """
    Returns whether the character is an identifier continuous.
    
    Parameters
    ----------
    character : `str`
        The character to check.
    
    Returns
    -------
    is_character_identifier_starter : `bool`
    """
    return character.isalpha() or character == '_' or character.isnumeric()


def is_at_end(parser_state):
    """
    Returns whether the parser state is at the end position.
    
    Parameters
    ----------
    parser_state : ``ParserState``
        The parser state to check its position.
    
    Returns
    -------
    is_at_end : `bool`
    """
    return parser_state.position >= parser_state.end


def exhaust_any(parser_state):
    """
    Exhausts any characters.
    
    Parameters
    ----------
    parser_state : ``ParserState``
        The parser state to exhaust characters from.
    
    Returns
    -------
    parsed_state : `int`
        Bitwise flag containing the state how the operation went.
    """
    if is_at_end(parser_state):
        return PARSED_STATE_END
    
    parser_state.position += 1
    return PARSED_STATE_SUCCESS


def exhaust_if(parser_state, condition):
    """
    Exhausts the next character if the given condition passes on it.
    
    Parameters
    ----------
    parser_state : ``ParserState``
        The parser state to exhaust characters from.
    condition : `(str) -> bool`
        Condition to call on the next character.
    
    Returns
    -------
    parsed_state : `int`
        Bitwise flag containing the state how the operation went.
    
    """
    if is_at_end(parser_state):
        return PARSED_STATE_END
    
    parser_state_position = parser_state.position
    character_at_position = parser_state.value[parser_state_position]
    if not condition(character_at_position):
        return PARSED_STATE_FAILURE
    
    parser_state.position = parser_state_position + 1
    return PARSED_STATE_SUCCESS


def exhaust_white_space(parser_state):
    """
    Exhausts the next white space character.
    
    Parameters
    ----------
    parser_state : ``ParserState``
        The parser state to exhaust characters from.
    
    Returns
    -------
    parsed_state : `int`
        Bitwise flag containing the state how the operation went.
    """
    return exhaust_if(parser_state, is_character_white_space)


def exhaust_line_break(parser_state):
    """
    Exhausts the next line break. It can be either `\r\n`, `\n`, `\r`.
    
    Parameters
    ----------
    parser_state : ``ParserState``
        The parser state to exhaust characters from.
    
    Returns
    -------
    parsed_state : `int`
        Bitwise flag containing the state how the operation went.
    """
    parsed_state = exhaust_if(parser_state, is_character_per_r)
    if parsed_state & PARSED_STATE_END:
        return parsed_state
    
    if parsed_state & PARSED_STATE_SUCCESS:
        if exhaust_if(parser_state, is_character_per_n) & PARSED_STATE_END:
            parsed_state |= PARSED_STATE_END
        
        parser_state.set_line_break()
        return parsed_state
    
    parsed_state = exhaust_if(parser_state, is_character_per_n)
    if parsed_state & PARSED_STATE_SUCCESS:
        parser_state.set_line_break()
    
    return parsed_state


def exhaust_non_comment_or_line_break(parser_state):
    """
    Exhausts the next non comment or line break character.
    
    Parameters
    ----------
    parser_state : ``ParserState``
        The parser state to exhaust characters from.
    
    Returns
    -------
    parsed_state : `int`
        Bitwise flag containing the state how the operation went.
    """
    return exhaust_if(parser_state, is_character_non_comment_or_line_break)


def repeat_exhauster(parser_state, exhauster):
    """
    Repeats the given exhauster.
    
    Parameters
    ----------
    parser_state : ``ParserState``
        The parser state to exhaust characters from.
    exhauster : `(ParserState) -> int`
        Exhauster to repeat.
    
    Returns
    -------
    parsed_state : `int`
        Bitwise flag containing the state how the operation went.
    """
    return_parsed_state = 0
    
    while True:
        parsed_state = exhauster(parser_state)
        # A parsing can end with `end | success` and `failure`
        if parsed_state & PARSED_STATE_SUCCESS:
            return_parsed_state |= PARSED_STATE_SUCCESS
        
        if parsed_state & PARSED_STATE_END:
            return_parsed_state |= PARSED_STATE_END
            return return_parsed_state
        
        if parsed_state & PARSED_STATE_FAILURE:
            break
        
        continue
    
    if return_parsed_state:
        return return_parsed_state
    
    return PARSED_STATE_FAILURE


def exhaust_white_space_all(parser_state):
    """
    Exhausts all white space in a row.
    
    Parameters
    ----------
    parser_state : ``ParserState``
        The parser state to exhaust characters from.
    
    Returns
    -------
    parsed_state : `int`
        Bitwise flag containing the state how the operation went.
    """
    return repeat_exhauster(parser_state, exhaust_white_space)


def exhaust_line_break_all(parser_state):
    """
    Exhausts all line breaks in a row.
    
    Parameters
    ----------
    parser_state : ``ParserState``
        The parser state to exhaust characters from.
    
    Returns
    -------
    parsed_state : `int`
        Bitwise flag containing the state how the operation went.
    """
    return repeat_exhauster(parser_state, exhaust_line_break)


def chain_exhausters(parser_state, exhausters):
    """
    Chains the given exhausters after each other and repeats them while any of them passes.
    
    Parameters
    ----------
    parser_state : ``ParserState``
        The parser state to exhaust characters from.
    exhausters : `tuple<(ParserState) -> int>`
        Exhauster to repeat.
    
    Returns
    -------
    parsed_state : `int`
        Bitwise flag containing the state how the operation went.
    """
    return_parsed_state = 0
    
    while True:
        for exhauster in exhausters:
            parsed_state = exhauster(parser_state)
            if parsed_state & PARSED_STATE_SUCCESS:
                return_parsed_state |= PARSED_STATE_SUCCESS
            
            if parsed_state & PARSED_STATE_END:
                return_parsed_state |= PARSED_STATE_END
                return return_parsed_state
            
            if parsed_state & PARSED_STATE_FAILURE:
                continue
            
            # If we did not fail, lets start over
            break
        
        else:
            break
        
        continue
    
    if return_parsed_state:
        return return_parsed_state
    
    return PARSED_STATE_FAILURE


def exhaust_line_break_and_white_space_all(parser_state):
    """
    Exhausts all line breaks and white space in a row.
    
    Parameters
    ----------
    parser_state : ``ParserState``
        The parser state to exhaust characters from.
    
    Returns
    -------
    parsed_state : `int`
        Bitwise flag containing the state how the operation went.
    """
    return chain_exhausters(parser_state, (exhaust_white_space_all, exhaust_line_break_all))


def exhaust_line(parser_state):
    """
    Exhausts the whole line. Ends after the first line break.
    
    Parameters
    ----------
    parser_state : ``ParserState``
        The parser state to exhaust characters from.
    
    Returns
    -------
    parsed_state : `int`
        Bitwise flag containing the state how the operation went.
    """
    while True:
        parsed_state = exhaust_line_break(parser_state)
        if parsed_state & PARSED_STATE_SUCCESS:
            return parsed_state
        
        if parsed_state & PARSED_STATE_END:
            parsed_state |= PARSED_STATE_SUCCESS
            return parsed_state
        
        exhaust_any(parser_state)
        continue


def exhaust_till_comment_or_line_break(parser_state):
    """
    Exhausts till the next comment or line break.
    
    Parameters
    ----------
    parser_state : ``ParserState``
        The parser state to exhaust characters from.
    
    Returns
    -------
    parsed_state : `int`
        Bitwise flag containing the state how the operation went.
    """
    return repeat_exhauster(parser_state, exhaust_non_comment_or_line_break)


def exhaust_comment(parser_state):
    """
    Exhausts the commented value.
    
    Parameters
    ----------
    parser_state : ``ParserState``
        The parser state to exhaust characters from.
    
    Returns
    -------
    parsed_state : `int`
        Bitwise flag containing the state how the operation went.
    """
    parsed_state = exhaust_if(parser_state, is_character_comment)
    if parsed_state & (PARSED_STATE_FAILURE | parsed_state & PARSED_STATE_END):
        return parsed_state
    
    if exhaust_line(parser_state) & PARSED_STATE_END:
        parsed_state |= PARSED_STATE_END
    
    return parsed_state


def parse_key_unquoted(parser_state):
    """
    Parses an unquoted key.
    
    Parameters
    ----------
    parser_state : ``ParserState``
        The parser state to exhaust characters from.
    
    Returns
    -------
    parsed_state : `int`
        Bitwise flag containing the state how the operation went.
    value : `None`, `str`
        The parsed out value.
    """
    parser_state_position = parser_state.position
    
    parsed_state = exhaust_if(parser_state, is_character_identifier_starter)
    if not (parsed_state & PARSED_STATE_SUCCESS):
        if parsed_state & PARSED_STATE_FAILURE:
            parsed_state = embed_error_code(parsed_state, ERROR_CODE_KEY_STARTER_INVALID)
        return parsed_state, None
    
    while True:
        continuous_parsed_state = exhaust_if(parser_state, is_character_identifier_continuous)
        if continuous_parsed_state & PARSED_STATE_SUCCESS:
            continue
        
        if continuous_parsed_state & PARSED_STATE_FAILURE:
            break
        
        if continuous_parsed_state & PARSED_STATE_END:
            parsed_state |= PARSED_STATE_END
            break
        
        # No more cases
        continue
    
    value = parser_state.get_value_in_range(parser_state_position, parser_state.position)
    return parsed_state, value


def parse_value_unquoted(parser_state):
    """
    Parses an unquoted value.
    
    Parameters
    ----------
    parser_state : ``ParserState``
        The parser state to exhaust characters from.
    
    Returns
    -------
    parsed_state : `int`
        Bitwise flag containing the state how the operation went.
    value : `None`, `str`
        The parsed out value.
    """
    parser_state_position = parser_state.position
    parsed_state = exhaust_till_comment_or_line_break(parser_state)
    if parsed_state & (PARSED_STATE_SUCCESS | PARSED_STATE_END):
        value = parser_state.get_value_in_range(parser_state_position, parser_state.position).rstrip()
        if not value:
            value = None
    else:
        value = None
    
    return parsed_state, value


def parse_next(parser_state):
    """
    Parses the next character.
    
    Parameters
    ----------
    parser_state : ``ParserState``
        The parser state to exhaust characters from.
    
    Returns
    -------
    parsed_state : `int`
        Bitwise flag containing the state how the operation went.
    value : `None`, `str`
        The parsed out value.
    """
    if is_at_end(parser_state):
        return PARSED_STATE_END, None
    
    parser_state_position = parser_state.position
    value = parser_state.value[parser_state_position]
    parser_state.position = parser_state_position + 1
    return PARSED_STATE_SUCCESS, value


def parse_quoted_content(parser_state, expected_ending):
    """
    Parses a quoted value's (or key's) content till it ends with the expected ending.
    
    Parameters
    ----------
    parser_state : ``ParserState``
        The parser state to exhaust characters from.
    expected_ending : `str`
        The expected ending character of the string.
    
    Returns
    -------
    parsed_state : `int`
        Bitwise flag containing the state how the operation went.
    value : `None`, `str`
        The parsed out value.
    """
    value_parts = []
    
    while True:
        parsed_state, value = parse_next(parser_state)
        if parsed_state == PARSED_STATE_END:
            parsed_state = embed_error_code(parsed_state | PARSED_STATE_FAILURE, ERROR_CODE_QUOTE_NOT_CLOSED)
            break
        
        if value == expected_ending:
            break
        
        if value != '\\':
            value_parts.append(value)
            continue
        
        parsed_state, value = parse_next(parser_state)
        if parsed_state == PARSED_STATE_END:
            value_parts.append(value)
            parsed_state = embed_error_code(parsed_state | PARSED_STATE_FAILURE, ERROR_CODE_QUOTE_NOT_CLOSED)
            break
        
        escaped = ESCAPE_MAP.get(value, None)
        if escaped is None:
            value_parts.append('\\')
            value_parts.append(value)
        else:
            value_parts.append(escaped)
    
    if value_parts:
        value = decode(''.join(value_parts), 'unicode-escape')
    else:
        value = None
    
    return parsed_state, value


def parse_key_or_value(parser_state, parsing_key):
    """
    Parses a key or a value.
    
    Parameters
    ----------
    parser_state : ``ParserState``
        The parser state to exhaust characters from.
    parsing_key : `bool`
        Whether we are parsing a key.
    
    Returns
    -------
    parsed_state : `int`
        Bitwise flag containing the state how the operation went.
    value : `None`, `str`
        The parsed out value.
    """
    # Should not happen -> do not embed error message
    if is_at_end(parser_state):
        return PARSED_STATE_END | PARSED_STATE_FAILURE, None
    
    parser_state_position = parser_state.position
    character_at_position = parser_state.value[parser_state_position]
    if character_at_position in ('\'', '"'):
        parser_state.position = parser_state_position + 1
        return parse_quoted_content(parser_state, character_at_position)
    
    if parsing_key:
        parser = parse_key_unquoted
    else:
        parser = parse_value_unquoted
    
    return parser(parser_state)


def maybe_build_item(key, value):
    """
    Builds a parsed item.
    
    Parameters
    ----------
    key : `None`, `str`
        Parsed key.
    value : `None`, `str`
        The parsed out value.
    
    Returns
    -------
    item : `None`, `tuple` (`str`, `str` | `None`)
    """
    if (key is not None):
        return (key, value)


def parse_item_part_end(parser_state, key, value):
    """
    Parses an item's part's end.
    
    Parameters
    ----------
    parser_state : ``ParserState``
        The parser state to exhaust characters from.
    key : `None`, `str`
        Already parsed out key.
    value : `None`, `str`
        Already parsed out value.
    
    Returns
    -------
    parse_state_item_pair : `None` | `tuple` (`int`, `None`, `tuple` (`str`, `str` | `None`))
        If the item ended returns a `tuple` of `parsed_state` and `item` fields.
    """
    # white space
    parsed_state = exhaust_white_space_all(parser_state)
    if parsed_state & PARSED_STATE_END:
        return parsed_state | PARSED_STATE_SUCCESS, maybe_build_item(key, value)
    
    # line break
    parsed_state = exhaust_line_break(parser_state)
    if parsed_state & (PARSED_STATE_END | PARSED_STATE_SUCCESS):
        return parsed_state | PARSED_STATE_SUCCESS, maybe_build_item(key, value)
    
    # comment sign ?
    parsed_state = exhaust_comment(parser_state)
    if parsed_state & (PARSED_STATE_END | PARSED_STATE_SUCCESS):
        return parsed_state | PARSED_STATE_SUCCESS, maybe_build_item(key, value)
    
    return None


def parse_item(parser_state):
    """
    Parses out an item from the parser.
    
    Parameters
    ----------
    parser_state : ``ParserState``
        The parser state to parse the next item from.
    
    Returns
    -------
    parsed_state : `int`
        Bitwise flag containing the state how the operation went.
    item : `None`, `tuple` (`str`, `str` | `None`)
        The parsed out item if any.
    """
    # We parse till there is something
    while True:
        parsed_state = exhaust_line_break_and_white_space_all(parser_state)
        if parsed_state & PARSED_STATE_END:
            return parsed_state | PARSED_STATE_SUCCESS, None
        
        parsed_state = exhaust_comment(parser_state)
        if parsed_state & PARSED_STATE_END:
            return parsed_state | PARSED_STATE_SUCCESS, None
        
        if parsed_state & PARSED_STATE_SUCCESS:
            continue
        
        break
    
    # key = value
    # ^^^
    parsed_state, key = parse_key_or_value(parser_state, True)
    if parsed_state & PARSED_STATE_FAILURE:
        # Ignore value on failure
        return parsed_state, None
    
    if parsed_state & PARSED_STATE_END:
        return parsed_state, maybe_build_item(key, None)
    
    # parse: white space | linebreak | comment
    end_of_line_output = parse_item_part_end(parser_state, key, None)
    if end_of_line_output is not None:
        return end_of_line_output
    
    # key = value
    #     ^
    parsed_state = exhaust_if(parser_state, is_character_equal)
    if parsed_state & (PARSED_STATE_END | PARSED_STATE_FAILURE):
        return embed_error_code(parsed_state, ERROR_CODE_EXPECTED_EQUAL_SIGN), maybe_build_item(key, None)
    
    # parse: white space | linebreak | comment
    end_of_line_output = parse_item_part_end(parser_state, key, None)
    if end_of_line_output is not None:
        return end_of_line_output
    
    # key = value
    #       ^^^^^
    parsed_state, value = parse_key_or_value(parser_state, False)
    if parsed_state & PARSED_STATE_FAILURE:
        # Ignore value on failure
        return parsed_state, maybe_build_item(key, None)
    
    # parse: white space | linebreak | comment
    end_of_line_output = parse_item_part_end(parser_state, key, value)
    if end_of_line_output is not None:
        return end_of_line_output
    
    # The line is not ended?
    return embed_error_code(PARSED_STATE_FAILURE, ERROR_CODE_VALUE_ALREADY_PARSED), maybe_build_item(key, value)


def add_item(variables, item):
    """
    Adds an item to the variables.
    
    Parameters
    ----------
    variables : `dict` of (`str`, `str`) items
        The parsed variables.
    item : `None`, `tuple` (`str`, `None` | `str`)
        The item to add.
    
    Returns
    -------
    success : `bool`
    """
    if item is None:
        return False
    
    key, value = item
    if variables.get(key, None) is not None:
        return False
        
    variables[key] = value
    return True


def parse_variables(content):
    """
    Parses out the variables from the given input content.
    
    Parameters
    ----------
    content : `str`
        The content to parse.
    
    Returns
    -------
    variables : `dict` of (`str`, `str` | `None`) items
        The parsed out variables.
    parser_failure_info : `None`, ``ParserFailureInfo``
        Error position if any. `-1` if not applicable.
    """
    variables = {}
    parser_failure_info = None
    
    parser_state = ParserState(content)
    
    while True:
        parsed_state, item = parse_item(parser_state)
        add_item(variables, item)
        
        if parsed_state & PARSED_STATE_FAILURE:
            parser_failure_info = ParserFailureInfo.from_parser_state(parser_state, uproot_error_code(parsed_state))
            break
        
        if parsed_state & PARSED_STATE_END:
            break
        
        if parsed_state & PARSED_STATE_SUCCESS:
            continue
        
        # No other case
        break
    
    return variables, parser_failure_info
