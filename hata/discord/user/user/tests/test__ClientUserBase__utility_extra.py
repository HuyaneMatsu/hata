from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....bases import Icon, IconType
from ....client import Client
from ....color import Color
from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji
from ....guild import Guild
from ....role import Role

from ...guild_profile import GuildProfile

from ..client_user_base import ClientUserBase


def test__ClientUserBase__delete():
    """
    Tests whether ``ClientUserBase._delete` works as intended.
    """
    user_id = 202302060034
    guild_id = 202302060035
    
    user = ClientUserBase._create_empty(user_id)
    user.guild_profiles[guild_id] = GuildProfile()
    guild = Guild.precreate(guild_id)
    guild.users[user_id] = user
    
    user._delete()
    
    vampytest.assert_eq(user.guild_profiles, {})
    vampytest.assert_eq(guild.users, {})


def test__ClientUserBase__color_at():
    """
    Tests whether ``ClientUserBase.color_at` works as intended.
    """
    user_id = 202302060036
    guild_id = 202302060037
    role_id = 202302060072
    
    color = Color(23)
    
    user = ClientUserBase._create_empty(user_id)
    role = Role.precreate(role_id, color = color)
    user.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id])
    
    output = user.color_at(0)
    vampytest.assert_instance(output, Color)
    vampytest.assert_eq(output, 0)
    
    output = user.color_at(guild_id)
    vampytest.assert_instance(output, Color)
    vampytest.assert_eq(output, color)


def test__ClientUserBase__name_at__name():
    """
    Tests whether ``ClientUserBase.name_at` works as intended.
    
    Case: Just name.
    """
    user_id = 202305160002
    name = 'rin'
    
    user = ClientUserBase._create_empty(user_id)
    user.name = name
    
    output = user.name_at(0)
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, name)


def test__ClientUserBase__name_at__no_nick():
    """
    Tests whether ``ClientUserBase.name_at` works as intended.
    
    Case: In guild, but no nick.
    """
    user_id = 202305160003
    guild_id = 202302060004
    name = 'rin'
    
    user = ClientUserBase._create_empty(user_id)
    user.guild_profiles[guild_id] = GuildProfile()
    user.name = name
    
    output = user.name_at(guild_id)
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, name)


def test__ClientUserBase__name_at__with_nick():
    """
    Tests whether ``ClientUserBase.name_at` works as intended.
    
    Case: In guild, but no nick.
    """
    user_id = 202305160005
    guild_id = 202302060006
    name = 'rin'
    nick = 'orin'
    display_name = 'cat'
    
    user = ClientUserBase._create_empty(user_id)
    user.guild_profiles[guild_id] = GuildProfile(nick = nick)
    user.name = name
    user.display_name = display_name
    
    output = user.name_at(guild_id)
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, nick)


def test__ClientUserBase__name_at__with_display_name():
    """
    Tests whether ``ClientUserBase.name_at` works as intended.
    
    Case: Has display name.
    """
    user_id = 202302060007
    name = 'rin'
    display_name = 'cat'
    
    user = ClientUserBase._create_empty(user_id)
    user.name = name
    user.display_name = display_name
    
    output = user.name_at(0)
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, display_name)


def test__ClientUserBase__has_name_like_at():
    """
    Tests whether ``ClientUserBase.has_name_like_at`` works as intended.
    """
    name = 'orin'
    nick = 'hell'
    display_name = 'cat'
    
    user_id = 202302060041
    guild_id_0 = 202302060042
    guild_id_1 = 202302060043
    
    user = ClientUserBase._create_empty(user_id)
    user.name = name
    user.display_name = display_name
    
    user.guild_profiles[guild_id_0] = GuildProfile(nick = nick)
    user.guild_profiles[guild_id_1] = GuildProfile()
    
    for input_value, guild_id, expected_output in (
        ('Orin', 0, True),
        ('Okuu', 0, False),
        ('Cat', 0, True),
        ('Bird', 0, False),
        ('@orin', 0, True),
        ('@okuu', 0, False),
        ('orin#0000', 0, True),
        ('okuu#0000', 0, False),
        ('orin#0010', 0, False),
        ('rin', 0, True),
        ('hell', guild_id_0, True),
        ('hell', guild_id_1, False),
        ('hel', guild_id_0, True),
        ('hel', guild_id_1, False),
        ('hello', guild_id_0, False),
        ('hello', guild_id_1, False),
        ('@hel', guild_id_0, True),
        ('@hel', guild_id_1, False),
    ):
        vampytest.assert_eq(user.has_name_like_at(input_value, guild_id), expected_output)


