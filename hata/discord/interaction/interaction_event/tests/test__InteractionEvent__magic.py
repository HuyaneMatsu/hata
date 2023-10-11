import vampytest

from ....application import Entitlement
from ....channel import Channel
from ....guild import create_partial_guild_from_id
from ....localization import Locale
from ....permission import Permission
from ....message import Message
from ....user import User

from ...interaction_metadata import InteractionMetadataApplicationCommand

from ..interaction_event import InteractionEvent
from ..preinstanced import InteractionType


def test__InteractionEvent__repr():
    """
    Tests whether ``InteractionEvent.__repr__`` works as intended.
    """
    application_id = 202211070025
    application_permissions = Permission(123)
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
    

def test__InteractionEvent__eq():
    """
    Tests whether ``InteractionEvent.__hash__`` works as intended.
    """
    application_id = 202211070036
    application_permissions = Permission(123)
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
    interaction_id = 202211070041
    
    keyword_parameters = {
        'application_id': application_id,
        'application_permissions': application_permissions,
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
    
    interaction_event = InteractionEvent.precreate(interaction_id, **keyword_parameters)
    
    vampytest.assert_eq(interaction_event, interaction_event)
    vampytest.assert_ne(interaction_event, object())
    
    # we use identity check, so double precreate it
    
    test_interaction_event = InteractionEvent.precreate(interaction_id, **keyword_parameters)
    vampytest.assert_eq(interaction_event, test_interaction_event)
    
    # assert with partial
    
    test_interaction_event = InteractionEvent(**keyword_parameters)
    vampytest.assert_eq(interaction_event, test_interaction_event)
    
    # Assert with different fields
    
    for field_name, field_value in (
        ('application_id', 202211070042),
        ('application_permissions', Permission(456)),
        ('channel', Channel.precreate(202211070043)),
        ('entitlements', None),
        ('guild', create_partial_guild_from_id(202211070044)),
        ('interaction', InteractionMetadataApplicationCommand(name = 'important')),
         # interaction & interaction_type must match, so we skip this
        # ('interaction_type', InteractionType.application_command),
        ('user_locale', Locale.english_gb),
        ('message', Message.precreate(202211070045, content = 'Rise')),
        ('token', 'Resolution'),
        ('user', User.precreate(202211070046, name = 'princess')),
        ('user_permissions', Permission(756)),
    ):
        test_interaction_event = InteractionEvent(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(interaction_event, test_interaction_event)


def test__InteractionEvent__unpack():
    """
    Tests whether ``InteractionEvent.__iter__`` and ``InteractionEvent.__len__`` works as intended.
    """
    interaction_event = InteractionEvent()
    vampytest.assert_eq(len([*interaction_event]), len(interaction_event))
