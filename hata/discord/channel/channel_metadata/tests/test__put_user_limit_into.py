import vampytest

from ..constants import USER_LIMIT_DEFAULT
from ..fields import put_user_limit_into


def test__put_user_limit_into():
    """
    Tests whether ``put_user_limit_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (USER_LIMIT_DEFAULT, False, {'user_limit': USER_LIMIT_DEFAULT}),
        (1, False, {'user_limit': 1}),
    ):
        data = put_user_limit_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