def test__ClientUserBase__has_role():
    """
    Tests whether ``ClientUserBase.has_role`` works as intended.
    """
    user_id = 202302060044
    guild_id = 202302060045
    role_id = 202302060046
    
    user = ClientUserBase._create_empty(user_id)
    role = Role.precreate(role_id, guild_id = guild_id)
    guild = Guild.precreate(guild_id)
    
    output = user.has_role(role)
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)
    
    # No roles
    
    user.guild_profiles[guild_id] = GuildProfile()
    output = user.has_role(role)
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)
    
    # Default role
    default_role = Role.precreate(guild_id, guild_id = guild_id)
    guild.roles[guild_id] = default_role
    
    output = user.has_role(default_role)
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)
    
    # Has other role
    user.guild_profiles[guild_id] = GuildProfile(role_ids = [202302060047])
    output = user.has_role(role)
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)
    
    # has role
    
    user.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id])
    output = user.has_role(role)
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)


def test__ClientUserBase__top_role_at():
    """
    Tests whether ``ClientUserBase.top_role_at`` works as intended.
    """
    user_id = 202302060048
    guild_id = 202302060049
    role_id = 202302060050
    default = object()
    
    user = ClientUserBase._create_empty(user_id)
    role = Role.precreate(role_id, guild_id = guild_id)
    
    # No guild
    output = user.top_role_at(0, default = default)
    vampytest.assert_is(output, default)
    
    # Not in guild
    output = user.top_role_at(guild_id, default = default)
    vampytest.assert_is(output, default)
    
    # In guild, no roles
    user.guild_profiles[guild_id] = GuildProfile()
    output = user.top_role_at(guild_id, default = default)
    vampytest.assert_is(output, default)
    
    # In guild, no roles, guild has default role
    default_role = Role.precreate(guild_id, guild_id = guild_id)
    guild = Guild.precreate(guild_id)
    guild.roles[guild_id] = default_role
    
    output = user.top_role_at(guild_id, default = default)
    vampytest.assert_is(output, default_role)
    
    # In guild, has role
    
    user.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id])
    output = user.top_role_at(guild_id, default = default)
    vampytest.assert_is(output, role)


