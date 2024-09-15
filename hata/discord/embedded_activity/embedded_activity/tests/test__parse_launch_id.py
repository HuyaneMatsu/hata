import vampytest

from ..fields import parse_launch_id


def _iter_options():
    launch_id = 202409010064

    yield {}, 0
    yield {'launch_id': None}, 0
    yield {'launch_id': str(launch_id)}, launch_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_launch_id(input_data):
    """
    Tests whether ``parse_launch_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_launch_id(input_data)
    vampytest.assert_instance(output, int)
    return output
