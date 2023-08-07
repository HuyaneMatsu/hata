from datetime import datetime as DateTime

import vampytest

from ....application import Application
from ....channel import Channel
from ....guild import Guild
from ....user import User

from ..flags import InviteFlag
from ..invite import Invite
from ..preinstanced import InviteTargetType, InviteType


def test__Invite__repr():
    """
    Tests whether ``Invite.__repr__`` works as intended.
    """
    approximate_online_count = 11
    approximate_user_count = 13
    code = '202308060077'
    channel = Channel.precreate(202308060078)
    created_at = DateTime(2016, 5, 14)
    flags = InviteFlag(11)
    guild = Guild.precreate(202308060079)
    inviter = User.precreate(202308060080)
    max_age = 3600
    max_uses = 100
    target_application = Application.precreate(202308060081)
    target_type = InviteTargetType.stream
    target_user = User.precreate(202308060082)
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
    
    vampytest.assert_instance(repr(invite), str)


def test__Invite__hash():
    """
    Tests whether ``Invite.__hash__`` works as intended.
    """
    approximate_online_count = 11
    approximate_user_count = 13
    code = '202308070000'
    channel = Channel.precreate(202308070001)
    created_at = DateTime(2016, 5, 14)
    flags = InviteFlag(11)
    guild = Guild.precreate(202308070002)
    inviter = User.precreate(202308070003)
    max_age = 3600
    max_uses = 100
    target_application = Application.precreate(202308070004)
    target_type = InviteTargetType.stream
    target_user = User.precreate(202308070005)
    temporary = True
    invite_type = InviteType.guild
    uses = 69
    
    invite = Invite(
        flags = flags,
        max_age = max_age,
        max_uses = max_uses,
        target_application = target_application,
        target_type = target_type,
        target_user = target_user,
        temporary = temporary,
    )
    
    vampytest.assert_instance(hash(invite), int)
    
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
    
    vampytest.assert_instance(hash(invite), int)


def test__Invite__eq():
    """
    Tests whether ``Invite.__eq__`` works asi intended.
    """
    code = '202308070006'
    flags = InviteFlag(11)
    max_age = 3600
    max_uses = 100
    target_application = Application.precreate(202308070007)
    target_type = InviteTargetType.stream
    target_user = User.precreate(202308070008)
    temporary = True
    
    keyword_parameters = {
        'flags': flags,
        'max_age': max_age,
        'max_uses': max_uses,
        'target_application': target_application,
        'target_type': target_type,
        'target_user': target_user,
        'temporary': temporary,
    }
    
    invite = Invite.precreate(code, **keyword_parameters)
    
    vampytest.assert_eq(invite, invite)
    vampytest.assert_ne(invite, object())
    
    test_invite = Invite(**keyword_parameters)
    vampytest.assert_eq(invite, test_invite)
    
    
    for field_name, field_value in (
        ('flags', InviteFlag(12)),
        ('max_age', 7200),
        ('max_uses', 200),
        ('target_application', None),
        ('target_type', InviteTargetType.embedded_application),
        ('target_user', None),
        ('temporary', False),
    ):
        test_invite = Invite(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(invite, test_invite)
