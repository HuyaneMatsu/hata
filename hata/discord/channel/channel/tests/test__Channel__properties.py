from datetime import datetime as DateTime

import vampytest

from ....client import Client
from ....core import BUILTIN_EMOJIS
from ....bases import Icon, IconType
from ....guild import Guild, create_partial_guild_from_id
from ....user import ClientUserBase, User, ZEROUSER, create_partial_user_from_id

from ...forum_tag import ForumTag
from ...channel_metadata import ChannelFlag, ForumLayout, SortOrder, VideoQualityMode, VoiceRegion
from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..preinstanced import ChannelType
from ..channel import Channel


def test__Channel__thread_users__0():
    """
    Tests whether ``Channel.thread_users`` works as intended.
    
    Only testing for a thread channel obviously.
    """
    channel = Channel.precreate(202208080000, channel_type = ChannelType.guild_thread_public)
    
    vampytest.assert_is(channel.thread_users, None)
    
    value = {}
    channel.thread_users = value
    vampytest.assert_is(channel.thread_users, value)
    
    channel.thread_users = None
    vampytest.assert_is(channel.thread_users, None)


def test__Channel__general_properties():
    """
    Checks whether the general proxy properties of the ``Channel`` work as intended.
    """
    for channel_type, field_name, value in (
        (ChannelType.private_group, 'application_id', 202301210011),
        (ChannelType.guild_thread_public, 'applied_tag_ids', (202209180147, 202209180148)),
        (ChannelType.guild_thread_public, 'archived', True),
        (ChannelType.guild_thread_public, 'archived_at', DateTime(2022, 5, 14)),
        (ChannelType.guild_thread_public, 'auto_archive_after', 604800),
        (ChannelType.guild_forum, 'available_tags', (ForumTag('tumoneko'), )),
        (ChannelType.guild_voice, 'bitrate', 50000),
        (ChannelType.guild_forum, 'default_thread_auto_archive_after', 604800),
        (ChannelType.guild_forum, 'default_thread_reaction', BUILTIN_EMOJIS['heart']),
        (ChannelType.guild_forum, 'default_thread_slowmode', 69),
        (ChannelType.guild_forum, 'flags', ChannelFlag(1)),
        (ChannelType.guild_thread_private, 'invitable', False),
        (ChannelType.guild_thread_private, 'name', 'fated'),
        (ChannelType.guild_text, 'nsfw', True),
        (ChannelType.guild_thread_private, 'open', False),
        (ChannelType.guild_thread_private, 'owner_id', 202209180149),
        (ChannelType.guild_thread_private, 'parent_id', 202209180150),
        (ChannelType.guild_text, 'position', 7),
        (ChannelType.guild_voice, 'region', VoiceRegion.brazil),
        (ChannelType.guild_text, 'slowmode', 32),
        (ChannelType.guild_text, 'topic', 'determination'),
        (ChannelType.guild_voice, 'user_limit', 66),
        (ChannelType.guild_voice, 'video_quality_mode', VideoQualityMode.full),
        (ChannelType.guild_forum, 'default_sort_order', SortOrder.creation_date),
        (ChannelType.guild_forum, 'default_forum_layout', ForumLayout.list),
    ):
        channel = Channel(channel_type = channel_type, **{field_name: value})
        
        vampytest.assert_eq(getattr(channel, field_name), value)


def test__Channel__icon():
    """
    Tests whether ``Channel.icon`` works as intended.
    """
    icon = Icon(IconType.static, 123)
    
    channel = Channel.precreate(202209180151, channel_type = ChannelType.private_group, icon = icon)
    vampytest.assert_eq(channel.icon, icon)


def test__Channel__permission_overwrites():
    """
    Tests whether ``Channel.permission_overwrites`` works as intended.
    """
    # permission_overwrites
    permission_overwrites = [
        PermissionOverwrite(202209180152, target_type = PermissionOverwriteTargetType.user)
    ]
    
    channel = Channel(channel_type = ChannelType.guild_text, permission_overwrites = permission_overwrites)
    
    vampytest.assert_eq(
        channel.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in permission_overwrites},
    )


def test__Channel__owner__0():
    """
    Tests whether ``Channel.owner`` works a intended.
    
    Case: has owner.
    """
    owner_id = 202209200000
    channel_type = ChannelType.private_group
    
    channel = Channel(channel_type = channel_type, owner_id = owner_id)
    
    owner = channel.owner
    vampytest.assert_instance(owner, ClientUserBase)
    vampytest.assert_eq(owner.id, owner_id)


def test__Channel__owner__1():
    """
    Tests whether ``Channel.owner`` works a intended.
    
    Case: no owner.
    """
    channel_type = ChannelType.private_group
    
    channel = Channel(channel_type = channel_type)
    
    owner = channel.owner
    vampytest.assert_is(owner, ZEROUSER)


