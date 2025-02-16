import vampytest

from ..fields import put_separated


def test__put_separated():
    """
    Tests whether ``put_separated`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'hoist': False}),
        (True, False, {'hoist': True}),
    ):
        data = put_separated(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
