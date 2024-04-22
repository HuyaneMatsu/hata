__all__ = ()

from json import JSONDecodeError
from os import get_terminal_size
from reprlib import repr as short_repr

from scarletio import from_json
from scarletio.web_common import FormData
from scarletio.web_common.form_data import FORM_DATA_FIELD_TYPE_JSON


TYPE_NAME_UNEXPECTED = 'Object'
TYPE_NAME_STRING = 'String'
TYPE_NAME_BINARY = 'Binary'
TYPE_NAME_BOOLEAN = 'Boolean'
TYPE_NAME_INTEGER = 'Integer'
TYPE_NAME_FLOAT = 'Float'
TYPE_NAME_LIST = 'List'
TYPE_NAME_HASH_MAP = 'HashMap'
TYPE_NAME_FORM_DATA = 'FormData'

MODIFIER_LENGTH = 'length'

VALUE_INDENT = '    '
VALUE_NONE = 'null'
VALUE_BOOLEAN_TRUE = 'true'
VALUE_BOOLEAN_FALSE = 'false'
VALUE_QUOTE = '"'
VALUE_PAYLOAD = 'payload'

ESCAPABLE = {VALUE_QUOTE, '\\', '\r', '\n', '\t'}

LINE_WIDTH_DEFAULT = 120

STRING_MIN_LINE_LENGTH = 40
STRING_BREAK_TO_MULTI_LINE_OVER = 60
STRING_MAX_RENDER_LENGTH = 6000


def reconstruct_payload(payload):
    """
    Tries to reconstruct the given payload.
    
    Parameters
    ----------
    payload : `object`
        The payload to try to reconstruct.
    
    Returns
    -------
    reconstructed_value : `None | str`
    """
    if payload is None: # nothing to do
        return None
    
    line_width = _get_terminal_line_width()
    
    into = [VALUE_PAYLOAD, ' = ']
    used_characters = len(VALUE_PAYLOAD) + 3
    
    if isinstance(payload, str):
        into = reconstruct_json_into(payload, into, 0, line_width, used_characters)
    
    elif isinstance(payload, FormData):
        into = reconstruct_form_data_into(payload, into, line_width)
    
    elif isinstance(payload, bytes):
        into = reconstruct_binary_into(payload, into, 0, line_width, used_characters)
    
    else:
        into = reconstruct_unexpected_into(payload, into, 0, line_width, len(VALUE_PAYLOAD) + 3)
    
    return ''.join(into)


def reconstruct_json_into(value, into, indent, line_width, used_characters):
    """
    Reconstructs a json payload extending the given `into` list.
    
    Parameters
    ----------
    value : `str`
        Json payload data to reconstruct.
    into : `list<str>`
        A list to extend it's content.
    indent : `int`
        The amount of indents to add.
    line_width : `int`
        Allowed line width.
    used_characters : `int`
        Additionally used characters.
    
    Returns
    -------
    into : `list<str>`
    """
    try:
        json_data = from_json(value)
    except JSONDecodeError:
        into = reconstruct_string_into(value, into, indent, False, line_width, used_characters)
    else:
        into = reconstruct_value_into(json_data, into, indent, False, line_width, used_characters)
    
    return into


def reconstruct_value_into(value, into, indent, value_is_file, line_width, used_characters):
    """
    Reconstructs a value extending the given `into` list.
    
    Parameters
    ----------
    value : `None`, `str`, `list`, `dict`, `int`, `float`, `bool`
        The deserialized json value.
    into : `list<str>`
        A list to extend it's content.
    indent : `int`
        The amount of indents to add.
    value_is_file : `bool`
        Whether the value is a file and should not shown.
    line_width : `int`
        Allowed line width.
    used_characters : `int`
        Additionally used characters.
    
    Returns
    -------
    into : `list<str>`
    """
    if value is None:
        into = reconstruct_null_into(into, indent, line_width, used_characters)
    
    elif isinstance(value, bool):
        into = reconstruct_boolean_into(value, into, indent, line_width, used_characters)

    elif isinstance(value, str):
        into = reconstruct_string_into(value, into, indent, value_is_file, line_width, used_characters)
    
    elif isinstance(value, int):
        into = reconstruct_integer_into(value, into, indent, line_width, used_characters)
    
    elif isinstance(value, float):
        into = reconstruct_float_into(value, into, indent, line_width, used_characters)
    
    elif isinstance(value, list):
        into = reconstruct_list_into(value, into, indent, line_width)
    
    elif isinstance(value, dict):
        into = reconstruct_hash_map_into(value, into, indent, line_width)
    
    elif isinstance(value, bytes):
        # bytes is used at form data
        into = reconstruct_binary_into(value, into, indent, line_width, used_characters)
    
    elif isinstance(value, set):
        # Set can be a substitution to list.
        into = reconstruct_list_into([*value], into, indent, line_width)
    
    else:
        into = reconstruct_unexpected_into(value, into, indent, line_width, used_characters)
    
    return into


