import vampytest

from ...activity_party import ActivityParty

from ..fields import validate_party


def _iter_options__passing():
    party = ActivityParty(party_id = 'hell')
    
    yield None, None
    yield party, party


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_party(input_value):
    """
    Tests whether `validate_party` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | ActivityParty`
    
    Raises
    ------
    TypeError
    """
    output = validate_party(input_value)
    vampytest.assert_instance(output, ActivityParty, nullable = True)
    return output
