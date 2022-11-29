import vampytest

from ..fields import put_hook_into


def test__put_hook_into():
    """
    Tests whether ``put_hook_into`` works as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'hook': False}),
        (True, False, {'hook': True}),
    ):
        data = put_hook_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
