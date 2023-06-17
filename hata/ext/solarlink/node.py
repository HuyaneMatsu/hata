__all__ = ('SolarNode', )

from scarletio import (
    Future, RichAttributeErrorBaseType, Task, from_json, repeat_timeout, sleep, to_json, write_exception_async
)
from scarletio.web_common import ConnectionClosed, InvalidHandshake, WebSocketProtocolError

from ...discord.channel import VoiceRegion
from ...discord.core import KOKORO

from .constants import (
    HEADER_AUTHORIZATION, HEADER_CLIENT_NAME, HEADER_RESUME_KEY, HEADER_SHARD_COUNT, HEADER_USER_ID,
    LAVALINK_KEY_EVENT_TYPE, LAVALINK_KEY_GATEWAY_OPERATION_EVENT, LAVALINK_KEY_GATEWAY_OPERATION_PLAYER_UPDATE,
    LAVALINK_KEY_GATEWAY_OPERATION_STATS, LAVALINK_KEY_GUILD_ID, LAVALINK_KEY_NODE_OPERATION,
    LAVALINK_KEY_NODE_OPERATION_SET_RESUME_KEY, LAVALINK_KEY_NODE_RESUME_KEY, LAVALINK_KEY_PLAYER_STATE
)
from .exceptions import SolarAuthenticationError
from .parsers import PARSERS
from .stats import Stats


EXTENSION_USER_AGENT = 'hata.ext.solarlink'
DEFAULT_PENALTY = 9e30