def reconstruct_null_into(into, indent, line_width, used_characters):
    """
    Reconstructs a null value to the given `into` list.
    
    Parameters
    ----------
    into : `list<str>`
        A list to extend it's content.
    indent : `int`
        The amount of indents to add.
    line_width : `int`
        Allowed line width.
    used_characters : `int`
        The amount of used characters.
    
    Returns
    -------
    into : `list<str>`
    """
    should_wrap = line_width < (
        used_characters +
        indent * len(VALUE_INDENT) +
        len(VALUE_NONE)
    )
    
    if should_wrap:
        into = _wrap_begin(into, indent)
    
    into.append(VALUE_NONE)
    
    if should_wrap:
        into = _wrap_end(into, indent)
    
    return into


def reconstruct_boolean_into(value, into, indent, line_width, used_characters):
    """
    Reconstructs a boolean value to the given `into` list.
    
    Parameters
    ----------
    value : `bool`
        The boolean value.
    into : `list<str>`
        A list to extend it's content.
    indent : `int`
        The amount of indents to add.
    line_width : `int`
        Allowed line width.
    used_characters : `int`
        The amount of used characters.
    
    Returns
    -------
    into : `list<str>`
    """
    if value:
        value_representation = VALUE_BOOLEAN_TRUE
    else:
        value_representation = VALUE_BOOLEAN_FALSE
    
    should_wrap = line_width < (
        used_characters +
        indent * len(VALUE_INDENT) +
        len(value_representation)
    )
    
    if should_wrap:
        into = _wrap_begin(into, indent)
    
    into.append(value_representation)
    
    if should_wrap:
        into = _wrap_end(into, indent)
    
    return into


def _reconstruct_string_as_single_line_into(value, into):
    """
    Reconstructs a string as single line extending the given `into` list.
    
    Parameters
    ----------
    value : `str`
        The string value.
    into : `list<str>`
        A list to extend it's content.
    
    Returns
    -------
    into : `list<str>`
    """
    into.append(_get_string_representation(value))
    return into


def _reconstruct_string_as_multi_line_into(value, into, indent, line_width):
    """
    Reconstructs a string as multi line extending the given `into` list.
    
    Parameters
    ----------
    value : `str`
        The string value.
    into : `list<str>`
        A list to extend it's content.
    indent : `int`
        The amount of indents to add.
    line_width : `int`
        Allowed line width.
    
    Returns
    -------
    into : `list<str>`
    """
    into.append('(\n')
    
    string_indent = indent + 1
    
    length_limit = line_width - string_indent * len(VALUE_INDENT)
    if length_limit < STRING_MIN_LINE_LENGTH:
        length_limit = STRING_MIN_LINE_LENGTH
    
    for representation in _iter_string_representation_range(value, length_limit):
        for counter in range(string_indent):
            into.append(VALUE_INDENT)
        
        into.append(representation)
        into.append('\n')
    
    for counter in range(indent):
        into.append(VALUE_INDENT)
    
    into.append(')')
    
    return into


