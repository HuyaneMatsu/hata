import vampytest

from ..fields import put_bot_require_code_grant_into


def test__put_bot_require_code_grant_into():
    """
    Tests whether ``put_bot_require_code_grant_into`` works as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'bot_require_code_grant': False}),
        (True, False, {'bot_require_code_grant': True}),
    ):
        data = put_bot_require_code_grant_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
