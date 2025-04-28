import vampytest

from ....application import ApplicationIntegrationType, Entitlement
from ....channel import Channel
from ....guild import create_partial_guild_from_id
from ....localization import Locale
from ....permission import Permission
from ....message import Message
from ....user import User

from ...interaction_metadata import InteractionMetadataApplicationCommand, InteractionMetadataBase

from ..interaction_event import InteractionEvent
from ..preinstanced import InteractionType


def test__InteractionEvent__repr():
    """
    Tests whether ``InteractionEvent.__repr__`` works as intended.
    """
    application_id = 202211070025
    application_permissions = Permission(123)
    attachment_size_limit = 10 << 20
    authorizer_user_ids = {
        ApplicationIntegrationType.user_install: 202407170008,
        ApplicationIntegrationType.guild_install: 202407170009,
    }
    channel = Channel.precreate(202211070026)
    entitlements = [Entitlement.precreate(202310050018), Entitlement.precreate(202310050019)]
    guild = create_partial_guild_from_id(202211070027)
    interaction = InteractionMetadataApplicationCommand(name = '3L')
    interaction_type = InteractionType.application_command
    message = Message.precreate(202211070028, content = 'Rise')
    token = 'Fall'
    user = User.precreate(202211070029, name = 'masuta spark')
    user_locale = Locale.thai
    user_permissions = Permission(234)
    interaction_id = 202211070030
    
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
        user_locale = user_locale,
        message = message,
        token = token,
        user = user,
        user_permissions = user_permissions
    )
    
    vampytest.assert_instance(repr(interaction_event), str)
    

def test__InteractionEvent__hash():
    """
    Tests whether ``InteractionEvent.__hash__`` works as intended.
    """
    application_id = 202211070031
    application_permissions = Permission(123)
    attachment_size_limit = 10 << 20
    authorizer_user_ids = {
        ApplicationIntegrationType.user_install: 202407170010,
        ApplicationIntegrationType.guild_install: 202407170011,
    }
    channel = Channel.precreate(202211070032)
    entitlements = [Entitlement.precreate(202310050021), Entitlement.precreate(202310050022)]
    guild = create_partial_guild_from_id(202211070033)
    interaction = InteractionMetadataApplicationCommand(name = '3L')
    interaction_type = InteractionType.application_command
    message = Message.precreate(202211070034, content = 'Rise')
    token = 'Fall'
    user = User.precreate(202211070009, name = 'masuta spark')
    user_locale = Locale.thai
    user_permissions = Permission(234)
    interaction_id = 202211070035
    
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
    
    vampytest.assert_instance(hash(interaction_event), int)


def _iter_options__eq():
    application_id = 202211070036
    application_permissions = Permission(123)
    attachment_size_limit = 10 << 20
    authorizer_user_ids = {
        ApplicationIntegrationType.user_install: 202407170015,
        ApplicationIntegrationType.guild_install: 202407170016,
    }
    channel = Channel.precreate(202211070037)
    entitlements = [Entitlement.precreate(202310050023), Entitlement.precreate(202310050024)]
    guild = create_partial_guild_from_id(202211070038)
    interaction = InteractionMetadataApplicationCommand(name = '3L')
    interaction_type = InteractionType.application_command
    message = Message.precreate(202211070039, content = 'Rise')
    token = 'Fall'
    user = User.precreate(202211070040, name = 'masuta spark')
    user_locale = Locale.thai
    user_permissions = Permission(234)
    
    keyword_parameters = {
        'application_id': application_id,
        'application_permissions': application_permissions,
        'attachment_size_limit': attachment_size_limit,
        'authorizer_user_ids': authorizer_user_ids,
        'channel': channel,
        'entitlements': entitlements,
        'guild': guild,
        'interaction': interaction,
        'interaction_type': interaction_type,
        'user_locale': user_locale,
        'message': message,
        'token': token,
        'user': user,
        'user_permissions': user_permissions,
    }
    
    yield (
        {},
        {},
        True,
    )
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'application_id': 202211070042,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'application_permissions': Permission(456),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'application_permissions': 11 << 20,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'authorizer_user_ids': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'channel': Channel.precreate(202211070043),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'entitlements': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'guild': create_partial_guild_from_id(202211070044),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'interaction': InteractionMetadataApplicationCommand(name = 'important'),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'interaction_type': InteractionType.ping,
            'interaction': InteractionMetadataBase(),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'user_locale': Locale.english_gb,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'message': Message.precreate(202211070045, content = 'Rise'),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'token': 'Resolution',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'user': User.precreate(202211070046, name = 'princess'),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'user_permissions': Permission(756),
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__InteractionEvent__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``InteractionEvent.__hash__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    interaction_event_0 = InteractionEvent(**keyword_parameters_0)
    interaction_event_1 = InteractionEvent(**keyword_parameters_1)
    
    output = interaction_event_0 == interaction_event_1
    vampytest.assert_instance(output, bool)
    return output


def test__InteractionEvent__eq__precreate():
    """
    Tests whether ``InteractionEvent.__eq__`` works as intended.
    
    Case: precreate.
    """
    interaction_id_0 = 202407170012
    interaction_id_1 = 202407170013
    application_id = 202407170014
    
    interaction_event_0 = InteractionEvent.precreate(interaction_id_0, application_id = application_id)
    interaction_event_1 = InteractionEvent.precreate(interaction_id_1, application_id = application_id)
    interaction_event_2 = InteractionEvent(application_id = application_id)
    
    vampytest.assert_eq(interaction_event_0, interaction_event_0)
    vampytest.assert_ne(interaction_event_0, interaction_event_1)
    vampytest.assert_eq(interaction_event_2, interaction_event_0)
    vampytest.assert_eq(interaction_event_2, interaction_event_1)


def test__InteractionEvent__unpack():
    """
    Tests whether ``InteractionEvent.__iter__`` and ``InteractionEvent.__len__`` works as intended.
    """
    interaction_event = InteractionEvent()
    vampytest.assert_eq(len([*interaction_event]), len(interaction_event))
