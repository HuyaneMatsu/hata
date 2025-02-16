import vampytest

from ..fields import put_image_large


def test__put_image_large():
    """
    Tests whether ``put_image_large`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        ('a', False, {'large_image': 'a'}),
    ):
        data = put_image_large(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
