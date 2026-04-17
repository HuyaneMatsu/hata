import vampytest

from ..fields import put_raid_protection


def _iter_options():
    yield False, False, {}
    yield False, True, {'mention_raid_protection_enabled': False}
    yield True, False, {'mention_raid_protection_enabled': True}
    yield True, True, {'mention_raid_protection_enabled': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_raid_protection(input_value, defaults):
    """
    Tests whether ``put_raid_protection`` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_raid_protection(input_value, {}, defaults)
