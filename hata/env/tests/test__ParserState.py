import vampytest

from ..parsing import ParserState


def _assert_fields_set(parser_state):
    """
    Asserts whether every fields are set of the given parser state.
    
    Parameters
    ----------
    parser_state : ``ParserState``
        The parser state to check.
    """
    vampytest.assert_instance(parser_state, ParserState)
    vampytest.assert_instance(parser_state.end, int)
    vampytest.assert_instance(parser_state.position, int)
    vampytest.assert_instance(parser_state.value, list)


def test__ParserState__new():
    """
    Tests whether ``ParserState.__new__`` works as intended.
    """
    value = 'Koishi'
    
    parser_state = ParserState(value)
    _assert_fields_set(parser_state)
    
    vampytest.assert_eq(parser_state.end, len(value))
    vampytest.assert_eq(parser_state.position, 0)
    vampytest.assert_eq(parser_state.get_value_in_range(0, len(value)), value)


def test__ParserState__repr():
    """
    Tests whether ``ParserState.__repr__`` works as intended.
    """
    value = 'Koishi'
    
    parser_state = ParserState(value)
    
    vampytest.assert_instance(repr(parser_state), str)


def test__ParserState__get_value_in_range():
    """
    Tests whether ``ParserState.get_value_in_range`` works as intended.
    """
    value = 'Koish'
    start = 1
    end = 4
    
    parser_state = ParserState(value)
    
    output = parser_state.get_value_in_range(start, end)
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, value[start : end])
