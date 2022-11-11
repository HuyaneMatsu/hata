import vampytest

from ....channel import Channel
from ....message import Attachment, Message
from ....role import Role
from ....user import User

from ..resolved import Resolved

from .test__Resolved__constructor import _assert_is_all_field_set


def test__Resolved__copy():
    """
    Tests whether ``Resolved.copy`` works as intended.
    """
    entity_id = 202211050032
    
    attachment = Attachment.precreate(entity_id)
    channel = Channel.precreate(entity_id)
    role = Role.precreate(entity_id)
    message = Message.precreate(entity_id)
    user = User.precreate(entity_id)
    

    resolved = Resolved(
        attachments = [attachment],
        channels = [channel],
        roles = [role],
        messages = [message],
        users = [user],
    )
    
    copy = resolved.copy()
    _assert_is_all_field_set(copy)
    vampytest.assert_is_not(copy, resolved)
    vampytest.assert_eq(copy, resolved)


def test__Resolved__copy_with__0():
    """
    Tests whether ``Resolved.copy_with`` works as intended.
    
    Case: No fields given.
    """
    entity_id = 202211050033
    
    attachment = Attachment.precreate(entity_id)
    channel = Channel.precreate(entity_id)
    role = Role.precreate(entity_id)
    message = Message.precreate(entity_id)
    user = User.precreate(entity_id)
    

    resolved = Resolved(
        attachments = [attachment],
        channels = [channel],
        roles = [role],
        messages = [message],
        users = [user],
    )
    
    copy = resolved.copy_with()
    _assert_is_all_field_set(copy)
    vampytest.assert_is_not(copy, resolved)
    vampytest.assert_eq(copy, resolved)



def test__Resolved__copy_with__1():
    """
    Tests whether ``Resolved.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_entity_id = 202211050034
    new_entity_id = 202211050035
    
    old_attachment = Attachment.precreate(old_entity_id)
    new_attachment = Attachment.precreate(new_entity_id)
    old_channel = Channel.precreate(old_entity_id)
    new_channel = Channel.precreate(new_entity_id)
    old_role = Role.precreate(old_entity_id)
    new_role = Role.precreate(new_entity_id)
    old_message = Message.precreate(old_entity_id)
    new_message = Message.precreate(new_entity_id)
    old_user = User.precreate(old_entity_id)
    new_user = User.precreate(new_entity_id)

    resolved = Resolved(
        attachments = [old_attachment],
        channels = [old_channel],
        roles = [old_role],
        messages = [old_message],
        users = [old_user],
    )
    
    copy = resolved.copy_with(
        attachments = [new_attachment],
        channels = [new_channel],
        roles = [new_role],
        messages = [new_message],
        users = [new_user],
        
    )
    _assert_is_all_field_set(copy)
    vampytest.assert_is_not(copy, resolved)

    vampytest.assert_eq(copy.attachments, {new_attachment.id: new_attachment})
    vampytest.assert_eq(copy.channels, {new_channel.id: new_channel})
    vampytest.assert_eq(copy.roles, {new_role.id: new_role})
    vampytest.assert_eq(copy.messages, {new_message.id: new_message})
    vampytest.assert_eq(copy.users, {new_user.id: new_user})


def test__Resolved__resolve_attachment():
    """
    Tests whether ``Resolved.resolve_attachment`` works as intended.
    """
    attachment = Attachment.precreate(202211080000)
    resolved = Resolved(attachments = [attachment])
    
    for resolved, entity_id, expected_output in (
        (Resolved(), 0, None),
        (resolved, 0, None),
        (resolved, attachment.id, attachment),
    ):
        output = resolved.resolve_attachment(entity_id)
        vampytest.assert_is(output, expected_output)


def test__Resolved__resolve_channel():
    """
    Tests whether ``Resolved.resolve_channel`` works as intended.
    """
    channel = Channel.precreate(202211080001)
    resolved = Resolved(channels = [channel])
    
    for resolved, entity_id, expected_output in (
        (Resolved(), 0, None),
        (resolved, 0, None),
        (resolved, channel.id, channel),
    ):
        output = resolved.resolve_channel(entity_id)
        vampytest.assert_is(output, expected_output)


def test__Resolved__resolve_role():
    """
    Tests whether ``Resolved.resolve_role`` works as intended.
    """
    role = Role.precreate(202211080002)
    resolved = Resolved(roles = [role])
    
    for resolved, entity_id, expected_output in (
        (Resolved(), 0, None),
        (resolved, 0, None),
        (resolved, role.id, role),
    ):
        output = resolved.resolve_role(entity_id)
        vampytest.assert_is(output, expected_output)


def test__Resolved__resolve_message():
    """
    Tests whether ``Resolved.resolve_message`` works as intended.
    """
    message = Message.precreate(202211080003)
    resolved = Resolved(messages = [message])
    
    for resolved, entity_id, expected_output in (
        (Resolved(), 0, None),
        (resolved, 0, None),
        (resolved, message.id, message),
    ):
        output = resolved.resolve_message(entity_id)
        vampytest.assert_is(output, expected_output)


def test__Resolved__resolve_user():
    """
    Tests whether ``Resolved.resolve_user`` works as intended.
    """
    user = User.precreate(202211080004)
    resolved = Resolved(users = [user])
    
    for resolved, entity_id, expected_output in (
        (Resolved(), 0, None),
        (resolved, 0, None),
        (resolved, user.id, user),
    ):
        output = resolved.resolve_user(entity_id)
        vampytest.assert_is(output, expected_output)


def test__Resolved__resolve_mentionable():
    """
    Tests whether ``Resolved.resolve_mentionable`` works as intended.
    """
    role = Role.precreate(202211080005)
    user = User.precreate(202211080006)
    
    resolved = Resolved(roles = [role], users = [user])
    
    for resolved, entity_id, expected_output in (
        (Resolved(), 0, None),
        (resolved, 0, None),
        (resolved, role.id, role),
        (resolved, user.id, user),
    ):
        output = resolved.resolve_mentionable(entity_id)
        vampytest.assert_is(output, expected_output)


def test__Resolved__resolve_entity():
    """
    Tests whether ``Resolved.resolve_entity`` works as intended.
    """
    attachment = Attachment.precreate(202211080007)
    channel = Channel.precreate(202211080008)
    message = Message.precreate(202211080009)
    role = Role.precreate(202211080010)
    user = User.precreate(202211080011)
    
    resolved = Resolved(
        attachments = [attachment],
        channels = [channel],
        messages = [message],
        roles = [role],
        users = [user]
    )
    
    for resolved, entity_id, expected_output in (
        (Resolved(), 0, None),
        (resolved, 0, None),
        (resolved, attachment.id, attachment),
        (resolved, channel.id, channel),
        (resolved, message.id, message),
        (resolved, role.id, role),
        (resolved, user.id, user),
    ):
        output = resolved.resolve_entity(entity_id)
        vampytest.assert_is(output, expected_output)
