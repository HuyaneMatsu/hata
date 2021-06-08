## 1.1.84 *\[2021-06-??\]*

#### Improvements

- `Guild.nsfw` is now a property.

##### hata.ext.slash

- Add `expression` converter for slash commands.

#### Bug Fixes

- Routed wrapped command's name were detected incorrectly.
- Fix a `TypeError` in `Client.webhook_get_all_channel`. (Pichu#0357)

##### hata.ext.kokoro_sqlalchemy
- `AsyncResultProxy.fetchone` returned an awaitable returning the result instead of the result.

## 1.1.83 *\[2021-06-02\]*

#### Summary

Fix up components in slash.

#### Improvements

- Add `UserBase.custom_activity`.
- Rework `UserBase.custom_activity`.
- Add `componnets` parameter to `Client.interaction_response_message_edit`.
- Add `componnets` parameter to `Client.interaction_followup_message_edit`.

##### hata.ext.slash
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

##### hata.ext.slash
- Message edition with `InteractionResponse` was not working as intended.

#### Renames, Deprecation & Removals

##### hata.ext.slash
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


##### hata.ext.extension_loader

- Load all sub files from an extension. (Pichu#0357)
- `ExtensionLoader.load_extension`, `.load`, `.unload`, `.reload` now accepts iterable and folders as well.

##### hata.ext.slash

- Commands were not getting their display name as their description by default (but their raw name).
- Routing slash commands dropped `TypeError`.

#### Bug Fixes

- Fix an `AttributeError` in `ChannelGroup._from_partial_data`.
- `ChannelThread` has no attribute `thread_users`.
- Fix a `NameError` in `_debug_component_custom_id`. (Zeref Draganeel#3581)
- Fix a `TypeError` in `Client.message_edit`. (Zeref Draganeel#3581)

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
- Convert nested component list to row. (Zeref Draganeel#3581)

#### Bug Fixes

- Fix a `NameError` in `Client.webhook_message_create`.

##### hata.ext.slash
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

- When removing all the options of an application command, they was not edited accordingly. (Zeref Draganeel#3581)
- `create_partial_guild` could drop `NameError`.
- Fix `KeyError` in `create_component`.
- `Client.interaction_response_message_create` ignored `show_for_invoking_user_only` if other fields were not present.

##### hata.ext.slash
- `name` could have higher priority when setting slash command description than `description` itself.
    (Zeref Draganeel#3581)

## 1.1.78 *\[2021-05-18\]*

#### Summary

Fix some bugs and improve slash command creation.

#### Improvements

- Add `interaction` parameter to `message.custom`. (Zeref Draganeel#3581)
- Increase `content`'s max length to 4k in `message.custom`.
- Add `components` parameter to `message.custom`. (Zeref Draganeel#3581)
- Add `thread` parameter to `message.custom`. (Zeref Draganeel#3581)
- Add `InteractionEvent.is_responding`.
- Add `InteractionEvent.is_acknowledging`.
- `InteractionEvent.wait_for_response_message` now raises `RuntimeError` if ephemeral message was sent.
- Add `Interaction.is_unanswered`.
- Add `UserFlag.certified_moderator`.

##### hata.ext.slash
- `abort` now supports `components` parameter in `show_for_invoking_user_only` mode. (Zeref Draganeel#3581)
- Slash command description defaults to it's name instead of raising an exception. (Zeref Draganeel#3581)
- Slash choices now can be any iterable object. (Zeref Draganeel#3581)
- `client` and `interaction_event` parameters are now optional for slash commands.
- `get_request_coroutines` now converts unhandled objects into `str` instances and propagates them to be sent.
    (Zeref Draganeel#3581)

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
- Fix an `AttributeError` in `Guild._delete`. (Zeref Draganeel#3581)

#### Renames, Deprecation & Removals

- Rename `InteractionEvent._response_state` to `._response_flag`.

## 1.1.77 *\[2021-05-17\]*

#### Summary

Start supporting anyio (all bugs included). (Mina Ashido]|[💻⭐#3506)

#### Improvements

##### hata.ext.asyncio
- Add `asyncio.futures.Task.get_coro`.
- Add `asyncio.base_events._run_until_complete_cb`.
- Add `asyncio.process.Process`.
- Add `asyncio.futures.Task.__weakref__`.
- Add `asyncio` functions and methods now create weakreferable tasks.

#### Bug fixed

- `CallableAnalyzer` was not adding `*args` and `**kwargs` to `.arguments`.
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

- Fix a typo on `ComponentSelect.to_data`. (Zeref Draganeel#3581)
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
    (Zeref Draganeel#3581)
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
- Improve `Guild.get_emoji_like` matching. (Zeref Draganeel#3581)

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
- Fix an `AttributeError` from `1.1.72`. (Zeref Draganeel#3581)
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
- `Button.default_style` should be `ButtonStyle.violet`. (Zeref Draganeel#3581)

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
- Add `iter_component_interactions`. (ToxicKidz#6969) (Zeref Draganeel#3581)
- Add `Slasher.add_component_interaction_waiter`.
- Add `Slasher.remove_component_interaction_waiter`.

#### Improvements

- Add `application_id` keyword to `Message.custom`.
- Add `COMPONENT_LABEL_LENGTH_MAX`. (Zeref Draganeel#3581)
- Add `COMPONENT_CUSTOM_ID_LENGTH_MAX`. (Zeref Draganeel#3581)
- `Component.style` defaults to `None`.
- Extend `Component.__repr__`.

#### Bug Fixes

- Fix a `TypeError` in `Component.__repr__`. (Zeref Draganeel#3581)
- `Message.custom` was not checking `type_` parameter.
- `is_coroutine_function` returned non-bool. (ToxicKidz#6969)
- `is_coroutine_generator_function` returned non-bool. 
- Handle python3.10 things correctly. (Zeref Draganeel#3581)
- Add a missing return to `hata.ext.async.asyncio.LifoQueue`. (ᓚᘏᗢ | NeKo Mancer#1477)

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
- Add `PaginationBase.is_active`. (Zeref Draganeel#3581)
- Add `UserMenuFactory`, `UserMenuRunner`, `UserPagination`. (Zeref Draganeel#3581)

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
- `ActivityRich.__new__` was not picking up `url` correctly. (Zeref Draganeel#3581)
- Fix a typo in `Client.role_edit` causing `AssertionError`. (Zeref Draganeel#3581)

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

- Mark keyword only parameters as keyword only in docstrings as well. (Zeref Draganeel#3581)
- `export` & `include`. (sleep-cult#3040)
- `_EventHandlerManager.remove`'s `name` parameter should be optional. (Zeref Draganeel#3581)

##### ext.slash
- Move slash sync coroutine creation to task creation to avoid resource warning at edge cases.

#### Bug Fixes

##### ext.slash
- `Slasher.__delvenet__` with unloading behavior delete was not deleting the commands. (Zeref Draganeel#3581)


## 1.1.65  *\[2021-04-14\]*

#### Summary

Lazy choice definition.

#### New Features

##### ext.slash
- Add lazy interaction choice definition. (Zeref Draganeel#3581)

#### Improvements

- Move json conversion to backend.
- Fix some spacing. (sleep-cult#3040)
- `ActivityFlag` now use lower case flag names.
- Create `urls.py` from `http.URLS` module.

#### Bug Fixes

- Fix an `AttributeError` in `User._from_client`. (Zeref Draganeel#3581)
- Fix typo `MAX_RERP_ELEMENT_LIMIT` -> `MAX_REPR_ELEMENT_LIMIT`.

##### ext.slash
- `CommandState._try_purge_from_changes` returned values in bad order. (Zeref Draganeel#3581)
- `CommandState._try_purge` returned values in bad order. (Zeref Draganeel#3581)


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
- `Icon.__repr__` displayed incorrect names. (Zeref Draganeel#3581)
- Dupe client check was not working. (Zeref Draganeel#3581)
- Fix reading readme issue on windows. (Zeref Draganeel#3581)
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
- Slash commands now instant sync if added runtime. (Zeref Draganeel#3581)

#### Optimizations

- Speed up multi client dispatch event parsers.

#### Improvements

##### ext.slash
- Add sync-time slash command addition and removal detection and handling.
- Move slash extension's parts into different files to improve readability.

#### Renames, Deprecation & Removals

##### ext.slash
- Rework `Slasher.do_main_sync` and rename to `.sync`.
