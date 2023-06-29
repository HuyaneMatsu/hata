import vampytest

from ....client import Client
from ....guild import Guild
from ....permission import Permission
from ....role import Role
from ....user import GuildProfile, User, VoiceState

from ...channel import Channel
from ...forum_tag import ForumTag

from ..preinstanced import ChannelType

from .test__Channel__constructor import _assert_fields_set


def test__Channel__copy():
    """
    Tests whether ``Channel.copy`` works as intended.
    """
    channel_type = ChannelType.guild_text
    name = 'Yuuka'
    
    channel = Channel(
        channel_type = channel_type,
        name = name,
    )
    
    copy = channel.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(channel, copy)
    
    vampytest.assert_eq(channel, copy)


def test__Channel__copy_with__0():
    """
    Tests whether ``Channel.copy_with`` works as intended.
    
    Case: No fields given.
    """
    channel_type = ChannelType.guild_text
    name = 'Yuuka'
    
    channel = Channel(
        channel_type = channel_type,
        name = name,
    )
    
    copy = channel.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(channel, copy)
    
    vampytest.assert_eq(channel, copy)


def test__Channel__copy_with__1():
    """
    Tests whether ``Channel.copy_with`` works as intended.
    
    Case: Fields given.
    """
    old_channel_type = ChannelType.guild_text
    old_name = 'Yuuka'
    
    new_channel_type = ChannelType.guild_voice
    new_name = 'koishi'
    
    channel = Channel(
        channel_type = old_channel_type,
        name = old_name,
    )
    
    copy = channel.copy_with(
        channel_type = new_channel_type,
        name = new_name,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(channel, copy)
    
    vampytest.assert_is(copy.type, new_channel_type)
    vampytest.assert_eq(copy.name, new_name)


def test__Channel__get_user__0():
    """
    Tests whether ``Channel.get_user`` works as intended.
    
    Case: private.
    """
    channel_id = 202209200021
    user_name = 'Cross World'
    user_discriminator = 69
    
    user = User.precreate(202209200020, name = user_name, discriminator = user_discriminator)
    channel = Channel.precreate(channel_id, channel_type = ChannelType.private, users = [user])
    
    for input_value, expected_output in (
        ('hello', None),
        (user.name, user),
        (user.full_name, user),
    ):
        output = channel.get_user(input_value)
        vampytest.assert_is(output, expected_output)


def test__Channel__get_user__1():
    """
    Tests whether ``Channel.get_user`` works as intended.
    
    Case: guild.
    """
    channel_id = 202209200022
    guild_id = 202209200023
    user_name = 'Cross World'
    user_discriminator = 69
    
    user = User.precreate(202209200024, name = user_name, discriminator = user_discriminator)
    user.guild_profiles[guild_id] = GuildProfile()
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id)
    role = Role.precreate(guild_id, guild_id = guild_id, permissions = Permission().update_by_keys(view_channel = True))
    guild = Guild.precreate(guild_id)
    guild.roles[guild_id] = role
    guild.users[user.id] = user
    
    for input_value, expected_output in (
        ('hello', None),
        (user.name, user),
        (user.full_name, user),
    ):
        output = channel.get_user(input_value)
        vampytest.assert_is(output, expected_output)


def test__Channel__get_user_like__0():
    """
    Tests whether ``Channel.get_user_like`` works as intended.
    
    Case: private.
    """
    channel_id = 202209200025
    user_name = 'Cross World'
    user_discriminator = 69
    user_display_name = 'Far East'
    
    user = User.precreate(
        202209200026,
        name = user_name,
        discriminator = user_discriminator,
        display_name = user_display_name,
    )
    channel = Channel.precreate(channel_id, channel_type = ChannelType.private, users = [user])
    
    for input_value, expected_output in (
        ('hello', None),
        (user.name, user),
        (user.name[:-2], user),
        (user.full_name, user),
        (user.display_name, user),
        (user.display_name[:-2], user),
    ):
        output = channel.get_user_like(input_value)
        vampytest.assert_is(output, expected_output)



