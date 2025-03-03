import vampytest

from ..fields import put_custom_install_url


def _iter_options():
    yield None, False, {}
    yield 'https://orindance.party/', False, {'custom_install_url': 'https://orindance.party/'}
    yield None, True, {'custom_install_url': None}
    yield 'https://orindance.party/', True, {'custom_install_url': 'https://orindance.party/'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_custom_install_url(input_value, defaults):
    """
    Tests whether ``put_custom_install_url`` is working as intended.
    
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
    return put_custom_install_url(input_value, {}, defaults)
