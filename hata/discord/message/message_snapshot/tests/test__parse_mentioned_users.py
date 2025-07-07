import vampytest

from ....user import ClientUserBase, GuildProfile, User

from ..fields import parse_mentioned_users


def _iter_options():
    user_0 = User.precreate(202407200002)
    user_1 = User.precreate(202407200003)
    
    yield {}, None
    yield {'message': None}, None
    yield {'message': {}}, None
    yield {'message': {'mentions': None}}, None
    yield {'message': {'mentions': []}}, None
    yield (
        {'message': {'mentions': [user_0.to_data(include_internals = True), user_1.to_data(include_internals = True)]}},
        (user_0, user_1),
    )
    yield (
        {'message': {'mentions': [user_1.to_data(include_internals = True), user_0.to_data(include_internals = True)]}},
        (user_0, user_1),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_mentioned_users(input_data):
    """
    Tests whether ``parse_mentioned_users`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | tuple<ClientUserBase>``
    """
    output = parse_mentioned_users(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, ClientUserBase)
    
    return output


def test__parse_mentioned_users__with_guild_profile():
    """
    Tests whether ``parse_mentioned_users`` works as intended.
    
    Case: with guild profile.
    """
    user_id_0 = 202407200004
    user_id_1 = 202407200005
    guild_id = 202407200006
    name_0 = 'Orin'
    name_1 = 'Okuu'
    nick_0 = 'Dancing cat'
    
    input_data = {
        'message': {
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
                },
            ],
        },
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
