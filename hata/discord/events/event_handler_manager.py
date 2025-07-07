__all__ = ()

from functools import partial as partial_func

from scarletio import RichAttributeErrorBaseType, Task, WeakReferer

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
    '_plugin_events_deprecated',
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
    #    warn(
    #        (
    #            '`Client.events.stuff` is deprecated and will be removed in 2030 jan.\n'
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
    # Currently there are no deprecations for this.
    # Here is 1 for future reference just in case:
    """
    if name == 'role_delete':
        analyzer = CallableAnalyzer(func)
        if analyzer.is_async():
            real_analyzer = analyzer
        else:
            real_analyzer = CallableAnalyzer(func.__call__, as_method = True)
        
        min_, max_ = real_analyzer.get_non_reserved_positional_parameter_range()
        if (min_ == 3) and not analyzer.accepts_args():
            warn(
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
    """
    return func


def _check_duplicate_plugin_event_name(plugin, event_name, plugin_events, plugin_deprecated_events):
    """
    Checks whether there is a duplicated event name already registered.
    
    Parameters
    ----------
    plugin : ``EventHandlerPlugin``
        The plugin we check an event name of.
    
    event_name : `str`
        The event name being checked.
    
    plugin_events : `None | dict<str, EventHandlerPlugin>`
        Already registered plugin events.
    
    plugin_deprecated_events : `None | dict<str, (EventHandlerPlugin, PluginDeprecation, str)>`
        Already registered deprecated plugin events.
    
    Raises
    ------
    RuntimeError
    """
    while True:
        if (plugin_events is not None):
            try:
                other_plugin = plugin_events[event_name]
            except KeyError:
                pass
            else:
                break
        
        if (plugin_deprecated_events is not None):
            try:
                other_plugin, deprecation = plugin_deprecated_events[event_name]
            except KeyError:
                pass
            else:
                break
        
        return
    
    raise RuntimeError(
        f'`{event_name!r}` of `{plugin!r}` is already defined by: `{other_plugin!r}`.'
    )


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
    @client.events(overwrite = True)
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
    client.events.remove(MyEventHandlerType, by_type = True)
    ```
    
    Attributes
    ----------
    _launch_called : `bool`
        Whether The respective client's `.events.launch` was called already.
    
    _plugin_events : `None | dict<str | EventHandlerPlugin>`
        Event name to plugin relation.
    
    _plugin_events_deprecated : `None | dict<str, (EventHandlerPlugin, EventDeprecation)>`
        Event name to plugin relation used for deprecated events.
    
    _plugins : `None | set<EventHandlerPlugin>`
        Plugins added to the event handler.
    
    client_reference : `WeakReferer<Client>`
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
        
        +---------------------------+-------------------------------------------------------------------+
        | Keys                      | Values                                                            |
        +===========================+===================================================================+
        | description               | `None`, `str`                                                     |
        +---------------------------+-------------------------------------------------------------------+
        | description_localizations | `None`, `dict` of (``Locale``, `str`) items                       |
        +---------------------------+-------------------------------------------------------------------+
        | handler_type              | ``ApplicationCommandHandlerType``                                 |
        +---------------------------+-------------------------------------------------------------------+
        | integration_context_types | `None`, `tuple` of ``ApplicationCommandIntegrationContextType``   |
        +---------------------------+-------------------------------------------------------------------+
        | integration_types         | `None`, `tuple` of ``ApplicationIntegrationType``                 |
        +---------------------------+-------------------------------------------------------------------+
        | name                      | `str`                                                             |
        +---------------------------+-------------------------------------------------------------------+
        | name_localizations        | `None`, `dict` of (``Locale``, `str`) items                       |
        +---------------------------+-------------------------------------------------------------------+
        | nsfw                      | `bool`                                                            |
        +---------------------------+-------------------------------------------------------------------+
        | options                   | `None`, `list` of ``ApplicationCommandOption``                    |
        +---------------------------+-------------------------------------------------------------------+
        | required_permissions      | ``Permission``                                                    |
        +---------------------------+-------------------------------------------------------------------+
        | target_type               | ``ApplicationCommandTargetType``                                  |
        +---------------------------+-------------------------------------------------------------------+
        | version                   | `int`                                                             |
        +---------------------------+-------------------------------------------------------------------+
    
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
        | excluded_channel_ids          | `None | tuple<int>`                                       |
        +-------------------------------+-----------------------------------------------------------+
        | excluded_role_ids             | `None | tuple<int>`                                       |
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
        | applied_tag_ids                       | `None | tuple<int>`                                       |
        +---------------------------------------+-----------------------------------------------------------+
        | archived                              | `bool`                                                    |
        +---------------------------------------+-----------------------------------------------------------+
        | archived_at                           | `None | DateTime`                                         |
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
        | default_thread_reaction_emoji         | `None`, ``Emoji``                                         |
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
        | status                                | `None`, `str`                                             |
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
    
    client_update(client: ``Client``, old_attributes: `None | dict`):
        Called when the client is updated. The passed `old_attributes` parameter contains the client's overwritten
        attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +-----------------------+-------------------------------+
        | Keys                  | Values                        |
        +=======================+===============================+
        | avatar                | ``Icon``                      |
        +-----------------------+-------------------------------+
        | avatar_decoration     | ``None | AvatarDecoration``   |
        +-----------------------+-------------------------------+
        | banner                | ``Icon``                      |
        +-----------------------+-------------------------------+
        | banner_color          | `None`, ``Color``             |
        +-----------------------+-------------------------------+
        | discriminator         | `int`                         |
        +-----------------------+-------------------------------+
        | display_name          | `None`, `str`                 |
        +-----------------------+-------------------------------+
        | email                 | `None`, `str`                 |
        +-----------------------+-------------------------------+
        | email_verified        | `bool`                        |
        +-----------------------+-------------------------------+
        | flags                 | ``UserFlag``                  |
        +-----------------------+-------------------------------+
        | locale                | ``Locale``                    |
        +-----------------------+-------------------------------+
        | mfa_enabled           | `bool`                        |
        +-----------------------+-------------------------------+
        | name                  | `str`                         |
        +-----------------------+-------------------------------+
        | name_plate            | ``None | NamePlate``          |
        +-----------------------+-------------------------------+
        | premium_type          | ``PremiumType``               |
        +-----------------------+-------------------------------+
        | primary_guild_badge   | `None`, ``GuildBadge``        |
        +-----------------------+-------------------------------+
    
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
    
    embedded_activity_create(client: ``Client``, embedded_activity: ``EmbeddedActivity``)
        Called when an embedded activity is created.
    
    embedded_activity_delete(client: ``Client``, embedded_activity: ``EmbeddedActivity``)
        Called when an embedded activity is deleted (all users left).
    
    embedded_activity_update(client: ``Client``, embedded_activity: ``EmbeddedActivity``,
            old_attributes: `None | dict`)
        Called when an embedded activity is updated. The passed `old_attributes` parameter contains the old states of
        the respective activity in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +-------------------+-----------------------------------+
        | Keys              | Values                            |
        +===================+===================================+
        | assets            | `None`, ``ActivityAssets``        |
        +-------------------+-----------------------------------+
        | buttons           | `None | tuple<str>`               |
        +-------------------+-----------------------------------+
        | created_at        | `DateTime`                        |
        +-------------------+-----------------------------------+
        | details           | `None`, `str`                     |
        +-------------------+-----------------------------------+
        | flags             | ``ActivityFlag``                  |
        +-------------------+-----------------------------------+
        | hang_type         | ``HangType``                      |
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
        
    embedded_activity_user_add(client: ``Client``, embedded_activity: ``EmbeddedActivity``,
            user_id: `int`)
        Called when a user joins an embedded activity. It is not called for the person(s) creating the activity.
    
    embedded_activity_user_delete(client: ``Client``, embedded_activity: ``EmbeddedActivity``,
            user_id: `int`)
        Called when a user leaves / is removed from an embedded activity.
    
    emoji_create(client: ``Client``, emoji: ``Emoji``):
        Called when an emoji is created at a guild.
    
    emoji_delete(client: ``Client``, emoji: ``Emoji``):
        Called when an emoji is deleted.
        
        Deleted emoji's `.guild` attribute is set to `None`.
        
    emoji_update(client: ``Client``, emoji: ``Emoji``, old_attributes: `None | dict`):
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
        | role_ids          | `None | tuple<int>`           |
        +-------------------+-------------------------------+
    
    entitlement_create(client : ``Client``, entitlement: ``Entitlement``):
        Called when entitlement is created.
    
    entitlement_delete(client: ``Client``, entitlement: ``Entitlement``)
        Called when an entitlement is deleted.
    
    entitlement_update(client: ``Client``, entitlement: ``Entitlement``, old_attributes: `None | dict`)
        Called when an entitlement is updated. The passed `old_attributes` parameter contains the emoji's overwritten
        attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +---------------------------+-----------------------------------------------+
        | Key                       | Value                                         |
        +===========================+===============================================+
        | consumed                  | `bool`                                        |
        +---------------------------+-----------------------------------------------+
        | deleted                   | `bool`                                        |
        +---------------------------+-----------------------------------------------+
        | ends_at                   | `None | DateTime`                             |
        +---------------------------+-----------------------------------------------+
        | starts_at                 | `None | DateTime`                             |
        +---------------------------+-----------------------------------------------+
    
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
    
    guild_update(client: ``Client``, guild: ``Guild``, old_attributes: `None | dict`):
        Called when a guild is updated. The passed `old_attributes` parameter contains the guild's overwritten attributes
        in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +---------------------------------------+---------------------------------------+
        | Keys                                  | Values                                |
        +========================================+=======================================+
        | afk_channel_id                        | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | afk_timeout                           | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | available                             | `bool`                                |
        +---------------------------------------+---------------------------------------+
        | banner                                | ``Icon``                              |
        +---------------------------------------+---------------------------------------+
        | boost_count                           | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | boost_level                           | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | boost_progress_bar_enabled            | `bool`                                |
        +---------------------------------------+---------------------------------------+
        | explicit_content_filter_level         | ``ExplicitContentFilterLevel``        |
        +---------------------------------------+---------------------------------------+
        | default_message_notification_level    | ``MessageNotificationLevel``          |
        +---------------------------------------+---------------------------------------+
        | description                           | `None`, `str`                         |
        +---------------------------------------+---------------------------------------+
        | discovery_splash                      | ``Icon``                              |
        +---------------------------------------+---------------------------------------+
        | features                              | `None`, `tuple` of ``GuildFeature``   |
        +---------------------------------------+---------------------------------------+
        | home_splash                           | ``Icon``                              |
        +---------------------------------------+---------------------------------------+
        | hub_type                              | ``HubType``                           |
        +---------------------------------------+---------------------------------------+
        | icon                                  | ``Icon``                              |
        +---------------------------------------+---------------------------------------+
        | incidents                             | `None`, ``GuildIncidents``            |
        +---------------------------------------+---------------------------------------+
        | inventory_settings                    | `None`, ``GuildInventorySettings``    |
        +---------------------------------------+---------------------------------------+
        | invite_splash                         | ``Icon``                              |
        +---------------------------------------+---------------------------------------+
        | max_presences                         | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | max_stage_channel_video_users         | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | max_users                             | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | max_voice_channel_video_users         | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | mfa_level                             | ``MfaLevel``                          |
        +---------------------------------------+---------------------------------------+
        | name                                  | `str`                                 |
        +---------------------------------------+---------------------------------------+
        | nsfw_level                            | ``NsfwLevel``                         |
        +---------------------------------------+---------------------------------------+
        | owner_id                              | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | locale                                | ``Locale``                            |
        +---------------------------------------+---------------------------------------+
        | public_updates_channel_id             | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | rules_channel_id                      | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | safety_alerts_channel_id              | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | system_channel_id                     | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | system_channel_flags                  | ``SystemChannelFlag``                 |
        +---------------------------------------+---------------------------------------+
        | vanity_code                           | `None`, `str`                         |
        +---------------------------------------+---------------------------------------+
        | verification_level                    | ``VerificationLevel``                 |
        +---------------------------------------+---------------------------------------+
        | widget_channel_id                     | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | widget_enabled                        | `bool`                                |
        +---------------------------------------+---------------------------------------+
    
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
            guild_profile: `None` | ``GuildProfile``):
        Called when a user left (kicked or banned counts as well) from a guild. The `profile` parameter is the user's
        respective guild profile for the guild.
    
    guild_user_update(client : Client, guild: ``Guild``, user: ``ClientUserBase``, old_attributes: `None | dict`):
        Called when a user's ``GuildProfile`` is updated. The passed `old_attributes` parameter contains the
        guild profile's overwritten attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +-------------------+-------------------------------+
        | Keys              | Values                        |
        +===================+===============================+
        | avatar            | ``Icon``                      |
        +-------------------+-------------------------------+
        | avatar_decoration | ``None | AvatarDecoration``   |
        +-------------------+-------------------------------+
        | banner            | ``Icon``                      |
        +-------------------+-------------------------------+
        | boosts_since      | `None | DateTime`             |
        +-------------------+-------------------------------+
        | flags             | `None`, ``GuildProfileFlags`` |
        +-------------------+-------------------------------+
        | nick              | `None`, `str`                 |
        +-------------------+-------------------------------+
        | pending           | `bool`                        |
        +-------------------+-------------------------------+
        | role_ids          | `None | tuple<int>`           |
        +-------------------+-------------------------------+
        | timed_out_until   | `None | DateTime`             |
        +-------------------+-------------------------------+
    
    guild_enhancement_entitlements_create(client : ``Client``, event : ``GuildEnhancementEntitlementsCreateEvent``):
        Called when enhancement entitlements are created for a guild.
    
    guild_enhancement_entitlements_delete(client : ``Client``, event : ``GuildEnhancementEntitlementsDeleteEvent``):
        Called when enhancement entitlements are deleted for a guild.
    
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
        | components                        | ``None | tuple<Component>``                                           |
        +-----------------------------------+-----------------------------------------------------------------------+
        | content                           | `None`, `str`                                                         |
        +-----------------------------------+-----------------------------------------------------------------------+
        | edited_at                         | `None | DateTime`                                                     |
        +-----------------------------------+-----------------------------------------------------------------------+
        | embeds                            | `None`, `tuple` of ``Embed``                                          |
        +-----------------------------------+-----------------------------------------------------------------------+
        | flags                             | ``MessageFlag``                                                       |
        +-----------------------------------+-----------------------------------------------------------------------+
        | mentioned_channels_cross_guild    | ``None | tuple<Channel>``                                             |
        +-----------------------------------+-----------------------------------------------------------------------+
        | mentioned_everyone                | `bool`                                                                |
        +-----------------------------------+-----------------------------------------------------------------------+
        | mentioned_role_ids                | `None | tuple<int>`                                                   |
        +-----------------------------------+-----------------------------------------------------------------------+
        | mentioned_users                   | `None`, `tuple` of ``ClientUserBase``                                 |
        +-----------------------------------+-----------------------------------------------------------------------+
        | pinned                            | `bool`                                                                |
        +-----------------------------------+-----------------------------------------------------------------------+
        | poll                              | ``PollChange``                                                        |
        +-----------------------------------+-----------------------------------------------------------------------+
        | resolved                          | ``None | Resolved``                                                   |
        +-----------------------------------+-----------------------------------------------------------------------+
        
        A special case is if a message is (un)pinned or (un)suppressed, because then the `old_attributes` parameter is
        not going to contain `edited`, only `pinned`, `flags`. If the embeds are (un)suppressed of the message, then
        `old_attributes` might contain also `embeds`.
        
        > If the message is partial (usually when it is not cached), `old_attributes` is passed as `None`.
    
    poll_vote_add(client : ``Client``, event : ``PollVoteAddEvent``):
        Called when a user votes on a poll.
    
    poll_vote_delete(client : ``Client``, event : ``PollVoteDeleteEvent``):
        Called when a user removes their vote from a poll.
    
    reaction_add(client: ``Client``, event: ``ReactionAddEvent``):
        Called when a user reacts on a message with the given emoji.
    
    reaction_clear(client: ``Client``, message: ``Message``, reactions: {`None`, ``ReactionMapping``}):
        Called when the reactions of a message are cleared. The passed `old_reactions` parameter are the old reactions
        of the message.
        
        > If the message is partial (usually when it is not cached), `reactions` is passed as `None`.
    
    reaction_delete(client: ``Client``, event: ``ReactionDeleteEvent``):
        Called when a user removes it's reaction from a message.
    
    reaction_delete_emoji(client: ``Client``, message: ``Message``, emoji : ``Emoji``,
            removed_reactions : `None`, `dict` of (``Reaction``, ``ReactionMappingLine``)):
        Called when all the reactions of a specified emoji are removed from a message.
        
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
    
    role_update(client: ``Client``, role: ``Role``, old_attributes: `None | dict`):
        Called when a role is updated.
        
        Every item in `old_attributes` is optional and they can be any of the following:
        
        +-----------------------+---------------------------+
        | Keys                  | Values                    |
        +=======================+===========================+
        | color                 | ``Color``                 |
        +-----------------------+---------------------------+
        | color_configuration   | ``ColorConfiguration``    |
        +-----------------------+---------------------------+
        | flags                 | ``RoleFlag``              |
        +-----------------------+---------------------------+
        | icon                  | ``Icon``                  |
        +-----------------------+---------------------------+
        | mentionable           | `bool`                    |
        +-----------------------+---------------------------+
        | name                  | `str`                     |
        +-----------------------+---------------------------+
        | permissions           | ``Permission``            |
        +-----------------------+---------------------------+
        | position              | `int`                     |
        +-----------------------+---------------------------+
        | separated             | `bool`                    |
        +-----------------------+---------------------------+
        | unicode_emoji         | ``None | Emoji``          |
        +-----------------------+---------------------------+
    
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
        | end                       | `None | DateTime`                             |
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
        | schedule                  | ``None | Schedule``                           |
        +---------------------------+-----------------------------------------------+
        | sku_ids                   | `None | tuple<int>`                           |
        +---------------------------+-----------------------------------------------+
        | start                     | `None | DateTime`                             |
        +---------------------------+-----------------------------------------------+
        | status                    | ``ScheduledEventStatus``                      |
        +---------------------------+-----------------------------------------------+
    
    scheduled_event_user_subscribe(client: ``Client``, event: ``ScheduledEventSubscribeEvent``):
        Called when a user subscribes to a scheduled event.
    
    scheduled_event_user_unsubscribe(client: ``Client``, event: ``ScheduledEventUnsubscribeEvent``):
        Called when a user unsubscribes from a scheduled event.
    
    scheduled_event_occasion_overwrite_create(client: ``Client``, event: ``ScheduledEventOccasionOverwriteCreateEvent``):
        Called when a singular occasion of a reoccurring scheduled event is overwritten.
    
    scheduled_event_occasion_overwrite_update(client: ``Client``, event: ``ScheduledEventOccasionOverwriteCreateEvent``,
            old_attributes : `None | dict`):
        Called when a singular occasion of a reoccurring scheduled event's overwrite is updated.
        
        If the scheduled event occasion overwrite is cached, `old_attributes` will be a dictionary including the
        changed attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional any can be any of the following:
        
        +---------------------------+-----------------------------------------------+
        | Key                       | Value                                         |
        +===========================+===============================================+
        | cancelled                 | `bool`                                        |
        +===========================+===============================================+
        | end                       | `None | DateTime`                             |
        +---------------------------+-----------------------------------------------+
        | start                     | `None | DateTime`                             |
        +---------------------------+-----------------------------------------------+
    
    scheduled_event_occasion_overwrite_delete(client: ``Client``, event: ``ScheduledEventOccasionOverwriteDeleteEvent``):
        Called when a singular occasion of a reoccurring scheduled event is not overwritten anymore.
    
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
    
    sticker_update(client : Client, sticker: ``Sticker``, old_attributes: `None | dict`):
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
    
    
    subscription_create(client : ``Client``, subscription: ``Subscription``):
        Called when subscription is created.
    
    subscription_delete(client: ``Client``, subscription: ``Subscription``)
        Called when an subscription is deleted.
    
    subscription_update(client: ``Client``, subscription: ``Subscription``, old_attributes: `None | dict`)
        Called when an subscription is updated. The passed `old_attributes` parameter contains the emoji's overwritten
        attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +---------------------------+-----------------------------------------------+
        | Key                       | Value                                         |
        +===========================+===============================================+
        | cancelled_at              | `None | DateTime`                             |
        +---------------------------+-----------------------------------------------+
        | country_code              | `None`, `str`                                 |
        +---------------------------+-----------------------------------------------+
        | current_period_end        | `None | DateTime`                             |
        +---------------------------+-----------------------------------------------+
        | current_period_start      | `None | DateTime`                             |
        +---------------------------+-----------------------------------------------+
        | renewal_sku_ids           | `None | tuple<int>`                           |
        +---------------------------+-----------------------------------------------+
        | sku_ids                   | `None | tuple<int>`                           |
        +---------------------------+-----------------------------------------------+
        | status                    | ``SubscriptionStatus``                        |
        +---------------------------+-----------------------------------------------+
    
    thread_user_add(client : ``Client``, thread_channel: ``Channel``, user: ``ClientUserBase``):
        Called when a user is added or joined a thread channel.
    
    thread_user_delete(client : ``Client``, thread_channel: ``Channel``, user: ``ClientUserBase``, \
            thread_profile: ``ThreadProfile``):
        Called when a user is removed or left a thread channel.
    
    thread_user_update(client : ``Client``, thread_channel: ``Channel``, user: ``ClientUserBase``, \
            old_attributes: `None | dict`):
        Called when a user's thread profile is updated. The passed `old_attributes` parameter contains the
        thread profile's overwritten attributes in `attribute-name` - `old-value` relation.
        
        > Note that this event is limited only to the respective client and is not triggered for other users.
        
        Every item in `old_attributes` is optional they can be any of the following:
        
        +-------------------+-------------------------------+
        | Keys              | Values                        |
        +===================+===============================+
        | flags             | ``ThreadProfileFlag``         |
        +-------------------+-------------------------------+
    
    typing(client: ``Client``, channel: ``Channel``, user: ``ClientUserBase``, timestamp: `DateTime`):
        Called when a user is typing at a channel. The `timestamp` parameter represents when the typing started.
        
        However a typing requests stands for 8 seconds, but the official Discord client usually just spams it.
    
    unknown_dispatch_event(client: ``Client``, name: `str`, data: `object`):
        Called when an unknown dispatch event is received.
    
    user_update(client: ``Client``, user: ``ClientUserBase``, old_attributes: `None | dict`):
        Called when a user is updated This event not includes guild profile changes. The passed `old_attributes`
        parameter contains the user's overwritten attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional they can be any of the following:
        
        +-----------------------+-------------------------------+
        | Keys                  | Values                        |
        +=======================+===============================+
        | avatar                | ``Icon``                      |
        +-----------------------+-------------------------------+
        | avatar_decoration     | ``None | AvatarDecoration``   |
        +-----------------------+-------------------------------+
        | banner                | ``Icon``                      |
        +-----------------------+-------------------------------+
        | banner_color          | `None`, ``Color``             |
        +-----------------------+-------------------------------+
        | discriminator         | `int`                         |
        +-----------------------+-------------------------------+
        | display_name          | `None`, `str`                 |
        +-----------------------+-------------------------------+
        | email                 | `None`, `str`                 |
        +-----------------------+-------------------------------+
        | email_verified        | `bool`                        |
        +-----------------------+-------------------------------+
        | flags                 | ``UserFlag``                  |
        +-----------------------+-------------------------------+
        | locale                | ``Locale``                    |
        +-----------------------+-------------------------------+
        | mfa_enabled           | `bool`                        |
        +-----------------------+-------------------------------+
        | name                  | `str`                         |
        +-----------------------+-------------------------------+
        | name_plate            | ``None | NamePlate``          |
        +-----------------------+-------------------------------+
        | premium_type          | ``PremiumType``               |
        +-----------------------+-------------------------------+
        | primary_guild_badge   | `None`, ``GuildBadge``        |
        +-----------------------+-------------------------------+
    
    user_presence_update(client: ``Client``, user: ``ClientUserBase``, old_attributes: `None | dict`):
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
        | statuses      | `dict<str, str>`                  |
        +---------------+-----------------------------------+
    
    user_voice_join(client: ``Client``, voice_state: ``VoiceState``)
        Called when a user joins a voice channel.
    
    user_voice_leave(client: ``client``, voice_state: ``VoiceState``, old_channel_id : `int`)
        Called when a user leaves from a voice channel.
    
    user_voice_move(client: ``Client``, voice_state: ``VoiceState``, old_channel_id : `int`)
        Called when a user moves between two voice channels
    
    user_voice_update(client: ``Client``, voice_state: ``VoiceState``, old_attributes: `None | dict`):
        Called when a voice state of a user is updated.
        
        Every item in `old_attributes` is optional and they can be the following:
        
        +-----------------------+-----------------------+
        | Keys                  | Values                |
        +=======================+=======================+
        | deaf                  | `str`                 |
        +-----------------------+-----------------------+
        | mute                  | `bool`                |
        +-----------------------+-----------------------+
        | requested_to_speak_at | `None | DateTime`     |
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
        
        > This also includes soundboard sounds as well. The other event is likely to not be working anymore.
    
    voice_client_join(client : ``Client``, voice_state : ``VoiceState``)
        Called when the client join a voice channel.
        
        > This event has a default handler defined, which is used by hata's ``VoiceClient``.
        >
        > When using 3rd party voice library, make sure to register your by passing `overwrite = True` parameter as
        > well.
    
    voice_client_ghost(client : ``Client``, voice_state : ``VoiceState``)
        Called when the client has a voice state in a channel, when logging in.
        
        > This event has a default handler defined, which is used by hata's ``VoiceClient``.
        >
        > When using 3rd party voice library, make sure to register your by passing `overwrite = True` parameter as
        > well.
    
    voice_client_leave(client : ``Client``, voice_state : ``VoiceState``, old_channel_id : `int`)
        Called when the client leaves / is removed fro ma voice channel.
        
        > This event has a default handler defined, which is used by hata's ``VoiceClient``.
        >
        > When using 3rd party voice library, make sure to register your by passing `overwrite = True` parameter as
        > well.
    
    voice_client_move(client : ``Client``, voice_state : ``VoiceState``, old_channel_id : `int`)
        Called when the client moves / is moved between two channels.
        
        > This event has a default handler defined, which is used by hata's ``VoiceClient``.
        >
        > When using 3rd party voice library, make sure to register your by passing `overwrite = True` parameter as
        > well.
    
    voice_client_shutdown(client : ``Client``)
        Called when the client disconnects. Should be used to disconnect the client's voice clients.
    
        > This event has a default handler defined, which is used by hata's ``VoiceClient``.
        >
        > When using 3rd party voice library, make sure to register your by passing `overwrite = True` parameter as
        > well.
    
    voice_client_update(client : ``Client``, voice_state : ``VoiceState``, old_attributes : `dict`)
        Called when the client's state is updated.
        
        > This event has a default handler defined, which is used by hata's ``VoiceClient``.
        >
        > When using 3rd party voice library, make sure to register your by passing `overwrite = True` parameter as
        > well.
        
        Every item in `old_attributes` is optional and they can be the following:
        
        +-----------------------+-----------------------+
        | Keys                  | Values                |
        +=======================+=======================+
        | deaf                  | `str`                 |
        +-----------------------+-----------------------+
        | mute                  | `bool`                |
        +-----------------------+-----------------------+
        | requested_to_speak_at | `None | DateTime`     |
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
        > When using 3rd party voice library, make sure to register your by passing `overwrite = True` parameter as
        > well.
    
    voice_server_update(client: ``Client``, event: ``VoiceServerUpdateEvent``)
        Called initially when the client connects to a voice channels of a guild. Also called when a guild's voice
        server is updated.
        
        > This event has a default handler defined, which is used by hata's ``VoiceClient``.
        >
        > When using 3rd party voice library, make sure to register your by passing `overwrite = True` parameter as
        > well.
    
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
        object.__setattr__(self, '_plugin_events_deprecated', None)
        
        for name in EVENT_HANDLER_NAME_TO_PARSER_NAMES:
            object.__setattr__(self, name, DEFAULT_EVENT_HANDLER)
        
        object.__setattr__(self, '_launch_called', False)
        
        for event_handler_name, event_handler, instance_event_handler in DEFAULT_EVENT_HANDLERS:
            if instance_event_handler:
                event_handler = event_handler()
            object.__setattr__(self, event_handler_name, event_handler)
    
    
    def __call__(self, func = None, *, name = ..., overwrite = ...):
        """
        Adds the given `func` as an event handler.
        
        Parameters
        ----------
        func : `None`, `callable` = `None`, Optional
            The async callable to add as an event handler.
            
            If given as `None` will return a decorator.
        
        name : `None`, `str`, Optional (Keyword only)
            A name to be used instead of the passed `func`'s when adding it.
        
        overwrite : `bool`, Optional (Keyword only)
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
        
        if name is ...:
            name = None
        
        if overwrite is ...:
            overwrite = False
        
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
        
        plugin_events_deprecated = self._plugin_events_deprecated
        if (plugin_events_deprecated is not None):
            try:
                event_handler_plugin, deprecation = plugin_events_deprecated[name]
            except KeyError:
                pass
            else:
                deprecation.trigger(name, 2)
                return getattr(event_handler_plugin, name)
        
        RichAttributeErrorBaseType.__getattr__(self, name)
    
    
    def __dir__(self):
        """Returns the attributes of the event handler manager."""
        directory = object.__dir__(self)
        plugins = self._plugins
        if (plugins is not None):
            directory = set(directory)
            
            for plugin in plugins:
                plugin_event_names = plugin._plugin_event_names
                if (plugin_event_names is not None):
                    directory.update(plugin_event_names)
            
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
        event_handler : `None | object`
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
        plugin : `EventHandlerPlugin | type<EventHandlerPlugin>`
            The plugin to add.
        
        Returns
        -------
        plugin : ``EventHandlerPlugin``
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
                f'`plugin` can be `{EventHandlerPlugin.__name__}`, got {type(plugin).__name__}; {plugin!r}.'
            )
        
        plugin_events = self._plugin_events
        plugin_events_deprecated = self._plugin_events_deprecated
        
        event_names = plugin._plugin_event_names
        deprecated_events = plugin._plugin_event_deprecations
        
        # precheck
        if (event_names is not None):
            for event_name in event_names:
                _check_duplicate_plugin_event_name(plugin, event_name, plugin_events, plugin_events_deprecated)
        
        if (deprecated_events is not None):
            for event_name, deprecation in deprecated_events:
                _check_duplicate_plugin_event_name(plugin, event_name, plugin_events, plugin_events_deprecated)
        
        # assign
        if (event_names is not None):
            if (plugin_events is None):
                plugin_events = {}
                object.__setattr__(self, '_plugin_events', plugin_events)
            
            for event_name in event_names:
                plugin_events[event_name] = plugin
        
        if (deprecated_events is not None):
            if (plugin_events_deprecated is None):
                plugin_events_deprecated = {}
                object.__setattr__(self, '_plugin_events_deprecated', plugin_events_deprecated)
            
            for event_name, deprecation in deprecated_events:
                plugin_events_deprecated[event_name] = (plugin, deprecation)
        
        plugins = self._plugins
        if plugins is None:
            plugins = set()
            object.__setattr__(self, '_plugins', plugins)
        
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
