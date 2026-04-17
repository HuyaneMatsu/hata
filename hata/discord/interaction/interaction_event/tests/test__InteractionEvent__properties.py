import vampytest

from ....channel import Channel
from ....client import Client
from ....guild import Guild, create_partial_guild_from_id
from ....localization import Locale
from ....user import User

from ..interaction_event import InteractionEvent


def test__InteractionEvent__channel_id():
    """
    Tests whether ``InteractionEvent.channel_id`` works as intended.
    """
    channel_id = 202211070049
    channel = Channel.precreate(channel_id)
    
    interaction_event = InteractionEvent(channel = channel)
    
    output = interaction_event.channel_id
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, channel_id)


def test__InteractionEvent__user_id():
    """
    Tests whether ``InteractionEvent.user_id`` works as intended.
    """
    user_id = 202304250000
    user = User.precreate(user_id)
    
    interaction_event = InteractionEvent(user = user)
    
    output = interaction_event.user_id
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, user_id)


def _iter_options__guild_id():
    guild_id = 202211070050
    
    yield InteractionEvent(), 0
    yield InteractionEvent(guild = create_partial_guild_from_id(guild_id)), guild_id
    

@vampytest._(vampytest.call_from(_iter_options__guild_id()).returning_last())
def test__InteractionEvent__guild_id(interaction_event):
    """
    Tests whether ``InteractionEvent.guild_id`` works as intended.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        Interaction event to validate with.
    
    Returns
    -------
    output : `int`
    """
    output = interaction_event.guild_id
    vampytest.assert_instance(output, int)
    return output


def _iter_options__guild_locale():
    guild_id = 202310100007
    guild_locale = Locale.dutch
    
    yield InteractionEvent(), Locale.english_us
    yield InteractionEvent(guild = Guild.precreate(guild_id, locale = guild_locale)), guild_locale
    

@vampytest._(vampytest.call_from(_iter_options__guild_locale()).returning_last())
def test__InteractionEvent__guild_locale(interaction_event):
    """
    Tests whether ``InteractionEvent.guild_locale`` works as intended.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        Interaction event to validate with.
    
    Returns
    -------
    output : `int`
    """
    output = interaction_event.guild_locale
    vampytest.assert_instance(output, Locale)
    return output


def test__InteractionEvent__client_0():
    """
    Tests whether ``InteractionEvent.client`` works as intended.
    
    Case: has client.
    """
    application_id = 202211070051
    
    client = Client(
        'token_202211070000',
        application_id = application_id,
    )
    try:
        interaction_event = InteractionEvent(application_id = application_id)
    
        interaction_client = interaction_event.client
        vampytest.assert_instance(interaction_client, Client)
        vampytest.assert_is(interaction_client, client)
    finally:
        client._delete()
        client = None


def test__InteractionEvent__client_1():
    """
    Tests whether ``InteractionEvent.client`` works as intended.
    
    Case: no client.
    """
    interaction_event = InteractionEvent()
    
    with vampytest.assert_raises(RuntimeError):
        interaction_event.client


def test__InteractionEvent__voice_client__0():
    """
    Tests whether ``InteractionEvent.voice_client`` works as intended.
    
    Case: no voice_client.
    """
    interaction_event = InteractionEvent()

    voice_client = interaction_event.voice_client
    vampytest.assert_is(voice_client, None)
