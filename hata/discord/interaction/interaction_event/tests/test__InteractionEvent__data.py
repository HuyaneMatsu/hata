import vampytest

from ....application import Entitlement
from ....channel import Channel
from ....guild import create_interaction_guild_data, create_partial_guild_from_id
from ....localization import Locale
from ....permission import Permission
from ....message import Message
from ....user import GuildProfile, User

from ...interaction_metadata import InteractionMetadataApplicationCommand

from ..interaction_event import InteractionEvent
from ..preinstanced import InteractionType

from .test__InteractionEvent__constructor import _assert_attributes_set


def test__InteractionEvent__from_data():
    """
    Tests whether ``InteractionEvent.from_data`` works as intended.
    """
    application_id = 202211070005
    application_permissions = Permission(123)
    channel = Channel.precreate(202211070006)
    entitlements = [Entitlement.precreate(202310050014), Entitlement.precreate(202310050015)]
    guild = create_partial_guild_from_id(202211070007)
    interaction = InteractionMetadataApplicationCommand(name = '3L')
    interaction_type = InteractionType.application_command
    message = Message.precreate(202211070008, content = 'Rise')
    token = 'Fall'
    user = User.precreate(202211070009, name = 'masuta spark')
    user_locale = Locale.thai
    user_permissions = Permission(234)
    guild_profile = GuildProfile(nick = 'Senya')
    interaction_id = 202211070010
    
    
    data = {
        'application_id': str(application_id),
        'app_permissions': format(application_permissions, 'd'),
        'channel': channel.to_data(include_internals = True),
        'entitlements': [entitlement.to_data(include_internals = True) for entitlement in entitlements],
        'guild': create_interaction_guild_data(guild),
        'data': interaction.to_data(defaults = True),
        'type': interaction_type.value,
        'locale': user_locale.value,
        'message': message.to_data(defaults = True, include_internals = True),
        'token': token,
        'member': {
            **guild_profile.to_data(defaults = True, include_internals = True),
            'permissions': format(user_permissions, 'd'),
            'user': user.to_data(defaults = True, include_internals = True),
        },
        'id': str(interaction_id),
    }
    
    interaction_event = InteractionEvent.from_data(data)
    
    _assert_attributes_set(interaction_event)
    
    vampytest.assert_eq(interaction_event.application_id, application_id)
    vampytest.assert_eq(interaction_event.application_permissions, application_permissions)
    vampytest.assert_is(interaction_event.channel, channel)
    vampytest.assert_eq(interaction_event.entitlements, tuple(entitlements))
    vampytest.assert_is(interaction_event.guild, guild)
    vampytest.assert_eq(interaction_event.interaction, interaction)
    vampytest.assert_is(interaction_event.message, message)
    vampytest.assert_eq(interaction_event.token, token)
    vampytest.assert_is(interaction_event.type, interaction_type)
    vampytest.assert_is(interaction_event.user, user)
    vampytest.assert_is(interaction_event.user_locale, user_locale)
    vampytest.assert_eq(interaction_event.user_permissions, user_permissions)
    
    vampytest.assert_eq(interaction_event.user.guild_profiles[guild.id], guild_profile)


def test__InteractionEvent__to_data():
    """
    Tests whether ``InteractionEvent.to_data`` works as intended.
    
    Case: include defaults.
    """
    application_id = 202211070019
    application_permissions = Permission(123)
    channel = Channel.precreate(202211070020)
    entitlements = [Entitlement.precreate(202310050016), Entitlement.precreate(202310050017)]
    guild = create_partial_guild_from_id(202211070021)
    interaction = InteractionMetadataApplicationCommand(name = '3L')
    interaction_type = InteractionType.application_command
    message = Message.precreate(202211070022, content = 'Rise')
    token = 'Fall'
    user = User.precreate(202211070023, name = 'masuta spark')
    user_locale = Locale.thai
    user_permissions = Permission(234)
    guild_profile = GuildProfile(nick = 'Senya')
    interaction_id = 202211070024
    user.guild_profiles[guild.id] = guild_profile
    
    
    interaction_event = InteractionEvent.precreate(
        interaction_id,
        application_id = application_id,
        application_permissions = application_permissions,
        channel = channel,
        entitlements = entitlements,
        guild = guild,
        interaction = interaction,
        interaction_type = interaction_type,
        message = message,
        token = token,
        user = user,
        user_locale = user_locale,
        user_permissions = user_permissions
    )
    
    expected_output = {
        'application_id': str(application_id),
        'app_permissions': format(application_permissions, 'd'),
        'channel': channel.to_data(defaults = True, include_internals = True),
        'entitlements': [
            entitlement.to_data(defaults = True, include_internals = True) for entitlement in entitlements
        ],
        'guild': create_interaction_guild_data(guild),
        'guild_id': str(guild.id),
        'guild_locale': guild.locale.value,
        'id': str(interaction_id),
        'locale': user_locale.value,
        'message': message.to_data(defaults = True, include_internals = True),
        'token': token,
        'type': interaction_type.value,
        'member': {
            **guild_profile.to_data(defaults = True, include_internals = True),
            'permissions': format(user_permissions, 'd'),
            'user': user.to_data(defaults = True, include_internals = True),
        },
        'data': interaction.to_data(defaults = True),
    }
    
    
    vampytest.assert_eq(
        interaction_event.to_data(
            defaults = True,
        ),
        expected_output,
    )