def test__Channel__get_user_like__1():
    """
    Tests whether ``Channel.get_user_like`` works as intended.
    
    Case: guild.
    """
    channel_id = 202209200027
    guild_id = 202209200028
    user_name = 'Cross World'
    user_discriminator = 69
    user_display_name = 'Far East'
    
    user = User.precreate(
        202209200029,
        name = user_name,
        discriminator = user_discriminator,
        display_name = user_display_name,
    )
    user.guild_profiles[guild_id] = GuildProfile()
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id)
    role = Role.precreate(guild_id, guild_id = guild_id, permissions = Permission().update_by_keys(view_channel = True))
    guild = Guild.precreate(guild_id)
    guild.roles[guild_id] = role
    guild.users[user.id] = user
    
    for input_value, expected_output in (
        ('hello', None),
        (user.name, user),
        (user.name[:-2], user),
        (user.full_name, user),
        (user.display_name, user),
        (user.display_name[:-2], user),
    ):
        output = channel.get_user_like(input_value)
        vampytest.assert_is(output, expected_output)


def test__Channel__get_users_like__0():
    """
    Tests whether ``Channel.get_users_like`` works as intended.
    
    Case: private.
    """
    channel_id = 202209200030
    user_name = 'Cross World'
    user_discriminator = 69
    user_display_name = 'Far East'
    
    user = User.precreate(
        202209200031,
        name = user_name,
        discriminator = user_discriminator,
        display_name = user_display_name,
    )
    channel = Channel.precreate(channel_id, channel_type = ChannelType.private, users = [user])
    
    for input_value, expected_output in (
        ('hello', []),
        (user.name, [user]),
        (user.name[:-2], [user]),
        (user.full_name, [user]),
        (user.display_name, [user]),
        (user.display_name[:-2], [user]),
    ):
        output = channel.get_users_like(input_value)
        vampytest.assert_instance(output, list)
        vampytest.assert_eq(output, expected_output)



def test__Channel__get_users_like__1():
    """
    Tests whether ``Channel.get_users_like`` works as intended.
    
    Case: guild.
    """
    channel_id = 202209200032
    guild_id = 202209200033
    user_name = 'Cross World'
    user_discriminator = 69
    user_display_name = 'Far East'
    
    user = User.precreate(
        202209200034,
        name = user_name,
        discriminator = user_discriminator,
        display_name = user_display_name,
    )
    user.guild_profiles[guild_id] = GuildProfile()
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id)
    role = Role.precreate(guild_id, guild_id = guild_id, permissions = Permission().update_by_keys(view_channel = True))
    guild = Guild.precreate(guild_id)
    guild.roles[guild_id] = role
    guild.users[user.id] = user
    
    for input_value, expected_output in (
        ('hello', []),
        (user.name, [user]),
        (user.name[:-2], [user]),
        (user.full_name, [user]),
        (user.display_name, [user]),
        (user.display_name[:-2], [user]),
    ):
        output = channel.get_users_like(input_value)
        vampytest.assert_instance(output, list)
        vampytest.assert_eq(output, expected_output)


def test__Channel__users__0():
    """
    Tests whether ``Channel.users`` works as intended.
    
    Case: private.
    """
    channel_id = 202209200035
    user = User.precreate(202209200036)
    channel = Channel.precreate(channel_id, channel_type = ChannelType.private, users = [user])
    
    users = channel.users
    vampytest.assert_instance(users, list)
    vampytest.assert_eq(users, [user])


def test__Channel__users__1():
    """
    Tests whether ``Channel.users`` works as intended.
    
    Case: private.
    """
    channel_id = 202209200037
    guild_id = 202209200038
    
    user = User.precreate(202209200039)
    user.guild_profiles[guild_id] = GuildProfile()
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id)
    role = Role.precreate(guild_id, guild_id = guild_id, permissions = Permission().update_by_keys(view_channel = True))
    guild = Guild.precreate(guild_id)
    guild.roles[guild_id] = role
    guild.users[user.id] = user
    
    users = channel.users
    vampytest.assert_instance(users, list)
    vampytest.assert_eq(users, [user])


def test__Channel__iter_users__0():
    """
    Tests whether ``Channel.iter_users`` works as intended.
    
    Case: private.
    """
    channel_id = 202209200040
    
    user = User.precreate(202209200041)
    channel = Channel.precreate(channel_id, channel_type = ChannelType.private, users = [user])
    
    iter_users = channel.iter_users()
    vampytest.assert_true(hasattr(iter_users, '__next__'))
    vampytest.assert_eq([*iter_users], [user])


