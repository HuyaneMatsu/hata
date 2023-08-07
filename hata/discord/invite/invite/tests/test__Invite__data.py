from datetime import datetime as DateTime

import vampytest

from ....application import Application
from ....channel import Channel, create_partial_channel_data
from ....guild import Guild, create_partial_guild_data
from ....user import User
from ....utils import datetime_to_timestamp

from ..flags import InviteFlag
from ..invite import Invite
from ..preinstanced import InviteTargetType, InviteType

from .test__Invite__constructor import _assert_fields_set


def test__Invite__set_attributes():
    """
    Tests whether ``Invite._set_attributes`` works as intended.
    """
    invite = Invite.precreate('202308060015')
    
    channel = Channel.precreate(202308060016)
    created_at = DateTime(2016, 5, 14)
    flags = InviteFlag(11)
    guild = Guild.precreate(
        202308060017,
        approximate_online_count = 21,
        approximate_user_count = 23,
    )
    inviter = User.precreate(202308060018)
    max_age = 3600
    max_uses = 100
    target_application = Application.precreate(202308060019)
    target_type = InviteTargetType.stream
    target_user = User.precreate(202308060020)
    temporary = True
    invite_type = InviteType.guild
    uses = 69
    approximate_online_count = 11
    approximate_user_count = 13
    
    data = {
        'channel': create_partial_channel_data(channel),
        'created_at': datetime_to_timestamp(created_at),
        'flags': int(flags),
        'guild': create_partial_guild_data(guild),
        'inviter': inviter.to_data(include_internals = True),
        'max_age': max_age,
        'max_uses': max_uses,
        'target_application': target_application.to_data_invite(include_internals = True),
        'target_type': target_type.value,
        'target_user': target_user.to_data(include_internals = True),
        'temporary': temporary,
        'type': invite_type.value,
        'uses': uses,
        'approximate_presence_count': approximate_online_count,
        'approximate_member_count': approximate_user_count,
    }
    
    invite._set_attributes(data)
    vampytest.assert_is(invite.channel, channel)
    vampytest.assert_eq(invite.created_at, created_at)
    vampytest.assert_eq(invite.flags, flags)
    vampytest.assert_is(invite.guild, guild)
    vampytest.assert_is(invite.inviter, inviter)
    vampytest.assert_eq(invite.max_age, max_age)
    vampytest.assert_eq(invite.max_uses, max_uses)
    vampytest.assert_is(invite.target_application, target_application)
    vampytest.assert_is(invite.target_type, target_type)
    vampytest.assert_is(invite.target_user, target_user)
    vampytest.assert_eq(invite.temporary, temporary)
    vampytest.assert_is(invite.type, invite_type)
    vampytest.assert_eq(invite.uses, uses)
    
    vampytest.assert_eq(invite.approximate_online_count, approximate_online_count)
    vampytest.assert_eq(invite.approximate_user_count, approximate_user_count)
    
    vampytest.assert_eq(guild.approximate_online_count, approximate_online_count)
    vampytest.assert_eq(guild.approximate_user_count, approximate_user_count)


def test__Invite__set_attributes__no_counts():
    """
    Tests whether ``Invite._set_attributes`` works as intended.
    
    Case: No counts.
    """
    approximate_online_count = 11
    approximate_user_count = 12
    
    invite = Invite.precreate(
        '202308060021',
        approximate_online_count = approximate_online_count,
        approximate_user_count = approximate_user_count,
    )
    
    guild = Guild.precreate(
        202308060022,
        approximate_online_count = 21,
        approximate_user_count = 23,
    )
    
    data = {
        'guild': create_partial_guild_data(guild),
    }
    
    invite._set_attributes(data)
    
    vampytest.assert_eq(invite.approximate_online_count, 0)
    vampytest.assert_eq(invite.approximate_user_count, 0)
    
    vampytest.assert_ne(guild.approximate_online_count, 0)
    vampytest.assert_ne(guild.approximate_user_count, 0)


