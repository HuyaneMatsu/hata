import vampytest

from ....application import ApplicationIntegrationType, Entitlement, SKU
from ....channel import Channel
from ....guild import create_partial_guild_from_id
from ....localization import Locale
from ....message import Message
from ....permission import Permission
from ....user import ClientUserBase, User, create_partial_user_from_id
from ....utils import now_as_id

from ...interaction_metadata import InteractionMetadataApplicationCommand, InteractionMetadataMessageComponent
from ...responding.constants import (
    RESPONSE_FLAG_ACKNOWLEDGED, RESPONSE_FLAG_ACKNOWLEDGING, RESPONSE_FLAG_DEFERRED, RESPONSE_FLAG_EPHEMERAL,
    RESPONSE_FLAG_RESPONDED, RESPONSE_FLAG_RESPONDING
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
    interaction_event._response_flags |= RESPONSE_FLAG_ACKNOWLEDGING
    vampytest.assert_false(interaction_event.is_unanswered())


def test__InteractionEvent__is_acknowledging():
    """
    Tests whether ``InteractionEvent.is_acknowledging`` works as intended.
    """
    interaction_event = InteractionEvent()
    vampytest.assert_false(interaction_event.is_acknowledging())
    
    interaction_event = InteractionEvent()
    interaction_event._response_flags |= RESPONSE_FLAG_ACKNOWLEDGING
    vampytest.assert_true(interaction_event.is_acknowledging())


def test__InteractionEvent__is_acknowledged():
    """
    Tests whether ``InteractionEvent.is_acknowledged`` works as intended.
    """
    interaction_event = InteractionEvent()
    vampytest.assert_false(interaction_event.is_acknowledged())
    
    interaction_event = InteractionEvent()
    interaction_event._response_flags |= RESPONSE_FLAG_ACKNOWLEDGED
    vampytest.assert_true(interaction_event.is_acknowledged())


def test__InteractionEvent__is_deferred():
    """
    Tests whether ``InteractionEvent.is_deferred`` works as intended.
    """
    interaction_event = InteractionEvent()
    vampytest.assert_false(interaction_event.is_deferred())
    
    interaction_event = InteractionEvent()
    interaction_event._response_flags |= RESPONSE_FLAG_DEFERRED
    vampytest.assert_true(interaction_event.is_deferred())

    interaction_event = InteractionEvent()
    interaction_event._response_flags |= RESPONSE_FLAG_DEFERRED | RESPONSE_FLAG_RESPONDED
    vampytest.assert_false(interaction_event.is_deferred())


def test__InteractionEvent__is_responding():
    """
    Tests whether ``InteractionEvent.is_responding`` works as intended.
    """
    interaction_event = InteractionEvent()
    vampytest.assert_false(interaction_event.is_responding())
    
    interaction_event = InteractionEvent()
    interaction_event._response_flags |= RESPONSE_FLAG_RESPONDING
    vampytest.assert_true(interaction_event.is_responding())


def test__InteractionEvent__is_responded():
    """
    Tests whether ``InteractionEvent.is_responded`` works as intended.
    """
    interaction_event = InteractionEvent()
    vampytest.assert_false(interaction_event.is_responded())
    
    interaction_event = InteractionEvent()
    interaction_event._response_flags |= RESPONSE_FLAG_RESPONDED
    vampytest.assert_true(interaction_event.is_responded())


def test__InteractionEvent__is_expired():
    """
    Tests whether ``InteractionEvent.is_expired`` works as intended.
    """
    interaction_event = InteractionEvent()
    vampytest.assert_true(interaction_event.is_expired())
    
    interaction_event = InteractionEvent.precreate(now_as_id())
    vampytest.assert_false(interaction_event.is_expired())


def test__InteractionEvent__is_response_invoking_user_only():
    """
    Tests whether ``InteractionEvent.is_response_invoking_user_only`` works as intended.
    """
    interaction_event = InteractionEvent()
    vampytest.assert_false(interaction_event.is_response_invoking_user_only())
    
    interaction_event = InteractionEvent()
    interaction_event._response_flags |= RESPONSE_FLAG_EPHEMERAL
    vampytest.assert_true(interaction_event.is_response_invoking_user_only())


def test__InteractionEvent__copy():
    """
    Tests whether ``InteractionEvent.copy`` works as intended.
    """
    application_id = 202211070052
    application_permissions = Permission(123)
    attachment_size_limit = 10 << 22
    authorizer_user_ids = {
        ApplicationIntegrationType.user_install: 202407170017,
        ApplicationIntegrationType.guild_install: 202407170018,
    }
    channel = Channel.precreate(202211070053)
    entitlements = [Entitlement.precreate(202310050025), Entitlement.precreate(202310050026)]
    guild = create_partial_guild_from_id(202211070054)
    interaction = InteractionMetadataApplicationCommand(name = '3L')
    interaction_type = InteractionType.application_command
    message = Message.precreate(202211070055, content = 'Rise')
    token = 'Fall'
    user = User.precreate(202211070056, name = 'masuta spark')
    user_locale = Locale.thai
    user_permissions = Permission(234)
    
    interaction_id = 202211070057
    
    interaction_event = InteractionEvent.precreate(
        interaction_id,
        application_id = application_id,
        application_permissions = application_permissions,
        attachment_size_limit = attachment_size_limit,
        authorizer_user_ids = authorizer_user_ids,
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
    
    copy = interaction_event.copy()
    _assert_attributes_set(copy)
    vampytest.assert_not_is(interaction_event, copy)
    vampytest.assert_eq(interaction_event, copy)
    vampytest.assert_eq(copy.id, 0)


def test__InteractionEvent__copy__with__no_fields():
    """
    Tests whether ``InteractionEvent.copy_with`` works as intended.
    
    Case: No fields given.
    """
    application_id = 202211070058
    application_permissions = Permission(123)
    attachment_size_limit = 10 << 20
    authorizer_user_ids = {
        ApplicationIntegrationType.user_install: 202407170019,
        ApplicationIntegrationType.guild_install: 202407170020,
    }
    channel = Channel.precreate(202211070059)
    entitlements = [Entitlement.precreate(202310050027), Entitlement.precreate(202310050028)]
    guild = create_partial_guild_from_id(202211070060)
    interaction = InteractionMetadataApplicationCommand(name = '3L')
    interaction_type = InteractionType.application_command
    message = Message.precreate(202211070061, content = 'Rise')
    token = 'Fall'
    user = User.precreate(202211070062, name = 'masuta spark')
    user_locale = Locale.thai
    user_permissions = Permission(234)
    
    interaction_id = 202211070063
    
    interaction_event = InteractionEvent.precreate(
        interaction_id,
        application_id = application_id,
        application_permissions = application_permissions,
        attachment_size_limit = attachment_size_limit,
        authorizer_user_ids = authorizer_user_ids,
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
    
    copy = interaction_event.copy_with()
    _assert_attributes_set(copy)
    vampytest.assert_not_is(interaction_event, copy)
    vampytest.assert_eq(interaction_event, copy)
    vampytest.assert_eq(copy.id, 0)


def test__InteractionEvent__copy__with__all_fields():
    """
    Tests whether ``InteractionEvent.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_application_id = 202211070064
    old_application_permissions = Permission(123)
    old_attachment_size_limit = 10 << 20
    old_authorizer_user_ids = {
        ApplicationIntegrationType.user_install: 202407170021,
        ApplicationIntegrationType.guild_install: 202407170022,
    }
    old_channel = Channel.precreate(202211070066)
    old_entitlements = [Entitlement.precreate(202310050028), Entitlement.precreate(202310050029)]
    old_guild = create_partial_guild_from_id(202211070068)
    old_interaction = InteractionMetadataApplicationCommand(name = '3L')
    old_interaction_type = InteractionType.application_command
    old_message = Message.precreate(202211070070, content = 'Rise')
    old_token = 'Fall'
    old_user = User.precreate(202211070072, name = 'masuta spark')
    old_user_locale = Locale.thai
    old_user_permissions = Permission(234)
    
    new_application_id = 202211070065
    new_application_permissions = Permission(951)
    new_attachment_size_limit = 11 << 20
    new_authorizer_user_ids = {
        ApplicationIntegrationType.user_install: 202407170023,
        ApplicationIntegrationType.guild_install: 202407170024,
    }
    new_channel = Channel.precreate(202211070067)
    new_entitlements = [Entitlement.precreate(202310050030), Entitlement.precreate(202310050031)]
    new_guild = create_partial_guild_from_id(202211070069)
    new_interaction = InteractionMetadataMessageComponent(custom_id = 'Renna')
    new_interaction_type = InteractionType.message_component
    new_message = Message.precreate(202211070071, content = 'Rise')
    new_token = 'Fall'
    new_user = User.precreate(202211070073, name = 'Marisa')
    new_user_locale = Locale.finnish
    new_user_permissions = Permission(654)
    
    interaction_event = InteractionEvent(
        application_id = old_application_id,
        application_permissions = old_application_permissions,
        attachment_size_limit = old_attachment_size_limit,
        authorizer_user_ids = old_authorizer_user_ids,
        channel = old_channel,
        entitlements = old_entitlements,
        guild = old_guild,
        interaction = old_interaction,
        interaction_type = old_interaction_type,
        message = old_message,
        token = old_token,
        user = old_user,
        user_locale = old_user_locale,
        user_permissions = old_user_permissions
    )
    
    copy = interaction_event.copy_with(
        application_id = new_application_id,
        application_permissions = new_application_permissions,
        attachment_size_limit = new_attachment_size_limit,
        authorizer_user_ids = new_authorizer_user_ids,
        channel = new_channel,
        entitlements = new_entitlements,
        guild = new_guild,
        interaction = new_interaction,
        interaction_type = new_interaction_type,
        message = new_message,
        token = new_token,
        user = new_user,
        user_locale = new_user_locale,
        user_permissions = new_user_permissions
    )
    _assert_attributes_set(copy)
    vampytest.assert_not_is(interaction_event, copy)

    vampytest.assert_eq(copy.application_id, new_application_id)
    vampytest.assert_eq(copy.application_permissions, new_application_permissions)
    vampytest.assert_eq(copy.attachment_size_limit, new_attachment_size_limit)
    vampytest.assert_eq(copy.authorizer_user_ids, new_authorizer_user_ids)
    vampytest.assert_is(copy.channel, new_channel)
    vampytest.assert_eq(copy.entitlements, tuple(new_entitlements))
    vampytest.assert_is(copy.guild, new_guild)
    vampytest.assert_eq(copy.interaction, new_interaction)
    vampytest.assert_is(copy.message, new_message)
    vampytest.assert_eq(copy.token, new_token)
    vampytest.assert_is(copy.type, new_interaction_type)
    vampytest.assert_is(copy.user, new_user)
    vampytest.assert_is(copy.user_locale, new_user_locale)
    vampytest.assert_eq(copy.user_permissions, new_user_permissions)


def _iter_options__iter__has_entitlement():
    entitlement_0 = Entitlement.precreate(202310050032)
    entitlement_1 = Entitlement.precreate(202310050033)
    
    yield InteractionEvent(entitlements = None), entitlement_0, False
    yield InteractionEvent(entitlements = [entitlement_0]), entitlement_0, True
    yield InteractionEvent(entitlements = [entitlement_1]), entitlement_0, False
    yield InteractionEvent(entitlements = [entitlement_0, entitlement_1]), entitlement_0, True


@vampytest._(vampytest.call_from(_iter_options__iter__has_entitlement()).returning_last())
def test__InteractionEvent__has_entitlement(interaction_event, entitlement):
    """
    Tests whether ``InteractionEvent.has_entitlement`` works as intended.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        Interaction event to get check.
    entitlement : ``Entitlement``
        The entitlement to test for.
    
    Returns
    -------
    output : `bool`
    """
    output = interaction_event.has_entitlement(entitlement)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__iter__iter_entitlement():
    entitlement_0 = Entitlement.precreate(202310050034)
    entitlement_1 = Entitlement.precreate(202310050035)
    
    yield InteractionEvent(entitlements = None), set()
    yield InteractionEvent(entitlements = [entitlement_0]), {entitlement_0}
    yield InteractionEvent(entitlements = [entitlement_0, entitlement_1]), {entitlement_0, entitlement_1}


@vampytest._(vampytest.call_from(_iter_options__iter__iter_entitlement()).returning_last())
def test__InteractionEvent__has_entitlement(interaction_event):
    """
    Tests whether ``InteractionEvent.has_entitlement`` works as intended.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        Interaction event to get check.
    
    Returns
    -------
    output : `bool`
    """
    return {*interaction_event.iter_entitlements()}


def _iter_options__iter__has_sku():
    sku_id_0 = 202310050036
    sku_id_1 = 202310050037
    
    sku_0 = SKU.precreate(sku_id_0)
    
    entitlement_0 = Entitlement.precreate(202310050038, sku_id = sku_id_0)
    entitlement_1 = Entitlement.precreate(202310050039, sku_id = sku_id_1)
    
    yield InteractionEvent(entitlements = None), sku_0, False
    yield InteractionEvent(entitlements = [entitlement_0]), sku_0, True
    yield InteractionEvent(entitlements = [entitlement_1]), sku_0, False
    yield InteractionEvent(entitlements = [entitlement_0, entitlement_1]), sku_0, True


@vampytest._(vampytest.call_from(_iter_options__iter__has_sku()).returning_last())
def test__InteractionEvent__has_sku(interaction_event, sku):
    """
    Tests whether ``InteractionEvent.has_sku`` works as intended.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        Interaction event to get check.
    sku : ``SKU``
        The stock keeping unit to test for.
    
    Returns
    -------
    output : `bool`
    """
    output = interaction_event.has_sku(sku)
    vampytest.assert_instance(output, bool)
    return output



def _iter_options__get_authorizer_user_id():
    user_id = 202407170025
    
    yield (
        None,
        ApplicationIntegrationType.user_install,
        0,
    )
    
    yield (
        {
            ApplicationIntegrationType.user_install: user_id,
        },
        ApplicationIntegrationType.user_install,
        user_id,
    )
    
    yield (
        {
            ApplicationIntegrationType.guild_install: user_id,
        },
        ApplicationIntegrationType.user_install,
        0,
    )
    
    yield (
        {
            ApplicationIntegrationType.guild_install: user_id,
        },
        ApplicationIntegrationType.guild_install,
        user_id,
    )
    
    yield (
        {
            ApplicationIntegrationType.guild_install: user_id,
        },
        ApplicationIntegrationType.user_install,
        0,
    )
    
    
    yield (
        {
            ApplicationIntegrationType.user_install: user_id,
        },
        ApplicationIntegrationType.user_install.value,
        user_id,
    )


@vampytest._(vampytest.call_from(_iter_options__get_authorizer_user_id()).returning_last())
def test__InteractionEvent__get_authorizer_user_id(authorizer_user_ids, integration_type):
    """
    Tests whether ``InteractionEvent.get_authorizer_user_id`` works as intended.
    
    Parameters
    ----------
    authorizer_user_ids : `dict<ApplicationIntegrationType, int>`
        The authorizer users identifiers.
    
    integration_type : `ApplicationIntegrationType | int`
        Integration type to query for.
    
    Returns
    -------
    output : `int`
    """
    interaction_event = InteractionEvent(
        authorizer_user_ids = authorizer_user_ids,
    )
    
    output = interaction_event.get_authorizer_user_id(integration_type)
    vampytest.assert_instance(output, int)
    return output


def _iter_options__get_authorizer_user():
    user_id = 202407170026
    user = create_partial_user_from_id(user_id)
    
    yield (
        None,
        ApplicationIntegrationType.user_install,
        None,
    )
    
    yield (
        {
            ApplicationIntegrationType.user_install: user_id,
        },
        ApplicationIntegrationType.user_install,
        user,
    )
    
    yield (
        {
            ApplicationIntegrationType.guild_install: user_id,
        },
        ApplicationIntegrationType.user_install,
        None,
    )
    
    yield (
        {
            ApplicationIntegrationType.guild_install: user_id,
        },
        ApplicationIntegrationType.guild_install,
        user,
    )
    
    yield (
        {
            ApplicationIntegrationType.guild_install: user_id,
        },
        ApplicationIntegrationType.user_install,
        None,
    )
    
    
    yield (
        {
            ApplicationIntegrationType.user_install: user_id,
        },
        ApplicationIntegrationType.user_install.value,
        user,
    )


@vampytest._(vampytest.call_from(_iter_options__get_authorizer_user()).returning_last())
def test__InteractionEvent__get_authorizer_user(authorizer_user_ids, integration_type):
    """
    Tests whether ``InteractionEvent.get_authorizer_user`` works as intended.
    
    Parameters
    ----------
    authorizer_user_ids : `dict<ApplicationIntegrationType, int>`
        The authorizer users identifiers.
    
    integration_type : `ApplicationIntegrationType | int`
        Integration type to query for.
    
    Returns
    -------
    output : `None | ClientUserBase`
    """
    interaction_event = InteractionEvent(
        authorizer_user_ids = authorizer_user_ids,
    )
    
    output = interaction_event.get_authorizer_user(integration_type)
    vampytest.assert_instance(output, ClientUserBase, nullable = True)
    return output