def test__Channel__iter_users__1():
    """
    Tests whether ``Channel.iter_users`` works as intended.
    
    Case: private.
    """
    channel_id = 202209200042
    guild_id = 202209200043
    
    user = User.precreate(202209200044)
    user.guild_profiles[guild_id] = GuildProfile()
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id)
    role = Role.precreate(guild_id, guild_id = guild_id, permissions = Permission().update_by_keys(view_channel = True))
    guild = Guild.precreate(guild_id)
    guild.roles[guild_id] = role
    guild.users[user.id] = user
    
    iter_users = channel.iter_users()
    vampytest.assert_true(hasattr(iter_users, '__next__'))
    vampytest.assert_eq([*iter_users], [user])


def test__Channel__has_name_like():
    """
    Tests whether ``Channel.has_name_like`` works as intended.
    
    Case: private.
    """
    channel_name = 'Senya'
    channel_id = 202209200045
    
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, name = channel_name)
    
    for input_value, expected_output in (
        ('king', False),
        (channel_name, True),
        (channel_name[:-2], True),
        ('#' + channel_name, True),
    ):
        output = channel.has_name_like(input_value)
        
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Channel__permissions_for_roles():
    """
    Tests whether `channel.permissions_for_roles` wont raise when called and returns the correct type.
    
    TODO add extra test cases.
    """
    channel = Channel.precreate(202208150000)
    permission = channel.permissions_for_roles()
    vampytest.assert_instance(permission, Permission)


def test__Channel__permissions_for():
    """
    Tests whether `channel.permissions_for` wont raise when called and returns the correct type.
    
    TODO add extra test cases.
    """
    channel = Channel.precreate(202209200046)
    user = User.precreate(202209200047)
    
    permission = channel.permissions_for(user)
    vampytest.assert_instance(permission, Permission)


def test__Channel__cached_permissions_for():
    """
    Tests whether `channel.cached_permissions_for` wont raise when called and returns the correct type.
    """
    client = Client(
        token = 'token_20220909_0003',
    )
    
    try:
        channel = Channel.precreate(202209200048)
        
        permission = channel.cached_permissions_for(client)
        vampytest.assert_instance(permission, Permission)
    
    # Cleanup
    finally:
        client._delete()
        client = None
        clients = None


def test__Channel__checks():
    """
    Tests whether ``Channel`` checks work.
    """
    channel_type = ChannelType.guild_voice
    
    channel = Channel(channel_type = channel_type)
    
    for check, expected_output in (
        (Channel.is_in_group_textual, True),
        (Channel.is_in_group_guild_textual, True),
        (Channel.is_in_group_guild_system, False),
        (Channel.is_in_group_connectable, True),
        (Channel.is_in_group_guild_connectable, True),
        (Channel.is_in_group_private, False),
        (Channel.is_in_group_guild, True),
        (Channel.is_in_group_thread, False),
        (Channel.is_in_group_threadable, False),
        (Channel.is_in_group_invitable, True),
        (Channel.is_in_group_guild_sortable, True),
        (Channel.is_guild_text, False),
        (Channel.is_private, False),
        (Channel.is_guild_voice, True),
        (Channel.is_private_group, False),
        (Channel.is_guild_category, False),
        (Channel.is_guild_announcements, False),
        (Channel.is_guild_store, False),
        (Channel.is_thread, False),
        (Channel.is_guild_thread_announcements, False),
        (Channel.is_guild_thread_public, False),
        (Channel.is_guild_thread_private, False),
        (Channel.is_guild_stage, False),
        (Channel.is_guild_directory, False),
        (Channel.is_guild_forum, False),
    ):
        output = check(channel)
        vampytest.assert_instance(output, int)
        if expected_output:
            vampytest.assert_true(output)
        else:
            vampytest.assert_false(output)


def test__Channel__iter_applied_tag_ids():
    """
    Tests whether ``Channel.iter_applied_tag_ids`` works as intended.
    """
    for applied_tag_ids in (
        [],
        [202209270000],
    ):
        channel = Channel(channel_type = ChannelType.guild_thread_public, applied_tag_ids = applied_tag_ids)
        
        vampytest.assert_eq(applied_tag_ids, [*channel.iter_applied_tag_ids()])


