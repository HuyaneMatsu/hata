import vampytest

from ..base import DiscordGatewayBase
from ..constants import LATENCY_DEFAULT


def _assert_fields_set(gateway):
    """
    Tests whether the gateway has ever of its attributes set.
    
    Parameters
    ----------
    gateway : ``DiscordGatewayBase``
        The gateway to check.
    """
    vampytest.assert_instance(gateway, DiscordGatewayBase)


def test__DiscordGatewayBase__new():
    """
    Tests whether ``DiscordGatewayBase.__new__`` works as intended.
    """
    gateway = DiscordGatewayBase()
    _assert_fields_set(gateway)


def test__DiscordGatewayBase__repr():
    """
    Tests whether ``DiscordGatewayBase.__repr__`` works as intended.
    """
    gateway = DiscordGatewayBase()
    
    output = repr(gateway)
    vampytest.assert_instance(output, str)


async def test__DiscordGatewayBase__run():
    """
    Tests whether ``DiscordGatewayBase.run`` works as intended.
    
    This function is a coroutine.
    """
    gateway = DiscordGatewayBase()
    
    with vampytest.assert_raises(NotImplementedError):
        await gateway.run()


def test__DiscordGatewayBase__latency():
    """
    Tests whether ``DiscordGatewayBase.latency`` works as intended.
    """
    gateway = DiscordGatewayBase()
    
    output = gateway.latency
    vampytest.assert_instance(output, float)
    vampytest.assert_eq(output, LATENCY_DEFAULT)


async def test__DiscordGatewayBase__terminate():
    """
    Tests whether ``DiscordGatewayBase.terminate`` works as intended.
    
    This function is a coroutine.
    """
    gateway = DiscordGatewayBase()
    
    await gateway.terminate()


async def test__DiscordGatewayBase__close():
    """
    Tests whether ``DiscordGatewayBase.close`` works as intended.
    
    This function is a coroutine.
    """
    gateway = DiscordGatewayBase()
    
    await gateway.close()


async def test__DiscordGatewayBase__send_as_json():
    """
    Tests whether ``DiscordGatewayBase.send_as_json`` works as intended.
    
    This function is a coroutine.
    """
    gateway = DiscordGatewayBase()
    
    data = {'hello': 'mister'}
    
    await gateway.send_as_json(data)


async def test__DiscordGatewayBase__beat():
    """
    Tests whether ``DiscordGatewayBase.beat`` works as intended.
    
    This function is a coroutine.
    """
    gateway = DiscordGatewayBase()
    
    await gateway.beat()


async def test__DiscordGatewayBase__abort():
    """
    Tests whether ``DiscordGatewayBase.abort`` works as intended.
    
    This function is a coroutine.
    """
    gateway = DiscordGatewayBase()
    
    gateway.abort()

