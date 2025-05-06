import vampytest

from ..fields import put_value


def test__put_value():
    """
    Tests whether ``put_value`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {'value': None}),
        (None, True, {'value': None}),
        ('a', False, {'value': 'a'}),
        (12.6, False, {'value': 12.6}),
        (6, False, {'value': 6}),
    ):
        data = put_value(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
