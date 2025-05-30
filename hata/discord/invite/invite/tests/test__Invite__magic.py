from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....application import Application
from ....channel import Channel
from ....guild import Guild, GuildActivityOverview
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
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    flags = InviteFlag(11)
    guild = Guild.precreate(202308060079)
    guild_activity_overview = GuildActivityOverview.precreate(202308060079)
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
        guild_activity_overview = guild_activity_overview,
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
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    flags = InviteFlag(11)
    guild = Guild.precreate(202308070002)
    guild_activity_overview = GuildActivityOverview.precreate(202308070002)
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
        guild_activity_overview = guild_activity_overview,
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


def test__Invite__eq__non_partial_and_other():
    """
    tests whether ``Invite.__eq__`` works as intended.
    
    Case: non partial and other objects.
    """
    code = '202308070006'
    
    flags = InviteFlag(11)
    
    invite = Invite.precreate(code, flags = flags)
    
    vampytest.assert_eq(invite, invite)
    vampytest.assert_ne(invite, object())
    
    test_invite = Invite(flags = flags)
    vampytest.assert_eq(invite, test_invite)


def _iter_options__eq():
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
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'flags': InviteFlag(12),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'max_age': 7200,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'max_uses': 200,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'target_application': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'target_type': InviteTargetType.embedded_application,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'target_user': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'temporary': False,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__Invite__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``Invite.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    invite_0 = Invite(**keyword_parameters_0)
    invite_1 = Invite(**keyword_parameters_1)
    
    output = invite_0 == invite_1
    vampytest.assert_instance(output, bool)
    return output
