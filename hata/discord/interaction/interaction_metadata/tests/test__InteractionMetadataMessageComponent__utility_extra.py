import vampytest

from ....channel import Channel
from ....component import ComponentType
from ....role import Role
from ....user import User

from ...resolved import Resolved

from ..message_component import InteractionMetadataMessageComponent


def test__InteractionMetadataMessageComponent__iter_values():
    """
    Tests whether ``InteractionMetadataMessageComponent.iter_values`` works as intended.
    """
    for values, expected_output in (
        (None, []),
        (['automatically'], ['automatically']),
        (['push', 'up'], ['push', 'up']),
    ):
        interaction_metadata = InteractionMetadataMessageComponent(values = values)
    vampytest.assert_eq([*interaction_metadata.iter_values()], expected_output)


def test__InteractionMetadataMessageComponent__iter_entries():
    """
    Tests whether ``InteractionMetadataMessageComponent.iter_entities`` works as intended.
    """
    role = Role.precreate(202211100012)
    user = User.precreate(202211100013)
    
    resolved = Resolved(
        roles = [role],
        users = [user]
    )
    
    for values, expected_output in (
        (None, []),
        ([str(role.id)], [role]),
        ([str(role.id), str(user.id)], [role, user]),
    ):
        interaction_metadata = InteractionMetadataMessageComponent(
            values = values,
            component_type = ComponentType.mentionable_select,
            resolved = resolved,
        )
        
        vampytest.assert_eq([*interaction_metadata.iter_entities()], expected_output)


def test__MessageComponent__entities():
    """
    Tests whether ``MessageComponent.entities`` works as intended.
    """
    extra_target_id = 202211080021
    
    channel = Channel.precreate(202211080018)
    role = Role.precreate(202211080019)
    user = User.precreate(202211080020)
    
    resolved = Resolved(
        channels = [channel],
        roles = [role],
        users = [user]
    )
    
    for interaction_metadata, expected_output in (
        (
            InteractionMetadataMessageComponent(
                resolved = resolved,
            ),
            [],
        ), (
            InteractionMetadataMessageComponent(
                resolved = resolved,
                values = [str(extra_target_id)],
            ),
            [],
        ), (
            InteractionMetadataMessageComponent(
                resolved = resolved,
                values = ['owo'],
            ),
            [],
        ), (
            InteractionMetadataMessageComponent(
                values = [str(extra_target_id)],
            ),
            [],
        ), (
            InteractionMetadataMessageComponent(
                resolved = resolved,
                values = [str(channel.id)],
            ),
            [],
        ), (
            InteractionMetadataMessageComponent(
                values = [str(extra_target_id)],
                component_type = ComponentType.user_select,
            ),
            [],
        ), (
            InteractionMetadataMessageComponent(
                resolved = resolved,
                values = [str(channel.id)],
                component_type = ComponentType.channel_select,
            ),
            [channel],
        ), (
            InteractionMetadataMessageComponent(
                resolved = resolved,
                values = [str(user.id)],
                component_type = ComponentType.user_select,
            ),
            [user],
        ), (
            InteractionMetadataMessageComponent(
                resolved = resolved,
                values = [str(role.id)],
                component_type = ComponentType.role_select,
            ),
            [role],
        ), (
            InteractionMetadataMessageComponent(
                resolved = resolved,
                values = [str(role.id), str(user.id)],
                component_type = ComponentType.mentionable_select,
            ),
            [role, user],
        )
    ):
        vampytest.assert_eq(interaction_metadata.entities, expected_output)



def _iter_options__value():
    yield None, None
    yield ['automatically'], 'automatically'
    yield ['push', 'up'], 'push'


@vampytest._(vampytest.call_from(_iter_options__value()).returning_last())
def test__InteractionMetadataMessageComponent__value(values):
    """
    Tests whether ``InteractionMetadataMessageComponent.value`` works as intended.
    
    Parameters
    ----------
    values : `None`, `list` of `str`
        Values to create the metadata with.
    
    Returns
    -------
    output : `None`, `str`
    """
    interaction_metadata = InteractionMetadataMessageComponent(values = values)
    return interaction_metadata.value
