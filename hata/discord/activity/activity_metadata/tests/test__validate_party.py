import vampytest

from ...activity_party import ActivityParty

from ..fields import validate_party


def test__validate_party__0():
    """
    Tests whether `validate_party` works as intended.
    
    Case: passing.
    """
    party = ActivityParty(party_id = 'hell')
    
    for input_value, expected_output in (
        (None, None),
        (party, party),
    ):
        output = validate_party(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_party__1():
    """
    Tests whether `validate_party` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_party(input_value)
