## 1.3.51 *\[2024-03-18\]*

#### Improvements

- Add `Locale.spanish_la`.
- Add `create_partial_sticker_from_id`.
- `DiscordException.status` is now cached (to enable modifying it).
- `DiscordException.retry_after` is now cached (to enable modifying it).
- `DiscordException.code` now supports setting & deleting (resetting).
- `DiscordException.debug_info` now supports setting & deleting (resetting).
- `DiscordException.errors` now supports setting & deleting (resetting).
- `DiscordException.request_info` now supports setting & deleting (resetting).
- `DiscordException.message` now supports setting & deleting (resetting).
- `DiscordException.response` now can be `None` (to enable more relaxed constructing).
- `Client.webhook_message_create` now creates a thread channel as would been intended.
    Also stores the created message accordingly.

### Bug fixes

- `AllowedMentionProxy.from_data` parsed allowed role ids always as empty.
- `AllowedMentionProxy.to_data` did not handle nothing is allowed case correctly.
- `AllowedMentionProxy.__or__` handled `._allow_replied_user` cases incorrectly.
- `AllowedMentionProxy.__sub__` handled `._allow_replied_user` cases incorrectly.
- `AllowedMentionProxy.__and__` handled `._allowed_role_ids` cases incorrectly.
- `AllowedMentionProxy.__and__` handled `._allowed_user_ids` cases incorrectly.
- `AllowedMentionProxy.__sub__` handled `._allowed_role_ids` cases incorrectly.
- `AllowedMentionProxy.__sub__` handled `._allowed_user_ids` cases incorrectly.
- `AllowedMentionProxy.allowed_users.fset` did not accept standalone user instance as expected.
- `normalize_executed_file` could raise on windows. (al_loiz_icu)
- `Client.guild_create` required `afk_timeout` parameter as non-default or else it raised. (tari._.)

### Renames, Deprecations & Removals

- Rename `create_forum_tag_from_id` to `create_partial_forum_tag_from_id`.

## 1.3.50 *\[2024-02-03\]*

#### Improvements

- Add `Client.api` to separate down the api logic from `Client.http`. `Client.http` is not a general `HttpClient`.
- Add `DiscordApiClient` to separate the api logic down from `DiscordHTTPClient`.
- Add `http` parameter to `Client.__new__`.
- Add `api` parameter to `Client.__new__`.
- Add `DiscordGatewayBase` as a base type for gateways.
- Add `DiscordGatewayBase.abort` to instantly abort connections on unexpected shutdown.
- Add tests for client gateway.
- Do not start `VoiceClient` in `.__new__`, instead add a new `.start` method.

### Bug fixes

- `Client.sticker_create` failed if `tags` were given as `None` or as an empty container.
- Fix incorrect reconnect attempt on lost internet connection causing a shard to go dormant if sharded.
- Fix incorrect handling of `GeneratorExit` in `Client._connect`.
- Fix incorrect handling of `session_id` in `VoiceClient`.
- Fix typo in `DiscordGatewayVoice._resume`.
- Fix incorrect handling of `GeneratorExit` in `VoiceClient._connect`.
- `VoiceClient._token` was not set in the constructor.
- Fix `AutoModerationRule.__repr__` raised when rendering non-default `.event_type`.

#### ext.slash
- Fix could not overwrite `menu.attribute` if attribute was previously set to a component.

### Renames, Deprecations & Removals

- Deprecate `DiscordHTTPClient`, use `DiscordApiClient` instead.
- Rename `DiscordGatewaySharder` to `DiscordGatewayClientSharder`.
- Rename `DiscordGateway` to `DiscordGatewayClientShard`.

## 1.3.49 *\[2023-12-31\]*

#### Improvements

- Use new scarletio in dependencies.

## 1.3.48 *\[2023-12-17\]*

### Improvements

- Add `31` new unicode emojis.
- Add `Unicode.unicode_aliases`.
- Add `Unicode.iter_unicode_aliases`.

### Bug fixes

- `repr(DiscordException)` was not called when rendering traceback. (From 1.3.47.)

### Renames, Deprecations & Removals

- Deprecate command routing by giving a parameter as tuple. Please use multiple decorators instead. Turns out this
    was broken already at many places.
- Deprecate from class command constructors. Please use a decorator instead. Turns out this was broken already at
    many places.
- Rename `ContentFilterLevel` to `ExplicitContentFilterLevel` to match it better what it exactly does.
- Rename `content_filter` to `explicit_content_filter_level` to match it better what it exactly does.
- Rename `MFA` to `MfaLevel` to match it better what it exactly does.
- Rename `mfa` to `mfa_level` to match it better what it exactly does. (Case of guilds.)
- Rename `message_notification` to `default_message_notification_level` to match it better what it exactly does.
- Rename `mfa` to `mfa_enabled` to match it better what it exactly does. (Case of users.)
- Rename `MFA` in error codes to `mfa`.

## 1.3.47 *\[2023-12-09\]*

### Improvements

- Add set `length` limit to `Component.url`.
- Add set `length` limit to `Embed.url`.
- Add set `length` limit to `EmbedAuthor.url`.
- Add set `length` limit to `EmbedAuthor.icon_url`.
- Add set `length` limit to `EmbedFooter.icon_url`.
- Add set `length` limit to `EmbedImage.url`.
- Add set `length` limit to `EmbedProvider.url`.
- Add set `length` limit to `EmbedThumbnail.url`.
- Add set `length` limit to `EmbedVideo.url`.
- `Client.onboarding_screen_edit` now flattens emojis in `screen.prompts?[n].options?[n]`.
- Add `Application.guild`.
- Add `Application.approximate_guild_count`.
- Add new `DiscordHTTPClient.application_get_own`. Rename old to `.oauth2_application_get_own`.
- Add new `RATE_LIMIT_GROUPS.application_get_own`. Rename old to `.RATE_LIMIT_GROUPS`.
- Update stored embedded activities.
- Add `OrientationLockState`.
- Add `PlatformType`.
- Add `LabelType`.
- Add `ReleasePhase`.
- Add `ClientPlatformConfiguration`.
- Add `EmbeddedActivityConfiguration`.
- Add `Application.embedded_activity_configuration`.
- Add `Application.monetized`.
- Add `ApplicationMonetizationState˙.
- Add `Application.creator_monetization_state`.
- Add `SKUFlag.creator_monetization`.
- Add `SKUFlag.guild_product`.
- Add `SKUType.package`.
- Add `SKUType.giftable`.
- Add `ApplicationVerificationState`.
- Add `ApplicationFlag.iframe_form`.
- Add `ApplicationDiscoveryEligibilityFlags`.
- Add `ApplicationDiscoverabilityState`.
- Add `ApplicationExplicitContentFilterLevel`.
- Add `ApplicationInteractionVersion`.
- Add `ApplicationMonetizationEligibilityFlags`.
- Add `ApplicationStoreState`.
- Add `ApplicationRPCState`.
- Add `Application.discoverability_state`.
- Add `Application.discovery_eligibility_flags`.
- Add `Application.explicit_content_filter_level`.
- Add `Application.integration_public`.
- Add `Application.integration_requires_code_grant`.
- Add `Application.interaction_endpoint_url`.
- Add `ApplicationInteractionEventType`.
- Add `Application.interaction_event_types`.
- Add `Application.iter_interaction_event_types`.
- Add `Application.interaction_version`.
- Add `ApplicationInternalGuildRestriction`.
- Add `Application.internal_guild_restriction`.
- Add `Application.redirect_urls`.
- Add `Application.monetization_eligibility_flags`
- Add `Application.monetization_state`.
- Add `Application.iter_redirect_urls`.
- Add `Application.rpc_state`.
- Add `Application.store_state`.
- Add `Application.verification_state`.
- Add `ApplicationOverlayMethodFlags`.
- Add `Application.overlay_method_flags`.
- Add `ERROR_CODES.cloudflare_block`.
- Add `EmbedType.gift`.
- Add `EmbedType.safety_policy_notice`.
- Add `MessageType.purchase_notification`.
- Update `MessageType.welcome`'s formatter.
- Update `MessageType.guild_incidents_disable`'s formatter.
- Update `MessageType.guild_incidents_enable`'s formatter.
- Update `MessageType.private_channel_integration_add`'s formatter.
- Update `MessageType.private_channel_integration_remove`'s formatter.
- Update `MessageType.application_subscription`'s formatter.
- Update `MessageType.role_subscription_purchase`'s formatter.
- Update `MessageType.thread_created`'s formatter.
- Add `reason` parameter to `Client.channel_follow`.
- Add `reason` parameter to `DiscordHTTPClient.channel_follow`.
- Move guild permission cache reset from dispatch event parsers to the client type directly.
- Add `applied_tag_ids` parameter to `Client.webhook_message_create`.
- Add `thread_name` parameter to `Client.webhook_message_create`.
- `Application.to_data` now is used for templating. Warning is only dropped when `include_internals` is given as `True`.
- Add `Application.application_edit_own`.
- Add `DiscordHTTPClient.application_edit_own`.
- Add `RATE_LIMIT_GROUPS.application_edit_own`.
- `DiscordException` is now slotted.

### Bug fixes

- Fix `Embed.post_review` should have been `.post_preview` (typo).

### Renames, Deprecations & Removals

- Rename `Channel.default_thread_reaction` to `.default_thread_reaction_emoji` to be aligned with the new reactions
    structure.
- Rename `Application.bot_require_code_grant` to `.bot_requires_code_grant`.
- Rename `MessageType.application_subscription` to `.application_guild_subscription`.

## 1.3.46 *\[2023-11-26\]*

### Improvements

- Add `ClientWrapper.__iter__`.
- Add `ClientWrapper.__contains__`.
- Add `ClientWrapper.__eq__`.
- Add `ClientWrapperEventsProxy.__repr__`.
- Add `ClientWrapperEventsProxy.__eq__`.
- Add `ClientWrapperEventsProxy.__delattr__`.
- Add `ClientWrapperEventsProxy.__setattr__`.

#### ext.slash

- Routed command registration output now supports registering nested commands.
- Routed command registration output now supports registering auto completers.
- Routed command registration output now supports registering exception handlers.
- Add `AutocompleteInterface` to group up autocomplete logic.
- Add `CommandInterface` to group up command logic (not much at this case).
- Add `ExceptionHandlerInterface` to group up exception handler logic.
- Add `NestableInterface` to group up nesting logic.
- Add `SelfReferenceInterface` to group up self-reference logic.

### Renames, Deprecations & Removals

- Rename `ClientWrapper._events_wrapper` to `ClientWrapperEventsProxy`.
- `ClientWrapper.__delattr__` removed.
- `ClientWrapper.__setattr__` removed.

## 1.3.45 *\[2023-11-19\]*

### Improvements

- Add `ERROR_CODES.entitlement_already_granted`.
- Add `ERROR_CODES.invalid_sku`.
- Now rate limit handler handles missing headers better in case Discord shits itself.
- Now icon converter handles the case when discord returns incorrect base16 128 bit hash.
- Now `VOICE_STATE` dispatch event handler handles when discord returns no user.
- Add actually working `emoji` audit log change conversions for soundboard sounds.
- Add `permission_overwrite` audit log change conversion for application commands.

#### ext.plugin_loader

- `import_plugin` now drops `RuntimeError` if called from `KOKORO`.

### Bug fixes

- Fix `timedelta_to_id_difference` did not convert days or bigger units.
- Some audit log change conversions were built badly failing `.to_data`.
- Fix `TypeError` in `GUILD_AUDIT_LOG_ENTRY_CREATE`. (from 1.3.44)

### Renames, Deprecations & Removals

- Remove `AuditLogChange.is_modification`, `.is_addition` and `.is_removal`.
    The whole system had to be remade again to support the missing entries.

## 1.3.44 *\[2023-10-31\]*

### Improvements

- Add `AvatarDecoration`. The old `.avatar_decoration` attributes are updated.
- Add `AuditLogEvent.none`.
- Add missing `integration_type` converter for audit log details.
- Add `AuditLogTargetType.detail_conversions`.
- Add `AuditLogTargetType.message`.
- Add `AuditLogChange.flags`.
- Add `AuditLogChange.__eq__`.
- Add `AuditLogChange.__hash__`.
- Add `AuditLogChange.has_before`.
- Add `AuditLogChange.has_after`.
- Add `AuditLogChange.is_modification`.
- Add `AuditLogChange.is_addition`.
- Add `AuditLogChange.is_removal`.
- Add `AuditLogEntryDetailConversion`.
- Add `AuditLogEntryDetailConversionGroup`.
- Add `AuditLogChange.from_fields`.
- Add `AuditLogEntryChangeConversion`.
- Add `AuditLogEntryChangeConversionGroup`.
- Add `mention_limit` audit log converter.
- Add `raid_protection` audit log converter.
- Add `flags` audit log converter (for user conversions).
- Add `AuditLogChange.create_clean`.
- Add `AuditLogEntry.created_at`.
- Add `AuditLogEntry.__eq__`.
- Add `AuditLogEntry.__hash__`.
- Add `AuditLogEntry.get_change`.
- Add `AuditLogEntry.iter_changes`.
- Add `AuditLogEntry.get_detail`.
- Add `AuditLogEntry.iter_details`.
- Add `AuditLogEntry.__new__`.
- Add `AuditLogEntry.to_data`.
- Add `AuditLogEntry.precreate`.
- Add `AuditLogEntry.copy`.
- Add `AuditLogEntry.copy_with`.
- Add `ApplicationCommand.precreate`.
- Add `SoundboardSound` target conversion to audit logs.
- Add `AuditLogEntryTargetType.soundboard_sound`.
- Add soundboard sound conversion for audit log changes.
- Add `Inviter.inviter_id`.
- Add `GuildProfileFlag` audit log change converter.
- Add `InviteFlag` audit log change converter.
- Add `channel_id` audit log detail conversion for application command related entries.
- Add `StickerType` audit log change converter.
- Add `id` audit log detail conversion for channel related entries.
- Add `bypasses_verification` audit log change converter for user related entries.
- Add `IntegrationType` audit log change converter.
- Add `guild_id` audit log detail conversion for application command related entries.
- Add `OnboardingMode` audit log change converter.

#### ext.slash
- Add `InteractionAbortedError.__eq__`.
- Add `InteractionAbortedError.__hash__`.
- Add `InteractionResponse.__hash__`.
- Add `InteractionResponse.set_abort`.
- `InteractionAbortedError` is now directly importable.

### Bug fixes

- Fix `TypeError` in `Client.channel_thread_get_all_archived_private`.
- Fix `TypeError` in `Client.channel_thread_get_all_archived_public`.
- Fix `TypeError` in `Client.channel_thread_get_all_self_archived`.

### Renames, Deprecations & Removals

- Rename `AuditLogEvent.member_kick` to `.user_kick`. Deprecate `.member_kick`.
- Rename `AuditLogEvent.member_prune` to `.user_prune`. Deprecate `.member_prune`.
- Rename `AuditLogEvent.member_ban_add` to `.user_ban_add`. Deprecate `.member_ban_add`.
- Rename `AuditLogEvent.member_ban_remove` to `.user_ban_remove`. Deprecate `.member_ban_remove`.
- Rename `AuditLogEvent.member_update` to `.user_update`. Deprecate `.member_update`.
- Rename `AuditLogEvent.member_role_update` to `.user_role_update`. Deprecate `.member_role_update`.
- Rename `AuditLogEvent.member_move` to `.user_move`. Deprecate `.member_move`.
- Rename `AuditLogEvent.member_disconnect` to `.user_disconnect`. Deprecate `.member_disconnect`.
- Rename `Icon.from_base16_hash` to `.from_base_16_hash`. Deprecate `.from_base16_hash`.
- Rename `Client.integration_edit`'s `enable_emojis` parameter to `emojis_enabled`.
- Rename `AuditLogEntry.__new__` to `.from_data`.
- Rename `AuditLogTargetType` to `AuditLogEntryTargetType`
- Rename `AuditLogEvent` to `AuditLogEntryType`.
- Rename `event` parameters representing `AuditLogEvent` to `entry_type`. 
- Remove `AuditLogEntryTargetType.thread`. Now it would be same as `.channel`.

## 1.3.43 *\[2023-10-15\]*

### Improvements

- Add `create_partial_guild_from_interaction_guild_data`.
- `InteractionEvent.guild` is now an attribute using recently added `guild` field in the payload.
    This makes `.guild_id` and `.guild_locale` properties.
- Add `Message.resolved`.
- Add `EntitySelectDefaultValueType`.
- Add `EntitySelectDefaultValue`.
- Add `ComponentMetadataEntitySelectBase`.
- Add `ComponentMetadataBase.default_values`.
- Add `Component.default_values`.
- Add `Component.iter_default_values`.
- Component constructor functions now omit default values, to validation later.

### Bug fixes

- `ScheduledEvent.guild` could return non-None if a guild with id of `0` was cached.

### Renames, Deprecations & Removals

- `Guild.preferred_locale` is now `.locale`.
- Deprecate `Guild.preferred_locale`.
- Rename `InteractionEvent.locale` to `.user_locale`.
- Deprecate `InteractionEvent.locale`.
- `InteractionComponent`'s `type_` parameters renamed to `component_type`.

## 1.3.41 *\[2023-10-08\]*

### Improvements

- Enable setting `scheduled_event_id` of `Stage`.
- Add InteractionResponseType.require_subscription`.
- Add `Client.interaction_require_subscription`.
- Add `SKUType.guild_role`.
- Add `SKUType.giftable`.
- Add `SKUType.application_guild_subscription`.
- Add `SKUType.application_user_subscription`.
- Add `MessageType.guild_incidents_report_raid`.
- Add `MessageType.guild_incidents_report_false_alarm`.
- Add `MessageType.guild_chat_revive`.
- Add `MessageType.custom_gift`.
- Add `MessageType.guild_gaming_stats`.
- Add `MessageType.poll`.
- Add `SKUType.subscription_group`.
- Move `EMBEDDED_ACTIVITY_NAME_TO_APPLICATION_ID` and related under `application/application/constants`.
- Add `SKU`.
- Add `SKUS`.
- Add `Entitlement`.
- Add `ENTITLEMENTS`.
- Add `EntitlementOwnerType`.
- Add `InteractionEvent.entitlements`.
- Add `InteractionEvent.has_entitlement`.
- Add `InteractionEvent.iter_entitlements`.
- Add `InteractionEvent.has_sku`.
- Update rate limit handlers to ignore rate limit headers they are not responsible to handle.
- Add `RATE_LIMIT_GROUPS.entitlement_get_chunk`.
- Add `RATE_LIMIT_GROUPS.sku_get_all`.
- Add `RATE_LIMIT_GROUPS.entitlement_create`.
- Add `RATE_LIMIT_GROUPS.entitlement_delete`.
- Add `DiscordHTTPClient.sku_get_all`.
- Add `DiscordHTTPClient.entitlement_get_chunk`.
- Add `DiscordHTTPClient.entitlement_create`.
- Add `DiscordHTTPClient.entitlement_delete`.
- Add `Client.entitlement_create`
- Add `Client.entitlement_delete`
- Add `Client.entitlement_get_chunk`
- Add `Client.entitlement_get_all`
- Add `Client.sku_get_all`.
- Add `Client.events.entitlement_create`.
- Add `Client.events.entitlement_delete`.
- Add `Client.events.entitlement_update`.

### Renames, Deprecations & Removals

- Rename `SKUFeatureType` to `SKUFeature`.

## 1.3.40 *\[2023-09-30\]*

### Improvements

- Add `GuildInventorySettings`.
- Add `Guild.inventory_settings`.
- Add `RATE_LIMIT_GROUPS.guild_inventory_settings_edit`.
- Add `DiscordHTTPClient.guild_inventory_edit`.
- Add `Client.guild_inventory_settings_edit`.
- Add `GuildIncidents`.
- Add `Guild.incidents`.
- Add `RATE_LIMIT_GROUPS.guild_incidents_edit`.
- Add `DiscordHTTPClient.guild_inventory_edit`.
- Add `Client.guild_incidents_edit`.
- Add `MessageType.guild_incidents_enable`.
- Add `MessageType.guild_incidents_disable`.
- Add `timed_out_until` parameter to `Client.user_guild_profile_edit`.
    Now its purpose is different from the `duration` one.
- Remove `timeout_duration` parameter of `Client.guild_profile_edit`. You could never actually edit it.
- Remove `email` and `password` parameters of `Client.edit`. Also `bio` since it is not working.
- Change `Embed.__repr__` to `.get_short_repr`. Add new detailed `.__repr__` instead.
    (Its just hard to debug with short repr.)

### Bug fixes

- `Client.edit` raised `AttributeError`.

##### ext.commands_v2
- `guild_converter` failed for a long time (probably).

## 1.3.39 *\[2023-09-17\]*

### Improvements

- Add `AutoModerationRuleTriggerType.user_profile`.
- Add `AutoModerationEventType.user_update`.
- Add `AutoModerationActionType.block_user_interaction`.
- Add `ChannelMetadataBase.status`.
- Add `Channel.status`.
- Implement `.status` at `ChannelMetadataGuildVoice`.
- Add `AuditLogEvent.channel_status_update`.
- Add `AuditLogEvent.channel_status_delete`.
- Add `status` detail converter.
- Add `VOICE_CHANNEL_STATUS_UPDATE` parser.
- Add `CHANNEL_TOPIC_UPDATE` parser.
- Add `Client.channel_edit_status`.
- Add `DiscordHTTPClient.channel_edit_status`.
- Add `RATE_LIMIT_GROUPS.channel_edit_status`

## 1.3.38 *\[2023-09-09\]*

### Improvements

- Add `ReactionAddEvent.type`.
- Add `ReactionAddEvent.reaction`.
- Add `ReactionMapping.reaction_count`.
- Add `ReactionMapping.copy`.
- `ReactionMapping` is now `Reaction` - `ReactionMappingLine` relation.
- Rebrand twitter :rocket:.
- Add `ConnectionType.domain`.
- Add `set_voice_channel_status` permission.
- `Client.reaction_add` no longer accepts the new `reaction_type` parameter, instead the `emoji`
    (or `reaction` as it is called now) accepts `Reaction` instance.
- `Client.reaction_delete` now accepts `Reaction` as its `emoji` (or `reaction` as it is called now) parameter.
- `Client.reaction_delete_own` now accepts `Reaction` as its `emoji` (or `reaction` as it is called now) parameter.
- `Client.reaction_user_get_chunk` now accepts `Reaction` as its `emoji` (or `reaction` as it is called now) parameter.
- `Client.reaction_user_get_all` now accepts `Reaction` as its `emoji` (or `reaction` as it is called now) parameter.
- `Client.reaction_get_all` now requests non-standard reactions as well.

## 1.3.37 *\[2023-09-03\]*

### Improvements

- Add `TeamMemberRole`.
- Add `TeamMember.role`.
- Repurpose ``AuditLogRole.__new__``, rename to `.from_data`.
- Add `AuditLogRole.__new__`.
- Add `AuditLogRole.to_data`.
- Add `AuditLogRole.copy`.
- Add `AuditLogRole.copy_with`.
- Add `Reaction`. (Will be used only in the next update.)

### Bug fixes

- `AuditLogRole.__repr__` raised `AttributeError`.

### Renames, Deprecations & Removals

- Deprecate `TeamMemberPermission`.
- Deprecate `TeamMember.permissions`.
- Deprecate `TeamMember.iter_permissions`.

## 1.3.36 *\[2023-08-23\]*

### Improvements

- `Client.invite_create` now supports templating and additional `target_type`,
    `target_user_id`, `target_application_id` (, ...) parameters.
- Add `use_clyde_ai` permission.
- Add `ReactionType`.
- Add `reaction_type` parameter to `Client.reaction_add`.

### Bug fixes

- `Client.permission_overwrite_create` was not inserting the `id` key detected from the `target` parameter.
    Could cause `RuntimeError`.
- `Client.permission_overwrite_create` was not inserting the `id` key detected from the `target_id` parameter.
    Could cause `RuntimeError`.
- `PermissionOverwrite.from_data` did not handle missing keys.
    Could cause `KeyError` at `Client.permission_overwrite_create`.

### Renames, Deprecations & Removals

- Deprecate `Client.stream_invite_create`. Please use `.invite_create` instead.
- Deprecate `Client.application_invite_create`. Please use `.invite_create` instead.
- Rename `RATE_LIMIT_GROUPS.vanity_invite_edit` to `invite_edit_vanity`.
- Rename `RATE_LIMIT_GROUPS.vanity_invite_get` to `invite_get_vanity`.
- Rename `DiscordHTTPClient.vanity_invite_edit` to `invite_edit_vanity`.
- Rename `DiscordHTTPClient.vanity_invite_get` to `invite_get_vanity`.
- Rename `Client.vanity_invite_edit` to `invite_edit_vanity`.
- Rename `Client.vanity_invite_get` to `invite_get_vanity`.
- Deprecate `Client.vanity_invite_edit`.
- Deprecate `Client.vanity_invite_get`.

## 1.3.35 *\[2023-08-11\]*

#### Improvements

- Add `raise_if_missing_or_empty` parameter to `get_bool_env`.
- Add `raise_if_missing_or_empty` parameter to `get_int_env`.
- Add `EnvGetter`.
- Add `GuildFeature.creator_accepted_new_terms`.
- Add `GuildFeature.creator_monetizable_owner_onboarding`.
- Add `GuildFeature.web_page`.
- Add `GuildFeature.home_deprecation`.
- Add `GuildFeature.guide_screen_enabled`.
- Add `GuildFeature.clyde_disabled`.
- Add `GuildFeature.clyde_enabled`.
- Add `GuildFeature.soundboard_enabled`.
- Add `GuildFeature.shard`.
- Add `GuildFeature.summaries_disabled_by_user`.
- Add `GuildFeature.summaries_enabled`.
- Add `GuildFeature.summaries_enabled_by_user`.
- Add `GuildFeature.summaries_enabled_global_access`. This is actually just a guessed name. :KoishiFail:
- Add `GuildFeature.channel_icon_emojis_generated`.
- Add `GuildFeature.raid_alerts_disabled`.
- Add `GuildFeature.auto_moderation_trigger_user_profile`.
- Add `GuildFeature.embedded_activities_had_early_access`.
- Add `GuildFeature.users_screen_enabled`.
- Add `GuildFeature.guests_enabled`.
- Scaffold now uses adaptive library name everywhere (In case someone copies the library and renames it, kekw).
- Add `GuildFeature.community_experiment_large_gated`.
- Scaffold now uses `EnvGetter` to get all environmental variables at once & raise one exception in case multiple are
    missing. This means the generated structure also changed.
