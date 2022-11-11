import vampytest

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
    channel_id = 202211070006
    guild_id = 202211070007
    guild_locale = Locale.hindi
    interaction = InteractionMetadataApplicationCommand(name = '3L')
    interaction_type = InteractionType.application_command
    locale = Locale.thai
    message = Message.precreate(202211070008, content = 'Rise')
    token = 'Fall'
    user = User.precreate(202211070009, name = 'masuta spark')
    user_permissions = Permission(234)
    guild_profile = GuildProfile(nick = 'Senya')
    interaction_id = 202211070010
    
    
    data = {
        'application_id': str(application_id),
        'app_permissions': format(application_permissions, 'd'),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
        'guild_locale': guild_locale.value,
        'data': interaction.to_data(defaults = True),
        'type': interaction_type.value,
        'locale': locale.value,
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
    vampytest.assert_eq(interaction_event.channel_id, channel_id)
    vampytest.assert_eq(interaction_event.guild_id, guild_id)
    vampytest.assert_is(interaction_event.guild_locale, guild_locale)
    vampytest.assert_eq(interaction_event.interaction, interaction)
    vampytest.assert_is(interaction_event.locale, locale)
    vampytest.assert_is(interaction_event.message, message)
    vampytest.assert_eq(interaction_event.token, token)
    vampytest.assert_is(interaction_event.type, interaction_type)
    vampytest.assert_is(interaction_event.user, user)
    vampytest.assert_eq(interaction_event.user_permissions, user_permissions)
    
    vampytest.assert_eq(interaction_event.user.guild_profiles[guild_id], guild_profile)
    vampytest.assert_eq(interaction_event._cached_users, [user]),


def test__InteractionEvent__to_data():
    """
    Tests whether ``InteractionEvent.to_data`` works as intended.
    
    Case: include defaults.
    """
    application_id = 202211070019
    application_permissions = Permission(123)
    channel_id = 202211070020
    guild_id = 202211070021
    guild_locale = Locale.hindi
    interaction = InteractionMetadataApplicationCommand(name = '3L')
    interaction_type = InteractionType.application_command
    locale = Locale.thai
    message = Message.precreate(202211070022, content = 'Rise')
    token = 'Fall'
    user = User.precreate(202211070023, name = 'masuta spark')
    user_permissions = Permission(234)
    guild_profile = GuildProfile(nick = 'Senya')
    interaction_id = 202211070024
    user.guild_profiles[guild_id] = guild_profile
    
    
    interaction_event = InteractionEvent.precreate(
        interaction_id,
        application_id = application_id,
        application_permissions = application_permissions,
        channel_id = channel_id,
        guild_id = guild_id,
        guild_locale = guild_locale,
        interaction = interaction,
        interaction_type = interaction_type,
        locale = locale,
        message = message,
        token = token,
        user = user,
        user_permissions = user_permissions
    )
    
    data = {
        'application_id': str(application_id),
        'app_permissions': format(application_permissions, 'd'),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
        'guild_locale': guild_locale.value,
        'id': str(interaction_id),
        'locale': locale.value,
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
        data,
    )
