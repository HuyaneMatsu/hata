import vampytest

from ...activity_party import ActivityParty

from ..fields import parse_party


def _iter_options():
    party = ActivityParty(party_id = 'hell')
    
    yield ({}, None)
    yield ({'party': None}, None)
    yield ({'party': party.to_data()}, party)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_party(input_data):
    """
    Tests whether ``parse_party`` works as intended.
    
    Parameters
    ----------
    input_data : dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | ActivityParty`
    """
    output = parse_party(input_data)
    vampytest.assert_instance(output, ActivityParty, nullable = True)
    return output