- `cli` now calls `help` by default and not `interpreter`.
- `run` command not available when calling the library.
- `scaffold` command only available when calling the library.
- Add new `--all` parameter to `help` cli commands. This also means that `help list-all` is renamed to `help list`.
- Add `create_partial_guild_data`.
- Add `ConnectionType.none`.
- Add `create_partial_invite_data`.
- Add `create_partial_invite_from_data`.
- Add `Invite.channel_id`.
- Add `Invite.guild_id`.
- Add `Invite.InviteFlag`.
- Add `Invite.flags`.
- Add `Invite.target_application_id`.
- Add `Invite.target_user_id`.
- Add `Invite.to_data`.
- Repurpose `Invite.__new__`.
- `Invite.__eq__` now works with partial instances as well.
- `Invite.__hash__` now works with partial instances as well.
- Add `Invite.copy`.
- Add `Invite.copy_with`.
- `EMBEDDED_ACTIVITY_NAME_TO_APPLICATION_ID` and related variables moved under `.discord.application.constants`.

### Bug fixes

- `InteractionEvent.value` was bound to auto complete instead of message component. This was not intended.
- `get_bool_env` returned incorrect value if variable was any of: `0`, `1`.
- `Invite._create_empty` did not set `.target_application`.
- `ApplicationType` was not importable directly. :KoishiFail:
- `ActivitySecrets` was not importable directly. :KoishiFail:

### Renames, Deprecations & Removals

- Deprecate `ConnectionType.unknown` (use `.none` instead).
- Rename `GuildFeature.onboarding` to `.onboarding_enabled`.
- Deprecate `GuildFeature.onboarding`.
- Rename `Invite.__new__` to `.from_data`.
- Deprecate unused `Invite.nsfw_level`. It is returned with the guild and not with the invite actually :KoishiFail:.

## 1.3.34 *\[2023-07-22\]*

#### Improvements

- `Client.guild_get_all` now also updates the guilds' approximate counts.
- Add `AttachmentFlag`.
- Add `Attachment.flags`.
- Add `ERROR_CODES.cannot_enable_onboarding_requirements_not_met`.
- Add `ERROR_CODES.cannot_update_onboarding_requirements_not_met`.
- Add `OnboardingMode`.
- Add `OnboardingScreen.mode`.
- Add `Client.onboarding_screen_edit`.
- Add `DiscordHTTPClient.onboarding_screen_edit`.
- Add `RATE_LIMIT_GROUPS.onboarding_screen_edit`.

#### Renames, Deprecation & Removals

- Rename `DiscordHTTPClient.guild_get_all` to `.guild_get_chunk`.
- Rename `RATE_LIMIT_GROUPS.guild_get_all` to `.guild_get_chunk`.

## 1.3.33 *\[2023-07-15\]*

#### Improvements

- Add `ChannelFlag.hide_media_download_option`.
- Add `ChannelFlag.media_channel`.
- Add `ChannelFlag.summaries_disabled`.
- Add `ChannelFlag.role_subscription_template_preview_channel`.
- Add `ChannelFlag.broadcasting`.
- Add `ChannelMetadataGuildMedia`.
- Add `ChannelMetadataGuildForumBase`.
- Add `ChannelTypeFlag.forum`. (This is an internal object.)
- Add `ChannelType.guild_media`.
- Add `Channel.is_guild_media`.
- Add `Channel.is_in_group_forum`.
- `guild_stage` channels are now textual. Applies to both permissions and checks.
- `Client.forum_thread_create` now allows media channels too.
- `Client.forum_tag_delete` now allows media channel too.
- `Client.forum_tag_edit` now allows media channel too.
- `Client.forum_tag_create` now allows media channel too.
- Add `RoleFlag`.
- Add `Role.flags`.
- Add `RoleFlags` change converter to audit logs.
- Add `flags` parameter to `Client.role_create` and `.role_edit`.
- Add `AudioSetting`.
- Add `RawAudio`.

##### ext.plugin_loader
- Test directories and files are not marked as plugins anymore.

#### ext.slash
- Add `InteractionResponse.__eq__`.

#### Bug Fixes

- Fix `TypeError` in `User.__hash__`. Occurred at the case of partial users.

## 1.3.32 *\[2023-07-04\]*

#### Improvements

- Add support for all the parameters in `Guild.precreate`.
- When all clients leave a guild its entities such as: channels, roles, users, etc are not cleaned up anymore.
    This caused bugs on user side. On wrapper side this was the intended behavior since 2019.
    Now cleanup happens when the guild is repopulated. Note that guild profiles are still cleaned up initially.
- Add `Guild.__new__` as a template constructor.
- `Guild.__eq__` now supports template instances.
- `Guild.__hash__` now supports template instances.
- Add `Guild.copy`.
- `Guild.widget_url` is now a property to match other `..._url` properties. Added `..._url_as` version.
- Add `Guild.get_roles_like`.
- Add `Guild.get_channels_like`.
- Add `Guild.iter_channels`.
- Add `Guild.get_users_like`.
- Add `Guild.iter_users`.
- Add `Guild.iter_roles`.
- Add `Guild.iter_emojis`.
- Add `Guild.iter_stickers`.
- Add `Guild.iter_scheduled_events`.
- Add `Guild.iter_stages`.
- Add `Guild.iter_threads`.
- Add `Guild.iter_voice_states`.
- `Guild.get_user...` methods now handle `display_name` correctly.
- `Channel.get_user...` methods now handle `display_name` correctly.
- Add `GUILD_SOUNDBOARD_SOUNDS_UPDATE` event parsers.
- Add never linked (ops) `thread_user_update` event.
- `guild_user_update` has been changed from `client, user, guild, old_attributes` to
    `client, guild, user, old_attributes` to match other event handlers.
- Rename `..._edit` event handlers to `..._update` to reflect better what happened. `..._edit` format is still accepted.
- Repurpose and rename `GuildUserChunkEvent.__new__` to `.from_data`.
- Add `GuildUserChunkEvent.__new__`.
- Add `GuildUserChunkEvent.to_data`.
- Add `GuildUserChunkEvent.copy`.
- Add `GuildUserChunkEvent.copy_with`.

#### Bug Fixes

- `scaffold` command always failed if `project-name` was directly defined.
- `Message` did not update the referenced message's content fields even if it would been required.
- A message was updated with non-intent data even if there was a client with intent data.
    This was caused by checking whether "any" mask is matching instead "all".
- `NsfwLevel.age_restricted` had incorrect `.value`.
- Fix `Channel.display_name` formatting for multiple types.
- Fix `AttributeError` in `Guild.channel_list_flattened`.
- Channel sorting was partially broken producing incorrect order.
- `Guild.permissions_for` returned incorrect value if a webhook was given and the guild's default role had
    administrator permission.
- `Guild.permissions_for` did not handle guild profile roles and guild roles de-sync correctly.
- `Guild.permissions_for_roles` did not ignore partial roles as intended. Broke probably a few years ago.
- Fix `TypeError` from `GuildUserChunkEvent.__repr__` (bad return).
- Fix `ActivityMetadataCustom.__repr__` format. (Missing `>` sign.)

##### ext.plugin_loader
- Fix `IndexError` in `_is_plugin_name_in_plugin_root_names`.

##### ext.rpc
- Fix a broken import.

#### Renames, Deprecation & Removals

- Remove unused `COMMUNITY_FEATURES` importable variable.
- Rename `Guild.is_large` to `.large`.
- Deprecate `Guild.is_large`.
- Rename `Guild._embedded_activity_states` to `embedded_activity_states`.
- Deprecate `Guild.thread_channels`.
- Rename `Guild.widget_url` to `.widget_url_as`.
- Rename `EMOJI_UPDATE_EDIT` to `EMOJI_EVENT_UPDATE`. No longer directly importable, since used in internal functions.
- Rename `EMOJI_UPDATE_DELETE` to `EMOJI_EVENT_DELETE`. No longer directly importable, since used in internal functions.
- Rename `EMOJI_UPDATE_CREATE` to `EMOJI_EVENT_CREATE`. No longer directly importable, since used in internal functions.
- Rename `EMOJI_UPDATE_NONE` to `EMOJI_EVENT_NONE`. No longer directly importable, since used in internal functions.
- Rename `STICKER_UPDATE_EDIT` to `STICKER_EVENT_UPDATE`.
    No longer directly importable, since used in internal functions.
- Rename `STICKER_UPDATE_DELETE` to `STICKER_EVENT_DELETE`.
    No longer directly importable, since used in internal functions.
- Rename `STICKER_UPDATE_CREATE` to `STICKER_EVENT_CREATE`.
    No longer directly importable, since used in internal functions.
- Rename `STICKER_UPDATE_NONE` to `STICKER_EVENT_NONE`. No longer directly importable, since used in internal functions.
- Rename `VOICE_STATE_NONE` to `VOICE_STATE_EVENT_NONE`.
    No longer directly importable, since used in internal functions.
- Rename `VOICE_STATE_JOIN` to `VOICE_STATE_EVENT_JOIN`.
    No longer directly importable, since used in internal functions.
- Rename `VOICE_STATE_LEAVE` to `VOICE_STATE_EVENT_LEAVE`.
    No longer directly importable, since used in internal functions.
- Rename `VOICE_STATE_UPDATE` to `VOICE_STATE_EVENT_UPDATE`.
    No longer directly importable, since used in internal functions.
- Rename `VOICE_STATE_MOVE` to `VOICE_STATE_EVENT_MOVE`. No longer directly importable, since used in internal functions.
- Deprecate `Guild.text_channels`. Use `[*Guild.iter_channels(Channel.is_guild_text)]` instead.
- Deprecate `Guild.voice_channels`. Use `[*Guild.iter_channels(Channel.is_guild_voice)]` instead.
- Deprecate `Guild.category_channels`. Use `[*Guild.iter_channels(Channel.is_guild_category)]` instead.
- Deprecate `Guild.announcement_channels`. Use `[*Guild.iter_channels(Channel.is_guild_announcements)]` instead.
- Deprecate `Guild.store_channels`. Use `[*Guild.iter_channels(Channel.is_guild_store)]` instead.
- Deprecate `Guild.stage_channels`. Use `[*Guild.iter_channels(Channel.is_guild_stage)]` instead.
- Deprecate `Guild.forum_channels`. Use `[*Guild.iter_channels(Channel.is_guild_forum)]` instead.
- Deprecate `Guild.messageable_channels`. Use `[*Guild.iter_channels(Channel.is_in_group_guild_textual)]` instead.
- Deprecate `Guild.connectable_channels`. Use `[*Guild.iter_channels(Channel.is_in_group_guild_connectable)]` instead.
- Rename `MessageNotificationLevel.null` to `.none`.
- Deprecate `MessageNotificationLevel.null`. Use `.null` instead.
- Rename `GuildUserChunkEvent.index` too `.chunk_index`.
- Deprecate `GuildUserChunkEvent.index`.
- Rename `GuildUserChunkEvent.count` too `.chunk_count`.
- Deprecate `GuildUserChunkEvent.count`.

## 1.3.31 *\[2023-05-30\]*

#### Improvements

- Add shortcut to `Client.request_soundboard_sounds` if there is nothing to do.
- Add `SoundboardSound.is_custom_sound`.
- Add `SoundboardSound.is_default_sound`.
- Add `Guild.iter_soundboard_sounds`.
- When receiving `SoundboardSoundsEvent`, the guild's soundboard cache will be completely re-populated.
- Add `soundboard_sounds` parameter to `Guild.precreate`.
- Add `Guild.get_soundboard_sound`.
- Add `Guild.get_soundboard_sound_like`.
- Add `Guild.get_soundboard_sounds_like`.

### Bug fixes

##### ext.slash
- `file` parameter was not propagated when responding on not acknowledged component interactions.

##### ext.plugin_loader
- `Plugins` were sorted incorrectly causing them to be loaded in bad order. This caused deadlock.

## 1.3.30 *\[2023-05-29\]*

#### Improvements

- Add `--profile` parameter to `run` command.
- Add `raise_if_missing_or_empty` parameter to `get_str_env`.
- `get_bool_env` now accepts `0` and `1` too.
- Add `scaffold` command (experimental).
- Add `.env` file loading built in. This also means that the `.env` files will be finally found (poggers).
- Add `UserBase.display_name`.
- `GuildJoinRequestFormResponse` now support rich attribute exceptions.
- Repurpose and rename `GuildJoinRequestFormResponse.__new__` to `.from_data`.
- Add `GuildJoinRequestFormResponse.to_data`.
- Add `GuildJoinRequestFormResponse.__new__`.
- Add `GuildJoinRequestFormResponse.copy`.
- Add `GuildJoinRequestFormResponse.copy_with`.
- Repurpose and rename `GuildJoinRequestDeleteEvent.__new__` to `.from_data`.
- Add `GuildJoinRequestDeleteEvent.to_data`.
- Add `GuildJoinRequestDeleteEvent.__new__`.
- Add `GuildJoinRequestDeleteEvent.copy`.
- Add `GuildJoinRequestDeleteEvent.copy_with`.
- Repurpose and rename `GuildJoinRequest.__new__` to `.from_data`.
- Add `GuildJoinRequest.to_data`.
- Add `GuildJoinRequest.__new__`.
- Add `GuildJoinRequest.copy`.
- Add `GuildJoinRequest.copy_with`.
- Add `GuildJoinRequest.iter_form_responses`.
- Repurpose and rename `GuildWidgetUser.__init__` to `.from_data`.
- Add `GuildWidgetUser.to_data`.
- Add `GuildWidgetUser.__new__`.
- Add `GuildWidgetUser.copy`.
- Add `GuildWidgetUser.copy_with`.
- Repurpose and rename `GuildWidget.__init__` to `.from_data`.
- Add `GuildWidget.__new__`.
- Add `GuildWidget.to_data`.
- Add `GuildWidget.copy`.
- Add `GuildWidget.copy_with`.
- Add `GuildWidget.iter_channels`.
- Add `GuildWidget.iter_users`.
- Add `parse_message_jump_url`.
- Exception is now raised if loading `.env` file fails.
- Update `GuildPremiumPerks.sound_limit`.
- Add `SOUNDBOARD_SOUNDS`.
- Add `SoundboardSound`.
- Add `create_partial_soundboard_sound_from_id`.
- Add `create_partial_soundboard_sound_from_partial_data`.
- Add `create_partial_sticker_data`.
- Add `create_partial_sticker_from_partial_data`.
- Add `RATE_LIMIT_GROUPS.soundboard_sound_get_all_default`.
- Add `DiscordHTTPClient.soundboard_sound_get_all_default`.
- Add `Client.soundboard_sound_get_all_default`.
- Add `RATE_LIMIT_GROUPS.soundboard_sound_create`.
- Add `Client.request_soundboard_sounds`.
- Add `SoundboardSoundsEvent`.
- Add `Client.events.soundboard_sound_create`.
- Add `Client.events.soundboard_sound_update`.
- Add `Client.events.soundboard_sound_delete`.
- Add `Client.events.soundboard_sounds`.
- Add `Guild.soundboard_sounds`.
- Add default event handler `SoundboardSoundsEventHandler` for `Client.events.soundboard_sounds`.
- Add `Guild.soundboard_sounds_cached`.
- Add `Client.soundboard_sound_create`.
- Add `Client.soundboard_sound_delete`.
- Add `Client.soundboard_sound_edit`.
- Add `RATE_LIMIT_GROUPS.soundboard_sound_delete`.
- Add `RATE_LIMIT_GROUPS.soundboard_sound_edit`.
- Add `DiscordHTTPClient.soundboard_sound_create`.
- Add `DiscordHTTPClient.soundboard_sound_delete`.
- Add `DiscordHTTPClient.soundboard_sound_edit`.

### Bug fixes

- `run` command now stops the event loop if interrupted during connection.
- `run --console` command was not writing "interrupted" (when interrupted obviously) as expected.
- `Client.channel_create` identified `channel_type` parameter as extra.

#### Renames, Deprecation & Removals

- Rename `GuildRequestFormResponse` to `GuildJoinRequestFormResponse`.
- Deprecate `GuildRequestFormResponse`.
- Rename `GuildJoinRequest.last_seen` to `.last_seen_at`.
- Deprecate `GuildJoinRequest.last_seen`.
- Deprecate `GuildWidgetUser.mention`.
- Deprecate `GuildWidgetUser.mention_nick`.
- Deprecate `MESSAGE_JUMP_URL_RP` import. Use `parse_message_jump_url` instead.
- Deprecate `Sticker.to_partial_data`. Use `create_partial_sticker_data instead.
- Deprecate `Sticker.from_partial_data`. Use `create_partial_sticker_from_partial_data` instead.
- Rename `Client.sticker_guild_get_all` to `.sticker_get_all_guild`.
- Rename `DiscordHTTPClient.sticker_guild_get_all` to `.sticker_get_all_guild`.
- Rename `RATE_LIMIT_GROUPS.sticker_guild_get_all` to `.sticker_get_all_guild`.
- Deprecate `Client.sticker_guild_get_all`.
- Rename `Client.sticker_guild_create` to `.sticker_create`.
- Rename `DiscordHTTPClient.sticker_guild_create` to `.sticker_create`.
- Rename `RATE_LIMIT_GROUPS.sticker_guild_create` to `.sticker_create`.
- Deprecate `Client.sticker_guild_create`.
- Rename `Client.sticker_guild_edit` to `.sticker_edit`.
- Rename `DiscordHTTPClient.sticker_guild_edit` to `.sticker_edit`.
- Rename `RATE_LIMIT_GROUPS.sticker_guild_edit` to `.sticker_edit`.
- Deprecate `Client.sticker_guild_edit`.
- Rename `Client.sticker_guild_delete` to `.sticker_delete`.
- Rename `DiscordHTTPClient.sticker_guild_delete` to `.sticker_delete`.
- Rename `RATE_LIMIT_GROUPS.sticker_guild_delete` to `.sticker_delete`.
- Deprecate `Client.sticker_guild_delete`.
- Rename `Client.sticker_guild_get` to `.sticker_get_guild`.
- Rename `DiscordHTTPClient.sticker_guild_get` to `.sticker_get_guild`.
- Rename `RATE_LIMIT_GROUPS.sticker_guild_get` to `.sticker_get_guild`.
- Deprecate `Client.sticker_guild_get`.
- Deprecate `Client.request_members`.
- Rename `Client.request_members` to `.request_users`.
- Deprecate `Client.request_all_members_of`.
- Rename `Client.request_all_members_of` to `.request_all_users_of`.
- Rename `IntentFlag.guild_emojis_and_stickers` to `.guild_expressions`.
- Deprecate `IntentFlag.guild_emojis_and_stickers`.

## 1.3.29 *\[2023-05-08\]*

#### Improvements

- Add `InteractionEvent.channel_id` replaced with `InteractionEvent.channel`.
- Add `InteractionEvent.user_id`.
- Add `MessageCall`.
- Add `create_partial_channel_data`.
- Add `Message.call`.
- Add `Message.__new__` back.
- Add `Message.iter_mentioned_users`.
- Add `Message.iter_mentioned_role_ids`.
- Add `Message.iter_mentioned_channels`.
- Add `Message.iter_mentioned_channels_cross_guild`.
- Add `Message.iter_mentioned_roles`.
- Add `Message.copy`.
- Add `Message.copy_with`.
- `Message.__eq__` now supports partial instances.
- `Message.__hash__` now supports partial instances.
- Add `ReactionMappingLine.__hash__`.
- Add `stage_start` message content converter.
- Add `stage_end` message content converter.
- Add `stage_speaker` message content converter.
- Add `stage_topic_change` message content converter.
- Add `auto_moderation_action` message content converter.

### Bug fixes

- `call` message content converter no longer raises `AttributeError`.

#### Renames, Deprecation & Removals

- Deprecate `channel_id` parameters of `InteractionEvent`. Use `channel` instead.
- `create_partial_channel_from_data` no longer accepts `None`.
- Rename `Message.cross_mentions` to `.mentioned_channels_cross_guild`.
- Deprecate `Message.cross_mentions`.
- Rename `Message.everyone_mention` to `.mentioned_everyone`.
- Deprecate `Message.everyone_mention`.
- Rename `Message.user_mentions` to `.mentioned_users`.
- Deprecate `Message.user_mentions`.
- Rename `Message.role_mention_ids` to `.mentioned_role_ids`.
- Deprecate `Message.role_mention_ids`.
- Rename `Message.has_user_mentions` to `.has_mentioned_users`.
- Deprecate `Message.has_user_mentions`.
- Rename `Message.has_role_mentions` to `.has_mentioned_roles`.
- Deprecate `Message.has_role_mentions`.
- Deprecate `Message.has_partial`.
- Deprecate `Message.has_deleted`.
- Rename `Message.has_cross_mentions` to `.has_mentioned_channels_cross_guild`.
- Deprecate `Message.has_cross_mentions`.
- Remove `UnknownCrossMention` (Not used).
- Rename `Message.has_channel_mentions` to `.has_mentioned_channels`.
- Deprecate `Message.has_channel_mentions`.
- Deprecate `Message.custom`.

## 1.3.28 *\[2023-04-25\]*

#### Improvements

- Repurpose `MessageInteraction.__init__`, rename to `.from_data`.
- Add `MessageInteraction.__new__`.
- Add `MessageInteraction.precreate`.
- Add `MessageInteraction.__eq__`.
- Add `MessageInteraction.partial`.
- Add `MessageInteraction.__hash__`.
- Add `MessageInteraction.copy`.
- Add `MessageInteraction.copy_with`.
- Add `Attachment.waveform`.
- Add `Attachment.duration`.
- Add `ERROR_CODES.voice_message_not_supports_additional_content`.
- Add `ERROR_CODES.voice_message_must_have_one_audio_attachment`.
- Add `ERROR_CODES.voice_message_must_have_supporting_metadata`.
- Add `ERROR_CODES.cannot_edit_voice_message`.
- Add `ERROR_CODES.cannot_send_voice_message_to_this_channel`.
- Add `ERROR_CODES.clyde_consent_required`.
- Add `MessageType.private_channel_integration_add`.
- Add `MessageType.private_channel_integration_remove`.
- Add `MessageType.premium_referral`.
- Add `EmbedType.auto_moderation_notification`.
- Add `EmbedType.text`.
- Add `EmbedType.post_review`.
- Add `send_voice_messages` `Permission`.
- Update `upload_limit` to `25MB`.

##### ext.plugin_loader
- Add `Plugin.sort_key`.
- Plugin sorting improved. (Using sort key instead of name).
- Add `PluginException.plugin`.
- Add `PluginException.get_plugins`.
- Add `PluginError.get_plugin_tree_iterator_for_action`.
- Add `PluginError.get_plugin_tree_iterator_for_load`.
- Add `PluginError.get_plugin_tree_iterator_for_unload`.
- `PluginLoader` now picks up previously built but failed /cancelled plugin trees when retrying load / reload.
- Add `PluginError.get_plugin_tree_iterator_for_syntax_check`.
- `mark_as_plugin_root_directory` now ignores directories such as `__pycache__` and `tests` even if they have an
    `__init__.py` in them.
- `PluginLoader.get_plugin` now accepts paths as `name`.
- `PluginLoader.load_plugin` now accepts `Plugin`, `PluginTree`, `None` and `iterable` of them as well.
- `PluginLoader.reload_plugin` now accepts `Plugin`, `PluginTree`, `None` and `iterable` of them as well.
- `PluginLoader.unload_plugin` now accepts `Plugin`, `PluginTree`, `None` and `iterable` of them as well.
- `PluginLoader.get_plugin` now handles non-existent paths.
- `PluginLoader` now handles deleted files after unload / before load.
- Registered plugins by absolute path now get name correctly if they under a plugin root directory.

### Bug fixes

- `Message.clean_embeds` raised `AttributeError`. (from 1.3.26)

##### ext.plugin_loader
- Failing syntax checks did not abort further actions.
- `PluginLoader.remove` now removes the plugins as intended.

#### Renames, Deprecation & Removals

- Rname `MessageType.add_user` to `.user_add`.
- Rname `MessageType.remove_user` to `.user_remove`.
- Deprecate `MessageType.add_user`.
- Deprecate `MessageType.remove_user`.

## 1.3.27 *\[2023-04-14\]*

#### Improvements

- `.IntegrationMetadataBase.__new__` is now `.from_keyword_parameters`. Add new `.__new__` method.
- `.IntegrationMetadataBase.copy_with` is now `.copy_with_keyword_parameters`. Add new `.copy_with` method.
- `ComponentMetadataBase.__new__` is now `.from_keyword_parameters`. Add new `.__new__` method.
- `ComponentMetadataBase.copy_with` is now `.copy_with_keyword_parameters`. Add new `.copy_with` method.
- `ActivityMetadataBase.__new__` is now `.from_keyword_parameters`. Add new `.__new__` method.
- `ActivityMetadataBase.copy_with` now supports the `component_type` parameter.
- `ApplicationCommandOptionMetadataBase.__new__` is now `.from_keyword_parameters`. Add new `.__new__` method.
- `ApplicationCommandOptionMetadataBase.copy_with` now supports the `component_type` parameter.
- `ChannelMetadataBase.__new__` is now `.from_keyword_parameters`. Add new `.__new__` method.
- Add `ChannelMetadataBase.copy`.
- Add `ChannelMetadataBase.copy_with`.
- Add `ChannelMetadataBase.copy_with_keyword_parameters`.
- Add `Channel.copy`.
- Add `Channel.copy_with`.
- Bump max embeds from 10 to 15.
- Add `Channel.iter_channels`.
- Add `Channel.iter_voice_users`.
- Add `Channel.iter_audience`.
- Add `Channel.iter_speakers`.
- Add `Channel.iter_moderators`.
- Repurpose `MessageApplication.__init__`, rename to `.from_data`.
- Add `MessageApplication.__new__`.
- Add `MessageApplication.__hash__`.
- Add `MessageApplication.__eq__`.
- Add `MessageApplication.precreate`.
- Add `MessageApplication.copy`.
- Add `MessageApplication.copy_with`.
- Add `MessageApplication._create_empty`.
- Add `MessageApplication.partial`.

##### ext.slash
- `abort` call from a component command is now handled as intended (so always creates a new message).

##### ext.plugin_loader
- Add `Plugin.get_module_proxy`.
- Add `Plugin.iter_loaded_plugins_in_directory`.
- Loading a `Plugin` of an `__init__` file now scans already loaded plugins directly under it and assigns them to the
    module as intended. This should stop random looking `NameError`-s on reload if the file's structure is incorrect.

#### Bug Fixes

- `Channel.audience` returned the speakers.
- `Channel.speakers` returned the audience.
- `Client.owners_access` and `Client.activate_authorization_code` used `parse_` instead of `validate_` on input
    resulting `AttributeError`. (from 1.3.25) (Gilgamesh#8939)
- `Embed.__new__`'s `title` parameter was not converted to string as intended.

#### Renames, Deprecation & Removals

- Remove `ChannelMetadataBase.precreate`.
- Rename `Channel.channel_list` to `.channels` (for consistency).
- Deprecate `Channel.channel_list`.

## 1.3.26 *\[2023-04-07\]*

#### Improvements

- Add `EmbedFieldBase`.
- Add `EmbedThumbnail.__hash__`.
- Add `EmbedThumbnail.contents`.
- Add `EmbedThumbnail.iter_contents`.
- `EmbedThumbnail` now supports rich attribute exceptions.
- Add `EmbedVideo.__hash__`.
- Add `EmbedVideo.contents`.
- Add `EmbedVideo.iter_contents`.
- `EmbedVideo` now supports rich attribute exceptions.
- Add `EmbedImage.__hash__`.
- Add `EmbedImage.contents`.
- Add `EmbedImage.iter_contents`.
- `EmbedImage` now supports rich attribute exceptions.
- Add `EmbedProvider.__hash__`.
- Add `EmbedProvider.contents`.
- Add `EmbedProvider.iter_contents`.
- `EmbedProvider` now supports rich attribute exceptions.
- Add `EmbedAuthor.__hash__`.
- Add `EmbedAuthor.contents`.
- Add `EmbedAuthor.iter_contents`.
- `EmbedAuthor` now supports rich attribute exceptions.
- Add `EmbedFooter.__hash__`.
- Add `EmbedFooter.contents`.
- Add `EmbedFooter.iter_contents`.
- `EmbedFooter` now supports rich attribute exceptions.
- Add `EmbedType`.
- Add `Embed.iter_fields`.
- `Embed.iter_contents` now reflects display order. (This applies to `.contents` too ofc.)
- Add `Embed.clean_copy`.
- Add `EmbedAuthor.clean_copy`.
- Add `EmbedField.clean_copy`.
- Add `EmbedFooter.clean_copy`.
- Add `EmbedImage.clean_copy`.
- Add `EmbedProvider.clean_copy`.
- Add `EmbedThumbnail.clean_copy`.
- Add `EmbedVideo.clean_copy`.
- Add `Embed.__hash__`.
- Add `Guild.max_stage_channel_video_users`.
- Add `max_video_channel_users` audit log converter.
- Add `max_stage_video_channel_users` audit log converter.
- Add `use_soundboard` permission.
- Add `AuditLogEvent.soundboard_sound_create`.
- Add `AuditLogEvent.soundboard_sound_edit`.
- Add `AuditLogEvent.soundboard_sound_delete`.
- Add `AuditLogEvent.onboarding_prompt_create`.
- Add `AuditLogEvent.onboarding_prompt_update`.
- Add `AuditLogEvent.onboarding_prompt_delete`.
- Add `AuditLogEvent.onboarding_screen_create`.
- Add `AuditLogEvent.onboarding_screen_update`.
- Add `create_guild_expressions` permission.
- Add `create_events` permission.
- Add `use_external_sounds` permission.
- Add `VoiceChannelEffectAnimationType`.
- Add `VoiceChannelEffect`.
- Add `Client.events.voice_channel_effect`.
- `FlagBase.update_by_keys` now supports any shift if they are given in `_(\d+)` format.
- Add `keywords` converter to audit logs.
- Add `regex_patterns` converter to audit logs.
- Add `excluded_keywords` converter to audit logs.
- Add `default_channel_ids` converter to audit logs.
- Add `prompts` converter to audit logs.
- Update `permission_overwrites` audit log converters to reflect the new api.
- Update (channel) `type` audit log converter to reflect the new api.
- Add `(onboarding prompt) `type` audit log converter.
- Add `in_onboarding` converter to audit logs.
- Add `options` converter to audit logs.
- Add `required` converter to audit logs.
- Add `single_select` converter to audit logs.
- `AuditLogChange` instances now supports rich attribute errors.
- `IconSlot` and `IconType` now supports new `v2_a_` icon prefixes.
- `UserBase.avatar_decoration_url` and `.avatar_decoration_url_as` now supports the new avatar decorations.

