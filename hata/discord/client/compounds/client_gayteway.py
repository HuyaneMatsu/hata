__all__ = ()

import warnings
from time import time as time_now

from scarletio import Compound, Future, Theory

from ....env import CACHE_PRESENCE

from ...activity import ACTIVITY_UNKNOWN, Activity, ActivityType
from ...bases import maybe_snowflake_pair
from ...channel import Channel
from ...core import KOKORO
from ...events.event_handler_manager import EventHandlerManager
from ...events.handling_helpers import WaitForHandler
from ...gateway.client_gateway import (
    DiscordGateway, PRESENCE as GATEWAY_OPERATION_CODE_PRESENCE,
    REQUEST_GUILD_USERS as GATEWAY_OPERATION_CODE_REQUEST_GUILD_USERS,
    REQUEST_SOUNDBOARD_SOUNDS as GATEWAY_OPERATION_REQUEST_SOUNDBOARD_SOUNDS
)
from ...preconverters import preconvert_preinstanced_type
from ...user import Status
from ...voice import VoiceClient

from ..functionality_helpers import MassUserChunker, SingleUserChunker
from ..request_helpers import get_guild_and_id, get_guild_id


def _assert__edit_presence__afk(afk):
    """
    Asserts the `afk` parameter of ``Client.edit_presence`` method.
    
    Parameters
    ----------
    afk : `bool`
        Whether the client is afk or not (?).
    
    Raises
    ------
    AssertionError
        - If `afk` is not `bool`.
    """
    if not isinstance(afk, bool):
        raise AssertionError(
            f'`afk` can be `bool`, got {afk.__class__.__name__}; {afk!r}.'
        )
    
    return True


def _assert__request_users__limit(limit):
    """
    Asserts the `limit` parameter of ``Client.request_users`` method.
    
    Parameters
    ----------
    limit : `int`
        The amount of users to be received. Limited to `100`.
    
    Raises
    ------
    AssertionError
        - If `limit` is not `int`.
        - If `limit` is out of the expected range [1:100].
    """
    if not isinstance(limit, int):
        raise AssertionError(
            f'`limit` can be `int`, got {limit.__class__.__name__}; {limit!r}.'
        )
    
    if limit < 1 or limit > 100:
        raise AssertionError(
            f'`limit` is out of the expected range [1:100], got {limit!r}.'
        )
    
    return True


def _assert__request_users__name(name):
    """
    Asserts the `name` parameter of ``Client.request_users`` method.
    
    Parameters
    ----------
    name : `str`
        The received user's name or nick should start with this string.
    
    Raises
    ------
    AssertionError
            - If `name` is not `str`.
            - If `name` length is out of the expected range [1:32].
    """
    if not isinstance(name, str):
        raise AssertionError(
            f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
        )
    
    name_length = len(name)
    if name_length < 1 or name_length > 32:
        raise AssertionError(
            f'`name` length can be in range [1:32], got {name_length!r}; {name!r}.'
        )
    
    return True


