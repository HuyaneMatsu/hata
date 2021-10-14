## 1.1.111

#### Improvements

- Add `GuildFeature.animated_banner`.
- Add `EventHandlerManager.register_plugin`.
- Do parameter count checks inside of `EventHandlerManager.__setattr__` as well.
- Add `EventHandlerPlugin` and other respective classes.

## 1.1.110 *\[2021-10-10]*

#### Bug Fixes

- `client.events.user_voice_leave` could be triggered with `client.events.user_voice_move`. Same for voice client
    events.
- `VOICE_STATE_UPDATE__CAL_SC` was not calling user events if client's voice state changed.
- `client.events.user_voice_update` could be called with bad parameter.

## 1.1.109 *\[2021-10-8\]*

### Summary

Improve auto completion and error handling of slash extension.

#### Improvements

- Add `ERROR_CODES.max_scheduled_events`.
- Add `UserFlag.bot_http_interactions`.
- Add `InvalidHandshake.response`.
- Add `InvalidHandshake.message`.
- Add `InvalidHandshake.request`.
- Add `AbortHandshake.request`.
- Add `ScheduledEvent.sku_ids`.
- Add `ScheduledEventEntityType.voice`.
- Add `ScheduledEventEntityType.location`.
- Add `manage_events` permission.
- Add `ScheduledEvent._update_attributes`.
- Add `Client.scheduled_event_create`.
- Add `Client.scheduled_event_edit`.
- Add `Client.scheduled_event_delete`.
- Add `Client.scheduled_event_get`.
- Add `Client.scheduled_event_get_all_guild`.
- Add `DiscordHttpClient.scheduled_event_create`.
- Add `DiscordHttpClient.scheduled_event_edit`.
- Add `DiscordHttpClient.scheduled_event_delete`.
- Add `DiscordHttpClient.scheduled_event_get`.
- Add `DiscordHttpClient.scheduled_event_get_all_guild`.
- Add `RATE_LIMIT_GROUPS.scheduled_event_get_all_guild`.
- Add `RATE_LIMIT_GROUPS.scheduled_event_create`.
- Add `RATE_LIMIT_GROUPS.scheduled_event_delete`.
- Add `RATE_LIMIT_GROUPS.scheduled_event_get`.
- Add `RATE_LIMIT_GROUPS.scheduled_event_edit`.
- Add `Client.events.scheduled_event_create`.
- Add `Client.events.scheduled_event_delete`.
- Add `Client.events.scheduled_event_edit`.
- Add `Client.events.scheduled_event_user_subscribe`.
- Add `Client.events.scheduled_event_user_unsubscribe`.

##### hata.ext.slash

- Auto completers now can be registered to command groups and to ``Slasher`` as well.
- Auto completers with multiple parameter names can be registered with 1 call.
- Add `.error` decorator for slasher application commands, to auto completers and to component commands.

#### Renames, Deprecation & Removals

- Rename `ScheduledEvent.scheduled_start` to `.start`.
- Rename `ScheduledEvent.scheduled_end` to `.end`.

## 1.1.108 *\[2021-10-01\]*

### Summary

Add unicode emoji support for roles.

#### Improvements

##### hata.ext.slash

- Add `first` parameter to `Slasher.error`.
- Add `create_unicode_emoji`.
- Add `Role.unicode_emoji`.
- Add `unicode_emoji` parameter to `Role.precreate`.
- Add `unicode_emoji` transformer to audit logs.
- `Client.role_edit`'s `icon` parameter now can be `Emoji` instance as well.
- `Client.role_create`'s `icon` parameter now can be `Emoji` instance as well.

#### Bug Fixes

- `create_partial_emoji_from_data` could return `Emoji` without all attribute set.
- `Client.role_edit` could raise `TypeError` if `position` is given.

#### Renames, Deprecation & Removals

- Deprecate `commands` extension.

## 1.1.107 *\[2021-09-30\]*

### Summary

Voice rework to support 3rd party libraries.

#### Improvements

