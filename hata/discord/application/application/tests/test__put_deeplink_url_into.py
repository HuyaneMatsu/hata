import vampytest

from ..fields import put_deeplink_url_into


def _iter_options():
    yield None, False, {}
    yield 'https://orindance.party/', False, {'deeplink_uri': 'https://orindance.party/'}
    yield None, True, {'deeplink_uri': None}
    yield 'https://orindance.party/', True, {'deeplink_uri': 'https://orindance.party/'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_deeplink_url_into(input_value, defaults):
    """
    Tests whether ``put_deeplink_url_into`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Value to serialize.
    
    defaults : `bool`
        Whether values with their defaults should be also serialized.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_deeplink_url_into(input_value, {}, defaults)
