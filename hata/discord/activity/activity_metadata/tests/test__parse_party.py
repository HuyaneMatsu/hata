import vampytest

from ...activity_party import ActivityParty

from ..fields import parse_party


def test__parse_party():
    """
    Tests whether ``parse_party`` works as intended.
    """
    party = ActivityParty(party_id = 'hell')
    
    for input_data, expected_output in (
        ({}, None),
        ({'party': None}, None),
        ({'party': party.to_data()}, party),
    ):
        output = parse_party(input_data)
        vampytest.assert_eq(output, expected_output)
