import vampytest

from ..parsing import (
    PARSED_STATE_END, PARSED_STATE_FAILURE, PARSED_STATE_SUCCESS, ParserState, exhaust_if, repeat_exhauster
)


def CONDITION(character):
    return character == 'i'


def EXHAUSTER(parser_state):
    # i -> SUCCESS | END
    # ii -> SUCCESS
    # a -> FAIL
    # ia -> SUCCESS
    parsed_state = exhaust_if(parser_state, CONDITION)
    if parsed_state & PARSED_STATE_END:
        return parsed_state
    
    if parsed_state & PARSED_STATE_SUCCESS:
        if exhaust_if(parser_state, CONDITION) & PARSED_STATE_END:
            parsed_state |= PARSED_STATE_END
        
        return parsed_state
    
    return PARSED_STATE_FAILURE


@vampytest.call_with('', 0, PARSED_STATE_END, 0)
@vampytest.call_with('a', 0, PARSED_STATE_FAILURE, 0)
@vampytest.call_with('a', 1, PARSED_STATE_END, 1)
@vampytest.call_with('i', 0, PARSED_STATE_SUCCESS | PARSED_STATE_END, 1)
@vampytest.call_with('ia', 0, PARSED_STATE_SUCCESS, 1)
@vampytest.call_with('a', 0, PARSED_STATE_FAILURE, 0)
@vampytest.call_with('ii', 0, PARSED_STATE_SUCCESS | PARSED_STATE_END, 2)
@vampytest.call_with('iia', 0, PARSED_STATE_SUCCESS, 2)
def test__repeat_exhauster(value, position, expected_output, expected_position):
    """
    Tests whether ``repeat_exhauster`` works as intended.
    """
    state = ParserState(value)
    state.position = position
    
    output = repeat_exhauster(state, EXHAUSTER)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, expected_output)
    vampytest.assert_eq(state.position, expected_position)
