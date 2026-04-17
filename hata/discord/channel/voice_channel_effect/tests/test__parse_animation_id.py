import vampytest

from ..fields import parse_animation_id


def _iter_options():
    animation_id = 202304030011
    
    yield {}, 0
    yield {'animation_id': None}, 0
    yield {'animation_id': str(animation_id)}, animation_id
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_animation_id(input_data):
    """
    Tests whether ``parse_animation_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_animation_id(input_data)
    vampytest.assert_instance(output, int)
    return output
