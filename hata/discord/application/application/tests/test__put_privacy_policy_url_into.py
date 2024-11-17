import vampytest

from ..fields import put_privacy_policy_url_into


def _iter_options():
    yield None, False, {}
    yield 'https://orindance.party/', False, {'privacy_policy_url': 'https://orindance.party/'}
    yield None, True, {'privacy_policy_url': None}
    yield 'https://orindance.party/', True, {'privacy_policy_url': 'https://orindance.party/'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_privacy_policy_url_into(input_value, defaults):
    """
    Tests whether ``put_privacy_policy_url_into`` is working as intended.
    
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
    return put_privacy_policy_url_into(input_value, {}, defaults)
