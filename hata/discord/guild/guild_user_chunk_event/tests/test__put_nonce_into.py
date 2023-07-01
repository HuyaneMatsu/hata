import vampytest

from ..fields import put_nonce_into


def _iter_options():
    yield None, False, {}
    yield None, True, {'nonce': None}
    yield 'Orin', False, {'nonce': 'Orin'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_nonce_into(nonce, defaults):
    """
    Tests whether ``put_nonce_into`` works as intended.
    
    Parameters
    ---------
    nonce : `None | str`
        The nonce to serialize.
    defaults : `bool`
        Whether default should be included as well in the output.
    
    Returns
    -------
    output_data : `dict<str, object>`
    """
    return put_nonce_into(nonce, {}, defaults)
