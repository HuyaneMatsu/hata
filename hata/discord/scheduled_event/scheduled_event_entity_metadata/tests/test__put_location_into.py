import vampytest

from ..fields import put_location_into


def test__put_location_into():
    """
    Tests whether ``put_location_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {'location': ''}),
        ('a', False, {'location': 'a'}),
    ):
        data = put_location_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
