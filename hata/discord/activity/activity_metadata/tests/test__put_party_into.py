import vampytest

from ...activity_party import ActivityParty

from ..fields import put_party_into


def test__put_party_into():
    """
    Tests whether ``put_party_into`` is working as intended.
    """
    party = ActivityParty(party_id = 'hell')
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (party, False, {'party': party.to_data()}),
        (party, True, {'party': party.to_data(defaults = True)}),
    ):
        data = put_party_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
