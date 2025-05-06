import vampytest

from ..fields import put_width


def test__put_width():
    """
    Tests whether ``put_width`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (0, False, {'width': 0}),
    ):
        data = put_width(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
