__all__ = ()

from time import time as time_now

from scarletio import CancelledError, Compound, Future, Theory, future_or_timeout

from ....env import CACHE_PRESENCE

from ...activity import ACTIVITY_UNKNOWN, Activity, ActivityType
from ...bases import maybe_snowflake_pair
from ...channel import Channel
from ...core import KOKORO
from ...events.event_handler_manager import EventHandlerManager
from ...events.handling_helpers import WaitForHandler
from ...gateway.client_gateway import (
    DiscordGateway, PRESENCE as GATEWAY_OPERATION_CODE_PRESENCE,
    REQUEST_MEMBERS as GATEWAY_OPERATION_CODE_REQUEST_MEMBERS
)
from ...preconverters import preconvert_preinstanced_type
from ...user import Status
from ...voice import VoiceClient

from ..functionality_helpers import MassUserChunker, SingleUserChunker
from ..request_helpers import get_guild_id


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


def _assert__request_members__limit(limit):
    """
    Asserts the `limit` parameter of ``Client.request_members`` method.
    
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


def _assert__request_members__name(name):
    """
    Asserts the `name` parameter of ``Client.request_members`` method.
    
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
        
        Notes
        -----
        This method is an alternative version of ``.client_edit_presence`` till further decision.
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
    
    
    async def request_all_members_of(self, guild):
        """
        Requests all members of the given guild.
        
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
        await self._request_members(guild_id)
    
    
    async def _request_members(self, guild_id):
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
            'op': GATEWAY_OPERATION_CODE_REQUEST_MEMBERS,
            'd': {
                'guild_id': guild_id,
                'query': '',
                'limit': 0,
                'presences': CACHE_PRESENCE,
                'nonce': nonce
            },
        }
        
        gateway = self.gateway_for(guild_id)
        await gateway.send_as_json(data)
        
        try:
            await waiter
        except CancelledError:
            try:
                del event_handler.waiters[nonce]
            except KeyError:
                pass
    
    
    async def request_members(self, guild, name, limit=1):
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
        
        assert _assert__request_members__limit(limit)
        assert _assert__request_members__name(name)
        
        event_handler = self.events.guild_user_chunk
        
        self._user_chunker_nonce = nonce = self._user_chunker_nonce + 1
        nonce = format(nonce, '0>16x')
        
        event_handler.waiters[nonce] = waiter = SingleUserChunker()
        
        data = {
            'op': GATEWAY_OPERATION_CODE_REQUEST_MEMBERS,
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
        
        try:
            return await waiter
        except CancelledError:
            try:
                del event_handler.waiters[nonce]
            except KeyError:
                pass
            
            return []
    
    
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
            self.events(wait_for_handler, name=event_name)
        
        future = Future(KOKORO)
        wait_for_handler.waiters[future] = check
        
        if (timeout is not None):
            future_or_timeout(future, timeout)
        
        try:
            return await future
        finally:
            waiters = wait_for_handler.waiters
            del waiters[future]
            
            if not waiters:
                self.events.remove(wait_for_handler, name=event_name)