def test__Invite__update_attributes():
    """
    Tests whether ``Invite._update_attributes`` works as intended.
    """
    invite = Invite.precreate('202308060023')
    
    channel = Channel.precreate(202308060024)
    created_at = DateTime(2016, 5, 14)
    flags = InviteFlag(11)
    guild = Guild.precreate(
        202308060025,
        approximate_online_count = 21,
        approximate_user_count = 23,
    )
    inviter = User.precreate(202308060026)
    max_age = 3600
    max_uses = 100
    target_application = Application.precreate(202308060027)
    target_type = InviteTargetType.stream
    target_user = User.precreate(202308060028)
    temporary = True
    invite_type = InviteType.guild
    uses = 69
    approximate_online_count = 11
    approximate_user_count = 13
    
    data = {
        'channel': create_partial_channel_data(channel),
        'created_at': datetime_to_timestamp(created_at),
        'flags': int(flags),
        'guild': create_partial_guild_data(guild),
        'inviter': inviter.to_data(include_internals = True),
        'max_age': max_age,
        'max_uses': max_uses,
        'target_application': target_application.to_data_invite(include_internals = True),
        'target_type': target_type.value,
        'target_user': target_user.to_data(include_internals = True),
        'temporary': temporary,
        'type': invite_type.value,
        'uses': uses,
        'approximate_presence_count': approximate_online_count,
        'approximate_member_count': approximate_user_count,
    }
    
    invite._update_attributes(data)
    vampytest.assert_is(invite.channel, channel)
    vampytest.assert_eq(invite.created_at, created_at)
    vampytest.assert_eq(invite.flags, flags)
    vampytest.assert_is(invite.guild, guild)
    vampytest.assert_is(invite.inviter, inviter)
    vampytest.assert_eq(invite.max_age, max_age)
    vampytest.assert_eq(invite.max_uses, max_uses)
    vampytest.assert_is(invite.target_application, target_application)
    vampytest.assert_is(invite.target_type, target_type)
    vampytest.assert_is(invite.target_user, target_user)
    vampytest.assert_eq(invite.temporary, temporary)
    vampytest.assert_is(invite.type, invite_type)
    vampytest.assert_eq(invite.uses, uses)
    
    vampytest.assert_eq(invite.approximate_online_count, approximate_online_count)
    vampytest.assert_eq(invite.approximate_user_count, approximate_user_count)
    
    vampytest.assert_eq(guild.approximate_online_count, approximate_online_count)
    vampytest.assert_eq(guild.approximate_user_count, approximate_user_count)


def test__Invite__update_attributes__no_counts():
    """
    Tests whether ``Invite._update_attributes`` works as intended.
    
    Case: No counts.
    """
    approximate_online_count = 11
    approximate_user_count = 12
    
    invite = Invite.precreate(
        '202308060029',
        approximate_online_count = approximate_online_count,
        approximate_user_count = approximate_user_count,
    )
    
    guild = Guild.precreate(
        202308060030,
        approximate_online_count = 21,
        approximate_user_count = 23,
    )
    
    data = {
        'guild': create_partial_guild_data(guild),
    }
    
    invite._update_attributes(data)
    
    vampytest.assert_eq(invite.approximate_online_count, approximate_online_count)
    vampytest.assert_eq(invite.approximate_user_count, approximate_user_count)
    
    vampytest.assert_ne(guild.approximate_online_count, 0)
    vampytest.assert_ne(guild.approximate_user_count, 0)


def test__Invite__set_counts_only():
    """
    Tests whether ``Invite._set_counts_only`` works as intended.
    """
    approximate_online_count = 11
    approximate_user_count = 12
    
    guild = Guild.precreate(
        202308060031,
        approximate_online_count = 21,
        approximate_user_count = 23,
    )
    
    invite = Invite.precreate(
        '202308060032',
        guild = guild,
        approximate_online_count = approximate_online_count,
        approximate_user_count = approximate_user_count,
    )
    
    data = {
        'approximate_presence_count': approximate_online_count,
        'approximate_member_count': approximate_user_count,
    }
    
    invite._set_counts_only(data)
    
    vampytest.assert_eq(invite.approximate_online_count, approximate_online_count)
    vampytest.assert_eq(invite.approximate_user_count, approximate_user_count)
    
    vampytest.assert_eq(guild.approximate_online_count, approximate_online_count)
    vampytest.assert_eq(guild.approximate_user_count, approximate_user_count)


def test__Invite__set_counts_only__no_counts():
    """
    Tests whether ``Invite._set_counts_only`` works as intended.
    
    Case: No counts.
    """
    guild = Guild.precreate(
        202308060033,
        approximate_online_count = 21,
        approximate_user_count = 23,
    )
    
    invite = Invite.precreate(
        '202308060034',
        guild = guild,
        approximate_online_count = 11,
        approximate_user_count = 13,
    )
    
    data = {}
    
    invite._set_counts_only(data)
    
    vampytest.assert_eq(invite.approximate_online_count, 0)
    vampytest.assert_eq(invite.approximate_user_count, 0)
    
    vampytest.assert_ne(guild.approximate_online_count, 0)
    vampytest.assert_ne(guild.approximate_user_count, 0)


