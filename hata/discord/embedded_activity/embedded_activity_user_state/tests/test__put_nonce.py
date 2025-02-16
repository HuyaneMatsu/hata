import vampytest

from ..fields import put_nonce


def _iter_options():
    yield None, False, {}
    yield None, True, {'nonce': None}
    yield 'Orin', False, {'nonce': 'Orin'}
    yield 'Orin', True, {'nonce': 'Orin'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_nonce(nonce, defaults):
    """
    Tests whether ``put_nonce`` works as intended.
    
    Parameters
    ---------
    nonce : `None | str`
        The value to serialize.
    defaults : `bool`
        Whether defaults should be included as well.
    
    Returns
    -------
    output_data : `dict<str, object>`
    """
    return put_nonce(nonce, {}, defaults)
