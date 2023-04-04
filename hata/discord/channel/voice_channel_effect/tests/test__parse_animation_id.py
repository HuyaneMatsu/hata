import vampytest

from ..fields import parse_animation_id


def test__parse_animation_id():
    """
    Tests whether ``parse_animation_id`` works as intended.
    """
    animation_id = 202304030011
    
    for input_data, expected_output in (
        ({}, 0),
        ({'animation_id': None}, 0),
        ({'animation_id': str(animation_id)}, animation_id),
    ):
        output = parse_animation_id(input_data)
        vampytest.assert_eq(output, expected_output)
