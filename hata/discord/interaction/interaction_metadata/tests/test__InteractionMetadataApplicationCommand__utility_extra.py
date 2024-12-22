import vampytest

from ....channel import Channel
from ....message import Attachment, Message
from ....role import Role
from ....user import User

from ...resolved import Resolved

from ..application_command import InteractionMetadataApplicationCommand

def _iter_options():
    extra_target_id = 202211080017
    
    attachment = Attachment.precreate(202211080012)
    channel = Channel.precreate(202211080013)
    message = Message.precreate(202211080014)
    role = Role.precreate(202211080015)
    user = User.precreate(202211080016)
    
    resolved = Resolved(
        attachments = [attachment],
        channels = [channel],
        messages = [message],
        roles = [role],
        users = [user]
    )
    
    yield (
        {},
        None,
    )
        
    yield(
        {'target_id': extra_target_id},
        None,
    )
    
    yield (
        {'resolved': resolved},
        None,
    )
    
    yield (
        {'resolved': resolved, 'target_id': extra_target_id},
        None,
    )
    
    yield (
        {'resolved': resolved, 'target_id': attachment.id},
        attachment,
    )
    
    yield (
        {'resolved': resolved, 'target_id': channel.id},
        channel,
    )
    yield (
        {'resolved': resolved, 'target_id': message.id},
        message,
    )
    
    yield (
        {'resolved': resolved, 'target_id': role.id},
        role,
    )
    
    yield (
        {'resolved': resolved, 'target_id': user.id},
        user,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__InteractionMetadataApplicationCommand__target(keyword_parameters):
    """
    Tests whether ``InteractionMetadataApplicationCommand.target`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        keyword parameters to construct the metadata from.
    
    Returns
    -------
    output : `object`
    """
    interaction_metadata = InteractionMetadataApplicationCommand(**keyword_parameters)
    return interaction_metadata.target
