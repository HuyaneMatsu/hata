import vampytest

from ..fields import put_placeholder_into


def test__put_placeholder_into():
    """
    Tests whether ``put_placeholder_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        ('a', False, {'placeholder': 'a'}),
    ):
        data = put_placeholder_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
