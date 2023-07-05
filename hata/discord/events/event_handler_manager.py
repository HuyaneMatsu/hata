__all__ = ()

import warnings
from functools import partial as partial_func

from scarletio import CallableAnalyzer, RichAttributeErrorBaseType, Task, WeakReferer

from ..core import KOKORO

from .core import (
    DEFAULT_EVENT_HANDLER, EVENT_HANDLER_NAMES, EVENT_HANDLER_NAME_TO_PARSER_NAMES, PARSER_SETTINGS,
    get_plugin_event_handler, get_plugin_event_handler_and_parameter_count, get_plugin_event_handler_and_parser_names
)
from .default_event_handlers import (
    default_error_event_handler, default_voice_client_ghost_event_handler, default_voice_client_join_event_handler,
    default_voice_client_leave_event_handler, default_voice_client_move_event_handler,
    default_voice_client_shutdown_event_handler, default_voice_client_update_event_handler,
    default_voice_server_update_event_handler
)
from .event_handler_plugin import EventHandlerPlugin
from .event_types import WebhookUpdateEvent
from .handling_helpers import (
    ChunkWaiter, _iterate_event_handler, asynclist, check_name, check_parameter_count_and_convert
)
from .soundboard_sounds_event_handler import SoundboardSoundsEventHandler


DEFAULT_EVENT_HANDLERS = (
    ('error', default_error_event_handler, False),
    ('guild_user_chunk', ChunkWaiter, True),
    ('soundboard_sounds', SoundboardSoundsEventHandler, True),
    ('voice_server_update', default_voice_server_update_event_handler, False),
    ('voice_client_ghost', default_voice_client_ghost_event_handler, False),
    ('voice_client_join', default_voice_client_join_event_handler, False),
    ('voice_client_move', default_voice_client_move_event_handler, False),
    ('voice_client_leave', default_voice_client_leave_event_handler, False),
    ('voice_client_update', default_voice_client_update_event_handler, False),
    ('voice_client_shutdown', default_voice_client_shutdown_event_handler, False),
)

EVENT_HANDLER_ATTRIBUTES = frozenset((
    '_launch_called',
    'client_reference',
    '_plugin_events',
    '_plugins',
))

# All silent added at 2023-06-29

DEPRECATION_LEVEL_NONE = 0
DEPRECATION_LEVEL_REMOVED = 1 << 0
DEPRECATION_LEVEL_SHOULD_WRAP = 1 << 1
DEPRECATION_LEVEL_RENAMED_SILENT = 1 << 2


EVENT_DEPRECATION_TABLE = {
    'client_edit': DEPRECATION_LEVEL_RENAMED_SILENT,
    'message_edit': DEPRECATION_LEVEL_RENAMED_SILENT,
    'user_edit': DEPRECATION_LEVEL_RENAMED_SILENT,
    'guild_user_edit': DEPRECATION_LEVEL_RENAMED_SILENT | DEPRECATION_LEVEL_SHOULD_WRAP,
    'channel_edit': DEPRECATION_LEVEL_RENAMED_SILENT,
    'emoji_edit': DEPRECATION_LEVEL_RENAMED_SILENT,
    'sticker_edit': DEPRECATION_LEVEL_RENAMED_SILENT,
    'guild_edit': DEPRECATION_LEVEL_RENAMED_SILENT,
    'integration_edit': DEPRECATION_LEVEL_RENAMED_SILENT,
    'role_edit': DEPRECATION_LEVEL_RENAMED_SILENT,
    'stage_edit': DEPRECATION_LEVEL_RENAMED_SILENT,
    'scheduled_event_edit': DEPRECATION_LEVEL_RENAMED_SILENT,
    'auto_moderation_rule_edit': DEPRECATION_LEVEL_RENAMED_SILENT,
    'webhook_update': DEPRECATION_LEVEL_SHOULD_WRAP,
    'guild_user_update': DEPRECATION_LEVEL_SHOULD_WRAP,
    'role_delete': DEPRECATION_LEVEL_SHOULD_WRAP
}


def _get_event_deprecation_state(name):
    """
    Checks whether the event is deprecated.
    
    If it is deprecated returns `True` and drops a warning.
    
    Parameters
    ----------
    name : `str`
        The event handler's name.
    
    Returns
    -------
    deprecation_level : `int`
    """
    # if name == 'stuff':
    #    warnings.warn(
    #        (
    #            '`Client.events.stuff` is deprecated and will be removed in 2222 yay.\n'
    #            'Please use `Client.events.stiff(client, event)` instead.'
    #        ),
    #        FutureWarning,
    #        stacklevel = 3,
    #    )
    #    
    #    return DEPRECATION_LEVEL_REMOVED
    return EVENT_DEPRECATION_TABLE.get(name, DEPRECATION_LEVEL_NONE)


SILENT_NAME_TRANSLATION_TABLE = {
    'client_edit': 'client_update',
    'message_edit': 'message_update',
    'user_edit': 'user_update',
    'guild_user_edit': 'guild_user_update',
    'channel_edit': 'channel_update',
    'emoji_edit': 'emoji_update',
    'sticker_edit': 'sticker_update',
    'guild_edit': 'guild_update',
    'integration_edit': 'integration_update',
    'role_edit': 'role_update',
    'stage_edit': 'stage_update',
    'scheduled_event_edit': 'scheduled_event_update',
    'auto_moderation_rule_edit': 'auto_moderation_rule_update',
}


def _translate_name_deprecation_silent(name):
    """
    Translates silent name deprecation without warning.
    
    Parameters
    ----------
    name : `str`
        The event handler's name.
    
    Returns
    -------
    name : `str`
    """
    return SILENT_NAME_TRANSLATION_TABLE.get(name, name)


def _wrap_maybe_deprecated_event(name, func):
    """
    Wraps the given maybe deprecated event handler.
    
    Parameters
    ----------
    name : `str`
        The event's name.
    func : `object`
        Event handler.
    
    Returns
    -------
    func : ``FunctionType``
        The wrapper or maybe not wrapped event handler.
    """
    if name == 'webhook_update':
        analyzer = CallableAnalyzer(func)
        if analyzer.is_async():
            real_analyzer = analyzer
        else:
            real_analyzer = CallableAnalyzer(func.__call__, as_method = True)
        
        for parameter in real_analyzer.parameters:
            if 'channel' in parameter.name:
                has_channel_parameter = True
                break
        else:
            has_channel_parameter = False
        
        if has_channel_parameter:
            warnings.warn(
                (
                    f'`Client.events.webhook_update`\'s `channel` parameter` is removed.\n'
                    f'Please use `event` (type {WebhookUpdateEvent.__name__}) parameter instead.'
                ),
                FutureWarning,
                stacklevel = 3,
            )
            
            if analyzer is not real_analyzer:
                func = func()
            
            async def webhook_update_event_handler_wrapper(client, event):
                return await func(client, event.channel)
            
            return webhook_update_event_handler_wrapper
    
    elif name == 'guild_user_update':
        analyzer = CallableAnalyzer(func)
        if analyzer.is_async():
            real_analyzer = analyzer
        else:
            real_analyzer = CallableAnalyzer(func.__call__, as_method = True)
        
        for index, parameter in enumerate(real_analyzer.parameters, 0):
            if 'guild' in parameter.name:
                guild_parameter_index = index
                break
        else:
            guild_parameter_index = -1
        
        for index, parameter in enumerate(real_analyzer.parameters, 0):
            if 'user' in parameter.name:
                user_parameter_index = index
                break
        else:
            user_parameter_index = -1
        
        if (
            guild_parameter_index != -1 and user_parameter_index != -1 and
            guild_parameter_index > user_parameter_index
        ):
            warnings.warn(
                (
                    f'`Client.events.guild_user_update`\'s `user` and `guild` parameters have been switched to match'
                    f'other event handlers.\n'
                    f'Please change your event handler definition to `client, guild, user, old_attributes`.'
                ),
                FutureWarning,
                stacklevel = 3,
            )
            
            if analyzer is not real_analyzer:
                func = func()
            
            async def guild_user_update_event_handler_wrapper(client, guild, user, old_attributes):
                return await func(client, guild, user, old_attributes)
            
            return guild_user_update_event_handler_wrapper
    
    
    elif name == 'role_delete':
        analyzer = CallableAnalyzer(func)
        if analyzer.is_async():
            real_analyzer = analyzer
        else:
            real_analyzer = CallableAnalyzer(func.__call__, as_method = True)
        
        min_, max_ = real_analyzer.get_non_reserved_positional_parameter_range()
        if (min_ == 3) and not analyzer.accepts_args():
            warnings.warn(
                (
                    f'`Client.events.role_delete`\'s `guild` parameter` is removed.\n'
                    f'Please just use `client, role` parameters instead.'
                ),
                FutureWarning,
                stacklevel = 3,
            )
            
            if analyzer is not real_analyzer:
                func = func()
            
            async def role_delete_event_handler_wrapper(client, role):
                return await func(client, role, role.guild)
            
            return role_delete_event_handler_wrapper
    
    return func


