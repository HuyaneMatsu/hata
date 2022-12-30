import vampytest

from ..fields import parse_image_large


def test__parse_image_large():
    """
    Tests whether ``parse_image_large`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'large_image': None}, None),
        ({'large_image': ''}, None),
        ({'large_image': 'a'}, 'a'),
    ):
        output = parse_image_large(input_data)
        vampytest.assert_eq(output, expected_output)
