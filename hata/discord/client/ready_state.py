__all__ = ()

from collections import deque

from scarletio import CancelledError, Future, Task, TaskGroup, WeakReferer, set_docs, sleep

from ...env import CACHE_PRESENCE, CACHE_USER

from ..core import KOKORO
from ..events.intent import INTENT_MASK_GUILD_PRESENCES, INTENT_MASK_GUILD_USERS
from ..gateway.client_gateway import REQUEST_GUILD_USERS as GATEWAY_OPERATION_CODE_REQUEST_GUILD_USERS


READY_STATE_TO_DO_GUILD_IDS = set()
GUILD_RECEIVE_TIMEOUT = 5.0
SHARD_CONNECT_TIMEOUT = 12.0

USER_REQUEST_STATE_NONE = 0
USER_REQUEST_STATE_TIMEOUT = 1
USER_REQUEST_STATE_DONE = 2
USER_REQUEST_STATE_CANCELLED = 3
USER_REQUEST_STATE_ERROR = 4

class ShardUserRequester:
    """
    User requested task of a shard.
    
    Attributes
    ----------
    can_request_users : `bool`
        Whether the client can request users with it's gateway.
    gateway : ``DiscordGateway``
        The shard's gateway.
    guild_create_waiter : `None`, ``Future``
        Water to wait for guild create event. Used when no more guild id is received to use up.
    guild_ids : `set` of `int`
        The guild's id to request the users of.
    received_guild_ids : `deque` of `tuple` (`int`, `bool`)
        A queue of received tuples. Each tuple contains a guild's identifier and whether it's users should be
        requested.
    state : `int`
        A state containing the requester's state.
    task : `None`, ``Task`` of ``._runner``
        A task executing the user requesting.
    """
    __slots__ = (
        'can_request_users', 'gateway', 'guild_create_waiter', 'guild_ids', 'received_guild_ids', 'state', 'task'
    )
    
    def __new__(cls, gateway, guild_ids, can_request_users):
        """
        Creates a new user requester.
        
        Parameters
        ----------
        gateway : ``DiscordGateway``
            The shard's gateway.
        guild_ids : `set` of `int`
            The guild's id to request the users of.
        can_request_users : `bool`
            Whether the client can request users with it's gateway.
        """
        self = object.__new__(cls)
        self.can_request_users = can_request_users
        self.gateway = gateway
        self.guild_ids = guild_ids
        self.received_guild_ids = deque()
        self.guild_create_waiter = None
        self.state = USER_REQUEST_STATE_NONE
        self.task = Task(KOKORO, self._runner())
        return self
    
    async def _runner(self):
        """
        Requests the users of the represented shard's guilds.
        
        This method is a coroutine.
        """
        try:
            guild_ids = self.guild_ids
            received_guild_ids = self.received_guild_ids
            can_request_users = self.can_request_users
            
            if can_request_users:
                sub_data = {
                    'guild_id': 0,
                    'query': '',
                    'limit': 0,
                    'presences': CACHE_PRESENCE,
                }
                
                data = {
                    'op': GATEWAY_OPERATION_CODE_REQUEST_GUILD_USERS,
                    'd': sub_data
                }
            
            while guild_ids:
                
                if not received_guild_ids:
                    guild_create_waiter = Future(KOKORO)
                    guild_create_waiter.apply_timeout(GUILD_RECEIVE_TIMEOUT)
                    self.guild_create_waiter = guild_create_waiter
                    
                    try:
                        await guild_create_waiter
                    except TimeoutError:
                        self.state = USER_REQUEST_STATE_TIMEOUT
                        return
                    finally:
                        self.guild_create_waiter = None
                
                guild_id, should_request_users = received_guild_ids.popleft()
                guild_ids.discard(guild_id)
                
                if not can_request_users:
                    continue
                
                try:
                    READY_STATE_TO_DO_GUILD_IDS.remove(guild_id)
                except KeyError:
                    continue
                
                if not should_request_users:
                    continue
                
                sub_data['guild_id'] = guild_id
                await self.gateway.send_as_json(data)
                await sleep(0.6, KOKORO)
        
        except (CancelledError, GeneratorExit):
            self.state = USER_REQUEST_STATE_CANCELLED
            raise
        
        except:
            self.state = USER_REQUEST_STATE_ERROR
            raise
        
        else:
            self.state = USER_REQUEST_STATE_DONE
        
        finally:
            self.task = None
    
    
    def cancel(self):
        """
        Cancels the user request task.
        """
        task = self.task
        if (task is not None):
            self.task = None
            task.cancel()
    
    
    def feed(self, guild_id, should_request_users):
        """
        Feeds a guild identifier to the shard user requesters.
        
        Parameters
        ----------
        guild_id : `int`
            The guild's identifier.
        should_request_users : `bool`
            Whether the guild's users should be requested.
        
        Returns
        -------
        request_enqueued : `bool`
            Whether the request is queued up.
        """
        if guild_id in self.guild_ids:
            self.received_guild_ids.append((guild_id, should_request_users))
            
            request_enqueued = True
        else:
            request_enqueued = False
        
        guild_create_waiter = self.guild_create_waiter
        if (guild_create_waiter is not None):
            guild_create_waiter.set_result_if_pending(None)
        
        return request_enqueued
    
    def discard(self, guild_id):
        """
        Discards a guild's identifier from the shard user requester.
        
        Parameters
        ----------
        guild_id : `int`
            The guild's identifier.
        """
        self.guild_ids.discard(guild_id)


