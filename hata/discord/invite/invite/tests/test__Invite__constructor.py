from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....application import Application
from ....channel import Channel
from ....guild import Guild
from ....user import ClientUserBase, User

from ..flags import InviteFlag
from ..invite import Invite
from ..preinstanced import InviteTargetType, InviteType



def _assert_fields_set(invite):
    """
    Checks whether every fields of the given invite are set.
    
    Parameters
    ----------
    invite : ``Invite``
        The invite to check.
    """
    vampytest.assert_instance(invite, Invite)
    
    vampytest.assert_instance(invite.approximate_online_count, int)
    vampytest.assert_instance(invite.approximate_user_count, int)
    vampytest.assert_instance(invite.channel, Channel, nullable = True)
    vampytest.assert_instance(invite.code, str)
    vampytest.assert_instance(invite.created_at, DateTime, nullable = True)
    vampytest.assert_instance(invite.flags, InviteFlag)
    vampytest.assert_instance(invite.guild, Guild, nullable = True)
    vampytest.assert_instance(invite.inviter, ClientUserBase)
    vampytest.assert_instance(invite.max_age, int, nullable = True)
    vampytest.assert_instance(invite.max_uses, int, nullable = True)
    vampytest.assert_instance(invite.target_application, Application, nullable = True)
    vampytest.assert_instance(invite.target_type, InviteTargetType)
    vampytest.assert_instance(invite.target_user, ClientUserBase, nullable = True)
    vampytest.assert_instance(invite.temporary, bool)
    vampytest.assert_instance(invite.type, InviteType)
    vampytest.assert_instance(invite.uses, int, nullable = True)


def test__Invite__new__no_fields():
    """
    Tests whether ``Invite.__new__`` works as intended.
    
    Case: No fields given.
    """
    invite = Invite()
    _assert_fields_set(invite)


def test__Invite__new__all_fields():
    """
    Tests whether ``Invite.__new__`` works as intended.
    
    Case: All fields given.
    """
    flags = InviteFlag(11)
    max_age = 3600
    max_uses = 100
    target_application = Application.precreate(202308060066)
    target_type = InviteTargetType.stream
    target_user = User.precreate(202308060067)
    temporary = True

    invite = Invite(
        flags = flags,
        max_age = max_age,
        max_uses = max_uses,
        target_application = target_application,
        target_type = target_type,
        target_user = target_user,
        temporary = temporary,
    )
    
    vampytest.assert_eq(invite.flags, flags)
    vampytest.assert_eq(invite.max_age, max_age)
    vampytest.assert_eq(invite.max_uses, max_uses)
    vampytest.assert_is(invite.target_application, target_application)
    vampytest.assert_is(invite.target_type, target_type)
    vampytest.assert_is(invite.target_user, target_user)
    vampytest.assert_eq(invite.temporary, temporary)


def test__Invite__create_empty():
    """
    Tests whether ``Invite._create_empty`` works as intended.
    """
    code = '202308060068'
    
    invite = Invite._create_empty(code)
    _assert_fields_set(invite)
    
    vampytest.assert_eq(invite.code, code)


def test__Invite__precreate__no_fields():
    """
    Tests whether ``Invite.precreate`` works as intended.
    
    Case: No fields given.
    """
    code = '202308060069'
    
    invite = Invite.precreate(code)
    _assert_fields_set(invite)
    
    vampytest.assert_eq(invite.code, code)


def test__Invite__precreate__caching():
    """
    Tests whether ``Invite.precreate`` works as intended.
    
    Case: Caching.
    """
    code = '202308060070'
    
    invite = Invite.precreate(code)
    test_invite = Invite.precreate(code)
    
    vampytest.assert_eq(invite, test_invite)


def test__Invite__precreate__all_fields():
    """
    Tests whether ``Invite.precreate`` works as intended.
    
    Case: All fields given.
    """
    approximate_online_count = 11
    approximate_user_count = 13
    code = '202308060071'
    channel = Channel.precreate(202308060072)
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    flags = InviteFlag(11)
    guild = Guild.precreate(202308060073)
    inviter = User.precreate(202308060074)
    max_age = 3600
    max_uses = 100
    target_application = Application.precreate(202308060075)
    target_type = InviteTargetType.stream
    target_user = User.precreate(202308060076)
    temporary = True
    invite_type = InviteType.guild
    uses = 69
    
    invite = Invite.precreate(
        code,
        approximate_online_count = approximate_online_count,
        approximate_user_count = approximate_user_count,
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
    )
    _assert_fields_set(invite)
    
    vampytest.assert_eq(invite.approximate_online_count, approximate_online_count)
    vampytest.assert_eq(invite.approximate_user_count, approximate_user_count)
    vampytest.assert_is(invite.channel, channel)
    vampytest.assert_eq(invite.code, code)
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
