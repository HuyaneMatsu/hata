import vampytest

from ....channel import Channel
from ....message import Attachment, Message
from ....role import Role
from ....user import User

from ...resolved import Resolved

from ..application_command import InteractionMetadataApplicationCommand
from ..message_component import InteractionMetadataMessageComponent


@vampytest.call_with(InteractionMetadataApplicationCommand)
@vampytest.call_with(InteractionMetadataMessageComponent)
def test__InteractionMetadata__resolve_attachment(interaction_metadata_type):
    """
    Tests whether ``.resolve_attachment`` works as intended.
    
    Parameters
    ----------
    interaction_metadata_type : `type<InteractionMetadataBase>`
        The interaction metadata type to run the test with.
    """
    attachment = Attachment.precreate(202211100000)
    resolved = Resolved(attachments = [attachment])
    
    for resolved, entity_id, expected_output in (
        (None, 0, None),
        (None, attachment.id, None),
        (Resolved(), 0, None),
        (resolved, 0, None),
        (resolved, attachment.id, attachment),
    ):
        interaction_metadata = interaction_metadata_type(resolved = resolved)
        output = interaction_metadata.resolve_attachment(entity_id)
        vampytest.assert_is(output, expected_output)


@vampytest.call_with(InteractionMetadataApplicationCommand)
@vampytest.call_with(InteractionMetadataMessageComponent)
def test__InteractionMetadata__resolve_channel(interaction_metadata_type):
    """
    Tests whether ``.resolve_channel`` works as intended.
    
    Parameters
    ----------
    interaction_metadata_type : `type<InteractionMetadataBase>`
        The interaction metadata type to run the test with.
    """
    channel = Channel.precreate(202211100001)
    resolved = Resolved(channels = [channel])
    
    for resolved, entity_id, expected_output in (
        (None, 0, None),
        (None, channel.id, None),
        (Resolved(), 0, None),
        (resolved, 0, None),
        (resolved, channel.id, channel),
    ):
        interaction_metadata = interaction_metadata_type(resolved = resolved)
        output = interaction_metadata.resolve_channel(entity_id)
        vampytest.assert_is(output, expected_output)


@vampytest.call_with(InteractionMetadataApplicationCommand)
@vampytest.call_with(InteractionMetadataMessageComponent)
def test__InteractionMetadata__resolve_role(interaction_metadata_type):
    """
    Tests whether ``.resolve_role`` works as intended.
    
    Parameters
    ----------
    interaction_metadata_type : `type<InteractionMetadataBase>`
        The interaction metadata type to run the test with.
    """
    role = Role.precreate(202211100002)
    resolved = Resolved(roles = [role])
    
    for resolved, entity_id, expected_output in (
        (None, 0, None),
        (None, role.id, None),
        (Resolved(), 0, None),
        (resolved, 0, None),
        (resolved, role.id, role),
    ):
        interaction_metadata = interaction_metadata_type(resolved = resolved)
        output = interaction_metadata.resolve_role(entity_id)
        vampytest.assert_is(output, expected_output)


@vampytest.call_with(InteractionMetadataApplicationCommand)
@vampytest.call_with(InteractionMetadataMessageComponent)
def test__InteractionMetadata__resolve_message(interaction_metadata_type):
    """
    Tests whether ``.resolve_message`` works as intended.
    
    Parameters
    ----------
    interaction_metadata_type : `type<InteractionMetadataBase>`
        The interaction metadata type to run the test with.
    """
    message = Message.precreate(202211100003)
    resolved = Resolved(messages = [message])
    
    for resolved, entity_id, expected_output in (
        (None, 0, None),
        (None, message.id, None),
        (Resolved(), 0, None),
        (resolved, 0, None),
        (resolved, message.id, message),
    ):
        interaction_metadata = interaction_metadata_type(resolved = resolved)
        output = interaction_metadata.resolve_message(entity_id)
        vampytest.assert_is(output, expected_output)


@vampytest.call_with(InteractionMetadataApplicationCommand)
@vampytest.call_with(InteractionMetadataMessageComponent)
def test__InteractionMetadata__resolve_user(interaction_metadata_type):
    """
    Tests whether ``.resolve_user`` works as intended.
    
    Parameters
    ----------
    interaction_metadata_type : `type<InteractionMetadataBase>`
        The interaction metadata type to run the test with.
    """
    user = User.precreate(202211100004)
    resolved = Resolved(users = [user])
    
    for resolved, entity_id, expected_output in (
        (None, 0, None),
        (None, user.id, None),
        (Resolved(), 0, None),
        (resolved, 0, None),
        (resolved, user.id, user),
    ):
        interaction_metadata = interaction_metadata_type(resolved = resolved)
        output = interaction_metadata.resolve_user(entity_id)
        vampytest.assert_is(output, expected_output)


@vampytest.call_with(InteractionMetadataApplicationCommand)
@vampytest.call_with(InteractionMetadataMessageComponent)
def test__InteractionMetadata__resolve_mentionable(interaction_metadata_type):
    """
    Tests whether ``.resolve_mentionable`` works as intended.
    
    Parameters
    ----------
    interaction_metadata_type : `type<InteractionMetadataBase>`
        The interaction metadata type to run the test with.
    """
    role = Role.precreate(202211100005)
    user = User.precreate(202211100006)
    
    resolved = Resolved(roles = [role], users = [user])
    
    for resolved, entity_id, expected_output in (
        (None, 0, None),
        (None, role.id, None),
        (None, user.id, None),
        (Resolved(), 0, None),
        (resolved, 0, None),
        (resolved, role.id, role),
        (resolved, user.id, user),
    ):
        interaction_metadata = interaction_metadata_type(resolved = resolved)
        output = interaction_metadata.resolve_mentionable(entity_id)
        vampytest.assert_is(output, expected_output)


@vampytest.call_with(InteractionMetadataApplicationCommand)
@vampytest.call_with(InteractionMetadataMessageComponent)
def test__InteractionMetadata__resolve_entity(interaction_metadata_type):
    """
    Tests whether ``.resolve_entity`` works as intended.
    
    Parameters
    ----------
    interaction_metadata_type : `type<InteractionMetadataBase>`
        The interaction metadata type to run the test with.
    """
    attachment = Attachment.precreate(202211100007)
    channel = Channel.precreate(202211100008)
    message = Message.precreate(202211100009)
    role = Role.precreate(202211100010)
    user = User.precreate(202211100011)
    
    resolved = Resolved(
        attachments = [attachment],
        channels = [channel],
        messages = [message],
        roles = [role],
        users = [user]
    )
    
    for resolved, entity_id, expected_output in (
        (None, 0, None),
        (None, attachment.id, None),
        (None, channel.id, None),
        (None, message.id, None),
        (None, role.id, None),
        (None, user.id, None),
        (Resolved(), 0, None),
        (resolved, 0, None),
        (resolved, attachment.id, attachment),
        (resolved, channel.id, channel),
        (resolved, message.id, message),
        (resolved, role.id, role),
        (resolved, user.id, user),
    ):
        interaction_metadata = interaction_metadata_type(resolved = resolved)
        output = interaction_metadata.resolve_entity(entity_id)
        vampytest.assert_is(output, expected_output)