if CACHE_PRESENCE:
    def should_request_users_of(client, guild):
        if client._should_request_users:
            if client.intents & INTENT_MASK_GUILD_PRESENCES:
                should_request_users = guild.large
            else:
                should_request_users = True
        else:
            should_request_users = False
        
        return should_request_users

elif CACHE_USER:
    def should_request_users_of(client, guild):
        return client._should_request_users

else:
    def should_request_users_of(client, guild):
        return False


set_docs(
    should_request_users_of,
    """
    Returns whether the users of the given guild should be requested.
    
    Parameters
    ----------
    guild : ``Guild``
        A received guild instance.
    
    Returns
    -------
    client : ``Client``
        The respective client instance.
    should_request_users : `bool`
        Whether the guild's users should be requested.
    """
)


class ReadyState:
    """
    Attributes
    ----------
    client_reference : ``WeakReferer`` to ``Client``
        Reference to the ready state's client.
    shard_count : `int`
        The amount of shards of the client.
    shard_user_requesters : `dict` of (`int`, ``ShardUserRequester``) items.
        User requester for each shard.
    shard_ready_waiter : `None` of ``Future``
        Waiter for shard ready event.
    task : `None`, ``Task`` to ``._runner``
        Task, which waits for all the user requests to finish.
    """
    __slots__ = ('client_reference', 'shard_count', 'shard_user_requesters', 'shard_ready_waiter', 'task')
    
    def __new__(cls, client):
        """
        Creates a new ready state instance from the given parameters.
        
        Parameters
        ----------
        client : ``Client``
            The respective client instance.
        """
        self = object.__new__(cls)
        self.shard_count = client.shard_count
        self.shard_user_requesters = {}
        self.task = Task(KOKORO, self._runner())
        self.shard_ready_waiter = None
        self.client_reference = WeakReferer(client)
        
        return self
    
    def shard_ready(self, client, guild_datas, shard_id):
        """
        Sets the ready state's `.last_ready` to the current time and increases it's `.guild_left_counter` by the
        length of the given data.
        
        Parameters
        ----------
        guild_datas : `list` of `Any`
            Received guild datas.
        shard_id : `int`
            The shard's identifier.
        """
        shard_user_requesters = self.shard_user_requesters
        try:
            shard_user_requester = shard_user_requesters[shard_id]
        except KeyError:
            pass
        else:
            shard_user_requester.cancel()
        
        shard_count = client.shard_count
        gateway = client.gateway
        if shard_count:
            gateway = gateway.gateways[shard_id]
        
        guild_ids = set(int(guild_data['id']) for guild_data in guild_datas)
        
        can_request_users = client.intents & INTENT_MASK_GUILD_USERS
        
        if can_request_users:
            READY_STATE_TO_DO_GUILD_IDS.update(guild_ids)
        
        shard_user_requesters[shard_id] = ShardUserRequester(gateway, guild_ids, can_request_users)
        
        shard_ready_waiter = self.shard_ready_waiter
        if (shard_ready_waiter is not None):
            shard_ready_waiter.set_result_if_pending(None)
    
    def call_ready(self):
        """
        Calls the ready event handler of the respective client.
        """
        client = self.client_reference()
        if (client is not None):
            client.ready_state = None
            Task(KOKORO, client.events.ready(client))
    
    
    def feed_guild(self, client, guild):
        """
        Feeds the given `guild` to the ready state. Sets the last received guild's time to the current time and ends
        the ready state if there are no more guilds to receive.
        
        Parameters
        ----------
        client : ``Client``
            The respective client instance.
        guild : ``Guild``
            Received guild.
        
        Returns
        -------
        request_enqueued : `bool`
            Whether the request is queued up.
        """
        should_request_users = should_request_users_of(client, guild)
        
        guild_id = guild.id
        
        shard_count = self.shard_count
        if shard_count == 0:
            shard_id = 0
        else:
            shard_id = (guild_id >> 22) % shard_count
        
        try:
            shard_user_requester = self.shard_user_requesters[shard_id]
        except KeyError:
            request_enqueued = False
        else:
            if shard_user_requester.state == USER_REQUEST_STATE_NONE:
                request_enqueued = shard_user_requester.feed(guild_id, should_request_users)
            else:
                request_enqueued = False
        
        return request_enqueued
    
    
    async def _runner(self):
        """
        Runner task of the ready state waiting for all guild users to be requested.
        
        This method is a coroutine.
        """
        try:
            shard_count = self.shard_count
            if not shard_count:
                shard_count = 1
            
            while True:
                tasks = None
                done_tasks = 0
                
                for shard_user_requester in self.shard_user_requesters.values():
                    if shard_user_requester.state == USER_REQUEST_STATE_NONE:
                        if tasks is None:
                            tasks = []
                        
                        tasks.append(shard_user_requester.task)
                    else:
                        done_tasks += 1
                
                if (tasks is not None):
                    await TaskGroup(KOKORO, tasks).wait_all()
                    continue
                
                if done_tasks == shard_count:
                    break
                
                shard_ready_waiter = Future(KOKORO)
                shard_ready_waiter.apply_timeout(SHARD_CONNECT_TIMEOUT)
                self.shard_ready_waiter = shard_ready_waiter
                
                try:
                    await shard_ready_waiter
                except TimeoutError:
                    return
                finally:
                    self.shard_ready_waiter = None
        
        finally:
            self.task = None
            self.call_ready()
    
    def cancel(self):
        """
        Cancels the ready state.
        """
        task = self.task
        if (task is not None):
            self.task = None
            task.cancel()
            
            for shard_user_requester in self.shard_user_requesters.values():
                shard_user_requester.cancel()
    
    def __iter__(self):
        """
        Waits till the ready state receives all of it's shards and guilds, or till timeout occurs.
        
        This method is an awaitable generator.
        """
        task = self.task
        if (task is not None):
            try:
                yield from task
            except CancelledError:
                if self.task is not None:
                    raise
    
    __await__ = __iter__
    
    def discard_guild(self, guild):
        """
        Discards a guild from the guild requests.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild to discard from the ready state.
        """
        guild_id = guild.id
        
        shard_count = self.shard_count
        if shard_count == 0:
            shard_id = 0
        else:
            shard_id = (guild_id >> 22) % shard_count
        
        try:
            shard_user_requester = self.shard_user_requesters[shard_id]
        except KeyError:
            pass
        else:
            try:
                shard_user_requester.remove(guild_id)
            except KeyError:
                pass
            else:
                if guild.partial:
                    READY_STATE_TO_DO_GUILD_IDS.discard(guild_id)