def test__ClientUserBase__can_use_emoji__unicode():
    """
    Tests whether ``ClientUserBase.can_use_emoji`` works as intended.
    
    Case: unicode.
    """
    user_id = 202510010090
    
    emoji = BUILTIN_EMOJIS['heart']
    
    user = ClientUserBase._create_empty(user_id)
    
    output = user.can_use_emoji(emoji)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__ClientUserBase__can_use_emoji__custom_allowed():
    """
    Tests whether ``ClientUserBase.can_use_emoji`` works as intended.
    
    Case: custom & allowed.
    """
    user_id = 202510010100
    guild_id = 202510010101
    emoji_id = 202510010102
    
    emoji = Emoji.precreate(
        emoji_id,
        guild_id = guild_id,
        name = 'hina',
    )
    
    role = Role.precreate(
        guild_id,
        guild_id = guild_id,
    )
    
    user = ClientUserBase._create_empty(user_id)
    user.guild_profiles[guild_id] = GuildProfile()
    
    guild = Guild.precreate(
        guild_id,
        emojis = [emoji],
        roles = [role],
        users = [user],
    )
    
    output = user.can_use_emoji(emoji)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__ClientUserBase__can_use_emoji__custom_emoji_deleted():
    """
    Tests whether ``ClientUserBase.can_use_emoji`` works as intended.
    
    Case: custom & emoji deleted.
    """
    user_id = 202511260010
    guild_id = 202511260011
    emoji_id = 202511260012
    
    emoji = Emoji.precreate(
        emoji_id,
        guild_id = guild_id,
        name = 'hina',
    )
    
    role = Role.precreate(
        guild_id,
        guild_id = guild_id,
    )
    
    user = ClientUserBase._create_empty(user_id)
    user.guild_profiles[guild_id] = GuildProfile()
    
    guild = Guild.precreate(
        guild_id,
        roles = [role],
        users = [user],
    )
    
    output = user.can_use_emoji(emoji)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__ClientUserBase__can_use_emoji__custom_not_available():
    """
    Tests whether ``ClientUserBase.can_use_emoji`` works as intended.
    
    Case: custom & not available.
    """
    user_id = 202510010110
    guild_id = 202510010111
    emoji_id = 202510010112
    
    emoji = Emoji.precreate(
        emoji_id,
        guild_id = guild_id,
        name = 'hina',
        available = False,
    )
    
    role = Role.precreate(
        guild_id,
        guild_id = guild_id,
    )
    
    user = ClientUserBase._create_empty(user_id)
    user.guild_profiles[guild_id] = GuildProfile()
    
    guild = Guild.precreate(
        guild_id,
        emojis = [emoji],
        roles = [role],
        users = [user],
    )
    
    output = user.can_use_emoji(emoji)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__ClientUserBase__can_use_emoji__custom_not_in_guild():
    """
    Tests whether ``ClientUserBase.can_use_emoji`` works as intended.
    
    Case: custom & not in guild.
    """
    user_id = 202510010120
    guild_id = 202510010121
    emoji_id = 202510010122
    
    emoji = Emoji.precreate(
        emoji_id,
        guild_id = guild_id,
        name = 'hina',
    )
    
    role = Role.precreate(
        guild_id,
        guild_id = guild_id,
    )
    
    user = ClientUserBase._create_empty(user_id)
    
    guild = Guild.precreate(
        guild_id,
        emojis = [emoji],
        roles = [role],
    )
    
    output = user.can_use_emoji(emoji)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__ClientUserBase__can_use_emoji__custom_role_bound_guild_owner():
    """
    Tests whether ``ClientUserBase.can_use_emoji`` works as intended.
    
    Case: custom & role bound & guild owner.
    """
    user_id = 202510010130
    guild_id = 202510010131
    emoji_id = 202510010132
    
    role_id_bound = 202510010143
    
    emoji = Emoji.precreate(
        emoji_id,
        guild_id = guild_id,
        name = 'hina',
        roles = [role_id_bound],
    )
    
    role = Role.precreate(
        guild_id,
        guild_id = guild_id,
    )
    
    user = ClientUserBase._create_empty(user_id)
    user.guild_profiles[guild_id] = GuildProfile()
    
    guild = Guild.precreate(
        guild_id,
        emojis = [emoji],
        roles = [role],
        users = [user],
        owner_id = user_id,
    )
    
    output = user.can_use_emoji(emoji)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__ClientUserBase__can_use_emoji__custom_role_bound_no_role():
    """
    Tests whether ``ClientUserBase.can_use_emoji`` works as intended.
    
    Case: custom & role bound & no role.
    """
    user_id = 202510010140
    guild_id = 202510010141
    emoji_id = 202510010142
    
    role_id_bound = 202510010143
    
    emoji = Emoji.precreate(
        emoji_id,
        guild_id = guild_id,
        name = 'hina',
        roles = [role_id_bound],
    )
    
    role = Role.precreate(
        guild_id,
        guild_id = guild_id,
    )
    
    user = ClientUserBase._create_empty(user_id)
    user.guild_profiles[guild_id] = GuildProfile()
    
    guild = Guild.precreate(
        guild_id,
        emojis = [emoji],
        roles = [role],
        users = [user],
    )
    
    output = user.can_use_emoji(emoji)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__ClientUserBase__can_use_emoji__custom_role_bound_no_role_intersection():
    """
    Tests whether ``ClientUserBase.can_use_emoji`` works as intended.
    
    Case: custom & role bound & no role intersection.
    """
    user_id = 202510010150
    guild_id = 202510010151
    emoji_id = 202510010152
    
    role_id_bound_0 = 202510010153
    role_id_bound_1 = 202510010154
    
    emoji = Emoji.precreate(
        emoji_id,
        guild_id = guild_id,
        name = 'hina',
        roles = [role_id_bound_0],
    )
    
    role = Role.precreate(
        guild_id,
        guild_id = guild_id,
    )
    
    user = ClientUserBase._create_empty(user_id)
    user.guild_profiles[guild_id] = GuildProfile(
        role_ids = [role_id_bound_1,]
    )
    
    guild = Guild.precreate(
        guild_id,
        emojis = [emoji],
        roles = [role],
        users = [user],
    )
    
    output = user.can_use_emoji(emoji)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__ClientUserBase__can_use_emoji__custom_role_bound_with_role_intersection():
    """
    Tests whether ``ClientUserBase.can_use_emoji`` works as intended.
    
    Case: custom & role bound & no role intersection.
    """
    user_id = 202510010160
    guild_id = 202510010161
    emoji_id = 202510010162
    
    role_id_bound = 202510010163
    
    emoji = Emoji.precreate(
        emoji_id,
        guild_id = guild_id,
        name = 'hina',
        roles = [role_id_bound],
    )
    
    role = Role.precreate(
        guild_id,
        guild_id = guild_id,
    )
    
    user = ClientUserBase._create_empty(user_id)
    user.guild_profiles[guild_id] = GuildProfile(
        role_ids = [role_id_bound,]
    )
    
    guild = Guild.precreate(
        guild_id,
        emojis = [emoji],
        roles = [role],
        users = [user],
    )
    
    output = user.can_use_emoji(emoji)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__ClientUserBase__has_higher_role_than():
    """
    Tests whether ``ClientUserBase.has_higher_role_than`` works as intended.
    """
    user_id = 202302060055
    guild_id = 202302060057
    role_id_0 = 202302060056
    role_id_1 = 202302060058
    role_id_2 = 202302060059
    
    user = ClientUserBase._create_empty(user_id)
    guild = Guild.precreate(guild_id)
    
    role_0 = Role.precreate(role_id_0, guild_id = guild_id, position = 2)
    role_1 = Role.precreate(role_id_1, guild_id = guild_id, position = 1)
    role_2 = Role.precreate(role_id_2, guild_id = guild_id, position = 3)
    
    # Not in guild
    
    output = user.has_higher_role_than(role_0)
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)
    
    # in guild -> owner
    
    user.guild_profiles[guild_id] = GuildProfile()
    guild.owner_id = user_id
    
    output = user.has_higher_role_than(role_0)
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)
    
    guild.owner_id = 0
    
    # in guild -> no roles
    
    output = user.has_higher_role_than(role_0)
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)
    
    # in guild -> has role, but lower
    
    user.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id_1])
    
    output = user.has_higher_role_than(role_0)
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)
    
    # in guild -> has role, but higher
    
    user.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id_2])
    
    output = user.has_higher_role_than(role_0)
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)
    
    # in guild -> has role, but same
    
    user.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id_0])
    
    output = user.has_higher_role_than(role_0)
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)
    