def test__Channel__iter_applied_tags():
    """
    Tests whether ``Channel.iter_applied_tags`` works as intended.
    """
    for applied_tags in (
        [],
        [ForumTag.precreate(202209270001)],
    ):
        channel = Channel(
            channel_type = ChannelType.guild_thread_public,
            applied_tag_ids = [tag.id for tag in applied_tags],
        )
        
        vampytest.assert_eq(applied_tags, [*channel.iter_applied_tags()])


def test__Channel__iter_available_tags():
    """
    Tests whether ``Channel.iter_available_tags`` works as intended.
    """
    for available_tags in (
        [],
        [ForumTag.precreate(202209270002)],
    ):
        channel = Channel(
            channel_type = ChannelType.guild_forum,
            available_tags = available_tags,
        )
        
        vampytest.assert_eq(available_tags, [*channel.iter_available_tags()])


def test__Channel__delete__0():
    """
    Tests whether ``Channel._delete`` works as intended.
    
    Case: private.
    """
    client_id = 202211090000
    channel_id = 202211090001
    user_id = 202211090002
    
    client = Client(
        token = 'token_20221209_0000',
        client_id = client_id,
    )
    
    try:
        user = User.precreate(user_id)
        
        channel = Channel.precreate(channel_id, channel_type = ChannelType.private, users = [client, user])
        client.private_channels[user_id] = channel
        
        channel._delete(client)
        
        vampytest.assert_not_in(user_id, client.private_channels)
    
    # Cleanup
    finally:
        client._delete()
        client = None


def test__Channel__delete__1():
    """
    Tests whether ``Channel._delete`` works as intended.
    
    Case: group.
    """
    client_id = 202211090003
    channel_id = 202211090004
    
    client = Client(
        token = 'token_20221209_0001',
        client_id = client_id,
    )
    
    try:
        channel = Channel.precreate(channel_id, channel_type = ChannelType.private_group)
        client.group_channels[channel_id] = channel
        
        channel._delete(client)
        
        vampytest.assert_not_in(channel_id, client.group_channels)
    
    # Cleanup
    finally:
        client._delete()
        client = None


def test__Channel__delete__2():
    """
    Tests whether ``Channel._delete`` works as intended.
    
    Case: guild main.
    """
    guild_id = 202211090005
    channel_id = 202211090006
    
    guild = Guild.precreate(guild_id)
    
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_category, guild_id = guild_id)
    guild.channels[channel_id] = channel
    
    channel._delete(None)
    
    vampytest.assert_not_in(channel_id, guild.channels)


def test__Channel__delete__3():
    """
    Tests whether ``Channel._delete`` works as intended.
    
    Case: guild thread.
    """
    guild_id = 202211090007
    channel_id = 202211090008
    
    guild = Guild.precreate(guild_id)
    
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_thread_public, guild_id = guild_id)
    guild.threads[channel_id] = channel
    
    channel._delete(None)
    
    vampytest.assert_not_in(channel_id, guild.threads)


def test__Channel__iter_threads():
    """
    Tests whether ``Channel.iter_threads` works as intended.
    """
    channel_id_0 = 202211090009
    channel_id_1 = 202211090010
    channel_id_2 = 202211090011
    guild_id = 202211090012
    
    guild = Guild.precreate(guild_id)
    channel = Channel.precreate(channel_id_0, channel_type = ChannelType.guild_text, guild_id = guild_id)
    thread_0 = Channel.precreate(
        channel_id_1, channel_type = ChannelType.guild_thread_public, parent_id = channel_id_0, guild_id = guild_id
    )
    thread_1 = Channel.precreate(
        channel_id_2, channel_type = ChannelType.guild_thread_public, parent_id = channel_id_0, guild_id = guild_id
    )
    
    guild.channels[channel_id_0] = channel
    guild.threads[channel_id_1] = thread_0
    guild.threads[channel_id_2] = thread_1
    
    vampytest.assert_eq({*channel.iter_threads()}, {thread_0, thread_1})


def test__Channel__threads():
    """
    Tests whether ``Channel.threads` works as intended.
    """
    channel_id_0 = 202211090013
    channel_id_1 = 202211090014
    channel_id_2 = 202211090015
    guild_id = 202211090016
    
    guild = Guild.precreate(guild_id)
    channel = Channel.precreate(channel_id_0, channel_type = ChannelType.guild_text, guild_id = guild_id)
    thread_0 = Channel.precreate(
        channel_id_1, channel_type = ChannelType.guild_thread_public, parent_id = channel_id_0, guild_id = guild_id
    )
    thread_1 = Channel.precreate(
        channel_id_2, channel_type = ChannelType.guild_thread_public, parent_id = channel_id_0, guild_id = guild_id
    )
    
    guild.channels[channel_id_0] = channel
    guild.threads[channel_id_1] = thread_0
    guild.threads[channel_id_2] = thread_1
    
    output = channel.threads
    vampytest.assert_instance(output, list)
    vampytest.assert_eq({*output}, {thread_0, thread_1})


