import vampytest

from ..fields import put_temporary_into


def test__put_temporary_into():
    """
    Tests whether ``put_temporary_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'ephemeral': False}),
        (True, False, {'ephemeral': True}),
    ):
        data = put_temporary_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
