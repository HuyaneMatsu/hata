__all__ = ()

from scarletio import Compound

from ...channel import Channel
from ...http import DiscordHTTPClient
from ...scheduled_event import PrivacyLevel
from ...stage import Stage

from ..request_helpers import get_channel_id, get_stage_channel_id


class ClientCompoundStageEndpoints(Compound):
    
    http : DiscordHTTPClient
    
    
    async def stage_create(
        self, channel, topic, *, privacy_level=PrivacyLevel.guild_only, send_start_notification=False,
    ):
        """
        Edits the given stage channel.
        
        Will trigger a `stage_create` event.
        
        > The endpoint has a long rate limit, so please use ``.stage_edit`` to edit just the stage's topic.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to edit.
        
        topic : `None`, `str`
            The new topic of the stage.
        
        privacy_level : ``PrivacyLevel``, `int` = `PrivacyLevel.guild_only`, Optional (Keyword only)
            The new privacy level of the stage. Defaults to guild only.
        
        send_start_notification : `bool` = `False`, Optional (Keyword only)
            Whether @everyone should be notified when the stage is started.
            
            > You must have `mention everyone` permission.
        
        Returns
        -------
        stage : ``Stage``
            The created stage instance.
        
        Raises
        ------
        TypeError
            - If `channel` was not given as ``Channel`` neither as `int`.
            - If `privacy_level` was not given neither as ``PrivacyLevel`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `topic` was not given neither as `None`, `str`.
            - If `topic`'s length is out of range [1:120].
            - If `send_start_notification` is not `bool`
        """
        # channel_id
        channel_id = get_channel_id(channel, Channel.is_guild_stage)
        
        # topic
        if topic is None:
            topic = ''
        else:
            if __debug__:
                if not isinstance(topic, str):
                    raise AssertionError(
                        f'`topic` can be `None`, `str`, got {topic.__class__.__name__}; {topic!r}.'
                    )
                
                topic_length = len(topic)
                if (topic_length < 1) or (topic_length > 120):
                    raise AssertionError(
                        f'`topic` length can be in range [1:120], got {topic_length!r}; {topic!r}.'
                    )
        
        # privacy_level
        if isinstance(privacy_level, PrivacyLevel):
            privacy_level = privacy_level.value
        
        elif isinstance(privacy_level, int):
            privacy_level = privacy_level
        
        else:
            raise TypeError(
                f'`privacy_level` can be `{PrivacyLevel.__name__}`, `int` , got '
                f'{privacy_level.__class__.__name__}; {privacy_level!r}.'
            )
        
        # send_start_notification
        if __debug__:
            if not isinstance(send_start_notification, bool):
                raise AssertionError(
                    f'`send_start_notification` can be `bool`, '
                    f'got {send_start_notification.__class__.__name__}; {send_start_notification!r}.'
                )
        
        
        data = {
            'channel_id': channel_id,
            'topic': topic,
            'privacy_level': privacy_level,
        }
        
        if send_start_notification:
            data['send_start_notification'] = True
        
        
        data = await self.http.stage_create(data)
        return Stage(data)
    
    
    async def stage_edit(self, stage, topic=..., *, privacy_level=...):
        """
        Edits the given stage channel.
        
        Will trigger a `stage_edit` event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        stage : ``Stage``, ``Channel``, `int`
            The stage to edit. Can be given as it's channel's identifier.
        topic : `str`
            The new topic of the stage.
        privacy_level : ``PrivacyLevel``, `int`, Optional (Keyword only)
            The new privacy level of the stage.
        
        Raises
        ------
        TypeError
            - If `stage` was not given as ``Stage``, ``Channel`` neither as `int`.
            - If `privacy_level` was not given neither as ``PrivacyLevel`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `topic` was not given neither as `None` nor as `str`.
            - If `topic`'s length is out of range [1:120].
        """
        channel_id = get_stage_channel_id(stage)
        
        data = {}
        
        if (topic is not ...):
            if __debug__:
                if not isinstance(topic, str):
                    raise AssertionError(
                        f'`topic` can be `None`, `str`, got {topic.__class__.__name__}; {topic!r}.'
                    )
                
                topic_length = len(topic)
                if (topic_length < 1) or (topic_length > 120):
                    raise AssertionError(
                        f'`topic` length can be in range [1:120], got {topic_length!r}; {topic!r}.'
                    )
            
            data['topic'] = topic
        
        
        if (privacy_level is not ...):
            if isinstance(privacy_level, PrivacyLevel):
                privacy_level = privacy_level.value
            elif isinstance(privacy_level, int):
                privacy_level = privacy_level
            else:
                raise TypeError(
                    f'`privacy_level` can be `{PrivacyLevel.__name__}`, `int` , got '
                    f'{privacy_level.__class__.__name__}; {privacy_level!r}.'
                )
            
            data['privacy_level'] = privacy_level
        
        
        if not data:
            return
        
        await self.http.stage_edit(channel_id, data)
        # We receive data, but ignore it, so we can dispatch it.
    
    
    async def stage_delete(self, stage):
        """
        Deletes the given stage channel.
        
        Will trigger a `stage_delete` event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        stage : ``Stage``, ``Channel``, `int`
            The stage to delete. Can be given as it's channel's identifier.
        
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
        
        await self.http.stage_delete(channel_id)
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
        
        data = await self.http.stage_get(channel_id)
        return Stage(data)