def test__Channel__iter_delete__0():
    """
    Tests whether ``Channel._iter_delete`` works as intended.
    
    Case: private.
    """
    client_id = 202211090017
    channel_id = 202211090018
    user_id = 202211090019
    
    client = Client(
        token = 'token_20221209_0002',
        client_id = client_id,
    )
    
    try:
        user = User.precreate(user_id)
        
        channel = Channel.precreate(channel_id, channel_type = ChannelType.private, users = [client, user])
        client.private_channels[user_id] = channel
        
        channels = {*channel._iter_delete(client)}
        
        vampytest.assert_eq(channels, {channel})
        vampytest.assert_not_in(user_id, client.private_channels)
    
    # Cleanup
    finally:
        client._delete()
        client = None


def test__Channel__iter_delete__1():
    """
    Tests whether ``Channel._iter_delete`` works as intended.
    
    Case: group.
    """
    client_id = 202211090020
    channel_id = 202211090021
    
    client = Client(
        token = 'token_20221209_0003',
        client_id = client_id,
    )
    
    try:
        channel = Channel.precreate(channel_id, channel_type = ChannelType.private_group)
        client.group_channels[channel_id] = channel
        
        channels = {*channel._iter_delete(client)}
        
        vampytest.assert_eq(channels, {channel})
        vampytest.assert_not_in(channel_id, client.group_channels)
    
    # Cleanup
    finally:
        client._delete()
        client = None


def test__Channel__iter_delete__2():
    """
    Tests whether ``Channel._iter_delete`` works as intended.
    
    Case: guild main.
    """
    guild_id = 202211090022
    channel_id = 202211090023
    
    guild = Guild.precreate(guild_id)
    
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_category, guild_id = guild_id)
    guild.channels[channel_id] = channel
    
    channels = {*channel._iter_delete(None)}
    
    vampytest.assert_eq(channels, {channel})
    vampytest.assert_not_in(channel_id, guild.channels)


def test__Channel__iter_delete__3():
    """
    Tests whether ``Channel._iter_delete`` works as intended.
    
    Case: guild thread.
    """
    guild_id = 202211090024
    channel_id = 202211090025
    
    guild = Guild.precreate(guild_id)
    
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_thread_public, guild_id = guild_id)
    guild.threads[channel_id] = channel
    
    channels = {*channel._iter_delete(None)}
    
    vampytest.assert_eq(channels, {channel})
    vampytest.assert_not_in(channel_id, guild.threads)


def test__Channel__iter_delete__4():
    """
    Tests whether ``Channel._iter_delete`` works as intended.
    
    Case: guild thread.
    """
    guild_id = 202211090026
    channel_id = 202211090027
    
    guild = Guild.precreate(guild_id)
    
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_thread_public, guild_id = guild_id)
    guild.threads[channel_id] = channel
    
    channels = {*channel._iter_delete(None)}
    
    vampytest.assert_eq(channels, {channel})
    vampytest.assert_not_in(channel_id, guild.threads)


def test__Channel__iter_delete__5():
    """
    Tests whether ``Channel._iter_delete`` works as intended.
    
    Case: guild forum.
    """
    guild_id = 202211090026
    channel_id_0 = 202211090027
    channel_id_1 = 202211090028
    channel_id_2 = 202211090029
    
    
    guild = Guild.precreate(guild_id)
    
    channel = Channel.precreate(channel_id_0, channel_type = ChannelType.guild_forum, guild_id = guild_id)
    thread_0 = Channel.precreate(
        channel_id_1, channel_type = ChannelType.guild_thread_public, parent_id = channel_id_0, guild_id = guild_id
    )
    thread_1 = Channel.precreate(
        channel_id_2, channel_type = ChannelType.guild_thread_public, parent_id = channel_id_0, guild_id = guild_id
    )
    
    guild.channels[channel_id_0] = channel
    guild.threads[channel_id_1] = thread_0
    guild.threads[channel_id_2] = thread_1
    
    
    channels = {*channel._iter_delete(None)}
    
    vampytest.assert_eq(channels, {channel, thread_0, thread_1})
    vampytest.assert_not_in(channel_id_0, guild.channels)
    vampytest.assert_not_in(channel_id_1, guild.threads)
    vampytest.assert_not_in(channel_id_2, guild.threads)