def test__ClientUserBase__has_higher_role_than_at():
    """
    Tests whether ``ClientUserBase.has_higher_role_than_at`` works as intended.
    """
    user_id_0 = 202302060060
    user_id_1 = 202302060061
    guild_id = 202302060062
    role_id_0 = 202302060063
    role_id_1 = 202302060064
    role_id_2 = 202302060065
    
    user_0 = ClientUserBase._create_empty(user_id_0)
    user_1 = ClientUserBase._create_empty(user_id_1)
    
    guild = Guild.precreate(guild_id)
    
    role_0 = Role.precreate(role_id_0, guild_id = guild_id, position = 2)
    role_1 = Role.precreate(role_id_1, guild_id = guild_id, position = 1)
    role_2 = Role.precreate(role_id_2, guild_id = guild_id, position = 3)
    
    # same user
    
    output = user_0.has_higher_role_than_at(user_0, 0)
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)
    
    # same user -> guild owner
    
    guild.owner_id = user_id_0
    output = user_0.has_higher_role_than_at(user_0, guild_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)
    guild.owner_id = 0
    
    # No guild
    
    output = user_0.has_higher_role_than_at(user_0, 0)
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)
    
    # self is not in the guild
    
    output = user_0.has_higher_role_than_at(user_0, guild_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)
    
    # self is the guild owner
    
    guild.owner_id = user_id_0
    user_0.guild_profiles[guild_id] = GuildProfile()
    user_1.guild_profiles[guild_id] = GuildProfile()
    output = user_0.has_higher_role_than_at(user_1, guild_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)
    guild.owner_id = 0
    
    # other not in the guild
    
    user_1.guild_profiles.pop(guild_id, None)
    output = user_0.has_higher_role_than_at(user_1, guild_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)
    
    # other is guild owner
    
    guild.owner_id = user_id_1
    user_1.guild_profiles[guild_id] = GuildProfile()
    output = user_0.has_higher_role_than_at(user_1, guild_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)
    guild.owner_id = 0
    
    # self has no top role
    
    output = user_0.has_higher_role_than_at(user_1, guild_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)
    
    # other has no top role
    
    user_0.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id_0])
    output = user_0.has_higher_role_than_at(user_1, guild_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)
    
    # same roles
    
    user_0.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id_0])
    user_1.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id_0])
    output = user_0.has_higher_role_than_at(user_1, guild_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)

    # lower roles
    
    user_0.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id_0])
    user_1.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id_2])
    output = user_0.has_higher_role_than_at(user_1, guild_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)

    # higher roles
    
    user_0.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id_0])
    user_1.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id_1])
    output = user_0.has_higher_role_than_at(user_1, guild_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)


