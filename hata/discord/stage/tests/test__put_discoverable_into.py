import vampytest

from ..fields import put_discoverable_into


def test__put_discoverable_into():
    """
    Tests whether ``put_discoverable_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (True, False, {}),
        (True, True, {'discoverable_disabled': False}),
        (False, False, {'discoverable_disabled': True}),
    ):
        data = put_discoverable_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
