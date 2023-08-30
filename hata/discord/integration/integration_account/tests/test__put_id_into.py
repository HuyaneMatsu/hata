import vampytest

from ..fields import put_id_into


def _iter_options():
    integration_account_id = 'koishi'
    yield '', False, {'id': ''}
    yield '', True, {'id': ''}
    yield integration_account_id, False, {'id': integration_account_id}
    yield integration_account_id, True, {'id': integration_account_id}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_id_into(input_value, defaults):
    """
    Tests whether ``put_id_into`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_id_into(input_value, {}, defaults)
