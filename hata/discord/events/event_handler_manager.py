__all__ = ()

import warnings
from functools import partial as partial_func

from ...backend.utils import WeakReferer

from .core import DEFAULT_EVENT_HANDLER, EVENT_HANDLER_NAME_TO_PARSER_NAMES, get_event_parser_parameter_count, \
    PARSER_SETTINGS
from .handling_helpers import ChunkWaiter, check_parameter_count_and_convert, asynclist, \
    check_name
from .default_event_handlers import default_error_event_handler, default_voice_server_update_event_handler, \
    default_voice_client_ghost_event_handler, default_voice_client_join_event_handler, \
    default_voice_client_move_event_handler, default_voice_client_leave_event_handler, \
    default_voice_client_update_event_handler, default_voice_client_shutdown_event_handler

class EventHandlerManager:
    """
    After a client gets a dispatch event from Discord, it's parser might ensure an event. These events are stored
    inside of a ``EventHandlerManager`` and can be accessed through ``Client.events``.
    
    Each added event should be an async callable accepting a predefined amount of positional parameters.
    
    Attributes
    ----------
    _launch_called : `bool`
        Whether The respective client's `.events.launch` was called already.
    client_reference : ``WeakReferer``
        Weak reference to the parent client to avoid reference loops.
    
    Additional Event Attributes
    --------------------------
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
        
        +-----------------------+---------------------------------------------------+
        | Keys                  | Values                                            |
        +=======================+===================================================+
        | default_permission    | `bool`                                            |
        +-----------------------+---------------------------------------------------+
        | description           | `None` or `str`                                   |
        +-----------------------+---------------------------------------------------+
        | name                  | `str`                                             |
        +-----------------------+---------------------------------------------------+
        | options               | `None` or `list` of ``ApplicationCommandOption``  |
        +-----------------------+---------------------------------------------------+
        | target_type           | ``ApplicationCommandTargetType``                  |
        +-----------------------+---------------------------------------------------+
    
    channel_create(client: ``Client``, channel: ``ChannelBase``)
        Called when a channel is created.
        
        > This event is not called when a private channel is created.
    
    channel_delete(client: ``Client``, channel: ``ChannelBase``)
        Called when a channel is deleted.
    
    channel_edit(client: ``Client``, channel: ``ChannelBase``, old_attributes: `dict`)
        Called when a channel is edited. The passed `old_attributes` parameter contains the channel's overwritten
        attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +-----------------------+---------------------------------------+
        | Keys                  | Values                                |
        +=======================+=======================================+
        | archived              | `bool`                                |
        +-----------------------+---------------------------------------+
        | archived_at           | `None` or `datetime`                  |
        +-----------------------+---------------------------------------+
        | auto_archive_after    | `int`                                 |
        +-----------------------+---------------------------------------+
        | bitrate               | `int`                                 |
        +-----------------------+---------------------------------------+
        | icon                  | ``Icon``                              |
        +-----------------------+---------------------------------------+
        | invitable             | `bool`                                |
        +-----------------------+---------------------------------------+
        | parent_id             | `int`                                 |
        +-----------------------+---------------------------------------+
        | name                  | `str`                                 |
        +-----------------------+---------------------------------------+
        | nsfw                  | `bool`                                |
        +-----------------------+---------------------------------------+
        | open                  | `bool`                                |
        +-----------------------+---------------------------------------+
        | overwrites            | `list` of ``PermissionOverwrite``     |
        +-----------------------+---------------------------------------+
        | owner_id              | `int`                                 |
        +-----------------------+---------------------------------------+
        | position              | `int`                                 |
        +-----------------------+---------------------------------------+
        | region                | `None` or ``VoiceRegion``             |
        +-----------------------+---------------------------------------+
        | slowmode              | `int`                                 |
        +-----------------------+---------------------------------------+
        | topic                 | `None` or `str`                       |
        +-----------------------+---------------------------------------+
        | type                  | `int`                                 |
        +-----------------------+---------------------------------------+
        | user_limit            | `int`                                 |
        +-----------------------+---------------------------------------+
        | video_quality_mode    | ``VideoQualityMode``                  |
        +-----------------------+---------------------------------------+
    
    channel_group_user_add(client: ``Client``, channel: ``ChannelGroup``, user: ``ClientUserBase``):
        Called when a user is added to a group channel.
    
    channel_group_user_delete(client: ``Client``, channel: ``ChannelGroup``, user: ``ClientUserBase``):
        Called when a user is removed from a group channel.
    
    channel_pin_update(client: ``Client``, channel: ``ChannelTextBase``):
        Called when a channel's pins are updated.
    
    client_edit(client: ``Client``, old_attributes: `dict`):
        Called when the client is edited. The passed `old_attributes` parameter contains the client's overwritten
        attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +-----------------------+-----------------------+
        | Keys                  | Values                |
        +=======================+=======================+
        | avatar                | ``Icon``              |
        +-----------------------+-----------------------+
        | banner                | ``Icon``              |
        +-----------------------+-----------------------+
        | banner_color          | `None` or ``Color``   |
        +-----------------------+-----------------------+
        | discriminator         | `int`                 |
        +-----------------------+-----------------------+
        | email                 | `None` or `str`       |
        +-----------------------+-----------------------+
        | flags                 | ``UserFlag``          |
        +-----------------------+-----------------------+
        | locale                | `str                  |
        +-----------------------+-----------------------+
        | mfa                   | `bool`                |
        +-----------------------+-----------------------+
        | name                  | `str                  |
        +-----------------------+-----------------------+
        | premium_type          | ``PremiumType``       |
        +-----------------------+-----------------------+
        | verified              | `bool`                |
        +-----------------------+-----------------------+
    
    embed_update(client: ``Client``, message: ``Message``, change_state: `int`):
        Called when a message is not edited, only it's embeds are updated.
        
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
    
    emoji_create(client: ``Client``, emoji: ``Emoji``):
        Called when an emoji is created at a guild.
    
    emoji_delete(client: ``Client``, emoji: ``Emoji``):
        Called when an emoji is deleted.
        
        Deleted emoji's `.guild` attribute is set to `None`.
        
    emoji_edit(client : Client, emoji: ``Emoji``, old_attributes: `dict`):
        Called when an emoji is edited. The passed `old_attributes` parameter contains the emoji's overwritten
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
        | role_ids          | `None` or `tuple` of `int`    |
        +-------------------+-------------------------------+
    
    error(client: ``Client``, name: `str`, err: `Any`):
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
    
    guild_delete(client: ``Client``, guild: ``Guild``, profile: ``GuildProfile``):
        Called when the guild is deleted or just the client left (kicked or banned as well) from it. The `profile`
        parameter is the client's respective guild profile for the guild.
    
    guild_edit(client: ``Client``, guild: ``Guild``, old_attributes: `dict`):
        Called when a guild is edited. The passed `old_attributes` parameter contains the guild's overwritten attributes
        in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +---------------------------+-------------------------------+
        | Keys                      | Values                        |
        +===========================+===============================+
        | afk_channel_id            | `int`                         |
        +---------------------------+-------------------------------+
        | afk_timeout               | `int`                         |
        +---------------------------+-------------------------------+
        | available                 | `bool`                        |
        +---------------------------+-------------------------------+
        | banner                    | ``Icon``                      |
        +---------------------------+-------------------------------+
        | booster_count             | `int`                         |
        +---------------------------+-------------------------------+
        | content_filter            | ``ContentFilterLevel``        |
        +---------------------------+-------------------------------+
        | description               | `None` or `str`               |
        +---------------------------+-------------------------------+
        | discovery_splash          | ``Icon``                      |
        +---------------------------+-------------------------------+
        | features                  | `list` of ``GuildFeature``    |
        +---------------------------+-------------------------------+
        | icon                      | ``Icon``                      |
        +---------------------------+-------------------------------+
        | invite_splash             | ``Icon``                      |
        +---------------------------+-------------------------------+
        | max_presences             | `int`                         |
        +---------------------------+-------------------------------+
        | max_users                 | `int`                         |
        +---------------------------+-------------------------------+
        | max_video_channel_users   | `int`                         |
        +---------------------------+-------------------------------+
        | message_notification      | ``MessageNotificationLevel``  |
        +---------------------------+-------------------------------+
        | mfa                       | ``MFA``                       |
        +---------------------------+-------------------------------+
        | name                      | `str`                         |
        +---------------------------+-------------------------------+
        | nsfw_level                | `NsfwLevel`                   |
        +---------------------------+-------------------------------+
        | owner_id                  | `int`                         |
        +---------------------------+-------------------------------+
        | preferred_locale          | `str`                         |
        +---------------------------+-------------------------------+
        | premium_tier              | `int`                         |
        +---------------------------+-------------------------------+
        | public_updates_channel_id | `int`                         |
        +---------------------------+-------------------------------+
        | region                    | ``VoiceRegion``               |
        +---------------------------+-------------------------------+
        | rules_channel_id          | `int`                         |
        +---------------------------+-------------------------------+
        | system_channel_id         | `int`                         |
        +---------------------------+-------------------------------+
        | system_channel_flags      | ``SystemChannelFlag``         |
        +---------------------------+-------------------------------+
        | vanity_code               | `None` or `str`               |
        +---------------------------+-------------------------------+
        | verification_level        | ``VerificationLevel``         |
        +---------------------------+-------------------------------+
        | widget_channel_id         | `int`                         |
        +---------------------------+-------------------------------+
        | widget_enabled            | `bool`                        |
        +---------------------------+-------------------------------+
    
    guild_join_reject(client: ``Client``, guild: ``Guild``, user: ``ClientUserBase``):
        Called when a user leaves from a guild before completing it's verification screen.
        
        > ``.guild_user_delete`` is called as well.
    
    guild_user_add(client: ``Client``, guild: ``Guild``, user: ``ClientUserBase``):
        Called when a user joins a guild.
    
    guild_user_chunk(client: ``Client``, event: GuildUserChunkEvent):
        Called when a client receives a chunk of users from Discord requested by through it's gateway.
        
        The event has a default handler called ``ChunkWaiter``.
    
    guild_user_delete(client: ``Client``, guild: ``Guild``, user: ``ClientUserBase``, \
            profile: ``GuildProfile``):
        Called when a user left (kicked or banned counts as well) from a guild. The `profile` parameter is the user's
        respective guild profile for the guild.
    
    guild_user_edit(client : Client, user: ``ClientUserBase``, guild: ``Guild``, old_attributes: `dict`):
        Called when a user's ``GuildProfile`` is updated. The passed `old_attributes` parameter contains the message's
        overwritten attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +-------------------+-------------------------------+
        | Keys              | Values                        |
        +===================+===============================+
        | avatar            | ``Icon``                      |
        +-------------------+-------------------------------+
        | boosts_since      | `None` or `datetime`          |
        +-------------------+-------------------------------+
        | nick              | `None` or `str`               |
        +-------------------+-------------------------------+
        | pending           | `bool`                        |
        +-------------------+-------------------------------+
        | role_ids          | `None` or `tuple` of `int`    |
        +-------------------+-------------------------------+
    
    integration_create(client: ``Client``, guild: ``Guild``, integration: ``Integration``):
        Called when an integration is created inside of a guild. Includes cases when bots are added to the guild as
        well.
    
    integration_delete(client: ``Client``, guild: ``Guild``, integration_id: `int`, \
            application_id: {`None`, `int`}):
        Called when a guild has one of it's integrations deleted. If the integration is bound to an application, like
        a bot, then `application_id` is given as `int`.
    
    integration_edit(client: ``Client``, guild: ``Guild``, integration: ``Integration``):
        Called when an integration is edited inside of a guild.
    
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
    
    message_delete(client: ``Client``, message: {``Message``, ``MessageRepr``}):
        Called when a loaded message is deleted.
        
        > If `HATA_ALLOW_DEAD_EVENTS` environmental variable is given as `True`, and an uncached message is deleted,
        > then `message` is given as ``MessageRepr`` instance.
    
    message_edit(client: ``Client``, message: ``Message``, old_attributes: {`None`, `dict`}):
        Called when a loaded message is edited. The passed `old_attributes` parameter contains the message's overwritten
        attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +-------------------+-----------------------------------------------------------------------+
        | Keys              | Values                                                                |
        +===================+=======================================================================+
        | attachments       | `None` or (`tuple` of ``Attachment``)                                 |
        +-------------------+-----------------------------------------------------------------------+
        | components        | `None` or (`tuple` of ``ComponentBase``)                              |
        +-------------------+-----------------------------------------------------------------------+
        | content           | `None` or `str`                                                       |
        +-------------------+-----------------------------------------------------------------------+
        | cross_mentions    | `None` or (`tuple` of (``ChannelBase`` or ``UnknownCrossMention``))   |
        +-------------------+-----------------------------------------------------------------------+
        | edited_at         | `None` or `datetime`                                                  |
        +-------------------+-----------------------------------------------------------------------+
        | embeds            | `None` or `(tuple` of ``EmbedCore``)                                  |
        +-------------------+-----------------------------------------------------------------------+
        | flags             | ``UserFlag``                                                          |
        +-------------------+-----------------------------------------------------------------------+
        | mention_everyone  | `bool`                                                                |
        +-------------------+-----------------------------------------------------------------------+
        | pinned            | `bool`                                                                |
        +-------------------+-----------------------------------------------------------------------+
        | user_mentions     | `None` or (`tuple` of ``UserBase``)                                   |
        +-------------------+-----------------------------------------------------------------------+
        | role_mention_ids  | `None` or (`tuple` of `int`)                                          |
        +-------------------+-----------------------------------------------------------------------+
        
        A special case is if a message is (un)pinned or (un)suppressed, because then the `old_attributes` parameter is
        not going to contain `edited`, only `pinned` or `flags`. If the embeds are (un)suppressed of the message, then
        `old_attributes` might contain also `embeds`.
        
        > If `HATA_ALLOW_DEAD_EVENTS` environmental variable is given as `True`, and an uncached message is updated,
        > then `old_attributes` is given as `None`.
    
    reaction_add(client: ``Client``, event: ``ReactionAddEvent``):
        Called when a user reacts on a message with the given emoji.
        
        > If `HATA_ALLOW_DEAD_EVENTS` environmental variable is given as `True`, and the reaction is added on an
        > uncached message, then `message` is given as ``MessageRepr``.
    
    reaction_clear(client: ``Client``, message: {``Message``, ``MessageRepr``}, \
            reactions: {`None`, ``reaction_mapping``}):
        Called when the reactions of a message are cleared. The passed `old_reactions` parameter are the old reactions
        of the message.
        
        > If `HATA_ALLOW_DEAD_EVENTS` environmental variable is given as `True`, and the reactions are removed from
        > and uncached message, then `message` is given as ``MessageRepr`` and `old_reactions` as `None`.
    
    reaction_delete(client: ``Client``, event: ``ReactionDeleteEvent``):
        Called when a user removes it's reaction from a message.
        
        Note, if `HATA_ALLOW_DEAD_EVENTS` environmental variable is given as `True`, and the reaction is removed from
        and uncached message, then `message` is given as ``MessageRepr``.
    
    reaction_delete_emoji(client: ``Client``, message: {``Message``, ``MessageRepr``}, \
            users: {`None`, ``reaction_mapping_line``}):
        Called when all the reactions of a specified emoji are removed from a message. The passed `users` parameter
        are the old reactor users of the given emoji.
        
        > If `HATA_ALLOW_DEAD_EVENTS` environmental variable is given as `True`, and the reactions are removed from
        > and uncached message, then `message` is given as ``MessageRepr`` and `users` as `None`.
    
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
    
    role_delete(client: ``Client``, role: ``Role``, guild: ``Guild``):
        Called when a role is deleted from a guild.
        
        Deleted role's `.guild` attribute is set as `None`.
    
    role_edit(client: ``Client``, role: ``Role``, old_attributes: `dict`):
        Called when a role is edited.
        
        Every item in `old_attributes` is optional and they can be any of the following:
        
        +---------------+-----------------------+
        | Keys          | Values                |
        +===============+=======================+
        | color         | ``Color``             |
        +---------------+-----------------------+
        | icon          | ``Icon``              |
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
        | unicode_emoji | `None` or ``Emoji``   |
        +---------------+-----------------------+
    
    shutdown(client : ``Client``):
        Called when ``Client.stop`` or ``Client.disconnect`` is called indicating, that the client is logging off and
        all data should be saved if needed.
    
    stage_create(client: ``Client``, stage: ``Stage``):
        Called when a stage is created.
    
    stage_delete(client: ``Client``, stage: ``Stage``):
        Called when a stage is deleted.
    
    stage_edit(client: ``Client``, stage: ``Stage``, old_attributes: `dict`):
        Called when a stage is edited.
    
        Every item in `old_attributes` is optional and they can be any of the following:
        
        +---------------+-----------------------+
        | Keys          | Values                |
        +===============+=======================+
        | discoverable  | `bool`                |
        +---------------+-----------------------+
        | invite_code   | `None` or `str`       |
        +---------------+-----------------------+
        | privacy_level | ``PrivacyLevel``      |
        +---------------+-----------------------+
        | topic         | `str`                 |
        +---------------+-----------------------+
    
    sticker_create(client: ``Client``, sticker: ``Sticker``):
        Called when an sticker is created at a guild.
    
    sticker_delete(client: ``Client``, sticker: ``Sticker``):
        Called when an sticker is deleted.
    
    sticker_edit(client : Client, sticker: ``Sticker``, old_attributes: `dict`):
        Called when an sticker is edited. The passed `old_attributes` parameter contains the sticker's overwritten
        attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +-----------------------+-----------------------------------+
        | Keys                  | Values                            |
        +=======================+===================================+
        | available             | `bool`                            |
        +-----------------------+-----------------------------------+
        | description           | `None` or `str`                   |
        +-----------------------+-----------------------------------+
        | name                  | `str`                             |
        +-----------------------+-----------------------------------+
        | sort_value            | `int`                             |
        +-----------------------+-----------------------------------+
        | tags                  | `None`  or `frozenset` of `str`   |
        +-----------------------+-----------------------------------+
    
    thread_user_add(client : ``Client``, thread_channel: ``ChannelThread``, user: ``ClientUserBase``):
        Called when a user is added or joined a thread channel.
    
    thread_user_delete(client : ``Client``, thread_channel: ``ChannelThread``, user: ``ClientUserBase``, \
            thread_profile: ``ThreadProfile``):
        Called when a user is removed or left a thread channel.
    
    typing(client: ``Client``, channel: ``ChannelTextBase``, user: ``ClientUserBase``, timestamp: `datetime`):
        Called when a user is typing at a channel. The `timestamp` parameter represents when the typing started.
        
        However a typing requests stands for 8 seconds, but the official Discord client usually just spams it.
    
    user_edit(client: ``Client``, user: ``ClientUserBase``, old_attributes: `dict`):
        Called when a user is edited This event not includes guild profile changes. The passed `old_attributes`
        parameter contains the message's overwritten attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional they can be any of the following:
        
        +---------------+-----------------------+
        | Keys          | Values                |
        +===============+=======================+
        | avatar        | ``Icon``              |
        +---------------+-----------------------+
        | banner        | ``Icon``              |
        +---------------+-----------------------+
        | banner_color  | `None` or ``Color``   |
        +---------------+-----------------------+
        | discriminator | `int`                 |
        +---------------+-----------------------+
        | flags         | ``UserFlag``          |
        +---------------+-----------------------+
        | name          | `str`                 |
        +---------------+-----------------------+
    
    user_presence_update(client: ``Client``, user: ``ClientUserBase``, old_attributes: `dict`):
        Called when a user's presence is updated.
        
        The passed `old_attributes` parameter contain the user's changed presence related attributes in
        `attribute-name` - `old-value` relation. An exception from this is `activities`, because that is a
        ``ActivityChange`` instance containing all the changes of the user's activities.
        
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
        | is_speaker            | `bool`                |
        +-----------------------+-----------------------+
        | mute                  | `bool`                |
        +-----------------------+-----------------------+
        | requested_to_speak_at | `None` or `datetime`  |
        +-----------------------+-----------------------+
        | self_deaf             | `bool`                |
        +-----------------------+-----------------------+
        | self_mute             | `bool`                |
        +-----------------------+-----------------------+
        | self_stream           | `bool`                |
        +-----------------------+-----------------------+
        | self_video            | `bool`                |
        +-----------------------+-----------------------+
    
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
        | is_speaker            | `bool`                |
        +-----------------------+-----------------------+
        | mute                  | `bool`                |
        +-----------------------+-----------------------+
        | requested_to_speak_at | `None` or `datetime`  |
        +-----------------------+-----------------------+
        | self_deaf             | `bool`                |
        +-----------------------+-----------------------+
        | self_mute             | `bool`                |
        +-----------------------+-----------------------+
        | self_stream           | `bool`                |
        +-----------------------+-----------------------+
        | self_video            | `bool`                |
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
    
    webhook_update(client: ``Client``, channel: ``ChannelGuildBase``):
        Called when a webhook of a channel is updated. Discord not provides further details tho.
    """
    __slots__ = ('client_reference', '_launch_called', *sorted(EVENT_HANDLER_NAME_TO_PARSER_NAMES))
    
    def __init__(self, client):
        """
        Creates an ``EventHandlerManager`` for the given client.
        
        Parameters
        ----------
        client : ``Client``
        """
        client_reference = WeakReferer(client)
        object.__setattr__(self, 'client_reference', client_reference)
        for name in EVENT_HANDLER_NAME_TO_PARSER_NAMES:
            object.__setattr__(self, name, DEFAULT_EVENT_HANDLER)
        
        object.__setattr__(self, 'error', default_error_event_handler)
        object.__setattr__(self, '_launch_called', False)
        object.__setattr__(self, 'guild_user_chunk', ChunkWaiter())
        object.__setattr__(self, 'voice_server_update', default_voice_server_update_event_handler)
        object.__setattr__(self, 'voice_client_ghost', default_voice_client_ghost_event_handler)
        object.__setattr__(self, 'voice_client_join', default_voice_client_join_event_handler)
        object.__setattr__(self, 'voice_client_move', default_voice_client_move_event_handler)
        object.__setattr__(self, 'voice_client_leave', default_voice_client_leave_event_handler)
        object.__setattr__(self, 'voice_client_update', default_voice_client_update_event_handler)
        object.__setattr__(self, 'voice_client_shutdown', default_voice_client_shutdown_event_handler)
    
    
    def __call__(self, func=None, name=None, overwrite=False):
        """
        Adds the given `func` to the event descriptor as en event handler.
        
        Parameters
        ----------
        func : `callable`, Optional
            The async callable to add as an event handler.
        name : `None` or `str`, Optional
            A name to be used instead of the passed `func`'s when adding it.
        overwrite : `bool`, Optional
            Whether the passed `func` should overwrite the already added ones with the same name or extend them.
        
        Returns
        -------
        func : `callable`
            The added callable or `functools.partial` instance if `func` was not given.
        
        Raises
        ------
        AttributeError
            Invalid event name.
        TypeError
            - If `func` was not given as callable.
            - If `func` is not as async and neither cannot be converted to an async one.
            - If `func` expects less or more non reserved positional parameters as `expected` is.
            - If `name` was not passed as `None` or type `str`.
        """
        if func is None:
            return partial_func(self, name=name, overwrite=overwrite)
        
        name = check_name(func, name)
        
        parameter_count = get_event_parser_parameter_count(name)
        func = check_parameter_count_and_convert(func, parameter_count, name=name)
        
        if overwrite:
            setattr(self, name, func)
            return func
        
        parser_names = EVENT_HANDLER_NAME_TO_PARSER_NAMES.get(name, None)
        if (parser_names is None):
            raise AttributeError(f'Event name: {name!r} is invalid.')
        
        if func is DEFAULT_EVENT_HANDLER:
            return func
        
        actual = getattr(self, name)
        if actual is DEFAULT_EVENT_HANDLER:
            object.__setattr__(self, name, func)
            
            for parser_name in parser_names:
                parser_setting = PARSER_SETTINGS[parser_name]
                parser_setting.add_mention(self.client_reference())
            return func
        
        if type(actual) is asynclist:
            list.append(actual, func)
            return func
        
        new = asynclist()
        list.append(new, actual)
        list.append(new, func)
        object.__setattr__(self, name, new)
        return func
    
    
    def clear(self):
        """
        Clears the ``EventHandlerManager`` to the same state as it were just created.
        """
        delete = type(self).__delattr__
        for name in EVENT_HANDLER_NAME_TO_PARSER_NAMES:
            delete(self, name)
        
        object.__setattr__(self, 'error', default_error_event_handler)
        object.__setattr__(self, 'guild_user_chunk', ChunkWaiter())
        object.__setattr__(self, 'voice_server_update', default_voice_server_update_event_handler)
        object.__setattr__(self, 'voice_client_ghost', default_voice_client_ghost_event_handler)
        object.__setattr__(self, 'voice_client_join', default_voice_client_join_event_handler)
        object.__setattr__(self, 'voice_client_move', default_voice_client_move_event_handler)
        object.__setattr__(self, 'voice_client_leave', default_voice_client_leave_event_handler)
        object.__setattr__(self, 'voice_client_update', default_voice_client_update_event_handler)
        object.__setattr__(self, 'voice_client_shutdown', default_voice_client_shutdown_event_handler)
    
    def __setattr__(self, name, value):
        """
        Sets the given event handler under the specified event name. Updates the respective event's parser(s) if needed.
        
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
        parser_names = EVENT_HANDLER_NAME_TO_PARSER_NAMES.get(name, None)
        if (parser_names is None) or (not parser_names):
            object.__setattr__(self, name, value)
            return
        
        for parser_name in parser_names:
            parser_setting = PARSER_SETTINGS[parser_name]
            actual = getattr(self, name)
            object.__setattr__(self, name, value)
            if actual is DEFAULT_EVENT_HANDLER:
                if value is DEFAULT_EVENT_HANDLER:
                    continue
                
                parser_setting.add_mention(self.client_reference())
                continue
            
            if value is DEFAULT_EVENT_HANDLER:
                parser_setting.remove_mention(self.client_reference())
            continue
    
    def __delattr__(self, name):
        """
        Removes the event with switching it to `DEFAULT_EVENT_HANDLER`, and updates the event's parser if needed.
        
        Parameters
        ----------
        name : `str`
            The name of the event.
        
        Raises
        ------
        AttributeError
            The ``EventHandlerManager`` has no attribute named as the given `name`.
        """
        actual = getattr(self, name)
        if actual is DEFAULT_EVENT_HANDLER:
            return
        
        object.__setattr__(self, name, DEFAULT_EVENT_HANDLER)
        
        parser_names=EVENT_HANDLER_NAME_TO_PARSER_NAMES.get(name, None)
        if (parser_names is None) or (not parser_names):
            # parser name can be an empty string as well for internal events
            return
        
        for parser_name in parser_names:
            parser_setting = PARSER_SETTINGS[parser_name]
            parser_setting.remove_mention(self.client_reference())
    
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
        event_handler : `str`, `None`
            The matched event handler if any.
        """
        if name == 'client':
            return None
        
        try:
            actual = getattr(self, name)
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
    
    def remove(self, func, name=None, by_type=False, count=-1):
        """
        Removes the given event handler from the the event descriptor.
        
        Parameters
        ----------
        func : `Any`
            The event handler to remove.
        name : `str`, Optional
            The event's name.
        by_type : `bool`, Optional
            Whether `func` was given as the type of the real event handler. Defaults to `False`.
        count : `int`, Optional
            The maximal amount of the same events to remove. Negative numbers count as unlimited. Defaults to `-1`.
        """
        if (count == 0) or (name == 'client'):
            return
        
        name = check_name(func, name)
        
        try:
            actual = getattr(self, name)
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
                object.__setattr__(self, name, actual)
                return
        
        else:
            if by_type:
                actual = type(actual)
            
            if actual != func:
                return
        
        object.__setattr__(self, name, DEFAULT_EVENT_HANDLER)
        
        parser_names = EVENT_HANDLER_NAME_TO_PARSER_NAMES.get(name, None)
        if (parser_names is None):
            return
        
        for parser_name in parser_names:
            parser_setting = PARSER_SETTINGS[parser_name]
            parser_setting.remove_mention(self.client_reference())
        return
