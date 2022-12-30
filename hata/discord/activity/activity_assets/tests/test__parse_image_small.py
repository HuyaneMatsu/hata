import vampytest

from ..fields import parse_image_small


def test__parse_image_small():
    """
    Tests whether ``parse_image_small`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'small_image': None}, None),
        ({'small_image': ''}, None),
        ({'small_image': 'a'}, 'a'),
    ):
        output = parse_image_small(input_data)
        vampytest.assert_eq(output, expected_output)