def _reconstruct_string_as_annotation_into(value, into, indent, line_width, used_characters):
    """
    Reconstructs a string as an annotation extending the given `into` list.
    
    Parameters
    ----------
    value : `str`
        The string value.
    into : `list<str>`
        A list to extend it's content.
    indent : `int`
        The amount of indents to add.
    line_width : `int`
        Allowed line width.
    used_characters : `int`
        The amount of used characters.
    
    Returns
    -------
    into : `list<str>`
    """
    length_representation = str(len(value))
    estimated_length = (
        used_characters +
        indent * len(VALUE_INDENT) +
        len(TYPE_NAME_STRING) + 5 + len(MODIFIER_LENGTH) + len(length_representation)
    )
    
    should_wrap = line_width < estimated_length
    
    if should_wrap:
        into = _wrap_begin(into, indent)
    
    into.append(TYPE_NAME_STRING)
    into.append('<')
    into.append(MODIFIER_LENGTH)
    into.append(' = ')
    into.append(str(len(value)))
    into.append('>')
    
    if should_wrap:
        into = _wrap_end(into, indent)
    
    return into


def reconstruct_string(value, indent, value_is_file, line_width, used_characters):
    """
    Reconstructs the given string.
    
    Parameters
    ----------
    value : `str`
        The string value.
    indent : `int`
        The amount of indents to add.
    value_is_file : `bool`
        Whether the value is a file and should not be shown.
    used_characters : `int`
        The amount of used characters.
    
    Returns
    -------
    result : `str`
    """
    return ''.join(reconstruct_string_into(value, [], indent, value_is_file, line_width, used_characters))


def reconstruct_string_into(value, into, indent, value_is_file, line_width, used_characters):
    """
    Reconstructs a string value to the given `into` list.
    
    Parameters
    ----------
    value : `str`
        The string value.
    into : `list<str>`
        A list to extend it's content.
    indent : `int`
        The amount of indents to add.
    value_is_file : `bool`
        Whether the value is a file and should not be shown.
    line_width : `int`
        Allowed line width.
    used_characters : `int`
        The amount of used characters.
    
    Returns
    -------
    into : `list<str>`
    """
    if value_is_file or (len(value) > STRING_MAX_RENDER_LENGTH):
        into = _reconstruct_string_as_annotation_into(value, into, indent, line_width, used_characters)
    
    else:
        if _is_string_length_over(value, line_width - used_characters - len(VALUE_INDENT) * indent):
            into = _reconstruct_string_as_multi_line_into(value, into, indent, line_width)
        
        else:
            into = _reconstruct_string_as_single_line_into(value, into)
    
    return into


def reconstruct_integer_into(value, into, indent, line_width, used_characters):
    """
    Reconstructs an integer value to the given `into` list.
    
    Parameters
    ----------
    value : `int`
        The integer value.
    into : `list<str>`
        A list to extend it's content.
    into : `list<str>`
        A list to extend it's content.
    indent : `int`
        The amount of indents to add.
    line_width : `int`
        Allowed line width.
    
    Returns
    -------
    into : `list<str>`
    """
    representation = repr(value)
    
    should_wrap = line_width < (
        used_characters +
        indent * len(VALUE_INDENT) +
        len(representation)
    )
    
    if should_wrap:
        into = _wrap_begin(into, indent)
    
    into.append(representation)
    
    if should_wrap:
        into = _wrap_end(into, indent)
    
    return into


def reconstruct_float_into(value, into, indent, line_width, used_characters):
    """
    Reconstructs a float value to the given `into` list.
    
    Parameters
    ----------
    value : `float`
        The float value.
    into : `list<str>`
        A list to extend it's content.
    indent : `int`
        The amount of indents to add.
    line_width : `int`
        Allowed line width.
    used_characters : `int`
        The amount of used characters.
    
    Returns
    -------
    into : `list<str>`
    """
    value_representation = repr(value)
    
    should_wrap = line_width < (
        used_characters +
        indent * len(VALUE_INDENT) +
        len(value_representation)
    )
    
    if should_wrap:
        into = _wrap_begin(into, indent)
    
    into.append(value_representation)
    
    if should_wrap:
        into = _wrap_end(into, indent)
    
    return into


