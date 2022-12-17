import vampytest

from ..fields import put_separated_into


def test__put_separated_into():
    """
    Tests whether ``put_separated_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'hoist': False}),
        (True, False, {'hoist': True}),
    ):
        data = put_separated_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
