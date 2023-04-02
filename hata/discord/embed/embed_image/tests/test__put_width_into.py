import vampytest

from ..fields import put_width_into


def test__put_width_into():
    """
    Tests whether ``put_width_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (0, False, {'width': 0}),
    ):
        data = put_width_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
