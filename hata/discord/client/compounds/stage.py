__all__ = ()

from scarletio import Compound

from ...channel import Channel
from ...http import DiscordApiClient
from ...payload_building import build_create_payload, build_edit_payload
from ...stage import Stage
from ...stage.stage.utils import STAGE_CREATE_FIELD_CONVERTERS, STAGE_EDIT_FIELD_CONVERTERS

from ..request_helpers import get_channel_id, get_stage_and_channel_id, get_stage_channel_id


class ClientCompoundStageEndpoints(Compound):
    
    api : DiscordApiClient
    
    
    async def stage_create(self, channel, stage_template = None, *, reason = None, **keyword_parameters):
        """
        Edits the given stage channel.
        
        Will trigger a `stage_create` event.
        
        > The endpoint has a long rate limit, so please use ``.stage_edit`` to edit just the stage's topic.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to create the stage at.
        
        stage_template : `None`, ``Stage`` = `None`, Optional
            Stage entity to use as a template.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the guild's audit logs.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters to create the role with.
        
        Other Parameters
        ----------------
        privacy_level : ``PrivacyLevel``, `int`, Optional (Keyword only)
            The new privacy level of the stage. Defaults to guild only.
        
        scheduled_event : `int`, ``ScheduledEvent``, Optional (Keyword only)
            Alternative for `scheduled_event_id`.
        
        scheduled_event_id : `int`, ``ScheduledEvent``, Optional (Keyword only)
            The scheduled event's identifier that started the stage.
        
        send_start_notification : `bool`, Optional (Keyword only)
            Whether @everyone should be notified when the stage is started.
            
            > You must have `mention everyone` permission.
        
        topic : `None`, `str`, Optional (Keyword only)
            The topic of the stage.
        
        Returns
        -------
        stage : ``Stage``
            The created stage instance.
        
        Raises
        ------
        TypeError
            - If `channel` was not given as ``Channel`` neither as `int`.
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        # channel_id
        channel_id = get_channel_id(channel, Channel.is_guild_stage)
        
        data = build_create_payload(stage_template, STAGE_CREATE_FIELD_CONVERTERS, keyword_parameters)
        data['channel_id'] = channel_id
        
        stage_data = await self.api.stage_create(data, reason)
        return Stage.from_data(stage_data)
    
    
    async def stage_edit(self, stage, stage_template = None, *, reason = None, **keyword_parameters):
        """
        Edits the given stage channel.
        
        Will trigger a `stage_edit` event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        stage : ``Stage``, ``Channel``, `int`
            The stage to edit. Can be given as it's channel's identifier.
        
        stage_template : `None`, ``Stage`` = `None`, Optional
            Stage entity to use as a template.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the guild's audit logs.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters to create the role with.
        
        Other Parameters
        ----------------
        privacy_level : ``PrivacyLevel``, `int`, Optional (Keyword only)
            The new privacy level of the stage.
        
        topic : `None`, `str`, Optional (Keyword only)
            The new topic of the stage.
        
        Raises
        ------
        TypeError
            - If `channel` was not given as ``Channel`` neither as `int`.
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        stage, channel_id = get_stage_and_channel_id(stage)
        
        data = build_edit_payload(stage, stage_template, STAGE_EDIT_FIELD_CONVERTERS, keyword_parameters)
        
        if data:
            await self.api.stage_edit(channel_id, data, reason)
            # We receive data, but ignore it, so we can dispatch it.
    
    
    async def stage_delete(self, stage, *, reason = None):
        """
        Deletes the given stage channel.
        
        Will trigger a `stage_delete` event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        stage : ``Stage``, ``Channel``, `int`
            The stage to delete. Can be given as it's channel's identifier.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the guild's audit logs.
        
        Raises
        ------
        TypeError
            If `stage` was not given as ``Stage``, ``Channel`` neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_stage_channel_id(stage)
        
        await self.api.stage_delete(channel_id, reason)
        # We receive no data.
    
    
    async def stage_get(self, channel):
        """
        Gets the stage of the given stage channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The stage's channel's identifier.
        
        Raises
        ------
        TypeError
            If `channel` was not given as ``Channel`` neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(channel, Channel.is_guild_stage)
        
        data = await self.api.stage_get(channel_id)
        return Stage.from_data(data)