def test__ClientUserBase__get_guild_profile_for():
    """
    Tests whether ``ClientUserBase.has_higher_role_than_at`` works as intended.
    """
    user_id = 202302060065
    guild_id_0 = 202302060066
    guild_id_1 = 202302060067
    
    user = ClientUserBase._create_empty(user_id)
    
    # No guild
    
    vampytest.assert_is(user.get_guild_profile_for(0), None)
    
    # other guild
    
    user.guild_profiles[guild_id_0] = GuildProfile()
    vampytest.assert_is(user.get_guild_profile_for(guild_id_1), None)
    
    # present guild
    
    guild_profile = GuildProfile()
    
    user.guild_profiles[guild_id_0] = guild_profile
    vampytest.assert_is(user.get_guild_profile_for(guild_id_0), guild_profile)


def test__ClientUserBase__iter_guilds_and_profiles():
    """
    Tests whether ``ClientUserBase.iter_guilds_and_profiles`` works as intended.
    """
    user_id = 202302060065
    guild_id_0 = 202302060066
    guild_id_1 = 202302060067
    
    user = ClientUserBase._create_empty(user_id)
    
    guild_0 = Guild.precreate(guild_id_0)
    guild_1 = Guild.precreate(guild_id_1)
    
    guild_profile_0 = GuildProfile(nick = 'orin')
    guild_profile_1 = GuildProfile(nick = 'rin')
    
    user.guild_profiles[guild_id_0] = guild_profile_0
    user.guild_profiles[guild_id_1] = guild_profile_1
    
    vampytest.assert_eq(
        {*user.iter_guilds_and_profiles()},
        {(guild_0, guild_profile_0), (guild_1, guild_profile_1),},
    )