def test__Channel__owner__2():
    """
    Tests whether ``Channel.owner`` works a intended.
    
    Case: owner already cached.
    """
    owner_id = 202209200001
    channel_type = ChannelType.private_group    
    
    channel = Channel(channel_type = channel_type, owner_id = owner_id)
    
    user = create_partial_user_from_id(owner_id)
    
    owner = channel.owner
    vampytest.assert_instance(owner, ClientUserBase)
    vampytest.assert_is(owner, user)


def test__Channel__parent__0():
    """
    Tests whether ``Channel.parent`` works as intended.
    
    Case: has parent.
    """
    parent_id = 202209200002
    channel_type = ChannelType.guild_text
    
    channel = Channel(channel_type = channel_type, parent_id = parent_id)
    
    parent = channel.parent
    vampytest.assert_instance(parent, Channel)
    vampytest.assert_eq(parent.id, parent_id)


def test__Channel__parent__1():
    """
    Tests whether ``Channel.parent`` works as intended.
    
    Case: has no parent.
    """
    channel_type = ChannelType.guild_text
    
    channel = Channel(channel_type = channel_type)
    
    parent = channel.parent
    vampytest.assert_is(parent, None)


def test__Channel__parent__2():
    """
    Tests whether ``Channel.parent`` works as intended.
    
    Case: parent already cached.
    """
    parent_id = 202209200003
    channel_type = ChannelType.guild_text
    
    channel = Channel(channel_type = channel_type, parent_id = parent_id)
    
    parent_channel = Channel.precreate(parent_id)
    
    parent = channel.parent
    vampytest.assert_instance(parent, Channel)
    vampytest.assert_is(parent, parent_channel)


def test__Channel__display_name():
    """
    Tests whether ``Channel.display_name`` works as intended.
    """
    for channel_type, channel_name, additional_keyword_parameters in (
        (ChannelType.unknown, None, None),
        (ChannelType.guild_text, None, None),
        (ChannelType.guild_text, 'hello', None),
        (ChannelType.private, None, None),
        (ChannelType.private, None, [('users', [User.precreate(202209200004)])]),
        (ChannelType.private, None, [('users', [User.precreate(202209200005), User.precreate(202209200006)])]),
        (ChannelType.guild_voice, 'hello', None),
        (ChannelType.private_group, None, None),
        (ChannelType.private_group, 'hello', None),
        (ChannelType.private_group, 'hello', [('users', [User.precreate(202209200007)])]),
        (ChannelType.guild_category, 'hello', None),
        (ChannelType.guild_announcements, 'hello', None),
        (ChannelType.guild_store, 'hello', None),
        (ChannelType.guild_thread_announcements, 'hello', None),
        (ChannelType.guild_thread_public, 'hello', None),
        (ChannelType.guild_thread_private, 'hello', None),
        (ChannelType.guild_stage, 'hello', None),
        (ChannelType.guild_directory, 'hello', None),
        (ChannelType.guild_forum, 'hello', None),
    ):
        keyword_parameters = {'channel_type': channel_type}
        
        if (channel_name is not None):
            keyword_parameters['name'] = channel_name
        
        if (additional_keyword_parameters is not None):
            keyword_parameters.update(additional_keyword_parameters)
        
        channel = Channel(**keyword_parameters)
        
        display_name = channel.display_name
        vampytest.assert_instance(display_name, str)
        
        if (channel_name is not None):
            vampytest.assert_eq(display_name.casefold(), channel_name)


def test__Channel__mention():
    """
    Tests whether ``Channel.mention`` works as intended.
    """
    channel_id = 202209200008
    
    channel = Channel.precreate(channel_id)
    
    mention = channel.mention
    vampytest.assert_instance(mention, str)


def test__Channel__partial__0():
    """
    Tests whether ``Channel.partial`` works as intended.
    
    Case: partial created with `.__new__`.
    """
    channel = Channel(ChannelType.unknown)
    
    partial = channel.partial
    vampytest.assert_instance(partial, bool)
    vampytest.assert_true(partial)


def test__Channel__partial__1():
    """
    Tests whether ``Channel.partial`` works as intended.
    
    Case: partial created with `.precreate`
    """
    channel_id = 202209200009
    
    channel = Channel.precreate(channel_id)
    
    partial = channel.partial
    vampytest.assert_instance(partial, bool)
    vampytest.assert_true(partial)


def test__Channel__partial__2():
    """
    Tests whether ``Channel.partial`` works as intended.
    
    Case: non-partial private.
    """
    client = Client(
        token = 'token_20220909_0000',
    )
    
    try:
        channel_id = 202209200010
        
        channel = Channel.precreate(channel_id, channel_type = ChannelType.private, users = [client])
        
        partial = channel.partial
        vampytest.assert_instance(partial, bool)
        vampytest.assert_false(partial)
    
    # Cleanup
    finally:
        client._delete()
        client = None