#### Bug Fixes

- `EmbedThumbnail.copy` returned the same instance.
- `EmbedThumbnail.copy_with` returned the same instance.
- `EmbedImage.copy` returned the same instance.
- `EmbedImage.copy_with` returned the same instance.
- `EmbedAuthor.copy` returned the same instance.
- `EmbedAuthor.copy_with` returned the same instance.
- `EmbedFooter.copy` returned the same instance.
- `EmbedFooter.copy_with` returned the same instance.
- `auto_moderation_action_execution` event parsers were not updated to use the updated api.
- `auto_moderation_rule_actions` audit log converters were not updated to use the updated api.
- `SetupFunction.__call__` did not populate `**keyword_parameters` as intended. (Anri#6175)

#### Renames, Deprecation & Removals

- Rename `EmbedAuthor.proxy_icon_url` to `.icon_proxy_url`.
- Deprecate `EmbedAuthor.proxy_url_url`.
- Rename `EmbedFooter.proxy_icon_url` to `.icon_proxy_url`.
- Deprecate `EmbedFooter.proxy_url_url`.
- Rename `EmbedCore` to `Embed`.
- Remove & Deprecate `EmbedCore` reference.
- Remove & Deprecate `EmbedBase` reference.
- Rename `Guild.max_video_channel_users` to `.max_voice_channel_video_users`
- Deprecate `Guild.max_video_channel_users`.
- Rename `Permission`'s `manage_emojis_and_stickers` to `manage_guild_expressions`.
- Deprecate `Permission`'s `manage_emojis_and_stickers`.
- Rename `AuditLogEvent.auto_moderation_rule_edit` to `.auto_moderation_rule_update`.
- Rename `AuditLogEvent.role_prompt_edit` to `.role_prompt_update`.
- Deprecate `AuditLogEvent.auto_moderation_rule_edit`.
- Deprecate `AuditLogEvent.role_prompt_edit`.
- Deprecate `Embed._data`.

## 1.3.25 *\[2023-03-24\]*

#### Improvements

- Add `Stage.guild_id`.
- Add `Stage.channel_id`.
- Add `Stage.partial`.
- Repurpose `Stage.__new__`, rename to `.from_data`.
- Add `Stage.to_data`.
- Add `Stage.__new__`.
- Add `Stage.precreate`.
- Add `Stage.copy`.
- Add `Stage.copy_with`.
- `Stage.__eq__` now supports partial instances.
- `Stage.__hash__` now supports partial instances.
- `Stage._delete` will no longer remove itself from the cache.
- `Client`'s stage endpoints now support `reason` parameter (except the get one ofc).
- Add `ScheduledEventSubscribeEvent.to_data`.
- Repurpose `ScheduledEventSubscribeEvent.__new__`, rename to `.from_data`.
- Add `ScheduledEventSubscribeEvent.__new__`.
- Add `ScheduledEventSubscribeEvent.copy`.
- Add `ScheduledEventSubscribeEvent.copy_with`.
- Add `ScheduledEventSubscribeEvent.guild`.
- Add ScheduledEventSubscribeEvent.user`.
- Add `ScheduledEventEntityMetadataBase.location`.
- Add `ScheduledEventEntityMetadataBase.speaker_ids`.
- Add `ScheduledEventEntityMetadataBase.iter_speaker_ids`.
- Add `ScheduledEventEntityMetadataBase.speakers`.
- Add `ScheduledEventEntityMetadataBase.iter_speakers`.
- Add `ScheduledEventEntityMetadataBase.copy`.
- Add `ScheduledEventEntityMetadataBase.copy_with`.
- Repurpose `ScheduledEvent.__new__`, rename to `.from_data`.
- Add `ScheduledEvent.__new__`.
- Add `ScheduledEvent.to_data`.
- `ScheduledEvent.__hash__` now supports partial instances.
- `ScheduledEvent.__eq__` now supports partial instances.
- Add `ScheduledEvent.copy`.
- Add `ScheduledEvent.copy_with`.
- Add `ScheduledEvent.precreate`.
- Add `ScheduledEvent.partial`.
- Add `ScheduledEvent.iter_sku_ids`.
- Add `ScheduledEvent.from_data_is_created`.
- Add `ScheduledEventEntityMetadataBase.from_keyword_parameters`.
- Add `ScheduledEventEntityMetadataBase.copy_with_keyword_parameters`.
- Add `ApplicationFlag.auto_moderation_rule_create_badge`.
- Add `ChannelFlag.guild_resource_channel`.
- Add `ChannelFlag.clyde_ai`.
- Add `ChannelFlag.scheduled_for_deletion`.
- Add `GuildProfileFlag.home_actions_started`.
- Add `GuildProfileFlag.home_actions_completed`.
- Add `GuildProfileFlag.auto_moderation_quarantined_name_or_nick`.
- Add `GuildProfileFlag.auto_moderation_quarantined_bio`.
- Add `UserFlag.collaborator`.
- Add `UserFlag.collaborator_restricted`.
- Add `Color.from_hsl_tuple`.
- Add `Color.as_hsl_tuple`.
- Add `Color.from_hsl_float_tuple`.
- Add `Color.as_hsl_float_tuple`.
- Add `ScheduledEvent.url`.

#### Bug Fixes

- `shard_ready_waiter` was not set correct, always producing timeout. (Caused `ready` to be called later as intended.)
- `guild.scheduled_events` were populated incorrectly.

## 1.3.24 *\[2023-03-10\]*

#### Improvements

- Add `UserBase.get_status_by_platform`.
- Add `AutoModerationActionMetadataBlock`.
- Add `AutoModerationAction.custom_message`.
- Add `AutoModerationActionMetadataBase.custom_message`.
- Add `OnboardingPromptOption`.
- Add `OnboardingPrompt`.
- Add `OnboardingPromptType`.
- Add `OnboardingScreen`.
- Add `Client.onboarding_screen_get`.
- Add `DiscordHTTPClient.onboarding_screen_get`.
- Add `RATE_LIMIT_GROUPS.onboarding_screen_get`.

## 1.3.23 *\[2023-03-02\]*

#### Improvements

- Add `ApplicationCommandPermission.copy_with`.
- Add `ApplicationCommandPermission.iter_permission_overwrites`.
- Add `ApplicationCommandOptionChoice.with_translation`.
- Add `ApplicationCommandOptionChoice.copy_with`.
- Add `ApplicationCommandOption.with_translation`.
- Add `ApplicationCommandOption.copy_with`.
- Add `ApplicationCommandOption.iter_choices`.
- Add `ApplicationCommandOption.iter_options`.
- Add `ApplicationCommand.copy_with`.
- Add `ApplicationCommand.with_translation`.
- Add `ApplicationCommand.iter_options`.
- Add `ApplicationCommandOption.metadata`.
- Add `ApplicationCommandOptionType.metadata_type`.
- Add `ApplicationCommandOptionMetadataBase`.
- Add `ApplicationCommandOptionMetadataChannel`.
- Add `ApplicationCommandOptionMetadataFloat`.
- Add `ApplicationCommandOptionMetadataInteger`.
- Add `ApplicationCommandOptionMetadataNested`.
- Add `ApplicationCommandOptionMetadataNumeric`.
- Add `ApplicationCommandOptionMetadataParameter`.
- Add `ApplicationCommandOptionMetadataPrimitive`.
- Add `ApplicationCommandOptionMetadataString`.
- Add `ApplicationCommandOptionMetadataSubCommand`.
- Add `ERROR_CODES.user_cannot_burst_react`.
- Add `ERROR_CODES.cannot_delete_guild_subscription_integration`.
- Add `ERROR_CODES.activity_launch_age_gated`.
- Add `ERROR_CODES.new_owner_ineligible_for_subscription`.
- Add `ERROR_CODES.max_blocked_users`.

#### Bug Fixes

- `reconstruct_payload` put an extra line-break after a long string.
- `ApplicationCommand.guild` raised `KeyError` if the guild was not cached.

#### Renames, Deprecation & Removals

- Deprecate `ApplicationCommandPermission.add_permission_overwrite`.
- Deprecate `ApplicationCommandOptionChoice.apply_translation`.
- Deprecate `ApplicationCommandOption.add_option`.
- Deprecate `ApplicationCommandOption.add_choice`.
- Deprecate `ApplicationCommandOption.apply_translation`.
- Deprecate `ApplicationCommand.add_option`.
- Deprecate `ApplicationCommand.apply_translation`.
- Rename `invalid_activity_launch_afk_channel` to `activity_launch_afk_channel`.

## 1.3.22 *\[2023-02-18\]*

#### Improvements

- Add `ForumTagUpdate`.
- Add `ForumTagChange`.
- Add `Connection.copy`.
- Add `GuildProfileFlag`.
- Add `MessageFlag.silent`.
- Add `GuildProfile.flags`.
- Add `UserBase.iter_guilds`.
- Add `Connection.copy_with`.
- Add `Message.iter_contents`.
- Add `IconType.animated_apng`.
- Add `EmbedBase.iter_contents.`
- Add `MessageFlag.voice_message`.
- Add `UserBase.avatar_decoration`.
- Add `Connection.metadata_visibility`.
- Add `ERROR_CODES.channels_too_large`.
- Add `UserBase.avatar_decoration_url`.
- Add `Connection.metadata_visibility`.
- Add `UserBase.avatar_decoration_hash`.
- Add `UserBase.avatar_decoration_type`.
- Add `UserBase.avatar_decoration_url_as`.
- Add `silent` parameter to `Client.message_create`.
- Add `silent` parameter to `Client.forum_thread_create`.
- Add `Connection.__hash__` now supports partial instances.
- `_EmbedFieldsProxy.__repr__` now shows the stored fields.
- Add `silent` parameter to `Client.webhook_message_create`.
- `DiscordHTTPClient.oauth2_token` switched to a newer endpoint.
- Add `suppress_embeds` parameter to `Client.webhook_message_create`.
- Add `silent` parameter to `Client.interaction_followup_message_create`.
- Add `silent` parameter to `Client.interaction_response_message_create`.
- Add `create_user_from_thread_user_data` to help with new thread user creation.
- `UserBase.statuses` now defaults to `None`. This will save a lot of memory when presence caching is enabled.

##### ext.slash
- Add `silent` parameter to `abort`.
- Add `silent` parameter to `InteractionResponse.__init__`.

#### Bug Fixes

- `InteractionEvent` response waiters were not added. (When did this broke???)
- `Client.events.channel_edit` never propagated if an existing forum tag was edited.

#### Renames, Deprecation & Removals

- Rename `DiscordHTTPClient.thread_user_get_all` to `.thread_user_get_chunk`.
- Rename `RATE_LIMIT_GROUPS.thread_user_get_all` to `.thread_user_get_chunk`.

#### Bug Fixes

##### ext.solar_link
- `Equalizer.to_data` could drop `TypeError`.

## 1.3.21 *\[2023-02-11\]*

#### Improvements

- Add `UserBase.mfa`.
- Add `Userbase.copy`.
- Add `userBase.email`.
- Add `VoiceState.copy`.
- Add `userBase.locale`.
- Add `WebhookBase.user`.
- Add `UserBase.__new__`.
- Add `WebhookBase.token`.
- Add `Oauth2Access.copy`.
- Add `VoiceState.to_data`.
- Add `UserBase.from_data`.
- Add `VoiceState.__new__`.
- Add `ActivityChange.copy`.
- Add `ActivityUpdate.copy`.
- Add `VoiceState.__hash__`.
- Add `Oauth2Access.__new__`.
- Add `VoiceState.copy_with`.
- Add `Oauth2Access.to_data`.
- Add `ActivityChange.__eq__`.
- Add `ActivityUpdate.__eq__`.
- Add `Oauth2Access.__repr__`.
- Add `Oauth2Access.__hash__`.
- Add `PlaceHolderFunctional`.
- Add `UserBase.premium_type`.
- Add `Oauth2Access.copy_with`.
- Add `Oauth2User.iter_scopes`.
- Add `UserBase.email_verified`.
- Add `Webhook.to_webhook_data`.
- Add `ActivityChange.__hash__`.
- Add `ActivityUpdate.__hash__`.
- Add `WebhookBase.source_guild`.
- Add `ConnectionType.instagram`.
- Add `ActivityChange.copy_with`.
- Add `ActivityUpdate.copy_with`.
- Add `Oauth2Access.iter_scopes`.
- Add `WebhookBase.application_id`.
- Add `WebhookBase.source_channel`.
- Add `ActivityChange.from_fields`.
- Add `ActivityUpdate.from_fields`.
- Rename `UserBase.verified` to `.email_verified`.
- `UserBase.__eq__` now works on partial instances.
- `UserBase.__hash__` now works on partial instances.
- Repurpose `Webhook.__new__`, rename to `.from_data`.
- `VoiceState` now supports rich attribute exceptions.
- Repurpose `VoiceState.__new__`. Rename to `.from_data`.
- Repurpose `Oauth2User.__new__`, rename to `.from_data`.
- `ActivityUpdate` nos supports rich attribute exceptions.
- `ActivityChange` nos supports rich attribute exceptions.
- Repurpose `WebhookRepr.__new__`, rename to `.from_data`.
- Repurpose `Oauth2Access.__init__`, rename to `.from_data`.
- `VoiceState.__eq__` now works on partial instances as well.

#### Bug Fixes

- `WebhookBase.can_use_emoji` dropped `AttributeError`.
- `Client.guild_user_get_all` had wrong exit condition, lol.
- `WebhookBase.can_use_emoji` dropped `TypeError` if the webhook's guild was partial.
- `ClientUserBase.top_role_at` returned `default` if the user had only the default role.
- `ClientUserBase._update_profile` did not force assign the user to the guild if it was missing.
- `ActivityMetadataCustom` was not popping empty name, making impossible to create custom custom activities.
- `ClientUserBase.guild_profile_role_ids` logic fixed when checking required roles (was broken when emoji role > 1).
- `ClientUserBase.has_higher_role_than_at` could return `True` when both user is same and also the owner of the guild.

##### ext.slash
- `power` had no name registered.

#### Renames, Deprecation & Removals

- Deprecate `UserBase.verified`.
- Deprecate `VoiceState.is_speaker`.
- Rename `VoiceState.is_speaker` to `.speaker`.
- Rename `ReactionAddEvent.from_values` to `.from_fields`.
- Deprecate `type_` parameter of `create_partial_webhook_from_id`. Use `webhook_type` instead.

## 1.3.20 *\[2023-01-22\]*

#### Improvements

- Add `Channel.application_id`.
- Add `MessageRoleSubscription`.
- Add `Message.role_subscription`.
- Add `ERROR_CODES.max_group_channels`.
- Add `ChannelMetadataBase.application_id`.

#### Bug Fixes

- Invoking user only messages modifications at guilds were multiple clients are present were not handled correctly.

## 1.3.19 *\[2023-01-15\]*

#### Improvements

- Add `Guild.safety_alerts_channel`.
- Add `Guild.safety_alerts_channel_id`.
- Add `RoleManagerType.application_role_connection`.
- Add `RoleManagerMetadataApplicationRoleConnection`.
- Add `safety_alerts_channel_id` audit log converter.
- Add `AutoModerationRuleTriggerMetadataBase.raid_protection`.
- Add `safety_alerts_channel` parameter to `Client.guild_edit`.
- Add `safety_alerts_channel_id` parameter to `Guild.precreate`.
- Add `safety_alerts_channel_id` parameter to `Client.guild_create`.

#### Bug Fixes

- `Guild._sync_stickers` dropped error, yeeting all stickers of the guild. (from 1.3.18).

## 1.3.18 *\[2023-01-15\]*

#### Improvements

- Add `Emoji.copy`.
- Add `Sticker.copy`.
- Add `Emoji.__new__`.
- Add `Emoji.partial`.
- Add `Emoji.to_data`.
- Add `Activity.copy`.
- Add `Sticker.has_tag`.
- Add `Emoji.copy_with`.
- Add `Sticker.__new__`.
- Add `StickerPack.copy`.
- Add `GuildPreview.copy`.
- Add `Sticker.copy_with`.
- Add `AuditLog.guild_id`.
- Add `StickerFormat.gif`.
- Add `Activity.copy_with`.
- Add `Sticker.__format__`.
- Add `WelcomeScreen.copy`.
- Add `StickerPack.to_data`.
- Add `StickerPack.partial`.
- Add `StickerPack.__new__`.
- Add `Emoji.iter_role_ids`.
- Add `GuildPreview.__new__`.
- Add `GuildPreview.to_data`.
- Add `ReactionAddEvent.copy`.
- Add `AuditLogEntry.user_id`.
- Add `WelcomeScreen.__new__`.
- Add `StickerPack.precreate`.
- Add `StickerPack.copy_with`.
- Add `GuildPreview.copy_with`.
- Add `ActivityFieldBase.copy`.
- Add `StickerPack.has_sticker`.
- Add `WelcomeScreen.copy_with`.
- Add `ReactionAddEvent.to_data`.
- Add `GuildPreview.has_feature`.
- Add `EmbeddedActivityStateKey`.
- Add `ActivityMetadataBase.copy`.
- Add `EmbeddedActivityState.key`.
- Add `StickerPack.iter_stickers`.
- Add `WelcomeScreenChannel.copy`.
- Add `EmbeddedActivityState.copy`.
- Add `GuildPreview.iter_features`.
- Add `ReactionAddEvent.copy_with`.
- Add `ReactionAddEvent.from_data`.
- Add `ActivityFieldBase.copy_with`.
- Add `ReactionAddEvent.from_values`.
- Add `WelcomeScreenChannel.__new__`.
- Add `EmbeddedActivityState.to_data`.
- Add `EmbeddedActivityState.__new__`.
- Add `ActivityMetadataBase.copy_with`.
- Add missing `StickerPack.banner_url`.
- Add `WelcomeScreenChannel.copy_with`.
- Add `EmbeddedActivityState.from_data`.
- Add `EmbeddedActivityState.copy_with`.
- `GuildPreview.__eq__` now deep compares.
- `GuildPreview.__hash__` now deep hashes.
- Add `WelcomeScreen.iter_welcome_channels`.
- Add `EmbeddedActivityState.application_id`.
- Add `Client.events.audit_log_entry_create`.
- `Emoji.__eq__` now supports partial instances.
- `Emoji.__hash__` now supports partial instances.
- `Sticker.__eq__` now supports partial instances.
- `Unicode` now support rich attribute exceptions.
- `Sticker.__hash__` now supports partial instances.
- Repurpose `Emoji.__new__`. Rename to `.from_data`.
- `StickerPack.__eq__` now supports partial instances.
- Repurpose `Sticker.__new__`. Rename to `.from_data`.
- `StickerPack.__hash__`` now supports partial instances.
- Repurpose `StickerPack.__new__`. Rename to `.from_data`.
- Repurpose `GuildPreview.__init__`. Rename to `.from_data`.
- Repurpose `EmbeddedActivityState.__new__`. Rename to `.from_data_is_created`.
- Add `create_partial_emoji_from_inline_data`. The same logic is excluded from `create_partial_emoji_from_data`.
- `ReactionAddEvent` and `ReactionDeleteEvent`-s now populate `.user.guild_profiles` with the local guild if applicable.

##### ext.slash

- Auto-completers now support coroutine generators.

#### Bug Fixes

- `Emoji.roles` sorted the roles incorrectly.
- `parse_reaction` could raise `AttributeError`.
- `create_unicode_emoji` could raise `AttributeError`.
- Initially received ``EmbeddedActivityState`` were not cached correctly.
- Some message update edge cases were not handled since they were after "edit check".

#### Renames, Deprecation & Removals

- Deprecate `WelcomeChannel`.
- Deprecate `IntentFlag.guild_bans`.
- Rename `WelcomeChannel` to `WelcomeScreenChannel`.
- Rename `Sticker._from_partial` to `.from_partial_data`.
- Deprecate `type` parameter of `WelcomeScreenChannel.custom`, use `step_type` instead.
- Deprecate `WelcomeScreenChannel.custom`. use `.__new__` or `.copy_with` respectively.

## 1.3.17 *\[2022-12-22\]*

#### Improvements

- Add `VerificationScreen.copy`.
- Add `VerificationScreen.__new__`.
- Add `VerificationScreenStep.copy`.
- Add `VerificationScreen.copy_with`.
- Add `VerificationScreen.iter_steps`.
- Add `VerificationScreenStep.__new__`.
- Add `VerificationScreenStep.copy_with˙.
- Add `VerificationScreenStep.iter_values`.
- Add `ERROR_CODES.max_webhooks_of_guilds`.

#### Bug Fixes

- Fix `NameError` in `Client.message_edit`. (from 1.3.16 probably)

#### Renames, Deprecation & Removals

- Deprecate `type` parameter of `VerificationScreenStep.custom`, use `step_type` instead.
- Deprecate `VerificationScreenStep.custom`. use `.__new__` or `.copy_with` respectively.
- Rename `VerificationScreen.created_at` to `.edited_at`.
- Deprecate VerificationScreen.created_at`.

## 1.3.16 *\[2022-12-21\]*

#### Improvements

- Add `EmojiCounts`.
- Add `ForumLayout`.
- Add `StickerCounts`.
- Add `Emoji.iter_roles`.
- Add `Emoji.is_premium`.
- Add `Integration.copy`.
- Add `GuildPremiumPerks`.
- Add `Guild.has_feature`.
- Add `InviteType.friend`.
- Add `ThreadProfile.copy`.
- Add `GuildDiscovery.copy`.
- Add `Guild.premium_perks`.
- Add `Guild.iter_features`.
- Add `ThreadProfile.__eq__`.
- Add `MessageActivity.copy`.
- Add `ThreadProfile.__new__`.
- Add `Role.manager_metadata`.
- Add `MessageType.stage_end`.
- Add `Integration.copy_with`.
- Add `RoleManagerMetadataBot`.
- Add `ThreadProfile.__hash__`.
- Add `GuildDiscovery.__new__`.
- Add `GuildDiscovery.to_data`.
- Add `RoleManagerMetadataBase`.
- Add `IntegrationAccount.copy`.
- Add `ThreadProfile.copy_with`.
- Add `MessageActivity.__new__`.
- Add `GuildFeature.onboarding`.
- Add `MessageType.stage_start`.
- Add `MessageActivity.__hash__`.
- Add `GuildDiscovery.copy_with`.
- Add `MessageActivity.copy_with`.
- Add `DiscoveryCategory.to_data`.
- Add `ERROR_CODES.card_declined`.
- Add `MessageType.stage_speaker`.
- Add `ConnectionType.crunchyroll`.
- Add `RoleManagerMetadataBooster`.
- Add `GuildFeature.home_override`.
- Add `RelationshipType.suggestion`.
- Add `IntegrationApplication.copy`.
- Add `Channel.default_forum_layout`.
- Add `GuildDiscovery.iter_keywords`.
- Add `RoleManagerType.subscription`.
- Add `IntegrationMetadataBase.copy`.
- Add `GuildFeature.burst_reactions`.
- Add `IntegrationAccount.copy_with`.
- Add `ERROR_CODES.user_quarantined`.
- Add `ERROR_CODES.invites_disabled`.
- Add `ERROR_CODES.max_premium_emoji`.
- Add `GuildDiscovery.sub_categories`.
- Add `RoleManagerType.metadata_type`.
- Add `RoleManagerMetadataIntegration`.
- Add `MessageType.stage_topic_change`.
- Add `RoleManagerMetadataSubscription`.
- Add `GuildFeature.channel_highlights`.
- Add `IntegrationApplication.cop_with`.
- Add `GuildFeature.creator_store_page`.
- Add `GuildFeature.raid_alerts_enabled`.
- Add `IntegrationMetadataBase.copy_with`.
- Add `ERROR_CODES.confirmation_required`.
- Add `MessageType.stage_request_to_speak`.
- Add `IntegrationType.guild_subscription`.
- Add `GuildFeature.text_in_stage_enabled`.
- Add `GuildFeature.onboarding_has_prompts`.
- Add `MessageType.application_subscription`.
- Add `GuildFeature.onboarding_ever_enabled`.
- Add `default_sort_order` audit log converter.
- Add `ERROR_CODES.feature_not_yet_rolled_out`.
- Add `ChannelMetadataBase.default_forum_layout`.
- Add `GuildFeature.channel_highlights_disabled`.
- Add `ERROR_CODES.auto_moderation_invalid_regex`.
- Add `GuildFeature.marketplaces_connection_roles`.
- Add `ERROR_CODES.vanity_url_requirements_not_met`.
- Add `GuildFeature.creator_monetizable_restricted`.
- Add `InviteTargetType.role_subscription_purchase`.
- Add `ERROR_CODES.subscription_renewal_in_progress`.
- Add `GuildFeature.creator_monetizable_temporarily`.
- Add `ChannelMetadataGuildForum.default_forum_layout`.
- Add `ERROR_CODES.invalid_activity_launch_afk_channel`.
- Add `ERROR_CODES.invalid_currency_for_payment_source`.
- Add `GuildFeature.creator_monetizable_premium_service`.
- `GuildDiscovery` now supports rich attribute exceptions.
- Add `ERROR_CODES.purchase_token_authorization_required`.
- `MessageActivity` now supports rich attribute exceptions.
- Move `PermissionOverwrite` under the `channel` directory.
- Add `ERROR_CODES.vanity_url_employee_only_guild_disabled`.
- Repurpose `ThreadProfile.__init__`. Rename to `.from_data`.
- `IntegrationAccount` now supports rich attribute exceptions.
- Repurpose `GuildDiscovery.__init__`. Rename to `.from_data`.
- Repurpose `MessageActivity.__init__`. Rename to `.from_data`.
- Add `ERROR_CODES.event_entity_type_different_from_the_entitys`.
- Add `ERROR_CODES.cannot_convert_emoji_between_premium_and_non_premium`.
- Add `ERROR_CODES.cannot_mix_subscription_and_non_subscription_roles_for_an_emoji`.

### Bug fixes

- Fix an `AttributeError` in `Client._delete`.
- `thread_user_difference_update` was always returning `None`.
- `Sticker.precreate`'s `format` and `type` parameters were broken.
- Rename `DiscordHTTPClient.guild_discovery_add_sub_category` used bad http method.
- At cases when `thread_user_pop` did not need to pop thread profile it still popped the thread user.

#### Renames, Deprecation & Removals

- Remove `DISCOVERY_CATEGORIES`.
- Remove `GuildDiscovery.guild`.
- Deprecate unpacking `Guild.emoji_counts`.
- Rename `DiscoveryCategory.id` to `.value`.
- Deprecate unpacking `Guild.sticker_counts`.
- Deprecate `cr_p_permission_overwrite_object`.
- Deprecate `Client.guild_discovery_add_subcategory`.
- Rename `DiscoveryCategory.from_id` to `._from_value`.
- Deprecate `Client.guild_discovery_delete_subcategory`.
- Deprecate `DiscoveryCategory.id`. Please use `.value` instead.
- Rename `DiscoveryCategory.local_names` to `.name_localizations`.
- Rename `thread_user_update` to `.thread_user_difference_update`.
- Remove `AuditLogEvent.guild_home_remove_item` to `.home_remove_item`.
- Rename `AuditLogEvent.guild_home_feature_item` to `.home_feature_item`.
- Rename `Client.guild_discovery_add_subcategory` to `.guild_discovery_add_sub_category`.
- Rename `Client.guild_discovery_delete_subcategory` to `.guild_discovery_delete_sub_category`.
- Rename `DiscordHTTPClient.guild_discovery_add_subcategory` to `.guild_discovery_add_sub_category`.
- Rename `RATE_LIMIT_GROUPS.guild_discovery_add_subcategory` to `.guild_discovery_add_sub_category`.
- Rename `DiscordHTTPClient.guild_discovery_delete_subcategory` to `.guild_discovery_delete_sub_category`.
- Rename `RATE_LIMIT_GROUPS.guild_discovery_delete_subcategory` to `.guild_discovery_delete_sub_category`.

## 1.3.15 *\[2022-12-13\]*

#### Improvements

- Add `Channel.threads`.
- Add `Channel.iter_threads`.
- Add `Channel._iter_delete`.
- Add `ApplicationRoleConnection`.
- Add `ChannelMetadataBase._iter_delete`.
- Add `ApplicationRoleConnectionMetadata`.
- Add `ApplicationRoleConnectionValueType`.
- Add `ApplicationRoleConnectionMetadataType`.
- Add `Client.user_application_role_connection_get`.
- Add `Client.user_application_role_connection_edit`.
- Add `Client.application_role_connection_metadata_get_all`.
- Add `Client.application_role_connection_metadata_edit_all`.
- Add `DiscordHTTPClient.user_application_role_connection_get`.
- Add `RATE_LIMIT_GROUPS.user_application_role_connection_get`.
- Add `DiscordHTTPClient.user_application_role_connection_edit`.
- Add `RATE_LIMIT_GROUPS.user_application_role_connection_edit`.
- Add `DiscordHTTPClient.application_role_connection_metadata_get_all`.
- Add `RATE_LIMIT_GROUPS.application_role_connection_metadata_get_all`.
- Add `DiscordHTTPClient.application_role_connection_metadata_edit_all`.
- Add `RATE_LIMIT_GROUPS.application_role_connection_metadata_edit_all`.

### Bug fixes

- Webhook message author name length was limited to 32 (can be up to 80 long).
- When a forum channel was deleted discord is not dropping thread deletes. Now this is handled.

## 1.3.14 *\[2022-12-03\]*

#### Improvements

- Repurpose `TeamMember.__init__`. Rename to `.from_data`.
- Add `TeamMember.to_data`.
- Add `TeamMember.__new__`.
- Add `TeamMemberPermission`.
- Add `TeamMember.copy`.
- Add `TeamMember.copy_with`.
- Add `TeamMember.iter_permissions`.
- `Team.__hash__` now supports partial instances.
- `Team.__eq__` now supports partial instances.
- Add `Team.iter_members`.
- Repurpose `Team.__new__`. Rename to `.from_data`.
- Add `Team.__new__`.
- Add `Team.copy`.
- Add `Team.copy_with`.
- Add `Team.precreate`.
- Add `Team.partial`.
- `TeamMember`-s are now sortable.
- Repurpose `ApplicationEntity.__init__`. Rename to `.from_data`.
- `ApplicationEntity.__eq__` now supports partial instances.
- Add `ApplicationEntity.partial`.
- Add `ApplicationEntity.__new__`.
- Add `ApplicationEntity.precreate`.
- `ApplicationEntity.__hash__` now supports partial instances.
- Add `ApplicationEntity.to_data`.
- Add `ApplicationEntity.copy`.
- Add `ApplicationEntity.copy_with`.
- `ApplicationInstallParameters` now supports rich attribute exceptions.
- Repurpose `ApplicationInstallParameters.__new__`. Rename to `.from_data`.
- Add `ApplicationInstallParameters.__new__`.
- Add `ApplicationInstallParameters.to_data`.
- Add `ApplicationInstallParameters.copy`.
- Add `ApplicationInstallParameters.copy_with`.
- `ApplicationExecutable` now supports rich attribute exceptions.
- Repurpose `ApplicationExecutable.__init__`. Rename to `.from_data`.
- Add `OperationSystem`.
- Add `ApplicationExecutable.to_data`.
- Add `ApplicationExecutable.__new__`.
- Add `ApplicationExecutable.copy`.
- Add `ApplicationExecutable.copy_with`.
- `ThirdPartySKU` now supports rich attribute exceptions.
- Repurpose `ThirdPartySKU.__init__`. Rename to `.from_data`.
- Add `ThirdPartySKU.to_data`.
- Add `ThirdPartySKU.__new__`.
- Add `ThirdPartySKU.copy`.
- Add `ThirdPartySKU.copy_with`.
- Repurpose `EULA.__new__`. Rename to `.from_data`.
- Add `EULA.__new__`.
- Add `EULA.to_data`.
- Add `EULA.__eq__` now supports partial instances.
- Add `EULA.precreate`.
- Add `EULA.copy`.
- Add `EULA.copy_with`.
- Add `EULA.partial`.
- `EULA.__hash__` now supports partial instances.
- Add `ApplicationFlag.embedded_iap`
- `ApplicationExecutable` is now sortable.
- Add `Team.to_data_user`.
- Add `ApplicationType`.
- `ThirdPartySKU` is now sortable.
- Add `Application.deeplink_url`.
- Add `Application.type`.
- Add Application.role_connections_verification_url`.
- Add `Application.from_data_ready`.
- Add `Application.from_data_own`.
- Add `Application.from_data_invite`.
- Add `Application.from_data_detectable`.
- Repurpose `Application.__new__`. Rename to `.from_data`.
- `Application.precreate` now accepts (way) more parameters.
- `Application.partial` now checks for it's client being more loose.
- Add `Application.__new__`.
- `Application.__hash__` now works on partial instances as well.
- `Application.__eq__` now works with partial instances as well.
- Add `Application.copy`.
- Add `Application.copy_with`.
- Add `Application.iter_aliases`.
- Add `Application.iter_developers`.
- Add `Application.iter_executables`.
- Add `Application.iter_publishers`.
- Add `Application.iter_rpc_origins`.
- Add `Application.iter_tags`.
- Add `Application.iter_third_party_skus`.
- Add `Application.to_data`.
- Add `Application.to_data_ready`.
- Add `Application.to_data_own`.
- Add `Application.to_data_invite`.
- Add `Application.to_data_detectable`.
- Add a way to deprecate flags.
- Add `UserBase.is_boosting`.

### Bug fixes

- Fix infinite loop in ``ApplicationInstallParameters.__repr__``.
- `Application.max_participants` now correctly defaults to `0`.
- Lookup channel's `.guild_id` if missing from message data. (We can count this as an api bug.)

#### Renames, Deprecation & Removals

- Rename `ApplicationSubEntity` to `ApplicationEntity`.
- Rename `ApplicationExecutable.is_launcher` to `launcher`.
- Deprecate `ApplicationExecutable.is_launcher`.
- Remove `EmbeddedActivityConfiguration` (not used anymore).
- Deprecate `Application.embedded_activity_configuration`.
- Rename `Message.__new__` to `.from_data`.
- Deprecate `Message.__new__`.
- Rename `Guild.__new__` to `.from_data`.
- Deprecate `Guild.__new__`.
- Rename `Activity.__new__`'s `type_` parameter to `activity_type`.
- Deprecate `Activity.__new__`'s `type_` parameter.
- Rename `ActivityParty.__new__`'s `id_` parameter to `party_id`.
- Deprecate `ActivityParty.__new__`'s `id_` parameter.
- Deprecate `manage_channel` permission. Please use `manage_channels` instead.

#### Improvements

## 1.3.13 *\[2022-11-22\]*

#### Improvements

- Add `AutoModerationActionMetadataBase.copy_with`.
- Add `AutoModerationActionMetadataBase.channel_id` (moved up).
- Add `AutoModerationActionMetadataBase.channel` (moved up).
- Add `AutoModerationActionMetadataBase.duration` (moved up).
- Add `AutoModerationRuleTriggerMetadataBase.regex_patterns`.
- Add `AutoModerationRuleTriggerMetadataBase.excluded_keywords` (moved up).
- Add `AutoModerationRuleTriggerMetadataBase.keyword_presets` (moved up).
- Add `AutoModerationRuleTriggerMetadataBase.mention_limit` (moved up).
- Add `AutoModerationRuleTriggerMetadataBase.keywords` (moved up).
- Add `AutoModerationRuleTriggerMetadataBase.iter_regex_patterns`.
- Add `AutoModerationRuleTriggerMetadataBase.iter_keywords` (moved up).
- Add `AutoModerationRuleTriggerMetadataBase.iter_keyword_presets` (moved up).
- Add `AutoModerationRuleTriggerMetadataBase.iter_excluded_keywords` (moved up).
- Add `AutoModerationRuleTriggerMetadataBase.copy_with`.
- Add `AutoModerationAction.channel_id`.
- Add `AutoModerationAction.duration`.
- Add `AutoModerationAction.channel`.
- Add `AutoModerationActionExecutionEvent.alert_system_message`.
- Add `AutoModerationActionExecutionEvent.rule`.
- Repurpose `AutoModerationActionExecutionEvent.__new__`. Rename to `.from_data`.
- Add `AutoModerationActionExecutionEvent.to_data`.
- Add `AutoModerationActionExecutionEvent.__new__`.
- Add `AutoModerationActionExecutionEvent.copy`.
- Add `AutoModerationActionExecutionEvent.copy_with`.
- Add `AutoModerationRule.precreate`.
- Add `AutoModerationRule.guild`.
- Add `AutoModerationRule._create_empty`.
- Add `GuildFeature.application_command_permissions_v2`.
- Add `Locale.indonesian`.
- Add `AutoModerationRuleTriggerMetadataKeyword.excluded_keywords.`
- `run_console_till_interruption` now picks up variables from main file too as intended.
- `interpreter` command now picks up variables correctly depending whether it was called from library or from outer
    sources, including outer main files.
- Add `Attachment` example.

### Bug fixes

- `Client.audit_log_get_chunk` did not populate the returned audit log :derp:.
- Fix `ValueError` when Discord says our rate limit resets at year 584556072.
- `Emoji.url` will not return `None` if the emoji's id is malformed. Instead will check for unicode value.

##### ext.plugin_loader
- `PluginError.messages` returned an incorrect value.

##### ext.patchouli
- Optional parameters were incorrectly displayed (was actually a bug caused by an older fix :derp:).

#### Renames, Deprecation & Removals

- Rename `Client.sticker_guild_create`'s `emoji_representation` parameter to `tags`.
- Rename `Client.sticker_guild_edit`'s `emoji_representation` parameter to `tags`.


## 1.3.12 *\[2022-11-12\]*

#### Improvements

- Repurpose `GuildProfile.__init__`. Rename it to `.from_data`.
- Add `GuildProfile.__new__`.
- Add `GuildProfile.__eq__`.
- Add `GuildProfile.__hash__`.
- Add `GuildProfile.iter_role_ids`.
- Add `GuildProfile.iter_roles`.
- Add `GuildProfile.to_data`.
- Add `GuildProfile.copy`.
- Add `GuildProfile.copy_with`.
- Repurpose `InteractionOption.__init__`. Rename to `.from_data`.
- Add `InteractionOption.to_data`.
- Add `InteractionOption.__new__`.
- Add `InteractionOption.get_value_of_recursive`.
- Repurpose `Attachment.__init__`. Rename to `.from_data`.
- Add `Attachment.__new__`.
- Add `Attachment.__hash__`.
- Add `Attachment.__eq__`.
- Add `Attachment.copy`.
- Add `Attachment.copy_with`.
- Add `Attachment.precreate`.
- Repurpose `Role.__new__. Rename to `.from_data`.
- Add `Role.__new__`.
- Add `Role.to_data`.
- Add `Role.copy`.
- Add `Role.copy_with`.
- Support partial `Role.__eq__`.
- Support partial `Role.__hash__`.
- `Role.is_default` is now a method (from property).
- `Icon.__eq__` now supports `tuple`-s.
- `Icon.__eq__` now supports `none`-s.
- Add `Resolved`.
- Add `InteractionMetadataComponent.resolved`.
- Add `InteractionType.metadata_type`.
- Add `InteractionEvent._create_empty`.
- `InteractionEvent.__eq__` now supports partial instances.
- `InteractionEvent.__hash__` now supports partial instances.
- Add `InteractionEvent.to_data`.
- Add `InteractionEvent._create_empty`.
- Add `InteractionEvent.copy`.
- Add `InteractionEvent.copy_with`.
- Add `InteractionOption.iter_options`.
- Add `InteractionComponent.iter_components`.
- Add `InteractionResponseContext.__eq__`.
- Add `InteractionResponseContext.__hash__`.
- Add `InteractionMetadataBase.resolve_user`.
- Add `InteractionMetadataBase.resolve_channel`.
- Add `InteractionMetadataBase.resolve_attachment`.
- Add `InteractionMetadataBase.resolve_role`.
- Add `InteractionMetadataBase.resolve_message`.
- Add `InteractionMetadataBase.resolve_mentionable`.
- Add `InteractionMetadataBase.entities`.
- Add `InteractionMetadataBase.iter_values`.
- Add `InteractionMetadataBase.iter_entities`.
- Add `InteractionMetadataBase.iter_components`.
- Add `InteractionMetadataBase.iter_options`.
- Add `InteractionEvent.component_type`.
- Add `InteractionEvent.components`.
- Add `InteractionEvent.custom_id`.
- Add `InteractionEvent.application_command_id`.
- Add `InteractionEvent.application_command_name`.
- Add `InteractionEvent.options`.
- Add `InteractionEvent.resolved`.
- Add `InteractionEvent.target_id`.
- Add `InteractionEvent.values`.
- Add `InteractionEvent.target`.
- Add `InteractionEvent.iter_options`.
- Add `InteractionEvent.focused_option`.
- Add `InteractionEvent.get_non_focused_values`.
- Add `InteractionEvent.get_value_of`.
- Add `InteractionEvent.value`.
- Add `InteractionEvent.iter_values`.
- Add `InteractionEvent.iter_entities`.
- Add `InteractionEvent.entities`.
- Add `InteractionEvent.iter_components`.
- Add `InteractionEvent.iter_custom_ids_and_values`.
- Add `InteractionEvent.get_custom_id_value_relation`.
- Add `InteractionEvent.get_value_for`.
- Add `InteractionEvent.get_match_and_value`.
- Add `InteractionEvent.iter_matches_and_values`.
- Add `InteractionEvent.resolve_attachment`.
- Add `InteractionEvent.resolve_channel`.
- Add `InteractionEvent.resolve_message`.
- Add `InteractionEvent.resolve_role`.
- Add `InteractionEvent.resolve_user`.
- Add `InteractionEvent.resolve_mentionable`.
- Add `InteractionEvent.resolve_entity`.
- `Client.interaction_followup_message_create` now supports sending only components.
- `Client.interaction_response_message_create` now supports sending only components.
- Add `PremiumType.nitro_basic`.
- Add `UserFlag.active_developer`.
- Add `ERROR_CODES.invalid_request_origin`.
- Add `ApplicationFlag.active`.
- Add `ConnectionType.tiktok`.
- Add `ERROR_CODES.rate_limit_resource`.
- Add `Oauth2Scope.role_connections_write`.
- Add `ERROR_CODES.ineligible_for_subscription`.
- Add `ERROR_CODES.rate_limit_service_resource`.
- Add `DiscordException.retry_after`.
- Add `GuildFeature.developer_support_guild`.

##### ext.slash

- Add `StringSelect`. (Alternative name of `Select`).
- Add `UserSelect`.
- Add `ChannelSelect`.
- Add `RoleSelect`.
- Add `MentionableSelect`.
- Add `CommandBase.mention`.
- Add `CommandBase.mention_at`.
- Add `CommandBase.__format__`.
- Add `SlashCommandCategory.mention`.
- Add `SlashCommandCategory.mention_at`.
- Add `SlashCommandCategory.__format__`.
- Add `SlashCommandFunction.mention`.
- Add `SlashCommandFunction.mention_at`.
- Add `SlashCommandFunction.__format__`.

#### Renames, Deprecation & Removals

- Deprecate `InteractionComponent.options`. Use `.values` instead.
- Deprecate `cr_p_role_object`. Use `Role(..).to_data(...)` instead.
- Deprecate `InteractionComponent.type`. Use `.component_type` instead.
- Deprecate `FormSubmitInteraction.options`. Use `.components` instead.
- Rename `ApplicationCommandAutocompleteInteraction` to `InteractionMetadataApplicationCommandAutocomplete`.
- Rename `ApplicationCommandInteraction` to `InteractionMetadataApplicationCommand`.
- Rename `ForumSubmitInteraction` to `InteractionMetadataForumSubmit`.
- Rename `ComponentInteraction` to `InteractionMetadataMessageComponent`.
- Rename `InteractionFieldBase` to `InteractionMetadataBase`.

## 1.3.11 *\[2022-10-25\]*

#### Improvements

- Add `Message.iter_components`.
- Add `Component.button_style`.
- Add `Component.text_input_style`.
- Add `Component.iter_components`.
- Add `Component.iter_options`.
- Add `Component.channel_types`.
- Add `InteractionForm.iter_components`.
- Add `create_button` to replace `ComponentButton`.
- Add `create_row` to replace `ComponentRow`.
- Add `create_string_select` to replace `ComponentSelect`.
- Add `create_text_input` to replace `ComponentTextInput`.
- Add `create_user_select`.
- Add `create_role_select`.
- Add `create_channel_select`.
- Add `create_mentionable_select`.
- Use `CauseGroup` at `DiscordHTTPClient.discord_request`.
- Add `HATA_LIBRARY_NAME` env variable.
- Add `HATA_LIBRARY_AGENT_APPENDIX` env variable.
- Add `HATA_LIBRARY_VERSION` env variable.
- `Client.message_create` now supports sending only components.

##### ext.plugin_loader
- Use `CauseGroup` for `PluginError`-s if applicable.
- New `PluginError`-s now store exception instead of traceback, so expose `filter_frames`.

#### Renames, Deprecation & Removals

- Rename `Guild.sticker_count` to `.sticker_counts` (it was actually a typo the whole time).
- Deprecate `Guild.sticker_count`.
- Deprecate `style` parameters of components.
- Deprecate `ComponentSelectOption`. Use `StringSelectOption` instead.
- Deprecate `ComponentBase`. Use `Component` instead. Remove all other component types.

## 1.3.10 *\[2022-10-16\]*

#### Improvements

- `Role.partial` will now handle correctly if the role is deleted.
- Add `guild_id` parameter to `create_partial_role_from_id`.
- Add `guild_id` parameter to `Role._create_empty`.
- `client.events.role_delete` now accepts only `2` parameters (3rd was redundant).
- Update `emoji_delete` rate limit documentation.
- Update `emoji_create` rate limit & documentation.
- Update `emoji_edit` rate limit documentation.
- Add `Client.forum_tag_create`.
- Add `Client.forum_tag_edit`.
- Add `Client.forum_tag_delete`.
- Add `RATE_LIMIT_GROUPS.forum_tag_delete`.
- Add `RATE_LIMIT_GROUPS.forum_tag_edit`.
- Add `RATE_LIMIT_GROUPS.forum_tag_create`.
- Add `DiscordHTTPClient.forum_tag_create`.
- Add `DiscordHTTPClient.forum_tag_edit`.
- Add `DiscordHTTPClient.forum_tag_delete`.
- Update `sticker_guild_delete` rate limit documentation.
- Update `sticker_guild_create` rate limit & documentation.
- Update `sticker_guild_edit` rate limit documentation.
- Add `IconSlot.parse_data_from_keyword_parameters`.
- Add `IconSlot.parse_from_keyword_parameters`.
- Add `IconSlot.put_into`.
- `Client.channel_edit` now accepts template entity + smaller changes to parameters.
- `Client.channel_create` now accepts template entity + smaller changes to parameters.
- `Client.channel_group_edit` now accepts template entity + smaller changes to parameters.
- `Client.thread_create` now accepts template entity + smaller changes to parameters.
- `Client.forum_thread_create` now accepts template entity + smaller changes to parameters.
- Add `PermissionOverwrite.copy`.
- `Client.permission_overwrite_edit` now accepts template entity + smaller changes to parameters.
- `Client.permission_overwrite_create` now accepts template entity + smaller changes to parameters.
- Add `GuildFeature.thread_limit_increased`.
- Add `MessageType.deletable`.
- Add `Connection.two_way_link`.
- Add `ConnectionVisibility`.
- Move `Connection.__init__` to `.from_data`
- Add `Connection.__new__`.
- Add `Connection.precreate`.
- Add `ConnectionType.unknown`.
- Add `Connection.__repr__`.
- Add `Connection.to_data`.
- Add `Connection._create_empty`.
- `Connection.__eq__` now supports rich comparing.
- Add `Connection.iter_integrations`.
- Move `IntegrationApplication.__init__` to `.from_data`.
- Add `IntegrationApplication.__new__`.
- Add `IntegrationApplication.precreate`.
- Add `IntegrationApplication.__repr__`.
- Add `IntegrationApplication.to_data`.
- `IntegrationApplication.__eq__` now supports rich comparing.
- Add `IntegrationApplication.partial`.
- Add `IntegrationApplication._create_empty`.
- Move `IntegrationAccount.__new__` to `.from_data`.
- Add `IntegrationAccount.__new__`
- Add `IntegrationAccount.to_data.`
- Add `IntegrationAccount.__eq__`.
- Add `IntegrationAccount.__hash__`.
- Add `IntegrationType.twitch`
- Integrations now use metadata system. (this actually contains a lot of changes)
- Add `Integration._create_empty`.
- Add `Integration.__hash__`.
- Add `Integration.from_data` (moved from `.__new__`)
- Repurpose `Integration.__new__` for partial constructor.
- Add `Integration.precreate`.
- `Integration.__hash__` now supports partial entities.
- `Integration.__eq__` now supports partial entities.
- Add `Integration.role`.
- Add `ERROR_CODES.cannot_edit_system_webhook`.
- Add `VoiceRegion.unknown`.
- Add `ERROR_CODES.invalid_activity_action`.
- `Channel.voice_region` is not nullable anymore.
- Add `SortOrder`.
- Add `ChannelMetadataBase.default_sort_order`.
- Add `Channel.default_sort_order`.
- Add `ChannelMetadataGuildForum.default_sort_order`.
- Add `default_sort_order` parameter to `Channel.__new__`.
- Add `default_sort_order` parameter to `Channel.precreate`.
- Add `default_sort_order` parameter to `Client.channel_create`.
- Add `default_sort_order` parameter to `Client.channel_edit`.
- Add `default_sort_order` audit log change converter.

##### ext.slash
- Allow `hdsl` for slash command description.

#### ext.plugin_loader
- Add `mark_as_plugin_root_directory`

#### Bug Fixes

- `EventHandlerManager.__setattr__` did not wrap deprecated event handlers if required..
- `EventHandlerManager.__call__` wrapped deprecated event handlers after validating them.
- `client.events.webhook_update` used different parameters as documented.
- Deprecated event handlers did not accept instantiable types.

##### ext.patchouli
- When html rendering codeblocks the lines were not closed with linebreaks. (Event Horizon#2913)

#### Renames, Deprecation & Removals

- Deprecate `cr_pg_channel_object`. Please use `Channel(...).to_data(...)` instead.
- Rename `Integration.detail` to `.details`.
- Rename `IntegrationDetail` to `IntegrationDetails`.

## 1.3.9 *\[2022-10-03\]*

#### Improvements

- Add `create_partial_emoji_from_id`.
- Add `Channel.iter_applied_tag_ids`.
- Add `Channel.iter_applied_tags`.
- Add `Channel.iter_available_tags`.
- Move `ReactionMapping.__init__` to `.from_data`. Add `.__new__`.
- Move `ReactionMappingLine.__init__` to `.from_data`. Add `.__new__`.
- Add missing `ReactionMappingLine.__eq__`.
- Add missing `ReactionMappingLine.__bool__`.
- Add missing `ReactionMapping.__repr__`.
- Add missing `ReactionMapping.__bool__`.
- Add missing `ReactionMapping.__eq__`.
- Overwrite `ReactionMappingLine.remove`.

### Bug fixes

- `AttributeError` in `Client.channel_edit`.
- `create_emoji_from_exclusive_data` overwrote emoji name & animated.

##### ext.plugin_loader
- Importing from plugins could fail & built tree could be bad.
- Plugins wont reference themselves.
- Plugin reload order improved.

#### Renames, Deprecation & Removals

- Rename `reaction_mapping` to `ReactionMapping`.
- Rename `reaction_mapping_line` to `ReactionMappingLine`.
- Deprecate `reaction_mapping`.
- Deprecate `reaction_mapping_line`.

## 1.3.8 *\[2022-09-20\]*

#### Improvements

- Partial `ApplicationCommand`-s are now hashable.
- `ApplicationCommand.__new__` now accepts `options` as any iterable (from list | tuple).
- `ApplicationCommandOption.__new__` now accepts `choices` as any iterable (from list | tuple).
- Add `ApplicationCommandOption.__hash__`.
- `ApplicationCommandOption.__new__` now accepts `options` as any iterable (from list | tuple).
- Add `ApplicationCommandOptionChoice.__hash__`.
- Fix some linting errors in `UserBase` subclasses.
- `datetime_to_unix_time` now ignores what stdlib thinks.
- Add `Activity`.
- Add `ActivityMetadataBase`.
- Add `CustomActivityMetadata`.
- Add `RichActivityMetadata`.
- Add `ActivityType`.
- Add `GuildFeature.invites_disabled`.
- Add `ERROR_CODES.cannot_send_message_to_forum_channel`.
- Add `ERROR_CODES.no_tags_available_for_non_moderators`.
- Add `ERROR_CODES.tag_required`.
- Add `ChannelFlag.guild_feed_removed`.
- Add `ChannelFlag.active_channels_removed`.
- Add `ChannelFlag.require_tag`.
- Add `ChannelFlag.spam`.
- Add `ForumTag`.
- `create_partial_emoji_from_data` now prioritizes `emoji_` prefix fields.
- Add `ChannelMetadataGuildForum.flags`.
- Add `put_partial_emoji_data_into`.
- Add `MessageType.interaction_premium_upsell`.
- Add `MessageType`.
- Add `MessageTypeFlag`.
- Add `ConnectionType.paypal`.
- Add `ConnectionType.ebay`.
- Add `available_tags` audit log change converter.
- Add `Channel.available_tags`.
- Add `ChannelMetadataForum.available_tags`.
- Add `ChannelMetadataForum.flags`.
- Add `ChannelMetadataGuildThreadPublic.applied_tag_ids`.
- Add `Channel.applied_tag_ids`.
- Add `Channel.applied_tags`.
- Add `create_forum_tag_from_id`.
- Add `applied_tag_ids` audit log change converter.
- Add `ChannelMetadataGuildTextBase.default_thread_slowmode`.
- Add `Channel.default_thread_slowmode`.
- Add `Channel.default_thread_auto_archive_after`.
- Add `default_thread_slowmode` audit log change converter.
- Add `create_emoji_from_exclusive_data`.
- Add `create_emoji_from_exclusive_data`.
- `preconvert_snowflake_array` now accepts any iterable (from set | list | tuple).
- Add `put_exclusive_emoji_data_into`.
- Add `ChannelMetadataForum.default_thread_reaction`.
- Add `Channel.default_thread_reaction`.
- Add `default_thread_slowmode` parameter to `Channel.precreate`.
- Add `default_thread_reaction` parameter to `Channel.precreate`.
- Add `available_tags` parameter to `Channel.precreate`.
- Add `applied_tag_ids` parameter to `Channel.precreate`.
- Add `default_thread_reaction` audit log change converter.
- Add `dotted_line_face` unicode emoji.
- Add `permission_overwrites` parameter to `Channel.precreate`.
- Add `position` parameter to `Channel.precreate`.
- Add `parent_id` parameter to `Channel.precreate`.
- Add `created_at` parameter to `Channel.precreate`.
- Add `archived` parameter to `Channel.precreate`.
- Add `archived_at` parameter to `Channel.precreate`.
- Add `users` parameter to `Channel.precreate`.
- Channel metadatas now use `.from_data` for being constructed from data and `__new__` has been repurposed for partial
    constructing.
- Implement `IconSlot.__set__`.
- Add `__hash__` method to all channel metadata type.
- Add `Channel.from_data` (renamed `.__new__`).
- Repurpose `Channel.__new__` as a partial constructor.
- Add `guild_id` parameter to `Channel.precreate`.
- `hash` works on fully-partial channels correctly.
- `==` works on fully-partial channels correctly.
- `Channel.parent` will not be `None` if the channel has parent, but not cached.

### Bug fixes

- `Activity` timestamps are now correctly converted.
- `eventlist.__init__` failed on `pypy3.8`.
- `create_partial_emoji_from_data` handled new unicode emoji cases incorrectly. (from 1.3.4) (Gilgamesh#8939)
- Some thread fields were wrongly deserialized.
- `IconSLot.preconvert` could drop `TypeError`.
- `ChannelMetadataPrivate._create_empty` set `.name` incorrectly.
- `ChannelMetadataGuildBase._iter_users` raised `AttributeError`.
- `ChannelMetadataPrivate.name` was not a property.
- `Channel.created_at` raised `AttributeError`.
- `Channel.iter_users` could raise `TypeError`.
- `Message.custom` did not detect `guild_id` from channel correctly. (Gilgamesh#8939)
- Add 111 new emojis.

#### Renames, Deprecation & Removals

- Deprecate `ACTIVITY_TYPES`, use `ActivityType` instead.
- Deprecate `ActivityRich`, use `Activity` instead.
- Remove `ActivityBase`.
- Deprecate `ActivityCustom`, use `Activity` instead.
- Remove `ActivityUnknown`.
- Rename `ActivityRich.track_id` to `.spotify_track_id`.
- Deprecate `ActivityRich.track_id`.
- Rename `ActivityRich.track_url` to `.spotify_track_url`.
- Deprecate `ActivityRich.track_url`.
- Deprecate `with_count` parameter of `Client.invite_get`. (From now on, it will always default to `True`.)
- Rename `Channel.is_in_group_messageable` to `.is_in_group_textual` with deprecation notice.
- Rename `Channel.is_in_group_guild_messageable` to `.is_in_group_guild_textual` with deprecation notice.
- Rename `Channel.is_in_group_guild_main_text` to `.is_in_group_guild_system` with deprecation notice.
- Rename `Channel.is_in_group_can_contain_threads` to `.is_in_group_threadable` with deprecation notice.
- Rename `Channel.is_in_group_can_create_invite_to` to `.is_in_group_invitable` with deprecation notice.
- Rename `Channel.is_in_group_guild_movable` to `.is_in_group_guild_sortable` with deprecation notice.
- Rename `.default_auto_archive_after` to `.default_thread_auto_archive_after`
- Rename `ChannelMetadataGuildForum.slowmode` to `.default_thread_slowmode`.
- Deprecate `Activity.bot_dict`, use `.to_data()` instead.
- Deprecate `Activity.user_dict`, use `.to_data(user = True)` instead.
- Deprecate `Activity.full_dict`, use `.to_data(include_internal = True)` instead.

## 1.3.7 *\[2022-09-04\]*

#### Improvements

- Add `ApplicationCommand.nsfw`.

##### ext.slash
- Add `nsfw` parameter to `Client.interactions`.

### Bug fixes

- `ApplicationCommandOption.__eq__` could return incorrect value depending on constructor used and on `.max_length`'s
    value.
- `Application._difference_update_attributes` set a field in the difference wrongly.

#### ext.slash
- Fix an `AttributeError` after editing an application command.

#### Renames, Deprecation & Removals

##### ext.slash
- Rename `.is_default` and `.is_global` attributes to `.default` and `.global_`. (only attributes)

## 1.3.6 *\[2022-08-30\]*

#### Improvements

- Add `NsfwLevel.nsfw`.
- `Message.guild` now works for invoking user only messages as well. (Gilgamesh#8939)
- Add `IntegrationType`.
- Add `OA2Access.has_scope`.
- `OA2Access.scopes` are now `None | tuple<Oauth2Scope>` from `set<str>`.
- Add `Oauth2Scope`.
- Add `Integration.scopes`.
- `IntegrationDetail.synced_at` now defaults to `None`.
- `DiscordException` mentioned the response status twice at a few cases.

#### Bug Fixes

- `Guild.nsfw` returned the opposite value. (Gilgamesh#8939)
- `IntegrationAccount.__new__` could raise `TypeError`. (since 1.3.4)

#### Renames, Deprecation & Removals

- Rename `OA2Access` to `Oauth2Access`. Deprecate `OA2Access`.
- Rename `UserOA2` to `Oauth2User`. Deprecate `UserOA2`.

## 1.3.5 *\[2022-08-27\]*

#### Bug Fixes

##### ext.patchouli
- Fix an `IndexError`.

## 1.3.4 *\[2022-08-24\]*

#### Improvements

- Add `Message._create_from_partial_data`.
- `Message.cross_reference` now can be set only as a `Message` instance (or `None`).
- Add `Message._create_from_partial_fields`.
- Dead message events are dispatched as well.
- Add `EMOJI_ALL_RP`.
- Add `parse_all_emojis`.
- Add `parse_all_emojis_ordered`.
- Add `DiscordEntity.id.fset`, so linter wont cry anymore about unsettable fields.
- Add `ConnectionType.riot_games`.
- `ApplicationCommand.description_localizations` is now applied towards the it's length correctly.
- `ApplicationCommand.name_localizations` is now applied towards the it's length correctly.
- `ApplicationCommandOption.description_localizations` is now applied towards the it's length correctly.
- `ApplicationCommandOption.name_localizations` is now applied towards the it's length correctly.
- `ApplicationCommandOptionChoice.name_localizations` is now applied towards the it's length correctly.
- `Client.application_command_permission_edit` now accepts any iterable as ``permission_overwrites``.

#### Bug Fixes

- `Channel.get_users_like` raised.
- `Channel.permissions_for_roles` raised.
- `ApplicationCommand.__len__` raised `TypeError` when `.description` was `None`.

##### ext.slash
- Expression parser allowed XOR, OR, AND, LSHIFT, RSHIFT operation between floats.
- Expression parser had broken pointer-range detection logic.

#### Renames, Deprecation & Removals

- Rename `.is_bot` to `bot` to make it more intuitive.
- Deprecate `.is_bot` everywhere.
- Deprecate `MessageReference`.
- Deprecate `MessageRepr`.
- Remove `ALLOW_DEAD_EVENTS`.

## 1.3.3 *\[2022-08-13\]*

- Require the newest scarletio version*

## 1.3.2 *\[2022-08-13\]*

#### Improvements

- Add `EntitlementType.premium_purchase`.
- Add `EntitlementType.application_subscription`.
- `EntitlementType`'s `.name` style updated.
- `SKUType`'s `.name` style updated.
- `SKUAccessType`'s `.name` style updated.
- `SKUGenre`'s `.name` style updated.
- `SKUFeatureType`'s `.name` style updated.
- Add `view_creator_monetization_analytics` `Permission` flag.
- Add `DiscordException.__format__`.
- Add `DiscordException.errors`.
- Add `DiscordException.debug_info`.
- Add `DiscordException.request_info`.
- Add `DiscordException.message`.
- `DiscordHTTPClient` constructor now only requires `bot` and `token` parameters (from `client`).
- Add and use `resume_gateway_url`.

#### Bug Fixes

- `Channel.thread_users.fset` was set as a `CoroutineFunction` instead of a normal one.
- `unix_time` could go out of range on windows.
- Fix a `typo` in `Client.achievement_edit` which could cause falsely triggering `AssertionError`.

## 1.3.1 *\[2022-07-25\]*

#### Improvements

- The shutdown event handlers will be ensured when a client connection receives a fatal exception.
- Add `run` command.
- Add `ApplicationFlag.application_command_badge`.
- Add `delete_message_duration` parameter to `Client.guild_ban_add` replacing the old `delete_message_days`.
- Add `AutoModerationRuleTriggerType.mention_spam`.
- Add `MentionSpamTriggerMetadata`.
- Add `AutoModerationRule` parameter to `AutoModerationRule.__new__`.
- Add `AutoModerationRule` parameter to `AutoModerationRule.copy_with`.
- Separate down the `guild ban` endpoints from the `guild` ones.
- Add `delete_message_duration` audit log detail converter and update the `delete_message_days` one.
- `Client.user_guild_profile_edit` now accepts `roles` as any iterable.
- Add `timeout_duration` parameter to `Client.user_guild_profile_edit` replacing the old `timed_out_until`.
- Add missing `unix_time_to_datetime` import.
- Add `ApplicationCommand.mention_sub_command`.
- Add `ApplicationCommand.mention_with`.
- Add sub-command mention option for `ApplicationCommand.__format__`.
- Add `timeout_duration` parameter to `Client.guild_profile_edit` replacing the old `timed_out_until`.

#### Bug Fixes

- Fix `AttributeError` in `handle_voice_client_shutdown` (typo).
- `unix_time_to_datetime` returned bad value.
- `Client.guild_profile_edit` now accepts `guild` as `int` as expected.

#### Renames, Deprecation & Removals

- Deprecate `delete_message_days` parameter of `Client.guild_ban_add`. Use `delete_message_duration` instead.
- Deprecate `timed_out_until` parameter of `Client.user_guild_profile_edit`. Use `timeout_duration` instead.
- Deprecate `timed_out_until` parameter of `Client.guild_profile_edit`. Use `timeout_duration` instead.

## 1.3.0 *\[2022-07-19\]*

### Summary

CPI interface reworked. Register commands with the `@register` decorator.

Extra features are planned in future updates

#### Improvements

- Add `GuildFeature.embedded_activities_experiment`.
- Add `GuildFeature.home_test`.
- Add `ERROR_CODES.upload_file_not_found`.
- Add `ERROR_CODES.failed_to_resize_asset_below_max_size`.

#### Bug Fixes

- Fix `AttributeError` in `SlashCommand._add_autocomplete_function`. (Al_Loiz [ICU]#5392)
- Fix `AttributeError` in `ClientUserBase._from_client`.
- Fix `DeprecationWarning` in `EventHandlerManager.clear`.
- `User` alter ego was created of clients when the client was not yet finalized by startup at `Client._delete`.
- Fix `AttributeError` at `ChannelMetadataPrivateGroup._precreate`.
- Fix `TypeError` at `ChannelMetadataPrivateGroup._delete` when checking alter ego-s in private group channels.

## 1.2.19 *\[2022-07-10\]*

#### Improvements

- Add `ApplicationCommandOption.min_length`.
- Add `ApplicationCommandOption.max_length`.
- Add `reason` parameter to `Client.auto_moderation_rule_create`.
- Add `reason` parameter to `Client.auto_moderation_rule_edit`.
- Add `reason` parameter to `Client.auto_moderation_rule_delete`.
- Add `MessageInteraction.joined_name`.
- Add `MessageInteraction.sub_command_name_stack` (better naming required).
- Add `InteractionEvent.application_permissions`.
- Add `KeywordPresetTriggerMetadata.excluded_keywords`.
- Add `excluded_keywords` parameter to `KeywordPresetTriggerMetadata.__new__`.
- Add `KeywordPresetTriggerMetadata.iter_keyword_presets`.
- Add `excluded_keywords` to `AutoModerationRule.__new__`.
- Add `excluded_keywords` to `AutoModerationRule.copy_with`.
- Add `ERROR_CODES.application_not_yet_available`.
- Add `ERROR_CODES.interaction_failed_to_send`.
- Add `ERROR_CODES.webhook_can_create_thread_only_in_forum_channel`.
- Add `ERROR_CODES.billing_non_refundable_payment_source`.
- Add `ERROR_CODES.quarantined`.
- Add `quarantined` `UserFlag`.
- Add `AuditLogEvent.auto_moderation_alert_message`.
- Add `AuditLogEvent.auto_moderation_user_timeout`.
- Add `AuditLogEvent.creator_monetization_request_created`.
- Add `AuditLogEvent.creator_monetization_terms_accepted`.
- Add `AuditLogEvent.role_prompt_create`.
- Add `AuditLogEvent.role_prompt_edit`.
- Add `AuditLogEvent.role_prompt_delete`.
- Add `AuditLogEvent.guild_home_feature_item`.
- Add `AuditLogEvent.guild_home_remove_item`.

##### ext.slash

- Slash command parameters now support `min_length`.
- Slash command parameters now support `max_length`.

#### Bug Fixes

- `AutoModerationAction.__eq__` could return incorrect value.
- `AutoModerationAction.copy_with` set attributes badly.
- `AutoModerationAction.copy_with` could raise `AttributeError`.
- `SendAlertMessageActionMetadata.__new__` could set `channel_id` as `None`.
- `create_partial_user_from_id` did not cache the user as expected.
- `AutoModerationRule.copy_with` could raise `TypeError` with false reason.
- Always update loading messages.
- `UserBase.to_data` raised `TypeError`.
- `ZEROUSER` was not put in cache, which could cause false result in tests.

#### Renames, Deprecation & Removals

- Rename `MessageType.new_guild_subscription` to `.guild_boost`.
- Deprecate `MessageType.new_guild_subscription`.
- Rename `MessageType.new_guild_subscription_tier_1` to `.guild_boost_tier_1`.
- Deprecate `MessageType.new_guild_subscription_tier_1`.
- Rename `MessageType.new_guild_subscription_tier_2` to `.guild_boost_tier_2`.
- Deprecate `MessageType.new_guild_subscription_tier_2`.
- Rename `MessageType.new_guild_subscription_tier_3` to `.guild_boost_tier_3`.
- Deprecate `MessageType.new_guild_subscription_tier_3`.

## 1.2.18 *\[2022-06-27\]*

#### Improvements

- Add `auto_moderation_message` to rich embed fields.
- Add `ConnectionType`.
- Change `Connection.type` from `str` to `ConnectionType`.
- Mark guild voice channel type as messageable. (this was missing from the previous update.)
- Update the identity payload.
- Add `AutoModerationRuleTriggerType`.
- Add `auto_moderation_configuration` intent.
- Add `auto_moderation_execution` intent.
- Add `AutoModerationEventType`.
- `RichAttributeErrorBaseType` now supports rich attribute errors.
- Add `AutoModerationRuleTriggerMetadata`.
- Add `KeywordTriggerMetadata`.
- Add `KeywordPresetTriggerMetadata`.
- Add `AutoModerationKeywordPresetType`.
- Add `ScheduledEventEntityMetadata.__hash__`.
- Add `AutoModerationAction`.
- Add `AutoModerationActionType`.
- Add `AutoModerationActionMetadata`.
- Add `SendAlertMessageActionMetadata`.
- Add `TimeoutActionMetadata`.
- Warn if a dispatch event parser is missing.
- Add `AutoModerationActionExecutionEvent`.
- Add `Client.events.auto_moderation_action_execution`.
- Add `Client.events.auto_moderation_rule_create`.
- Add `Client.events.auto_moderation_rule_delete`.
- Add `Client.events.auto_moderation_rule_edit`.
- Add `Client.auto_moderation_rule_get`.
- Add `Client.auto_moderation_rule_get_all`.
- Add `Client.auto_moderation_rule_create`.
- Add `Client.auto_moderation_rule_edit`.
- Add `Client.auto_moderation_rule_delete`.
- Add `DiscordHTTPClient.auto_moderation_rule_get`.
- Add `DiscordHTTPClient.auto_moderation_rule_get_all`.
- Add `DiscordHTTPClient.auto_moderation_rule_create`.
- Add `DiscordHTTPClient.auto_moderation_rule_edit`.
- Add `DiscordHTTPClient.auto_moderation_rule_delete`.
- Add `RATE_LIMIT_GROUPS.auto_moderation_rule_get`.
- Add `RATE_LIMIT_GROUPS.auto_moderation_rule_get_all`.
- Add `RATE_LIMIT_GROUPS.auto_moderation_rule_create`.
- Add `RATE_LIMIT_GROUPS.auto_moderation_rule_edit`.
- Add `RATE_LIMIT_GROUPS.auto_moderation_rule_delete`.
- Add `AuditLog.auto_moderation_rules`.
- Add new audit log converters.
- `Guild.get_emoji_like` now strips the colons down from emoji names.
- `Guild.get_emojis_like` now strips the colons down from emoji names.
- Add `ComponentRow.__iter__`.
- Add `force_update` parameter to `Client.message_get`.
- `Client.message_get` now accepts `Message` / `(channel_id, message_id)` parameters from the old `channel, message_id`.
- Add `ERROR_CODES.invalid_payment_source`.
- Add `Client.request_all_members_of`.

##### ext.plugin_loader

- Raise `ModuleNotFoundError` instead of `ImportError` if the module is just not found. So simple.

### Bug fixes

- `Client.sticker_guild_get_all` raised `TypeError`.
- `Client.application_command_permission_edit` raised `NameError`.
- `Client.achievement_create` could raise `NameError`.
- `Client.thread_create` could raise `TypeError`˛
- `Client.permission_overwrite_edit` raised `NameError`
- `Client.channel_edit` could raise `NameError`.
- `Client.guild_edit` could raise `NameError`.
- `thread_user_create` could have raise `AttributeError`.
- `ReactionAddEvent.__eq__` could have return incorrect value.
- `Client.thread_create` raised `TypeError`.
- `Client._should_request_users` were not respected at `guild_create` events outside of startup.

#### Renames, Deprecation & Removals

- Rename `Client.guild_sync_roles` to `.guild_role_get_all`.
- Deprecate `Client.guild_role_get_all`.
- Rename `Client.guild_sync_channels` to `.guild_channel_get_all`.
- Deprecate `Client.guild_channel_get_all`.
- Deprecate `Client.client_edit`.
- Rename `Client.client_edit` to `.edit`.
- Deprecate `Client.client_guild_profile_edit`.
- Rename `Client.client_guild_profile_edit` to `.guild_profile_edit`.
- Deprecate `Client.client_connection_get_all`.
- Rename `Client.client_connection_get_all` to `.connection_get_all`.
- Deprecate `Client.client_edit_presence`.
- Rename `.client.application_get` to `.application_get_own` around the board.
- Rename `AuditLogTargetType.auto_moderation` to `AuditLogTargetType.auto_moderation_rule`.

## 1.2.17 *\[2022-06-12\]*

### Summary

Rename `extension_loader` to `plugin_loader` to make library extensions and extension modules more distinct.
A change like this was requested for a while...

#### Improvements

- `hata.ext` directory now handles sub-file imports better.
- Add `weak` parameter to `bind`.
- Add `weak_cache_size` parameter to `bind`.
- Add `Guild.vanity_url`.
- Add `ChannelMetadataGuildVoice.nsfw`.
- Add `parse_custom_emojis_ordered`.
- Add `User.iter_activities`.
- Add `ActivityChange.iter_added`.
- Add `ActivityChange.iter_updated`.
- Add `ActivityChange.iter_removed`.
- Add `ActivityRich.twitch_preview_image_url`.
- Add `ActivityRich.spotify_cover_id`.
- Add `ActivityRich.youtube_video_id`.
- Add `ActivityRich.youtube_preview_image_url`.
- Add missing `infinity_vs16` emoji.
- Add +1 builtin emoji.
- `parse_custom_emojis` now accepts `None` as well.
- `User._difference_update_profile` was not updated with deprecation.
- `User._update_profile` was not updated with deprecation.

##### ext.slash

- Guild level permission overwrites are now snapshotted.

##### ext.plugin_loader

- Add `load_plugin`.
- Add `register_plugin`.
- Add `load_all_plugin`.
- Add `register_and_load_plugin`.
- Add `unload_plugin`.
- Add `unload_all_plugin`.
- Add `reload_plugin`.
- Add `reload_all_plugin`.
- Add `get_plugin`.
- Add `get_plugin_like`.
- Add `get_plugins_like`.
- Add `add_default_plugin_variables`.
- Add `clear_default_plugin_variables`.
- Add `remove_default_plugin_variables`.
- Add missing `PluginModuleProxyType.__dir__`.
- Add `Plugin.is_directory`.
- Add `Plugin.add_sub_module_plugin`.
- Add `Plugin.iter_sub_module_plugins`.
- Add `Plugin.are_sub_module_plugins_present_in`.
- Add `Plugin.clear_sub_module_plugins`.
- Add `Plugin.remove_sub_module_plugin`.

### Bug fixes

- `parse_custom_emojis` could have return `emoji` with incorrect `animated` value.
- `Guild._sync_channels` could raise `TypeError`.

#### Renames, Deprecation & Removals

- Rename `ActivityRich.album_cover_url` to `.spotify_album_cover_url`.
- Deprecate `ActivityRich.album_cover_url`.
- Rename `ActivityRich.duration` to `.spotify_track_duration`.
- Deprecate `ActivityRich.duration`.

##### ext.plugin_loader

- Rename `Extension` to `Plugin` + deprecate.
- Rename `ExtensionLoader` to `PluginLoader` + deprecate.
- Rename `import_extension` to `import_plugin` + deprecate.
- Rename `ExtensionLoader.load_extension` to `.register_and_load` + deprecate.
- Rename `ExtensionLoader.add` to `.register` + deprecate.
- Rename `ExtensionLoader.get_extension` to `.get_plugin` + deprecate.

~~and much more~~

## 1.2.16 *\[2022-05-29\]*

### Summary

- Rework slash extension command structure.

#### Improvements

- Boost level 0 sticker count is now 5.
- `OA2Access` now support rich attribute errors.
- `OA2Access.__repr__` will no longer display the token. :derp:
- `Client.application_command_permission_edit` now accepts `5` parameters from old `4` since it required oauth2 access.
    Warning dropped.
- `Client.application_command_permission_edit`'s `application_command` parameter accepts `None` (or `0`) as well.
- `PermissionOverwrite` now support rich error messages.
- Add `ApplicationCommandPermissionOverwrite.copy_with`.
- `Client.application_command_permission_edit` now accepts role overwrites with id of `0` defaulting to the guild's
    default role.
- Add `SystemChannelFlag.role_subscription_purchase`.
- Add `SystemChannelFlag.role_subscription_purchase_replies`.
- Add `MessageFlag.should_show_link_not_discord_warning`.
- Add `ERROR_CODES.auto_moderation_title_blocked`.
- Add `ERROR_CODES.poggermode_temporarily_disabled`.

##### ext.slash

- Add `CommandBase`.
- Add `CommandBaseApplicationCommand`.
- Add `ContextCommand`
- Add `__hash__` & `__eq__` to all `CommandBase` subclass.
- `SlasherCommandWrapper` now support rich attribute errors.
- `CommandChange` now support rich attribute errors.
- `CommandState` now support rich attribute errors.
- Add `assert_application_command_permission_missmatch_at` parameter to `Slasher.__new__`.
- Add `enforce_application_command_permissions` parameter to `Slasher.__new__`.
- `set_permission` now can be matmul-ed with null, type of self, client, slasher instances.

#### Bug Fixes

- `Client.user_guild_get_all` asserted down bad scope.
- `Fix `AttributeError` in `ChannelMetadataGuildBase._from_partial_data` (I hate `super`).
- `Client.application_command_permission_edit` could change inputted ``ApplicationCommandPermissionOverwrite``'s hash
    value.

##### ext.slash

- Fix various missing attribute issues in `CommandBase` subclasses, in `.copy`, `.__eq__` methods.
- `Slasher.create_event` now correctly registers `FormSubmitCommand`-s.
- `Slasher.create_event` now correctly identifies `FormSubmitCommand`-s.
- `Slasher.delete_event` wont fail on `ComponentCommand`-s, `FormSubmitCommand`-s.


#### Renames, Deprecation & Removals
- Rename `MessageType.convert_auto_moderation_action` to `.auto_moderation_action`. (Ops)
- Deprecate `MessageType.new_guild_sub`.
- Deprecate `MessageType.new_guild_sub_t1`.
- Deprecate `MessageType.new_guild_sub_t2`.
- Deprecate `MessageType.new_guild_sub_t3`.
- Rename `MessageType.new_guild_sub` to `.new_guild_subscription`.
- Rename `MessageType.new_guild_sub_t1` to `.new_guild_subscription_tier_1`.
- Rename `MessageType.new_guild_sub_t2` to `.new_guild_subscription_tier_2`.
- Rename `MessageType.new_guild_sub_t3` to `.new_guild_subscription_tier_3`.
- Rename `ERROR_CODES.sticker_animation_duration_exceeds_5_second` to
    `.sticker_animation_duration_exceeds_five_seconds`.
- Deprecate `ERROR_CODES.sticker_animation_duration_exceeds_5_second`.

##### ext.slash

- Rename `SlasherApplicationCommand` to `SlashCommand`.
- Rename `SlasherApplicationCommandFunction` to `SlashCommandFunction`.
- Rename `SlasherApplicationCommandCategory` to `SlashCommandCategory`.
- Rename `CustomIdBasedCommand` to `CommandBaseCustomId`.
- Rename `.call_auto_completion` to `.invoke_auto_completion`.
- Rename `SlashCommandFunction._command` to `._command_function`.
- Rename `SlasherApplicationCommandParameterAutoCompleter` to `SlashCommandParameterAutoCompleter`.
- Rename `CommandBase.__call__` to `.invoke`.
- Rename `SlashCommandParameterAutoCompleter.__call__` to `.invoke`.

## 1.2.15 *\[2022-05-21\]*

#### Improvements

- Allow auto completing `number` and `float` parameters as well.
- `GuildUserChunkEvent.channel` will not return `None` anymore.
- `EmbeddedActivityState.channel` will not return `None` anymore.
- `WelcomeScreen` now supports rich attribute errors.
- `WelcomeChannel` now supports rich attribute errors.
- `WelcomeChannel.channel` will not return `None` anymore.
- `WebhookBase.channel` will not return `None` anymore.
- `VoiceClient.channel` will not return `None` anymore.
- `VoiceClient` now supports rich attribute errors.
- `VoiceState.channel` will not return `None` anymore.
- `ScheduledEvent.channel` will not return `None` if it **can have** channel.
- `MessageReference.channel` will not return `None` if it **can have** channel.
- `MessageReference` now supports rich attribute errors.
- Add `MessageType.role_subscription_purchase`.
- `ApplicationCommandOptionChoice.__new__`'s `name` parameter can be `Enum`.
- `ApplicationCommandOptionChoice.__new__`'s `value` parameter can be `Enum`.
- Add `ApplicationCommandCountUpdate`.
- Add `Client.events.application_command_count_update`.
- Ad `previously` button to docs.


##### ext.slash

- Allow pep 593 annotations. (WizzyGeek#2356)
- Allow enums as choices. (WizzyGeek#2356)

##### ext.solarlink

- `SolarPlayerBase.channel` will not return `None` anymore.

#### Bug Fixes

- Fix a `NameError` in `cr_pg_channel_object`.
- `MessageReference.channel_id` could been `None`.
- Fix `TypeError` in `preconvert_int_options`. (Coryf88#0317)

## 1.2.14 *\[2022-05-05\]*

#### Improvements

- Add `AuditLog.application_commands`.
- `AuditLog` now supports rich attribute messages.
- Add `MessageType.auto_moderation_action`.
- Update `MessageType.name`-s.
- Add `GuildFeature.auto_moderation_enabled`.
- Add `Client.forum_thread_create`.
- Add `slowmode` parameter to `Client.thread_create`.
- Add `ERROR_CODES.cannot_edit_sticker_within_message`.
- Increase max application command permission overwrite count from `10` -> `100`.
- Mark `allow_by_default` parameter in `ApplicationCommand.__new__` as deprecated.
- Add `ApplicationCommand.allow_in_dm`.
- `ApplicationCommand.required_permissions` now defaults to `Permission()` from `None`.
- Add `application_command_id` audit log change key converter.

#### Renames, Deprecation & Removals

- Deprecate `ApplicationCommand.allow_by_default`.

##### hata.ext.slash

- Add `allow_in_dm` is now accepted by `SlasherApplicationCommand`.

## 1.2.13 *\[2022-04-27\]*

#### Bug Fixes

- Fix a `TypeError` in `ClientUserBase.has_name_like_at`.

## 1.2.12 *\[2022-04-24\]*

#### Improvements

- Add `UserBase.has_name_like`.
- Add `UserBase.has_name_like_at`.
` Improve `.get_user_like` and `.get_users_like` methods.

##### hata.ext.extension_loader

- Add `blocking` parameter to `ExtensionLoader.load`.
- Add `blocking` parameter to `ExtensionLoader.unload`.
- Add `blocking` parameter to `ExtensionLoader.reload`.
- Add `blocking` parameter to `ExtensionLoader.load_all`.
- Add `blocking` parameter to `ExtensionLoader.unload_all`.
- Add `blocking` parameter to `ExtensionLoader.reload_all`.
- Add `blocking` parameter to `ExtensionLoader.load_extension`.
- Cross extension `import` statements are now picked up.

## 1.2.11 *\[2022-04-18\]*

#### Improvements

- `Guild.get_channel_like`'s `type` parameter is replaced with `type_checker`.
- Enable calling `hata` without `python3 -m`. (WizzyGeek#2356)
- `run_console_till_interruption` will now indeed stop at interruption and not only at system exit. (Gilgamesh#8939)

##### hata.ext.commands_v2

- Add `alternative_checked_types` to `ConverterSetting`.
- Channel parameter annotations are now picked up familiarly to slash commands in favor of deprecating the type usage.

#### Bug Fixes

- `Client.message_get_chunk_from_zero` could raise `AttributeError`.
- `Client.message_get_chunk` could raise `AttributeError`. (winwinwinwin#0001)

## 1.2.10 *\[2022-04-16\]*

#### Bug Fixes

- Fix an `AttributeError` in `get_channel_id`. (koish#5800)
- Fix an `AttributeError` in `get_channel_guild_id_and_id`. (koish#5800)
- Fix a `TypeError` in `Channel.is_guild_voice`. (koish#5800)
- Fix a `TypeError` in `Channel.is_...` non-group methods.

##### hata.ext.commands_v2

- Fix a `TypeError` in `guild_converter`. (Gilgamesh#8939)
- Fix a `TypeError` in `invite_converter`.

## 1.2.9 *\[2022-04-16\]*

### Summary

- Add `hata.ext.solarlink`.

#### Improvements

- `EventHandlerBase` instances now support rich attribute errors.
- Define we want to use python3 highlights in md files, because some highlighters still use python2 as default.

##### ext.extension_loader

- `import_extension` now supports keyword parameters.
- Add `ExtensionLoader.add_done_callback`.
- Add `ExtensionLoader.add_done_callback_unique`.
- Add `ExtensionLoader.call_done_callbacks`.
- Add missing `EventHandlerSnapshotType.__repr__`.
- Improve snapshot extraction inheritance logic.
- Add `deep` parameter of `ExtensionLoader.load` defaults to `True`.
- Add `deep` parameter of `ExtensionLoader.unload` defaults to `True`.
- Add `deep` parameter of `ExtensionLoader.reload` defaults to `True`.
- Building shallow extensions trees  wont include children and parents.

##### ext.slash

- `SlashParameter` now supports rich attribute messages.
- `SlasherApplicationCommandParameterConfigurerWrapper` now support `autocomplete` parameter.
- `SlashParameter` now support `autocomplete` parameter.

#### Bug Fixes

- `Client.achievement_edit` could raise `TypeError` on older api versions.
- `Client.extensions` could raise `TypeError`. (from 1.2.6)

##### ext.extension_loader

- `ExtensionLoader` will return the same instance if already instanced. (Gilgamesh#8939)
- `ExtensionLoader.reload_all` raised `TypeError`. (from 1.2.7) (Forest#2913)
- `Extension.add_snapshot_extraction` was not storing the snapshots correctly.
- `Extension` default variables were not updated even if required. This could cause bugs when reloading nested
      extensions.

##### ext.slash

- `IndexError` in `match_application_commands_to_commands`. (Gilgamesh#8939)

## 1.2.8 *\[2022-04-11\]*

#### Improvements

- `Message.channel` now always returns a `Channel`. (WizzyGeek#2356)

#### Bug Fixes

- `ClientUserBase.can_use_emoji` could return incorrect value.
- Fix an `AttributeError` in `WebhookSourceChannel.channel`.
- `run_console_till_interruption` could raise `TypeError`. (Gilgamesh#8939)

##### ext.patchouli

- `TypeSerializer` could raise `TypeError`. (typo) (Gilgamesh#8939)

## 1.2.7 *\[2022-04-10\]*

#### Improvements

- Add `ERROR_CODES.unknown_tag`.
- Add `ERROR_CODES.max_pinned_threads_in_forum_channel`.
- Add `ERROR_CODES.max_forum_channel_tags`.
- Add `ERROR_CODES.tag_name_not_unique`.
- Move out `ChannelMetadataThreadBase.invitable` field to `ChannelMetadataThreadPrivate`.
- Add `ChannelFlag`.
- Add default `flags` attribute to every `ChannelMetadataBase` subclass.
- Add `ChannelMetadataThreadPublic.flags`.
- Add `ChannelFlag` audit log converter.
- Add `Channel.flags`.
- Add `ChannelMetadataGuildForum.topic`.
- Add `ChannelMetadataGuildForum.slowmode`.
- Add `ApplicationCommand.guild`.
- Add `ApplicationCommand.guild_id`.
- Update `guild_ban_get_chunk` endpoint's rate limits.
- Add `Client.guild_ban_get_chunk`.
- `ObjectBinderBase` now support rich attribute errors..
- Add `ObjectBinderBase.clear`.
- Add `ObjectBinderBase.supports_clearing`.
- Add `ObjectBinderBase.supports_state_transfer`.
- Add `ObjectBinderBase.__repr__`.
- Add `ObjectBinderBase.iter_true_items`.
- Add `ObjectBinderBase.get_states`.
- Add `ObjectBinderBase.set_states`.
- `ObjectBinderBase` now support re-assigning the same value.

#### ext.extension_loader

- Add `deep` parameter to `ExtensionLoader.load`.
- Add `deep` parameter to `ExtensionLoader.unload`.
- Add `deep` parameter to `ExtensionLoader.reload`.

#### Renames, Deprecation & Removals

- Rename `DiscordHTTPClient.guild_ban_get_all` to `.guild_ban_get_chunk`.
- Rename `RATE_LIMIT_GROUPS.guild_ban_get_all` to `.guild_ban_get_chunk`.

#### Bug Fixes

- Thread metadata field were missing when calling `Channel.to_data()`.

#### ext.extension_loader

- Fix a dead lock when importing through an extension's `__init__.py` file.

#### ext.commands_v2

`ClientWrapperExtension` was not extended with the `.commands` decorator. (Gilgamesh#8939)

## 1.2.6 *\[2022-04-07\]*

### Summary

Channels now have a metadata system, making every channel share the same type.

This fixes a case when a precreated channel could mess up the channel's and other related entities lifecycle.

#### Improvements

- Add `should_request_users` parameter to `Client` constructor.
- Add `Channel` type inheriting all methods & properties of the old `ChannelBase`.
- Add `Channel.is_in_group_messageable`.
- Add `Channel.is_in_group_guild_messageable`.
- Add `Channel.is_in_group_guild_main_text`.
- Add `Channel.is_in_group_connectable`.
- Add `Channel.is_in_group_guild_connectable`.
- Add `Channel.is_in_group_private`.
- Add `Channel.is_in_group_guild`.
- Add `Channel.is_in_group_thread`.
- Add `Channel.is_in_group_can_contain_threads`.
- Add `Channel.is_guild_text`.
- Add `Channel.is_private`.
- Add `Channel.is_guild_voice`.
- Add `Channel.is_private_group`.
- Add `Channel.is_guild_category`.
- Add `Channel.is_guild_announcements`.
- Add `Channel.is_guild_store`.
- Add `Channel.is_thread`.
- Add `Channel.is_guild_thread_announcements`.
- Add `Channel.is_guild_thread_public`.
- Add `Channel.is_guild_thread_private`.
- Add `Channel.is_guild_stage`.
- Add `Channel.is_guild_directory`.
- Add `Channel.is_guild_forum`.
- Add `CHANNEL_TYPES.GROUP_IN_PRODUCTION`.
- Add `get_channel_type_name`.
- Add `get_channel_type_names`.
- Add `Channel.is_in_group_can_create_invite_to`.
- Add `CHANNEL_TYPED.GROUP_CAN_CREATE_INVITE_TO`.
- Add `CHANNEL_TYPES.GROUP_GUILD_MOVABLE`.
- Add `Channel.is_in_group_guild_movable`.
- Add `HubType`.
- Add `Guild.hub_type`.
- Add `hub_type` audit log converter.
- Add `send_start_notification` parameter to `Client.stage_create`.
- Enable animated `banner` in `Client.guild_edit` if the guild has `animated banner` feature.
- Do not require community feature in `Client.guild_edit` to edit `description`.
- Set `form` title max length to `45`.

##### ext.extension_loader

- Exception messages will not show internal frames.
- `Extension` class now supports rich attribute errors.
- When circularly loading extensions, `ImportError` is raised.
- `EXTENSION_LOADER.load_extension` returns the loaded extension.
- Add `Extension.__gt__`.
- Add `Extension.__lt__`.
- `EXTENSION_LOADER.load` returns the loaded extensions.
- `EXTENSION_LOADER.unload` returns the unloaded extensions.
- `EXTENSION_LOADER.reload` returns the reloaded extensions.
- Add `Extension.path`.
- Now python implementation errors wont stop us to load & reload modules caused by dead locked imports.
- Sync extension loading & unloading to avoid parallel calls on a single file.
- `ExtensionLoader` class now supports rich attribute errors.

##### ext.commands_v2

- Add missing `CommandContentParser.__repr__`.
- `CommandContentParser` now support rich attribute error messages.
- Add missing `CommandContentParser.__eq__`.
- Add missing `CommandContentParser.__hash__`.
- `ContentParserParameter` now support rich attribute error messages.
- Add missing `ContentParserParameter.__eq__`.
- Add missing `ContentParserParameter.__hash__`.
- `ContentParserParameterDetail` now support rich exception messages.
- Add missing `ContentParserParameterDetail.__eq__`.
- Add missing `ContentParserParameterDetail.__hash__`.
- `ConverterSetting` now support rich attribute error messages.
- Add missing `ConverterSetting.__eq__`.
- Add missing `ConverterSetting.__hash__`.
- `ContentParameterParser` now support rich exception messages.
- `ContentParameterParserContextBase` now support rich attribute error messages.
- Add missing `ContentParameterParserContextBase.__repr__`.
- Add missing `ContentParameterParserContextBase.__eq__`.
- Add missing `ContentParameterParserContextBase.__hash__`.
- Add missing `CommandProcessor.__repr__`.

#### Bug Fixes

- `datetime_to_unix_time` returned incorrect value.
- `run_console_till_interruption` could raise is called outside from a module. (Forest#2913)
- `User.from_data` didn't update guild profile every time.

##### ext.slash

- `Slasher.discard_kept_commands` was missing the last `s` from the end. :derp:

##### ext.commands_v2

- Commands were not unlinked correctly.

#### Renames, Deprecation & Removals

- Deprecate `ChannelBase`.
- Deprecate `ChannelTextBase`.
- Deprecate `ChannelGuildBase`.
- Deprecate `ChannelGuildMainBase`.
- Deprecate `ChannelCategory`.
- Deprecate `ChannelDirectory`.
- Deprecate `ChannelForum`.
- Deprecate `ChannelStore`.
- Deprecate `ChannelGuildUndefined`.
- Deprecate `ChannelVoiceBase`.
- Deprecate `ChannelVoice`.
- Deprecate `ChannelStage`.
- Deprecate `ChannelPrivate`.
- Deprecate `ChannelGroup`.
- Deprecate `ChannelThread`.
- Rename `CHANNEL_NAMES.GROUP_GUILD_TEXT_LIKE` to `.GROUP_GUILD_MAIN_TEXT`.
- Deprecate `Guild.booster_count`.
- Rename `Guild.booster_count` to `.boost_count`.
- Deprecate `ButtonStyle.violet`.
- Rename `ButtonStyle.violet` to `.blue` (seems like they never intended it to be burple)

## 1.2.5 *\[2022-03-23\]*

#### Improvements

- `allow_by_default` should not default based on `required_permissions`.
- Force request application command localizations.
- Improve `DiscordGatewayException` error messages.
- Improve `ChannelTextBase` docs mentioning that you are looking at a bad class for general channel methods.
- Plugged in cli commands are now supported.
- Add `Locale.native_name`.

### Bug fixes

- Use `create_event_loop` instead of `EventThread`, so `get_event_loop` wont fail in the main thread initially.

#### Renames, Deprecation & Removals

- Rename `Locale.spanish_sp` to `.spanish`
- Deprecate `Locale.spanish_sp`.
- Rename `Locale.portuguese_br` to `.portuguese`
- Deprecate `Locale.portuguese_br`.

## 1.2.4 *\[2022-03-15\]*

#### Improvements

- Add `ApplicationCommand.version`.
- Add `ApplicationCommand.edited_at`.
- Add `e` format code to `ApplicationCommand`.
- Add `ApplicationCommand._create_empty`.
- `ApplicationCommandOption` now supports rich attribute errors.
- `ApplicationCommandOptionChoice` now supports rich attribute errors.
- `ApplicationCommandPermission` now supports rich attribute errors.
- `ApplicationCommandPermissionOverwrite` now supports rich attribute errors.
- `Client.achievement_create`'s `description_localizations` parameter is now validated.
- `Client.achievement_create`'s `name_localizations` parameter is now validated.
- `Client.achievement_edit`'s `description_localizations` parameter is now validated.
- `Client.achievement_edit`'s `name_localizations` parameter is now validated.
- Add `required_permissions` parameter to `ApplicationCommand.__new__`.
- Add `ApplicationCommand.required_permissions`.
- `ApplicationCommandOptionChoice.__new__`'s `value` parameter is not optional and defaults to `name`.
- Add `name_localizations` parameter to `ApplicationCommandOptionChoice.__new__`.
- Add `ApplicationCommandOptionChoice.name_localizations`.
- Add `name_localizations` parameter to `ApplicationCommandOption.__new__`.
- Add `ApplicationCommandOption.name_localizations`.
- Add `description_localizations` parameter to `ApplicationCommandOption.__new__`.
- Add `ApplicationCommandOption.description_localizations`.
- Add `name_localizations` parameter to `ApplicationCommand.__new__`.
- Add `ApplicationCommand.name_localizations`.
- Add `description_localizations` parameter to `ApplicationCommand.__new__`.
- Add `ApplicationCommand.description_localizations`.
- Add `ApplicationCommandOptionChoice.copy`.
- Add `OA2Access.expires_at`.
- `ApplicationCommand.__new__`'s `description` parameter defaults to `name` one.
- Add `ApplicationCommand.apply_translation`.
- Add `ApplicationCommandOption.apply_translation`.
- Add `ApplicationCommandOptionChoice.apply_translation`.
- Add `ComponentType.user_select`.
- Add `ComponentType.role_select`.
- Add `ComponentType.mentionable_select`.
- Add `ComponentType.channel_select`.

#### ext.slash
- Add `required_permissions` parameter to slasher application commands.
- Add `SlasherSyncError` to improve sync exceptions' readability. (experimental)

### Bug fixes

- `Achievement.description_localizations` not correctly defaulted to `None`.
- `Achievement.name_localizations` not correctly defaulted to `None`.
- `ChannelGuildBase.to_data` returned incorrect value (typo). (FoxeiZ)

#### Renames, Deprecation & Removals

- Rename `OA2Access.expires_in` to `.expires_after`.
- Deprecate `OA2Access.expires.in`.

## 1.2.3 *\[2022-03-08\]*

#### Improvements

- Change embed author constructor parameter order to `name, icon_url, url` from `icon_url`, `name`, `url`. On this
    way it is more intuitive and matches the footer's parameter order as well. Drop warning if passed in bad order.
- `MessageInteraction` now picks up the `member` field from payload.
- Update max auto-completion options to 25 (from 20).
- Auto generate bit flag getters, setters and deleters instead of using descriptors (this improves performance).
- Add `ERROR_CODES.invalid_oauth2_redirect_url`.

#### ext.slash
- `int` fields with applied max or min values are translated to `number` ones.

### Bug fixes
- `Sticker.user` was not updated when expected.
- Update message content fields correctly when polling from cache.

#### Renames, Deprecation & Removals
- Rename `start_embedded_activities` to `use_embedded_activities` permission.
- Add deprecated `Permission.can_start_embedded_activities` property.

## 1.2.2 *\[2022-02-28\]*

#### Improvements

- Add `User.from_data`. New user constructor, which can bind guild profile even if the guild is uncached.
- Add `ERROR_CODES.unknown_guild_welcome_screen`.
- `Role` constructor now accepts `guild_id` instead of `Guild`.
- `Client.events.guild_user_add` will fire instantly even if the guild is not cached.
- `Client.events.role_create` will fire instantly even if the guild is not cached.
- Add `VoiceServerUpdateEvent.guild` property.
- Add `GuildUserChunkEvent.guild` property.
- Add `WebhookUpdateEvent`.

### Bug fixes

- `_delete_reaction_with_task` ignored `GeneratorExit`.
- `Client.connect` ignored `GeneratorExit`.
- `WaitForHandler.__call__` ignored `GeneratorExit`.
- `_with_error` ignored `GeneratorExit`.

##### ext.commands_v2

- `CommandProcessor.__call__` ignored `GeneratorExit`.
- `process_command_coroutine_generator` ignored `GeneratorExit`.
- `CheckCustom.__call__` ignored `GeneratorExit`.
- `CommandContext.invoke` ignored `GeneratorExit`.

##### ext.command_utils

- `ChooseMenu.__call__` ignored `GeneratorExit`.
- `Closer.__call__` ignored `GeneratorExit`.
- `UserMenu.__call__` ignored `GeneratorExit`.
- `UserMenu._handle_close_exception` ignored `GeneratorExit`.
- `PaginationBase._handle_close_exception` ignored `GeneratorExit`.
- `Pagination.__call__` ignored `GeneratorExit`.

##### ext.extension_loader

- `ExtensionLoader._load_extension` ignored `GeneratorExit`.
- `ExtensionLoader._unload_extension` ignored `GeneratorExit`.

#### ext.slash

- `acknowledge_component_interaction` ignored `GeneratorExit`.
- `Slasher._sync_permission_task` ignored `GeneratorExit`.
- `Slasher._create_command` ignored `GeneratorExit`.
- `Slasher._delete_command` ignored `GeneratorExit`.
- `Slasher._edit_command` ignored `GeneratorExit`.
- `Slasher._edit_guild_command_to_non_global` ignored `GeneratorExit`.
- `Slasher._register_command_task` ignored `GeneratorExit`.
- `Slasher._dispatch_application_command_event` ignored `GeneratorExit`.
- `Slasher._dispatch_application_command_autocomplete_event` ignored `GeneratorExit`.
- `Slasher._sync_guild_task` ignored `GeneratorExit`.
- `Slasher._sync_global_task` ignored `GeneratorExit`.
- `process_command_coroutine_generator` ignored `GeneratorExit`.
- `Menu._handle_close_exception` ignored `GeneratorExit`.
- `Menu.__call__` ignored `GeneratorExit`.
- `Menu._canceller_function` ignored `GeneratorExit`.
- `FormSubmitCommand.__call__` ignored `GeneratorExit`.
- `handle_command_exception` ignored `GeneratorExit`.
- `ComponentCommand.__call__` ignored `GeneratorExit`.
- `SlasherApplicationCommandFunction.__call__` ignored `GeneratorExit`.
- `SlasherApplicationCommandParameterAutoCompleter.__call__` ignored `GeneratorExit`.

#### Renames, Deprecation & Removals

- Deprecate `User.__new__`. Use `User.from_data` instead.
- `Client.events.webhook_update` now has `client, events` parameters (from `client, channel`). If added with `channel`
    parameter, deprecation is dropped.

## 1.2.1 *\[2022-02-22\]*

#### Improvements

- Add `DiscordException.debug_options`.

### Bug fixes

- `Sticker.description` now correctly defaults to `None`.

## 1.2.0 *\[2022-02-20\]*

### API v10 checklist:

- \[ALL VERSIONS\] application.summary now returns an empty string. This field will be removed in v11 \[x\]
- Achievement localization format has changed. name and description are now strings, and localized strings are now
    stored in name_localizations and description_localizations \[x\]
- /channels/<channel_id>/threads/active has been removed \[x\]
- Existing attachments must be specified when PATCHing messages with new attachments. Any attachments not specified
    will be removed and replaced with the specified list \[x\]
- Audit log reason as a body/query parameter is no longer supported, and you should instead use the X-Audit-Log-Reason
    header. \[x\]
- Message routes accept embeds rather than embed \[x\]
- Requests to v10 and higher will no longer be supported on discordapp.com \[x\]

#### Improvements
- API v10 hype.
- Add `message_content` intent.
- Add `create_identifier_custom_id_from_name`.
- `ComponentTextInput` now auto-generates `custom_id` from `label` parameter instead.
- `ComponentSelectOption`'s `label` parameter is optional and defaults to `value`. (Gilgamesh#8939)
- Add `Achievement.description_localizations`.
- Add `Achievement.name_localizations`.
- Add `description_localizations` parameter to `Client.achievement_create`.
- Add `name_localizations` parameter to `Client.achievement_create`.
- `Client.achievement_get` now accepts `Achievement` instances as well.
- Add `description_localizations` parameter to `Client.achievement_edit`.
- Add `name_localizations` parameter to `Client.achievement_edit`.
- Add `EmbeddedActivityConfiguration.premium_tier_treatment_default`.
- Add `EmbeddedActivityConfiguration.premium_tier_treatment_map`.
- Add `VoiceRegion.deprecated`.
- Add `force_update` parameter to `Client.emoji_get`.
- Add `Emoji._set_attributes`.
- Add `Client.emoji_guild_get_all` (renamed from `guild_sync_emojis`).
- `Client.emoji_edit` now accepts snowflake pair as well.
- `Client.emoji_guild_get_all` wont create a partial guild.
- `Client.emoji_guild_get_all` now returns a list emojis.
- `Client.sticker_guild_get_all` wont create a partial guild.
- `Client.sticker_guild_get_all` now returns a list emojis.
- Add missing `InteractionResponseContext.__repr__`.
- Add `Message.has_any_content_field`.
- Update content fields of message if required.
- Synchronise message edit dispatch event parsers based on message content availability.

#### ext.slash

- Returned and yielded values from form commands will depending the form was invoked by a message component or
    application command.
- Followup yields from a message component command are sent followup messages instead of editing the source message.

#### Bug Fixes

- `Guild.get_emoji_like` returned the default value always. (from 1.1.137)
- `Guild.get_sticker_like` returned the default value always. (from 1.1.137)
- `Guild.get_stickers_like` returned the empty list.
- Deferred interactions were never marked as responded.

#### Renames, Deprecation & Removals

- `IntegrationApplication.summary` is removed & deprecated.
- `Application.summary` is removed & deprecated.
- `summary` parameter of `Application.precreate` is deprecated.
- `Guild.region` is removed & deprecated.
- `region` parameter of `Client.guild_create` is deprecated.
- `region` parameter of `Guild.precreate` is deprecated.
- `region` parameter of `Client.guild_edit` is deprecated.
- `Client.emoji_get`'s 2nd parameter is deprecated.
- Deprecate `Client.guild_sync_emojis`.
- `Client.sticker_guild_get`'s 2nd parameter is deprecated.
- Deprecate `Client.guild_sync_stickers`.


## 1.1.137 *\[2022-02-15\]*

#### Improvements

- Add `ERROR_CODES.interaction_already_acknowledged`.
- Add `AllowedMentionProxy.update` now returns itself.
- Add `AllowedMentionProxy.__and__`.
- Add `AllowedMentionProxy.__rand__`.
- Add `AllowedMentionProxy.__xor__`.
- Add `AllowedMentionProxy.__rxor__`.
- Add `AllowedMentionProxy.__or__`.
- Add `AllowedMentionProxy.__ror__`.
- Add `AllowedMentionProxy.__add__`.
- Add `AllowedMentionProxy.__radd__`.
- Add `AllowedMentionProxy.__sub__`.
- Add `AllowedMentionProxy.__rsub__`.
- Add `AllowedMentionProxy.__iter__`.
- Add `GuildFeature.creator_monetizable`.
- Add `GuildFeature.creator_monetizable_disabled`.
- Add `seconds_to_elapsed_time` (requires dateutil).
- Add `Message.iter_attachments`.
- Add `Message.iter_embeds`.
- Add `Message.iter_stickers`.
- Add `Guild.forum_channels`.
- Add `Guild.get_emojis_like`.
- `Guild.get_sticker_like` now matches tags as well.
- Add `Guild.get_stickers_like`.
- Add `Sticker.iter_tags`.
- `EmbeddedActivityState`-s now raise rich attribute errors.
- Add ``ActivityFieldBase`` base class for activity fields.
- Add `ActivityTimestamps.__hash__`.
- Add `ActivityAssets.__hash__`.
- Add `ActivityParty.__hash__`.
- Add `ActivityParty.__hash__`.
- Add `ActivitySecrets.__hash__`.
- Add `ActivityTimestamps.__hash__`.
- Add `ActivityAssets.__bool__`.
- Add `ActivityParty.__bool__`.
- Add `ActivityParty.__bool__`.
- Add `ActivitySecrets.__bool__`.
- `ActivityBase`-s now raise rich attribute errors.
- `VerificationScreen`-s now raise rich attribute errors.
- `VerificationScreenStep`-s now raise rich attribute errors.
- `TeamMember`-s now raise rich attribute errors.
- `RateLimitGroup`-s now raise rich attribute errors.
- `RateLimitContextBase`-s now raise rich attribute errors.
- `RateLimitHandlerBase`-s now raise rich attribute errors.
- `Icon`-s now raise rich attribute errors.
- `PreinstancedBase`-s now raise rich attribute errors.
- Add new embeddable activities (still experimental).
- Add `AuditLogEvent.auto_moderation_rule_create`.
- Add `AuditLogEvent.auto_moderation_rule_edit`.
- Add `AuditLogEvent.auto_moderation_rule_delete`.
- Add `AuditLogEvent.auto_moderation_block_message`.
- Add `ERROR_CODES.activity_launch_no_access`.
- Add `ERROR_CODES.activity_launch_premium_tier`.
- Add `ERROR_CODES.activity_launch_concurrent_activities`.
- Add `ERROR_CODES.invalid_user_settings_data`.
- Add `ERROR_CODES.auto_moderation_message_blocked`.
- Add `AuditLogTargetType.auto_moderation`.
- Add `Application.max_participants`.
- Add `EmbeddedActivityConfiguration`.
- Add `Activity.embedded_activity_configuration`.
- Add `ERROR_CODES.terms_of_service_required`.
- Add `ERROR_CODES.auto_moderation_message_blocked`.

#### ext.slash
- `get_request_coroutines` now wont acknowledge the interaction event if it returns `None`.

### Bug fixes
- `AllowedMentionProxy.update` could set `._allow_replied_user` incorrectly.

#### ext.slash
- `allowed_mentions` response modifier was not applied correctly.

## 1.1.136 *\[2022-02-09\]*

#### Improvements
- Move `ext.asyncio` to `scarletio`.

### Bug fixes

- `_debug_component_text_input_value` checked for bad type. (Gilgamesh#8939)
- `AttributeError` in `Guild._difference_update_attributes`.
- `AttributeError` in `AllowedMentionProxy.__hash__`.

##### ext.slash
- `get_show_for_invoking_user_only_of` could return `None`.

## 1.1.135 *\[2022-02-08\]*

#### Improvements

- Add `ScheduledEvent.image_url`.
- Add `ScheduledEvent.image_url_as`.
- Remove extra redirect in interaction client methods, since it could(?) confuse flow order.
- Add `run_console_till_interruption` (experimental).

##### ex.top_gg
- Add missing `TopGGClient.__repr__`.

### Bug fixes

- `Client.channel_follow` raised `NameError`.

##### ext.commands_v2
- `CommandProcessor.commands` is now populated correctly.


## 1.1.134 *\[2022-01-25\]*

### Summary

Rework audit logs once again.

#### Improvements

- Add `InviteType`.
- Add `Invite.type`.
- Add `type` parameter to `Invite.precreate`.
- Add `Invite.nsfw_level`.
- Add `type` parameter to `Invite.nsfw_level`.
- Add `invite._create_empty`.
- Add `Client.edit_presence`. (Forest#2913)
- Add `suppress_embeds` parameter to `Client.message_create`.
- Make `Client.message_suppress_embeds` work again (it's endpoint was removed).
- Add `suppress_embeds` parameter to `Client.interaction_followup_message_create`.
- Add `suppress_embeds` parameter to `Client.interaction_response_message_create`.
- Update `AuditLogEvent` names.
- Add `AuditLogEvent.application_command_update`.
- Add `AuditLogEvent.target_type`.
- Add `AuditLogTargetType`.
- Add `AuditLogRole` Now these are used inside of audit logs instead of generic `Role` objects.
- Add `NsfwLevel` change key converter for audit logs.
- Add `StickerFormat` change key converter for audit logs.
- Add `guild_id` change key converter for audit logs.
- Add `preferred_locale` change key converter for audit logs.
- Add `user_limit` change key converter for audit logs.
- Add `pending` change key converter for audit logs.
- Add `available` change key converter for audit logs.
- Add `image` change key converter for audit logs.
- Add `afk_timeout` change key converter for audit logs.
- Add `role_ids` change key converter for audit logs.
- Add `parent_id` transformer to audit logs.
- Add `invitable` transformer to audit logs.
- Add `AuditLogEvent.stage_create`.
- Add `AuditLogEvent.stage_update`.
- Add `AuditLogEvent.stage_delete`.
- Add `AuditLogEntry.target_id`.
- Add `AuditLogEntry.parent`.
- `AuditLogIterator` is now `AuditLog` subclass.
- Add `ALLOW_DEBUG_MESSAGES` env variable.
- Add `ApplicationCommandAutocompleteInteraction.get_non_focused_values`.
- Add `ERROR_CODES.rate_limit_edit_to_message_older_than_one_hour`.
- Add `ChannelThread._created_at`.
- Add `created_at` parameter to `ChannelThread.precreate`.
- Add `asset` change key converter for audit logs. (sticker)
- Add `id` change key converter for audit logs. (sticker)
- Add `type` change key converter for audit logs. (sticker)
- Add `location` change key converter for audit logs. (scheduled event)
- Add `type` change key converter for audit logs. (webhook)
- Add `application_id` change key converter for audit logs. (webhook)

##### ext.slash
- Default slasher exception handler now forwards error message for message component interactions as well.
- Add `suppress_embeds` parameter to `InteractionResponse.__init__`.
- Add `suppress_embeds` parameter to `abort`.

#### Bug Fixes

##### ext.asyncio
- Add missing `Task._log_destroy_pending`. (Nova#3379)


#### Renames, Deprecation & Removals

- Rename `Client.message_edit`'s `suppress` parameter to `suppress_embeds`.
- Deprecate `Client.message_edit`'s `suppress` parameter in favor of `suppress_embeds`.
- Rename `AuditLogEvent.channel_overwrite_create` to `.channel_permission_overwrite_create`.
- Deprecate `AuditLogEvent.channel_overwrite_create` in favor of `.channel_permission_overwrite_create`.
- Rename `AuditLogEvent.channel_overwrite_update` to `.channel_permission_overwrite_update`.
- Deprecate `AuditLogEvent.channel_overwrite_update` in favor of `.channel_permission_overwrite_update`.
- Rename `AuditLogEvent.channel_overwrite_delete` to `.channel_permission_overwrite_delete`.
- Deprecate `AuditLogEvent.channel_overwrite_delete` in favor of `.channel_permission_overwrite_delete`.

## 1.1.133 *\[2022-01-15\]*

#### Improvements

- Add `wait` parameter to `client.interaction_application_command_acknowledge`.
- Add `wait` parameter to `client.interaction_component_acknowledge`.

##### ext.slash
- Component commands now support response modifier parameters as well.
- Interaction commands are now all acknowledged asynchronously.
- Add `ResponseModifier.wait_for_acknowledgement`.

#### Bug Fixes
- Opus not loading on windows. (FoxeiZ)

## 1.1.132 *\[2022-01-15\]*

#### Improvements

- Add `ERROR_CODES.community_and_rules_channel_cannot_be_changed_to_announcement`.
- Add `seconds_to_id_difference`.
- Add `InteractionEvent.is_expired`.
- Add `timedelta_to_id_difference`.
- Add `id_difference_to_timedelta`.

##### ext.slash
- `show_for_invoking_user_only` parameter of `SlasherApplicationCommand.__new__` is now keyword only and is not routed
    anymore.
- Add `allowed_mentions` parameter to `SlasherApplicationCommand.__new__`.

#### Bug Fixes

- `EmbedBase.__bool__` could return incorrect value.
- `EmbedBase.__len__` could return incorrect value.
- `EmbedBase.contents` excluded `.provider.name`
- `Embed.copy_with` assigned `type` field with different name.

## 1.1.131 *\[2022-01-04\]*

#### Improvements

- Add `banner` parameter to `Client.channel_edit`.
- Add `banner` parameter to `client.channel_create`.
- Add `banner` parameter to `cr_pg_channel_object`.

#### Bug Fixes

##### ext.slash
- `InteractionResponse` could not `yield` back a `Message` if expected.

## 1.1.130 *\[2022-01-02\]*

#### Improvements

- Add `GuildPreview.stickers`.
- Add `ApplicationCommandPermissionOverwriteTargetType.channel`.
- `Emoji.__new__`'s second parameter modified from `Guild` to `int`.

#### Bug Fixes

- Fix a logic error in `Client.role_edit` when editing `icon`.
- Fix an `AttributeError` in `ApplicationCommandPermission.__repr__`.
- Fix a `TypeError` in `Stage._difference_update_attributes`.
- `UserBase.avatar_url_for` was a property (instead of method).

##### ext.top_gg
- `TopGGGloballyRateLimited` accepted +1 parameters causing `TypeError`-s
    (luckily this exception was never dropped).

##### ext.slash
- Bad method was called for an acknowledged component interaction commands.
- Tried to acknowledge an application command interaction event when already acknowledged and a file was being sent.

## 1.1.129 *\[2021-12-24\]*

#### Improvements

- Add `bind`. (Forest#2913)
- Add `ERROR_CODES.invalid_json`.
- Add `format_loop_time`.
- Add `ApplicationFlag.embedded_released`.
- Add `ApplicationFlag.embedded_first_party`.
- Add `ApplicationCommandOptionType.attachment`.
- Add `creator` change key converter for audit logs.
- Add `entity_id` change key converter for audit logs.
- Add `entity_metadata` change key converter for audit logs.
- Add `end` change key converter for audit logs.
- Add `start` change key converter for audit logs.
- Add `GuildJoinRequestStatus`.
- Add missing `EventBase.__eq__`.
- Add missing `EventBase.__hash__`.
- Add missing `ReactionAddEvent.__eq__`.
- Add missing `ReactionAddEvent.__hash__`.
- Add missing `ReactionAddEvent.__eq__`.
- Add missing `ReactionAddEvent.__hash__`.
- Add missing `ReactionDeleteEvent.__eq__`.
- Add missing `ReactionDeleteEvent.__hash__`.
- Add missing `GuildUserChunkEvent.__eq__`.
- Add missing `GuildUserChunkEvent.__hash__`.
- Add missing `VoiceServerUpdateEvent.__eq__`.
- Add missing `VoiceServerUpdateEvent.__hash__`.
- `ScheduledEventUnsubscribeEvent` is now subclass of `ScheduledEventSubscribeEvent`.
- Add missing `ScheduledEventUnsubscribeEvent.__eq__`.
- Add missing `ScheduledEventUnsubscribeEvent.__hash__`.
- Add missing `ScheduledEventSubscribeEvent.__eq__`.
- Add missing `ScheduledEventSubscribeEvent.__hash__`.
- Add `GuildJoinRequest`.
- Add `GuildJoinRequestStatus`.
- Add `GuildRequestFormResponse`.
- Add `GuildFeature.role_subscription_purchasable`.
- Add `GuildFeature.text_in_voice_enabled`.
- Add `GuildFeature.has_directory_entry`.
- Add `GuildFeature.linked_to_hub`.
- Add `MessageFlag.failed_to_mention_some_roles_in_thread`.
- Add `VerificationScreenStepType.text input`.
- Add `VerificationScreenStepType.paragraph`.
- Add `VerificationScreenStepType.multiple_choices`.
- Add `VerificationScreenStepType.verification`.
- Add `VerificationFieldPlatform` (name might change later).
- Add `GuildJoinRequestDeleteEvent`.
- Add `Client.events.guild_join_request_create`.
- Add `Client.events.guild_join_request_delete`.
- Add `Client.events.guild_join_request_update`.
- Add `Guild._embedded_activity_states`.
- Add `EmbeddedActivityState`.
- Add `EMBEDDED_ACTIVITY_STATES`.
- Add `Client.events.embedded_activity_create`.
- Add `Client.events.embedded_activity_delete`.
- Add `Client.events.embedded_activity_update`.
- Add `Client.events.embedded_activity_user_add`.
- Add `Client.events.embedded_activity_user_delete`.
- Add `ApplicationCommandInteraction.resolved_attachments`.
- Move message history to it's own class to reduce the cost of channel, with no messages.
- `ChannelVoice` now supports receiving messages.
- `ChannelStage` now supports receiving messages.
- Add `InteractionEvent.locale`.
- Add `InteractionEvent.guild_locale`.
- Add `Client.events.unknown_dispatch_event`.
- `user_avatar_url_for` now accepts `guild` as `int`.
- `user_avatar_url_for_as` now accepts `guild` as `int`.
- `user_avatar_url_at` now accepts `guild` as `int`.
- `user_avatar_url_at_as` now accepts `guild` as `int`.

##### ext.asyncio
- Add attachment converter to slash commands.

#### Bug Fixes

- Another `KeyError` in `DiscordGateway._received_message` when using fosscord. (Forest#2913)
- `ReactionDeleteEvent` had duped slots.
- Fix an `AttributeError` in `GuildUserChunkEvent.__new__` when user caching is disabled (you don not get the event,
    at that case anyways).

#### Renames, Deprecation & Removals
- Deprecate `Client.events.guild_join_reject` in favor of `.guild_join_request_delete`.

## 1.1.128 *\[2021-12-15\]*

### Scheduled event checklist:

- `guild_object.guild_scheduled_events` \[x\] 1.1.128
- `guild_scheduled_event_object` \[x\]
- `guild_scheduled_event_object.id` \[x\]
- `guild_scheduled_event_object.guild_id` \[x\]
- `guild_scheduled_event_object.channel_id` \[x\]
- `guild_scheduled_event_object.creator_id` \[x\] (check `.creator`)
- `guild_scheduled_event_object.name` \[x\]
- `guild_scheduled_event_object.description` \[x\]
- `guild_scheduled_event_object.scheduled_start_time` \[x\]
- `guild_scheduled_event_object.scheduled_end_time` \[x\]
- `guild_scheduled_event_object.privacy_level` \[x\]
- `guild_scheduled_event_object.privacy_level.GUILD_ONLY` \[x\]
- `guild_scheduled_event_object.status` \[x\]
- `guild_scheduled_event_object.status.SCHEDULED` \[x\]
- `guild_scheduled_event_object.status.ACTIVE` \[x\]
- `guild_scheduled_event_object.status.COMPLETED` \[x\]
- `guild_scheduled_event_object.status.CANCELED` \[x\]
- `guild_scheduled_event_object.entity_type` \[x\]
- `guild_scheduled_event_object.entity_type.STAGE_INSTANCE` \[x\]
- `guild_scheduled_event_object.entity_type.VOICE` \[x\]
- `guild_scheduled_event_object.entity_type.EXTERNAL` \[x\]
- `guild_scheduled_event_object.entity_id` \[x\]
- `guild_scheduled_event_object.entity_metadata` \[x\]
- `guild_scheduled_event_object.entity_metadata.location` \[x\]
- `guild_scheduled_event_object.creator` \[x\] 1.1.128
- `guild_scheduled_event_object.user_count` \[x\]
- `GET /guilds/{guild_id}/scheduled-events` \[x\]
    - `with_user_count` \[x\]
- `POST /guilds/{guild_id}/scheduled-events` \[x\]
    - `channel_id` \[x\]
    - `entity_metadata` \[x\]
    - `name` \[x\]
    - `privacy_level` \[x\]
    - `scheduled_start_time` \[x\]
    - `scheduled_end_time` \[x\]
    - `description` \[x\]
    - `entity_type` \[x\]
    - `reason` \[x\] 1.1.128
- `DELETE /guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}` \[x\]
- `GET /guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}` \[x\]
    - `with_user_count` \[x\]
- `PATCH /guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}` \[x\]
    - `channel_id` \[x\] 1.1.128
    - `entity_metadata` \[x\] 1.1.128
    - `name` \[x\]
    - `privacy_level` \[x\] 1.1.128
    - `scheduled_start_time` \[x\]
    - `scheduled_end_time` \[x\]
    - `description` \[x\]
    - `entity_type` \[x\] 1.1.128
    - `status` \[x\] 1.1.128
    - `reason` \[x\] 1.1.128
- `GET /guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}/users` \[x\] 1.1.128
    - `with_member` \[x\] 1.1.128
    - `before` \[x\] 1.1.128
    - `after` \[x\] 1.1.128
    - `limit` \[x\] 1.1.128
- `GUILD_SCHEDULED_EVENTS (1 << 16)` \[x\] 1.1.128
    - `GUILD_SCHEDULED_EVENT_CREATE` \[x\]
    - `GUILD_SCHEDULED_EVENT_UPDATE` \[x\]
    - `GUILD_SCHEDULED_EVENT_DELETE` \[x\]
    - `GUILD_SCHEDULED_EVENT_USER_ADD` \[x\]
    - `GUILD_SCHEDULED_EVENT_USER_REMOVE` \[x\]

#### Improvements

- Add `ERROR_CODES.invalid_guild`.
- Add `ERROR_CODES.rate_limit_server_send`.
- Add `ERROR_CODES.rate_limit_daily_application_command_creation`.
- Add `FormSubmitInteraction.iter_matches_and_values`.
- Add `ComponentTextInput.required`.
- Add `ComponentTextInput.value`.
- Add `Guild.scheduled_events`.
- Add `ScheduledEvent.creator_id`.
- Add `ScheduledEvent.creator`.
- Add `scheduled_event_edit` parameter to `Client.scheduled_event_edit`.
- Add `stage` parameter to `Client.scheduled_event_edit`.
- Add `voice` parameter to `Client.scheduled_event_edit`.
- Add `location` parameter to `Client.scheduled_event_edit`.
- Add `status` parameter to `Client.scheduled_event_edit`.
- Update `scheduled_event_get_all_guild` endpoint.
- Update `scheduled_event_create` endpoint.
- `ScheduledEvent` instances now support weakreferencing.
- Update `scheduled_event_get` endpoint.
- Update `scheduled_event_edit` endpoint.
- Update `scheduled_event_delete` endpoint.
- Add `reason` parameter to `Client.scheduled_event_edit`.
- Add `reason` parameter to `Client.scheduled_event_create`.
- Add `RATELIMIT_GROUPS.scheduled_event_user_get_chunk`
- Add `DiscordHTTPClient.scheduled_event_user_get_chunk`.
- Add `Client.scheduled_event_user_get_chunk`.
- Add `Client.scheduled_event_user_get_all`.
- Add `IntentFlag.guild_scheduled_events`.
- Add missing `ScheduledEventEntityMetadata.__eq__`.
- Add missing `StageEntityMetadata.__eq__`.
- Add missing `LocationEntityMetadata.__eq__`.

#### Bug Fixes

- `KeyError` in `DiscordGateway._received_message` when using fosscord. (Forest#2913)
- `KeyError` in `Client.client_gateway_reshard` when using fosscord. (Forest#2913)
- `AttributeError` in `ScheduledEvent.__new__`.
- `NameError` in `Client.thread_user_get`.

## 1.1.127 *\[2021-12-07\]*

#### Improvements

- Add `DiscordHTTPClient.sticker_pack_get`.
- Add `RATE_LIMIT_GROUPS.sticker_pack_get`.
- Add `Client.sticker_pack_get`.
- Add `ApplicationCommandTargetType.channel`.
- Add `INTERACTION_RESPONSE_TYPES.form`.
- Add `Client.interaction_form_send`.
- Add `InteractionForm.title`.

## 1.1.126 *\[2021-12-05\]*

#### Improvements

- Add missing `EventHandlerManager.__dir__`.
- Add missing `_EventHandlerManager.__dir__`.
- Add missing `ComponentDynamic.__dir__`.

##### ext.slash
- Add missing `ComponentDescriptorState.__dir__`.

### Bug fixes

##### ext.asyncio
- A removed value was imported.

## 1.1.125 *\[2021-12-05\]*

### Bug fixes

- Connecting to voice failed (new typo).
- `VoiceState.__new__` was not setting an attribute correctly.

## 1.1.124 *\[2021-12-05\]*

### Summary

Hata's backend has been moved to it's [repo](https://github.com/HuyaneMatsu/scarletio); This was a common request
around the board.

#### Improvements

- Add `ChannelForum`.
- Add `CHANNEL_TYPES.GROUP_CAN_CONTAIN_THREADS`.
- `DiscordEntity`-s now drop rich `AttributeError`. Soon coming for other types as well.

##### ext.asyncio
- `Task` instances returned by `current_task()` now support dynamic attributes (They are not tasks anymore.)
    (winwinwinwin#0001)

### Bug fixes

##### ext.asyncio
- `gather` could never finish. (winwinwinwin#0001)

## 1.1.123 *\[2021-11-28\]*

#### Improvements

##### ext.asyncio
- `create_server` now expects and handles `start_serving` parameter. (Forest#2913)
- `create_unix_server` now expects and handles `start_serving` parameter. (Forest#2913)
- Add `.subprocess.PIPE`. (winwinwinwin#0001)
- Add `.subprocess.DEVNULL`. (winwinwinwin#0001)
- Add `.subprocess.STDOUT`. (winwinwinwin#0001)
- `ReadProtocolBase` now implements `readexactly`. (winwinwinwin#0001)

### Bug fixes

- `EventThread.create_server` could raise `TypeError` (typo). (Forest#2913)

## 1.1.122 *\[2021-11-28\]*

#### Improvements

- Add `FormSubmitInteraction.get_custom_id_value_relation`.
- Add `FormSubmitInteraction.get_value_for`.
- Add `FormSubmitInteraction.get_match_and_value`.
- Add `FormSubmitInteraction.iter_custom_ids_and_values`.
- Add `FormSubmitInteractionOption.iter_custom_ids_and_values`.

##### ext.asyncio
- Implement `Semaphore`. (winwinwinwin#0001)
- Implement `BoundedSemaphore`. (winwinwinwin#0001)

## 1.1.121 *\[2021-11-28\]*

#### Improvements

- Add `ERROR_CODES.cannot_update_finished_scheduled_event`.
- Add `ERROR_CODES.failed_to_create_stage_needed_for_scheduled_event`.
- Add `banner` parameter to `ChannelText.precreate`.
- Add `ChannelText.banner`.
- Add `ApplicationInstallParameters`.
- Add `Application.custom_install_url`.
- Add `Application.install_parameters`.
- Add `Application.tags`.
- Add `TextInputStyle`.
- Add `InteractionType.form_submit`.
- Add `ComponentType.text_input`.
- Add `ComponentTextInput`.
- Rename `coro` to `coroutine` and `fut` to `future` everywhere. This might break some code.
- Add missing `ComponentSelectOption.__eq__`.
- Add `Permission.moderate_members`.
- Add `AuditLogIterator.scheduled_events`.
- Add `AuditLog.scheduled_events`.
- Add missing `ComponentBase.__new__`.
- Add `InteractionForm`.
- Add `FormSubmitInteraction`.
- Add missing `ApplicationCommandInteraction.__hash__`.
- Add missing `ApplicationCommandInteraction.__eq__`.
- Add missing `ApplicationCommandInteractionOption.__hash__`.
- Add missing `ApplicationCommandInteractionOption.__eq__`.
- Add missing `ApplicationCommandAutocompleteInteractionOption.__hash__`.
- Add missing `ApplicationCommandAutocompleteInteractionOption.__eq__`.
- `ApplicationCommandAutocompleteInteraction` not inherits anymore from `DiscordEntity`.
- Add missing `ApplicationCommandAutocompleteInteraction.__hash__`
- Add missing `ApplicationCommandAutocompleteInteraction.__eq__`
- Add `CHANNEL_TYPES.guild_forum`.
- Add `AsyncQueue.set_result_wait`.
- Add images to `slash.md`.

##### ext.extension_loader
- Syntax is checked before executing a module when reloading.
- Add `Extension.file_name`.

##### ext.top_gg
- Added to `setup.py`.

##### ext.asyncio
- Add `start_unix_server`. (Forest#2913)
- Add `Queue.put`. (Forest#2913)

#### Bug Fixes
- `Client.multi_client_message_delete_sequence` was not calling `Message.is_deletable` when getting messages from
cache.
- Fix bad logic in `EventThread.create_server`. (Forest#2913)

##### ext.slash
- `abort` was not defining `show_for_invoking_user_only` by default. (When was this bug made?)

#### Renames, Deprecation & Removals

- Rename `ComponentInteraction.component_type` to `.type`.
- Deprecate `ComponentInteraction.component_type`.

##### ext.slash
- Rename `Slasher.regex_custom_id_to_component_command` to `._regex_custom_id_to_component_command`.
- Rename `Slasher.string_custom_id_to_component_command` to `._string_custom_id_to_component_command`.
- Deprecate `Slasher.regex_custom_id_to_component_command`.
- Deprecate `Slasher.string_custom_id_to_component_command`.

## 1.1.120 *\[2021-11-17\]*

#### Improvements

- Add `GuildFeature.internal_employee_only`.
- Add `GuildFeature.channel_banners`.
- Add `Guild.boost_progress_bar_enabled`.
- Add `boost_progress_bar_enabled` change key converter for audit logs.
- Add `boost_progress_bar_enabled` parameter to `Guild.precreate`.
- Add `boost_progress_bar_enabled` parameter to `Client.guild_edit`.
- Add `boost_progress_bar_enabled` parameter to `Client.guild_create`.
- Add `DiscordException.sent_data`.
- Add `DiscordException.received_data`.
- Add `ERROR_CODES.exactly_one_guild_id_parameter_is_required`.
- Add `channel_banner_url` for future reference.
- Add `channel_banner_url_as` for future reference.
- Add `GuildProfile.timed_out_until`.
- Add `repeat_timeout.
- Rename `GUILD_SCHEDULED_EVENT_USER_CREATE` to `GUILD_SCHEDULED_EVENT_USER_ADD`.
- Rename `GUILD_SCHEDULED_EVENT_USER_DELETE` to `GUILD_SCHEDULED_EVENT_USER_REMOVE`.
- Add `ScheduledEventSubscribeEvent`.
- Add `ScheduledEventUnsubscribeEvent`.
- `Client.events.scheduled_event_user_subscribe` now accepts 2 parameters.
- `Client.events.scheduled_event_user_unsubscribe` now accepts 2 parameters.
- Add `timed_out_until` parameter to `Client.client_guild_profile_edit`.
- Add `timed_out_until` parameter to `Client.user_guild_profile_edit`.
- Add `timed_out_until` change key converter for audit logs.
- Add `HATA_LIBRARY_URL` environmental variable.
- Newly added `launch` event handlers will be ensured instantly if launch was already called.

##### ext.slash
- Add `ComponentCommand.name`.
- Add `name` parameter to `ComponentCommand.__new__`.
- `_render_application_command_exception` now uses `repr(command)`.

#### Bug Fixes

##### ext.slash
- `ComponentCommand.__new__` could raise exception with bad error message.
- `SlasherApplicationCommand.__new__` could pass `None` to `raw_name_to_display` dropping `TypeError` if routing.

#### Renames, Deprecation & Removals

- Deprecate `DiscordException.data`, use `.received_data` instead.
- Rename `DiscordException._cr_code` to `._get_code`.
- Rename `DiscordException._cr_messages` to `._create_messages`.

## 1.1.119 *\[2021-11-09\]*

#### Improvements

- Add `UserBase.to_data`.
- Add `MessageActivity.to_data`.
- Add `MessageApplication.to_data`.
- Add `Attachment.to_data`.
- Add `MessageInteraction.to_data`.
- Add `reaction_mapping.to_data`.
- Add `MessageReference.to_data`.
- Add `Message.to_message_reference_data`.
- Add `Sticker.to_partial_data`.
- Add `Message.to_data`.
- Add `ChannelBase.to_data`.
- Add `ChannelPrivate.to_data`.
- Add `ChannelGroup.to_data`.
- Add `ChannelGuildBase.to_data`.
- Add `ChannelGuildBase.to_data`.
- Add `ChannelCategory.to_data`.
- Add `ChannelDirectory.to_data`.
- Add `ChannelStore.to_data`.
- Add `ChannelText.to_data`.
- Add `ChannelGuildUndefined.to_data`.
- Add `ChannelVoiceBase.to_data`.
- Add `ChannelVoice.to_data`.
- Add `ChannelStage.to_data`.
- Add `ChannelThread.to_data`.

#### Bug Fixes

- `log_time_converter` could return value of incorrect type. (Al_Loiz \[ICU\]#5392) (from 1.1.117)

## 1.1.118 *\[2021-11-05\]*

#### Bug Fixes

- An another `TypeError` in `Role._delete`.

## 1.1.117 *\[2021-11-05\]*

### Summary

Update file uploading system.

#### Improvements

- Add `ApplicationCommandAutocompleteInteraction.get_value_of`.
- Add `ApplicationCommandAutocompleteInteractionOption.get_value_of`.
- Add `EventHandlerManager.iter_event_names_and_handlers`.
- Add `Attachment.description`.
- Support API version 10. (coming soon to Discord)

##### ext.extension_loader
- Plugins are supported.

#### Bug Fixes
- `Client._request_members` raised `TypeError`.
- `Client.role_edit` raised `TypeError`. (Forest#2913)
- `Client.role_delete` raised `TypeError`. (Forest#2913)
- `time_to_id` was used even if deprecated +typod deprecation message. (Al_Loiz \[ICU\]#5392)

## 1.1.116 *\[2021-11-01\]*

#### Improvements

- Add `ApplicationFlag.gateway_message_content`.
- Add `ApplicationFlag.gateway_message_content_limited`.
- Add `DiscordHTTPClient.thread_user_get`.
- Add `RATELIMIT_GROUPS.thread_user_get`.
- Add `Client.thread_user_get`.
- `Emoji.__format__` now returns `.as_emoji` if `code` is given as `''`.
- Add `wait_for_interruption`.

#### Bug Fixes

- `UserBase.avatar_url_at` was incorrectly set as property.
- Threads on unarchiving were not put to cache.

##### ext.slash
- Operations before and after parentheses start were not converted to their prefix versions even if applicable.
- Full division operation was used when executing remainder. (Gilgamesh#8939)
- `InteractionResponse` was not passing `show_for_invoking_user_only` correctly, causing `abort` to misbehave.
    (from 1.1.103)
- Multi parameter autocomplete in direct slash commands failed. (Al_Loiz \[ICU\]#5392)

## 1.1.115 *\[2021-10-24\]*

#### Bug Fixes

- Remove a random print call.

## 1.1.114 *\[2021-10-24\]*

#### Bug Fixes

- Fix an `AttributeError` in `default_voice_client_join_event_handler`.
- Fix an `AttributeError` in `default_voice_client_move_event_handler`.

## 1.1.113 *\[2021-10-23\]*

#### Improvements

- Add `SystemChannelFlag.join_sticker_replies`

##### ext.commands_v2
- Add `release_at` check decorator and `CheckReleaseAt` check class. (Gilgamesh#8939)

#### Bug Fixes

- Fix a `TypeError` in `parse_cookie_date`. (Gilgamesh#8939)

##### ext.slash
- `SlasherApplicationCommandParameterAutoCompleter` has no exception handlers implemented.
- `SlasherApplicationCommand.create_event` returned incorrect value.
- `SlasherApplicationCommandCategory.create_event` returned incorrect value.
- Fix a `TypeError` in `SlasherApplicationCommandCategory.as_option`.
- A bad logic could cause auto completion not be called inside of sub commands.

## 1.1.112 *\[2021-10-19\]*

#### Improvements

- Add `UserFlag.spammer`.
- Add `ApplicationCommandOption.min_value`.
- Add `ApplicationCommandOption.max_value`.
- Add `min_value` parameter to `ApplicationCommandOption`.
- Add `max_value` parameter to `ApplicationCommandOption`.

##### ext.slash
- Add `min_value` parameter to `SlasherApplicationCommandParameterConfigurerWrapper`.
- Add `max_value` parameter to `SlasherApplicationCommandParameterConfigurerWrapper`.
- Add `SlashParameter` type.

### Bug fixes

- `Embed.__bool__` could return incorrect value.

## 1.1.111 *\[2021-10-17\]*

### Summary

Make `client.events` pluginable.

#### Improvements

- Add `GuildFeature.animated_banner`.
- Add `EventHandlerManager.register_plugin`.
- Do parameter count checks inside of `EventHandlerManager.__setattr__` as well.
- Add `EventHandlerPlugin` and other respective classes.
- `VoiceClient.channel` is now a property.
- `VoiceClient.guild` is now a property.
- Add `VoiceClient.channel_id` is now a property.
- Add `VoiceClient.guild_id` is now a property.
- Get `user_id` from token when creating a client.

##### ext.commands_v2
- Add `CommandContext.channel_id`.
- Add `CommandContext.guild_id`.

#### Bug Fixes

- Multiple `Client` methods could raise `AttributeError` by calling a bad method. (Gilgamesh#8939)

## 1.1.110 *\[2021-10-10\]*

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
- Add `DiscordHTTPClient.scheduled_event_create`.
- Add `DiscordHTTPClient.scheduled_event_edit`.
- Add `DiscordHTTPClient.scheduled_event_delete`.
- Add `DiscordHTTPClient.scheduled_event_get`.
- Add `DiscordHTTPClient.scheduled_event_get_all_guild`.
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

##### ext.slash
- Auto completers now can be registered to command groups and to `Slasher` as well.
- Auto completers with multiple parameter names can be registered with 1 call.
- Add `.error` decorator for slasher application commands, to auto completers and to component commands.

#### Renames, Deprecation & Removals

- Rename `ScheduledEvent.scheduled_start` to `.start`.
- Rename `ScheduledEvent.scheduled_end` to `.end`.

## 1.1.108 *\[2021-10-01\]*

### Summary

Add unicode emoji support for roles.

#### Improvements

##### ext.slash
- Add `first` parameter to `Slasher.error`.
- Add `create_unicode_emoji`.
- Add `Role.unicode_emoji`.
- Add `unicode_emoji` parameter to `Role.precreate`.
- Add `unicode_emoji` change key converter for audit logs.
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
- `Client.client_login_static` could return string (instead of dict) when using custom host. (Forest#2913)
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

- Fix a `NameError` in `Client.application_command_permission_edit`. (Gilgamesh#8939)
- Fix a possible `AttributeError` in `Client.custom`. (Gilgamesh#8939)
- `Message.custom` was not setting `.guild_id` accordingly. (Gilgamesh#8939)
- Fix an `AttributeError` in `convert_thread_created`. (Gilgamesh#8939)
- `Message.custom` was not marking the message as partial accordingly.
- Fix a `NameError` in `Client.message_delete_sequence`. (Gilgamesh#8939)

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
- Add `CHANNEL_TYPES.GROUP_GUILD_MAIN_TEXT`.
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
- Add `Message.has_channel_mentions`.
- Add `Message.has_type`.
- Add `Message._create_empty`.
- Add `Message._clear_cache`.
- Add `message.is_deletable`.
- Add `Message.precreate`.
- Add `preconvert_snowflake_array`.

##### ext.command_utils
- `ChannelOutputStream.flush` now forces newly written content to new message. (Gilgamesh#8939)

#### Bug Fixes
- `unix_time_to_datetime` raised `ValueError` if received value out of the expected range. (Tari#0002)

##### ext.command_utils
- `ChannelOutputStream` made chunks of bad size. (Gilgamesh#8939)

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
- Add `ApplicationCommandInteraction.resolve_entity`.
- Add `ApplicationCommandInteraction.target`.
- `ApplicationCommandInteraction.options` is now `tuple`, `None` (from `list`, `None`)
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
- `Guild.public_updates_channel` is now a property.
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
- `WebhookBase.channel` is now a property.
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
- Add `DiscordHTTPClient.guild_thread_get_all_active`.
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
- Remove `PermissionOverwrite.target_role`.
- Remove `PermissionOverwrite.target_user_id`.
- Rename `.overwrites` to `.permission_overwrites`.
- Rename `._invalidate_perm_cache` to `._invalidate_permission_cache`
- Rename `._cache_perm` to `._permission_cache`.
- Rename `overwrites` parameter of `cr_pg_channel_object` to `permission_overwrites`.
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
- Rename `DiscordHTTPClient.thread_get_chunk_active` to `.channel_thread_get_chunk_active`.
- Rename `request_thread_channels` to `request_channel_thread_channels`.
- Deprecate `Client.thread_get_all_archived_private`.
- Rename `Client.thread_get_all_archived_private` to `.channel_thread_get_all_archived_private`.
- Rename `DiscordHTTPClient.thread_get_chunk_archived_private` to `.channel_thread_get_chunk_archived_private`.
- Rename `RATE_LIMIT_GROUPS.thread_get_chunk_archived_private` to `.channel_thread_get_chunk_archived_private`.
- Deprecate `Client.thread_get_all_archived_public`.
- Rename `Client.thread_get_all_archived_public` to `.channel_thread_get_all_archived_public`.
- Rename `DiscordHTTPClient.thread_get_chunk_archived_public` to `.channel_thread_get_chunk_archived_public`.
- Rename `RATE_LIMIT_GROUPS.thread_get_chunk_archived_public` to `.channel_thread_get_chunk_archived_public`.
- Deprecate `Client.thread_get_all_self_archived`.
- Rename `Client.thread_get_all_self_archived` to `.channel_thread_get_all_self_archived`.
- Rename `DiscordHTTPClient.thread_get_chunk_self_archived` to `.channel_thread_get_chunk_self_archived`.
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
- Add `privacy_level` change key converter for audit logs.
- Add `ScheduledEventStatus`.
- Add `status` change key converter for audit logs.
- Add `ScheduledEventEntityType`.
- Add `entity_type` change key converter for audit logs.
- Add `sku_ids` change key converter for audit logs.
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
- Fix a `TypeError` in `EventThread.create_unix_connection`.
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
- Add `auto_archive_after` change key converter for audit logs.
- Add `default_auto_archive_after` change key converter for audit logs.
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

- Remove `ActivityBase.created`.
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
- Add `banner_color` parameter to `User.precreate`.
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
- Fix a `TypeError` in `SlashCommand._get_sync_permission_ids`.
- Fix an `AttributeError` in `Slasher._register_command`.

#### Renames, Deprecation & Removals

- Rename `GuildFeature.vanity` to `.vanity_invite`.
- Deprecate `GuildFeature.vanity`.
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
- `'hata.discord.embed'` was not listed in `setup.py`. (Gilgamesh#8939)
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
- Fix a conversion error in `Client.thread_create`. (Gilgamesh#8939)

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

- Add `typer.__await__`. (Gilgamesh#8939)
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
- `Sticker.tags` use `frozenset` + `None` (from `list` + `None`).
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
- Include date, method and url in `DiscordException` error message.

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
- `InteractionResponse` now will always yield back a `Message` instance.

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
- Rename `SlashResponse` to `InteractionResponse`.
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
- `ExtensionLoader.load_extension`, `.load`, `.unload`, `.reload` now accepts iterable and directories as well.

##### ext.slash

- Commands were not getting their display name as their description by default (but their raw name).
- Routing slash commands dropped `TypeError`.

#### Bug Fixes

- Fix an `AttributeError` in `ChannelGroup._from_partial_data`.
- `ChannelThread` has no attribute `thread_users`.
- Fix a `NameError` in `_debug_component_custom_id`. (Gilgamesh#8939)
- Fix a `TypeError` in `Client.message_edit`. (Gilgamesh#8939)

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
- Convert nested component list to row. (Gilgamesh#8939)

#### Bug Fixes

- Fix a `NameError` in `Client.webhook_message_create`.

##### ext.slash
- `InteractionResponse` with `force_new_message = True` was not handling `show_for_invoking_user_only` correctly.
- When passing `allowed_mentions`, `tts` to `abort`, do not set `show_for_invoking_user_only=False` if not given.

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

- When removing all the options of an application command, they was not edited accordingly. (Gilgamesh#8939)
- `create_partial_guild` could drop `NameError`.
- Fix `KeyError` in `create_component`.
- `Client.interaction_response_message_create` ignored `show_for_invoking_user_only` if other fields were not present.

##### ext.slash
- `name` could have higher priority when setting slash command description than `description` itself.
    (Gilgamesh#8939)

## 1.1.78 *\[2021-05-18\]*

#### Summary

Fix some bugs and improve slash command creation.

#### Improvements

- Add `interaction` parameter to `message.custom`. (Gilgamesh#8939)
- Increase `content`'s max length to 4k in `message.custom`.
- Add `components` parameter to `message.custom`. (Gilgamesh#8939)
- Add `thread` parameter to `message.custom`. (Gilgamesh#8939)
- Add `InteractionEvent.is_responding`.
- Add `InteractionEvent.is_acknowledging`.
- `InteractionEvent.wait_for_response_message` now raises `RuntimeError` if ephemeral message was sent.
- Add `Interaction.is_unanswered`.
- Add `UserFlag.certified_moderator`.

##### ext.slash
- `abort` now supports `components` parameter in `show_for_invoking_user_only` mode. (Gilgamesh#8939)
- Slash command description defaults to it's name instead of raising an exception. (Gilgamesh#8939)
- Slash choices now can be any iterable object. (Gilgamesh#8939)
- `client` and `interaction_event` parameters are now optional for slash commands.
- `get_request_coroutines` now converts unhandled objects into `str` instances and propagates them to be sent.
    (Gilgamesh#8939)

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
- Fix an `AttributeError` in `Guild._delete`. (Gilgamesh#8939)

#### Renames, Deprecation & Removals

- Rename `InteractionEvent._response_state` to `._response_flag`.

## 1.1.77 *\[2021-05-17\]*

#### Summary

Start supporting anyio (all bugs included). (Forest#2913)

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
    (Forest#2913)

#### Improvements

- Add `ERROR_CODES.max_ban_fetches`.
- Add `DiscordHTTPClient.thread_create_public`.
- Add `RATE_LIMIT_GROUPS.thread_create_public`.
- Add `Client.thread_create`.
- Add `WebhookType.application`.
- Add `Message.attachment`. (Forest#2913)

#### Bug fixed

- Fix a typo on `ComponentSelect.to_data`. (Gilgamesh#8939)
- Threads were badly bound and unbound from a guild.

##### ext.extension_loader
- Directory loading failed (typo).

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
    (Gilgamesh#8939)
- Add `mentionable_id` parameter support for slash commands.
- Add `configure_parameter` to overwrite slash command annotations.

#### Bug fixed

- Fix a `NameError` in `MessageType._from_value`.
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
- `ChannelPrivate.guild` and `ChannelGroup.guild` is now a property of `ChannelBase`.
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
- Add `ERROR_CODES.unknown_store_directory_layout`.
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
- Improve `Guild.get_emoji_like` matching. (Gilgamesh#8939)

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
- Fix an `AttributeError` from `1.1.72`. (Gilgamesh#8939)
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
- Add `get_channel_stdin`. (experimental) (Forest#2913)
- Add `get_channel_stdout`. (experimental) (Forest#2913)

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
- Add `client.extensions`. (Forest#2913) (ᓚᘏᗢ | NeKo Mancer#1477)
- Add `EXTENSION_LOADER.get_extension`.

#### Improvements

##### ext.slash
- `Button.default_style` should be `ButtonStyle.violet`. (Gilgamesh#8939)

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
- Add `iter_component_interactions`. (ToxicKidz#6969) (Gilgamesh#8939)
- Add `Slasher.add_component_interaction_waiter`.
- Add `Slasher.remove_component_interaction_waiter`.

#### Improvements

- Add `application_id` keyword to `Message.custom`.
- Add `COMPONENT_LABEL_LENGTH_MAX`. (Gilgamesh#8939)
- Add `COMPONENT_CUSTOM_ID_LENGTH_MAX`. (Gilgamesh#8939)
- `Component.style` defaults to `None`.
- Extend `Component.__repr__`.

#### Bug Fixes

- Fix a `TypeError` in `Component.__repr__`. (Gilgamesh#8939)
- `Message.custom` was not checking `type_` parameter.
- `is_coroutine_function` returned non-bool. (ToxicKidz#6969)
- `is_coroutine_generator_function` returned non-bool. 
- Handle python3.10 things correctly. (Gilgamesh#8939)
- Add a missing return to `ext.async.asyncio.LifoQueue`. (ᓚᘏᗢ | NeKo Mancer#1477)

#### Renames, Deprecation & Removals

- Rename `Component.__init__` to `.from_data`.


## 1.1.69  *\[2021-04-24\]*

#### Summary

Add components.

#### New Features

- Add `InteractionType.message_component`.
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

- Add `components` parameter to `Client.message_create`.
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
- Add `PaginationBase.is_active`. (Gilgamesh#8939)
- Add `UserMenuFactory`, `UserMenuRunner`, `UserPagination`. (Gilgamesh#8939)

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
- `ActivityRich.__new__` was not picking up `url` correctly. (Gilgamesh#8939)
- Fix a typo in `Client.role_edit` causing `AssertionError`. (Gilgamesh#8939)

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
- Rename `Pagination.page` to `.page_index`.

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
- Add `video_quality_mode` change key converter for audit logs.
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

- Mark keyword only parameters as keyword only in docstrings as well. (Gilgamesh#8939)
- `export` & `include`. (sleep-cult#3040)
- `_EventHandlerManager.remove`'s `name` parameter should be optional. (Gilgamesh#8939)

##### ext.slash
- Move slash sync coroutine creation to task creation to avoid resource warning at edge cases.

#### Bug Fixes

##### ext.slash
- `Slasher.__delevent__` with unloading behavior delete was not deleting the commands. (Gilgamesh#8939)


## 1.1.65  *\[2021-04-14\]*

#### Summary

Lazy choice definition.

#### New Features

##### ext.slash
- Add lazy interaction choice definition. (Gilgamesh#8939)

#### Improvements

- Move json conversion to backend.
- Fix some spacing. (sleep-cult#3040)
- `ActivityFlag` now use lower case flag names.
- Create `urls.py` from `http.URLS` module.

#### Bug Fixes

- Fix an `AttributeError` in `User._from_client`. (Gilgamesh#8939)
- Fix typo `MAX_RERP_ELEMENT_LIMIT` -> `MAX_REPR_ELEMENT_LIMIT`.

##### ext.slash
- `CommandState._try_purge_from_changes` returned values in bad order. (Gilgamesh#8939)
- `CommandState._try_purge` returned values in bad order. (Gilgamesh#8939)


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
- `Icon.__repr__` displayed incorrect names. (Gilgamesh#8939)
- Dupe client check was not working. (Gilgamesh#8939)
- Fix reading readme issue on windows. (Gilgamesh#8939)
- Fix a `TypeError` in `User._update_presence`. (from 1.1.63)
- `EventWaitforMeta._call_channel_edit` passed bad args to guild waiters.
- Fix a `NameError` in `EventLoop.create_datagram_endpoint`. (Forest#2913)
- Fix a `NameError` in `cr_pg_channel_object`. (Forest#2913)
- Fix a `NameError` in `Client.request_members`. (Forest#2913)
- Fix a `NameError` in `Client.message_create`. (Forest#2913)
- Fix a `NameError` in `Client.interaction_followup_message_edit`. (Forest#2913)
- Fix a `NameError` in `Client.interaction_followup_message_create`. (Forest#2913)
- Fix a `NameError` in `Client.interaction_response_message_edit`. (Forest#2913)
- Fix a `NameError` in `Client.interaction_response_message_create`. (Forest#2913)
- Fix a `NameError` in `Client.webhook_message_edit`. (Forest#2913)
- Fix a `NameError` in `Client.webhook_message_create`. (Forest#2913)
- Fix a `NameError` in `Client.message_edit`. (Forest#2913)
- Fix a `NameError` in `Client.permission_overwrite_edit`. (Forest#2913)
- Fix a `NameError` in `ApplicationCommandOption.add_option`. (Forest#2913)
- Fix a `TypeError` in `Client.interaction_response_message_edit`. (Forest#2913)
- Fix a `NameError` in `Client.guild_edit`. (Forest#2913)
- Fix a `NameError` in `Client.channel_edit`. (Forest#2913)
- Fix a `NameError` in `Client.guild_user_add`. (Forest#2913)
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
- Slash commands now instant sync if added runtime. (Gilgamesh#8939)

#### Optimizations

- Speed up multi client dispatch event parsers.

#### Improvements

##### ext.slash
- Add sync-time slash command addition and removal detection and handling.
- Move slash extension's parts into different files to improve readability.

#### Renames, Deprecation & Removals

##### ext.slash
- Rework `Slasher.do_main_sync` and rename to `.sync`.
