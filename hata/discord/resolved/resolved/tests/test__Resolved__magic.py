import vampytest

from ....channel import Channel
from ....message import Attachment, Message
from ....role import Role
from ....user import User

from ..resolved import Resolved


def test__Resolved__repr():
    """
    Tests whether ``Resolved.__repr__`` works as intended.
    """
    entity_id = 202211050036
    
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
    
    vampytest.assert_instance(repr(resolved), str)


def test__Resolved__hash():
    """
    Tests whether ``Resolved.__hash__`` works as intended.
    """
    entity_id = 202211050037
    
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
    
    vampytest.assert_instance(hash(resolved), int)


def test__Resolved__eq():
    """
    Tests whether ``Resolved.__eq__`` works as intended.
    """
    entity_id = 202211050038
    
    attachment = Attachment.precreate(entity_id)
    channel = Channel.precreate(entity_id)
    role = Role.precreate(entity_id)
    message = Message.precreate(entity_id)
    user = User.precreate(entity_id)
    
    
    keyword_parameters = {
        'attachments': [attachment],
        'channels': [channel],
        'roles': [role],
        'messages': [message],
        'users': [user],
    }
    
    resolved = Resolved(**keyword_parameters)
    
    
    vampytest.assert_eq(resolved, resolved)
    vampytest.assert_ne(resolved, object())
    
    for field_name, field_value in (
        ('attachments', None),
        ('channels', None),
        ('roles', None),
        ('messages', None),
        ('users', None),
    ):
        test_resolved = Resolved(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(resolved, test_resolved)
