#### 1.1.70 *\[2021-04-??\]*

Full Button support incoming.


##### Internal

- Add a missing return to `hata.ext.async.asyncio.LifoQueue`. (ᓚᘏᗢ | NeKo Mancer#1477)
- Rename `Component.__init__` to `.from_data`.
- Add `Component.to_data`.
- `Component.style` defaults to `None`.
- Add `Component.__new__` as a generic constructor.
- Extend `Component.__repr__`.
- Add `Component.copy`.
- Add `Component.__eq__`.
- Add `ComponentInteraction.__eq__`.
- Add `ComponentInteraction.__hash__`.
- Add `Component.__hash__`.

#### 1.1.69  *\[2021-04-24\]*

##### Public API:

- Hata now uses api version 9. (sleep-cult#3040)
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

##### Internal:

- Rename `AsyncQue` to `AsyncQueue`.
- `Message.custom` never set `.interaction`.
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
- Remove `DiscordHTTPClient.thread_user_get_all`
- Remove `RATE_LIMIT_GROUPS.thread_user_get_all`
- Update `RATE_LIMIT_GROUPS.thread_user_add`.
- Update `DiscordHTTPClient.thread_user_add`.
- Update `RATE_LIMIT_GROUPS.thread_user_delete`.
- Update `DiscordHTTPClient.thread_user_delete`.
- Add `ERROR_CODES.unknown_approval_form`.
- Rename `ERROR_CODES.unknown_build` to `.unknown_team`.
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
- Rename `ERROR_CODES.invalid_gift_redemption_exhausted` to `.invalid_application_name`.
- Add `ERROR_CODES.authentication_required`.
- `InteractionEvent` instances are weakreferable.
- Add `InteractionResponseTypes.component`.


#### 1.1.68  *\[2021-04-23\]*

##### Public API:

- Add `Client.webhook_message_get`.
- Add `Client.interaction_response_message_get`.
- Add `GuildFeature.discoverable_disabled`.
- Add `GuildDiscovery.application_actioned`.
- Add `GuildDiscovery.application_requested`.
- Add `Guild.approximate_user_count`. (sleep-cult#3040)
- dd `Guild.approximate_online_count`. (sleep-cult#3040)
- Add `PaginationBase` base class for pagination-like objects.
- Add `PaginationBase.is_active`. (Zeref Draganeel#3524)
- Add `UserMenuFactory`, `UserMenuRunner`, `UserPagination`. (Zeref Draganeel#3524)
- Allow `API_VERSION` `9`. (sleep-cult#3040)

##### Internal:

- Add `webhook` tpe assertion to `Client.webhook_message_create`.
- Add `webhook` tpe assertion to `Client.webhook_message_edit`.
- Add `webhook` tpe assertion to `Client.webhook_message_delete`.
- Add `RATE_LIMIT_GROUPS.webhook_message_get`.
- Add `DiscordHTTPClient.webhook_message_get`.
- Add `RATE_LIMIT_GROUPS.interaction_response_message_get`.
- Add `DiscordHTTPClient.interaction_response_message_get`.
- Rename `GuildFeature.enabled_discoverable_before` to `discoverable_enabled_before`.
- Rename `GuildPreview.online_count` to `.approximate_online_count`.
- Rename `GuildPreview.user_count` to `.approximate_user_count`.
- Rename `Invite.online_count` to `.approximate_online_count`.
- Rename `Invite.user_count` to `.approximate_user_count`.
- Rename `GuildWidget.online_count` to `.approximate_online_count`.
- Rename `Guild.member_count` to `.user_count`.
- `create_partial_guild` was not setting `.user_count`.
- `Guild.precreate` was not setting `.user_count`.
- Add `Guild._update_counts_only`.
- Move out `UserBase.__rich__` methods.
- Add `WebhookBase` class. (base class for webhook likes).
- Fix an inheritance error in `ClientUserPBase.from_client`.
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
- `ActivityRich.__new__` was not picking up `url` correctly. (Zeref Draganeel#3524)
- Rename `Timeouter.__step` to `._step`.
- Rename `Task.__step` to `._step`.
- Rename `Task.__wake_up` to `._wake_up`.
- `ChooseMenu.__new__` 's `timeout`, `message`, `prefix`, `check` are now keyword only parameters.
- `Pagination.__new__`'s `timeout`, `message`, `check` are now keyword only parameters.
- `Closer.__new__`'s `timeout`, `message`, `check` are now keyword only parameters.
- Discord might not include `message.interaction` every time, so handle it.
- Discord might not include `message.content` every time, so handle it.
- Add `Message._late_init`.
- Discord might not include `message.embeds` every time, so handle it.
- Fix a typo in `Client.role_edit` causing `AssertionError`. (Zeref Draganeel#3581)

#### 1.1.67  *\[2021-04-20\]*

##### Public API:

- Add `ClientUserBase`. (base class for clients and users).
- Add `ClientUserPBase`. (base class for clients and of users if presences are enabled).
- Add normal link graves to `hata.ext.patchouli`.
- Add `StagePrivacyLevel`.
- Add `Stage`.
- Add `Client.stage_create`.
- Add `Client.stage_edit`.
- Add `Client.stage_delete`.
- Add `Client.events.stage_create`.
- Add `Client.events.stage_edit`.
- Add `Client.events.stage_delete`.

##### Internal:

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
- Fix a bad `include` call in `guild.py`.
- Add `DiscordHTTPClient.discovery_guild_get_all`. 
- Add `RATE_LIMIT_GROUPS.discovery_guild_get_all`.
- Add `RATE_LIMIT_GROUPS.GROUP_PERMISSION_OVERWRITE_MODIFY`.
- Update `RATE_LIMIT_GROUPS.permission_overwrite_delete`.
- Update `RATE_LIMIT_GROUPS.permission_overwrite_create`.
- Add `RATE_LIMIT_GROUPS.stage_delete`.
- Add `DiscordHTTPClient.stage_delete`.
- Add `ERROR_CODES.unknown_stage`.

#### 1.1.66  *\[2021-04-15\]*

##### Public API:

- Add `Guild.nsfw`.

##### Internal:

- Move slash sync coroutine creation to task creation to avoid resource warning at edge cases.
- Mark keyword only parameters as keyword only in docstrings as well. (Zeref Draganeel#3524)
- `export`. (sleep-cult#3040)
- `_EventHandlerManager.remove`'s `name` parameter should be optional. (Zeref Draganeel#3524)
- `Slasher.__delvenet__` with unloading behavior delete was not deleting the commands. (Zeref Draganeel#3524)

#### 1.1.65  *\[2021-04-14\]*

##### Internal:

- Fix some spacing. (sleep-cult#3040)
- `ActivityFlag` now use lower case flag names.
- Create `urls.py` from `http.URLS` module.
- Fix type `MAX_RERP_ELEMENT_LIMIT` -> `MAX_REPR_ELEMENT_LIMIT`.
- Move json conversion to backend.
- `CommandState._try_purge_from_changes` returned values in bad order. (Zeref Draganeel#3524)
- `CommandState._try_purge` returned values in bad order. (Zeref Draganeel#3524)
- Fix an `AttributeError` in `User._from_client`. (Zeref Draganeel#3524)
- Add lazy interaction choice definition. (Zeref Draganeel#3524)

#### 1.1.64  *\[2021-04-12\]*

##### Public API:

`CLIENTS` now uses `dict` type instead of `ClientDictionary`.

##### Internal:

- `Client._delete` could construct not a fully built `User` object. Add `User._from_client` to fix this.
- Remove `ClientDictionary`.
- Speed up `dict.get` by passing default value.
- Fix some bad assignments in `Client._delete`.
- `Icon.__repr__` did not upper case `IconType.name`. (Pichu#0357)
- `Icon.__repr__` displayed incorrect names. (Zeref Draganeel#3524)
- Dupe client check was not working. (Zeref Draganeel#3524)
- Fix reading readme issue on windows. (Zeref Draganeel#3524)
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

#### 1.1.63  *\[2021-04-11\]*

##### Public API:

- Rework `Slasher.do_main_sync` and rename to `.sync`,
- Slash commands now instant sync meanwhile added runtime. (Zeref Draganeel#3524)
- Add `ExtensionLoader.is_processing_extension`.

##### Internal:

- Speed up multi client dispatch event parsers.
- Add some new embed methods.
- Add sync-time slash command addition and removal detection and handling.
- Move slash extension's parts into different files to improve readability.