def reconstruct_list_into(value, into, indent, line_width):
    """
    Reconstructs a list value extending the given `into` list.
    
    Parameters
    ----------
    value : `list`
        The list value.
    into : `list<str>`
        A list to extend it's content.
    indent : `int`
        The amount of indents to add.
    line_width : `int`
        Allowed line width.
    
    Returns
    -------
    into : `list<str>`
    """
    length = len(value)
    
    into.append('[')
    
    if length:
        into.append('\n')
        
        element_indent = indent + 1
        
        for index, list_element in enumerate(value):
            for counter in range(element_indent):
                into.append(VALUE_INDENT)
            
            index_string = str(index)
            into.append(index_string)
            into.append(': ')
            
            reconstruct_value_into(list_element, into, element_indent, False, line_width, len(index_string) + 3)
            
            into.append(',\n')
        
        for counter in range(indent):
            into.append(VALUE_INDENT)
    
    into.append(']')
    return into


def reconstruct_hash_map_into(value, into, indent, line_width):
    """
    Reconstructs a hash map value extending the given `into` list.
    
    Parameters
    ----------
    value : `dict`
        The hash map value.
    into : `list<str>`
        A list to extend it's content.
    indent : `int`
        The amount of indents to add.
    line_width : `int`
        Allowed line width.
    
    Returns
    -------
    into : `list<str>`
    """
    length = len(value)
    
    into.append('{')
    
    if length:
        into.append('\n')
        item_indent = indent + 1
        
        for item_key, item_value in sorted(value.items(), key = _hash_map_key_sort_key):
            for counter in range(item_indent):
                into.append(VALUE_INDENT)
            
            item_key_representation = reconstruct_string(item_key, item_indent, False, line_width, 3)
            into.append(item_key_representation)
            into.append(': ')
            
            if item_key_representation.endswith(')'):
                used_characters = 1 + 3
            else:
                used_characters = len(item_key_representation) + 3
            
            reconstruct_value_into(item_value, into, item_indent, False, line_width, used_characters)
            
            into.append(',\n')
        
        for counter in range(indent):
            into.append(VALUE_INDENT)
    
    into.append('}')
    
    return into


def reconstruct_unexpected_into(value, into, indent, line_width, used_characters):
    """
    Reconstructs a value with an unexpected type to the given `into` list.
    
    Parameters
    ----------
    value : `object`
        Le value.
    into : `list<str>`
        A list to extend it's content.
    indent : `int`
        The amount of indents to add.
    line_width : `int`
        Allowed line width.
    used_characters : `int`
        The amount of used characters.
    
    Returns
    -------
    into : `list<str>`
    """
    value_representation = short_repr(value)
    
    should_wrap = line_width < (
        used_characters +
        indent * len(VALUE_INDENT) +
        len(TYPE_NAME_UNEXPECTED) + 2 + len(value_representation)
    )
    
    if should_wrap:
        into = _wrap_begin(into, indent)
    
    into.append(TYPE_NAME_UNEXPECTED)
    into.append(': ')
    into.append(value_representation)
    
    if should_wrap:
        into = _wrap_end(into, indent)
    
    return into


def reconstruct_binary_into(value, into, indent, line_width, used_characters):
    """
    Reconstructs a binary value to the given `into` list.
    
    Parameters
    ----------
    value : `binary`
        The binary value.
    into : `list<str>`
        A list to extend it's content.
    indent : `int`
        The amount of indents to add.
    line_width : `int`
        Allowed line width.
    used_characters : `int`
        The amount of used characters.
    
    Returns
    -------
    into : `list<str>`
    """
    length_representation = str(len(value))
    
    should_wrap = line_width < (
        used_characters +
        indent * len(VALUE_INDENT) +
        len(TYPE_NAME_BINARY) + 5 + len(MODIFIER_LENGTH) + len(length_representation)
    )
    
    if should_wrap:
        into = _wrap_begin(into, indent)
    
    into.append(TYPE_NAME_BINARY)
    into.append('<')
    into.append(MODIFIER_LENGTH)
    into.append(' = ')
    into.append(str(len(value)))
    into.append('>')
    
    if should_wrap:
        into = _wrap_end(into, indent)
    
    return into


