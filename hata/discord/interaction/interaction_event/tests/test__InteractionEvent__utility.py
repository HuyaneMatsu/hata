import vampytest

from ....application import ApplicationIntegrationType, Entitlement, SKU
from ....channel import Channel
from ....component import ComponentType, InteractionComponent
from ....guild import create_partial_guild_from_id
from ....localization import Locale
from ....message import Attachment, Message
from ....permission import Permission
from ....resolved import Resolved
from ....role import Role
from ....user import ClientUserBase, User, create_partial_user_from_id
from ....utils import now_as_id

from ...interaction_metadata import (
    InteractionMetadataApplicationCommand, InteractionMetadataFormSubmit, InteractionMetadataMessageComponent
)
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
    application_command_name = '3L'
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
    interaction_type = InteractionType.application_command
    message = Message.precreate(202211070055, content = 'Rise')
    resolved = Resolved(attachments = [Attachment.precreate(202509100007)])
    token = 'Fall'
    user = User.precreate(202211070056, name = 'masuta spark')
    user_locale = Locale.thai
    user_permissions = Permission(234)
    
    interaction_id = 202211070057
    
    interaction_event = InteractionEvent.precreate(
        interaction_id,
        application_command_name = application_command_name,
        application_id = application_id,
        application_permissions = application_permissions,
        attachment_size_limit = attachment_size_limit,
        authorizer_user_ids = authorizer_user_ids,
        channel = channel,
        entitlements = entitlements,
        guild = guild,
        interaction_type = interaction_type,
        message = message,
        resolved = resolved,
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


def test__InteractionEvent__copy_with__no_fields():
    """
    Tests whether ``InteractionEvent.copy_with`` works as intended.
    
    Case: No fields given.
    """
    application_command_name = '3L'
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
    interaction_type = InteractionType.application_command
    message = Message.precreate(202211070061, content = 'Rise')
    resolved = Resolved(attachments = [Attachment.precreate(202509100008)])
    token = 'Fall'
    user = User.precreate(202211070062, name = 'masuta spark')
    user_locale = Locale.thai
    user_permissions = Permission(234)
    
    interaction_id = 202211070063
    
    interaction_event = InteractionEvent.precreate(
        interaction_id,
        application_command_name = application_command_name,
        application_id = application_id,
        application_permissions = application_permissions,
        attachment_size_limit = attachment_size_limit,
        authorizer_user_ids = authorizer_user_ids,
        channel = channel,
        entitlements = entitlements,
        guild = guild,
        interaction_type = interaction_type,
        message = message,
        resolved = resolved,
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


def test__InteractionEvent__copy_with__all_fields():
    """
    Tests whether ``InteractionEvent.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_application_id = 202211070064
    old_application_command_name = '3L'
    old_application_permissions = Permission(123)
    old_attachment_size_limit = 10 << 20
    old_authorizer_user_ids = {
        ApplicationIntegrationType.user_install: 202407170021,
        ApplicationIntegrationType.guild_install: 202407170022,
    }
    old_channel = Channel.precreate(202211070066)
    old_entitlements = [Entitlement.precreate(202310050028), Entitlement.precreate(202310050029)]
    old_guild = create_partial_guild_from_id(202211070068)
    old_interaction_type = InteractionType.application_command
    old_message = Message.precreate(202211070070, content = 'Rise')
    old_resolved = Resolved(attachments = [Attachment.precreate(202509100009)])
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
    new_component = InteractionComponent(
        ComponentType.button,
        custom_id = 'Renna',
    )
    new_entitlements = [Entitlement.precreate(202310050030), Entitlement.precreate(202310050031)]
    new_guild = create_partial_guild_from_id(202211070069)
    new_interaction_type = InteractionType.message_component
    new_message = Message.precreate(202211070071, content = 'Rise')
    new_resolved = Resolved(attachments = [Attachment.precreate(202509100010)])
    new_token = 'Fall'
    new_user = User.precreate(202211070073, name = 'Marisa')
    new_user_locale = Locale.finnish
    new_user_permissions = Permission(654)
    
    interaction_event = InteractionEvent(
        application_id = old_application_id,
        application_command_name = old_application_command_name,
        application_permissions = old_application_permissions,
        attachment_size_limit = old_attachment_size_limit,
        authorizer_user_ids = old_authorizer_user_ids,
        channel = old_channel,
        entitlements = old_entitlements,
        guild = old_guild,
        interaction_type = old_interaction_type,
        message = old_message,
        resolved = old_resolved,
        token = old_token,
        user = old_user,
        user_locale = old_user_locale,
        user_permissions = old_user_permissions,
    )
    
    copy = interaction_event.copy_with(
        application_id = new_application_id,
        application_permissions = new_application_permissions,
        attachment_size_limit = new_attachment_size_limit,
        authorizer_user_ids = new_authorizer_user_ids,
        channel = new_channel,
        component = new_component,
        entitlements = new_entitlements,
        guild = new_guild,
        interaction_type = new_interaction_type,
        message = new_message,
        resolved = new_resolved,
        token = new_token,
        user = new_user,
        user_locale = new_user_locale,
        user_permissions = new_user_permissions,
    )
    _assert_attributes_set(copy)
    vampytest.assert_not_is(interaction_event, copy)

    vampytest.assert_eq(copy.application_id, new_application_id)
    vampytest.assert_eq(copy.application_permissions, new_application_permissions)
    vampytest.assert_eq(copy.attachment_size_limit, new_attachment_size_limit)
    vampytest.assert_eq(copy.authorizer_user_ids, new_authorizer_user_ids)
    vampytest.assert_is(copy.channel, new_channel)
    vampytest.assert_eq(copy.component, new_component)
    vampytest.assert_eq(copy.entitlements, tuple(new_entitlements))
    vampytest.assert_is(copy.guild, new_guild)
    vampytest.assert_is(copy.message, new_message)
    vampytest.assert_eq(copy.resolved, new_resolved)
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


def _iter_options__resolve_attachment():
    attachment = Attachment.precreate(202211100000)
    
    yield (
        None,
        0,
        None,
    )
    
    yield (
        None,
        attachment.id,
        None,
    )
    
    yield (
        Resolved(),
        0,
        None,
    )
    
    yield (
        Resolved(
            attachments = [attachment],
        ),
        0,
        None,
    )
    
    yield (
        Resolved(
            attachments = [attachment],
        ),
        attachment.id,
        attachment,
    )
    

@vampytest._(vampytest.call_from(_iter_options__resolve_attachment()).returning_last())
def test__InteractionEvent__resolve_attachment(resolved, entity_id):
    """
    Tests whether ``InteractionEvent.resolve_attachment`` works as intended.
    
    Parameters
    ----------
    resolved : ``None | Resolved``
        resolved to use.
    
    entity_id : `int`
        Entity identifier to query for.
    
    Returns
    -------
    output : ``None | Attachment``
    """
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        resolved = resolved,
    )
    
    output = interaction_event.resolve_attachment(entity_id)
    vampytest.assert_instance(output, Attachment, nullable = True)
    return output


def _iter_options__resolve_message():
    message = Message.precreate(202211100001)
    
    yield (
        None,
        0,
        None,
    )
    
    yield (
        None,
        message.id,
        None,
    )
    
    yield (
        Resolved(),
        0,
        None,
    )
    
    yield (
        Resolved(
            messages = [message],
        ),
        0,
        None,
    )
    
    yield (
        Resolved(
            messages = [message],
        ),
        message.id,
        message,
    )


@vampytest._(vampytest.call_from(_iter_options__resolve_message()).returning_last())
def test__InteractionEvent__resolve_message(resolved, entity_id):
    """
    Tests whether ``InteractionEvent.resolve_message`` works as intended.
    
    Parameters
    ----------
    resolved : ``None | Resolved``
        resolved to use.
    
    entity_id : `int`
        Entity identifier to query for.
    
    Returns
    -------
    output : ``None | Message``
    """
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        resolved = resolved,
    )
    
    output = interaction_event.resolve_message(entity_id)
    vampytest.assert_instance(output, Message, nullable = True)
    return output


def _iter_options__resolve_channel():
    channel = Channel.precreate(202211100002)
    
    yield (
        None,
        0,
        None,
    )
    
    yield (
        None,
        channel.id,
        None,
    )
    
    yield (
        Resolved(),
        0,
        None,
    )
    
    yield (
        Resolved(
            channels = [channel],
        ),
        0,
        None,
    )
    
    yield (
        Resolved(
            channels = [channel],
        ),
        channel.id,
        channel,
    )


@vampytest._(vampytest.call_from(_iter_options__resolve_channel()).returning_last())
def test__InteractionEvent__resolve_channel(resolved, entity_id):
    """
    Tests whether ``InteractionEvent.resolve_channel`` works as intended.
    
    Parameters
    ----------
    resolved : ``None | Resolved``
        resolved to use.
    
    entity_id : `int`
        Entity identifier to query for.
    
    Returns
    -------
    output : ``None | Channel``
    """
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        resolved = resolved,
    )
    
    output = interaction_event.resolve_channel(entity_id)
    vampytest.assert_instance(output, Channel, nullable = True)
    return output


def _iter_options__resolve_role():
    role = Role.precreate(202211100004)
    
    yield (
        None,
        0,
        None,
    )
    
    yield (
        None,
        role.id,
        None,
    )
    
    yield (
        Resolved(),
        0,
        None,
    )
    
    yield (
        Resolved(
            roles = [role],
        ),
        0,
        None,
    )
    
    yield (
        Resolved(
            roles = [role],
        ),
        role.id,
        role,
    )


@vampytest._(vampytest.call_from(_iter_options__resolve_role()).returning_last())
def test__InteractionEvent__resolve_role(resolved, entity_id):
    """
    Tests whether ``InteractionEvent.resolve_role`` works as intended.
    
    Parameters
    ----------
    resolved : ``None | Resolved``
        resolved to use.
    
    entity_id : `int`
        Entity identifier to query for.
    
    Returns
    -------
    output : ``None | Role``
    """
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        resolved = resolved,
    )
    
    output = interaction_event.resolve_role(entity_id)
    vampytest.assert_instance(output, Role, nullable = True)
    return output


def _iter_options__resolve_user():
    user = User.precreate(202211100005)
    
    yield (
        None,
        0,
        None,
    )
    
    yield (
        None,
        user.id,
        None,
    )
    
    yield (
        Resolved(),
        0,
        None,
    )
    
    yield (
        Resolved(
            users = [user],
        ),
        0,
        None,
    )
    
    yield (
        Resolved(
            users = [user],
        ),
        user.id,
        user,
    )


@vampytest._(vampytest.call_from(_iter_options__resolve_user()).returning_last())
def test__InteractionEvent__resolve_user(resolved, entity_id):
    """
    Tests whether ``InteractionEvent.resolve_user`` works as intended.
    
    Parameters
    ----------
    resolved : ``None | Resolved``
        resolved to use.
    
    entity_id : `int`
        Entity identifier to query for.
    
    Returns
    -------
    output : ``None | User``
    """
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        resolved = resolved,
    )
    
    output = interaction_event.resolve_user(entity_id)
    vampytest.assert_instance(output, User, nullable = True)
    return output


def _iter_options__resolve_mentionable():
    role = Role.precreate(202211100007)
    user = User.precreate(202211100006)
    
    yield (
        None,
        0,
        None,
    )
    
    yield (
        None,
        role.id,
        None,
    )
    
    yield (
        None,
        user.id,
        None,
    )
    
    yield (
        Resolved(),
        0,
        None,
    )
    
    yield (
        Resolved(
            users = [user],
            roles = [role],
        ),
        0,
        None,
    )
    
    yield (
        Resolved(
            roles = [role],
            users = [user],
        ),
        role.id,
        role,
    )
    
    yield (
        Resolved(
            roles = [role],
            users = [user],
        ),
        user.id,
        user,
    )


@vampytest._(vampytest.call_from(_iter_options__resolve_mentionable()).returning_last())
def test__InteractionEvent__resolve_mentionable(resolved, entity_id):
    """
    Tests whether ``InteractionEvent.resolve_mentionable`` works as intended.
    
    Parameters
    ----------
    resolved : ``None | Resolved``
        resolved to use.
    
    entity_id : `int`
        Entity identifier to query for.
    
    Returns
    -------
    output : ``None | Role | User``
    """
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        resolved = resolved,
    )
    
    output = interaction_event.resolve_mentionable(entity_id)
    vampytest.assert_instance(output, Role, User, nullable = True)
    return output


def _iter_options__resolve_entity():
    attachment = Attachment.precreate(202211100008)
    channel = Channel.precreate(202211100009)
    message = Message.precreate(202211100010)
    role = Role.precreate(202211100011)
    user = User.precreate(202211100012)
    
    yield (
        None,
        0,
        None,
    )
    
    yield (
        None,
        attachment.id,
        None,
    )
    
    yield (
        None,
        channel.id,
        None,
    )
    
    yield (
        None,
        message.id,
        None,
    )
    
    yield (
        None,
        role.id,
        None,
    )
    
    yield (
        None,
        user.id,
        None,
    )
    
    yield (
        Resolved(),
        0,
        None,
    )
    
    yield (
        Resolved(
            attachments = [attachment],
            channels = [channel],
            messages = [message],
            roles = [role],
            users = [user],
        ),
        0,
        None,
    )
    
    yield (
        Resolved(
            attachments = [attachment],
            channels = [channel],
            messages = [message],
            roles = [role],
            users = [user],
        ),
        attachment.id,
        attachment,
    )
    
    yield (
        Resolved(
            attachments = [attachment],
            channels = [channel],
            messages = [message],
            roles = [role],
            users = [user],
        ),
        channel.id,
        channel,
    )
    
    yield (
        Resolved(
            attachments = [attachment],
            channels = [channel],
            messages = [message],
            roles = [role],
            users = [user],
        ),
        message.id,
        message,
    )
    
    yield (
        Resolved(
            attachments = [attachment],
            channels = [channel],
            messages = [message],
            roles = [role],
            users = [user],
        ),
        role.id,
        role,
    )
    
    yield (
        Resolved(
            attachments = [attachment],
            channels = [channel],
            messages = [message],
            roles = [role],
            users = [user],
        ),
        user.id,
        user,
    )


@vampytest._(vampytest.call_from(_iter_options__resolve_entity()).returning_last())
def test__InteractionEvent__resolve_entity(resolved, entity_id):
    """
    Tests whether ``InteractionEvent.resolve_entity`` works as intended.
    
    Parameters
    ----------
    resolved : ``None | Resolved``
        resolved to use.
    
    entity_id : `int`
        Entity identifier to query for.
    
    Returns
    -------
    output : ``None | Attachment | Channel | Message | Role | User``
    """
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        resolved = resolved,
    )
    
    output = interaction_event.resolve_entity(entity_id)
    vampytest.assert_instance(output, Attachment, Channel, Message, Role, User, nullable = True)
    return output


def _iter_options__target():
    extra_target_id = 202211080017
    
    attachment = Attachment.precreate(202211080012)
    channel = Channel.precreate(202211080013)
    message = Message.precreate(202211080014)
    role = Role.precreate(202211080015)
    user = User.precreate(202211080016)
    
    yield (
        None,
        0,
        None,
    )
        
    yield(
        None,
        extra_target_id,
        None,
    )
    
    yield (
        None,
        0,
        None,
    )
    
    yield (
        Resolved(
            attachments = [attachment],
            channels = [channel],
            messages = [message],
            roles = [role],
            users = [user],
        ),
        extra_target_id,
        None,
    )
    
    yield (
        Resolved(
            attachments = [attachment],
            channels = [channel],
            messages = [message],
            roles = [role],
            users = [user],
        ),
        attachment.id,
        attachment,
    )
    
    yield (
        Resolved(
            attachments = [attachment],
            channels = [channel],
            messages = [message],
            roles = [role],
            users = [user],
        ),
        channel.id,
        channel,
    )
    
    yield (
        Resolved(
            attachments = [attachment],
            channels = [channel],
            messages = [message],
            roles = [role],
            users = [user],
        ),
        message.id,
        message,
    )
    
    yield (
        Resolved(
            attachments = [attachment],
            channels = [channel],
            messages = [message],
            roles = [role],
            users = [user],
        ),
        role.id,
        role,
    )
    
    yield (
        Resolved(
            attachments = [attachment],
            channels = [channel],
            messages = [message],
            roles = [role],
            users = [user],
        ),
        user.id,
        user,
    )


@vampytest._(vampytest.call_from(_iter_options__target()).returning_last())
def test__InteractionEvent__target(resolved, target_id):
    """
    Tests whether ``InteractionEvent.target`` field proxies work as intended.
    
    Parameters
    ----------
    resolved : ``None | Resolved``
        resolved to use.
    
    target_id : `int`
        Target identifier.
    
    Returns
    -------
    output : ``None | Attachment | Channel | Message | Role | User``
    """
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command,
        resolved = resolved,
        target_id = target_id,
    )
    
    output = interaction_event.target
    vampytest.assert_instance(output, Attachment, Channel, Message, Role, User, nullable = True)
    return output



def _iter_options__iter_entities():
    extra_target_id = 202509100013
    
    role = Role.precreate(202211100012)
    user = User.precreate(202211100013)
    
    
    yield (
        ComponentType.mentionable_select,
        Resolved(
            roles = [role],
            users = [user]
        ),
        None,
        [],
    )
    
    yield (
        ComponentType.mentionable_select,
        Resolved(
            roles = [role],
            users = [user]
        ),
        [
            str(role.id),
        ],
        [
            role,
        ],
    )
    
    yield (
        ComponentType.mentionable_select,
        Resolved(
            roles = [role],
            users = [user]
        ),
        [
            'owo',
        ],
        [],
    )
    
    yield (
        ComponentType.mentionable_select,
        Resolved(
            roles = [role],
            users = [user]
        ),
        [
            str(extra_target_id),
        ],
        [],
    )
    
    yield (
        ComponentType.mentionable_select,
        Resolved(
            roles = [role],
            users = [user]
        ),
        [
            str(role.id),
            str(user.id),
        ],
        [
            role,
            user,
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_entities()).returning_last())
def test__InteractionEvent__iter_entities(component_type, resolved, values):
    """
    Tests whether ``InteractionEvent.iter_entities`` works as intended.
    
    Parameters
    ----------
    component_type : ``ComponentType``
        The represented component type.
    
    resolved : ``None | Resolved``
        Resolved entities.
    
    values : `None | list<str>`
        Values to create the interaction with.
    
    Returns
    -------
    output : `list<object>`
    """
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.message_component,
        component = InteractionComponent(
            component_type,
            custom_id = 'koishi',
            values = values,
        ),
        resolved = resolved,
    )
    
    return [*interaction_event.iter_entities()]


@vampytest._(vampytest.call_from(_iter_options__iter_entities()).returning_last())
def test__InteractionEvent__entities(component_type, resolved, values):
    """
    Tests whether ``InteractionEvent.entities`` works as intended.
    
    Parameters
    ----------
    component_type : ``ComponentType``
        The represented component type.
    
    resolved : ``None | Resolved``
        Resolved entities.
    
    values : `None | list<str>`
        Values to create the interaction with.
    
    Returns
    -------
    output : `list<object>`
    """
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.message_component,
        component = InteractionComponent(
            component_type,
            custom_id = 'koishi',
            values = values,
        ),
        resolved = resolved,
    )
    
    return interaction_event.entities


def _iter_options__get_custom_id_value_relation():
    interaction_component_0 = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'negative',
        value = 'kaenbyou',
    )
    interaction_component_1 = InteractionComponent(
        ComponentType.string_select,
        custom_id = 'number',
        values = ['kaenbyou', 'rin'],
    )
    interaction_component_2 = InteractionComponent(
        ComponentType.none,
    )
    interaction_component_3 = InteractionComponent(
        ComponentType.row,
        components = [
            interaction_component_0,
            interaction_component_1,
        ],
    )
    
    yield (
        [
            interaction_component_0,
        ],
        {
            'negative' : (ComponentType.text_input, 'kaenbyou'),
        },
    )
    
    yield (
        [
            interaction_component_1,
        ],
        {
            'number' : (ComponentType.string_select, ('kaenbyou', 'rin')),
        },
    )
    
    yield (
        [
            interaction_component_2,
        ],
        {},
    )
    
    yield (
        [
            interaction_component_3,
        ],
        {
            'negative' : (ComponentType.text_input, 'kaenbyou'),
            'number' : (ComponentType.string_select, ('kaenbyou', 'rin')),
        },
    )


@vampytest._(vampytest.call_from(_iter_options__get_custom_id_value_relation()).returning_last())
def test__InteractionEvent__get_custom_id_value_relation(components):
    """
    Tests whether ``InteractionEvent.get_custom_id_value_relation`` works as intended.
    
    Parameters
    ----------
    components : ``None | list<InteractionComponent>``
        Components to create instance with.
    
    Returns
    -------
    output : `dict<str, (ComponentType, None | str | tuple<str>)>`
    """
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.form_submit,
        components = components,
    )
    
    return interaction_event.get_custom_id_value_relation()


def _iter_options__get_value_for():
    interaction_component = InteractionComponent(
        ComponentType.row,
        components = [
            InteractionComponent(
                ComponentType.text_input,
                custom_id = 'Ran',
                value = None,
            ),
            InteractionComponent(
                ComponentType.text_input,
                custom_id = 'Chen',
                value = 'Yakumo',
            ),
        ],  
    )
    
    yield (
        [
            interaction_component,
        ],
        'Ran',
        (
            ComponentType.text_input,
            None,
        ),
    )
    
    yield (
        [
            interaction_component,
        ],
        'Chen',
        (
            ComponentType.text_input,
            'Yakumo',
        ),
    )
    
    yield (
        [
            interaction_component,
        ],
        'Yukari',
        (
            ComponentType.none,
            None,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__get_value_for()).returning_last())
def test__InteractionEvent__get_value_for(components, custom_id_to_match):
    """
    Tests whether ``InteractionEvent.get_value_for`` works as intended.
    
    Parameters
    ----------
    components : ``None | list<InteractionComponent>``
        Components to create instance with.
    
    custom_id_to_match : `str`
        A respective components `custom_id` to match.
    
    Returns
    -------
    output : `(ComponentType, None | str | tuple<str>)`
    """
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.form_submit,
        components = components,
    )
    
    return interaction_event.get_value_for(custom_id_to_match)


def _iter_options__get_match_and_value():
    interaction_component = InteractionComponent(
        ComponentType.row,
        components = [
            InteractionComponent(
                ComponentType.text_input,
                custom_id = 'Ran',
                value = None,
            ),
            InteractionComponent(
                ComponentType.text_input,
                custom_id = 'Chen',
                value = 'Yakumo',
            ),
        ],  
    )
    
    yield (
        [
            interaction_component,
        ],
        (lambda custom_id: 'custom_id' if custom_id == 'Ran' else None),
        (
            'custom_id',
            ComponentType.text_input,
            None,
        ),
    )
    
    yield (
        [
            interaction_component,
        ],
        (lambda custom_id: 'custom_id' if custom_id == 'Chen' else None),
        (
            'custom_id',
            ComponentType.text_input,
            'Yakumo',
        ),
    )
    
    yield (
        [
            interaction_component,
        ],
        (lambda custom_id: 'custom_id' if custom_id == 'Yukari' else None),
        (
            None,
            ComponentType.none,
            None,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__get_match_and_value()).returning_last())
def test__InteractionEvent__get_match_and_value(components, matcher):
    """
    Tests whether ``InteractionEvent.get_match_and_value`` works as intended.
    
    Parameters
    ----------
    components : ``None | list<InteractionComponent>``
        Components to create instance with.
    
    matcher : `callable`
        Matcher to call on a `custom_id`.
    
    Returns
    -------
    output : `(None | object, ComponentType, None | str | tuple<str>)`
    """
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.form_submit,
        components = components,
    )
    
    return interaction_event.get_match_and_value(matcher)


def _iter_options__iter_matches_and_values():
    interaction_component = InteractionComponent(
        ComponentType.row,
        components = [
            InteractionComponent(
                ComponentType.text_input,
                custom_id = 'Ran',
                value = None,
            ),
            InteractionComponent(
                ComponentType.text_input,
                custom_id = 'Chen',
                value = 'Yakumo',
            ),
        ],  
    )
    
    yield (
        [
            interaction_component,
        ],
        (lambda custom_id: 'custom_id' if 'e' in custom_id else None),
        [
            (
                'custom_id',
                ComponentType.text_input,
                'Yakumo',
            ),
        ],
    )
    
    yield (
        [
            interaction_component,
        ],
        (lambda custom_id: 'Ran' if custom_id == 'Ran' else None),
        [
            (
                'Ran',
                ComponentType.text_input,
                None,
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_matches_and_values()).returning_last())
def test__InteractionEvent__iter_matches_and_values(components, matcher):
    """
    Tests whether ``InteractionEvent.iter_matches_and_values`` works as intended.
    
    Parameters
    ----------
    components : ``None | list<InteractionComponent>``
        Components to create instance with.
    
    matcher : `callable`
        Matcher to call on a `custom_id`.
    
    Returns
    -------
    output : `(None | object, ComponentType, None | str | tuple<str>)`
    """
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.form_submit,
        components = components,
    )
    
    return [*interaction_event.iter_matches_and_values(matcher)]