def test__ClientUserBase__iter_guilds():
    """
    Tests whether ``ClientUserBase.iter_guilds`` works as intended.
    """
    user_id = 202302140000
    guild_id_0 = 202302140001
    guild_id_1 = 202302140002
    
    user = ClientUserBase._create_empty(user_id)
    
    guild_0 = Guild.precreate(guild_id_0)
    guild_1 = Guild.precreate(guild_id_1)
    
    guild_profile_0 = GuildProfile(nick = 'orin')
    guild_profile_1 = GuildProfile(nick = 'rin')
    
    user.guild_profiles[guild_id_0] = guild_profile_0
    user.guild_profiles[guild_id_1] = guild_profile_1
    
    vampytest.assert_eq(
        {*user.iter_guilds()},
        {guild_0, guild_1},
    )


def test__ClientUserBase__is_boosting():
    """
    Tests whether ``ClientUserBase.is_boosting`` works as intended.
    """
    user_id = 202302060068
    guild_id = 202302060069
    
    user = ClientUserBase._create_empty(user_id)
    
    # no guild
    
    output = user.is_boosting(0)
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)

    # not in guild
    
    output = user.is_boosting(guild_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)

    # in guild -> but pleb
    
    user.guild_profiles[guild_id] = GuildProfile()
    output = user.is_boosting(guild_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)

    # in guild -> but chad
    
    user.guild_profiles[guild_id] = GuildProfile(boosts_since = DateTime(2015, 1, 1, tzinfo = TimeZone.utc)) # Clearly chad
    output = user.is_boosting(guild_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)


def test__ClientUserBase__partial():
    """
    Tests whether ``ClientUserBase.partial`` works as intended.
    """
    user_id = 202302060070
    guild_id = 202302060071
    
    # Not in any guild
    
    user = ClientUserBase._create_empty(user_id)
    
    output = user.partial
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)
    
    # In partial guild
    
    guild = Guild.precreate(guild_id)
    user.guild_profiles[guild_id] = GuildProfile()
    
    output = user.partial
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)
    
    # non-partial guild
    
    client = Client(
        token = 'token_20230206_0002',
    )
    
    try:
        guild.clients.append(client)
        
        output = user.partial
        vampytest.assert_instance(output, bool)
        vampytest.assert_false(output)
    
    # Cleanup
    finally:
        client._delete()
        client = None


def _iter_options__avatar_url_for():
    yield 202506020020, 0, None, False
    yield 202506020021, 202506020022, None, False
    yield 202506020023, 202506020024, Icon(IconType.animated, 3), True


@vampytest._(vampytest.call_from(_iter_options__avatar_url_for()).returning_last())
def test__ClientUserBase__avatar_url_for(user_id, guild_id, icon):
    """
    Tests whether ``ClientUserBase.avatar_url_for`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        Identifier to create user with.
    
    guild_id : `int`
        Guild identifier to add guild profile for.
    
    icon : ``None | Icon``
        Icon to create the user with.
    
    Returns
    -------
    has_avatar_url_for : `bool`
    """
    user = ClientUserBase()
    user.id = user_id
    
    if guild_id:
        user.guild_profiles[guild_id] = GuildProfile(avatar = icon)
    
    output = user.avatar_url_for(guild_id)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__avatar_url_for_as():
    yield 202506020025, 0, None, {'ext': 'webp', 'size': 128}, False
    yield 202506020026, 202506020027, None, {'ext': 'webp', 'size': 128}, False
    yield 202506020028, 202506020029, Icon(IconType.animated, 3), {'ext': 'webp', 'size': 128}, True