class ClientCompoundClientGateway(Compound):
    
    events : EventHandlerManager
    gateway : DiscordGateway
    bot : bool
    voice_clients : dict
    
    @Theory
    def gateway_for(self, guild_id): ...
    
    
    async def edit_presence(self, *, activity=..., status=..., afk=False):
        """
        Changes the client's presence (status and activity). If a parameter is not defined, it will not be changed.
        
        This method is a coroutine.
        
        Parameters
        ----------
        activity : ``Activity``, Optional (Keyword only)
            The new activity of the Client.
        status : `str`, ``Status``, Optional (Keyword only)
            The new status of the client.
        afk : `bool` = `False`, Optional (Keyword only)
            Whether the client is afk or not (?).
        
        Raises
        ------
        TypeError:
            - If the status is not `str`, ``Status``.
            - If activity is not ``Activity`` or has type ``ActivityType.custom``.
        ValueError:
            - If the status `str`, but not any of the predefined ones.
        """
        if status is ...:
            status = self._status
        else:
            status = preconvert_preinstanced_type(status, 'status', Status)
            self._status = status
        
        status = status.value
        
        if activity is ...:
            activity = self._activity
        elif activity is None:
            self._activity = ACTIVITY_UNKNOWN
        elif isinstance(activity, Activity) and (activity.type is not ActivityType.custom):
            self._activity = activity
        else:
            raise TypeError(
                f'`activity` can be `{Activity.__name__}` (except `{ActivityType.custom.name}`), got: '
                f'{activity.__class__.__name__}; {activity!r}.'
            )
        
        if activity is None:
            pass
        elif activity is ACTIVITY_UNKNOWN:
            activity = None
        else:
            activity = activity.to_data(user = not self.bot)
        
        if status == 'idle':
            since = int(time_now() * 1000.)
        else:
            since = 0
        
        assert _assert__edit_presence__afk(afk)
        
        
        data = {
            'op': GATEWAY_OPERATION_CODE_PRESENCE,
            'd': {
                'game': activity,
                'since': since,
                'status': status,
                'afk': afk,
            },
        }
        
        await self.gateway.send_as_json(data)
    
    
    async def join_voice(self, channel):
        """
        Joins a voice client to the channel. If there is an already existing voice client at the respective guild,
        moves it.
        
        If not every library is installed, raises `RuntimeError`, or if the voice client fails to connect raises
        `TimeoutError`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `tuple` (`int`, `int`)
            The channel to join to.
        
        Returns
        -------
        voice_client : ``VoiceClient``
        
        Raises
        ------
        RuntimeError
            If not every library is installed to join voice.
        TimeoutError
            If voice client fails to connect the given channel.
        TypeError
            If `channel` was not given neither as ``Channel`` nor as `tuple` (`int`, `int`).
        """
        while True:
            if isinstance(channel, Channel):
                if channel.is_in_group_guild_connectable() or channel.partial:
                    guild_id = channel.guild_id
                    channel_id = channel.id
                    break
            
            else:
                snowflake_pair = maybe_snowflake_pair(channel)
                if (snowflake_pair is not None):
                    guild_id, channel_id = snowflake_pair
                    break
                
            raise TypeError(
                f'`channel` can be a connectable channel, `tuple` (`int`, `int`)'
                f', got {channel.__class__.__name__}; {channel!r}.'
            )
        
        
        try:
            voice_client = self.voice_clients[guild_id]
        except KeyError:
            voice_client = await VoiceClient(self, guild_id, channel_id)
        else:
            if voice_client.channel_id != channel_id:
                gateway = self.gateway_for(guild_id)
                await gateway.change_voice_state(guild_id, channel_id)
        
        return voice_client
    
    
    async def request_soundboard_sounds(self, guilds, *, force_request = False):
        """
        Requests the soundboard sounds of the given guilds.
        
        This function is a coroutine.
        
        Parameters
        ----------
        guilds : `iterable` of (``Guild``, `int`)
            The guilds or their identifiers to request the sounds of.
        force_request : `bool` = `False`
            Whether the sounds should be requested even if they are already cached.
        
        Returns
        -------
        sounds : `None`, `list` of ``SoundboardSoundsEvent``
            Might return `None` if there are no guilds to request sounds from.
        """
        guild_ids = set()
        
        if force_request:
            for guild in guilds:
                guild_id = get_guild_id(guild)
                guild_ids.add(guild_id)
        
        else:
            for guild in guilds:
                guild, guild_id = get_guild_and_id(guild)
                if (guild is not None) and guild.soundboard_sounds_cached:
                    continue
                
                guild_ids.add(guild_id)
        
        if not guild_ids:
            return None
        
        by_gateway = {}
        
        for guild in guilds:
            guild_id = get_guild_id(guild)
            gateway = self.gateway_for(guild_id)
            
            try:
                guild_ids_for_gateway = by_gateway[gateway]
            except KeyError:
                guild_ids_for_gateway = []
                by_gateway[gateway] = guild_ids_for_gateway
            
            guild_ids_for_gateway.append(guild_id)
        
        
        for gateway, guild_ids_for_gateway in by_gateway.items():
            await gateway.send_as_json({
                'op': GATEWAY_OPERATION_REQUEST_SOUNDBOARD_SOUNDS,
                'd': {
                    'guild_ids': guild_ids_for_gateway,
                }
            })
        
        return await self.events.soundboard_sounds.wait_for_events_in_guilds(guild_ids)
    
    
    async def request_all_users_of(self, guild):
        """
        Requests all users of the given guild.
        
        > This method uses the client's gateway to request the users. If any of the parameters do not match their
        > expected value or if timeout occurs, returns instead of raising.
        
        If the ``Client`` is created with `should_request_users` parameter given as `False`, this parameter can be used
        to request users of specific guilds.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's members will be requested.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild`` or `int`.
        """
        guild_id = get_guild_id(guild)
        await self._request_users(guild_id)
    
    
    async def _request_users(self, guild_id):
        """
        Requests the members of the given guild. Called when the client joins a guild and user caching is enabled
        (so by default).
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild_id : ``int``
            The guild, what's members will be requested.
        """
        event_handler = self.events.guild_user_chunk
        
        self._user_chunker_nonce = nonce = self._user_chunker_nonce + 1
        nonce = format(nonce, '0>16x')
        
        event_handler.waiters[nonce] = waiter = MassUserChunker()
        
        data = {
            'op': GATEWAY_OPERATION_CODE_REQUEST_GUILD_USERS,
            'd': {
                'guild_id': guild_id,
                'query': '',
                'limit': 0,
                'presences': CACHE_PRESENCE,
                'nonce': nonce,
            },
        }
        
        gateway = self.gateway_for(guild_id)
        await gateway.send_as_json(data)
        
        if not (await waiter):
            try:
                del event_handler.waiters[nonce]
            except KeyError:
                pass
    
    
    async def request_users(self, guild, name, limit = 1):
        """
        Requests the members of the given guild by their name.
        
        > This method uses the client's gateway to request the users. If any of the parameters do not match their
        > expected value or if timeout occurs, returns an empty list instead of raising.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's members will be requested.
        name : `str`
            The received user's name or nick should start with this string.
        limit : `int` = `1`, Optional
            The amount of users to be received. Limited to `100`.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild`` or `int`.
        """
        guild_id = get_guild_id(guild)
        
        assert _assert__request_users__limit(limit)
        assert _assert__request_users__name(name)
        
        event_handler = self.events.guild_user_chunk
        
        self._user_chunker_nonce = nonce = self._user_chunker_nonce + 1
        nonce = format(nonce, '0>16x')
        
        event_handler.waiters[nonce] = waiter = SingleUserChunker()
        
        data = {
            'op': GATEWAY_OPERATION_CODE_REQUEST_GUILD_USERS,
            'd': {
                'guild_id': guild_id,
                'query': name,
                'limit': limit,
                'presences': CACHE_PRESENCE,
                'nonce': nonce,
            },
        }
        
        gateway = self.gateway_for(guild_id)
        await gateway.send_as_json(data)
        
        users = await waiter
        if users is None:
            try:
                del event_handler.waiters[nonce]
            except KeyError:
                pass
            
            users = []
        
        return users
    
    
    async def wait_for(self, event_name, check, timeout = None):
        """
        O(n) event waiter with massive overhead compared to other optimized event waiters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        event_name : `str`
            The respective event's name.
        check : `callable`
            Check, what tells that the waiting is over.
            
            If the `check` returns `True` the received `args` are passed to the waiter future and returned by the
            method. However if the check returns any non `bool` value, then that object is passed next to `args` and
            returned as well.
        
        timeout : `None`, `float` = `None`, Optional
            Timeout after `TimeoutError` is raised and the waiting is cancelled.
        
        Returns
        -------
        result : `Any`
            Parameters passed to the `check` and the value returned by the `check` if it's type is not `bool`.
        
        Raised
        ------
        TimeoutError
            Timeout occurred.
        BaseException
            Any exception raised by `check`.
        """
        wait_for_handler = self.events.get_handler(event_name, WaitForHandler)
        if wait_for_handler is None:
            wait_for_handler = WaitForHandler()
            self.events(wait_for_handler, name = event_name)
        
        future = Future(KOKORO)
        wait_for_handler.waiters[future] = check
        
        if (timeout is not None):
            future.apply_timeout(timeout)
        
        try:
            return await future
        finally:
            waiters = wait_for_handler.waiters
            del waiters[future]
            
            if not waiters:
                self.events.remove(wait_for_handler, name = event_name)
    
    
    async def request_members(self, *position_parameters, **keyword_parameters):
        """
        Deprecated and will be removed in 2023 December. Please use ``.request_users`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.request_members` is deprecated and will be removed in 2023 December. '
                f'Please use `.request_users` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return await self.request_users(*position_parameters, **keyword_parameters)
    
    
    async def request_all_members_of(self, *position_parameters, **keyword_parameters):
        """
        Deprecated and will be removed in 2023 December. Please use ``.request_all_users_of`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.request_all_members_of` is deprecated and will be removed in 2023 '
                f'December. '
                f'Please use `.request_all_users_of` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return await self.request_all_users_of(*position_parameters, **keyword_parameters)
