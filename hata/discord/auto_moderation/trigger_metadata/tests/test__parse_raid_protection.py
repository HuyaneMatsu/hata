import vampytest

from ..fields import parse_raid_protection


def _iter_options():
    yield {}, False
    yield {'mention_raid_protection_enabled': None}, False
    yield {'mention_raid_protection_enabled': False}, False
    yield {'mention_raid_protection_enabled': True}, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_raid_protection(input_data):
    """
    Tests whether ``parse_raid_protection`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    output = parse_raid_protection(input_data)
    vampytest.assert_instance(output, bool)
    return output