def test__Invite__update_counts_only():
    """
    Tests whether ``Invite._update_counts_only`` works as intended.
    """
    approximate_online_count = 11
    approximate_user_count = 12
    
    guild = Guild.precreate(
        202308060035,
        approximate_online_count = 21,
        approximate_user_count = 23,
    )
    
    invite = Invite.precreate(
        '202308060036',
        guild = guild,
        approximate_online_count = approximate_online_count,
        approximate_user_count = approximate_user_count,
    )
    
    data = {
        'approximate_presence_count': approximate_online_count,
        'approximate_member_count': approximate_user_count,
    }
    
    invite._update_counts_only(data)
    
    vampytest.assert_eq(invite.approximate_online_count, approximate_online_count)
    vampytest.assert_eq(invite.approximate_user_count, approximate_user_count)
    
    vampytest.assert_eq(guild.approximate_online_count, approximate_online_count)
    vampytest.assert_eq(guild.approximate_user_count, approximate_user_count)


def test__Invite__update_counts_only__no_counts():
    """
    Tests whether ``Invite._update_counts_only`` works as intended.
    
    Case: No counts.
    """
    approximate_online_count = 11
    approximate_user_count = 13
    
    guild = Guild.precreate(
        202308060037,
        approximate_online_count = 21,
        approximate_user_count = 23,
    )
    
    invite = Invite.precreate(
        '202308060038',
        guild = guild,
        approximate_online_count = approximate_online_count,
        approximate_user_count = approximate_user_count,
    )
    
    data = {}
    
    invite._update_counts_only(data)
    
    vampytest.assert_eq(invite.approximate_online_count, approximate_online_count)
    vampytest.assert_eq(invite.approximate_user_count, approximate_user_count)
    
    vampytest.assert_ne(guild.approximate_online_count, 0)
    vampytest.assert_ne(guild.approximate_user_count, 0)


def test__Invite__from_data():
    """
    Tests whether ``Invite.from_data`` works as intended.
    """
    code = '202308060039'
    channel = Channel.precreate(202308060040)
    created_at = DateTime(2016, 5, 14)
    flags = InviteFlag(11)
    guild = Guild.precreate(
        202308060041,
        approximate_online_count = 21,
        approximate_user_count = 23,
    )
    inviter = User.precreate(202308060042)
    max_age = 3600
    max_uses = 100
    target_application = Application.precreate(202308060043)
    target_type = InviteTargetType.stream
    target_user = User.precreate(202308060044)
    temporary = True
    invite_type = InviteType.guild
    uses = 69
    approximate_online_count = 11
    approximate_user_count = 13
    
    data = {
        'code': code,
        'channel': create_partial_channel_data(channel),
        'created_at': datetime_to_timestamp(created_at),
        'flags': int(flags),
        'guild': create_partial_guild_data(guild),
        'inviter': inviter.to_data(include_internals = True),
        'max_age': max_age,
        'max_uses': max_uses,
        'target_application': target_application.to_data_invite(include_internals = True),
        'target_type': target_type.value,
        'target_user': target_user.to_data(include_internals = True),
        'temporary': temporary,
        'type': invite_type.value,
        'uses': uses,
        'approximate_presence_count': approximate_online_count,
        'approximate_member_count': approximate_user_count,
    }
    
    invite = Invite.from_data(data)
    _assert_fields_set(invite)
    
    vampytest.assert_is(invite.channel, channel)
    vampytest.assert_eq(invite.created_at, created_at)
    vampytest.assert_eq(invite.flags, flags)
    vampytest.assert_is(invite.guild, guild)
    vampytest.assert_is(invite.inviter, inviter)
    vampytest.assert_eq(invite.max_age, max_age)
    vampytest.assert_eq(invite.max_uses, max_uses)
    vampytest.assert_is(invite.target_application, target_application)
    vampytest.assert_is(invite.target_type, target_type)
    vampytest.assert_is(invite.target_user, target_user)
    vampytest.assert_eq(invite.temporary, temporary)
    vampytest.assert_is(invite.type, invite_type)
    vampytest.assert_eq(invite.uses, uses)
    
    vampytest.assert_eq(invite.approximate_online_count, approximate_online_count)
    vampytest.assert_eq(invite.approximate_user_count, approximate_user_count)
    
    vampytest.assert_eq(guild.approximate_online_count, approximate_online_count)
    vampytest.assert_eq(guild.approximate_user_count, approximate_user_count)


