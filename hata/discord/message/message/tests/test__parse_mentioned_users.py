import vampytest

from ....user import ClientUserBase, GuildProfile

from ..fields import parse_mentioned_users


def test__parse_mentioned_users__0():
    """
    Tests whether ``parse_mentioned_users`` works as intended.
    
    Case: No input.
    """
    for input_data in (
        {},
        {'mentions': None},
        {'mentions': []},
    ):
        output = parse_mentioned_users(input_data)
        vampytest.assert_is(output, None)


def test__parse_mentioned_users__1():
    """
    Tests whether ``parse_mentioned_users`` works as intended.
    
    Case: Users.
    """
    user_id_0 = 202305010000
    user_id_1 = 202305010001
    guild_id = 202305010002
    name_0 = 'Orin'
    name_1 = 'Okuu'
    nick_0 = 'Dancing cat'
    
    input_data = {
        'mentions': [
            {
                'id': str(user_id_0),
                'name': name_0,
                'member': {
                    'nick': nick_0,
                }
            },
            {
                'id': str(user_id_1),
                'name': name_1,
            }
        ]
    }
    
    output = parse_mentioned_users(input_data, guild_id)
    
    vampytest.assert_is_not(output, None)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    
    vampytest.assert_instance(output[0], ClientUserBase)
    vampytest.assert_eq(output[0].id, user_id_0)
    vampytest.assert_eq(output[0].name, name_0)
    vampytest.assert_eq(output[0].guild_profiles, {guild_id: GuildProfile(nick = nick_0)})
    
    vampytest.assert_instance(output[1], ClientUserBase)
    vampytest.assert_eq(output[1].id, user_id_1)
    vampytest.assert_eq(output[1].name, name_1)
    vampytest.assert_eq(output[1].guild_profiles, {})