def test__Channel__iter_channels():
    """
    Tests whether ``Channel.iter_channels` works as intended.
    """
    channel_id_0 = 202304130070
    channel_id_1 = 202304130071
    channel_id_2 = 202304130072
    guild_id = 202304130073
    
    guild = Guild.precreate(guild_id)
    channel = Channel.precreate(channel_id_0, channel_type = ChannelType.guild_category, guild_id = guild_id)
    channel_0 = Channel.precreate(
        channel_id_1, channel_type = ChannelType.guild_text, parent_id = channel_id_0, guild_id = guild_id
    )
    channel_1 = Channel.precreate(
        channel_id_2, channel_type = ChannelType.guild_text, parent_id = channel_id_0, guild_id = guild_id
    )
    
    guild.channels[channel_id_0] = channel
    guild.channels[channel_id_1] = channel_0
    guild.channels[channel_id_2] = channel_1
    
    vampytest.assert_eq({*channel.iter_channels()}, {channel_0, channel_1})


def test__Channel__channels():
    """
    Tests whether ``Channel.channels` works as intended.
    """
    channel_id_0 = 202304130074
    channel_id_1 = 202304130075
    channel_id_2 = 202304130076
    guild_id = 202304130077
    
    guild = Guild.precreate(guild_id)
    channel = Channel.precreate(channel_id_0, channel_type = ChannelType.guild_category, guild_id = guild_id)
    channel_0 = Channel.precreate(
        channel_id_1, channel_type = ChannelType.guild_text, parent_id = channel_id_0, guild_id = guild_id
    )
    channel_1 = Channel.precreate(
        channel_id_2, channel_type = ChannelType.guild_text, parent_id = channel_id_0, guild_id = guild_id
    )
    
    guild.channels[channel_id_0] = channel
    guild.channels[channel_id_1] = channel_0
    guild.channels[channel_id_2] = channel_1
    
    output = channel.channels
    vampytest.assert_instance(output, list)
    vampytest.assert_eq({*output}, {channel_0, channel_1})


def test__Channel__iter_voice_users():
    """
    Tests whether ``Channel.iter_voice_users`` works as intended.
    """
    channel_id_0 = 202304130078
    channel_id_1 = 202304130083
    guild_id = 202304130079
    user_id_0 = 202304130080
    user_id_1 = 202304130081
    user_id_2 = 202304130082
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    user_2 = User.precreate(user_id_2)
    
    channel_0 = Channel.precreate(channel_id_0, channel_type = ChannelType.guild_voice, guild_id = guild_id)
    channel_1 = Channel.precreate(channel_id_1, channel_type = ChannelType.guild_voice, guild_id = guild_id)
    
    guild = Guild.precreate(guild_id)
    
    guild.voice_states[user_id_0] = VoiceState(channel_id = channel_id_0, guild_id = guild_id, user_id = user_id_0)
    guild.voice_states[user_id_1] = VoiceState(channel_id = channel_id_0, guild_id = guild_id, user_id = user_id_1)
    guild.voice_states[user_id_2] = VoiceState(channel_id = channel_id_1, guild_id = guild_id, user_id = user_id_2)
    
    vampytest.assert_eq({*channel_0.iter_voice_users()}, {user_0, user_1})


def test__Channel__voice_users():
    """
    Tests whether ``Channel.voice_users`` works as intended.
    """
    channel_id_0 = 202304130084
    channel_id_1 = 202304130085
    guild_id = 202304130086
    user_id_0 = 202304130087
    user_id_1 = 202304130088
    user_id_2 = 202304130089
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    user_2 = User.precreate(user_id_2)
    
    channel_0 = Channel.precreate(channel_id_0, channel_type = ChannelType.guild_voice, guild_id = guild_id)
    channel_1 = Channel.precreate(channel_id_1, channel_type = ChannelType.guild_voice, guild_id = guild_id)
    
    guild = Guild.precreate(guild_id)
    
    guild.voice_states[user_id_0] = VoiceState(channel_id = channel_id_0, guild_id = guild_id, user_id = user_id_0)
    guild.voice_states[user_id_1] = VoiceState(channel_id = channel_id_0, guild_id = guild_id, user_id = user_id_1)
    guild.voice_states[user_id_2] = VoiceState(channel_id = channel_id_1, guild_id = guild_id, user_id = user_id_2)
    
    output = channel_0.voice_users
    vampytest.assert_instance(output, list)
    vampytest.assert_eq({*output}, {user_0, user_1})


