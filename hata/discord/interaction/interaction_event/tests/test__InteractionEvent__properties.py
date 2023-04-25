import vampytest

from ....channel import Channel
from ....client import Client
from ....guild import Guild
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


def test__InteractionEvent__guild_0():
    """
    Tests whether ``InteractionEvent.guild`` works as intended.
    
    Case: Has guild.
    """
    guild_id = 202211070050
    interaction_event = InteractionEvent(guild_id = guild_id)
    
    guild = interaction_event.guild
    vampytest.assert_instance(guild, Guild)
    vampytest.assert_eq(guild.id, guild_id)


def test__InteractionEvent__guild_id__1():
    """
    Tests whether ``InteractionEvent.guild_id`` works as intended.
    
    Case: No guild.
    """
    guild_id = 0
    interaction_event = InteractionEvent(guild_id = guild_id)
    
    guild = interaction_event.guild
    vampytest.assert_is(guild, None)


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