def reconstruct_form_data_into(value, into, line_width):
    """
    Tries to reconstruct form data into the given `into` list.
    
    Parameters
    ----------
    value : ``FormData``
        The form data to reconstruct.
    into : `list<str>`
        A list to extend it's content.
    line_width : `int`
        Allowed line width.
    
    Returns
    -------
    into : `list<str>`
    """
    into.append(TYPE_NAME_FORM_DATA)
    
    fields = value.fields
    
    into.append('(')
    
    if fields:
        into.append('{\n')
        
        for index, field in enumerate(fields):
            field_type_options = field.type_options
            
            field_name = field_type_options['name']
            file_name = field_type_options.get('file_name', None)
            
            into.append(VALUE_INDENT)
            index_representation = str(index)
            into.append(index_representation)
            into.append(': ')
            
            #                        index              + ': ' + {field_name} + (',' | '(')
            used_characters = len(index_representation) +  2   +                     1
            
            field_name_representation = reconstruct_string(field_name, 1, False, line_width, used_characters)
            into.append(field_name_representation)
            
            if (file_name is not None) and (file_name != field_name):
                
                if field_name_representation.endswith(')'):
                    #                 ')' + ' | ' + {file_name} + ': ' + (',' | '(')
                    used_characters =  1  +   3   +                2   +      1
                else:
                    #                          index           + ': ' +         field_name             + ' | ' + {file_name} + ': ' + (',' | '(')
                    used_characters = len(index_representation) + 2   + len(field_name_representation) +   3   +                2   +      1
                
                into.append(' | ')
                file_name_representation = reconstruct_string(file_name, 1, False, line_width, used_characters)
                into.append(file_name_representation)
            else:
                file_name_representation = None
            
            into.append(': ')
            
            if (file_name_representation is not None) and file_name_representation.endswith(')'):
                #                 ")" + ': ' + (',' | '(')
                used_characters =  1  +  2   +      1
            else:
                if (file_name_representation is None):
                    used_characters = 0
                else:
                    #                 ' | ' +          field_name
                    used_characters =   3   + len(file_name_representation)
                
                if field_name_representation.endswith(')'):
                    #                 ')' +  ?(' | ' + field_name) + ': ' + (',' | '(') + {field_value}
                    used_characters =  1  +      used_characters   +  3   +      1
                else:
                    #                           index           + ': ' +           field_name           + ?(' | ' + field_name) + ': ' + {field_value} + (',' | '(')
                    used_characters = len(index_representation) +  2   + len(field_name_representation) +     used_characters   +  2   +                      1
            
            reconstruct_value_into(
                field.value, into, 1, field.type != FORM_DATA_FIELD_TYPE_JSON, line_width, used_characters
            )
            into.append(',\n')
        
        into.append('}')
    
    into.append(')')
    
    return into


def _hash_map_key_sort_key(item):
    """
    Used to sort hash maps based on their key.
    
    Parameters
    ----------
    item : `tuple` (`str`, `object`)
        An item of a hash map.
    
    Returns
    -------
    key : `str`
    """
    return item[0]


def _get_terminal_line_width():
    """
    Gets the terminal's line's width.
    
    Returns
    -------
    line_width : `int`
    """
    try:
        terminal_size = get_terminal_size()
    except OSError:
        line_width = LINE_WIDTH_DEFAULT
    else:
        line_width = terminal_size.columns
    
    return line_width


def _get_string_representation(string):
    """
    Gets the string's representation.
    
    Parameters
    ----------
    string : `str`
        Teh string to represent.
    
    Returns
    -------
    representation : `str`
    """
    return ''.join([
        VALUE_QUOTE,
        *(_get_character_representation(character) for character in string),
        VALUE_QUOTE,
    ])


def _iter_string_representation_range(string, length_limit):
    """
    Yields `length_limit` representation of the given `string`.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    string : `str`
        String to represent.
    length_limit : `int`
        Maximal allowed length. Should be at least `12`.
    
    Yields
    ------
    representation : `str`
    """
    start = 0
    length = len(string)
    
    while start < length:
        representation, start = _get_string_representation_range(string, start, length_limit)
        yield representation