def test__Channel__iter_audience():
    """
    Tests whether ``Channel.iter_audience`` works as intended.
    """
    channel_id_0 = 202304130090
    channel_id_1 = 202304130091
    guild_id = 202304130092
    user_id_0 = 202304130093
    user_id_1 = 202304130094
    user_id_2 = 202304130095
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    user_2 = User.precreate(user_id_2)
    
    channel_0 = Channel.precreate(channel_id_0, channel_type = ChannelType.guild_stage, guild_id = guild_id)
    channel_1 = Channel.precreate(channel_id_1, channel_type = ChannelType.guild_stage, guild_id = guild_id)
    
    guild = Guild.precreate(guild_id)
    
    guild.voice_states[user_id_0] = VoiceState(
        channel_id = channel_id_0, guild_id = guild_id, user_id = user_id_0, speaker = False,
    )
    guild.voice_states[user_id_1] = VoiceState(
        channel_id = channel_id_0, guild_id = guild_id, user_id = user_id_1, speaker = True,
    )
    guild.voice_states[user_id_2] = VoiceState(
        channel_id = channel_id_1, guild_id = guild_id, user_id = user_id_2, speaker = False,
    )
    
    vampytest.assert_eq({*channel_0.iter_audience()}, {user_0})


def test__Channel__audience():
    """
    Tests whether ``Channel.audience`` works as intended.
    """
    channel_id_0 = 202304130096
    channel_id_1 = 202304130097
    guild_id = 202304130098
    user_id_0 = 202304130099
    user_id_1 = 202304130100
    user_id_2 = 202304130101
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    user_2 = User.precreate(user_id_2)
    
    channel_0 = Channel.precreate(channel_id_0, channel_type = ChannelType.guild_stage, guild_id = guild_id)
    channel_1 = Channel.precreate(channel_id_1, channel_type = ChannelType.guild_stage, guild_id = guild_id)
    
    guild = Guild.precreate(guild_id)
    guild.voice_states[user_id_0] = VoiceState(
        channel_id = channel_id_0, guild_id = guild_id, user_id = user_id_0, speaker = False,
    )
    guild.voice_states[user_id_1] = VoiceState(
        channel_id = channel_id_0, guild_id = guild_id, user_id = user_id_1, speaker = True,
    )
    guild.voice_states[user_id_2] = VoiceState(
        channel_id = channel_id_1, guild_id = guild_id, user_id = user_id_2, speaker = False,
    )
    
    output = channel_0.audience
    vampytest.assert_instance(output, list)
    vampytest.assert_eq({*output}, {user_0})


def test__Channel__iter_speakers():
    """
    Tests whether ``Channel.iter_speakers`` works as intended.
    """
    channel_id_0 = 202304130102
    channel_id_1 = 202304130103
    guild_id = 202304130104
    user_id_0 = 202304130105
    user_id_1 = 202304130106
    user_id_2 = 202304130107
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    user_2 = User.precreate(user_id_2)
    
    channel_0 = Channel.precreate(channel_id_0, channel_type = ChannelType.guild_stage, guild_id = guild_id)
    channel_1 = Channel.precreate(channel_id_1, channel_type = ChannelType.guild_stage, guild_id = guild_id)
    
    guild = Guild.precreate(guild_id)
    
    guild.voice_states[user_id_0] = VoiceState(
        channel_id = channel_id_0, guild_id = guild_id, user_id = user_id_0, speaker = False,
    )
    guild.voice_states[user_id_1] = VoiceState(
        channel_id = channel_id_0, guild_id = guild_id, user_id = user_id_1, speaker = True,
    )
    guild.voice_states[user_id_2] = VoiceState(
        channel_id = channel_id_1, guild_id = guild_id, user_id = user_id_2, speaker = True,
    )
    
    vampytest.assert_eq({*channel_0.iter_speakers()}, {user_1})