class SolarNode(RichAttributeErrorBaseType):
    """
    Represents a Node connection with Lavalink.
    
    Attributes
    ----------
    _host : `str`
        Host of a lavalink node to connect to.
    _password : `str`
        The password used for authentication.
    _port : `int`
        Port of a lavalink node to connect to.
    _resume_key : `None`, `str`
        A resume key to resume websocket connection with lavalink.
    client : ``Client``
        The parent client of the node.
    players : `set` of ``SolarPlayerBase``
        The players using this node.
    reconnect_attempts : `int`
        How much times the gateway should try to reconnect before erroring out.
        
        Defaults to `3`. If defined as a negative number, the node will try to reconnect infinitely.
    
    region : `None`, ``VoiceRegion``
        The respective voice region of the node's players.
    stats : `None`, ``Stats``
        The statistics of the node.
    websocket : `None`, ``WebSocketClient``
        The connected websocket.
    """
    __slots__ = (
        '_host', '_password', '_port', '_resume_key', 'client', 'players', 'reconnect_attempts', 'region', 'stats',
        'websocket'
    )
    
    def __new__(cls, client, host, port, password, region, resume_key, reconnect_attempts):
        """
        Creates a new node connection with the given parameters.
        
        Parameters
        ----------
        client : ``Client``
            The parent client.
        host : `str`
            The host of the lavalink node to connect to.
        port : `int`
            The port of the lavalink node to connect to.
        password : `str`
            The password used for authentication.
        region : `None`, ``VoiceRegion``
            The respective voice region of the node's players.
        resume_key : `None`, `str`
            A resume key to resume websocket connection with lavalink.
        reconnect_attempts : `int`
            How much times the gateway should try to reconnect before erroring out.
        
        Raises
        ------
        TypeError
            - If `host` is not `str`.
            - If `port` is not `int`.
            - If `password is not `str`.
            - If `region` is neither `None`, nor ``VoiceRegion``.
            - If `resume_key` is neither `None`, nor `str`.
            - If `reconnect_attempts` is not `int`.
        """
        if type(host) is str:
            pass
        elif isinstance(host, str):
            host = str(host)
        else:
            raise TypeError(
                f'`host` can be `str`, got {host.__class__.__name__}; {host!r}.'
            )
        
        if type(port) is int:
            pass
        elif isinstance(port, int):
            port = int(port)
        else:
            raise TypeError(
                f'`port` can be `int`, got {port.__class__.__name__}; {port!r}.'
            )
        
        if type(password) is str:
            pass
        elif isinstance(password, str):
            password = str(password)
        else:
            raise TypeError(
                f'`password` can be `str`, got {password.__class__.__name__}; {password!r}.'
            )
        
        if (region is not None) and (not isinstance(region, VoiceRegion)):
            raise TypeError(
                f'`region` can be `None`, `{VoiceRegion.__name__}`, got '
                f'{region.__class__.__name__}; {region!r}.'
            )
        
        if (resume_key is None) or (type(resume_key) is str):
            pass
        elif isinstance(resume_key, str):
            resume_key = str(resume_key)
        else:
            raise TypeError(
                f'`resume_key` can be `None`, `str`, got '
                f'{resume_key.__class__.__name__}; {resume_key!r}.'
            )
        
        if type(reconnect_attempts) is int:
            pass
        elif isinstance(reconnect_attempts, int):
            reconnect_attempts = int(reconnect_attempts)
        else:
            raise TypeError(
                f'`reconnect_attempts` can be `int`, got '
                f'{reconnect_attempts.__class__.__name__}; {reconnect_attempts!r}.'
            )
        
        self = object.__new__(cls)
        
        self.client = client
        self._host = host
        self._port = port
        self._password = password
        self.region = region
        self.stats = None
        self.players = set()
        self.websocket = None
        self._resume_key = resume_key
        self.reconnect_attempts = reconnect_attempts
        return self
    
    
    @property
    def available(self):
        """
        Returns whether the node is available for requests.
        
        Returns
        -------
        available : `bool`
        """
        websocket = self.websocket
        if websocket is None:
            available = False
        else:
            available = websocket.open
        
        return available
    
    
    @property
    def penalty(self):
        """
        Returns the load-balancing penalty for this node.
        
        Returns
        -------
        penalty : `float`
        """
        if self.available:
            stats = self.stats
            if (stats is None):
                penalty = DEFAULT_PENALTY
            else:
                penalty = stats.total_penalty
        else:
            penalty = DEFAULT_PENALTY
        
        return penalty
    
    
    async def _send(self, data):
        """
        Sends the passed data to the node via the websocket connection.
        
        Parameters
        ----------
        data : `dict`
            The dict to send to Lavalink.
        """
        data = to_json(data)
        
        websocket = self.websocket
        if (websocket is not None):
            await websocket.send(data)
    
    
    async def _connect(self):
        """
        Connects to a lavalink node.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
        OSError
        ValueError
        ConnectionClosed
        InvalidHandshake
        WebSocketProtocolError
        """
        client = self.client
        
        shard_count = client.shard_count
        if not shard_count:
            shard_count = 1
        
        headers = {
            HEADER_AUTHORIZATION: self._password,
            HEADER_USER_ID : str(client.id),
            HEADER_CLIENT_NAME: EXTENSION_USER_AGENT,
            HEADER_SHARD_COUNT: str(shard_count),
        }
        
        resume_key = self._resume_key
        if (resume_key is not None):
            headers[HEADER_RESUME_KEY] = resume_key
        
        while True:
            websocket = self.websocket
            if (websocket is not None) and (not websocket.closed):
                await websocket.close(4000)
                self.websocket = None
            
            self.websocket = await self.client.http.connect_websocket(
                f'ws://{self._host}:{self._port}',
                headers = headers,
            )
            
            try:
                await self.websocket.ensure_open()
            except ConnectionClosed:
                continue
            
            break
        
        if (resume_key is not None):
            # Resume timeout defaults to `60` seconds, we will keep it.
            await self._send({
                LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_SET_RESUME_KEY,
                LAVALINK_KEY_NODE_RESUME_KEY: resume_key,
            })
        
        await self.client.solarlink._node_connected(self)
    
    
    async def run(self, waiter = None):
        """
        Keeps the node's gateway open.
        
        This method is a coroutine.
        """
        client = self.client
        reconnect_attempts = self.reconnect_attempts
        
        try:
            while True:
                try:
                    task = Task(KOKORO, self._connect())
                    task.apply_timeout(30.0)
                    await task
                    
                    if (waiter is not None):
                        waiter.set_result_if_pending(True)
                        waiter = None
                    
                    while True:
                        try:
                            with repeat_timeout(60.0) as loop:
                                for _ in loop:
                                    should_reconnect = await self._poll_event()
                                    if should_reconnect:
                                        break
                        except TimeoutError:
                            # timeout, no internet probably; try to reconnect
                            
                            # Make sure we are still online
                            if not client.running:
                                return
                            
                            # Try to reconnect later.
                            await sleep(5.0, KOKORO)
                            break
                        
                        if not client.running:
                            return
                        
                        reconnect_attempts = self.reconnect_attempts
                        task = Task(KOKORO, self._connect())
                        task.apply_timeout(30.0)
                        await task
                
                
                except (OSError, TimeoutError, ConnectionError, ConnectionClosed, WebSocketProtocolError,
                        InvalidHandshake, ValueError) as err:
                    
                    if not client.running:
                        return
                    
                    reconnect_attempts -= 1
                    
                    if isinstance(err, InvalidHandshake):
                        if err.response.status in (401, 403):
                            raise SolarAuthenticationError(self, err.response) from None
                        
                        sleep_amount = 0.0
                    
                    elif isinstance(err, ConnectionClosed):
                        sleep_amount = 0.0
                    
                    elif isinstance(err, TimeoutError):
                        sleep_amount = 0.0
                    
                    elif isinstance(err, ConnectionError): # no internet
                        sleep_amount = 5.0
                    
                    else:
                        sleep_amount = 1.0
                    
                    if not reconnect_attempts:
                        await write_exception_async(
                            err,
                            [
                                'Failed to connect to lavalink node ',
                                repr(self),
                                '.run:\n',
                            ],
                            loop = KOKORO,
                        )
                        
                        if (waiter is not None):
                            waiter.set_result_if_pending(False)
                            waiter = None
                        
                        return
                    
                    if sleep_amount:
                        await sleep(sleep_amount, KOKORO)
                    
                    continue
                
        
        except GeneratorExit:
            if (waiter is not None):
                waiter.set_result_if_pending(False)
                waiter = None
            
            raise
        
        except BaseException as err:
            if (waiter is not None):
                waiter.set_exception_if_pending(err)
                waiter = None
            
            raise
        finally:
            await client.solarlink._node_disconnected(self)
            
            if (waiter is not None):
                waiter.set_result_if_pending(False)
                waiter = None
    
    
    async def _poll_event(self):
        """
        Polls an event from the gateway and tries to handle it.
        
        This method is a coroutine.
        
        Returns
        -------
        should_reconnect : `bool`
        
        Raises
        ------
        ConnectionClosed
            If the websocket connection closed.
        """
        websocket = self.websocket
        if websocket is None:
            return True
        
        try:
            message = await websocket.receive()
        except ConnectionClosed as err:
            raise err
        
        return (await self._received_message(message))
    
    
    async def _received_message(self, message):
        """
        Processes a message received from a lavalink node.
        
        Parameters
        ----------
        message : `str`
            the received message.
        
        Returns
        -------
        should_reconnect : `bool`
        """
        message = from_json(message)
        
        operation = message[LAVALINK_KEY_NODE_OPERATION]
        
        if operation == LAVALINK_KEY_GATEWAY_OPERATION_STATS:
            self.stats = Stats(message)
            return False
        
        if operation == LAVALINK_KEY_GATEWAY_OPERATION_PLAYER_UPDATE:
            guild_id = int(message[LAVALINK_KEY_GUILD_ID])
            
            try:
                player = self.client.solarlink.players[guild_id]
            except KeyError:
                return False
            
            player._update_state(message[LAVALINK_KEY_PLAYER_STATE])
            return False
        
        elif operation == LAVALINK_KEY_GATEWAY_OPERATION_EVENT:
            event = message[LAVALINK_KEY_EVENT_TYPE]
            client = self.client
            
            try:
                parser = PARSERS[event]
            except KeyError:
                Task(
                    KOKORO,
                    client.events.error(
                        client,
                        f'{self.__class__.__name__}._received_message',
                        f'Unknown dispatch event {event}\nData: {message!r}',
                    ),
                )
                return False
            
            try:
                parser(self.client, message)
            except BaseException as err:
                Task(KOKORO, client.events.error(client, event, err))
            
            return False
        
        client = self.client
        Task(
            KOKORO,
            client.events.error(
                client,
                f'{self.__class__.__name__}._received_message',
                f'Unknown operation {operation}\nData: {message!r}',
            ),
        )
        return False
    
    
    async def start(self):
        """
        Starts the lavalink node.
        
        This method is a coroutine.
        
        Raises
        ------
        BaseException
            Any exception raised when trying to connect.
        """
        waiter = Future(KOKORO)
        Task(KOKORO, self.run(waiter = waiter))
        return await waiter
    
    
    async def close(self):
        """
        Closes it's ``.websocket`` with close code of `1000`.
        
        This method is a coroutine.
        """
        websocket = self.websocket
        if websocket is None:
            return
        
        self.websocket = None
        await websocket.close(1000)
    
    
    def __repr__(self):
        """Returns the node's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' client=')
        repr_parts.append(repr(self.client))
        
        repr_parts.append(', host=')
        repr_parts.append(repr(self._host))
        
        repr_parts.append(', port=')
        repr_parts.append(repr(self._port))
        
        region = self.region
        if (region is not None):
            repr_parts.append(', region=')
            repr_parts.append(region.name)
        
        resume_key = self._resume_key
        if (resume_key is not None):
            repr_parts.append(', resume_key=')
            repr_parts.append(repr(resume_key))
        
        repr_parts.append(', reconnect_attempts=')
        repr_parts.append(repr(self.reconnect_attempts))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
        


