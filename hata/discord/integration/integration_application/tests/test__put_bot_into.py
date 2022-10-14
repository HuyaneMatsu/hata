import vampytest

from ....user import User, ZEROUSER

from ..fields import put_bot_into


def test__put_bot_into():
    """
    Tests whether ``put_bot_into`` is working as intended.
    """
    user = User.precreate(202210080010, name = 'Ken', bot = True)
    
    for input_, defaults, expected_output in (
        (ZEROUSER, True, {'bot': None}),
        (ZEROUSER, False, {}),
        (user, True, {'bot': user.to_data()}),
    ):
        data = put_bot_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