def test__Invite__from_data__caching():
    """
    Tests whether ``Invite.from_data`` works as intended.
    
    Case: Caching.
    """
    code = '202308060045'
    
    
    data = {
        'code': code,
    }
    
    invite = Invite.from_data(data)
    test_invite = Invite.from_data(data)
    
    vampytest.assert_eq(invite, test_invite)


def test__Invite__to_data__with_internals():
    """
    Tests whether ``Invite.to_data`` works as intended.
    
    Case: Include internals.
    """
    code = '202308060053'
    channel = Channel.precreate(202308060054)
    created_at = DateTime(2016, 5, 14)
    flags = InviteFlag(11)
    guild = Guild.precreate(
        202308060055,
        approximate_online_count = 21,
        approximate_user_count = 23,
    )
    inviter = User.precreate(202308060056)
    max_age = 3600
    max_uses = 100
    target_application = Application.precreate(202308060057)
    target_type = InviteTargetType.stream
    target_user = User.precreate(202308060058)
    temporary = True
    invite_type = InviteType.guild
    uses = 69
    approximate_online_count = 11
    approximate_user_count = 13
    
    invite = Invite.precreate(
        code = code,
        channel = channel,
        created_at = created_at,
        flags = flags,
        guild = guild,
        inviter = inviter,
        max_age = max_age,
        max_uses = max_uses,
        target_application = target_application,
        target_type = target_type,
        target_user = target_user,
        temporary = temporary,
        invite_type = invite_type,
        uses = uses,
        approximate_online_count = approximate_online_count,
        approximate_user_count = approximate_user_count,
    )
    
    expected_output = {
        'flags': int(flags),
        'max_age': max_age,
        'max_uses': max_uses,
        'target_type': target_type.value,
        'temporary': temporary,
        
        'approximate_presence_count': approximate_online_count,
        'approximate_member_count': approximate_user_count,
        'channel': create_partial_channel_data(channel),
        'channel_id': str(channel.id),
        'code': code,
        'created_at': datetime_to_timestamp(created_at),
        'guild': create_partial_guild_data(guild),
        'guild_id': str(guild.id),
        'inviter': inviter.to_data(defaults = True, include_internals = True),
        'target_application': target_application.to_data_invite(defaults = True, include_internals = True),
        'target_user': target_user.to_data(defaults = True, include_internals = True),
        'type': invite_type.value,
        'uses': uses,
    }
    
    vampytest.assert_eq(invite.to_data(defaults = True, include_internals = True), expected_output)


def test__Invite__to_data__without_internals():
    """
    Tests whether ``Invite.to_data`` works as intended.
    
    Case: without include internals.
    """
    code = '202308060059'
    channel = Channel.precreate(202308060060)
    created_at = DateTime(2016, 5, 14)
    flags = InviteFlag(11)
    guild = Guild.precreate(
        202308060061,
        approximate_online_count = 21,
        approximate_user_count = 23,
    )
    inviter = User.precreate(202308060062)
    max_age = 3600
    max_uses = 100
    target_application = Application.precreate(202308060063)
    target_type = InviteTargetType.stream
    target_user = User.precreate(202308060064)
    temporary = True
    invite_type = InviteType.guild
    uses = 69
    approximate_online_count = 11
    approximate_user_count = 13
    
    invite = Invite.precreate(
        code = code,
        channel = channel,
        created_at = created_at,
        flags = flags,
        guild = guild,
        inviter = inviter,
        max_age = max_age,
        max_uses = max_uses,
        target_application = target_application,
        target_type = target_type,
        target_user = target_user,
        temporary = temporary,
        invite_type = invite_type,
        uses = uses,
        approximate_online_count = approximate_online_count,
        approximate_user_count = approximate_user_count,
    )
    
    expected_output = {
        'flags': int(flags),
        'max_age': max_age,
        'max_uses': max_uses,
        'target_type': target_type.value,
        'temporary': temporary,
        'target_application_id': str(target_application.id),
        'target_user_id': str(target_user.id),
    }
    
    vampytest.assert_eq(invite.to_data(defaults = True, include_internals = False), expected_output)


def test__Invite__update_attributes_partial():
    """
    Tests whether ``Invite._update_attributes_partial`` works as intended.
    """
    invite = Invite.precreate('202308070017')
    
    channel = Channel.precreate(202308070018)
    guild = Guild.precreate(202308070019)
    
    data = {
        'channel_id': str(channel.id),
        'guild_id': str(guild.id),
    }
    
    invite._update_attributes_partial(data)
    
    vampytest.assert_is(invite.channel, channel)
    vampytest.assert_is(invite.guild, guild)
