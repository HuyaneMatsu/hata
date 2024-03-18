import vampytest

from scarletio import Task

from ....application import Entitlement
from ....channel import Channel
from ....guild import Guild, create_partial_guild_from_id
from ....localization import Locale
from ....permission import Permission
from ....message import Message
from ....user import ClientUserBase, User

from ...interaction_metadata import InteractionMetadataBase, InteractionMetadataApplicationCommand

from ..interaction_event import InteractionEvent
from ..preinstanced import InteractionType


def _assert_attributes_set(interaction_event):
    """
    Asserts whether all attributes are set of the given interaction event.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The interaction event to assert.
    """
    vampytest.assert_instance(interaction_event, InteractionEvent)
    
    vampytest.assert_instance(interaction_event._async_task, Task, nullable = True)
    vampytest.assert_instance(interaction_event._response_flags, int)
    
    vampytest.assert_instance(interaction_event.application_id, int)
    vampytest.assert_instance(interaction_event.application_permissions, Permission)
    vampytest.assert_instance(interaction_event.channel, Channel)
    vampytest.assert_instance(interaction_event.entitlements, tuple, nullable = True)
    vampytest.assert_instance(interaction_event.guild, Guild, nullable = True)
    vampytest.assert_instance(interaction_event.id, int)
    vampytest.assert_instance(interaction_event.interaction, InteractionMetadataBase)
    vampytest.assert_instance(interaction_event.message, Message, nullable = True)
    vampytest.assert_instance(interaction_event.token, str)
    vampytest.assert_instance(interaction_event.type, InteractionType)
    vampytest.assert_instance(interaction_event.user, ClientUserBase)
    vampytest.assert_instance(interaction_event.user_locale, Locale)
    vampytest.assert_instance(interaction_event.user_permissions, Permission)


def test__InteractionEvent__new__no_fields():
    """
    Tests whether ``InteractionEvent.__new__`` works as intended.
    
    Case: No parameters given.
    """
    interaction_event = InteractionEvent()
    
    _assert_attributes_set(interaction_event)


def test__InteractionEvent__new__all_fields():
    """
    Tests whether ``InteractionEvent.__new__`` works as intended.
    
    Case: All parameters given.
    """
    application_id = 202211070000
    application_permissions = Permission(123)
    channel = Channel.precreate(202211070001)
    entitlements = [Entitlement.precreate(202310050010), Entitlement.precreate(202310050011)]
    guild = create_partial_guild_from_id(202211070002)
    interaction = InteractionMetadataApplicationCommand(name = '3L')
    interaction_type = InteractionType.application_command
    message = Message.precreate(202211070003, content = 'Rise')
    token = 'Fall'
    user = User.precreate(202211070004, name = 'masuta spark')
    user_locale = Locale.thai
    user_permissions = Permission(234)
    
    interaction_event = InteractionEvent(
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


def test__InteractionEvent__create_empty():
    """
    Tests whether ``InteractionEvent._create_empty`` works as intended.
    
    Case: No parameters given.
    """
    interaction_id = 202211070011
    
    interaction_event = InteractionEvent._create_empty(interaction_id)
    
    _assert_attributes_set(interaction_event)
    vampytest.assert_eq(interaction_event.id, interaction_id)



def test__InteractionEvent__precreate__no_fields():
    """
    Tests whether ``InteractionEvent.precreate`` works as intended.
    
    Case: No parameters given.
    """
    interaction_id = 202211070017
    
    interaction_event = InteractionEvent.precreate(interaction_id)
    
    _assert_attributes_set(interaction_event)
    vampytest.assert_eq(interaction_event.id, interaction_id)


def test__InteractionEvent__precreate__all_fields():
    """
    Tests whether ``InteractionEvent.precreate`` works as intended.
    
    Case: All parameters given.
    """
    application_id = 202211070012
    application_permissions = Permission(123)
    channel = Channel.precreate(202211070013)
    entitlements = [Entitlement.precreate(202310050012), Entitlement.precreate(202310050013)]
    guild = create_partial_guild_from_id(202211070014)
    interaction = InteractionMetadataApplicationCommand(name = '3L')
    interaction_type = InteractionType.application_command
    message = Message.precreate(202211070015, content = 'Rise')
    token = 'Fall'
    user = User.precreate(202211070016, name = 'masuta spark')
    user_locale = Locale.thai
    user_permissions = Permission(234)
    
    interaction_id = 202211070018
    
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
    
    _assert_attributes_set(interaction_event)
    vampytest.assert_eq(interaction_event.id, interaction_id)
    
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
