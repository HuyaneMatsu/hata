import vampytest

from ...activity_party import ActivityParty

from ..fields import put_party


def _iter_options():
    party = ActivityParty(party_id = 'hell')
    
    yield (None, False, {})
    yield (None, True, {'party': None})
    yield (party, False, {'party': party.to_data()})
    yield (party, True, {'party': party.to_data(defaults = True)})


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_party(input_value, defaults):
    """
    Tests whether ``put_party`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | ActivityParty`
        Value to serialise.
    defaults : `bool`
        Whether fields with their default value should be included.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_party(input_value, {}, defaults)
