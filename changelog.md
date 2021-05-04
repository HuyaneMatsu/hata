## 1.1.74 *\[2021-05-??\]*

#### Summary

Redo error code names and thread support.

#### New Features

- Add `ChannelGuildMainBase` superclass for main
- Add `manage_threads`, `use_public_threads` and `user_private_thread` permissions.
- Add `Guild.threads`.
- Add `UserBase.thread_profiles`.
- Add `ThreadProfile`.
- Add `ThreadProfileFlag`.
- Add `Message.thread.`

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
- Rename `client_code.py` to `core.py` and move many related types and functions, like `start_clients`, `stop_clients` and `Kokoro`,
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
- Add `get_channel_stdin`. (experimental) (Charlotte|💻⭐#5644)
- Add `get_channel_stdout`. (experimental) (Charlotte|💻⭐#5644)

#### Improvements

- Update changelog style. (Pichu#0357)
- Reduce generated data size by badly built `Component` instances.
- Add debug functions for components to avoid many repeated debug checks.

##### ext.slash
- Add `edit` parameter to `SlashResponse`.
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
- Add `client.extensions`. (Charlotte|💻⭐#5644) (ᓚᘏᗢ | NeKo Mancer#1477)
- Add `EXTENSION_LOADER.get_extension`.

#### Improvements

##### ext.slash
- `Button.default_style` should be `ButtonStyle.primary`. (Zeref Draganeel#3581)

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
- Add `components` parameter to `SlashResponse`.
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
- Add `RATE_LIMIT_GROUPS.thread_get_all_self_archived`.
- Add `DiscordHTTPClient.thread_get_all_self_archived`.
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
- Fix a `NameError` in `EventLoop.create_datagram_endpoint`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `cr_pg_channel_object`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.request_members`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.message_create`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.interaction_followup_message_edit`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.interaction_followup_message_create`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.interaction_response_message_edit`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.interaction_response_message_create`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.webhook_message_edit`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.webhook_message_create`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.message_edit`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.permission_overwrite_edit`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `ApplicationCommandOption.add_option`. (Charlotte|💻⭐#5644)
- Fix a `TypeError` in `Client.interaction_response_message_edit`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.guild_edit`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.channel_edit`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.guild_user_add`. (Charlotte|💻⭐#5644)
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
