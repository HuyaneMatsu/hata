import vampytest

from ..fields import put_value_into


def test__put_value_into():
    """
    Tests whether ``put_value_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        ('', False, {'value': ''}),
        ('a', False, {'value': 'a'}),
    ):
        data = put_value_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
