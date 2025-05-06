import vampytest

from ..fields import put_value


def test__put_value():
    """
    Tests whether ``put_value`` works as intended.
    """
    value = 1
    
    for input_value, defaults, expected_output in (
        (value, False, {'id': value}),
    ):
        data = put_value(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
