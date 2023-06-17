import vampytest

from ..fields import put_afk_channel_id_into


def iter_options():
    afk_channel_id = 202306080001
    
    yield 0, False, {}
    yield 0, True, {'afk_channel_id': None}
    yield afk_channel_id, False, {'afk_channel_id': str(afk_channel_id)}


@vampytest._(vampytest.call_from(iter_options()).returning_last())
def test__put_afk_channel_id_into(input_value, defaults):
    """
    Tests whether ``put_afk_channel_id_into`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The input value.
    defaults : `bool`
        Whether fields of default values should be included within the output as well.
    """
    return put_afk_channel_id_into(input_value, {}, defaults)
