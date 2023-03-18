__all__ = ()

import warnings

from scarletio import Compound

from ...http import DiscordHTTPClient
from ...payload_building import build_create_payload, build_edit_payload
from ...scheduled_event import ScheduledEvent
from ...scheduled_event.scheduled_event.utils import (
    SCHEDULED_EVENT_CREATE_FIELD_CONVERTERS, SCHEDULED_EVENT_EDIT_FIELD_CONVERTERS
)
from ...user import User
from ...utils import log_time_converter

from ..request_helpers import (
    get_guild_id, get_scheduled_event_and_guild_id_and_id, get_scheduled_event_guild_id_and_id
)


class ClientCompoundScheduledEventEndpoints(Compound):
    
    http : DiscordHTTPClient
    
    
    async def scheduled_event_create(
        self, guild, scheduled_event_template = None, *positional_parameters, reason = None, **keyword_parameters
    ):
        """
        Creates a guild scheduled events.
        
        To define, where the event will take place, use the `location`, `stage`, `voice` parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, where to create the scheduled event.
        
        scheduled_event_template : `None`, ``ScheduledEvent``` = `None`, Optional
            Scheduled event to use as a template.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters either to define the template, or to overwrite specific fields' values.
        
        Other Parameters
        ----------------
        description : `None`, `str` = `None`, Optional (Keyword only)
            The event's description. It's length can be in range [0:1000].
        
        end : `None`, `datetime` = `None`, Optional (Keyword only)
            When the event will end.
        
        location : `None`, `str` = `None`, Optional (Keyword only)
            The location, where the event will take place.
        
        name : `str`, Optional (Keyword only)
            The event's name. It's length can be in range [1:100].
        
        privacy_level : ``PrivacyLevel``, `int` = `None`, Optional (Keyword only)
            The privacy level of the event. Whether it is global or guild only.
        
        stage : `None`, ``Channel``, `int` = `None`, Optional (Keyword only)
            The stage channel, where the event will take place.
        
        start : `datetime`, Optional (Keyword only)
            When the event will start.
        
        voice : `None`, ``Channel``, `int` = `None`, Optional (Keyword only)
            The voice channel, where the event will take place.
        
        Returns
        -------
        scheduled_event : ``ScheduledEvent``
            The created scheduled event.
        
        Raises
        ------
        TypeError
            - If `guild` is neither ``Guild`` nor `int`.
            - Parameter of incorrect type given.
            - Extra parameters.
        ValueError
            - Parameter of incorrect value given.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        if isinstance(scheduled_event_template, str) or positional_parameters:
            warnings.warn(
                (
                    f'`{self.__class__.__name__}.scheduled_event_create`\'s `name` and `start` parameters has been '
                    f'moved to be keyword only. Positional support will be removed in 2023 august.'
                ),
                FutureWarning,
                stacklevel = 2,
            )
            
            if isinstance(scheduled_event_template, str):
                keyword_parameters['name'] = scheduled_event_template
            
            if positional_parameters:
                keyword_parameters['start'] = positional_parameters[0]
        
        
        guild_id = get_guild_id(guild)
        data = build_create_payload(
            scheduled_event_template, SCHEDULED_EVENT_CREATE_FIELD_CONVERTERS, keyword_parameters
        )
        scheduled_event_data = await self.http.scheduled_event_create(guild_id, data, reason)
        return ScheduledEvent.from_data(scheduled_event_data)
    
    
    async def scheduled_event_edit(
        self,
        scheduled_event,
        scheduled_event_template = None,
        *,
        reason = None,
        **keyword_parameters,
    ):
        """
        Edits the given scheduled event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        scheduled_event : ``ScheduledEvent``, `tuple` (`int`, `int`)
            The scheduled event to edit.
        
        scheduled_event_template : `None`, ``ScheduledEvent``` = `None`, Optional
            Scheduled event to use as a template.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters either to define the template, or to overwrite specific fields' values.
        
        Other Parameters
        ----------------
        description : `None`, `str`, Optional (Keyword only)
            The new description of the scheduled event. It's length can be in range [0:1000].
        
        end : `None`, `datetime`
            The end of the of the scheduled event.
        
        location : `str`, Optional (Keyword only)
            The new location, where the event will take place.
        
        name : `str`, Optional (Keyword only)
            The new name of the scheduled event. It's length can be in range [1:100].
        
        privacy_level : ``PrivacyLevel``, `int`, Optional (Keyword only)
            The privacy level of the event. Whether it is global or guild only.
        
        stage : ``Channel``, `int`, Optional (Keyword only)
            The new stage channel, where the event will take place.
        
        start : `datetime`, Optional (Keyword only)
            The new start of the scheduled event.
        
        status : `str`, ``ScheduledEventStatus``, Optional (Keyword only)
            Thew new status of the scheduled event.
        
        voice : ``Channel``, `int`, Optional (Keyword only)
            The new voice channel, where the event will take place.
        
        Raises
        ------
        TypeError
            - If `scheduled_event` is neither ``ScheduledEvent`` nor `tuple` (`int`, `int`).
            - Parameter of incorrect type given.
            - Extra parameters.
        ValueError
            - Parameter of incorrect value given.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        scheduled_event, guild_id, scheduled_event_id = get_scheduled_event_and_guild_id_and_id(scheduled_event)
        
        data = build_edit_payload(
            scheduled_event, scheduled_event_template, SCHEDULED_EVENT_EDIT_FIELD_CONVERTERS, keyword_parameters
        )
        if data:
            await self.http.scheduled_event_edit(guild_id, scheduled_event_id, data, reason)
    
    
    async def scheduled_event_delete(self, scheduled_event):
        """
        Edits the given scheduled event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        scheduled_event : ``ScheduledEvent``, `tuple` (`int`, `int`)
            The scheduled event to edit.
        
        Raises
        ------
        TypeError
            If `scheduled_event` is neither ``ScheduledEvent``, nor `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id, scheduled_event_id = get_scheduled_event_guild_id_and_id(scheduled_event)
        await self.http.scheduled_event_delete(guild_id, scheduled_event_id)
    
    
    async def scheduled_event_get(self, scheduled_event, *, force_update = False):
        """
        Gets the given scheduled event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        scheduled_event : ``ScheduledEvent``, `tuple` `int` and `int`
            The scheduled event to get.
        force_update : `bool` = `False`, Optional (Keyword only)
            Whether the scheduled event should be requested even if it supposed to be up to date.
        
        Returns
        -------
        scheduled_event : ``ScheduledEvent``
        
        Raises
        ------
        TypeError
            If `scheduled_event` is neither ``ScheduledEvent``, nor `tuple` (`int`, `int`) instance.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        scheduled_event, guild_id, scheduled_event_id = get_scheduled_event_and_guild_id_and_id(scheduled_event)
        if (scheduled_event is None) or force_update:
            data = await self.http.scheduled_event_get(guild_id, scheduled_event_id, {'with_user_count', None})
            
            scheduled_event, is_created = ScheduledEvent.from_data_is_created(data)
            if not is_created:
                scheduled_event._update_attributes(data)
        
        return scheduled_event
    
    
    async def scheduled_event_get_all_guild(self, guild):
        """
        Gets the given guild's scheduled event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to get it's scheduled of.
        
        Returns
        -------
        scheduled_events : `list` of ``ScheduledEvent``
        
        Raises
        ------
        TypeError
            If `guild` is neither ``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        scheduled_event_datas = await self.http.scheduled_event_get_all_guild(guild_id, {'with_user_count': True})
        return [ScheduledEvent.from_data(scheduled_event_data) for scheduled_event_data in scheduled_event_datas]
    
    
    async def scheduled_event_user_get_chunk(self, scheduled_event, *, after = None, before = None, limit = None):
        """
        Requests a chunk user subscribed to a scheduled event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        scheduled_event : ``ScheduledEvent``, `tuple` `int` and `int`
            The scheduled event to get.
        after : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp after the subscribed users were created.
        before : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp before the subscribed users were created.
        limit : `None`, `int` = `None`, Optional (Keyword only)
            The amount of scheduled event users to request. Can be between 1 and 100.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        
        Raises
        ------
        TypeError
            - If `scheduled_event` is neither ``ScheduledEvent``, nor `tuple` (`int`, `int`) instance.
            - If `after`, `before` was passed with an unexpected type.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `limit` was not given as `int`.
            - If `limit` is out of range [1:100].
        """
        guild_id, scheduled_event_id = get_scheduled_event_guild_id_and_id(scheduled_event)
        
        if limit is None:
            limit = 100
        else:
            if __debug__:
                if not isinstance(limit, int):
                    raise AssertionError(
                        f'`limit` can be `int`, got {limit.__class__.__name__}; {limit!r}.'
                    )
                
                if (limit < 1) or (limit > 100):
                    raise AssertionError(
                        f'`limit` is out from the expected [1:100] range, got {limit!r}.'
                    )
        
        query_parameters = {}
        
        if limit != 100:
            query_parameters['limit'] = limit
        
        if (after is not None):
            query_parameters['after'] = log_time_converter(after)
        
        if (before is not None):
            query_parameters['before'] = log_time_converter(before)
        
        if guild_id:
            query_parameters['with_member'] = True
        
        scheduled_event_user_datas = await self.http.scheduled_event_user_get_chunk(
            guild_id, scheduled_event_id, query_parameters
        )
        
        users = []
        for scheduled_event_user_data in scheduled_event_user_datas:
            user_data = scheduled_event_user_data['user']
            user = User.from_data(user_data, user_data.get('member', None), guild_id)
            users.append(user)
        
        return users
    
    
    async def scheduled_event_user_get_all(self, scheduled_event):
        """
        Requests a chunk user subscribed to a scheduled event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        scheduled_event : ``ScheduledEvent``, `tuple` `int` and `int`
            The scheduled event to get.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        
        Raises
        ------
        TypeError
            - If `scheduled_event` is neither ``ScheduledEvent``, nor `tuple` (`int`, `int`) instance.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id, scheduled_event_id = get_scheduled_event_guild_id_and_id(scheduled_event)
        
        query_parameters = {'after': 0}
        
        if guild_id:
            query_parameters['with_member'] = True
        
        users = []
        
        while True:
            scheduled_event_user_datas = await self.http.scheduled_event_user_get_chunk(
                guild_id, scheduled_event_id, query_parameters,
            )
            
            for scheduled_event_user_data in scheduled_event_user_datas:
                user_data = scheduled_event_user_data['user']
                user = User.from_data(user_data, user_data.get('member', None), guild_id)
                users.append(user)
            
            if len(scheduled_event_user_datas) < 100:
                break
            
            query_parameters['after'] = users[-1].id
        
        return users
