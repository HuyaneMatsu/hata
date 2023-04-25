import vampytest

from ....channel import Channel
from ....localization import Locale
from ....message import Message
from ....permission import Permission
from ....user import User
from ....utils import now_as_id

from ...interaction_metadata import InteractionMetadataApplicationCommand, InteractionMetadataMessageComponent
from ...responding.constants import (
    RESPONSE_FLAG_ACKNOWLEDGED, RESPONSE_FLAG_ACKNOWLEDGING, RESPONSE_FLAG_DEFERRED, RESPONSE_FLAG_RESPONDED,
    RESPONSE_FLAG_RESPONDING
)

from ..interaction_event import InteractionEvent
from ..preinstanced import InteractionType

from .test__InteractionEvent__constructor import _assert_attributes_set


def test__InteractionEvent__is_unanswered():
    """
    Tests whether ``InteractionEvent.is_unanswered`` works as intended.
    """
    interaction_event = InteractionEvent()
    vampytest.assert_true(interaction_event.is_unanswered())
    
    interaction_event = InteractionEvent()
    interaction_event._response_flag |= RESPONSE_FLAG_ACKNOWLEDGING
    vampytest.assert_false(interaction_event.is_unanswered())


def test__InteractionEvent__is_acknowledging():
    """
    Tests whether ``InteractionEvent.is_acknowledging`` works as intended.
    """
    interaction_event = InteractionEvent()
    vampytest.assert_false(interaction_event.is_acknowledging())
    
    interaction_event = InteractionEvent()
    interaction_event._response_flag |= RESPONSE_FLAG_ACKNOWLEDGING
    vampytest.assert_true(interaction_event.is_acknowledging())


def test__InteractionEvent__is_acknowledged():
    """
    Tests whether ``InteractionEvent.is_acknowledged`` works as intended.
    """
    interaction_event = InteractionEvent()
    vampytest.assert_false(interaction_event.is_acknowledged())
    
    interaction_event = InteractionEvent()
    interaction_event._response_flag |= RESPONSE_FLAG_ACKNOWLEDGED
    vampytest.assert_true(interaction_event.is_acknowledged())


def test__InteractionEvent__is_deferred():
    """
    Tests whether ``InteractionEvent.is_deferred`` works as intended.
    """
    interaction_event = InteractionEvent()
    vampytest.assert_false(interaction_event.is_deferred())
    
    interaction_event = InteractionEvent()
    interaction_event._response_flag |= RESPONSE_FLAG_DEFERRED
    vampytest.assert_true(interaction_event.is_deferred())

    interaction_event = InteractionEvent()
    interaction_event._response_flag |= RESPONSE_FLAG_DEFERRED | RESPONSE_FLAG_RESPONDED
    vampytest.assert_false(interaction_event.is_deferred())


def test__InteractionEvent__is_responding():
    """
    Tests whether ``InteractionEvent.is_responding`` works as intended.
    """
    interaction_event = InteractionEvent()
    vampytest.assert_false(interaction_event.is_responding())
    
    interaction_event = InteractionEvent()
    interaction_event._response_flag |= RESPONSE_FLAG_RESPONDING
    vampytest.assert_true(interaction_event.is_responding())


def test__InteractionEvent__is_responded():
    """
    Tests whether ``InteractionEvent.is_responded`` works as intended.
    """
    interaction_event = InteractionEvent()
    vampytest.assert_false(interaction_event.is_responded())
    
    interaction_event = InteractionEvent()
    interaction_event._response_flag |= RESPONSE_FLAG_RESPONDED
    vampytest.assert_true(interaction_event.is_responded())


def test__InteractionEvent__is_expired():
    """
    Tests whether ``InteractionEvent.is_expired`` works as intended.
    """
    interaction_event = InteractionEvent()
    vampytest.assert_true(interaction_event.is_expired())
    
    interaction_event = InteractionEvent.precreate(now_as_id())
    vampytest.assert_false(interaction_event.is_expired())



