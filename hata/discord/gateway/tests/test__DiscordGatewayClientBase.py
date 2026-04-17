import vampytest

from ..client_base import DiscordGatewayClientBase


async def test__DiscordGatewayClientBase__change_voice_state():
    """
    Tests whether ``DiscordGatewayClientBase.change_voice_state`` works as intended.
    
    This function is a coroutine.
    """
    gateway = DiscordGatewayClientBase()
    
    guild_id = 202401060000
    channel_id = 202401060001
    self_mute = True
    self_deaf = True
    
    await gateway.change_voice_state(guild_id, channel_id, self_mute = self_mute, self_deaf = self_deaf)


def test__DiscordGatewayClientBase__get_gateway__guild_id_is_zero():
    """
    Tests whether ``DiscordGatewayClientBase.get_gateway`` works as intended.
    
    Case: `guild_id` is zero.
    """
    gateway = DiscordGatewayClientBase()
    
    guild_id = 0
    
    output = gateway.get_gateway(guild_id)
    
    vampytest.assert_is(output, gateway)


def test__DiscordGatewayClientBase__get_gateway__guild_id_is_not_zero():
    """
    Tests whether ``DiscordGatewayClientBase.get_gateway`` works as intended.
    
    Case: `guild_id` is not zero.
    """
    gateway = DiscordGatewayClientBase()
    
    guild_id = 2
    
    output = gateway.get_gateway(guild_id)
    
    vampytest.assert_is(output, gateway)
