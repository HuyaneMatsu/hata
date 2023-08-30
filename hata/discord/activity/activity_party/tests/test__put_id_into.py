import vampytest

from ..fields import put_id_into


def _iter_options():
    activity_party_id = 'koishi'
    
    yield None, False, {}
    yield None, True, {'id': ''}
    yield activity_party_id, False, {'id': activity_party_id}
    yield activity_party_id, True, {'id': activity_party_id}


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
