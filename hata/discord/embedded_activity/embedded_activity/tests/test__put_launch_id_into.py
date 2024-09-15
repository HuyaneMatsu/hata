import vampytest

from ..fields import put_launch_id_into


def _iter_options():
    launch_id = 202409010065

    yield 0, False, {'launch_id': None}
    yield 0, True, {'launch_id': None}
    yield launch_id, False, {'launch_id': str(launch_id)}
    yield launch_id, True, {'launch_id': str(launch_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_launch_id_into(input_value, defaults):
    """
    Tests whether ``put_launch_id_into`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_launch_id_into(input_value, {}, defaults)
