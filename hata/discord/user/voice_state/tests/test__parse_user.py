import vampytest

from ...guild_profile import GuildProfile
from ...user import ClientUserBase, User

from ..fields import parse_user


def _iter_options():
    user_0 = User.precreate(202311110000, name = 'Yuuka')
    user_1 = User.precreate(202311110001, name = 'Yuuka')
    guild_profile_0 = GuildProfile(nick = 'Yukkuri')
    guild_id_0 = 202311110002
    
    yield {}, 0, None, None
    yield {'user': None}, 0, None, None
    yield {'user': user_0.to_data(include_internals = True)}, 0, user_0, {}
    yield {'user': user_0.to_data(include_internals = True)}, guild_id_0, user_0, {}
    yield (
        {
            'member': {
                'user': user_0.to_data(include_internals = True),
                **guild_profile_0.to_data(include_internals = True),
            },
        },
        0,
        user_0,
        {},
    )
    yield (
        {
            'member': {
                'user': user_1.to_data(include_internals = True),
                **guild_profile_0.to_data(include_internals = True),
            },
        },
        guild_id_0,
        user_1,
        {guild_id_0: guild_profile_0},
    )


@vampytest.call_from(_iter_options())
def test__parse_user(input_data, guild_id, expected_output, expected_guild_profiles):
    """
    Tests whether ``parse_user`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    guild_id : `int`
        Respective guild identifier to create form for as applicable.
    expected_output : `None | ClientUserBase`
        The expected user to be parsed.
    excepted_guild_profiles : `None | dict<int, GuildProfile>`
        The user's guild profile's expected to be parsed.
    """
    output = parse_user(input_data, guild_id)
    vampytest.assert_instance(output, ClientUserBase, nullable = True)
    vampytest.assert_is(output, expected_output)
    if (output is not None):
        vampytest.assert_eq(output.guild_profiles, expected_guild_profiles)
