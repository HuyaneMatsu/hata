import vampytest

from ....channel import Channel
from ....message import Attachment, Message
from ....role import Role
from ....user import User

from ...resolved import Resolved

from ..application_command import InteractionMetadataApplicationCommand


def test__InteractionMetadataApplicationCommand__target():
    """
    Tests whether ``InteractionMetadataApplicationCommand.target`` works as intended.
    """
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
    
    for interaction_metadata, expected_output in (
        (
            InteractionMetadataApplicationCommand(),
            None,
        ), (
            InteractionMetadataApplicationCommand(target_id = extra_target_id),
            None,
        ), (
            InteractionMetadataApplicationCommand(resolved = resolved),
            None,
        ), (
            InteractionMetadataApplicationCommand(resolved = resolved, target_id = extra_target_id),
            None,
        ), (
            InteractionMetadataApplicationCommand(resolved = resolved, target_id = attachment.id),
            attachment,
        ), (
            InteractionMetadataApplicationCommand(resolved = resolved, target_id = channel.id),
            channel,
        ), (
            InteractionMetadataApplicationCommand(resolved = resolved, target_id = message.id),
            message,
        ), (
            InteractionMetadataApplicationCommand(resolved = resolved, target_id = role.id),
            role,
        ), (
            InteractionMetadataApplicationCommand(resolved = resolved, target_id = user.id),
            user,
        ),
    ):
        vampytest.assert_is(interaction_metadata.target, expected_output)