- Add `VoiceServerUpdateEvent`.
- Add `Client.events.voice_server_update`.
- `VoiceState.channel` is now a property.
- Add `VoiceState.channel_id`.
- `VoiceState.user` is now a property.
- Add `VoiceState.user_id`.
- Add `Client.events.voice_client_ghost`.
- Add `VoiceState._update_channel`.
- Add `Client.events.voice_client_join`.
- Add `Client.events.voice_client_move`.
- Add `Client.events.voice_client_leave`.
- Add `Client.events.user_voice_move`.
- `Client.events.user_voice_leave` now accepts 3 parameters (from 2).
- `Guild._update_voice_state` is now a generator.
- Add `Client.events.voice_client_update`.
- Add `VoiceState._cache_user`.
- Add `Client.events.voice_client_shutdown`.
- `Client.client_login_static` could return string (instead of dict) when using custom host. (Mina Ashido]|[💻⭐#3506)
- `Embed.title` and `Embed.description` is now casted to string. (Nova#3379)
- `Embed.add_field`, `Embed.insert_field`, `_EmbedFieldsProxy.add_field` and `EmbedFieldsProxy.insert_field` now
    casts `name` and `value` parameters to string. (Nova#3379)
- `Embed.add_footer` now casts `text` parameter to string. (Nova#3379)
- `Embed.add_author` now casts `name` parameter to string. (Nova#3379)
- Add `ChannelBase.guild_id` property.
- Add `ActivityFlag.party_privacy_friends`.
- Add `ActivityFlag.party_privacy_voice_channel`.
- Add `ActivityFlag.embedded`.

#### Bug Fixes

- Fix a `NameError` in `Client.application_command_permission_edit`. (Gojo#8953)
- Fix a possible `AttributeError` in `Client.custom`. (Gojo#8953)
- `Message.custom` was not setting `.guild_id` accordingly. (Gojo#8953)
- Fix an `AttributeError` in `convert_thread_created`. (Gojo#8953)
- `Message.custom` was not marking the message as partial accordingly.
- Fix a `NameError` in `Client.message_delete_sequence`. (Gojo#8953)

#### Renames, Deprecation & Removals

- Rename `Client._gateway_for` to `.gateway_for`.
- Rename `DiscordGateway._change_voice_state` to `.change_voice_state`.
- Rename `Message.custom`'s `channel` parameter to `channel_id`.
- Deprecate `Message.custom`'s `channel`.

## 1.1.106 *\[2021-09-25\]*

### Summary

Add auto completion for slash commands.

#### Improvements

- Add `HATA_MESSAGE_CACHE_SIZE` environmental variable for easier message cache size configuration.
- Add `InteractionType.application_command_autocomplete`.
- Add `ApplicationCommandOption.autocomplete`.
- Add `INTERACTION_RESPONSE_TYPES.application_command_autocomplete_result`.
- Add `ApplicationCommandAutocompleteInteractionOption`.
- Add `ApplicationCommandAutocompleteInteraction`.

##### ext.slash

- `Slasher` now supports auto completion feature (this includes many new classes and functions). Use the
    `.autocomplete(parameter_name)` decorator on slash command to register an auto completion function.

#### Bug Fixes

##### ext.slash

- `SlasherApplicationCommand.create_event`, `SlasherApplicationCommand.create_event_from_class`
    `SlasherApplicationCommandCategory.create_event` and `SlasherApplicationCommandCategory.create_event_from_class`
    returned itself instead of the registered sub-command / sub-command-category.

## 1.1.105 *\[2021-09-21\]*

#### Improvements

- Add `ApplicationCommandOption.channel_types`.
- Add `channel_types` parameter to `ApplicationCommandOption.__new__`.
- Add `CHANNEL_TYPES.GROUP_GUILD_MESSAGEABLE`.
- Add `CHANNEL_TYPES.GROUP_GUILD_CONNECTABLE`.
- Add `CHANNEL_TYPES.GROUP_GUILD_TEXT_LIKE`.
- Add `GuildFeature.role_subscriptions_enabled`.
- Add `Attachment.temporary`.
- Add `MessageRepr.guild_id`.
- Add `MessageRepr.channel_id`.
- Add `ERROR_CODES.not_enough_guild_boosters`.

#### Bug Fixes

- `User` could be created with webhook id.
- `get_channel_id_and_message_id` could raise `AttributeError`.

##### ext.slash

- Add support for channel type specific annotations for slash commands.
- `configure_parameter` now accepts `channel_types` parameter.


## 1.1.104 *\[2021-09-15\]*

#### Improvements

- Add `client.events.shutdown`.
- Add `ERROR_CODES.rate_limit_widget_update`.
- Add `Role._create_empty`.

##### ext.extension_loader

- Absolute paths are supported.

#### Bug Fixes

- Clients could reconnect after disconnecting them with bad timing.
- `ComponentRow.copy_with` raised `NameError`. (catzoo#3026)

## 1.1.103 *\[2021-09-14\]*

#### Improvements

- `DiscordHTTPClient.guild_get` now supports query string parameters.
- Add `Client.guild_get` even tho `Client.guild_sync` exists, just to request guild specific data
    (especially user counts).
- Add `Permission.start_embedded_activities`.
- Add `role_icon_url`.
- Add `role_icon_url_as`.
- Add `Role.icon_url`.
- Add `Role.icon_url_as`.
- Add `Role.icon`.
- Add `role.icon_type`.
- Add `role.icon_type`.
- Add `icon` parameter to `Role.precreate`.
- Add `icon` parameter to `client.role_edit`.
- Add `icon` parameter to `Client.role_create`.

##### ext.slash

- `InteractionResponse` will not retrieve message if used within a `return` expression (Saving up 1 request usually).

#### Bug Fixes

- `Message._late_init` had a few bad checks, making embed and such fields to not update if needed.

## 1.1.102 *\[2021-09-??\]*

#### Improvements

- Add `EmbedThumbnail.copy`.
- Add `EmbedThumbnail.copy_with`.
- Add `EmbedVideo.copy`.
- Add `EmbedVideo.copy_with`.
- Add `EmbedImage.copy`.
- Add `EmbedImage.copy_with`.
- Add `EmbedAuthor.copy`.
- Add `EmbedAuthor.copy_with`.
- Add `EmbedFooter.copy`.
- Add `EmbedFooter.copy_with`.
- Add `EmbedField.copy`.
- Add `EmbedField.copy_with`.
- Add `EmbedBase.copy`.
- Add `EmbedBase.copy_with`.
- Add `EmbedCore.copy`.
- Add `EmbedCore.copy_with`.
- Add `Embed.copy`.
- Add `Embed.copy_with`.

#### Bug Fixes

- Fix an `AttributeError` in `Emoji._update_attributes`.

## 1.1.101 *\[2021-09-10\]*

### Summary

Stop creating functions runtime, but now we remove lambdas.

#### Improvements

- Add `GuildFeature.new_thread_permissions`.
- Ignore raised exceptions from `repr(exception)` inside of `render_exc_to_list`.

##### ext.slash

- Add `CommandState.get_active_command_count`.
- Add `Slasher.get_global_command_count`.
- Add `Slasher.get_guild_command_count`.
- Add `Slasher._get_command_count`.
- Add `Slasher.get_global_command_count_with_sub_commands`.
- Add `Slasher._get_command_count_with_sub_commands`.
- Add `Slasher.get_guild_command_count_with_sub_commands`.
- Add `CommandState.get_active_command_count_with_sub_commands`
- Add `SlasherApplicationCommand.get_real_command_count`.

##### hata.ext.asyncio

- Add `LifoQueue.get_nowait`.
- Add `Queue.get_nowait`.

#### Bug Fixes

##### ext.commands_v2

Fix an `AttributeError` caused from `CommandProcessor._add_category`.

##### hata.ext.asyncio

- `LifoQueue` and `Queue` `.get` method was not coroutine as expected. (catzoo#3026)

## 1.1.100 *\[2021-09-04\]*

### Summary

Fixing bugs.

#### Bug Fixes

- `https://bugs.python.org/issue29097` can pop up. (catzoo#3026)
- `Role._delete` could raise error (`tuple.index` raises instead of returning `-1`).

## 1.1.99 *\[2021-09-02\]*

### Summary

Use dynamic fields for messages in favor of the incoming message content intent.

#### Improvements

- `Message.reactions` now defaults to `None` (saves 64 bytes if the message has no reactions, which is like 99% of
    the cases).
- Add `ERROR_CODES.cannot_reply_without_read_message_history_permission`.
- Add `mention_channel_by_id`.
- Add `mention_role_by_id`.
- Add `mention_user_by_id`.
- Add `mention_user_nick_by_id`.
- Add `InteractionEvent.client`.
- Add `InteractionEvent.voice_client`.
- `Message.partial` works accordingly.
- Add `Message.has_partial`.
- Add `Messsage.has_channel_mentions`.
- Add `Messsage.has_type`.
- Add `Message._create_empty`.
- Add `Message._clear_cache`.
- Add `message.is_deletable`.
- Add `Message.precreate`.
- Add `preconvert_snowflake_array`.

##### ext.command_utils
- `ChannelOutputStream.flush` now forces newly written content to new message. (Gojo#8953)

#### Bug Fixes
- `unix_time_to_datetime` raised `ValueError` if received value out of the expected range. (Tari#0002)

##### ext.command_utils
- `ChannelOutputStream` made chunks of bad size. (Gojo#8953)

#### Renames, Deprecation & Removals

- Rename `Message._parse_channel_mentions` to `._get_channel_mentions`.
- Add `Message._get_role_mentions`.
- Remove unused `Message._create_unlinked`.
- Remove unused `Message._finish_init`.

## 1.1.98 *\[2021-08-28\]*

### Summary

Fixing bugs.

#### Improvements

- Add `escape_markdown`.
- Add `invitable` parameter to `Client.thread_create`.

#### Bug Fixes

- `Message.partial` returned reversed value causing different kind of issues.

## 1.1.97 *\[2021-08-25\]*

### Summary

Guild feature rework.

#### Improvements

- `GuildFeature._from_value` now correctly transforms `.name`.
- Add `GuildFeature.threads_enabled`.
- Add `GuildFeature.role_icons`.
- Guild feature names now use space instead of underscore.
- Add `GuildFeature.threads_enabled_testing`.

##### ext.patchouli
- `map_module` will no longer trigger warnings.

#### Bug Fixes

- Fix a `NameError` in `ComponentSelect.copy_with`.
- `Client.events.emoji_{}`, `Client.events.sticker_{}`, `Client.events.user_voice_{}`, `Client.events.stage_{}`
    `Client.events.user_thread_profile_edit` and  `Client.events.channel_delete` handlers were called incorrectly '
    (typo in a recent update maybe?).
- Fix `AttributeError` in `CHANNEL_DELETE__CAL_MC`.
- `Guild._update_emojis` was not cleaning up old emojis correctly.

#### Renames, Deprecation & Removals

- Rename `GuildFeature.verification_screen` to `.verification_screen_enabled`.
- Deprecate `GuildFeature.verification_screen`.
- Rename `GuildFeature.welcome_screen` to `.welcome_screen_enabled`.
- Deprecate `GuildFeature.welcome_screen`.
- Rename `GuildFeature.vip` to `.vip_voice_regions`.
- Deprecate `GuildFeature.vip`.
- Rename `GuildFeature.news` to `.announcement_channels`.
- Deprecate `GuildFeature.new`.

## 1.1.96 *\[2021-08-19\]*

### Summary

Add new emojis.

#### Improvements

- Add `ERROR_CODES.max_stickers`.
- Add `ERROR_CODES.rate_limit_prune`.
- Add `MessageType.context_command`.
- `Message.content` defaults to `None`.
- Add `Message.has_activity`.
- Add `Message.has_application`.
- Add `Message.has_application_id`.
- Add `Message.has_attachments`.
- Add `Message.has_components`.
- Add `Message.has_content`.
- Add `Message.has_cross_mentions`.
- Add `Message.has_referenced_message`.
- Add `Message.has_deleted`.
- Add `Message.has_edited_at`.
- Add `Message.has_embeds`.
- Add `Message.has_everyone_mention`.
- Add `Message.has_interaction`.
- Add `Message.has_nonce`.
- Add `Message.has_pinned`.
- Add `Message.has_reactions`.
- Add `Message.has_role_mention_ids`.
- Add `Message.has_stickers`.
- Add `Message.has_thread`.
- Add `Message.has_tts`.
- Add `Message.has_user_mentions`.
- Add `ApplicationCommand.is_context_command`.
- Add `ApplicationCommand.is_slash_command`.
- Add `send_messages_in_threads` permission.
- Add `ChannelGuildUndefined.permissions_for_roles`.
- Add `217` new emojis and fix `6` old alternative names.

#### Bug Fixes

- `GuildProfile.get_top_role` could return bad role. (from 1.1.94)
- `convert_thread_created` was not handling cases when guild is not cached.
- `Message.__len__` could return bad value for multiple message types.
- `ChannelStore.permissions_for_roles` returned `None`.
- `ChannelDirectory.permissions_for_roles` returned `None`.

##### ext.extension_loaded
- `.{}_all` methods could try to load the same extension multiple time.
- Python sets module variables late, so check globals instead.

#### Renames, Deprecation & Removals

- Deprecate `MessageType.application_command`.
- Rename `MessageType.application_command` to `.slash_command`.
- Rename `Permission.use_public_threads` to `.create_public_threads`.
- Rename `Permission.can_use_public_threads` to `.can_create_public_threads`.
- Rename `Permission.deny_use_public_threads` to `.deny_create_public_threads`.
- Rename `Permission.allow_use_public_threads` to `.allow_create_public_threads`.
- Deprecate `Permission.can_create_public_threads`.
- Deprecate `Permission.deny_create_public_threads`.
- Deprecate `Permission.allow_create_public_threads`.
- Remove unused `Permission.handle_overwrite`.
- Rename `Permission.can_use_private_threads` to `.can_create_private_threads`.
- Rename `Permission.deny_use_private_threads` to `.deny_create_private_threads`.
- Rename `Permission.allow_use_private_threads` to `.allow_create_private_threads`.
- Deprecate `Permission.can_create_private_threads`.
- Deprecate `Permission.deny_create_private_threads`.
- Deprecate `Permission.allow_create_private_threads`.

## 1.1.95 *\[2021-08-14\]*

### Summary

Sync slash extension's type names with recent application command target type addition.

#### Improvements

##### ext.extension_loaded
- `Extension.is_loaded` is a method now (from property).
- Add `Extension.is_unsatisfied`.
- Add `require`.

#### Bug Fixes

- No presence intent reduces large guild size to `0` so check presence intent when requesting guild members.
    (BrainDead#6105)
- Fix a bad intent masking, ops.

#### Renames, Deprecation & Removals

##### ext.slash
- Rename `SlashCommand` to `SlasherApplicationCommand`.
- Rename `SlashCommandParameterConversionError` to `SlasherApplicationCommandParameterConversionError`
- Rename `SlashCommandWrapper` to `SlasherCommandWrapper`.
- Rename `SlashCommandError` to `SlasherCommandError`.
- Rename `SlashCommandPermissionOverwriteWrapper` to `SlasherApplicationCommandPermissionOverwriteWrapper`.
- Rename `SlashCommandParameterConfigurerWrapper` to `SlasherApplicationCommandParameterConfigurerWrapper`.
- Rename `SlashCommandCategory` to `SlasherApplicationCommandCategory`.
- Rename `SlashCommandFunction` to `SlasherApplicationCommandFunction`.
- Rename `SlashCommand` to `SlasherApplicationCommand`.
- Rename `._add_slash_command` to `._add_application_command`.
- Rename `._remove_slash_command` to `._remove_application_command`.
- Rename `.get_should_remove_slash_commands` to `get_should_remove_application_commands`.
- Rename `._register_slash_command` to `._register_application_command`.
- Rename `._unregister_slash_command` to `._unregister_application_command`.

## 1.1.94 *\[2021-08-11\]*

### Summary

Make multiple entities to weakly bound to other ones.

#### Improvements

- Add `preconvert_float`.
- Add `message.channel_id` attribute.
- Add `message.guild_id` attribute.
- `Message.channel` is now a property.
- Add `Message.role_mention_ids`.
- `Message.role_mentions` is now a property.
- `Message` instances are now weakly bound to their channel, meaning messages can exist without their channel.
    After this channel cache will not be needed for message instances to be created.
- `InteractionEvent.__iter__` now iterates `type, user, interaction` (from `channel, user, interaction`).
- Add `InteractionEvent.channel_id` attribute.
- Add `InteractionEvent.guild_id` attribute.
- Add `InteractionEvent.channel` is now a property.
- Add `InteractionEvent.guild` is now a property.
- `InteractionEvent` is now weakly bound to it's channel and guild.
- Add `ApplicationCommandTargetType`.
- Add `ApplicationCommand.target_type`.
- `ApplicationCommand.description` is now optional for context application commands.
- Add `ApplicationCommandInteraction.resolved_messages`.
- Add `ApplicationCommandInteraction.target_id`.
- Add `ApplicationCommandInteraction.resovle_entity`.
- Add `ApplicationCommandInteraction.target`.
- `ApplicationCommandInteraction.options` is now `tuple` or `None` (from `list` or `None`)
- Add `id_to_datetime`.
- Add `id_to_unix_time`.
- Add `datetime_to_id`.
- Add `unix_time_to_id`.
- Add `datetime_to_unix_time`.
- Add `datetime_to_timestamp`.
- `ChannelGuildBase.guild_id`.
- `ChannelGuildBase.guild` is now a property.
- To `client.events.channel_delete` now only 3 parameter is passed (`client`, `channel`, from 3: `client`, `channel`,
    `guild`).
- Guild channels are now weakly bound to their guild.
- User guild profiles are now weakly bound to their guild.
- Add `ChannelGuildBase.parent_id`.
- `ChannelGuildBase.parent` is now a property.
- Add `UserBase.get_guild_profile_for`.
- Add `UserBase.iter_guild_profiles`.
- `GuildProfile.roles` is now a property.
- Add `GuildProfile.role_ids`.
- `ClientUserBase.has_role` could return `False` for default role.
- `Emoji.roles` is now a property.
- Add `Emoji.role_ids`.
- Add `iterable_of_instance_or_id_to_snowflakes`.
- `.overwrites` is now a dictionary (from list).
- Add `PermissionOverwrite.target_id`.
- Add `PermissionOverwrite.target_type`.
- Remove `._parse_overwrites`, add `parse_permission_overwrites` instead.
- Add `CHANNEL_TYPES`.
- Add `Guild.public_updates_channel_id`.
- `Guild.public_updates_channel` is nwo a property.
- Add `Guild.afk_channel_id`.
- `Guild.afk_channel` is now a property.
- Add `Guild.rules_channel_id`.
- `Guild.rules_channel` is now a property.
- Add `Guild.system_channel_id`.
- `Guild.system_channel` is now a property.
- Add `Guild.widget_channel_id`.
- `Guild.widget_channel` is now a property.
- Add `Client.guilds`.
- Add `WebhookBase.channel_id`.
- `WebhokBase.channel` is now a property.
- `User.guild_profiles` is now `guild_id` - `GuildProfile` relation (from `Guild` - `GuildProfile`).
- `User.thread_profiles` is now `None` / `thread_id` - `ThreadProfile` relation (from `None` /
    `ChannelThread` - `ThreadProfile`).
- Add `Role.guild_id`.
- `Role.guild` is now a property.
- Add `IntegrationDetail.role_id`.
- `IntegrationDetail.role` is now a property.
- Add `ChannelThread.invitable`.
- Add `invitable` parameter to `ChannelThread.precreate`.
- Add `open` parameter to `ChannelThread.precreate`.
- Add `DiscordHttpClient.guild_thread_get_all_active`.
- Add `RATE_LIMIT_GROUPS.guild_thread_get_all_active`.
- Add `Client.guild_thread_get_all_active`.
- Add `Emoji._create_unicode`.
- Add `ScheduledEventEntityMetadata`.
- Add `StageEntityMetadata`.
- Add `ScheduledEvent.channel_id`.
- Add `ScheduledEvent.entity_id`.
- Add `ScheduledEvent.entity_metadata`.
- Add `ScheduledEvent.image`.
- Add `ScheduledEvent.name`.
- Add `ScheduledEvent.scheduled_end`.
- Add `ScheduledEvent.scheduled_start`.
- Add `ScheduledEvent.__new__`.
- Add `ScheduledEvent._set_attributes`.
- Add `ScheduledEvent.__repr__`.
- Add `ScheduledEvent.entity`.
- Add `ScheduledEvent.channel`.
- Add `ScheduledEvent.guild`.
- Add `ScheduledEventEntityType.metadata_type`.
- Add `ScheduledEvent.entity_metadata`.
- Add `ScheduledEventEntityMetadata`.
- Add `StageEntityMetadata`.

##### ext.slash
- Add `target` parameter to `.interactions` decorator.
- Add `target` parameter for context commands.

#### Bug Fixes

- Fix an `AttributeError` in `Guild._delete`.
- `ChannelThread.__new__` was not setting `owner_id`.
- Deleted roles could not resolve removing their references correctly.
- `ApplicationCommandPermissionOverwrite.target` could raise `NameError`.

##### ext.slash
- Fix `AttributeError` in `SlashCommandParameterConfigurerWrapper`.

#### Renames, Deprecation & Removals

- Deprecate `id_to_time`.
- Rename `parse_time` to `timestamp_to_datetime`
- Deprecate `time_to_id`.
- Remove `Emoji._delete`.
- Remove `Sticker._delete`.
- Remove `PermissionOverwrite.taget_role`.
- Remove `PermissionOverwrite.targte_user_id`.
- Rename `.overwrites` to `.permission_overwrites`.
- Rename `._invalidate_perm_cache` to `._invalidate_permission_cache`
- Rename `._cache_perm` to `._permission_cache`.
- Rename `overwrties` parameter of `cr_pg_channel_object` to `permission_overwrties`.
- Deprecate `overwrites` parameter of `cr_pg_channel_object`.
- Rename `cr_p_overwrite_object` to `cr_p_permission_overwrite_object`.
- Deprecate `cr_p_overwrite_object`.
- Rename `ApplicationCommandPermissionOverwrite.type` to `.target_type`.
- Rename `ApplicationCommandPermissionOverwriteType` to `ApplicationCommandPermissionOverwriteTargetType`.
- Rename `ApplicationCommandPermission.add_overwrite` to `.add_permission_overwrite`.
- Rename `InteractionResponseTypes` to `INTERACTION_RESPONSE_TYPES`.
- Remove `PermissionOverwrite.id`.
- Remove `PermissionOverwrite.type`.
- Rename `CHANNEL_TYPES` to `CHANNEL_TYPE_MAP`.
- Deprecate `Client.thread_get_all_active`.
- Rename `Client.thread_get_all_active` to `.channel_thread_get_all_active`.
- Rename `RATE_LIMIT_GROUPS.thread_get_chunk_active` to `.channel_thread_get_chunk_active`.
- Rename `DiscordHttpClient.thread_get_chunk_active` to `.channel_thread_get_chunk_active`.
- Rename `request_thread_channels` to `request_channel_thread_channels`.
- Deprecate `Client.thread_get_all_archived_private`.
- Rename `Client.thread_get_all_archived_private` to `.channel_thread_get_all_archived_private`.
- Rename `DiscordHttpClient.thread_get_chunk_archived_private` to `.channel_thread_get_chunk_archived_private`.
- Rename `RATE_LIMIT_GROUPS.thread_get_chunk_archived_private` to `.channel_thread_get_chunk_archived_private`.
- Deprecate `Client.thread_get_all_archived_public`.
- Rename `Client.thread_get_all_archived_public` to `.channel_thread_get_all_archived_public`.
- Rename `DiscordHttpClient.thread_get_chunk_archived_public` to `.channel_thread_get_chunk_archived_public`.
- Rename `RATE_LIMIT_GROUPS.thread_get_chunk_archived_public` to `.channel_thread_get_chunk_archived_public`.
- Deprecate `Client.thread_get_all_self_archived`.
- Rename `Client.thread_get_all_self_archived` to `.channel_thread_get_all_self_archived`.
- Rename `DiscordHttpClient.thread_get_chunk_self_archived` to `.channel_thread_get_chunk_self_archived`.
- Rename `RATE_LIMIT_GROUPS.thread_get_chunk_self_archived` to `.channel_thread_get_chunk_self_archived`.


##### ext.slash
- Rename `SlashCommand._overwrite` to `._permission_overwrites`.
- Rename `SlashCommandPermissionOverwriteWrapper._overwrite` to `._permission_overwrite`.
- Rename `SlashCommand.add_overwrite` to `.add_permission_overwrite`.
- Rename `SlashCommand._get_sync_permission_ids` to `._get_permission_sync_ids`.
- Rename `SlashCommand.get_permission_overwrite_for` to `.get_permission_overwrites_for`.

## 1.1.93 *\[2021-08-01\]*

### Summary

Fix threads a lil bit.

#### Improvements

- Add `AuditLogEvent.scheduled_event_create`.
- Add `AuditLogEvent.scheduled_event_update`.
- Add `AuditLogEvent.scheduled_event_delete`.
- Add `privacy_level` transformer to audit logs.
- Add `ScheduledEventStatus`.
- Add `status` transformer for audit logs.
- Add `ScheduledEventEntityType`.
- Add `entity_type` transformer for audit logs.
- Add `sku_ids` transformer for audit logs.
- Add `DiscordHTTPClient.greet`.
- Add `RATE_LIMIT_GROUPS.greet`.
- Add `AuditLog.threads`.
- Add `AuditLogIterator.threads`.
- Add `ScheduledEvent` converter for audit logs.
- Add `ChannelThread` converter for audit logs.
- Add `GuildFeature.hub`.
- Add `ChannelDirectory`.
- Add `ERROR_CODES.relationship_already_friends`.
- Add `ERROR_CODES.phone_verification_required`.
- Add `ERROR_CODES.cannot_friend_self`.
- Add `ERROR_CODES.invalid_country_code`.
- Add `SKUFeatureType`.
- Add `SKUGenre`.
- Add `SKUFlag`.
- Add `SKUAccessType`.
- Add `SKUType`.
- Add `EntitlementType`.
- Add `'tweet'` extra embed type.
- Add `DiscordHTTPClient.channel_directory_counts`.
- Add `RATE_LIMIT_GROUPS.channel_directory_counts`.
- Add `DiscordHTTPClient.channel_directory_get_all`.
- Add `RATE_LIMIT_GROUPS.channel_directory_get_all`.
- Add `DiscordHTTPClient.channel_directory_search`.
- Add `RATE_LIMIT_GROUPS.channel_directory_search`.
- Add `ERROR_CODES.guild_monetization_required`.
- Add `ERROR_CODES.unknown_scheduled_event`.
- Add `ERROR_CODES.unknown_scheduled_event_user`.
- Add `ERROR_CODES.unknown_stream`.
- Add `ERROR_CODES.negative_invoice_amount`.
- Add `ERROR_CODES.unknown_billing_profile`.
- Add `ERROR_CODES.unknown_payment_source`.
- Add `ERROR_CODES.unknown_subscriptions`.
- Add `ERROR_CODES.already_subscribed`.
- Add `ERROR_CODES.invalid_plan`.
- Add `ERROR_CODES.already_cancelled`.
- Add `ERROR_CODES.invalid_payment`.
- Add `ERROR_CODES.payment_source_required`.
- Add `ERROR_CODES.already_refunded`.
- Add `ERROR_CODES.invalid_billing_address`
- Add `ERROR_CODES.already_purchased`.
- `Entity.__str__` should not default to `.name`, instead to `.__repr__`.
- Update rate limits of `thread_create` endpoint.
- Update rate limits of `thread_join` endpoint.
- Update rate limits of `thread_create_from_message` endpoint.
- Add `RATE_LIMIT_GROUPS.GROUP_THREAD_CREATE`.
- Add `RATE_LIMIT_GROUPS.GROUP_THREAD_ACTION`.
- Update rate limits of `thread_leave` endpoint.
- Update rate limits of `thread_user_add` endpoint.
- Update rate limits of `thread_user_delete` endpoint.
- Update rate limits of `thread_self_settings_edit` endpoint.
- Update rate limits of `thread_get_chunk_archived_public` endpoint.
- Update rate limits of `thread_get_chunk_self_archived` endpoint.
- Update rate limits of `thread_get_chunk_archived_private` endpoint.
- Update rate limits of `thread_get_chunk_active` endpoint.
- Update rate limits of `thread_user_get_all` endpoint.
- Add `type_` parameter to `Client.thread_create`.
- Add `ThreadProfileFlag.has_interacted`.
- Add `ThreadProfileFlag.all_messages`.
- Add `ThreadProfileFlag.only_mentions`.
- Add `ThreadProfileFlag.no_messages`.

#### Bug Fixes

- Fix an `AttributeError` in `Client.guild_sync`. (Pichu#0357)
- Fix a `NameError` in `EventThread.open_unix_connection`.
- Fix a `TypeError` in `EventTherad.create_unix_connection`.
- `User.__new__` was not setting `.thread_profiles`.
- Fix an `AttributeError` in `Client.thread_create`.
- `ChannelThread._create_empty` was not setting `.thread_users`.

#### Renames, Deprecation & Removals

- Deprecate `AuditLogChange.attr`.
- Rename `AuditLogChange.attr` to `.attribute_name`.
- Rename `StagePrivacyLevel` to `PrivacyLevel`
- Add `DiscordHTTPClient.thread_create_private` to `.thread_create`.
- Add `RATE_LIMIT_GROUPS.thread_create_private` to `.thread_create`.
- Add `DiscordHTTPClient.thread_create_public` to `.thread_create_from_message`.
- Add `RATE_LIMIT_GROUPS.thread_create_public` to `.thread_create_from_message`.
- Add `DiscordHTTPClient.thread_settings_edit` to `.thread_self_settings_edit`.
- Add `RATE_LIMIT_GROUPS.thread_settings_edit` to `.thread_self_settings_edit`.

## 1.1.92 *\[2021-07-28\]*

### Summary

Add rich creation for rich activity and for sub activity types.

#### Improvements

- Add `is_url`.
- Add `application_id` parameter to `ActivityRich`.
- Add `assets` parameter to `ActivityRich`.
- Add `created_at` parameter to `ActivityRich`.
- Add `details` parameter to `ActivityRich`.
- Add `flags` parameter to `ActivityRich`.
- Add `id_` parameter to `ActivityRich`.
- Add `party` parameter to `ActivityRich`.
- Add `secrets` parameter to `ActivityRich`.
- Add `session_id` parameter to `ActivityRich`.
- Add `state` parameter to `ActivityRich`.
- Add `sync_id` parameter to `ActivityRich`.
- Add `timestamps` parameter to `ActivityRich`.
- Add `EventThread.create_unix_connection`.
- Add `EventThread.create_unix_server`.
- Add `ComponentBase._replace_direct_sub_components`.
- Add `ComponentBase._iter_direct_sub_components`.
- Add `AuditLogEvent.thread_create`.
- Add `AuditLogEvent.thread_update`.
- Add `AuditLogEvent.thread_delete`.
- Add `auto_archive_after` transformer to audit logs.
- Add `default_auto_archive_after` transformer to audit logs.
- Add `Client.interaction_followup_message_get`.
- Add `DiscordHTTPClient.interaction_followup_message_get`.
- Add `RATE_LIMIT_GROUPS.interaction_followup_message_get`.

#### Bug Fixes

- Add missing `ComponentSelect.iter_components`.
- Handle correctly the cases, when `ComponentSelect.options` is `None`.
- `ComponentRow.components` is now `tuple`, `None` (from `list`, `tuple`, `None`).
- `ComponentSelect.options` is now `tuple`, `None` (from `list`, `None`).
- `Message.author` could be set as `WebhookRepr` for application command messages.

#### Renames, Deprecation & Removals

- Remove `Activitbase.created`.
- Rename `GuildFeature.thread_archive_3_day` to `thread_archive_three_day`.
- Rename `GuildFeature.thread_archive_7_day` to `thread_archive_seven_day`.


## 1.1.91 *\[2021-07-20\]*

### Summary

Add float type to slash commands.

#### Improvements

- Add `ApplicationCommandOptionType.float`.
- Add `ERROR_CODES.sticker_animation_duration_exceeds_5_second`.
- Add `UserBase._update`.
- Add `UserBase._update_no_return`.
- Add `ERROR_CODES.asset_size_too_large`.
- Add `ERROR_CODES.invalid_lottie_json`.
- Add `Permission.use_external_stickers`.
- Add `IntegrationExpireBehavior`.
- `IntegrationDetail.expire_behavior` is now `IntegrationExpireBehavior` type (from int).
- `Client.guild_create` limit increased 200 for nitro users.
- Rework channel message collection.
- `ActivityTimestamps.start` is now `datetime` (from int).
- `ActivityTimestamps.end` is now `datetime` (from int).
- Add `ActivityTimestamps.__new__`.
- Add `ActivityAssets.__new__`.
- Add `ActivityParty.__new__`.
- Add `ActivitySecrets.__new__`.
- Add `DiscordHTTPClient.status_incident_unresolved`.
- Add `DiscordHTTPClient.status_maintenance_active`.
- Add `DiscordHTTPClient.status_maintenance_upcoming`.
- Add `RATE_LIMIT_GROUPS.status_incident_unresolved`.
- Add `RATE_LIMIT_GROUPS.status_maintenance_active`.
- Add `RATE_LIMIT_GROUPS.status_maintenance_upcoming`.

##### ext.slash
- Add `float` converter.

#### Bug Fixes

- Fix an `AttributeError` in `Client._delete`.
- `ClientUserBase._update` always dropped back `banner_color` as edited.
- `ClientUserBase._update_no_return` reset the user's guild profiles.
- `ComponentSelect`'s `custom_id` parameter was incorrectly auto generated.

##### ext.slash
- Slash snapshot could be built badly yielding not empty difference wrongly. (bad indention)

#### Renames, Deprecation & Removals

- Remove `UserOA2.system`.
- Remove `Client.system`.
- Rename `Webhook._update` to `._set_attributes`.
- Rename `._update` to `._difference_update_attributes`.
- Rename `._update_no_return` to `._update_attributes`.
- Remove `MassUserChunker.left` (We only chunk 1 guild with it for now.)
- Rename `._update_presence` to `._difference_update_presence`.
- Rename `._update_presence_no_return` to `._difference_update`.
- Rename `._update_sizes_no_return` to `._set_sizes`.
- Rename `._update_profile_only` to `._difference_update_profile_only`.
- rename `._update_profile_only_no_return` to `._update_profile_only`.
- Rename `._update_profile` to `._difference_update_profile`.
- Rename `._update_profile_no_return` to `._update_profile`.
- Rename `DIS_ENDPOINT` to `DISCORD_ENDPOINT`
- Rename `ActivityTimestamps.__init__` -> `.from_data`.
- Rename `ActivityAssets.__init__` -> `.from_data`.
- Rename `ActivityParty.__init__` -> `.from_data`

## 1.1.90 *\[2021-07-16\]*

### Summary

Redo guild user syncing.

#### Improvements

- Add 5 second gateway connect rate limit per batch.
- Add notification when session start limit reaches low amount.
- Improve startup time of more clients by synchronizing guild member requests.
- If a client is removed from a guild meanwhile connecting, it's members wont be requested.
- Add `skip_ready_cycle`.
- `ClientUserbase.partial` is not a property (reduces ram usage).
- Do not request users if the client cannot.
- Cancel ready state on reconnect.
- `Client.events.sticker_delete` now accepts only 2 parameters (client, sticker) from 3 (client, sticker, guild).
- `Emoji.guild` is now a property, `Emoji.guild_id` is now an attribute.
- `Emoji.precreate` now accepts `guild_id` parameter instead of `guild`.
- `Client.events.emoji_delete` now accepts only 2 parameters (client, emoji) from 3 (client, emoji, guild).
- Add `UserBase.banner_color`.
- Add `banner_color` parameter to `User.precretae`.
- Add `banner_color` parameter to `Client.__new__`.
- Add `debug_options` parameters to `DiscordHTTPClient.__new__`.
- Add `http_debug_options` parameters to `Client.__new__`.
- Add `banner_color` parameter to `Client.client_edit`.
- Add `bio` parameter to `Client.client_edit`.
- Add `banner` parameter to `Client.client_edit`.

#### Bug Fixes

- Some attributes were not set by `Client.__new__`.
- Fix race conditions in `KOKORO`.
- Fix occasional `RuntimeWarning` in `AudioReader.run`.
- Fix occasional `RuntimeWarning` in `AudioPlayer.run`.

##### ext.slash
- `evaluate_two_sided_operations` returned 1 token too early.

## 1.1.89 *\[2021-07-08\]*

#### Summary

Add guild sticker methods.

#### Improvements

- Update sticker related rate limits.
- Add `DiscordHTTPClient.sticker_guild_edit`.
- Add `RATE_LIMIT_GROUPS.sticker_guild_edit`.
- Add `Sticker._update_from_partial`.
- Add `Client.sticker_guild_get`.
- Add `Client.sticker_guild_create`.
- Add `Client.sticker_guild_edit`.
- Add `Client.sticker_guild_delete`.
- Add `Client.guild_sync_stickers`.
- Add `Guild.sticker_count`.
- Add `AuditLogEvent.sticker_create`
- Add `AuditLogEvent.sticker_update`
- Add `AuditLogEvent.sticker_delete`
- `AuditLogEntry.target` now supports stickers.
- `AuditLogChange` now handles `tags` attribute accordingly.
- Add `ERROR_CODES.sticker_frame_rate_out_of_expected_range`.

##### ext.commands_v2
- Add sticker converter.

#### Bug Fixes

- `Client.sticker_get` was not updating the given sticker objects accordingly.
- `AuditLogEntry` do not raises `IndexError` if new type audit log event is received.
- Remove webhook caching per guild, since Discord API returns different data for each bot.
- `Client.message_create`'s `sticker` parameter passed as `Sticker` raised `TypeError`.

##### ext.slash
- Fix a `TypeError` in `SlashComamnd._get_sync_permission_ids`.
- Fix an `AttributeError` in `Slasher._register_command`.

#### Renames, Deprecation & Removals

- Rename `GuilFeatures.vanity` to `.vanity_invite`.
- Deprecate `GuilFeatures.vanity`.
- Rename `RATE_LIMIT_GROUPS.guild_emoji_get_all` to `.guild_emoji_get_all` (Now matches sticker endpoints).
- Rename `DiscordHTTPClient.guild_emoji_get_all` to `.guild_emoji_get_all` (Now matches sticker endpoints).
- Rename `Sticker.format_type` to `.format`.
- Deprecate `Sticker.format_type`.

## 1.1.88 *\[2021-07-03\]*

#### Summary

Fix a few bugs.

#### Improvements

- Add `ERROR_CODES.unknown_guild_member_verification_form`.
- Add `ERROR_CODES.guild_subscription_level_too_low`.
- Select component min values is `0`.
- Add `Client.webhook_get_own_channel`.
- Channel names can be 1 character long as well.
- Add `Client.interaction_application_command_acknowledge`.
- Add `ComponentSelect.enabled`.
- Add `python3 -m hata i`.
- Add `python3 -m hata v`.
- `Sticker.sort_value` defaults to `0`.
- Add `ERROR_CODES.sticker_maximum_dimensions_exceeded`.
- Add `Client.events.sticker_create`.
- Add `Client.events.sticker_delete`.
- Add `Client.events.sticker_edit`.
- Add `Sticker.available`.
- Add `Sticker._delete`.
- Add `available` parameter to `Sticker.precreate`.
- Add `Guild.sticker_limit`.

#### Bug Fixes

- Use `values` field instead of `options` when creating `ComponentInteraction` of a select.
- `CHANNEL_PINS_UPDATE` was not listed under guild messages intent.
- `'hata.discord.embed'` was not listed in `setup.py`. (Gojo#8953)
- Fix a `TypeError` in `Client.sticker_get`.

#### Renames, Deprecation & Removals

- Rename `IntentFlag.guild_emojis` to `.guild_emojis_and_stickers`.

## 1.1.87 *\[2021-06-30\]*

#### Summary

Regroup many code parts.

#### Improvements

- Add `ERROR_CODES.name_contains_disallowed_word`.
- Add `ERROR_CODES.stage_already_open`.
- Add `InviteStage`.
- Add `Invite.stage`.
- Add `Guild.stickers`.
- Add `Guild.get_sticker_like`.
- Add `Guild.get_sticker`.
- Add `Guild._update_stickers`.
- Add `Guild._sync_stickers`.
- `Guild.max_presences` now default to `0` if not received.
- Add `DiscordHTTPClient.sticker_get`.
- `Client.message_create` supports multiple embeds.
- `Client.message_edit` supports multiple embeds.
- Add `components` parameter to `Client.webhook_message_create`.
- Add `components` parameter to `Client.webhook_message_edit`.
- Add `Client.sticker_get`.
- Add `StickerPack._set_attributes`.
- Add `StickerPack._create_and_update`.
- Add `ActivityRich.track_id`.
- Add `ActivityRich.track_url`.
- Add `Sticker.partial`.
- Add `Emoji._create_empty`.
- Add `Sticker.precreate`.
- Add `Sticker._create_empty`.
- Add `available` parameter to `Emoji.precreate`.
- Add `managed` parameter to `Emoji.precreate`.
- Add `require_colons` parameter to `Emoji.precreate`.
- Add `guild` parameter to `Emoji.precreate`.
- Add `roles` parameter to `Emoji.precreate`.
- Add `user` parameter to `Emoji.precreate`.
- Add `iterable_of_instance_or_id_to_instances`.
- Add `preconvert_iterable_of_str`.
- Add `GuildFeature.ticket_events_enabled`.
- Add `GuildFeature.monetization_enabled`.
- Add `GuildFeature.more_sticker`.
- Add `GuildFeature.thread_archive_3_day`.
- Add `GuildFeature.thread_archive_7_day`.
- Add `GuildFeature.private_threads`.
- Add `UserBase._set_default_attributes`.
- Move `ClientUserBase._create_empty` up to `UserBase`.
- Add `WebhookBase._set_default_attributes`.
- Add `Webhook._set_default_attributes`.
- Move `Webhook.type` and `WebhookRepr.type` up to `WebhookBase`.
- Add `WebhookSourceGuild`.
- Add `WebhookSourceChannel`.
- Add `Webhook.source_channel`.
- Add `Webhook.source_guild`.
- Add `ComponentBase.copy_with` (and to sub classes).
- `StickerPack.cover_sticker_id` is optional.
- Add `RATE_LIMIT_GROUPS.client_guild_profile_edit`.
- Add `DiscordHTTPClient.client_guild_profile_edit`.
- Add `UserBase.banner` and related attributes, properties and methods.
- Add `Client.client_guild_profile_edit`.
- Add `banner` parameters to `Client`'s constructor.
- Add `banner` parameters to `User.precreate`.
- Add `banner` parameters to `Webhook.precreate`.
- Add `Sticker._create_partial`.
- Use `sticker_items` field instead of `sticker` in message data.

#### Bug Fixes

- `int` had higher priority, than `bool` query parameter conversion causing badly generated url.
- Fix `NameError` in `cr_pg_channel_object`.
- Fix `TypeError` in a few channel `__repr__` methods. (Pichu#0357)
- `Emoji.partial` could return bad value.
- `Emoji.__new__` could not set `.user` even if received.
- `Sticker.user` is now set correctly.
- `instance_or_id_to_instance`, `instance_or_id_to_snowflake` and `maybe_snowflake` had bad string max length check.
- `ClientUserBase._from_client` was not setting `avatar`.
- Fix a `NameError` in `Client.thread_create`.
- Fix a conversion error in `Client.thread_create`. (Gojo#8953)

##### ext.slash
- Component commands regex parsers could be generated with bad parameter index.
- Fix an `AttributeError` in `Slasher._add_component_command`.
- Fix an `AttributeError` in `Slasher._remove_component_command`.
- Fif a `TypeError` in `Slasher._add_component_command`.

#### Renames, Deprecation & Removals

- Rename `ActivityTypes` to `ACTIVITY_TYPES`.
- Deprecate `ActivityTypes`.
- Rename `Permission.manage_emojis` to `.manage_emojis_and_stickers`.
- Deprecate `Permission.can_manage_emojis`.
- Deprecate `Permission.allow_manage_emojis`.
- Deprecate `Permission.deny_manage_emojis`.
- Rename `RATE_LIMIT_GROUPS.client_edit_nick` to `.client_guild_profile_nick_edit`.
- Rename `DiscordHTTPClient.client_edit_nick` to `.client_guild_profile_nick_edit`.
- Deprecate `Client.client_edit_nick`.
- Rename `RATE_LIMIT_GROUPS.user_edit` to `.user_guild_profile_edit`.
- Rename `DiscordHTTPClient.user_edit` to `.user_guild_profile_edit`.
- Rename `Client.user_edit` to `.user_guild_profile_edit`.
- Deprecate `Client.user_edit`.

## 1.1.86 *\[2021-06-20\]*

#### Summary

Add sticker related endpoints and such.

#### Improvements

- Add `typer.__await__`. (Gojo#8953)
- Add `GuildProfile.avatar`.
- Add `UserBase.avatar_url_for`.
- Add `UserBase.avatar_url_for_as`.
- Add `UserBase.avatar_url_at`.
- Add `UserBase.avatar_url_at_as`.
- Add `StickerType.standard`.
- Add `StickerType.guild`.
- Add `Sticker.guild_id`.
- Add `Sticker.user`.
- Add `STICKERS`.
- Add `STICKER_PACKS`.
- Stickers are now cached.
- Add `Sticker._update_no_return`.
- Add `Sticker._update`.
- `Sticker.tags` use `frozsenset` + `None` (from `list` + `None`).
- Add `RATE_LIMIT_GROUPS.sticker_guild_get_all`.
- Add `DiscordHTTPClient.sticker_guild_get_all`.
- Add `ERROR_CODES.unknown_sticker`.
- Add `RATE_LIMIT_GROUPS.sticker_pack_get_all`.
- Add `DiscordHTTPClient.sticker_pack_get_all`.
- Add `RATE_LIMIT_GROUPS.sticker_guild_get`.
- Add `DiscordHTTPClient.sticker_guild_get`.
- Add `RATE_LIMIT_GROUPS.sticker_guild_create`.
- Add `DiscordHTTPClient.sticker_guild_create`.
- Add `StickerPack`.
- Add `ERROR_CODES.invalid_asset`.
- Add `ERROR_CODES.max_thread_participants`.
- Add `ERROR_CODES.message_has_thread`.
- Add `ERROR_CODES.thread_locked`.
- Add `ERROR_CODES.max_active_threads`.
- Add `ERROR_CODES.max_active_announcement_threads`.
- Add `ChannelText.default_auto_archive_after`.
- `ChannelThread.auto_archive_duration` is now in seconds to match everything else.
- Add `ERROR_CODES.max_guild_members`.

##### ext.slash
- Add regex based matching for `ComponentCommand`-s.

#### Bug Fixes

- `Client.interaction_component_message_edit` was not sending embeds.
- `Emoji._create_partial` always set `animated` as `True`.

##### ext.slash
- Parentheses evaluated by `evaluate_text` had wrong start and end index set.
- Prefix operations had higher priority than power in `evaluate_text`.

#### Renames, Deprecation & Removals

- Rename `ERROR_CODES.team_users_must_be_verified` to `team_members_must_be_verified`.

## 1.1.85 *\[2021-06-11\]*

#### Summary

Bug fixes.

#### Bug Fixes

##### ext.slash
- `default_slasher_exception_handler` could raise `TypeError`.
- `handle_command_exception` rendered `SlashCommandError`-s by default as well.
- Prefix operations were not executed on floats.

## 1.1.84 *\[2021-06-11\]*

#### Summary

Add component commands and expression parser for slash commands.

#### Improvements

- `Guild.nsfw` is now a property.
- Include date, method and url in ``DiscordException`` error message.

##### ext.slash
- Add `ComponentCommand`.
- Add `expression` converter for slash commands.
- Add `use_default_exception_handler` parameter to slasher.
- Add `Slasher.error`.

#### Bug Fixes

- Routed wrapped command's name were detected incorrectly.
- Fix a `TypeError` in `Client.webhook_get_all_channel`. (Pichu#0357)

##### ext.kokoro_sqlalchemy
- `AsyncResultProxy.fetchone` returned an awaitable returning the result instead of the result.

##### ext.commands_v2
- Converters without type could not be registered correctly.

## 1.1.83 *\[2021-06-02\]*

#### Summary

Fix up components in slash.

#### Improvements

- Add `UserBase.custom_activity`.
- Rework `UserBase.custom_activity`.
- Add `components` parameter to `Client.interaction_response_message_edit`.
- Add `components` parameter to `Client.interaction_followup_message_edit`.

##### ext.slash
- Add `event` parameter to `InteractionResponse`.
- `Slasher` now do not auto-acknowledges every potentially handled component interaction in favor of using
    `Client.interaction_component_message_edit` and `InteractionResponse` with `event` parameter.
- Add `message` parameter to `abort`.
- Add `event` parameter to `abort`.
- `InteractionResponse`'s `edit` parameter is now called `message` for consistency.
- `InteractionResponse` now will always yield back a ``Message`` instance.

#### Bug Fixes

- `InteractionResponseContext` was not marking the event responding correctly.
- Handle component remove correctly.

##### ext.slash
- Message edition with `InteractionResponse` was not working as intended.

#### Renames, Deprecation & Removals

- Remove `ChannelThread.archiver_id`.
- Remove `ChannelThread.archiver`.

##### ext.slash
- Deprecate `InteractionResponse`'s `force_new_message` parameter.

## 1.1.82 *\[2021-05-29\]*

#### Summary

Update stickers.

#### Improvements

- Rework `message.py`.
- Add `Sticker.sort_value`.
- Add `StickerType`.
- Add `Sticker.url`.
- Add `Sticker.type`.
- Add `StickerFormat.extension`.
- Add `Sticker.url_as`.
- Add `Message.sticker`.
- `Emoji.roles` now uses `None` & `tuple` (from `None` & `list`) to reduce ram usage.

#### Bug Fixes

- Make `Emoji.roles` ordered by id, to avoid derpy `client.events.emoji_edit` calls.

#### Renames, Deprecation & Removals

- Rename `StickerType` to `StickerFormat`.
- Rename `Sticker.type` to `.format_type`.
- Remove `Sticker.asset`.
- Remove `Sticker.preview_asset`.
- Rename `SlashResponse` to `Interactionresponse`.
- Deprecate `SlashResponse`.

## 1.1.81 *\[2021-05-28\]*

#### Summary

Add the rest of the thread endpoints to client.

#### Improvements

- Update discord media sizes.
- Add `Client.thread_join`.
- Add `Client.thread_leave`.
- Add `Client.thread_user_add`.
- Add `Client.thread_user_delete`.
- Add `DiscordHTTPClient.thread_user_get_all`.
- Add `RATE_LIMIT_GROUPS.thread_user_get_all`.
- Add `create_partial_channel_from_id`.
- Add `._create_empty` for each channel type.
- Add `._from_partial_data` for super channels as well.
- Add `Client.thread_user_get_all`.
- Separate `DiscordHTTPClient.thread_get_all_archived` to `.thread_get_chunk_archived_private` and
    `.thread_get_chunk_archived_public`
- Separate `RATE_LIMIT_GROUPS.thread_get_all_archived` to `.thread_get_chunk_archived_private` and
    `.thread_get_chunk_archived_public`
- Add `DiscordHTTPClient.thread_get_chunk_active`.
- Add `RATE_LIMIT_GROUPS.thread_get_chunk_active`.
- Add `Client.thread_get_all_active`.
- Add support for `datetime` query parameter.
- Add `parse_reaction`.
- Add `InteractionResponseTypes.component_message_edit`.
- Add `Client.interaction_component_message_edit`.
- Add `Client.thread_get_all_archived_public`.
- Add `Client.thread_get_all_archived_private`
- Add `Client.thread_get_all_self_archived`.


##### ext.extension_loader

- Load all sub files from an extension. (Pichu#0357)
- `ExtensionLoader.load_extension`, `.load`, `.unload`, `.reload` now accepts iterable and folders as well.

##### ext.slash

- Commands were not getting their display name as their description by default (but their raw name).
- Routing slash commands dropped `TypeError`.

#### Bug Fixes

- Fix an `AttributeError` in `ChannelGroup._from_partial_data`.
- `ChannelThread` has no attribute `thread_users`.
- Fix a `NameError` in `_debug_component_custom_id`. (Gojo#8953)
- Fix a `TypeError` in `Client.message_edit`. (Gojo#8953)

#### Renames, Deprecation & Removals

- Rename `create_partial_channel` to `create_partial_channel_from_data`.
- Rename `create_partial_user` to `create_partial_user_from_id`.
- Rename `create_partial_emoji` to `create_partial_emoji_from_data`.
- Rename `create_partial_integration` to `create_partial_integration_from_id`.
- Rename `create_partial_role` to `create_partial_role_from_id`.
- Rename `create_partial_guild` to `create_partial_guild_from_data`.
- Rename `create_partial_webhook` to `create_partial_webhook_from_id`.
- Rename `_thread_user_create` to `thread_user_create`.
- Rename `_thread_user_update` to `thread_user_update`.
- Rename `_thread_user_delete` to `thread_user_delete`.
- Rename `_thread_user_pop` to `thread_user_pop`.
- Deprecate `Client.download_url`.

## 1.1.80 *\[2021-05-22\]*

#### Summary

Rework `role.py` and `permission.py`.

#### Improvements

- Add `NsfwLevel`.
- Add `Guild.nsfw_level`.
- `get_components_data` now auto converts non rows elements to rows.
- `Client.interaction_followup_message_create` now instantly resolves `interaction.message` if applicable.
- Rework `permission.py`.
- Rework `role.py`.
- Add `PermissionOverwriteTargetType`.
- Add `parse_role_mention`.
- Add `parse_role`.
- Convert nested component list to row. (Gojo#8953)

#### Bug Fixes

- Fix a `NameError` in `Client.webhook_message_create`.

##### ext.slash
- `InteractionResponse` with `force_new_message=True` was not handling `show_for_invoking_user_only` correctly.
- When passing `allowed_mentions` or `tts` to `abort`, do not set `show_for_invoking_user_only=False` if not given.

#### Renames, Deprecation & Removals

- Rename `ButtonStyle.primary` to `.violet`.
- Rename `ButtonStyle.secondary` to `.gray`.
- Rename `ButtonStyle.success` to `.green`.
- Rename `ButtonStyle.destructive` to `.red`.
- Deprecate `ButtonStyle.primary`.
- Deprecate `ButtonStyle.secondary`.
- Deprecate `ButtonStyle.success`.
- Deprecate `ButtonStyle.destructive`.

## 1.1.79 *\[2021-05-20\]*

#### Summary

Update stages.

#### Improvements

- Add `Stage.invite_code`.
- Add `Stage._update`.
- Add `Stage._update_no_return`.
- Add `Stage.scheduled_event_id`.
- Add `Stage.discoverable`.
- Add `STAGES`.
- `Stage` are now weakreferable.
- Rework `Client.stage_edit`.
- Rework `Client.stage_delete`.
- Add `create_partial_guild_from_id`.
- Add `Guild.stages`.
- `Add Stage._delete`.
- Update `STAGE_INSTANCE_CREATE__OPT`.
- Update `STAGE_INSTANCE_UPDATE__CAL` to `STAGE_INSTANCE_UPDATE__CAL_SC`.
- Update `STAGE_INSTANCE_UPDATE__OPT`.
- Update `STAGE_INSTANCE_DELETE__CAL` to `STAGE_INSTANCE_DELETE__CAL_SC`.
- Update `STAGE_INSTANCE_DELETE__OPT`.
- Add `STAGE_INSTANCE_DELETE__CAL_MC`.
- Add `STAGE_INSTANCE_UPDATE__CAL_MC`.
- `Client.events` now accepts 3 parameters (from 2).
- `Stage.privacy_level` is now editable.
- Add `Component._iter_components`.
- `ComponentButton.custom_id` is now auto-set if needed.
- `ComponentSelect.custom_id` is now optional (moved after `options`) and auto-set if not given.
- `ComponentSelectOption` label is required.
- Add `PurchasedFlag`.
- Add `RATE_LIMIT_GROUPS.message_interaction`.
- Add `DiscordHTTPClient.message_interaction`.
- Add `RATE_LIMIT_GROUPS.stage_get`.
- Add `DiscordHTTPClient.stage_get`.
- Add `Client.stage_get`,

#### Bug fixed

- When removing all the options of an application command, they was not edited accordingly. (Gojo#8953)
- `create_partial_guild` could drop `NameError`.
- Fix `KeyError` in `create_component`.
- `Client.interaction_response_message_create` ignored `show_for_invoking_user_only` if other fields were not present.

##### ext.slash
- `name` could have higher priority when setting slash command description than `description` itself.
    (Gojo#8953)

## 1.1.78 *\[2021-05-18\]*

#### Summary

Fix some bugs and improve slash command creation.

#### Improvements

- Add `interaction` parameter to `message.custom`. (Gojo#8953)
- Increase `content`'s max length to 4k in `message.custom`.
- Add `components` parameter to `message.custom`. (Gojo#8953)
- Add `thread` parameter to `message.custom`. (Gojo#8953)
- Add `InteractionEvent.is_responding`.
- Add `InteractionEvent.is_acknowledging`.
- `InteractionEvent.wait_for_response_message` now raises `RuntimeError` if ephemeral message was sent.
- Add `Interaction.is_unanswered`.
- Add `UserFlag.certified_moderator`.

##### ext.slash
- `abort` now supports `components` parameter in `show_for_invoking_user_only` mode. (Gojo#8953)
- Slash command description defaults to it's name instead of raising an exception. (Gojo#8953)
- Slash choices now can be any iterable object. (Gojo#8953)
- `client` and `interaction_event` parameters are now optional for slash commands.
- `get_request_coroutines` now converts unhandled objects into `str` instances and propagates them to be sent.
    (Gojo#8953)

#### Bug fixed

- `edited_timestamp` can be missing from message payload.
- `type` can be missing from message payload.
- `attachments` can be missing from message payload.
- `embeds` can be missing from message payload.
- `mentions` can be missing from message payload.
- `content` can be missing from message payload.
- `mention_roles` can be missing from message payload.
- `components` can be missing from message payload.
- `Message._update` was not updating components of non guild messages.
- `Message._update_no_return` was not updating components of non guild messages.
- `IconType` `.name` and `.value` values were reversed.
- Fix an `AttributeError` in `Guild._delete`. (Gojo#8953)

#### Renames, Deprecation & Removals

- Rename `InteractionEvent._response_state` to `._response_flag`.

## 1.1.77 *\[2021-05-17\]*

#### Summary

Start supporting anyio (all bugs included). (Mina Ashido]|[💻⭐#3506)

#### Improvements

##### ext.asyncio
- Add `asyncio.futures.Task.get_coro`.
- Add `asyncio.base_events._run_until_complete_cb`.
- Add `asyncio.process.Process`.
- Add `asyncio.futures.Task.__weakref__`.
- Add `asyncio` functions and methods now create weakreferable tasks.

#### Bug fixed

- `CallableAnalyzer` was not adding `*args` and `**kwargs` to `.parameters`.
- Avoid using discord's media endpoint for attachments.

## 1.1.76 *\[2021-05-16\]*

#### Summary

Add `extensions` parameter to `Client`'s constructor.

#### New Features

- Add `extensions` parameter to `Client`'s constructor, allowing to run extension setup functions when constructing the
    client. This also means additional keyword parameters are supported to be forwarded to these setup functions.
    (Mina Ashido]|[💻⭐#3506)

#### Improvements

- Add `ERROR_CODES.max_ban_fetches`.
- Add `DiscordHTTPClient.thread_create_public`.
- Add `RATE_LIMIT_GROUPS.thread_create_public`.
- Add `Client.thread_create`.
- Add `WebhookType.applicaion`.
- Add `Message.attachment`. (Mina Ashido]|[💻⭐#3506)

#### Bug fixed

- Fix a typo on `ComponentSelect.to_data`. (Gojo#8953)
- Threads were badly bound and unbound from a guild.

##### ext.extension_loader
- Folder loading failed (typo).

#### Renames, Deprecation & Removals

- Rename `DiscordHTTPClient.create_private` to  `.thread_create_private`.
- Rename `RATE_LIMIT_GROUPS.create_private` to  `.thread_create_private`.

## *\[2021-05-14\]*

Happy Koishi day!

## 1.1.75 *\[2021-05-09\]*

#### Summary

Rework components and preinstanced types.
Refactor `client.py`, `interaction.py`, `emoji.py` and some move some types around.
Reduce `Message` entity size.

#### New Features

- Add `ComponentSelect`.
- Add `ComponentSelectOption`.
- Add ˙file` parameter to `Client.message_edit`.

#### Optimizations

- `Message.attachments` now ues `tuple` instead of `list`.
- `Message.stickers` now ues `tuple` instead of `list`.
- `Message.embeds` now ues `tuple` instead of `list`.
- `Message.components` now ues `tuple` instead of `list`.
- `Message.cross_mentions` now uses `tuple` instead of `list`.
- `Message.user_mentions` now uses `tuple` instead of `list`.
- `Message.role_mentions` now uses `tuple` instead of `list`.

#### Improvements

- Add `ComponentType.select`.
- Add `ComponentButton`.
- Add `ComponentRow`.
- Add `CreateComponent`.
- Add `PreinstancedMeta`. (sleep-cult#3040)
- Add `Preinstance`. (sleep-cult#3040)

##### ext.slash
- Update `abort`'s auto `show_for_invoking_user_only`, since now `show_for_invoking_user_only=True` supports embeds.
    (Gojo#8953)
- Add `mentionable_id` parameter support for slash commands.
- Add `configure_parameter` to overwrite slash command annotations.

#### Bug fixed

- Fix a `NmaeError` in `MessageType._from_value`.
- Fix an `AttributeError` in `ApplicationCommandPermissionOverwrite.__hash__`.
- `create_partial_emoji_data` could miss `animated` field.
- `create_partial_emoji` could miss `emoji_animated` field.
- `KeepType` always yeeted docstrings. (ᓚᘏᗢ | NeKo Mancer#1477)

#### Renames, Deprecation & Removals

- Remove `Component`.
- Rename `ComponentType.action_row` to `.row`.

## 1.1.74 *\[2021-05-05\]*

#### Summary

Redo error code names, dispatch event parsing and add thread support.

#### New Features

- Add `ChannelGuildMainBase` superclass for main.
- Add `manage_threads`, `use_public_threads` and `user_private_thread` permissions.
- Add `Guild.threads`.
- Add `UserBase.thread_profiles`.
- Add `ThreadProfile`.
- Add `ThreadProfileFlag`.
- Add `Message.thread`.
- Add `Client.events.thread_user_add`.
- Add `Client.events.thread_user_delete`.

#### Optimizations

- Use shifted mask instead of shifting and masking for sync-multi-client dispatch event parsers.

#### Improvements

- Rework `Client.webhook_get_token` to accept `webhook_id-webhook_token` pair.
- Rework `Client.webhook_delete_token` to accept `webhook_id-webhook_token` pair.
- Rework `Client.webhook_edit_token` to accept `webhook_id-webhook_token` pair.
- Rework `Client.webhook_message_create` to accept `webhook_id-webhook_token` pair.
- Rework `Client.webhook_message_edit` to accept `webhook_id-webhook_token` pair.
- Rework `Client.webhook_message_get` to accept `webhook_id-webhook_token` pair.
- Add `AllowedMentionPRoxy.update`.
- Add `ApplicationCommandOptionType.mentionable`.
- `ChannelPrivate.guild` and `ChannelGroup.guild` is now a property of `Channelbase`.
- Reduce `channel.py` size by spamming `copy_docs` calls.
- Update `ChannelThread`.
- Add `Guild_create_empty` to reduce duped code.
- Add `ERROR_CODES.invalid_action_for_archived_thread`
- Add `ERROR_CODES.invalid_thread_notification_setting`
- Add `ERROR_CODES.before_value_earlier_than_creation_time`
- Update `ChannelText.__repr__` to clarify whether the channel is announcements.
- Add `MessageType.thread_started`.
- Add `MessageFlag.MessageFlag`.
- Add `archived` parameter to `cr_pg_channel_object`.
- Add `archived_at` parameter to `cr_pg_channel_object`.
- Add `auto_archive_after` parameter to `cr_pg_channel_object`.
- Add `open_` parameter to `cr_pg_channel_object`.
- Add `ERROR_CODES.unknown_session`.
- Add `ERROR_CDEOS.unknown_store_directory_layout`.
- Add `ERROR_CODES.application_name_used`.
- Add `ERROR_CODES.invalid_role`.
- Add `ERROR_CODES.payment_source_required_to_redeem_gift`.
- Add `ERROR_CODES.guild_has_template`.
- Add `ERROR_CODES.max_bans`.
- Separate `parsers.py` into more parts to improve readability.
- Add `thread` parameter to `Client.webhook_message_create`.
- Add extra `tts` type assertion to `Client.webhook_message_create`.
- Add extra `wait` type assertion to `Client.webhook_message_create`.
- Remove non-chad aliases. (ᓚᘏᗢ | NeKo Mancer#1477)
- Improve `Guild.get_emoji_like` matching. (Gojo#8953)

#### ext.slash
- Add `mentionable` parameter support for slash commands.

#### Bug Fixes

- `Client.webhook_message_get` could raise `NameError` if called with partial webhook.
- When user caching is disabled `Guild.users` should be weak and not `User.guild_profiles`.
- `GuildProfile._update_no_return` used guild based cache, meaning it could not miss partial roles.

##### ext.asyncio
`Task.current_task`'s `loop` parameter should not be keyword only.
- Add `Queue.get`.
- Add `LifoQueue.get`.

#### Renames, Deprecation & Removals

- Rename `ChannelGuildMainBase.category` to `.parent`.
- Deprecate `ChannelGuildMainBase.category`.
- Rename `cr_pg_channel_object`'s parameter to `parent`.
- Deprecate `cr_pg_channel_object`'s `parent` parameter.
- Rename `Client.channel_move`'s `category` to `parent`.
- Deprecate `Client.channel_move`'s `parent` parameter.
- Rename `Client.channel_create`'s `category` to `parent`.
- Deprecate `Client.channel_create`'s `parent` parameter.
- Deprecate `ChannelGuildBase.parent` will be not set as `Guild` instance anymore.
- Rename `ERROR_CODES.slowmode_rate_limited` to `.rate_limit_slowmode`.
- Rename `ERROR_CODES.rate_limit_DM_open` to `.rate_limit_private_channel_opening`.
- Rename `ERROR_CODES.invalid_action_DM` to `.invalid_action_for_private_channel`.
- Rename `ERROR_CODES.user_not_connected` to `.user_not_connected_to_voice`.
- Rename `ERROR_CODES.invalid_oauth2_missing_scope` to `.invalid_oauth2_missing_scope`.
- Rename `ERROR_CODES.invalid_gift_self_redemption` to `.cannot_self_redeem_this_gift`.
- Rename `ERROR_CODES.channel_following_edit_rate_limited` to `.rate_limit_announcement_message_edit`.
- Rename `ERROR_CODES.channel_send_rate_limit` to `.rate_limit_channel_write`.
- Rename `ERROR_CODES.max_emoji` to `.max_emojis`.
- Rename `ERROR_CODES.max_animated_emoji` to `.max_animated_emojis`.
- Rename `ERROR_CODES.message_already_crossposted` to `.message_crossposted`.
- Rename `ERROR_CODES.invalid_access` to `.missing_access`.
- Rename `ERROR_CODES.invalid_widget_disabled` to `.widget_disabled`.
- Rename `ERROR_CODES.invalid_message_author` to `.cannot_edit_message_of_other_user`.
- Rename `ERROR_CODES.invalid_message_empty` to `.cannot_create_empty_message`.
- Rename `ERROR_CODES.invalid_message_send_non_text` to `.cannot_send_message_to_non_text_channel`.
- Rename `ERROR_CODES.invalid_message_verification_level` to `.channel_verification_level_too_high`.
- Rename `ERROR_CODES.invalid_oauth_app_bot` to `oauth2_application_has_no_bot`.
- Rename `ERROR_CODES.invalid_oauth_app_limit` to `oauth2_application_limit_reached`.
- rename `ERROR_CODES.invalid_oauth_state` to `.invalid_oauth2_state`.
- Rename `ERROR_CODES.invalid_permissions` to `missing_permissions`.
- Rename `ERROR_CODES.invalid_note` to `note_too_long`.
- Rename `ERROR_CODES.invalid_bulk_delete_count` to `.bulk_delete_amount_out_of_range`.
- Rename `ERROR_CODES.invalid_pin_message_channel` to `.cannot_pin_message_in_different_channel`.
- Rename `ERROR_CODES.invalid_or_taken_invite_code` to `.invite_code_invalid_or_taken`.
- Rename `ERROR_CODES.invalid_message_system` to `.invalid_action_for_system_message`.
- Rename `ERROR_CODES.invalid_channel_type` to `.invalid_action_for_this_channel_type`.
- Rename `ERROR_CODES.invalid_bulk_delete_message_age` to `.bulk_delete_message_too_old`.
- Rename `ERROR_CODES.cannot_add_user_to_guild_where_bot_is_not` to `.cannot_add_user_to_guild_where_the_bot_is_not_in`.
- Rename `ERROR_CODES.relationship_invalid_self` to `.relationship_invalid_target_self`.
- Rename `ERROR_CODES.relationship_invalid_user_bot` to `.relationship_invalid_target_bot`.
- Rename `client_code.py` to `core.py` and move many related types and functions, like `start_clients`, `stop_clients`
    and `Kokoro`,
- Rename `EventDescriptor` to `EventHandlerManager`.
- Rename `check_argcount_and_convert` to `check_parameter_count_and_convert`.
- Rename `Client.events.user_profile_edit` to `.guild_user_edit`.
- Deprecate `Client.events.user_profile_edit`.


## 1.1.73 *\[2021-05-01\]*

#### Summary

Fix some bugs.

#### New Features

- Add `AllowedMentionProxy`.

#### Improvements

- `parse_allowed_mentions` is now a standalone function and not a `Client` static method.

#### Bug Fixes

##### ext.asyncio
- Fix an `AttributeError` from `1.1.72`. (Gojo#8953)
- Add `Queue.put_nowait`. (ᓚᘏᗢ | NeKo Mancer#1477)
- Add `LifoQueue.put_nowait`. (ᓚᘏᗢ | NeKo Mancer#1477)

#### ext.slash
- `abort`'s `show_for_invoking_user_only` detected went oof when adding components.


## 1.1.72 *\[2021-04-30\]*

#### Summary

Channel input and output.

#### New Features

- Add `sanitize_content`. (experimental)

##### ext.command_utils
- Add `get_channel_stdin`. (experimental) (Mina Ashido]|[💻⭐#3506)
- Add `get_channel_stdout`. (experimental) (Mina Ashido]|[💻⭐#3506)

#### Improvements

- Update changelog style. (Pichu#0357)
- Reduce generated data size by badly built `Component` instances.
- Add debug functions for components to avoid many repeated debug checks.

##### ext.slash
- Add `edit` parameter to `InteractionResponse`.
- Add `components` parameter to `abort`.

#### Renames, Deprecation & Removals

- Rename `Message.edited` to `.edited_at`.
- Rename `EventThread.socket_sendall` to `.socket_send_all`.


## 1.1.71 *\[2021-04-26\]*

#### Summary

Split up `ext.extension_loader` to more parts and add `client.extensions`.

#### New Features

##### ext.extension_loader
- Add `Extension.short_name`.
- Add `Extension.is_loaded`. (ᓚᘏᗢ | NeKo Mancer#1477)

##### ext.extension_loader
- Add `client.extensions`. (Mina Ashido]|[💻⭐#3506) (ᓚᘏᗢ | NeKo Mancer#1477)
- Add `EXTENSION_LOADER.get_extension`.

#### Improvements

##### ext.slash
- `Button.default_style` should be `ButtonStyle.violet`. (Gojo#8953)

#### Bug Fixes

- Handle more python3.10 things correctly.

##### ext.commands
- `commands` snapshot was not correctly detecting empty snapshots.

#### Renames, Deprecation & Removals

##### ext.extension_loader
- Deprecate `EXTENSION_LOADER.extensions`.
- Rename `EXTENSION_LOADER.extensions` to `._extensions_by_name`.


## 1.1.70 *\[2021-04-26\]*

#### Summary

Improve component usage.

#### New Features

- Add `Component.to_data`.
- Add `Component.__new__` as a generic constructor.
- Add `Component.copy`.
- Add `Component.__eq__`.
- Add `ComponentInteraction.__eq__`.
- Add `ComponentInteraction.__hash__`.
- Add `Component.__hash__`.
- Add `Component.label`.
- Add `create_partial_emoji_data`.
- Add `Component.enabled`.
- Add `Message.application_id`.

##### ext.slash
- Add `Button`.
- Add `Row`.
- Add `components` parameter to `InteractionResponse`.
- Add `iter_component_interactions`. (ToxicKidz#6969) (Gojo#8953)
- Add `Slasher.add_component_interaction_waiter`.
- Add `Slasher.remove_component_interaction_waiter`.

#### Improvements

- Add `application_id` keyword to `Message.custom`.
- Add `COMPONENT_LABEL_LENGTH_MAX`. (Gojo#8953)
- Add `COMPONENT_CUSTOM_ID_LENGTH_MAX`. (Gojo#8953)
- `Component.style` defaults to `None`.
- Extend `Component.__repr__`.

#### Bug Fixes

- Fix a `TypeError` in `Component.__repr__`. (Gojo#8953)
- `Message.custom` was not checking `type_` parameter.
- `is_coroutine_function` returned non-bool. (ToxicKidz#6969)
- `is_coroutine_generator_function` returned non-bool. 
- Handle python3.10 things correctly. (Gojo#8953)
- Add a missing return to `ext.async.asyncio.LifoQueue`. (ᓚᘏᗢ | NeKo Mancer#1477)

#### Renames, Deprecation & Removals

- Rename `Component.__init__` to `.from_data`.


## 1.1.69  *\[2021-04-24\]*

#### Summary

Add components.

#### New Features

- Add `InteractionType.message_compontent`.
- Add `Component`.
- Add `Message.component`.
- Add `ComponentType`.
- Add `ButtonStyle`.
- Add `AsyncLifoQueue`.
- Add `InteractionEvent.message`.
- Add `ComponentInteraction`.
- Add `InteractionEvent.wait_for_response_message`.
- Add `InteractionEvent.InteractionEvent`.
- Add `Client.interaction_component_acknowledge`.
- Add `ComponentBase`, base class for `Component`-s for 3rd party support.
- Add `InteractionResponseTypes.component`.

#### Improvements

- Add `components` parameter to `Client.message_cerate`.
- Add `components` parameter to `Client.message_edit`.
- Add `components` parameter to `Client.interaction_response_message_create`.
- Add `components` parameter to `Client.interaction_response_followup_create`.
- Add `suppress` assertion to `Client.message_edit`.
- Hata now uses api version 9. (sleep-cult#3040)
- `InteractionEvent` instances are weakreferable.
- Add `RATE_LIMIT_GROUPS.thread_join`.
- Add `DiscordHTTPClient.thread_join`.
- Add `RATE_LIMIT_GROUPS.thread_leave`.
- Add `DiscordHTTPClient.thread_leave`.
- Add `RATE_LIMIT_GROUPS.thread_settings_edit`.
- Add `DiscordHTTPClient.thread_settings_edit`.
- Add `RATE_LIMIT_GROUPS.thread_get_all_archived`.
- Add `DiscordHTTPClient.thread_get_all_archived`.
- Add `RATE_LIMIT_GROUPS.thread_get_chunk_self_archived`.
- Add `DiscordHTTPClient.thread_get_chunk_self_archived`.
- Update `RATE_LIMIT_GROUPS.thread_user_add`.
- Update `DiscordHTTPClient.thread_user_add`.
- Update `RATE_LIMIT_GROUPS.thread_user_delete`.
- Update `DiscordHTTPClient.thread_user_delete`.
- Add `ERROR_CODES.unknown_approval_form`.
- Add `ERROR_CODES.unknown_team_member`.
- Add `ERROR_CODES.team_ownership_required`.
- Add `ERROR_CODES.max_application_game_SKUs`.
- Add `ERROR_CODES.max_teams`.
- Add `ERROR_CODES.max_companies`.
- Add `ERROR_CODES.user_in_team`.
- Add `ERROR_CODES.team_users_must_be_verified`.
- Add `ERROR_CODES.team_invitation_accepted`.
- Add `ERROR_CODES.user_identity_verification_processing`.
- Add `ERROR_CODES.user_identity_verification_succeeded`.
- Add `ERROR_CODES.authentication_required`.

#### Bug Fixes

- `Message.custom` never set `.interaction`.

#### Renames, Deprecation & Removals

- Rename `AsyncQue` to `AsyncQueue`.
- Rename `ERROR_CODES.unknown_build` to `.unknown_team`.
- Rename `ERROR_CODES.invalid_gift_redemption_exhausted` to `.invalid_application_name`.
- Remove `DiscordHTTPClient.thread_user_get_all`.
- Remove `RATE_LIMIT_GROUPS.thread_user_get_all`.

## 1.1.68  *\[2021-04-23\]*

#### Summary

`ext.command_utils` rework and user menus.

#### New Features

- Add `Client.webhook_message_get`.
- Add `Client.interaction_response_message_get`.
- Add `GuildFeature.discoverable_disabled`.
- Add `GuildDiscovery.application_actioned`.
- Add `GuildDiscovery.application_requested`.
- Add `Guild.approximate_user_count`. (sleep-cult#3040)
- Add `Guild.approximate_online_count`. (sleep-cult#3040)
- Allow `API_VERSION` `9`. (sleep-cult#3040)

##### ext.command_utils
- Add `PaginationBase` base class for pagination-like objects.
- Add `PaginationBase.is_active`. (Gojo#8953)
- Add `UserMenuFactory`, `UserMenuRunner`, `UserPagination`. (Gojo#8953)

#### Improvements

- Add `webhook` type assertion to `Client.webhook_message_create`.
- Add `webhook` type assertion to `Client.webhook_message_edit`.
- Add `webhook` type assertion to `Client.webhook_message_delete`.
- Add `RATE_LIMIT_GROUPS.webhook_message_get`.
- Add `DiscordHTTPClient.webhook_message_get`.
- Add `RATE_LIMIT_GROUPS.interaction_response_message_get`.
- Add `DiscordHTTPClient.interaction_response_message_get`.
- Add `Guild._update_counts_only`.
- Add `WebhookBase` class. (base class for webhook likes).
- Move out `UserBase.__rich__` methods.
- Discord might not include `message.interaction` every time, so handle it.
- Discord might not include `message.content` every time, so handle it.
- Add `Message._late_init` (to re-set not included parameters).
- Discord might not include `message.embeds` every time, so handle it.

##### ext.command_utils
- `ChooseMenu.__new__` 's `timeout`, `message`, `prefix`, `check` are now keyword only parameters.
- `Pagination.__new__`'s `timeout`, `message`, `check` are now keyword only parameters.
- `Closer.__new__`'s `timeout`, `message`, `check` are now keyword only parameters.

#### Bug Fixes

- Fix an inheritance error in `ClientUserPBase.from_client`.
- `create_partial_guild` was not setting `.user_count`.
- `Guild.precreate` was not setting `.user_count`.
- `ActivityRich.__new__` was not picking up `url` correctly. (Gojo#8953)
- Fix a typo in `Client.role_edit` causing `AssertionError`. (Gojo#8953)

#### Renames, Deprecation & Removals

- Rename `GuildFeature.enabled_discoverable_before` to `discoverable_enabled_before`.
- Rename `GuildPreview.online_count` to `.approximate_online_count`.
- Rename `GuildPreview.user_count` to `.approximate_user_count`.
- Rename `Invite.online_count` to `.approximate_online_count`.
- Rename `Invite.user_count` to `.approximate_user_count`.
- Rename `GuildWidget.online_count` to `.approximate_online_count`.
- Rename `Guild.member_count` to `.user_count`.
- Rename `Timeouter.__step` to `._step`.
- Rename `Task.__step` to `._step`.
- Rename `Task.__wake_up` to `._wake_up`.

##### ext.command_utils
- Rename `Pagination._canceller` to `._canceller_function`.
- Rename `Closer._canceller` to `._canceller_function`.
- Rename `ChooseMenu._canceller` to `._canceller_function`.
- Rename `Pagination.canceller` to `._canceller`.
- Rename `Closer.canceller` to `._canceller`.
- Rename `ChooseMenu.canceller` to `._canceller`.
- Rename `Pagination.task_flag` to `._task_flag`.
- Rename `Closer.task_flag` to `._task_flag`.
- Rename `ChooseMenu.task_flag` to `._task_flag`.
- Rename `Pagination.timeouter` to `._timeouter`.
- Rename `Closer.timeouter` to `._timeouter`.
- Rename `ChooseMenu.timeouter` to `._timeouter`.
- Rename `WaitAndContinue._canceller` to `._canceller_function`
- Rename `WaitAndContinue.timeouter` to `._timeouter`.
- Rename `Pagiantion.page` to `.page_index`.

## 1.1.67  *\[2021-04-20\]*

#### Summary

Add stage events and endpoints.

#### New Features

- Add `StagePrivacyLevel`.
- Add `Stage`.
- Add `Client.stage_create`.
- Add `Client.stage_edit`.
- Add `Client.stage_delete`.
- Add `Client.events.stage_create`.
- Add `Client.events.stage_edit`.
- Add `Client.events.stage_delete`.

##### ext.patchouli
- Add normal link graves.

#### Improvements

- Add `ClientUserBase`. (base class for clients and users).
- Add `ClientUserPBase`. (base class for clients and of users if presences are enabled).
- Add `video_quality_mode` transformer to audit logs.
- Update `Client.guild_create` for staff to 200.
- Add `DiscordHTTPClient.discovery_stage_get_all`.
- Add `RATE_LIMIT_GROUPS.discovery_stage_get_all`.
- Add `DiscordHTTPClient.stage_get_all`.
- Add `DiscordHTTPClient.stage_create`.
- Add `RATE_LIMIT_GROUPS.stage_get_all`.
- Add `RATE_LIMIT_GROUPS.stage_create`.
- Add `RATE_LIMIT_GROUPS.stage_edit`.
- Add `DiscordHTTPClient.stage_edit`.
- Add `DiscordHTTPClient.discovery_guild_get_all`. 
- Add `RATE_LIMIT_GROUPS.discovery_guild_get_all`.
- Add `RATE_LIMIT_GROUPS.GROUP_PERMISSION_OVERWRITE_MODIFY`.
- Update `RATE_LIMIT_GROUPS.permission_overwrite_delete`.
- Update `RATE_LIMIT_GROUPS.permission_overwrite_create`.
- Add `RATE_LIMIT_GROUPS.stage_delete`.
- Add `DiscordHTTPClient.stage_delete`.
- Add `ERROR_CODES.unknown_stage`.

#### Bug Fixes

- Fix a bad `include` call in `guild.py`.


## 1.1.66  *\[2021-04-15\]*

#### Summary

Use `export` & `include`.

#### New Features

- Add `Guild.nsfw`.

#### Improvements

- Mark keyword only parameters as keyword only in docstrings as well. (Gojo#8953)
- `export` & `include`. (sleep-cult#3040)
- `_EventHandlerManager.remove`'s `name` parameter should be optional. (Gojo#8953)

##### ext.slash
- Move slash sync coroutine creation to task creation to avoid resource warning at edge cases.

#### Bug Fixes

##### ext.slash
- `Slasher.__delvenet__` with unloading behavior delete was not deleting the commands. (Gojo#8953)


## 1.1.65  *\[2021-04-14\]*

#### Summary

Lazy choice definition.

#### New Features

##### ext.slash
- Add lazy interaction choice definition. (Gojo#8953)

#### Improvements

- Move json conversion to backend.
- Fix some spacing. (sleep-cult#3040)
- `ActivityFlag` now use lower case flag names.
- Create `urls.py` from `http.URLS` module.

#### Bug Fixes

- Fix an `AttributeError` in `User._from_client`. (Gojo#8953)
- Fix typo `MAX_RERP_ELEMENT_LIMIT` -> `MAX_REPR_ELEMENT_LIMIT`.

##### ext.slash
- `CommandState._try_purge_from_changes` returned values in bad order. (Gojo#8953)
- `CommandState._try_purge` returned values in bad order. (Gojo#8953)


## 1.1.64  *\[2021-04-12\]*

#### Summary

Fix duplicable client connections.

#### Optimizations

- Speed up `dict.get` by passing default value.

#### Improvements

- `CLIENTS` now uses `dict` type instead of `ClientDictionary`.

#### Bug Fixes

- Fix some bad assignments in `Client._delete`.
- `Icon.__repr__` did not upper case `IconType.name`. (Pichu#0357)
- `Icon.__repr__` displayed incorrect names. (Gojo#8953)
- Dupe client check was not working. (Gojo#8953)
- Fix reading readme issue on windows. (Gojo#8953)
- Fix a `TypeError` in `User._update_presence`. (from 1.1.63)
- `EventWaitforMeta._call_channel_edit` passed bad args to guild waiters.
- Fix a `NameError` in `EventLoop.create_datagram_endpoint`. (Mina Ashido]|[💻⭐#3506)
- Fix a `NameError` in `cr_pg_channel_object`. (Mina Ashido]|[💻⭐#3506)
- Fix a `NameError` in `Client.request_members`. (Mina Ashido]|[💻⭐#3506)
- Fix a `NameError` in `Client.message_create`. (Mina Ashido]|[💻⭐#3506)
- Fix a `NameError` in `Client.interaction_followup_message_edit`. (Mina Ashido]|[💻⭐#3506)
- Fix a `NameError` in `Client.interaction_followup_message_create`. (Mina Ashido]|[💻⭐#3506)
- Fix a `NameError` in `Client.interaction_response_message_edit`. (Mina Ashido]|[💻⭐#3506)
- Fix a `NameError` in `Client.interaction_response_message_create`. (Mina Ashido]|[💻⭐#3506)
- Fix a `NameError` in `Client.webhook_message_edit`. (Mina Ashido]|[💻⭐#3506)
- Fix a `NameError` in `Client.webhook_message_create`. (Mina Ashido]|[💻⭐#3506)
- Fix a `NameError` in `Client.message_edit`. (Mina Ashido]|[💻⭐#3506)
- Fix a `NameError` in `Client.permission_overwrite_edit`. (Mina Ashido]|[💻⭐#3506)
- Fix a `NameError` in `ApplicationCommandOption.add_option`. (Mina Ashido]|[💻⭐#3506)
- Fix a `TypeError` in `Client.interaction_response_message_edit`. (Mina Ashido]|[💻⭐#3506)
- Fix a `NameError` in `Client.guild_edit`. (Mina Ashido]|[💻⭐#3506)
- Fix a `NameError` in `Client.channel_edit`. (Mina Ashido]|[💻⭐#3506)
- Fix a `NameError` in `Client.guild_user_add`. (Mina Ashido]|[💻⭐#3506)
- `Client._delete` could construct not a fully built `User` object. Add `User._from_client` to fix this.

#### Renames, Deprecation & Removals

- Remove `ClientDictionary`.


## 1.1.63  *\[2021-04-11\]*

#### Summary

Sync run-time added commands instantly.

#### New Features

- Add `__bool__` methods to embed and to embed part classes.

##### ext.extension_loader
- Add `ExtensionLoader.is_processing_extension`.

##### ext.slash
- Slash commands now instant sync if added runtime. (Gojo#8953)

#### Optimizations

- Speed up multi client dispatch event parsers.

#### Improvements

##### ext.slash
- Add sync-time slash command addition and removal detection and handling.
- Move slash extension's parts into different files to improve readability.

#### Renames, Deprecation & Removals

##### ext.slash
- Rework `Slasher.do_main_sync` and rename to `.sync`.
