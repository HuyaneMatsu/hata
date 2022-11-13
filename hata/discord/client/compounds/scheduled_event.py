__all__ = ()

from datetime import datetime

from scarletio import Compound

from ...channel import Channel
from ...core import SCHEDULED_EVENTS
from ...http import DiscordHTTPClient
from ...scheduled_event import PrivacyLevel, ScheduledEvent, ScheduledEventEntityType, ScheduledEventStatus
from ...user import ClientUserBase, User
from ...utils import datetime_to_timestamp, log_time_converter
from ..request_helpers import (
    get_channel_id, get_guild_id, get_scheduled_event_guild_id_and_id, get_scheduled_event_and_guild_id_and_id
)


class ClientCompoundScheduledEventEndpoints(Compound):
    
    http : DiscordHTTPClient
    
    
    async def scheduled_event_create(
        self, guild, name, start, *, description = None, end=None, privacy_level=PrivacyLevel.guild_only,
        location=None, stage=None, voice=None, reason = None
    ):
        """
        Creates a guild scheduled events.
        
        To define, where the event will take place, use the `location`, `stage`, `voice` parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, where to create the scheduled event.
        name : `str`
            The event's name. It's length can be in range [1:100].
        start : `datetime``
            When the event will start.
        description : `None`, `str` = `None`, Optional (Keyword only)
            The event's description. It's length can be in range [0:1000].
        end : `None`, `datetime` = `None`, Optional (Keyword only)
            When the event will end.
        privacy_level : ``PrivacyLevel``, `int` = `None`, Optional (Keyword only)
            The privacy level of the event. Whether it is global or guild only.
        location : `None`, `str` = `None`, Optional (Keyword only)
            The location, where the event will take place.
        stage : `None`, ``Channel``, `int` = `None`, Optional (Keyword only)
            The stage channel, where the event will take place.
        voice : `None`, ``Channel``, `int` = `None`, Optional (Keyword only)
            The voice channel, where the event will take place.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Returns
        -------
        scheduled_event : ``ScheduledEvent``
            The created event.
        
        Raises
        ------
        TypeError
            - If `guild` is neither ``Guild``, nor `int`.
            - If `privacy_level` is neither ``PrivacyLevel``, nor `int`.
            - If `stage` is neither ``Channel``, nor `int`.
            - If `voice` is neither ``Channel``, nor `int`.
            - If neither `location`, `stage`, `voice` parameters is given.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` is not `str`.
            - If `name`'s length is out of the expected range.
            - If `description is neither `None` nor `str`.
            - If `description`'s length is out of the expected range.
            - If `location` is not `str`.
            - If `start` is not `datetime`.
            - If `end `is neither `None`, nor `datetime`.
        """
        guild_id = get_guild_id(guild)
        
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(
                    f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                )
            
            name_length = len(name)
            if (name_length < 1) or (name_length > 100):
                raise AssertionError(
                    f'`name` length can be in range [1:100], got {name_length!r}; {name!r}.'
                )
        
        if __debug__:
            if not isinstance(start, datetime):
                raise AssertionError(
                    f'`start` can be `datetime`, got {start.__class__.__name__}; {start!r}.'
                )
            
            if (end is not None) and (not isinstance(end, datetime)):
                raise AssertionError(
                    f'`end` can be `None`, `datetime`, got {end.__class__.__name__}; {end!r}.'
                )
        
        if isinstance(privacy_level, PrivacyLevel):
            privacy_level_value = privacy_level.value
        elif isinstance(privacy_level, int):
            privacy_level_value = privacy_level
        else:
            raise TypeError(
                f'`privacy_level` can be `{PrivacyLevel.__name__}` `int`, got '
                f'{privacy_level.__class__.__name__}; {privacy_level!r}.'
            )
        
        if (description is not None):
            if __debug__:
                if (not isinstance(description, str)):
                    raise AssertionError(
                        f'`description` can be `None`, `str`, got {description.__class__.__name__}, {description!r}.'
                    )
                
                description_length = len(description)
                if description_length > 1000:
                    raise AssertionError(
                        f'description length can be in range [0:1000], got {description_length!r}; {description!r}.'
                    )
            
            if not description:
                description = None
        
        if (location is not None):
            if __debug__:
                if not isinstance(location, str):
                    raise AssertionError(
                        f'`location` can be `str`, got {location.__class__.__name__}; {location!r}.'
                    )
            
            channel_id = None
            entity_metadata = {'location': location}
            entity_type = ScheduledEventEntityType.location
        
        elif (stage is not None):
            channel_id = get_channel_id(stage, Channel.is_guild_stage)
            entity_metadata = None
            entity_type = ScheduledEventEntityType.stage
        
        elif (voice is not None):
            channel_id = get_channel_id(voice, Channel.is_guild_voice)
            entity_metadata = None
            entity_type = ScheduledEventEntityType.voice
            
        else:
            raise TypeError(
                f'Either `location`, `stage`, `voice` parameters are required.'
            )
        
        data = {
            'name' : name,
            'privacy_level': privacy_level_value,
            'channel_id': channel_id,
            'entity_metadata': entity_metadata,
            'entity_type': entity_type.value,
            'scheduled_start_time': datetime_to_timestamp(start),
        }
        
        if (description is not None):
            data['description'] = description
        
        if (end is not None):
            data['scheduled_end_time'] = datetime_to_timestamp(end)
        
        data = await self.http.scheduled_event_create(guild_id, data, reason)
        return ScheduledEvent(data)
    
    # In theory you can edit the target entity is as well, but we will ignore it for now.
    
    async def scheduled_event_edit(
        self, scheduled_event, *, name=..., description = ..., start=..., end=..., privacy_level=..., status=...,
        location=..., stage=..., voice=..., reason = None
    ):
        """
        Edits the given scheduled event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        scheduled_event : ``ScheduledEvent``, `tuple`, (`int`, `int`)
            The scheduled event to edit.
        name : `str`, Optional (Keyword only)
            The new name of the scheduled event. It's length can be in range [1:100].
        description : `None`, `str`, Optional (Keyword only)
            The new description of the scheduled event. It's length can be in range [0:1000].
            
            Pass it as `None` to remove the old one.
        
        start : `datetime`, Optional (Keyword only)
            The new start of the scheduled event.
        
        end : `None`, `datetime`
            The end of the of the scheduled event.
            
            Pass it as `None` to remove the old end.
        
        privacy_level : ``PrivacyLevel``, `int`, Optional (Keyword only)
            The privacy level of the event. Whether it is global or guild only.
        
        status : `str`, ``ScheduledEventStatus``, Optional (Keyword only)
            Thew new status of the scheduled event.
        
        location : `str`, Optional (Keyword only)
            The new location, where the event will take place.
        
        stage : ``Channel``, `int`, Optional (Keyword only)
            The new stage channel, where the event will take place.
        
        voice : ``Channel``, `int`, Optional (Keyword only)
            The new voice channel, where the event will take place.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            - If `scheduled_event` is neither ``ScheduledEvent``, nor `tuple` (`int`, `int`).
            - If `privacy_level` is neither ``PrivacyLevel``, nor `int`.
            - If `stage` is neither ``Channel``, nor `int`.
            - If `voice` is neither ``Channel``, nor `int`.
            - If `privacy_level` is neither ``PrivacyLevel``, nor `int`.
            - If `status` is neither ``ScheduledEventStatus``, nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` is not `str`.
            - If `name`'s length is out of the expected range.
            - If `description is neither `None` nor `str`.
            - If `description`'s length is out of the expected range.
            - If `location` is not `str`.
            - If `start` is not `datetime`.
            - If `end `is neither `None`, nor `datetime`.
        """
        guild_id, scheduled_event_id = get_scheduled_event_guild_id_and_id(scheduled_event)
        
        data = {}
        
        if (name is not ...):
            if __debug__:
                if not isinstance(name, str):
                    raise AssertionError(
                        f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                    )
                
                name_length = len(name)
                if (name_length < 1) or (name_length > 100):
                    raise AssertionError(
                        f'`name` length can be in range [1:100], got {name_length!r}; {name!r}.'
                    )
            
            data['name'] = name
        
        
        if (description is not ...):
            if description is None:
                description = ''
            else:
                if __debug__:
                    if (not isinstance(description, str)):
                        raise AssertionError(
                            f'`description` can be `None`, `str`, got '
                            f'{description.__class__.__name__}; {description!r}.'
                        )
                    
                    description_length = len(description)
                    if description_length > 1000:
                        raise AssertionError(
                            f'description length can be in range [0:1000], got '
                            f'{description_length!r}; {description!r}.'
                        )
            
            data['description'] = description
        
        if (start is not ...):
            if __debug__:
                if not isinstance(start, datetime):
                    raise AssertionError(
                        f'`start` can be `datetime`, got {start.__class__.__name__}; {start!r}.'
                    )
            
            data['scheduled_start_time'] = datetime_to_timestamp(start)
        
        if (end is not ...):
            if __debug__:
                if (end is not None) and (not isinstance(end, datetime)):
                    raise AssertionError(
                        f'`end` can be `None`, `datetime`, got {end.__class__.__name__}; {end!r}.'
                    )
            
            data['scheduled_end_time'] = None if end is None else datetime_to_timestamp(end)
        
        if (privacy_level is not ...):
            if isinstance(privacy_level, PrivacyLevel):
                privacy_level_value = privacy_level.value
            elif isinstance(privacy_level, int):
                privacy_level_value = privacy_level
            else:
                raise TypeError(
                    f'`privacy_level` can be `{PrivacyLevel.__name__}`, `int`, got '
                    f'{privacy_level.__class__.__name__}; {privacy_level!r}.'
                )
            
            data['privacy_level'] = privacy_level_value
        
        if (status is not ...):
            if isinstance(status, ScheduledEventStatus):
                status_value = status.value
            elif isinstance(status, int):
                status_value = status
            else:
                raise TypeError(
                    f'`status` can be `{ScheduledEventStatus.__name__}`, `int` , got '
                    f'{status.__class__.__name__}; {status!r}.'
                )
            
            data['status'] = status_value
        
        if (location is not ...) or (stage is not ...) or (voice is not ...):
            if (location is not ...):
                if __debug__:
                    if not isinstance(location, str):
                        raise AssertionError(
                            f'`location` can be `str`, got {location.__class__.__name__}; {location!r}.'
                        )
                
                channel_id = None
                entity_metadata = {'location': location}
                entity_type = ScheduledEventEntityType.location
            
            elif (stage is not ...):
                channel_id = get_channel_id(stage, Channel.is_guild_stage)
                entity_metadata = None
                entity_type = ScheduledEventEntityType.stage
            
            # elif (voice is not ...):
            else:
                channel_id = get_channel_id(voice, Channel.is_guild_voice)
                entity_metadata = None
                entity_type = ScheduledEventEntityType.voice
            
            data['channel_id'] = channel_id
            data['entity_metadata'] = entity_metadata
            data['entity_type'] = entity_type.value
        
        
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
    
    
    async def scheduled_event_get(self, scheduled_event, *, force_update=False):
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
        
            if scheduled_event is None:
                try:
                    scheduled_event = SCHEDULED_EVENTS[scheduled_event_id]
                except KeyError:
                    scheduled_event = ScheduledEvent(data)
                else:
                    scheduled_event._update_attributes(data)
                    scheduled_event._update_counts_only(data)
            else:
                scheduled_event = ScheduledEvent(data)
        
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
        return [ScheduledEvent(scheduled_event_data) for scheduled_event_data in scheduled_event_datas]
    
    
    async def scheduled_event_user_get_chunk(self, scheduled_event, *, after=None, before=None, limit=None):
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
                guild_id,
                scheduled_event_id,
                query_parameters,
            )
            
            for scheduled_event_user_data in scheduled_event_user_datas:
                user_data = scheduled_event_user_data['user']
                user = User.from_data(user_data, user_data.get('member', None), guild_id)
                users.append(user)
            
            if len(scheduled_event_user_datas) < 100:
                break
            
            query_parameters['after'] = users[-1].id
        
        return users
