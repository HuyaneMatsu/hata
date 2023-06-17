__all__ = ('SolarClient', )

from random import choice

from scarletio import RichAttributeErrorBaseType, Task, TaskGroup, WeakReferer, run_coroutine, to_json
from scarletio.web_common.headers import AUTHORIZATION, CONTENT_TYPE

from ...discord.channel import Channel
from ...discord.client import Client
from ...discord.client.request_helpers import get_channel_guild_id_and_id
from ...discord.core import KOKORO
from ...discord.voice.utils import try_get_voice_region

from .event_handler_plugin import SolarLinkEventManager
from .exceptions import SolarAuthenticationError
from .node import SolarNode
from .player import SolarPlayer
from .player_base import SolarPlayerBase
from .route_planner import get_route_planner
from .track import GetTracksResult, Track


class SolarClient(RichAttributeErrorBaseType):
    """
    Represents a lavalink client used to manage nodes and connections.
    
    Attributes
    ----------
    _client_reference : ``Weakreferer`` to ``Client``
        Weakreference to the extended client instance.
    _events : ``SolarLinkEventManager``
        Event plugin for solarlink specific events.
    _player_queue : `None`, `list` of ``SolarPlayerBase``
        Solar players to join back to a node.
    nodes : `set` of ``SolarNode``
        All nodes the client is connected to.
    players : `dict` of (`int`, ``SolarPlayerBase``) items
        Active players of the client by their guild's identifier as key.
    """
    __slots__ = ('_client_reference', '_events', '_player_queue', 'nodes', 'players')
    
    def __new__(cls, client):
        """
        Creates and binds a lavalink manager client.
        
        Parameters
        ----------
        client : ``Client``
            Hata client instance to extend.
        """
        if not isinstance(client, Client):
            raise TypeError(
                f'`client` parameter can be `{Client.__name__}`, got {client.__class__.__name__}; {client!r}.'
            )
        
        event_plugin = SolarLinkEventManager()
        client.events.register_plugin(event_plugin)
        
        client_reference = WeakReferer(client)
        
        self = object.__new__(cls)
        self._client_reference = client_reference
        self.nodes = set()
        self.players = {}
        self._player_queue = None
        self._events = event_plugin
        return self
    
    
    def add_node(self, host, port, password, region, resume_key = None, reconnect_attempts=3):
        """
        Adds a node to Lavalink's node manager.
        
        The return of the method depends on the thread, from which it was called from.
        
        Parameters
        ----------
        host : `str`
            The address of the lavalink node.
        port : `int`
            The port used by the lavalink node.
        password : `str`
            The password used for authentication.
        region : `str`
            The region to assign this node to.
        resume_key : `str` = `None`, Optional
            A resume key used for resuming a session upon re-establishing a WebSocket connection to Lavalink.
        reconnect_attempts : `int` = `3`, Optional
            The amount of times connection with the node will be reattempted before giving up.
            Set to `-1` for infinite.
        
        Returns
        -------
        task : `bool`, ``Task``, ``FutureAsyncWrapper``
            - If the method was called from the client's thread (KOKORO), then returns a ``Task``. The task will return
                `True`, if connecting was successful.
            - If the method was called from an ``EventThread``, but not from the client's, then returns a
                `FutureAsyncWrapper`. The task will return `True`, if connecting was successful.
            - If the method was called from any other thread, then waits for the connector task to finish and returns
                `True`, if it was successful.
        
        Raises
        ------
        RuntimeError
            If the ``SolarClient``'s client is already deconstructed.
        TypeError
            - If `host` is not `str`.
            - If `port` is not `int`.
            - If `password is not `str`.
            - If `region` is neither `None`, nor ``VoiceRegion``.
            - If `resume_key` is neither `None`, nor `str`.
        """
        client = self._client_reference()
        if client is None:
            raise RuntimeError(f'`{self.__class__.__name__}` client is deconstructed.')
        
        node = SolarNode(
            client,
            host,
            port,
            password,
            region,
            resume_key,
            reconnect_attempts,
        )
        
        self.nodes.add(node)
        
        return run_coroutine(node.start(), KOKORO)
    
    
    async def get_tracks(self, query):
        """
        Gets all tracks associated with the given query.
        
        Parameters
        ----------
        query: : `str`
            The query to perform a search for.
        
        Returns
        -------
        tracks : `None`, ``GetTracksResult``
            Decoded tracks.
        
        Raises
        ------
        RuntimeError
            - If there are no available nodes.
            - If the ``SolarClient``'s client is already deconstructed.
        SolarAuthenticationError
            Authentication failed towards the node.
        """
        available_nodes = self.available_nodes
        if not available_nodes:
            raise RuntimeError('No available nodes!')
        
        client = self._client_reference()
        if client is None:
            raise RuntimeError(f'`{self.__class__.__name__}` client is deconstructed.')
        
        node = choice(self.available_nodes)
        
        async with client.http.get(
            f'http://{node._host}:{node._port}/loadtracks',
            headers = {
                AUTHORIZATION: node._password,
            },
            params = {
                'identifier': query,
            },
        ) as response:
            if response.status == 200:
                data = await response.json()
            
            elif response.status in (401, 403):
                raise SolarAuthenticationError(node, response)
            
            else:
                data = None
        
        if data is None:
            result = None
        else:
            result = GetTracksResult(data)
        
        return result
    
    
    async def decode_track(self, track):
        """
        Decodes a base64-encoded track string into a dictionary.
        
        Parameters
        ----------
        track : `str`
            The base64-encoded track string.
        
        Returns
        -------
        track : `None`, ``Track``
            Decoded track data.
        
        Raises
        ------
        RuntimeError
            - If there are no available nodes.
            - If the ``SolarClient``'s client is already deconstructed.
        SolarAuthenticationError
            Authentication failed towards the node.
        """
        client = self._client_reference()
        if client is None:
            raise RuntimeError(f'`{self.__class__.__name__}` client is deconstructed.')
        
        available_nodes = self.available_nodes
        if not available_nodes:
            raise RuntimeError('No available nodes!')
        
        node = choice(self.available_nodes)
        
        async with client.http.get(
            f'http://{node._host}:{node._port}/decodetrack',
            headers = {
                AUTHORIZATION: node._password,
            },
            params = {
                'track': track
            },
        ) as response:
            if response.status == 200:
                track_data = await response.json()
            
            elif response.status == 401 or response.status == 403:
                raise SolarAuthenticationError(node, response)
            
            else:
                track_data = None
        
        if track_data is None:
            track = None
        else:
            track = Track(track_data)
        
        return track
    
    
    async def decode_tracks(self, tracks):
        """
        Decodes a list of base64-encoded track strings.
        
        Parameters
        ----------
        tracks : `list` of `str`
            A list of base64-encoded track strings.
        
        Returns
        -------
        tracks : `list` of ``Track``
            The decoded tracks.
        
        Raises
        ------
        RuntimeError
            - If there are no available nodes.
            - If the ``SolarClient``'s client is already deconstructed.
        SolarAuthenticationError
            Authentication failed towards the node.
        """
        client = self._client_reference()
        if client is None:
            raise RuntimeError(f'`{self.__class__.__name__}` client is deconstructed.')
        
        available_nodes = self.available_nodes
        if not available_nodes:
            raise RuntimeError('No available nodes!')
        
        node = choice(available_nodes)
        
        async with client.http.post(
            f'http://{node._host}:{node._port}/decodetracks',
            headers = {
                AUTHORIZATION: node._password,
                CONTENT_TYPE: 'application/json',
            },
            data = to_json(tracks),
        ) as response:
            if response.status == 200:
                track_datas = await response.json()
            
            elif response.status in (401, 403):
                raise SolarAuthenticationError(node, response)
            
            else:
                track_datas = None
        
        if (track_datas is None) or (not track_datas):
            tracks = []
        else:
            tracks = [Track(track_data) for track_data in track_datas]
        
        return tracks
    
    
    async def routeplanner_status(self, node):
        """
        Gets the routeplanner status of the target node.
        
        This method is a coroutine.
        
        Parameters
        ----------
        node : ``SolarNode``
            The node to use for the query.
        
        Returns
        -------
        route_planner : `None`, ``RoutePlannerBase``
        
        Raises
        ------
        RuntimeError
            If the ``SolarClient``'s client is already deconstructed.
        """
        client = self._client_reference()
        if client is None:
            raise RuntimeError(f'`{self.__class__.__name__}` client is deconstructed.')
        
        async with client.http.get(
            f'http://{node._host}:{node._port}/routeplanner/status',
            headers = {
                AUTHORIZATION: node._password,
            },
        ) as response:
            if response.status == 200:
                route_planner_data = await response.json()
            
            elif response.status in (401, 403):
                raise SolarAuthenticationError(node, response)
            
            else:
                route_planner_data = None
        
        if route_planner_data is None:
            route_planner = None
        else:
            route_planner = get_route_planner(route_planner_data)
        
        return route_planner
        
    
    async def routeplanner_free_address(self, node, address):
        """
        Removes a single address from the addresses which are currently marked as failing.
        
        This method is a coroutine.
        
        Parameters
        ----------
        node : ``SolarNode``
            The node to use for the query.
        address : `str`
            The address to free.
        
        Returns
        -------
        success : `bool`
            Whether the address is freed up.
        
        Raises
        ------
        SolarAuthenticationError
            Authentication failed towards the node.
        RuntimeError
            If the ``SolarClient``'s client is already deconstructed.
        """
        client = self._client_reference()
        if client is None:
            raise RuntimeError(f'`{self.__class__.__name__}` client is deconstructed.')
        
        async with client.http.post(
            f'http://{node._host}:{node._port}/routeplanner/free/address',
            headers = {
                AUTHORIZATION: node._password,
                CONTENT_TYPE: 'application/json',
            },
            data = to_json(
                {'address': address}
            ),
        ) as response:
            status = response.status
            if status in (401, 403):
                raise SolarAuthenticationError(node, response)
            
            if status == 204:
                # Success
                return True
            
            if status == 500:
                # The node has no routeplanner configured.
                return False
            
            # Unexpected case.
            return False
    
    
    async def routeplanner_free_address_all(self, node):
        """
        Removes all addresses from the list which holds the addresses which are marked failing.
        
        This method is a coroutine.
        
        Parameters
        ----------
        node : ``SolarNode``
            The node to use for the query.
        
        Returns
        -------
        success : `bool`
        
        Raises
        ------
        SolarAuthenticationError
            Authentication failed towards the node.
        RuntimeError
            If the ``SolarClient``'s client is already deconstructed.
        """
        client = self._client_reference()
        if client is None:
            raise RuntimeError(f'`{self.__class__.__name__}` client is deconstructed.')
        
        async with client.http.post(
            f'http://{node._host}:{node._port}/routeplanner/free/all',
            headers = {
                AUTHORIZATION: node._password,
            },
        ) as response:
            status = response.status
            if status in (401, 403):
                raise SolarAuthenticationError(node, response)
            
            if status == 204:
                # Success
                return True
            
            if status == 500:
                # The node has no routeplanner configured
                return False
            
            # Unexpected case.
            return False
    
    
    @property
    def available_nodes(self):
        """
        Returns a list of available nodes.
        
        Returns
        -------
        available_nodes : `list` of ``SolarNode``
        """
        return [node for node in self.nodes if node.available]
    
    
    def remove_node(self, node):
        """
        Removes a node.
        
        Parameters
        ----------
        node : ``SolarNode``
            The node to remove from the list.
        """
        self.nodes.discard(node)
    
    
    def find_ideal_node(self, region=None):
        """
        Finds the least used node in the given region.
        
        Parameters
        ----------
        region : `None`, ``VoiceRegion`` = `None`, Optional
            The region to find a node in. Defaults to `None`.
        
        Returns
        -------
        node : `None`, ``SolarNode``
        """
        nodes = self.available_nodes
        if not nodes:
            return None
        
        if (region is not None):
            region_nodes = [node for node in nodes if node.region is region]
            if region_nodes:
                nodes = region_nodes
        
        return min(nodes, key = node_penalty_key)
    
    
    async def _node_connected(self, node):
        """
        Called when a node is connected from Lavalink.
        
        Parameters
        ----------
        node : `SolarNode`
            The node that has just connected.
        """
        player_queue = self._player_queue
        if (player_queue is not None):
            task_group = TaskGroup(KOKORO, (Task(KOKORO, player.change_node(node)) for player in player_queue))
            self._player_queue = None
            
            failed_task = await task_group.wait_exception()
            if (failed_task is not None):
                task_group.cancel_all()
                failed_task.get_result()
    
    
    async def _node_disconnected(self, node):
        """
        Called when a node is disconnected from Lavalink.
        
        Parameters
        ----------
        node : `SolarNode`
            The node that has just connected.
        """
        players = node.players
        
        if players:
            best_node = self.find_ideal_node(node.region)
            if best_node is None:
                player_queue = self._player_queue
                if player_queue is None:
                    player_queue = list(players)
                    self._player_queue = player_queue
                else:
                    player_queue.extend(players)
            else:
                task_group = TaskGroup(KOKORO, (Task(KOKORO, player.change_node(best_node)) for player in players))
                failed_task = await task_group.wait_exception()
                if (failed_task is not None):
                    task_group.cancel_all()
                    failed_task.get_result()
    
    
    def get_player(self, guild_id):
        """
        Gets a player.
        
        Parameters
        ----------
        guild_id : `int`
            The guild's identifier where the player is.
        
        Returns
        -------
        player : `None`, ``Player``
            Returns `None` if the guild has no player.
        """
        return self.players.get(guild_id, None)
    
    
    async def join_voice(self, channel, *, cls=SolarPlayer):
        """
        Joins a solar player to the channel. If there is an already existing solar player at the respective guild,
        moves it.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `tuple` (`int`, `int`)
            The channel to join to.
        cls : ``SolarPlayerBase`` = ``SolarPlayer``, Optional (Keyword only)
            The player's class to create.
        
        Returns
        -------
        solar_player : ``SolarPlayerBase``
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``Channel`` nor as `tuple` (`int`, `int`).
        RuntimeError
            - If there are no available nodes.
            - If the ``SolarClient``'s client is already deconstructed.
        """
        if (cls is not SolarPlayer) and (not issubclass(cls, SolarPlayerBase)):
            raise TypeError(
                f'`cls` can be `{SolarPlayerBase.__name__}` subclass, got {cls!r}.'
            )
        
        guild_id, channel_id = get_channel_guild_id_and_id(channel, Channel.is_in_group_guild_connectable)
        
        
        try:
            player = self.players[guild_id]
        except KeyError:
            region = try_get_voice_region(guild_id, channel_id)
            node = self.find_ideal_node(region)
            if node is None:
                raise RuntimeError('No available nodes!')
            
            player, waiter = cls(node, guild_id, channel_id)
            self.players[guild_id] = player
            await waiter
        
        else:
            if player.channel_id != channel_id:
                client = self._client_reference()
                if client is None:
                    raise RuntimeError(f'`{self.__class__.__name__}` client is deconstructed.')
                
                gateway = client.gateway_for(guild_id)
                await gateway.change_voice_state(guild_id, channel_id)
        
        return player
    
    
    def __repr__(self):
        """Returns the solar client's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        node_count = len(self.nodes)
        if node_count:
            repr_parts.append(' node count=')
            repr_parts.append(repr(node_count))
        
        player_count = len(self.players)
        if player_count:
            repr_parts.append(' player count=')
            repr_parts.append(repr(player_count))
        
        player_queue = self._player_queue
        if (player_queue is not None):
            repr_parts.append(' queued up players=')
            repr_parts.append(len(player_queue))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)


def node_penalty_key(node):
    """
    Key sued inside of ``SolarClient.find_ideal_node`` when deciding which is the ideal node based on their penalty.
    
    Parameters
    ----------
    node : ``SolarNode``
        A respective node.
    
    Returns
    -------
    penalty : `float`
        The node's penalty.
    """
    return node.penalty
