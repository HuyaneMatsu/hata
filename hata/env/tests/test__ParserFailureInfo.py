import vampytest

from ..parsing import ParserFailureInfo, ParserState


def _assert_fields_set(parser_failure_info):
    """
    Asserts whether every attributes are set of the given
    
    Parameters
    ----------
    parser_failure_info : ``ParserFailureInfo``
        The parser failure info to check.
    """
    vampytest.assert_instance(parser_failure_info, ParserFailureInfo)
    vampytest.assert_instance(parser_failure_info.error_code, int)
    vampytest.assert_instance(parser_failure_info.index, int)
    vampytest.assert_instance(parser_failure_info.line, str)
    vampytest.assert_instance(parser_failure_info.line_index, int)


def test__ParserFailureInfo__new():
    """
    Tests whether ``ParserFailureInfo.__new__`` works as intended.
    """
    error_code = 4
    index = 2
    line = 'hello'
    line_index = 6
    
    parser_failure_info = ParserFailureInfo(index, line, line_index, error_code)
    _assert_fields_set(parser_failure_info)
    
    vampytest.assert_eq(parser_failure_info.error_code, error_code)
    vampytest.assert_eq(parser_failure_info.index, index)
    vampytest.assert_eq(parser_failure_info.line, line)
    vampytest.assert_eq(parser_failure_info.line_index, line_index)


def test__ParserFailureInfo__from_parser_state__0():
    """
    Tests whether ``ParserFailureInfo.from_parser_state`` works as intended.
    
    Case: Expected input.
    """
    error_code = 4
    
    parser_state = ParserState('\nhello \nhi')
    parser_state.position = 3
    parser_state.line_start = 1
    parser_state.line_index = 1
    
    parser_failure_info = ParserFailureInfo.from_parser_state(parser_state, error_code)
    _assert_fields_set(parser_failure_info)
    
    vampytest.assert_eq(parser_failure_info.error_code, error_code)
    vampytest.assert_eq(parser_failure_info.index, 2)
    vampytest.assert_eq(parser_failure_info.line, 'hello')
    vampytest.assert_eq(parser_failure_info.line_index, 1)


def test__ParserFailureInfo__from_parser_state__1():
    """
    Tests whether ``ParserFailureInfo.from_parser_state`` works as intended.
    
    Case: End of line.
    """
    error_code = 4
    
    parser_state = ParserState('\nhello \nhi')
    parser_state.position = 6
    parser_state.line_start = 1
    parser_state.line_index = 1
    
    parser_failure_info = ParserFailureInfo.from_parser_state(parser_state, error_code)
    _assert_fields_set(parser_failure_info)
    
    vampytest.assert_eq(parser_failure_info.error_code, error_code)
    vampytest.assert_eq(parser_failure_info.index, 5)
    vampytest.assert_eq(parser_failure_info.line, 'hello')
    vampytest.assert_eq(parser_failure_info.line_index, 1)


def test__ParserFailureInfo__from_parser_state__2():
    """
    Tests whether ``ParserFailureInfo.from_parser_state`` works as intended.
    
    Case: End of content.
    """
    error_code = 4
    
    parser_state = ParserState('\naa')
    parser_state.position = 3
    parser_state.line_start = 1
    parser_state.line_index = 1
    
    parser_failure_info = ParserFailureInfo.from_parser_state(parser_state, error_code)
    _assert_fields_set(parser_failure_info)
    
    vampytest.assert_eq(parser_failure_info.error_code, error_code)
    vampytest.assert_eq(parser_failure_info.index, 2)
    vampytest.assert_eq(parser_failure_info.line, 'aa')
    vampytest.assert_eq(parser_failure_info.line_index, 1)


def test__ParserFailureInfo__repr():
    """
    Tests whether ``ParserFailureInfo.__repr__`` works as intended.
    
    Case: Expected input.
    """
    error_code = 4
    index = 2
    line = 'hello'
    line_index = 6
    
    parser_failure_info = ParserFailureInfo(index, line, line_index, error_code)
    vampytest.assert_instance(repr(parser_failure_info), str)


def test__ParserFailureInfo__eq():
    """
    Tests whether ``ParserFailureInfo.__eq__`` works as intended.
    """
    error_code = 4
    index = 2
    line = 'hello'
    line_index = 6
    
    keyword_parameters = {
        'error_code': error_code,
        'index': index,
        'line': line,
        'line_index': line_index,
    }
    
    parser_failure_info = ParserFailureInfo(**keyword_parameters)
    vampytest.assert_eq(parser_failure_info, parser_failure_info)
    vampytest.assert_ne(parser_failure_info, object())
    
    
    for field_name, field_value in (
        ('error_code', 3),
        ('index', 1),
        ('line', 'ayaya'),
        ('line_index', 3),
    ):
        test_parser_failure_info = ParserFailureInfo(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(parser_failure_info, test_parser_failure_info)


def test__ParserFailureInfo__hash():
    """
    Tests whether ``ParserFailureInfo.__hash__`` works as intended.
    
    Case: Expected input.
    """
    error_code = 4
    index = 2
    line = 'hello'
    line_index = 6
    
    parser_failure_info = ParserFailureInfo(index, line, line_index, error_code)
    vampytest.assert_instance(hash(parser_failure_info), int)


def test__ParserFailureInfo__get_error_message():
    """
    Test whether ``ParserFailureInfo.get_error_message`` works as intended.
    """
    output = ParserFailureInfo(0, '', 0, 1).get_error_message()
    vampytest.assert_instance(output, str)
    
    output = ParserFailureInfo(0, '', 0, -1).get_error_message()
    vampytest.assert_is(output, None)
