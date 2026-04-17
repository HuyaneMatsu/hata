import vampytest

from ..fields import put_activity_name


def test__put_activity_name():
    """
    Tests whether ``put_activity_name`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'game': {'name': ''}}),
        ('a', False, {'game': {'name': 'a'}}),
    ):
        data = put_activity_name(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
