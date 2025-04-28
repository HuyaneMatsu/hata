import vampytest

from ....application import Application
from ....channel import Channel
from ....guild import Guild, GuildActivityOverview
from ....user import User
from ....utils import is_url

from ..flags import InviteFlag
from ..invite import Invite
from ..preinstanced import InviteTargetType

from .test__Invite__constructor import _assert_fields_set


def test__Invite__copy():
    """
    Tests whether ``Invite.copy`` works as intended.
    """
    flags = InviteFlag(11)
    max_age = 3600
    max_uses = 100
    target_application = Application.precreate(202308070009)
    target_type = InviteTargetType.stream
    target_user = User.precreate(202308070010)
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
    
    copy = invite.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(invite, copy)
    vampytest.assert_eq(invite, copy)


def test__Invite__copy_with__no_fields():
    """
    Tests whether ``Invite.copy_with`` works as intended.
    
    Case: No fields given.
    """
    flags = InviteFlag(11)
    max_age = 3600
    max_uses = 100
    target_application = Application.precreate(202308070011)
    target_type = InviteTargetType.stream
    target_user = User.precreate(202308070012)
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
    
    copy = invite.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(invite, copy)
    vampytest.assert_eq(invite, copy)


def test__Invite__copy_with__all_fields():
    """
    Tests whether ``Invite.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_flags = InviteFlag(11)
    old_max_age = 3600
    old_max_uses = 100
    old_target_application = Application.precreate(202308070013)
    old_target_type = InviteTargetType.stream
    old_target_user = User.precreate(202308070014)
    old_temporary = True
    
    new_flags = InviteFlag(12)
    new_max_age = 7200
    new_max_uses = 200
    new_target_application = Application.precreate(202308070015)
    new_target_type = InviteTargetType.embedded_application
    new_target_user = User.precreate(202308070016)
    new_temporary = False
    
    invite = Invite(
        flags = old_flags,
        max_age = old_max_age,
        max_uses = old_max_uses,
        target_application = old_target_application,
        target_type = old_target_type,
        target_user = old_target_user,
        temporary = old_temporary,
    )
    
    copy = invite.copy_with(
        flags = new_flags,
        max_age = new_max_age,
        max_uses = new_max_uses,
        target_application = new_target_application,
        target_type = new_target_type,
        target_user = new_target_user,
        temporary = new_temporary,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(invite, copy)
    
    vampytest.assert_eq(copy.flags, new_flags)
    vampytest.assert_eq(copy.max_age, new_max_age)
    vampytest.assert_eq(copy.max_uses, new_max_uses)
    vampytest.assert_is(copy.target_application, new_target_application)
    vampytest.assert_is(copy.target_type, new_target_type)
    vampytest.assert_is(copy.target_user, new_target_user)
    vampytest.assert_eq(copy.temporary, new_temporary)


def _iter_options__channel_id():
    channel_id = 202308060007
    
    yield '202308060008', None, 0
    yield '202308060009', Channel.precreate(channel_id), channel_id


@vampytest._(vampytest.call_from(_iter_options__channel_id()).returning_last())
def test__test__Invite__channel_id(code, channel):
    """
    Tests whether ``Inviter.channel_id`` works as intended.
    
    Parameters
    ----------
    code : `str`
        Invite code.
    channel : ``None | Channel``
        Channel to create the invite with.
    
    Returns
    -------
    channel_id : `int`
    """
    return Invite.precreate(code, channel = channel).channel_id


def _iter_options__guild_id():
    guild_id = 202308060010
    
    yield '202308060011', None, 0
    yield '202308060012', Guild.precreate(guild_id), guild_id


@vampytest._(vampytest.call_from(_iter_options__guild_id()).returning_last())
def test__test__Invite__guild_id(code, guild):
    """
    Tests whether ``Inviter.guild_id`` works as intended.
    
    Parameters
    ----------
    code : `str`
        Invite code.
    guild : ``None | Guild``
        Guild to create the invite with.
    
    Returns
    -------
    guild_id : `int`
    """
    return Invite.precreate(code, guild = guild).guild_id


def test__Invite__url():
    """
    Tests whether ``Invite.url`` works as intended.
    """
    code = '202308060013'
    invite = Invite.precreate(code)
    
    url = invite.url
    vampytest.assert_instance(url, str)
    vampytest.assert_true(is_url(url))
    vampytest.assert_in(code, url)


def test__Invite__id():
    """
    Tests whether ``Invite.id`` works as intended.
    """
    code = '202308060014'
    invite = Invite.precreate(code)
    
    invite_id = invite.id
    vampytest.assert_instance(invite_id, int)
    vampytest.assert_false(invite_id)



def _iter_options__target_application_id():
    application_id = 202308060045
    
    yield '202308060046', None, 0
    yield '202308060047', Application.precreate(application_id), application_id


@vampytest._(vampytest.call_from(_iter_options__target_application_id()).returning_last())
def test__test__Invite__target_application_id(code, target_application):
    """
    Tests whether ``Inviter.application_id`` works as intended.
    
    Parameters
    ----------
    code : `str`
        Invite code.
    target_application : ``None | Application``
        Application to create the invite with.
    
    Returns
    -------
    target_application_id : `int`
    """
    return Invite.precreate(code, target_application = target_application).target_application_id


def _iter_options__target_user_id():
    user_id = 202308060048
    
    yield '202308060049', None, 0
    yield '202308060050', User.precreate(user_id), user_id


@vampytest._(vampytest.call_from(_iter_options__target_user_id()).returning_last())
def test__test__Invite__target_user_id(code, target_user):
    """
    Tests whether ``Inviter.target_user_id`` works as intended.
    
    Parameters
    ----------
    code : `str`
        Invite code.
    target_user : ``None | ClientUserBase``
        User to create the invite with.
    
    Returns
    -------
    target_user_id : `int`
    """
    return Invite.precreate(code, target_user = target_user).target_user_id


def _iter_options__partial():
    yield '', True
    yield '202308060065', False


@vampytest._(vampytest.call_from(_iter_options__partial()).returning_last())
def test__test__Invite__partial(code):
    """
    Tests whether ``Inviter.partial`` works as intended.
    
    Parameters
    ----------
    code : `str`
        Invite code.
    
    Returns
    -------
    partial : `bool`
    """
    if code:
        invite = Invite.precreate(code)
    else:
        invite = Invite()
    
    return invite.partial


def _iter_options__inviter_id():
    inviter_id = 202308060010
    
    yield '202310310001', None, 0
    yield '202310310002', User.precreate(inviter_id), inviter_id


@vampytest._(vampytest.call_from(_iter_options__inviter_id()).returning_last())
def test__test__Invite__inviter_id(code, inviter):
    """
    Tests whether ``Inviter.inviter_id`` works as intended.
    
    Parameters
    ----------
    code : `str`
        Invite code.
    inviter : ``None | ClientUserBase``
        User to create the invite with.
    
    Returns
    -------
    inviter_id : `int`
    """
    return Invite.precreate(code, inviter = inviter).inviter_id
