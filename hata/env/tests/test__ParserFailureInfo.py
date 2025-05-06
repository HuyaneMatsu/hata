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


def test__ParserFailureInfo__from_parser_state__expected_input():
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


def test__ParserFailureInfo__from_parser_state__end_of_line():
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


def test__ParserFailureInfo__from_parser_state__end_of_content():
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


def _iter_options__eq():
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
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'error_code': 3,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'index': 1,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'line': 'ayaya',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'line_index': 3,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ParserFailureInfo__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ParserFailureInfo.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    parser_failure_info_0 = ParserFailureInfo(**keyword_parameters_0)
    parser_failure_info_1 = ParserFailureInfo(**keyword_parameters_1)
    
    output = parser_failure_info_0 == parser_failure_info_1
    vampytest.assert_instance(output, bool)
    return output


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