def test__Channel__speakers():
    """
    Tests whether ``Channel.speakers`` works as intended.
    """
    channel_id_0 = 202304130108
    channel_id_1 = 202304130109
    guild_id = 202304130110
    user_id_0 = 202304130111
    user_id_1 = 202304130112
    user_id_2 = 202304130113
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    user_2 = User.precreate(user_id_2)
    
    channel_0 = Channel.precreate(channel_id_0, channel_type = ChannelType.guild_stage, guild_id = guild_id)
    channel_1 = Channel.precreate(channel_id_1, channel_type = ChannelType.guild_stage, guild_id = guild_id)
    
    guild = Guild.precreate(guild_id)
    guild.voice_states[user_id_0] = VoiceState(
        channel_id = channel_id_0, guild_id = guild_id, user_id = user_id_0, speaker = False,
    )
    guild.voice_states[user_id_1] = VoiceState(
        channel_id = channel_id_0, guild_id = guild_id, user_id = user_id_1, speaker = True,
    )
    guild.voice_states[user_id_2] = VoiceState(
        channel_id = channel_id_1, guild_id = guild_id, user_id = user_id_2, speaker = True,
    )
    
    output = channel_0.speakers
    vampytest.assert_instance(output, list)
    vampytest.assert_eq({*output}, {user_1})


def test__Channel__iter_moderators():
    """
    Tests whether ``Channel.iter_moderators`` works as intended.
    """
    channel_id_0 = 202304130114
    channel_id_1 = 202304130115
    guild_id = 202304130116
    user_id_0 = 202304130117
    user_id_1 = 202304130118
    user_id_2 = 202304130119
    role_id = 202304130120
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    user_2 = User.precreate(user_id_2)
    
    channel_0 = Channel.precreate(channel_id_0, channel_type = ChannelType.guild_stage, guild_id = guild_id)
    channel_1 = Channel.precreate(channel_id_1, channel_type = ChannelType.guild_stage, guild_id = guild_id)
    
    role = Role.precreate(role_id, guild_id = guild_id, permissions = Permission().update_by_keys(administrator = True))
    
    user_0.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id])
    user_1.guild_profiles[guild_id] = GuildProfile()
    user_2.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id])
    
    guild = Guild.precreate(guild_id)
    guild.roles[role_id] = role
    
    guild.voice_states[user_id_0] = VoiceState(channel_id = channel_id_0, guild_id = guild_id, user_id = user_id_0)
    guild.voice_states[user_id_1] = VoiceState(channel_id = channel_id_0, guild_id = guild_id, user_id = user_id_1)
    guild.voice_states[user_id_2] = VoiceState(channel_id = channel_id_1, guild_id = guild_id, user_id = user_id_2)
    
    vampytest.assert_eq({*channel_0.iter_moderators()}, {user_0})


def test__Channel__moderators():
    """
    Tests whether ``Channel.moderators`` works as intended.
    """
    channel_id_0 = 202304130121
    channel_id_1 = 202304130122
    guild_id = 202304130123
    user_id_0 = 202304130124
    user_id_1 = 202304130125
    user_id_2 = 202304130126
    role_id = 202304130127
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    user_2 = User.precreate(user_id_2)
    
    channel_0 = Channel.precreate(channel_id_0, channel_type = ChannelType.guild_stage, guild_id = guild_id)
    channel_1 = Channel.precreate(channel_id_1, channel_type = ChannelType.guild_stage, guild_id = guild_id)
    
    role = Role.precreate(role_id, guild_id = guild_id, permissions = Permission().update_by_keys(administrator = True))
    
    user_0.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id])
    user_1.guild_profiles[guild_id] = GuildProfile()
    user_2.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id])
    
    guild = Guild.precreate(guild_id)
    guild.roles[role_id] = role
    
    guild.voice_states[user_id_0] = VoiceState(channel_id = channel_id_0, guild_id = guild_id, user_id = user_id_0)
    guild.voice_states[user_id_1] = VoiceState(channel_id = channel_id_0, guild_id = guild_id, user_id = user_id_1)
    guild.voice_states[user_id_2] = VoiceState(channel_id = channel_id_1, guild_id = guild_id, user_id = user_id_2)
    
    output = channel_0.moderators
    vampytest.assert_instance(output, list)
    vampytest.assert_eq({*output}, {user_0})
