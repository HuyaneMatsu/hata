import vampytest

from ..fields import put_name_into


def test__put_name_into():
    """
    Tests whether ``put_name_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        ('', False, {'name': ''}),
        ('a', False, {'name': 'a'}),
    ):
        data = put_name_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