class EventHandlerManager(RichAttributeErrorBaseType):
    """
    After a client gets a dispatch event from Discord, it's parser might ensure an event. These events are stored
    inside of a ``EventHandlerManager`` and can be accessed through ``Client.events``.
    
    Each added event should be an async callable accepting a predefined amount of positional parameters.
    
    Adding Event Handlers
    ----------------------
    To add event handler just do:
    
    ```py
    @client.events
    async def message_create(client, message):
        ...
    ```
    
    If you are having an event handler with a different name, that is a problem, use the `name` parameter.
    
    ```py
    @client.events(name = 'message_create')
    async def filter_messages(client, message):
        ...
    ```
    
    You can also overwrite all existing event handler, with using the `overwrite` parameter, or by assigning it
    directly.
    
    ```py
    @client.events(overwrite=True)
    async def message_create(client, message):
        ...
    
    
    async def message_create(client, message):
        ...
    
    client.events.message_create = message_create
    ```
    
    If want to and an event handler to multiple clients, there is the ``ClientWrapper`` option.
    
    ```py
    ALL = ClientWrapper()
    
    @ALL.events
    async def launch(client):
        print(f'{client:f} launched!')
    ```
    
    Removing Event Handlers
    -----------------------
    If want to remove the events, use the ``.remove`` method. It is familiar when you use add an event handler.
    
    If names match, just calling `.remove(event_handler` is enough.
    
    ```py
    client.events.remove(message_create)
    ```
    
    If names do not match, it supports a name parameter for this reason.
    
    ```py
    client.events.remove(filter_messages, name = 'message_create')
    ```
    
    If you want to remove all event handlers from an event, using the `del` keyword is an option.
    
    ```py
    del client.events.message_create
    ```
    
    A special case is when you cant have the event handler, but have it's type. For these cases use it's type and the
    `by_type` parameter.
    
    ```py
    client.events.remove(MyEventHandlerType, by_type=True)
    ```
    
    Attributes
    ----------
    _launch_called : `bool`
        Whether The respective client's `.events.launch` was called already.
    _plugin_events : `None`, `dict` of (`str`, ``EventHandlerPlugin``) items
        Event name to plugin relation.
    _plugins : `None`, `set` of ``EventHandlerPlugin``
        Plugins added to the event handler.
    client_reference : ``WeakReferer`` to ``Client``
        Weak reference to the parent client to avoid reference loops.
    
    Additional Event Attributes
    ---------------------------
    application_command_count_update(client: ``Client``, event: ``ApplicationCommandCountUpdate``)
        Called when a guild's application commands changed.
    
    application_command_create(client: ``Client``, guild_id: `int`, application_command: ``ApplicationCommand``)
        Called when you create an application guild bound to a guild.
    
    application_command_delete(client: ``Client``, guild_id: `int`, application_command: ``ApplicationCommand``)
        Called when you delete one of your guild bound application commands.
    
    application_command_permission_update(client: ``Client``, \
            application_command_permission: ``ApplicationCommandPermission``)
        Called when an application command's permissions are updated inside of a guild.
    
    application_command_update(client : ``Client``, guild_id: `int`, application_command: ``ApplicationCommand``, \
            old_attributes : {`dict`, `None`})
        Called when you update one of your guild bound application command.
        
        `old_attributes` might be given as `None` if the `application_command` is not cached. If it is cached, is given
        as a `dict` which contains the updated attributes of the application command as keys and their old values as
        the values.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +---------------------------+---------------------------------------------------+
        | Keys                      | Values                                            |
        +===========================+===================================================+
        | description               | `None`, `str`                                     |
        +---------------------------+---------------------------------------------------+
        | description_localizations | `None`, `dict` of (``Locale``, `str`) items       |
        +---------------------------+---------------------------------------------------+
        | allow_in_dm               | `bool`                                            |
        +---------------------------+---------------------------------------------------+
        | name                      | `str`                                             |
        +---------------------------+---------------------------------------------------+
        | name_localizations        | `None`, `dict` of (``Locale``, `str`) items       |
        +---------------------------+---------------------------------------------------+
        | nsfw                      | `bool`                                            |
        +---------------------------+---------------------------------------------------+
        | options                   | `None`, `list` of ``ApplicationCommandOption``    |
        +---------------------------+---------------------------------------------------+
        | required_permissions      | ``Permission``                                    |
        +---------------------------+---------------------------------------------------+
        | target_type               | ``ApplicationCommandTargetType``                  |
        +---------------------------+---------------------------------------------------+
        | version                   | `int`                                             |
        +---------------------------+---------------------------------------------------+
    
    audit_log_entry_create(client: ``Client``, audit_log_entry : ``AuditLogEntry``)
        Called when an audit log entry is created inside of a guild.
        
        The client must have view audit log permissions in the guild to receive it.
    
    auto_moderation_action_execution(client: ``Client``, event: ``AutoModerationActionExecutionEvent``)
        Called when an auto moderation rule is executed.
    
    auto_moderation_rule_create(client: ``Client``, auto_moderation_rule: ``AutoModerationRule``)
        Called when an auto moderation rule is created.
    
    auto_moderation_rule_delete(client : ``Client``, auto_moderation_rule: ``AutoModerationRule``)
        Called when an auto moderation rule is deleted.
    
    auto_moderation_rule_update(client: ``Client``, auto_moderation_rule: ``AutoModerationRule``, 
            old_attributes: {`None`, `dict`})
        Called when an auto moderation rule is updated.
        
        If the rule is not cached `old_attributes` will be `None` instead of the overwritten attributes in
        `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +-------------------------------+-----------------------------------------------------------+
        | Keys                          | Values                                                    |
        +===============================+===========================================================+
        | actions                       | `None`, `tuple` of ``AutoModerationAction``               |
        +-------------------------------+-----------------------------------------------------------+
        | enabled                       | `bool`                                                    |
        +-------------------------------+-----------------------------------------------------------+
        | event_type                    | ``AutoModerationEventType``                               |
        +-------------------------------+-----------------------------------------------------------+
        | excluded_channel_ids          | `None`, `tuple` of `int`                                  |
        +-------------------------------+-----------------------------------------------------------+
        | excluded_role_ids             | `None`, `tuple` of `int`                                  |
        +-------------------------------+-----------------------------------------------------------+
        | name                          | `str`                                                     |
        +-------------------------------+-----------------------------------------------------------+
        | trigger_metadata              | ``AutoModerationRuleTriggerMetadata``                     |
        +-------------------------------+-----------------------------------------------------------+
        | trigger_type                  | ``AutoModerationRuleTriggerType``                         |
        +-------------------------------+-----------------------------------------------------------+
    
    channel_create(client: ``Client``, channel: ``Channel``)
        Called when a channel is created.
        
        > This event is not called when a private channel is created.
    
    channel_delete(client: ``Client``, channel: ``Channel``)
        Called when a channel is deleted.
    
    channel_update(client: ``Client``, channel: ``Channel``, old_attributes: {`dict`, `None`})
        Called when a channel is updated. The passed `old_attributes` parameter contains the channel's overwritten
        attributes in `attribute-name` - `old-value` relation.
        
        If the channel is uncached, but is updated, `old_attributes` will be given as `None`. This can happen when a
        thread is unarchived.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +---------------------------------------+-----------------------------------------------------------+
        | Keys                                  | Values                                                    |
        +=======================================+===========================================================+
        | applied_tag_ids                       | `None`, `tuple` of `int`                                  |
        +---------------------------------------+-----------------------------------------------------------+
        | archived                              | `bool`                                                    |
        +---------------------------------------+-----------------------------------------------------------+
        | archived_at                           | `None`, `datetime`                                        |
        +---------------------------------------+-----------------------------------------------------------+
        | auto_archive_after                    | `int`                                                     |
        +---------------------------------------+-----------------------------------------------------------+
        | available_tags                        | ``ForumTagChange``                                        |
        +---------------------------------------+-----------------------------------------------------------+
        | bitrate                               | `int`                                                     |
        +---------------------------------------+-----------------------------------------------------------+
        | default_forum_layout                  | ``ForumLayout``                                           |
        +---------------------------------------+-----------------------------------------------------------+
        | default_sort_order                    | ``SortOrder``                                             |
        +---------------------------------------+-----------------------------------------------------------+
        | default_thread_auto_archive_after     | `int`                                                     |
        +---------------------------------------+-----------------------------------------------------------+
        | default_thread_reaction               | `None`, ``Emoji``                                         |
        +---------------------------------------+-----------------------------------------------------------+
        | default_thread_slowmode               | `int`                                                     |
        +---------------------------------------+-----------------------------------------------------------+
        | flags                                 | ``ChannelFlag``                                           |
        +---------------------------------------+-----------------------------------------------------------+
        | icon                                  | ``Icon``                                                  |
        +---------------------------------------+-----------------------------------------------------------+
        | invitable                             | `bool`                                                    |
        +---------------------------------------+-----------------------------------------------------------+
        | metadata                              | ``ChannelMetadataBase``                                   |
        +---------------------------------------+-----------------------------------------------------------+
        | name                                  | `str`                                                     |
        +---------------------------------------+-----------------------------------------------------------+
        | nsfw                                  | `bool`                                                    |
        +---------------------------------------+-----------------------------------------------------------+
        | open                                  | `bool`                                                    |
        +---------------------------------------+-----------------------------------------------------------+
        | owner_id                              | `int`                                                     |
        +---------------------------------------+-----------------------------------------------------------+
        | parent_id                             | `int`                                                     |
        +---------------------------------------+-----------------------------------------------------------+
        | permission_overwrites                 | `None`, `dict` of (`int`, ``PermissionOverwrite``) items  |
        +---------------------------------------+-----------------------------------------------------------+
        | position                              | `int`                                                     |
        +---------------------------------------+-----------------------------------------------------------+
        | region                                | `None`, ``VoiceRegion``                                   |
        +---------------------------------------+-----------------------------------------------------------+
        | slowmode                              | `int`                                                     |
        +---------------------------------------+-----------------------------------------------------------+
        | topic                                 | `None`, `str`                                             |
        +---------------------------------------+-----------------------------------------------------------+
        | type                                  | ``ChannelType``                                           |
        +---------------------------------------+-----------------------------------------------------------+
        | user_limit                            | `int`                                                     |
        +---------------------------------------+-----------------------------------------------------------+
        | video_quality_mode                    | ``VideoQualityMode``                                      |
        +---------------------------------------+-----------------------------------------------------------+
    
    channel_group_user_add(client: ``Client``, channel: ``Channel``, user: ``ClientUserBase``):
        Called when a user is added to a group channel.
    
    channel_group_user_delete(client: ``Client``, channel: ``Channel``, user: ``ClientUserBase``):
        Called when a user is removed from a group channel.
    
    channel_pin_update(client: ``Client``, channel: ``Channel``):
        Called when a channel's pins are updated.
    
    client_update(client: ``Client``, old_attributes: `dict`):
        Called when the client is updated. The passed `old_attributes` parameter contains the client's overwritten
        attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +-----------------------+-----------------------+
        | Keys                  | Values                |
        +=======================+=======================+
        | avatar                | ``Icon``              |
        +-----------------------+-----------------------+
        | avatar_decoration     | ``Icon``              |
        +-----------------------+-----------------------+
        | banner                | ``Icon``              |
        +-----------------------+-----------------------+
        | banner_color          | `None`, ``Color``     |
        +-----------------------+-----------------------+
        | discriminator         | `int`                 |
        +-----------------------+-----------------------+
        | display_name          | `None`, `str`         |
        +-----------------------+-----------------------+
        | email                 | `None`, `str`         |
        +-----------------------+-----------------------+
        | email_verified        | `bool`                |
        +-----------------------+-----------------------+
        | flags                 | ``UserFlag``          |
        +-----------------------+-----------------------+
        | locale                | ``Locale``            |
        +-----------------------+-----------------------+
        | mfa                   | `bool`                |
        +-----------------------+-----------------------+
        | name                  | `str                  |
        +-----------------------+-----------------------+
        | premium_type          | ``PremiumType``       |
        +-----------------------+-----------------------+
    
    embed_update(client: ``Client``, message: ``Message``, change_state: `int`):
        Called when a message is not updated, only it's embeds are updated.
        
        Possible `change_state` values:
        
        +---------------------------+-------+
        | Respective name           | Value |
        +===========================+=======+
        | EMBED_UPDATE_NONE         | 0     |
        +---------------------------+-------+
        | EMBED_UPDATE_SIZE_UPDATE  | 1     |
        +---------------------------+-------+
        | EMBED_UPDATE_EMBED_ADD    | 2     |
        +---------------------------+-------+
        | EMBED_UPDATE_EMBED_REMOVE | 3     |
        +---------------------------+-------+
        
        At the case of `EMBED_UPDATE_NONE` the event is of course not called.
    
    embedded_activity_create(client: ``Client``, embedded_activity_state: ``EmbeddedActivityState``)
        Called when an embedded activity is created.
    
    embedded_activity_delete(client: ``Client``, embedded_activity_state: ``EmbeddedActivityState``)
        Called when an embedded activity is deleted (all users left).
    
    embedded_activity_update(client: ``Client``, embedded_activity_state: ``EmbeddedActivityState``,
            old_attributes: `dict`)
        Called when an embedded activity is updated. The passed `old_attributes` parameter contains the old states of
        the respective activity in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +-------------------+-----------------------------------+
        | Keys              | Values                            |
        +===================+===================================+
        | assets            | `None`, ``ActivityAssets``        |
        +-------------------+-----------------------------------+
        | created_at        | `datetime`                        |
        +-------------------+-----------------------------------+
        | details           | `None`, `str`                     |
        +-------------------+-----------------------------------+
        | flags             | ``ActivityFlag``                  |
        +-------------------+-----------------------------------+
        | name              | `str`                             |
        +-------------------+-----------------------------------+
        | metadata          | ``ActivityMetadataBase``          |
        +-------------------+-----------------------------------+
        | party             | `None`, ``ActivityParty``         |
        +-------------------+-----------------------------------+
        | secrets           | `None`, ``ActivitySecrets``       |
        +-------------------+-----------------------------------+
        | session_id        | `None`, `str`                     |
        +-------------------+-----------------------------------+
        | state             | `None`, `str`                     |
        +-------------------+-----------------------------------+
        | sync_id           | `None`, `str`                     |
        +-------------------+-----------------------------------+
        | timestamps        | `None`, `ActivityTimestamps``     |
        +-------------------+-----------------------------------+
        | url               | `None`, `str`                     |
        +-------------------+-----------------------------------+
        
    embedded_activity_user_add(client: ``Client``, embedded_activity_state: ``EmbeddedActivityState``,
            user_id: `int`)
        Called when a user joins an embedded activity. It is not called for the person(s) creating the activity.
        
    embedded_activity_user_delete(client: ``Client``, embedded_activity_state: ``EmbeddedActivityState``,
            user_id: `int`)
        Called when a user leaves / is removed from an embedded activity.
    
    emoji_create(client: ``Client``, emoji: ``Emoji``):
        Called when an emoji is created at a guild.
    
    emoji_delete(client: ``Client``, emoji: ``Emoji``):
        Called when an emoji is deleted.
        
        Deleted emoji's `.guild` attribute is set to `None`.
        
    emoji_update(client : Client, emoji: ``Emoji``, old_attributes: `dict`):
        Called when an emoji is updated. The passed `old_attributes` parameter contains the emoji's overwritten
        attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +-------------------+-------------------------------+
        | Keys              | Values                        |
        +===================+===============================+
        | animated          | `bool`                        |
        +-------------------+-------------------------------+
        | available         | `bool`                        |
        +-------------------+-------------------------------+
        | managed           | `bool`                        |
        +-------------------+-------------------------------+
        | name              | `int`                         |
        +-------------------+-------------------------------+
        | require_colons    | `bool`                        |
        +-------------------+-------------------------------+
        | role_ids          | `None`, `tuple` of `int`      |
        +-------------------+-------------------------------+
    
    error(client: ``Client``, name: `str`, err: `object`):
        Called when an unexpected error happens. Mostly the user itself should define where it is called, because
        it is not Discord event bound, but an internal event.
        
        The `name` parameter should be a `str` what tell where the error occurred, and `err` should be a `BaseException`
        instance or an error message (can be other as type `str` as well.)
        
        > This event has a default handler called ``default_error_event_handler``, which writes the error message to
        > `sys.stderr`.
    
    gift_update(client: ``Client``, gift: ``Gift``):
        Called when a gift code is sent to a channel.
    
    guild_ban_add(client: ``Client``, guild: ``Guild``, user: ``ClientUserBase``):
        Called when a user is banned from a guild.
    
    guild_ban_delete(client: ``Client``, guild: ``Guild``, user: ``ClientUserBase``):
        Called when a user is unbanned at a guild.
    
    guild_create(client: ``Client``, guild: ``Guild``):
        Called when a client joins or creates a guild.
    
    guild_delete(client: ``Client``, guild: ``Guild``, guild_profile: {`None`, ``GuildProfile``}):
        Called when the guild is deleted or just the client left (kicked or banned as well) from it. The `profile`
        parameter is the client's respective guild profile for the guild.
    
    guild_update(client: ``Client``, guild: ``Guild``, old_attributes: `dict`):
        Called when a guild is updated. The passed `old_attributes` parameter contains the guild's overwritten attributes
        in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +-------------------------------+---------------------------------------+
        | Keys                          | Values                                |
        +===============================+=======================================+
        | afk_channel_id                | `int`                                 |
        +-------------------------------+---------------------------------------+
        | afk_timeout                   | `int`                                 |
        +-------------------------------+---------------------------------------+
        | available                     | `bool`                                |
        +-------------------------------+---------------------------------------+
        | banner                        | ``Icon``                              |
        +-------------------------------+---------------------------------------+
        | boost_count                   | `int`                                 |
        +-------------------------------+---------------------------------------+
        | boost_progress_bar_enabled    | `bool`                                |
        +-------------------------------+---------------------------------------+
        | content_filter                | ``ContentFilterLevel``                |
        +-------------------------------+---------------------------------------+
        | description                   | `None`, `str`                         |
        +-------------------------------+---------------------------------------+
        | discovery_splash              | ``Icon``                              |
        +-------------------------------+---------------------------------------+
        | features                      | `None`, `tuple` of ``GuildFeature``   |
        +-------------------------------+---------------------------------------+
        | hub_type                      | ``HubType``                           |
        +-------------------------------+---------------------------------------+
        | icon                          | ``Icon``                              |
        +-------------------------------+---------------------------------------+
        | invite_splash                 | ``Icon``                              |
        +-------------------------------+---------------------------------------+
        | max_presences                 | `int`                                 |
        +-------------------------------+---------------------------------------+
        | max_stage_channel_video_users | `int`                                 |
        +-------------------------------+---------------------------------------+
        | max_users                     | `int`                                 |
        +-------------------------------+---------------------------------------+
        | max_voice_channel_video_users | `int`                                 |
        +-------------------------------+---------------------------------------+
        | message_notification          | ``MessageNotificationLevel``          |
        +-------------------------------+---------------------------------------+
        | mfa                           | ``MFA``                               |
        +-------------------------------+---------------------------------------+
        | name                          | `str`                                 |
        +-------------------------------+---------------------------------------+
        | nsfw_level                    | ``NsfwLevel``                         |
        +-------------------------------+---------------------------------------+
        | owner_id                      | `int`                                 |
        +-------------------------------+---------------------------------------+
        | preferred_locale              | ``Locale``                            |
        +-------------------------------+---------------------------------------+
        | premium_tier                  | `int`                                 |
        +-------------------------------+---------------------------------------+
        | public_updates_channel_id     | `int`                                 |
        +-------------------------------+---------------------------------------+
        | rules_channel_id              | `int`                                 |
        +-------------------------------+---------------------------------------+
        | safety_alerts_channel_id      | `int`                                 |
        +-------------------------------+---------------------------------------+
        | system_channel_id             | `int`                                 |
        +-------------------------------+---------------------------------------+
        | system_channel_flags          | ``SystemChannelFlag``                 |
        +-------------------------------+---------------------------------------+
        | vanity_code                   | `None`, `str`                         |
        +-------------------------------+---------------------------------------+
        | verification_level            | ``VerificationLevel``                 |
        +-------------------------------+---------------------------------------+
        | widget_channel_id             | `int`                                 |
        +-------------------------------+---------------------------------------+
        | widget_enabled                | `bool`                                |
        +-------------------------------+---------------------------------------+
    
    guild_join_request_create(client: ``Client``, join_request: ``GuildJoinRequest``)
        Called when a user completes the verification screen of the guild, which needs an approval.
    
    guild_join_request_delete(client: ``Client``, event: ``GuildJoinRequestDeleteEvent``)
        Called when a user leaves from a guild before completing it's verification screen.
        
        > ``.guild_user_delete`` is called as well.
    
    guild_join_request_update(client: ``Client``, join_request: ``GuildJoinRequest``)
        Called when a completed verification screen is updated (approved, denied and such).
    
    guild_user_add(client: ``Client``, guild: ``Guild``, user: ``ClientUserBase``):
        Called when a user joins a guild.
    
    guild_user_chunk(client: ``Client``, event: GuildUserChunkEvent):
        Called when a client receives a chunk of users from Discord requested by through it's gateway.
        
        The event has a default handler called ``ChunkWaiter``.
    
    guild_user_delete(client: ``Client``, guild: ``Guild``, user: ``ClientUserBase``, \
            profile: ``GuildProfile``):
        Called when a user left (kicked or banned counts as well) from a guild. The `profile` parameter is the user's
        respective guild profile for the guild.
    
    guild_user_update(client : Client, guild: ``Guild``, user: ``ClientUserBase``, old_attributes: `dict`):
        Called when a user's ``GuildProfile`` is updated. The passed `old_attributes` parameter contains the
        guild profile's overwritten attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +-------------------+-------------------------------+
        | Keys              | Values                        |
        +===================+===============================+
        | avatar            | ``Icon``                      |
        +-------------------+-------------------------------+
        | boosts_since      | `None`, `datetime`            |
        +-------------------+-------------------------------+
        | flags             | `None`, ``GuildProfileFlags`` |
        +-------------------+-------------------------------+
        | nick              | `None`, `str`                 |
        +-------------------+-------------------------------+
        | pending           | `bool`                        |
        +-------------------+-------------------------------+
        | role_ids          | `None`, `tuple` of `int`      |
        +-------------------+-------------------------------+
        | timed_out_until   | `None`, `datetime`            |
        +-------------------+-------------------------------+
    
    integration_create(client: ``Client``, guild: ``Guild``, integration: ``Integration``):
        Called when an integration is created inside of a guild. Includes cases when bots are added to the guild as
        well.
    
    integration_delete(client: ``Client``, guild: ``Guild``, integration_id: `int`, \
            application_id: {`None`, `int`}):
        Called when a guild has one of it's integrations deleted. If the integration is bound to an application, like
        a bot, then `application_id` is given as `int`.
    
    integration_update(client: ``Client``, guild: ``Guild``, integration: ``Integration``):
        Called when an integration is updated inside of a guild.
    
    integration_update(client: ``Client``, guild: ``Guild``):
        Called when an ``Integration`` of a guild is updated.
        
        > No integration data is included with the received dispatch event, so it cannot be passed to the event
        > handler either.
    
    interaction_create(client: ``Client``, event: ``InteractionEvent``)
        Called when a user interacts with an application command.
    
    invite_create(client: ``Client``, invite: Invite):
        Called when an invite is created  at a guild.
    
    invite_delete(client: ``Client``, invite: Invite):
        Called when an invite is deleted at a guild.
    
    launch(client : ``Client``):
        called when the client is launched up and the first ready dispatch event is received.
    
    message_create(client: ``Client``, message: ``Message``):
        Called when a message is sent to any of the client's text channels.
    
    message_delete(client: ``Client``, message: ``Message``):
        Called when a loaded message is deleted.
    
    message_update(client: ``Client``, message: ``Message``, old_attributes: {`None`, `dict`}):
        Called when a loaded message is updated. The passed `old_attributes` parameter contains the message's overwritten
        attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +-----------------------------------+-----------------------------------------------------------------------+
        | Keys                              | Values                                                                |
        +===================================+=======================================================================+
        | attachments                       | `None`, `tuple` of ``Attachment``                                     |
        +-----------------------------------+-----------------------------------------------------------------------+
        | call                              | `None`, ``MessageCall``                                               |
        +-----------------------------------+-----------------------------------------------------------------------+
        | components                        | `None`, `tuple` of ``Component``                                      |
        +-----------------------------------+-----------------------------------------------------------------------+
        | content                           | `None`, `str`                                                         |
        +-----------------------------------+-----------------------------------------------------------------------+
        | edited_at                         | `None`, `datetime`                                                    |
        +-----------------------------------+-----------------------------------------------------------------------+
        | embeds                            | `None`, `tuple` of ``Embed``                                          |
        +-----------------------------------+-----------------------------------------------------------------------+
        | flags                             | `UserFlag`                                                            |
        +-----------------------------------+-----------------------------------------------------------------------+
        | pinned                            | `bool`                                                                |
        +-----------------------------------+-----------------------------------------------------------------------+
        | mentioned_channels_cross_guild    | `None`, `tuple` of ``Channel``                                        |
        +-----------------------------------+-----------------------------------------------------------------------+
        | mentioned_everyone                | `bool`                                                                |
        +-----------------------------------+-----------------------------------------------------------------------+
        | mentioned_role_ids                | `None`, `tuple` of `int`                                              |
        +-----------------------------------+-----------------------------------------------------------------------+
        | mentioned_users                   | `None`, `tuple` of ``ClientUserBase``                                 |
        +-----------------------------------+-----------------------------------------------------------------------+
        
        A special case is if a message is (un)pinned or (un)suppressed, because then the `old_attributes` parameter is
        not going to contain `edited`, only `pinned`, `flags`. If the embeds are (un)suppressed of the message, then
        `old_attributes` might contain also `embeds`.
        
        > If the message is partial (usually when it is not cached), `old_attributes` is passed as `None`.
    
    reaction_add(client: ``Client``, event: ``ReactionAddEvent``):
        Called when a user reacts on a message with the given emoji.
    
    reaction_clear(client: ``Client``, message: ``Message``, reactions: {`None`, ``ReactionMapping``}):
        Called when the reactions of a message are cleared. The passed `old_reactions` parameter are the old reactions
        of the message.
        
        > If the message is partial (usually when it is not cached), `reactions` is passed as `None`.
    
    reaction_delete(client: ``Client``, event: ``ReactionDeleteEvent``):
        Called when a user removes it's reaction from a message.
    
    reaction_delete_emoji(client: ``Client``, message: ``Message``, users: {`None`, ``ReactionMappingLine``}):
        Called when all the reactions of a specified emoji are removed from a message. The passed `users` parameter
        are the old reactor users of the given emoji.
        
        > If the message is partial (usually when it is not cached), `users` is passed as `None`.
    
    ready(client: ``Client``):
        Called when the client finishes logging in. The event might be called more times, because the clients might
        dis- and reconnect.
    
    relationship_add(client: ``Client``, new_relationship: ``Relationship``):
        Called when the client gets a new relationship independently from it's type.
    
    relationship_change(client: ``Client``, old_relationship: ``Relationship``, new_relationship: ``Relationship``):
        Called when one of the client's relationships change.
    
    relationship_delete(client: ``Client``, old_relationship: ``Relationship``):
        Called when a relationship of a client is removed.
    
    role_create(client: ``Client``, role: ``Role``):
        Called when a role is created at a guild.
    
    role_delete(client: ``Client``, role: ``Role``):
        Called when a role is deleted from a guild.
    
    role_update(client: ``Client``, role: ``Role``, old_attributes: `dict`):
        Called when a role is updated.
        
        Every item in `old_attributes` is optional and they can be any of the following:
        
        +---------------+-----------------------+
        | Keys          | Values                |
        +===============+=======================+
        | color         | ``Color``             |
        +---------------+-----------------------+
        | icon          | ``Icon``              |
        +---------------+-----------------------+
        | flags         | ``RoleFlag``          |
        +---------------+-----------------------+
        | managed       | `bool`                |
        +---------------+-----------------------+
        | mentionable   | `bool`                |
        +---------------+-----------------------+
        | name          | `str`                 |
        +---------------+-----------------------+
        | permissions   | ``Permission``        |
        +---------------+-----------------------+
        | position      | `int`                 |
        +---------------+-----------------------+
        | separated     | `bool`                |
        +---------------+-----------------------+
        | unicode_emoji | `None`, ``Emoji``     |
        +---------------+-----------------------+
    
    scheduled_event_create(client: ``Client``, scheduled_event: ``ScheduledEvent``):
        Called when a scheduled event is created.
    
    scheduled_event_delete(client: ``Client``, scheduled_event: ``ScheduledEvent``):
        Called when a scheduled event is deleted.
    
    scheduled_event_update(client: ``Client``, scheduled_event: ``ScheduledEvent``, old_attributes: `None | dict`):
        Called when a scheduled event is updated.
        
        If the scheduled event is cached, `old_attributes` will be a dictionary including the changed attributes in
        `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional any can be any of the following:
        
        +---------------------------+-----------------------------------------------+
        | Key                       | Value                                         |
        +===========================+===============================================+
        | channel_id                | `int`                                         |
        +---------------------------+-----------------------------------------------+
        | description               | `None`, `str`                                 |
        +---------------------------+-----------------------------------------------+
        | end                       | `None`, `datetime`                            |
        +---------------------------+-----------------------------------------------+
        | entity_id                 | `int`                                         |
        +---------------------------+-----------------------------------------------+
        | entity_metadata           | ``ScheduledEventEntityMetadataBase``          |
        +---------------------------+-----------------------------------------------+
        | entity_type               | ``ScheduledEventEntityType``                  |
        +---------------------------+-----------------------------------------------+
        | image                     | ``Icon``                                      |
        +---------------------------+-----------------------------------------------+
        | name                      | `str`                                         |
        +---------------------------+-----------------------------------------------+
        | privacy_level             | ``PrivacyLevel``                              |
        +---------------------------+-----------------------------------------------+
        | sku_ids                   | `None`, `tuple` of `int`                      |
        +---------------------------+-----------------------------------------------+
        | start                     | `None`, `datetime`                            |
        +---------------------------+-----------------------------------------------+
        | status                    | ``ScheduledEventStatus``                      |
        +---------------------------+-----------------------------------------------+
    
    scheduled_event_user_subscribe(client: ``Client``, event: ``ScheduledEventSubscribeEvent``):
        Called when a user subscribes to a scheduled event.
    
    scheduled_event_user_unsubscribe(client: ``Client``, event: ``ScheduledEventUnsubscribeEvent``):
        Called when a user unsubscribes from a scheduled event.
    
    shutdown(client : ``Client``):
        Called when ``Client.stop``, ``Client.disconnect`` is called indicating, that the client is logging off and
        all data should be saved if needed.
    
    soundboard_sound_create(client : ``Client``, sound : ``SoundboardSound``)
        Called when a soundboard sound is created.
    
    soundboard_sound_delete(client : ``Client``, sound : ``SoundboardSound``)
        Called when a soundboard sound is deleted.
    
    soundboard_sound_update(client : ``Client``, sound : ``SoundboardSound``, old_attributes : `None | dict`)
        Called when a soundboard sound is updated.
    
        If the soundboard sound is cached, `old_attributes` will be a dictionary including the changed attributes in
        `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional any can be any of the following:
        
        +-----------+-------------------+
        | Keys      | Values            |
        +===========+===================+
        | available | `bool`            |
        +-----------+-------------------+
        | emoji     | `None`, ``Emoji`` |
        +-----------+-------------------+
        | name      | `str`             |
        +-----------+-------------------+
        | volume    | `float`           |
        +-----------+-------------------+
    
    soundboard_sounds(client : ``Client``, event : ``SoundboardSoundsEvent``)
        Called after a soundboard sounds request.
        
        > This event has a default handler defined,.
    
    stage_create(client : ``Client``, stage : ``Stage``):
        Called when a stage is created.
    
    stage_delete(client : ``Client``, stage : ``Stage``):
        Called when a stage is deleted.
    
    stage_update(client : ``Client``, stage : ``Stage``, old_attributes : `None | dict`):
        Called when a stage is updated.
        
        If the stage is cached, `old_attributes` will be a dictionary including the changed attributes in
        `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and they can be any of the following:
        
        +---------------+-----------------------+
        | Keys          | Values                |
        +===============+=======================+
        | discoverable  | `bool`                |
        +---------------+-----------------------+
        | invite_code   | `None`, `str`         |
        +---------------+-----------------------+
        | privacy_level | ``PrivacyLevel``      |
        +---------------+-----------------------+
        | topic         | `None`, `str`         |
        +---------------+-----------------------+
    
    sticker_create(client: ``Client``, sticker: ``Sticker``):
        Called when an sticker is created at a guild.
    
    sticker_delete(client: ``Client``, sticker: ``Sticker``):
        Called when an sticker is deleted.
    
    sticker_update(client : Client, sticker: ``Sticker``, old_attributes: `dict`):
        Called when an sticker is updated. The passed `old_attributes` parameter contains the sticker's overwritten
        attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +-----------------------+-----------------------------------+
        | Keys                  | Values                            |
        +=======================+===================================+
        | available             | `bool`                            |
        +-----------------------+-----------------------------------+
        | description           | `None`, `str`                     |
        +-----------------------+-----------------------------------+
        | name                  | `str`                             |
        +-----------------------+-----------------------------------+
        | sort_value            | `int`                             |
        +-----------------------+-----------------------------------+
        | tags                  | `None`  or `frozenset` of `str`   |
        +-----------------------+-----------------------------------+
    
    thread_user_add(client : ``Client``, thread_channel: ``Channel``, user: ``ClientUserBase``):
        Called when a user is added or joined a thread channel.
    
    thread_user_delete(client : ``Client``, thread_channel: ``Channel``, user: ``ClientUserBase``, \
            thread_profile: ``ThreadProfile``):
        Called when a user is removed or left a thread channel.
    
    thread_user_update(client : ``Client``, thread_channel: ``Channel``, user: ``ClientUserBase``, \
            old_attributes: `dict`):
        Called when a user's thread profile is updated. The passed `old_attributes` parameter contains the
        thread profile's overwritten attributes in `attribute-name` - `old-value` relation.
        
        > Note that this event is limited only to the respective client and is not triggered for other users.
        
        Every item in `old_attributes` is optional they can be any of the following:
        
        +-------------------+-------------------------------+
        | Keys              | Values                        |
        +===================+===============================+
        | flags             | ``ThreadProfileFlag``         |
        +-------------------+-------------------------------+
    
    typing(client: ``Client``, channel: ``Channel``, user: ``ClientUserBase``, timestamp: `datetime`):
        Called when a user is typing at a channel. The `timestamp` parameter represents when the typing started.
        
        However a typing requests stands for 8 seconds, but the official Discord client usually just spams it.
    
    unknown_dispatch_event(client: ``Client``, name: `str`, data: `object`):
        Called when an unknown dispatch event is received.
    
    user_update(client: ``Client``, user: ``ClientUserBase``, old_attributes: `dict`):
        Called when a user is updated This event not includes guild profile changes. The passed `old_attributes`
        parameter contains the user's overwritten attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional they can be any of the following:
        
        +-----------------------+-----------------------+
        | Keys                  | Values                |
        +=======================+=======================+
        | avatar                | ``Icon``              |
        +-----------------------+-----------------------+
        | avatar_decoration     | ``Icon``              |
        +-----------------------+-----------------------+
        | banner                | ``Icon``              |
        +-----------------------+-----------------------+
        | banner_color          | `None`, ``Color``     |
        +-----------------------+-----------------------+
        | discriminator         | `int`                 |
        +-----------------------+-----------------------+
        | display_name          | `None`, `str`         |
        +-----------------------+-----------------------+
        | email                 | `None`, `str`         |
        +-----------------------+-----------------------+
        | email_verified        | `bool`                |
        +-----------------------+-----------------------+
        | flags                 | ``UserFlag``          |
        +-----------------------+-----------------------+
        | locale                | ``Locale``            |
        +-----------------------+-----------------------+
        | mfa                   | `bool`                |
        +-----------------------+-----------------------+
        | name                  | `str`                 |
        +-----------------------+-----------------------+
        | premium_type          | ``PremiumType``       |
        +-----------------------+-----------------------+
    
    user_presence_update(client: ``Client``, user: ``ClientUserBase``, old_attributes: `dict`):
        Called when a user's presence is updated.
        
        The passed `old_attributes` parameter contain the user's changed presence related attributes in
        `attribute-name` - `old-value` relation. An exception from this is `activities`, because that is a
        ``ActivityChange`` containing all the changes of the user's activities.
        
        +---------------+-----------------------------------+
        | Keys          | Values                            |
        +===============+===================================+
        | activities    | ``ActivityChange``                |
        +---------------+-----------------------------------+
        | status        | ``Status``                        |
        +---------------+-----------------------------------+
        | statuses      | `dict` of (`str`, `str`) items    |
        +---------------+-----------------------------------+
    
    user_voice_join(client: ``Client``, voice_state: ``VoiceState``)
        Called when a user joins a voice channel.
    
    user_voice_leave(client: ``client``, voice_state: ``VoiceState``, old_channel_id : `int`)
        Called when a user leaves from a voice channel.
    
    user_voice_move(client: ``Client``, voice_state: ``VoiceState``, old_channel_id : `int`)
        Called when a user moves between two voice channels
    
    user_voice_update(client: ``Client``, voice_state: ``VoiceState``, old_attributes: `dict`):
        Called when a voice state of a user is updated.
        
        Every item in `old_attributes` is optional and they can be the following:
        
        +-----------------------+-----------------------+
        | Keys                  | Values                |
        +=======================+=======================+
        | deaf                  | `str`                 |
        +-----------------------+-----------------------+
        | mute                  | `bool`                |
        +-----------------------+-----------------------+
        | requested_to_speak_at | `None`, `datetime`    |
        +-----------------------+-----------------------+
        | self_deaf             | `bool`                |
        +-----------------------+-----------------------+
        | self_mute             | `bool`                |
        +-----------------------+-----------------------+
        | self_stream           | `bool`                |
        +-----------------------+-----------------------+
        | self_video            | `bool`                |
        +-----------------------+-----------------------+
        | speaker               | `bool`                |
        +-----------------------+-----------------------+
    
    voice_channel_effect(client : ``Client``, event : ``VoiceChannelEffect``)
        Called when a user invokes (or sends) a voice channel effect.
    
    voice_client_join(client : ``Client``, voice_state : ``VoiceState``)
        Called when the client join a voice channel.
        
        > This event has a default handler defined, which is used by hata's ``VoiceClient``.
        >
        > When using 3rd party voice library, make sure to register your by passing `overwrite=True` parameter as well.
    
    voice_client_ghost(client : ``Client``, voice_state : ``VoiceState``)
        Called when the client has a voice state in a channel, when logging in.
        
        > This event has a default handler defined, which is used by hata's ``VoiceClient``.
        >
        > When using 3rd party voice library, make sure to register your by passing `overwrite=True` parameter as well.
    
    voice_client_leave(client : ``Client``, voice_state : ``VoiceState``, old_channel_id : `int`)
        Called when the client leaves / is removed fro ma voice channel.
        
        > This event has a default handler defined, which is used by hata's ``VoiceClient``.
        >
        > When using 3rd party voice library, make sure to register your by passing `overwrite=True` parameter as well.
    
    voice_client_move(client : ``Client``, voice_state : ``VoiceState``, old_channel_id : `int`)
        Called when the client moves / is moved between two channels.
        
        > This event has a default handler defined, which is used by hata's ``VoiceClient``.
        >
        > When using 3rd party voice library, make sure to register your by passing `overwrite=True` parameter as well.
    
    voice_client_shutdown(client : ``Client``)
        Called when the client disconnects. Should be used to disconnect the client's voice clients.
    
        > This event has a default handler defined, which is used by hata's ``VoiceClient``.
        >
        > When using 3rd party voice library, make sure to register your by passing `overwrite=True` parameter as well.
    
    voice_client_update(client : ``Client``, voice_state : ``VoiceState``, old_attributes : `dict`)
        Called when the client's state is updated.
        
        > This event has a default handler defined, which is used by hata's ``VoiceClient``.
        >
        > When using 3rd party voice library, make sure to register your by passing `overwrite=True` parameter as well.
        
        Every item in `old_attributes` is optional and they can be the following:
        
        +-----------------------+-----------------------+
        | Keys                  | Values                |
        +=======================+=======================+
        | deaf                  | `str`                 |
        +-----------------------+-----------------------+
        | mute                  | `bool`                |
        +-----------------------+-----------------------+
        | requested_to_speak_at | `None`, `datetime`    |
        +-----------------------+-----------------------+
        | self_deaf             | `bool`                |
        +-----------------------+-----------------------+
        | self_mute             | `bool`                |
        +-----------------------+-----------------------+
        | self_stream           | `bool`                |
        +-----------------------+-----------------------+
        | self_video            | `bool`                |
        +-----------------------+-----------------------+
        | speaker               | `bool`                |
        +-----------------------+-----------------------+
        
        > This event has a default handler defined, which is used by hata's ``VoiceClient``.
        >
        > When using 3rd party voice library, make sure to register your by passing `overwrite=True` parameter as well.
    
    voice_server_update(client: ``Client``, event: ``VoiceServerUpdateEvent``)
        Called initially when the client connects to a voice channels of a guild. Also called when a guild's voice
        server is updated.
        
        > This event has a default handler defined, which is used by hata's ``VoiceClient``.
        >
        > When using 3rd party voice library, make sure to register your by passing `overwrite=True` parameter as well.
    
    webhook_update(client: ``Client``, event: ``WebhookUpdateEvent``):
        Called when a webhook of a channel is updated.
    """
    __slots__ = (*EVENT_HANDLER_ATTRIBUTES, *EVENT_HANDLER_NAMES)
    
    def __init__(self, client):
        """
        Creates an ``EventHandlerManager`` for the given client.
        
        Parameters
        ----------
        client : ``Client``
        """
        client_reference = WeakReferer(client)
        
        object.__setattr__(self, 'client_reference', client_reference)
        object.__setattr__(self, '_plugins', None)
        object.__setattr__(self, '_plugin_events', None)
        
        for name in EVENT_HANDLER_NAME_TO_PARSER_NAMES:
            object.__setattr__(self, name, DEFAULT_EVENT_HANDLER)
        
        object.__setattr__(self, '_launch_called', False)
        
        for event_handler_name, event_handler, instance_event_handler in DEFAULT_EVENT_HANDLERS:
            if instance_event_handler:
                event_handler = event_handler()
            object.__setattr__(self, event_handler_name, event_handler)
    
    
    def __call__(self, func = None, name = None, overwrite = False):
        """
        Adds the given `func` as an event handler.
        
        Parameters
        ----------
        func : `None`, `callable` = `None`, Optional
            The async callable to add as an event handler.
            
            If given as `None` will return a decorator.
        
        name : `None`, `str` = `None`, Optional
            A name to be used instead of the passed `func`'s when adding it.
        
        overwrite : `bool` = `False`, Optional
            Whether the passed `func` should overwrite the already added ones with the same name or extend them.
        
        Returns
        -------
        func : `callable`
            The added callable or `functools.partial` if `func` was not given.
        
        Raises
        ------
        LookupError
            Invalid event name.
        TypeError
            - If `func` was not given as callable.
            - If `func` is not as async and neither cannot be converted to an async one.
            - If `func` expects less or more non reserved positional parameters as `expected` is.
            - If `name` was not passed as `None` or type `str`.
        """
        if func is None:
            return partial_func(self, name = name, overwrite = overwrite)
        
        name = check_name(func, name)
        
        deprecation_state = _get_event_deprecation_state(name)
        if deprecation_state & DEPRECATION_LEVEL_REMOVED:
            return
        
        if deprecation_state & DEPRECATION_LEVEL_RENAMED_SILENT:
            name = _translate_name_deprecation_silent(name)
        
        plugin, parameter_count = get_plugin_event_handler_and_parameter_count(self, name)
        
        if plugin is None:
            raise LookupError(f'Invalid event name: {name!r}.') from None
        
        if plugin is self:
            parser_names = EVENT_HANDLER_NAME_TO_PARSER_NAMES.get(name, None)
        else:
            parser_names = None
        
        if deprecation_state & DEPRECATION_LEVEL_SHOULD_WRAP:
            func = _wrap_maybe_deprecated_event(name, func)
        
        func = check_parameter_count_and_convert(func, parameter_count, name = name)
        
        actual = getattr(plugin, name)
        
        if func is DEFAULT_EVENT_HANDLER:
            if actual is DEFAULT_EVENT_HANDLER:
                pass
            
            else:
                if overwrite:
                    object.__setattr__(plugin, name, DEFAULT_EVENT_HANDLER)
                    
                    if (parser_names is not None) and parser_names:
                        for parser_name in parser_names:
                            parser_setting = PARSER_SETTINGS[parser_name]
                            parser_setting.remove_mention(self.client_reference())
                
                else:
                    pass
        
        else:
            if actual is DEFAULT_EVENT_HANDLER:
                object.__setattr__(plugin, name, func)
                
                if (parser_names is not None) and parser_names:
                    for parser_name in parser_names:
                        parser_setting = PARSER_SETTINGS[parser_name]
                        parser_setting.add_mention(self.client_reference())
            
            else:
                if overwrite:
                    object.__setattr__(plugin, name, func)
                
                else:
                    if type(actual) is asynclist:
                        list.append(actual, func)
                    else:
                        new = asynclist()
                        list.append(new, actual)
                        list.append(new, func)
                        object.__setattr__(plugin, name, new)
        
        if self._launch_called and (name == 'launch'):
            client = self.client_reference()
            if (client is not None):
                Task(KOKORO, func(client))
        
        return func
    
    
    def clear(self):
        """
        Clears the ``EventHandlerManager`` to it's initial state.
        """
        delete = type(self).__delattr__
        for name in EVENT_HANDLER_NAME_TO_PARSER_NAMES:
            delete(self, name)
        
        for event_handler_name, event_handler, instance_event_handler in DEFAULT_EVENT_HANDLERS:
            if instance_event_handler:
                event_handler = event_handler()
            object.__setattr__(self, event_handler_name, event_handler)
    
    
    def __setattr__(self, name, value):
        """
        Sets the given event handler under the specified event name. Updates the respective event's parser(s) if
        needed.
        
        Parameters
        ----------
        name : `str`
            The name of the event.
        value : `callable`
            The event handler.
        
        Raises
        ------
        AttributeError
            The ``EventHandlerManager`` has no attribute named as the given `name`.
        """
        if name in EVENT_HANDLER_ATTRIBUTES:
            object.__setattr__(self, name, value)
            return
        
        deprecation_state = _get_event_deprecation_state(name)
        if deprecation_state & DEPRECATION_LEVEL_REMOVED:
            return
        
        if deprecation_state & DEPRECATION_LEVEL_RENAMED_SILENT:
            name = _translate_name_deprecation_silent(name)
        
        plugin, parameter_count = get_plugin_event_handler_and_parameter_count(self, name)
        
        if plugin is None:
            raise AttributeError(f'Unknown attribute: {name!r}.') from None
        
        if plugin is self:
            parser_names = EVENT_HANDLER_NAME_TO_PARSER_NAMES.get(name, None)
        else:
            parser_names = None
        
        
        if deprecation_state & DEPRECATION_LEVEL_SHOULD_WRAP:
            value = _wrap_maybe_deprecated_event(name, value)
        func = check_parameter_count_and_convert(value, parameter_count, name = name)
        
        actual = getattr(plugin, name)
        
        if func is DEFAULT_EVENT_HANDLER:
            if actual is DEFAULT_EVENT_HANDLER:
                pass
            
            else:
                object.__setattr__(plugin, name, DEFAULT_EVENT_HANDLER)
                
                if (parser_names is not None) and parser_names:
                    for parser_name in parser_names:
                        parser_setting = PARSER_SETTINGS[parser_name]
                        parser_setting.remove_mention(self.client_reference())
        
        else:
            if actual is DEFAULT_EVENT_HANDLER:
                object.__setattr__(plugin, name, func)
                
                if (parser_names is not None) and parser_names:
                    for parser_name in parser_names:
                        parser_setting = PARSER_SETTINGS[parser_name]
                        parser_setting.add_mention(self.client_reference())
            
            else:
                object.__setattr__(plugin, name, func)
        
        
        if self._launch_called and (name == 'launch'):
            client = self.client_reference()
            if (client is not None):
                Task(KOKORO, func(client))
    
    
    def __delattr__(self, name):
        """
        Removes the event handler with switching it to `DEFAULT_EVENT_HANDLER`, and updates the event's parser if
        needed.
        
        Parameters
        ----------
        name : `str`
            The name of the event.
        
        Raises
        ------
        AttributeError
            The ``EventHandlerManager`` has no attribute named as the given `name`.
        """
        deprecation_state = _get_event_deprecation_state(name)
        if deprecation_state & DEPRECATION_LEVEL_REMOVED:
            return
        
        if deprecation_state & DEPRECATION_LEVEL_RENAMED_SILENT:
            name = _translate_name_deprecation_silent(name)
        
        plugin, parser_names = get_plugin_event_handler_and_parser_names(self, name)
        if plugin is None:
            
            if name in EVENT_HANDLER_ATTRIBUTES:
                message = f'Cannot delete attribute: `{name}`.'
            else:
                message = f'Unknown attribute: `{name!r}`.'
            
            raise AttributeError(message)
        
        
        actual = getattr(plugin, name)
        if actual is DEFAULT_EVENT_HANDLER:
            return
        
        object.__setattr__(plugin, name, DEFAULT_EVENT_HANDLER)
        
        if (parser_names is not None) and parser_names:
            for parser_name in parser_names:
                parser_setting = PARSER_SETTINGS[parser_name]
                parser_setting.remove_mention(self.client_reference())
    
    
    def __getattr__(self, name):
        """
        Tries to get the attribute of a registered plugin.
        
        Parameters
        ----------
        name : `str`
            The name of the event.
        
        Returns
        -------
        event_handler : `object`
            Registered event handler if any.
        
        Raises
        ------
        AttributeError
            If non of the plugins have the given attribute.
        """
        deprecation_state = _get_event_deprecation_state(name)
        if deprecation_state & DEPRECATION_LEVEL_RENAMED_SILENT:
            name = _translate_name_deprecation_silent(name)
            try:
                return object.__getattribute__(self, name)
            except AttributeError:
                pass
        
        plugin_events = self._plugin_events
        if (plugin_events is not None):
            try:
                event_handler_plugin = plugin_events[name]
            except KeyError:
                pass
            else:
                return getattr(event_handler_plugin, name)
        
        RichAttributeErrorBaseType.__getattr__(self, name)
    
    
    def __dir__(self):
        """Returns the attributes of the event handler manager."""
        directory = object.__dir__(self)
        plugins = self._plugins
        if (plugins is not None):
            directory = set(directory)
            
            for plugin in plugins:
                directory.update(plugin._plugin_event_names)
            
            directory = sorted(directory)
        
        return directory
    
    
    def get_handler(self, name, type_):
        """
        Gets an event handler from the client's.
        
        Parameters
        ----------
        name : `str`
            The event's name.
        type_ : `type`
            The event handler's type.
        
        Returns
        -------
        event_handler : `None`, `object`
            The matched event handler if any.
        """
        plugin = get_plugin_event_handler(self, name)
        if plugin is None:
            return None
        
        try:
            actual = getattr(plugin, name)
        except AttributeError:
            return None
        
        if actual is DEFAULT_EVENT_HANDLER:
            return None
        
        if type(actual) is asynclist:
            for element in list.__iter__(actual):
                if type(element) is type_:
                    return element
        else:
            if type(actual) is type_:
                return actual
        
        return None
    
    
    def remove(self, func, name = None, by_type = False, count = -1):
        """
        Removes the given event handler from the the event descriptor.
        
        Parameters
        ----------
        func : `object`
            The event handler to remove.
        name : `None`, `str` = `None`, Optional
            The event's name.
        by_type : `bool` = `False`, Optional
            Whether `func` was given as the type of the real event handler. Defaults to `False`.
        count : `int` = `-1`, Optional
            The maximal amount of the same events to remove. Negative numbers count as unlimited. Defaults to `-1`.
        """
        if (count == 0) or (name in EVENT_HANDLER_ATTRIBUTES):
            return
        
        name = check_name(func, name)
        
        deprecation_state = _get_event_deprecation_state(name)
        if deprecation_state & DEPRECATION_LEVEL_REMOVED:
            return
        
        if deprecation_state & DEPRECATION_LEVEL_RENAMED_SILENT:
            name = _translate_name_deprecation_silent(name)
        
        plugin = get_plugin_event_handler(self, name)
        
        try:
            actual = getattr(plugin, name)
        except AttributeError:
            return
        
        if actual is DEFAULT_EVENT_HANDLER:
            return
        
        if type(actual) is asynclist:
            for index in reversed(range(list.__len__(actual))):
                element = list.__getitem__(actual, index)
                if by_type:
                    element = type(element)
                
                if element != func:
                    continue
                
                list.__delitem__(actual, index)
                count -= 1
                if count == 0:
                    break
                
                continue
            
            length = list.__len__(actual)
            if length > 1:
                return
            
            if length == 1:
                actual = list.__getitem__(actual, 0)
                object.__setattr__(plugin, name, actual)
                return
        
        else:
            if by_type:
                actual = type(actual)
            
            if actual != func:
                return
        
        object.__setattr__(plugin, name, DEFAULT_EVENT_HANDLER)
        
        if plugin is self:
            parser_names = EVENT_HANDLER_NAME_TO_PARSER_NAMES.get(name, None)
            if (parser_names is not None) and parser_names:
                for parser_name in parser_names:
                    parser_setting = PARSER_SETTINGS[parser_name]
                    parser_setting.remove_mention(self.client_reference())
        
        return
    
    
    def register_plugin(self, plugin):
        """
        Registers a plugin to the event handler manager.
        
        Parameters
        ----------
        plugin : ``EventHandlerPlugin``
            The plugin to add.
        
        Returns
        -------
        plugin : ``EventHandlerPlugin``, `type<EventHandlerPlugin>`
            The added plugin.
        
        Raises
        ------
        TypeError
            - If `plugin` is not ``EventHandlerPlugin``.
        RuntimeError
            - If an event name of the `plugin` is already defined by an other plugin.
        """
        if isinstance(plugin, EventHandlerPlugin):
            pass
        
        elif issubclass(plugin, EventHandlerPlugin):
            # Hax
            plugin = plugin()
        
        else:
            raise TypeError(
                f'`plugin` can be `{EventHandlerPlugin.__name__}`, got {plugin.__class__.__name__}; {plugin!r}.'
            )
        
        plugins = self._plugins
        if plugins is None:
            plugins = set()
            object.__setattr__(self, '_plugins', plugins)
        
        plugin_events = self._plugin_events
        event_names = plugin._plugin_event_names
        
        if (plugin_events is None):
            plugin_events = {}
            object.__setattr__(self, '_plugin_events', plugin_events)
            
        else:
            for event_name in event_names:
                try:
                    other_plugin = plugin_events[event_name]
                except KeyError:
                    pass
                else:
                    raise RuntimeError(
                        f'`{event_name!r}` of `{plugin!r}` is already defined by: `{other_plugin!r}`.'
                    )
        
        for event_name in event_names:
            plugin_events[event_name] = plugin
        
        plugins.add(plugin)
        
        return plugin
    
    
    def iter_event_names_and_handlers(self):
        """
        Iterates over all the event names and the handlers.
        
        This method is an iterable generator.
        
        Yields
        ------
        event_name : `str`
            The event's name.
        event_handler : `async-callable`
            The event's handler.
        """
        for event_name in EVENT_HANDLER_NAMES:
            for event_handler in _iterate_event_handler(getattr(self, event_name)):
                yield event_name, event_handler
        
        plugin_events = self._plugin_events
        if (plugin_events is not None):
            for event_name, event_handler_plugin in plugin_events.items():
                for event_handler in _iterate_event_handler(getattr(event_handler_plugin, event_name)):
                    yield event_name, event_handler
