import vampytest

from ..fields import put_values_into


def test__put_values_into():
    """
    Tests whether ``put_values_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'values': []}),
        (('a', ), False, {'values': ['a']}),
    ):
        data = put_values_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