@vampytest._(vampytest.call_from(_iter_options__avatar_url_for_as()).returning_last())
def test__ClientUserBase__avatar_url_for_as(user_id, guild_id, icon, keyword_parameters):
    """
    Tests whether ``ClientUserBase.avatar_url_for_as`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        Identifier to create user with.
    
    guild_id : `int`
        Guild identifier to add guild profile for.
    
    icon : ``None | Icon``
        Icon to create the user with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    has_avatar_url_for : `bool`
    """
    user = ClientUserBase()
    user.id = user_id
    
    if guild_id:
        user.guild_profiles[guild_id] = GuildProfile(avatar = icon)
    
    output = user.avatar_url_for_as(guild_id, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)

def _iter_options__avatar_url_at():
    yield 202506020030, None, 0, None, True
    yield 202506020031, Icon(IconType.animated, 3), 0, None, True
    yield 202506020033, None, 202506020034, None, True
    yield 202506020035, None, 202506020036, Icon(IconType.static, 2), True
    yield 202506020037, Icon(IconType.static, 3), 202506020038, Icon(IconType.static, 2), True


@vampytest._(vampytest.call_from(_iter_options__avatar_url_at()).returning_last())
def test__ClientUserBase__avatar_url_at(user_id, global_icon, guild_id, local_icon):
    """
    Tests whether ``ClientUserBase.avatar_url_at`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        Identifier to create user with.
    
    global_icon : ``None | Icon``
        Icon to create the user with.
    
    guild_id : `int`
        Guild identifier to add guild profile at.
    
    local_icon : ``None | Icon``
        Icon to create the user with.
    
    Returns
    -------
    has_avatar_url_at : `bool`
    """
    user = ClientUserBase(
        avatar = global_icon
    )
    user.id = user_id
    
    if guild_id:
        user.guild_profiles[guild_id] = GuildProfile(avatar = local_icon)
    
    output = user.avatar_url_at(guild_id)
    vampytest.assert_instance(output, str)
    return True


def _iter_options__avatar_url_at_as():
    yield 202506020039, None, 0, None, {'ext': 'webp', 'size': 128}, True
    yield 202506020040, Icon(IconType.animated, 3), 0, None, {'ext': 'webp', 'size': 128}, True
    yield 202506020041, None, 202506020042, None, {'ext': 'webp', 'size': 128}, True
    yield 202506020043, None, 202506020044, Icon(IconType.static, 2), {'ext': 'webp', 'size': 128}, True
    yield (
        202506020045,
        Icon(IconType.static, 3),
        202506020046,
        Icon(IconType.static, 2),
        {'ext': 'webp', 'size': 128},
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__avatar_url_at_as()).returning_last())
def test__ClientUserBase__avatar_url_at_as(user_id, global_icon, guild_id, local_icon, keyword_parameters):
    """
    Tests whether ``ClientUserBase.avatar_url_at_as`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        Identifier to create user with.
    
    global_icon : ``None | Icon``
        Icon to create the user with.
    
    guild_id : `int`
        Guild identifier to add guild profile at.
    
    local_icon : ``None | Icon``
        Icon to create the user with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    has_avatar_url_at : `bool`
    """
    user = ClientUserBase(
        avatar = global_icon
    )
    user.id = user_id
    
    if guild_id:
        user.guild_profiles[guild_id] = GuildProfile(avatar = local_icon)
    
    output = user.avatar_url_at_as(guild_id, **keyword_parameters)
    vampytest.assert_instance(output, str)
    return True


def _iter_options__banner_url_for():
    yield 202506020065, 0, None, False
    yield 202506020066, 202506020067, None, False
    yield 202506020068, 202506020069, Icon(IconType.animated, 3), True


