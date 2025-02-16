import vampytest

from ..fields import put_image_small


def test__put_image_small():
    """
    Tests whether ``put_image_small`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        ('a', False, {'small_image': 'a'}),
    ):
        data = put_image_small(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
