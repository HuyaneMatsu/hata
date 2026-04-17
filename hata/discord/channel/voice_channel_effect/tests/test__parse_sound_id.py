import vampytest

from ..fields import parse_sound_id


def _iter_options():
    sound_id = 202408180000
    
    yield {}, 0
    yield {'sound_id': None}, 0
    yield {'sound_id': str(sound_id)}, sound_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_sound_id(input_data):
    """
    Tests whether ``parse_sound_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_sound_id(input_data)
    vampytest.assert_instance(output, int)
    return output
