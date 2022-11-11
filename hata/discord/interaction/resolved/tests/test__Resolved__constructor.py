import vampytest

from ....channel import Channel
from ....message import Attachment, Message
from ....role import Role
from ....user import User

from ..resolved import Resolved


def _assert_is_all_field_set(resolved):
    """
    Asserts whether all fields of the given ``Resolved`` instance are set.
    
    Parameters
    ----------
    resolved : ``Resolved``
        The resolved instance.
    """
    vampytest.assert_instance(resolved, Resolved)
    vampytest.assert_instance(resolved.attachments, dict, nullable = True)
    vampytest.assert_instance(resolved.channels, dict, nullable = True)
    vampytest.assert_instance(resolved.roles, dict, nullable = True)
    vampytest.assert_instance(resolved.messages, dict, nullable = True)
    vampytest.assert_instance(resolved.users, dict, nullable = True)


def test__Resolved__new__0():
    """
    Tests whether ``Resolved.__new__`` works as intended.
    
    Case: no fields given.
    """
    resolved = Resolved()
    _assert_is_all_field_set(resolved)


def test__Resolved__new__1():
    """
    Tests whether ``Resolved.__new__`` works as intended.
    
    Case: all fields given.
    """
    entity_id = 202211050027
    
    attachments = {entity_id: Attachment.precreate(entity_id)}
    channels = {entity_id: Channel.precreate(entity_id)}
    roles = {entity_id: Role.precreate(entity_id)}
    messages = {entity_id: Message.precreate(entity_id)}
    users = {entity_id: User.precreate(entity_id)}
    
    resolved = Resolved(
        attachments = attachments,
        channels = channels,
        roles = roles,
        messages = messages,
        users = users,
    )
    _assert_is_all_field_set(resolved)
    
    vampytest.assert_eq(resolved.attachments, attachments)
    vampytest.assert_eq(resolved.channels, channels)
    vampytest.assert_eq(resolved.roles, roles)
    vampytest.assert_eq(resolved.messages, messages)
    vampytest.assert_eq(resolved.users, users)
