import vampytest

from ..parsing import (
    PARSED_STATE_END, PARSED_STATE_FAILURE, PARSED_STATE_SUCCESS, ParserState, chain_exhausters, exhaust_if
)


def CONDITION_0(character):
    return character == 'i'

def EXHAUSTER_0(parser_state):
    return exhaust_if(parser_state, CONDITION_0)


def CONDITION_1(character):
    return character == 'l'


def EXHAUSTER_1(parser_state):
    return exhaust_if(parser_state, CONDITION_1)


@vampytest.call_with('', 0, PARSED_STATE_END, 0)
@vampytest.call_with('a', 0, PARSED_STATE_FAILURE, 0)
@vampytest.call_with('a', 1, PARSED_STATE_END, 1)
@vampytest.call_with('i', 0, PARSED_STATE_SUCCESS | PARSED_STATE_END, 1)
@vampytest.call_with('ia', 0, PARSED_STATE_SUCCESS, 1)
@vampytest.call_with('a', 0, PARSED_STATE_FAILURE, 0)
@vampytest.call_with('ii', 0, PARSED_STATE_SUCCESS | PARSED_STATE_END, 2)
@vampytest.call_with('ll', 0, PARSED_STATE_SUCCESS | PARSED_STATE_END, 2)
@vampytest.call_with('iia', 0, PARSED_STATE_SUCCESS, 2)
@vampytest.call_with('lla', 0, PARSED_STATE_SUCCESS, 2)
@vampytest.call_with('alilia', 1, PARSED_STATE_SUCCESS, 5)
def test__chain_exhausters(value, position, expected_output, expected_position):
    """
    Tests whether ``chain_exhausters`` works as intended.
    """
    state = ParserState(value)
    state.position = position
    
    output = chain_exhausters(state, (EXHAUSTER_0, EXHAUSTER_1))
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, expected_output)
    vampytest.assert_eq(state.position, expected_position)
