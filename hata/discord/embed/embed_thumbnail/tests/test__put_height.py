import vampytest

from ..fields import put_height


def test__put_height():
    """
    Tests whether ``put_height`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (0, False, {'height': 0}),
    ):
        data = put_height(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
