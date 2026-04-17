import vampytest

from ..voice_base import DiscordGatewayVoiceBase

# no tests yet


async def test__DiscordGatewayVoiceBase__set_speaking():
    """
    Tests whether ``DiscordGatewayVoiceBase.set_speaking`` works as intended.
    
    This function is a coroutine.
    """
    speaking = True
    
    gateway = DiscordGatewayVoiceBase()
    
    await gateway.set_speaking(speaking)
