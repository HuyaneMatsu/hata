import vampytest

from ..fields import parse_sound_volume


def _iter_options():
    yield {}, 1.0
    yield {'sound_volume': 0.0}, 0.0
    yield {'sound_volume': 0.5}, 0.5
    yield {'sound_volume': 1.0}, 1.0


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_sound_volume(input_data):
    """
    Tests whether ``parse_sound_volume`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `float`
    """
    output = parse_sound_volume(input_data)
    vampytest.assert_instance(output, float)
    return output