def test__InteractionEvent__copy():
    """
    Tests whether ``InteractionEvent.copy`` works as intended.
    """
    application_id = 202211070052
    application_permissions = Permission(123)
    channel = Channel.precreate(202211070053)
    guild_id = 202211070054
    guild_locale = Locale.hindi
    interaction = InteractionMetadataApplicationCommand(name = '3L')
    interaction_type = InteractionType.application_command
    locale = Locale.thai
    message = Message.precreate(202211070055, content = 'Rise')
    token = 'Fall'
    user = User.precreate(202211070056, name = 'masuta spark')
    user_permissions = Permission(234)
    
    interaction_id = 202211070057
    
    interaction_event = InteractionEvent.precreate(
        interaction_id,
        application_id = application_id,
        application_permissions = application_permissions,
        channel = channel,
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
    
    copy = interaction_event.copy()
    _assert_attributes_set(copy)
    vampytest.assert_not_is(interaction_event, copy)
    vampytest.assert_eq(interaction_event, copy)
    vampytest.assert_eq(copy.id, 0)


def test__InteractionEvent__copy__with__0():
    """
    Tests whether ``InteractionEvent.copy_with`` works as intended.
    """
    application_id = 202211070058
    application_permissions = Permission(123)
    channel = Channel.precreate(202211070059)
    guild_id = 202211070060
    guild_locale = Locale.hindi
    interaction = InteractionMetadataApplicationCommand(name = '3L')
    interaction_type = InteractionType.application_command
    locale = Locale.thai
    message = Message.precreate(202211070061, content = 'Rise')
    token = 'Fall'
    user = User.precreate(202211070062, name = 'masuta spark')
    user_permissions = Permission(234)
    
    interaction_id = 202211070063
    
    interaction_event = InteractionEvent.precreate(
        interaction_id,
        application_id = application_id,
        application_permissions = application_permissions,
        channel = channel,
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
    
    copy = interaction_event.copy_with()
    _assert_attributes_set(copy)
    vampytest.assert_not_is(interaction_event, copy)
    vampytest.assert_eq(interaction_event, copy)
    vampytest.assert_eq(copy.id, 0)


def test__InteractionEvent__copy__with__1():
    """
    Tests whether ``InteractionEvent.copy_with`` works as intended.
    """
    old_application_id = 202211070064
    new_application_id = 202211070065
    old_application_permissions = Permission(123)
    new_application_permissions = Permission(951)
    old_channel = Channel.precreate(202211070066)
    new_channel = Channel.precreate(202211070067)
    old_guild_id = 202211070068
    new_guild_id = 202211070069
    old_guild_locale = Locale.hindi
    new_guild_locale = Locale.chinese_cn
    old_interaction = InteractionMetadataApplicationCommand(name = '3L')
    new_interaction = InteractionMetadataMessageComponent(custom_id = 'Renna')
    old_interaction_type = InteractionType.application_command
    new_interaction_type = InteractionType.message_component
    old_locale = Locale.thai
    new_locale = Locale.finnish
    old_message = Message.precreate(202211070070, content = 'Rise')
    new_message = Message.precreate(202211070071, content = 'Rise')
    old_token = 'Fall'
    new_token = 'Fall'
    old_user = User.precreate(202211070072, name = 'masuta spark')
    new_user = User.precreate(202211070073, name = 'Marisa')
    old_user_permissions = Permission(234)
    new_user_permissions = Permission(654)
    
    interaction_id = 202211070063
    
    interaction_event = InteractionEvent(
        application_id = old_application_id,
        application_permissions = old_application_permissions,
        channel = old_channel,
        guild_id = old_guild_id,
        guild_locale = old_guild_locale,
        interaction = old_interaction,
        interaction_type = old_interaction_type,
        locale = old_locale,
        message = old_message,
        token = old_token,
        user = old_user,
        user_permissions = old_user_permissions
    )
    
    copy = interaction_event.copy_with(
        application_id = new_application_id,
        application_permissions = new_application_permissions,
        channel = new_channel,
        guild_id = new_guild_id,
        guild_locale = new_guild_locale,
        interaction = new_interaction,
        interaction_type = new_interaction_type,
        locale = new_locale,
        message = new_message,
        token = new_token,
        user = new_user,
        user_permissions = new_user_permissions
    )
    _assert_attributes_set(copy)
    vampytest.assert_not_is(interaction_event, copy)

    vampytest.assert_eq(copy.application_id, new_application_id)
    vampytest.assert_eq(copy.application_permissions, new_application_permissions)
    vampytest.assert_is(copy.channel, new_channel)
    vampytest.assert_eq(copy.guild_id, new_guild_id)
    vampytest.assert_is(copy.guild_locale, new_guild_locale)
    vampytest.assert_eq(copy.interaction, new_interaction)
    vampytest.assert_is(copy.locale, new_locale)
    vampytest.assert_is(copy.message, new_message)
    vampytest.assert_eq(copy.token, new_token)
    vampytest.assert_is(copy.type, new_interaction_type)
    vampytest.assert_is(copy.user, new_user)
    vampytest.assert_eq(copy.user_permissions, new_user_permissions)
