import vampytest

from ..parsing import ParserState, is_at_end


@vampytest.call_with('', 0, True)
@vampytest.call_with(' ', 0, False)
@vampytest.call_with(' ', 1, True)
def test__is_at_end(value, position, expected_output):
    """
    Tests whether ``is_at_end`` works as intended.
    """
    state = ParserState(value)
    state.position = position
    
    output = is_at_end(state)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, expected_output)