@vampytest._(vampytest.call_from(_iter_options__banner_url_for()).returning_last())
def test__ClientUserBase__banner_url_for(user_id, guild_id, icon):
    """
    Tests whether ``ClientUserBase.banner_url_for`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        Identifier to create user with.
    
    guild_id : `int`
        Guild identifier to add guild profile for.
    
    icon : ``None | Icon``
        Icon to create the user with.
    
    Returns
    -------
    has_banner_url_for : `bool`
    """
    user = ClientUserBase()
    user.id = user_id
    
    if guild_id:
        user.guild_profiles[guild_id] = GuildProfile(banner = icon)
    
    output = user.banner_url_for(guild_id)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__banner_url_for_as():
    yield 202506020070, 0, None, {'ext': 'webp', 'size': 128}, False
    yield 202506020071, 202506020072, None, {'ext': 'webp', 'size': 128}, False
    yield 202506020073, 202506020074, Icon(IconType.animated, 3), {'ext': 'webp', 'size': 128}, True


@vampytest._(vampytest.call_from(_iter_options__banner_url_for_as()).returning_last())
def test__ClientUserBase__banner_url_for_as(user_id, guild_id, icon, keyword_parameters):
    """
    Tests whether ``ClientUserBase.banner_url_for_as`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        Identifier to create user with.
    
    guild_id : `int`
        Guild identifier to add guild profile for.
    
    icon : ``None | Icon``
        Icon to create the user with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    has_banner_url_for : `bool`
    """
    user = ClientUserBase()
    user.id = user_id
    
    if guild_id:
        user.guild_profiles[guild_id] = GuildProfile(banner = icon)
    
    output = user.banner_url_for_as(guild_id, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)

def _iter_options__banner_url_at():
    yield 202506020075, None, 0, None, False
    yield 202506020076, Icon(IconType.animated, 3), 0, None, True
    yield 202506020077, None, 202506020079, None, False
    yield 202506020078, None, 202506020080, Icon(IconType.static, 2), True
    yield 202506020081, Icon(IconType.static, 3), 202506020082, Icon(IconType.static, 2), True


@vampytest._(vampytest.call_from(_iter_options__banner_url_at()).returning_last())
def test__ClientUserBase__banner_url_at(user_id, global_icon, guild_id, local_icon):
    """
    Tests whether ``ClientUserBase.banner_url_at`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        Identifier to create user with.
    
    global_icon : ``None | Icon``
        Icon to create the user with.
    
    guild_id : `int`
        Guild identifier to add guild profile at.
    
    local_icon : ``None | Icon``
        Icon to create the user with.
    
    Returns
    -------
    has_banner_url_at : `bool`
    """
    user = ClientUserBase(
        banner = global_icon
    )
    user.id = user_id
    
    if guild_id:
        user.guild_profiles[guild_id] = GuildProfile(banner = local_icon)
    
    output = user.banner_url_at(guild_id)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__banner_url_at_as():
    yield 202506020083, None, 0, None, {'ext': 'webp', 'size': 128}, False
    yield 202506020084, Icon(IconType.animated, 3), 0, None, {'ext': 'webp', 'size': 128}, True
    yield 202506020085, None, 202506020086, None, {'ext': 'webp', 'size': 128}, False
    yield 202506020087, None, 202506020088, Icon(IconType.static, 2), {'ext': 'webp', 'size': 128}, True
    yield (
        202506020089,
        Icon(IconType.static, 3),
        202506020090,
        Icon(IconType.static, 2),
        {'ext': 'webp', 'size': 128},
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__banner_url_at_as()).returning_last())
def test__ClientUserBase__banner_url_at_as(user_id, global_icon, guild_id, local_icon, keyword_parameters):
    """
    Tests whether ``ClientUserBase.banner_url_at_as`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        Identifier to create user with.
    
    global_icon : ``None | Icon``
        Icon to create the user with.
    
    guild_id : `int`
        Guild identifier to add guild profile at.
    
    local_icon : ``None | Icon``
        Icon to create the user with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    has_banner_url_at : `bool`
    """
    user = ClientUserBase(
        banner = global_icon
    )
    user.id = user_id
    
    if guild_id:
        user.guild_profiles[guild_id] = GuildProfile(banner = local_icon)
    
    output = user.banner_url_at_as(guild_id, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)