def _get_string_representation_range(string, start, length_limit):
    """
    Gets string representation fulfilling the given range.
    
    Parameters
    ----------
    string : `str`
        The string to represent.
    start : `int`
        First character to represent.
    length_limit : `int`
        Maximal allowed length. Should be at least `12`.
    
    Returns
    -------
    representation : `str`
    end : `int`
    """
    result = [VALUE_QUOTE]
    length = len(VALUE_QUOTE) << 1
    
    for index in range(start, len(string)):
        character = string[index]
        length += _get_character_representation_length(character)
        # If `length_limit` is low make sure we add at least 1 character
        if (length > length_limit) and (start != index):
            end = index
            break
        
        result.append(_get_character_representation(character))
        
    else:
        end = len(string)
    
    result.append(VALUE_QUOTE)
    return ''.join(result), end


def _is_string_length_over(string, length_limit):
    """
    Gets the length of the given string if it would be quoted.
    
    Parameters
    ----------
    string : `str`
        The string to check.
    length_limit : `int`
        Max allowed length.
    
    Returns
    -------
    is_over : `bool`
    """
    length = len(VALUE_QUOTE) << 1
    
    for character in string:
        length += _get_character_representation_length(character)
        if length > length_limit:
            return True
    
    return False


def _get_character_representation_escaped_length(character):
    """
    Gets the character's representation length if it would be escaped.
    
    Parameters
    ----------
    character : `str`
        Character to get its escaped length of.
    
    Returns
    -------
    length : `int`
    """
    character_int = ord(character)
    if character_int >= 0x10000 or character_int < 0:
        length = 2 + 8
    elif character_int >= 0x100:
        length = 2 + 4
    else:
        length = 2 + 2
    return length


def _get_character_representation_length(character):
    """
    Returns the character's length.
    
    Parameters
    ----------
    character : `str`
        Character to get its length of.
    
    Returns
    -------
    length : `int`
    """
    if character in ESCAPABLE:
        length = 2
    elif character.isprintable():
        length = 1
    else:
        length = _get_character_representation_escaped_length(character)
    
    return length


def _get_character_representation_escaped(character):
    """
    Escapes the given character.
    
    Parameters
    ----------
    character : `str`
        The character to escape.
    
    Returns
    -------
    result : `str`
    """
    character_int = ord(character)
    if character_int >= 0x10000 or character_int < 0:
        prefix = '\\U'
        hexadecimal_length = 8
    
    elif character_int >= 0x100:
        prefix = '\\u'
        hexadecimal_length = 4
    
    else:
        prefix = '\\x'
        hexadecimal_length = 2
    
    result = [prefix]
    for index in reversed(range(hexadecimal_length)):
        result.append('0123456789abcdef'[(character_int >> (index << 2)) & 0x0f])
    
    return ''.join(result)


def _get_character_representation(character):
    """
    Gets the character's representation.
    
    Parameters
    ----------
    character : `str`
        Character to represent.
    
    Returns
    --------
    representation : `str`
    """
    if character == VALUE_QUOTE:
        representation = '\\' + VALUE_QUOTE
    
    elif character == '\n':
        representation = '\\n'
    elif character == '\r':
        representation = '\\r'
    elif character == '\t':
        representation = '\\t'
    elif character == '\\':
        representation = '\\\\'
    elif character.isprintable():
        representation = character
    else:
        representation = _get_character_representation_escaped(character)
    
    return representation


def _wrap_begin(into, indent):
    """
    Begins wrapping.
    
    Parameters
    ----------
    into : `list<str>`
        A list to extend it's content.
    indent : `int`
        The amount of indents to add.
    
    Returns
    -------
    into : `list<tr>`
    """
    into.append('(\n')
        
    for index in range(indent + 1):
        into.append(VALUE_INDENT)
    
    return into


def _wrap_end(into, indent):
    """
    Ends wrapping.
    
    Parameters
    ----------
    into : `list<str>`
        A list to extend it's content.
    indent : `int`
        The amount of indents to add.
    
    Returns
    -------
    into : `list<tr>`
    """
    into.append('\n')
    
    for index in range(indent):
        into.append(VALUE_INDENT)
    
    into.append(')')
    
    return into