def test__Channel__partial__3():
    """
    Tests whether ``Channel.partial`` works as intended.
    
    Case: partial private.
    """
    channel_id = 202209200011
    
    user = User.precreate(202209200012)
    channel = Channel.precreate(channel_id, channel_type = ChannelType.private, users = [user])
    
    partial = channel.partial
    vampytest.assert_instance(partial, bool)
    vampytest.assert_true(partial)


def test__Channel__partial__4():
    """
    Tests whether ``Channel.partial`` works as intended.
    
    Case: non-partial guild.
    """

    client = Client(
        token = 'token_20220909_0001',
    )
    
    try:
        channel_id = 202209200013
        guild_id = 202209200014
        
        guild = Guild.precreate(guild_id)
        guild.clients.append(client)
        
        channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id)
        
        partial = channel.partial
        vampytest.assert_instance(partial, bool)
        vampytest.assert_false(partial)
    
    # Cleanup
    finally:
        client._delete()
        client = None


def test__Channel__partial__5():
    """
    Tests whether ``Channel.partial`` works as intended.
    
    Case: partial guild.
    """
    channel_id = 202209200015
    guild_id = 202209200016
    
    guild = Guild.precreate(guild_id)
    
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id)
    
    partial = channel.partial
    vampytest.assert_instance(partial, bool)
    vampytest.assert_true(partial)


def test__Channel__clients__0():
    """
    Tests whether ``Channel.clients`` works as intended.
    
    Case: no clients.
    """
    channel_id = 202209200017
    
    channel = Channel.precreate(channel_id)
    
    clients = channel.clients
    vampytest.assert_instance(clients, list)
    vampytest.assert_eq(clients, [])


def test__Channel__clients__1():
    """
    Tests whether ``Channel.clients`` works as intended.
    
    Case: private.
    """
    client = Client(
        token = 'token_20220909_0002',
    )
    
    try:
        channel_id = 202209200018
        
        channel = Channel.precreate(channel_id, channel_type = ChannelType.private, users = [client])
            
        clients = channel.clients
        vampytest.assert_instance(clients, list)
        vampytest.assert_eq(clients, [client])
    
    # Cleanup
    finally:
        client._delete()
        client = None
        clients = None


def test__Channel__clients__2():
    """
    Tests whether ``Channel.clients`` works as intended.
    
    Case: guild.
    """
    client = Client(
        token = 'token_20220909_0002',
    )
    
    try:
        channel_id = 202209200018
        
        channel = Channel.precreate(channel_id, channel_type = ChannelType.private, users = [client])
            
        clients = channel.clients
        vampytest.assert_instance(clients, list)
        vampytest.assert_eq(clients, [client])
    
    # Cleanup
    finally:
        client._delete()
        client = None
        clients = None


def test__Channel__guild__0():
    """
    Tests whether ``Channel.guild`` works as intended.
    
    Case: no guild.
    """
    channel_id = 202209200049
    
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text)
    
    guild = channel.guild
    vampytest.assert_instance(guild, Guild, nullable = True)
    vampytest.assert_is(guild, None)


def test__Channel__guild__1():
    """
    Tests whether ``Channel.guild`` works as intended.
    
    Case: guild, but not cached..
    """
    channel_id = 202209200050
    guild_id = 202209200051
    
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id)
    
    guild = channel.guild
    vampytest.assert_instance(guild, Guild, nullable = True)
    vampytest.assert_is(guild, None)


def test__Channel__guild__2():
    """
    Tests whether ``Channel.guild`` works as intended.
    
    Case: guild, cached.
    """
    channel_id = 202209200052
    guild_id = 202209200053
    
    expected_guild = create_partial_guild_from_id(guild_id)
    
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id)
    
    guild = channel.guild
    vampytest.assert_instance(guild, Guild, nullable = True)
    vampytest.assert_is(guild, expected_guild)


def test__Channel__created_at__0():
    """
    Tests whether ``Channel.created_at`` works as intended.
    
    Case: auto.
    """
    channel_id = 202209200054
    
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_thread_public)
    
    created_at = channel.created_at
    vampytest.assert_instance(created_at, DateTime)


def test__Channel__created_at__1():
    """
    Tests whether ``Channel.created_at`` works as intended.
    
    Case: given.
    """
    channel_id = 202209200054
    
    expected_created_at = DateTime(2023, 11, 11)
    
    channel = Channel.precreate(
        channel_id, channel_type = ChannelType.guild_thread_public, created_at = expected_created_at
    )
    
    created_at = channel.created_at
    vampytest.assert_instance(created_at, DateTime)
    vampytest.assert_eq(created_at, expected_created_at)


def test__Channel__order_group():
    """
    Tests whether ``Channel.order_group`` works as intended.
    """
    channel = Channel(channel_type = ChannelType.unknown)
    
    order_group = channel.order_group
    vampytest.assert_instance(order_group, int)
