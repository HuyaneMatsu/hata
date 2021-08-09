__all__ = ()

from .rate_limit import RateLimitGroup, LIMITER_WEBHOOK, LIMITER_CHANNEL, StaticRateLimitGroup, LIMITER_GUILD, \
    LIMITER_INTERACTION

__doc__ = """
Defines the rate limit groups by hata. Hata uses burst half automatic rate limit handler.

Burst rate limit handler means, if (for example) 30 requests can be done to an endpoint before it resets, it will
let 30 requests to pass trough, and with 31th will wait till the limits expires.

Half automatic, since it automatically detects rate limit sizes with it's first request, but it do not detects
which endpoints are limited together and by which id, since they are set by their rate limit group.

It is optimistic, since Discord do not limits every endpoint, but endpoints which will be potentially changed
are marked as optimistic. They have a limiter set, but their limit can be subject of change. The implementation
lets trough 1 more request with each cycle, starting from `1`, till it reaches a set `n` limit. If any of the
requests return rate limit information, then changes the endpoints limitations to it. The increased pararellity
starting by `1` is to ensure, that the endpoint is mapped by first request. The increasing pararellity represents
the decreasing chance of getting any rate limit information back.

Limit Guides
------------
The following shortenings are used inside of group descriptions:
- `N/A` : Not applicable
- `UN` : Unknown
- `OPT` : Optimistic

Limiter types:
- `UNLIMITED`
- `GLOBAL`
- `channel_id`
- `guild_id`
- `webhook_id`

Required auth types:
- `N/A` (No auth required.)
- `UN` (Unknown, not bot.)
- `application`
- `bearer`
- `bot`
- `user`

Content Delivery Network Endpoint
---------------------------------
- Endpoint : `https://cdn.discordapp.com/`
- Method : `GET`
- Required auth : `N/A`
- Limiter : `UNLIMITED`
- Limit : `N/A`
- Resets after : `N/A`


Status Endpoints
----------------
- Endpoint base: `https://status.discord.com/api/v2`
- endpoints:
    - `/incidents/unresolved.json`
    - `/scheduled-maintenances/active.json`
    - `/scheduled-maintenances/upcoming.json`
- Method : `GET`
- Required auth : `N/A`
- Limiter : `UNLIMITED`
- Limit : `N/A`
- Resets after : `N/A`

Shared Groups
-------------
- GROUP_REACTION_MODIFY
    - Used by : `reaction_clear`, `reaction_delete_emoji`, `reaction_delete_own`, `reaction_add`, `reaction_delete`
    - Limiter : `channel_id`
    - Limit : `1`
    - Resets after : `0.25`

- GROUP_PIN_MODIFY
    - Used by : `message_unpin`, `message_pin`
    - Limiter : `channel_id`
    - Limit : `5`
    - Resets after : `4.0`

- GROUP_USER_MODIFY
    - Used by : `user_edit`, `user_move`
    - Limiter : `guild_id`
    - Limit : `10`
    - Resets after : `10.0`

- GROUP_USER_ROLE_MODIFY
    - Used by : `user_role_delete`, `user_role_add`
    - Limiter : `guild_id`
    - Limit : `10`
    - Resets after : `10.0`

- GROUP_WEBHOOK_EXECUTE
    - Used by : `webhook_message_create`, `webhook_message_delete`, `webhook_message_get`, `webhook_message_edit`
    - Limiter : `webhook_id`
    - Limit : `5`
    - Resets after : `2.0`

- GROUP_INTERACTION_EXECUTE
    - Used by: `interaction_followup_message_create`, `interaction_response_message_delete`,
        `interaction_response_message_edit`, `interaction_followup_message_delete`,
        `interaction_response_message_get`, `interaction_followup_message_edit`, `interaction_followup_message_get`
    - Limiter : `interaction_id`
    - Limit : `5`
    - Resets after : `2.0`

- GROUP_PERMISSION_OVERWRITE_MODIFY
    - Used by: `permission_overwrite_delete`, `permission_overwrite_create`
    - Limiter : `channel_id`
    - Limit : `10`
    - Resets after : `15.0`

- GROUP_THREAD_CREATE
    - Used by: `thread_create_from_message`, `thread_create`
    - Limiter : `GLOBAL`
    - Limit : `50`
    - Resets after : `300.0`

- GROUP_THREAD_ACTION
    - Used by: `thread_join`, `thread_leave`, `thread_user_add`, `thread_user_delete`
    - Limiter : `GLOBAL`
    - Limit : `5`
    - Resets after : `5.0`

Group Details
-----------
- oauth2_token
    - Endpoint : `oauth2/token`
    - Method : `POST`
    - Required auth : `application`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`

- application_get
    - Endpoint : `/applications/{application_id}`
    - Method : `GET`
    - Required auth : `UN`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Untested.

- achievement_get_all
    - Endpoint : `/applications/{application_id}/achievements`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `5`
    - Resets after : `5.0`

- achievement_create
    - Endpoint : `/applications/{application_id}/achievements`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `5`
    - Resets after : `5.0`

- achievement_delete
    - Endpoint : `/applications/{application_id}/achievements/{achievement_id}`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `5`
    - Resets after : `5.0`

- achievement_get
    - Endpoint : `/applications/{application_id}/achievements/{achievement_id}`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `5`
    - Resets after : `5.0`

- achievement_edit
    - Endpoint : `/applications/{application_id}/achievements/{achievement_id}`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `5`
    - Resets after : `5.0`

- application_command_global_get_all
    - Endpoint : `/applications/{application_id}/commands`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- application_command_global_create
    - Endpoint : `/applications/{application_id}/commands`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `5`
    - Resets after : `20.0`

- application_command_global_update_multiple
    - Endpoint : `/applications/{application_id}/commands`
    - Method : `PUT`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `2`
    - Resets after : `60.0`

- application_command_global_get
    - Endpoint : `/applications/{application_id}/commands/{application_command_id}`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- application_command_global_delete
    - Endpoint : `/applications/{application_id}/commands/{application_command_id}`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `5`
    - Resets after : `20.0`

- application_command_global_edit
    - Endpoint : `/applications/{application_id}/commands/{application_command_id}`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `5`
    - Resets after : `20.0`

- application_command_guild_get_all
    - Endpoint : `/applications/{application_id}/guilds/{guild_id}/commands`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- application_command_guild_create
    - Endpoint : `/applications/{application_id}/guilds/{guild_id}/commands`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `5`
    - Resets after : `20.0`

- application_command_guild_update_multiple
    - Endpoint : `/applications/{application_id}/guilds/{guild_id}/commands`
    - Method : `PUT`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `2`
    - Resets after : `60.0`

- application_command_permission_get_all_guild
    - Endpoint : `/applications/{application_id}/guilds/{guild_id}/commands/permissions'`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- application_command_guild_get
    - Endpoint : `/applications/{application_id}/guilds/{guild_id}/commands/{application_command_id}`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- application_command_guild_delete
    - Endpoint : `/applications/{application_id}/guilds/{guild_id}/commands/{application_command_id}`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `5`
    - Resets after : `20.0`

- application_command_guild_edit
    - Endpoint : `/applications/{application_id}/guilds/{guild_id}/commands/{application_command_id}`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `5`
    - Resets after : `20.0`

- application_command_permission_get
    - Endpoint : `/applications/{application_id}/guilds/{guild_id}/commands/{application_command_id}/permissions`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- application_command_permission_edit
    - Endpoint : `/applications/{application_id}/guilds/{guild_id}/commands/{application_command_id}/permissions`
    - Method : `PUT`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `5.0`
    - Resets after : `20.0`

- application_get_all_detectable
    - Endpoint : `/applications/detectable`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`

- client_logout
    - Endpoint : `/auth/logout`
    - Method : `POST`
    - Required auth : `user`
    - Limiter : `GLOBAL`
    - Limit : `N/A`
    - Resets after : `N/A`
    - Notes : Untested.

- channel_delete
    - Endpoint : `/channels/{channel_id}`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- channel_group_leave
    - Endpoint : `/channels/{channel_id}`
    - Method : `DELETE`
    - Required auth : `user`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`
    - Notes : Untested.

- channel_edit
    - Endpoint : `/channels/{channel_id}`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `5`
    - Resets after : `15`
    - Notes : Has sub-limits.

- channel_group_edit
    - Endpoint : `/channels/{channel_id}`
    - Method : `PATCH`
    - Required auth : `user`
    - Limiter : `channel_id`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Untested.

- channel_directory_counts
    - Endpoint : `/channels/{channel_id}/directory-entries/counts`
    - Method : `GET`
    - Required auth : `user`
    - Limiter : `channel_id`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Untested.

- channel_directory_get_all
    - Endpoint : `/channels/{channel_id}/directory-entries/list`
    - Method : `GET`
    - Required auth : `user`
    - Limiter : `channel_id`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Untested.

- channel_directory_search
    - Endpoint : `/channels/{channel_id}/directory-entries/search`
    - Method : `GET`
    - Required auth : `user`
    - Limiter : `channel_id`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Untested.

- channel_follow
    - Endpoint : `/channels/{channel_id}/followers`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- greet
    - Endpoint : `/channels/{channel_id}/greet`
    - Method : `POST`
    - Required auth : `user`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Untested.

- invite_get_all_channel
    - Endpoint : `/channels/{channel_id}/invites`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- invite_create
    - Endpoint : `/channels/{channel_id}/invites`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `5`
    - Resets after : `15.0`

- message_get_chunk
    - Endpoint : `/channels/{channel_id}/messages`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `5`
    - Resets after : `5.0`

- message_create
    - Endpoint : `/channels/{channel_id}/messages`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `5`
    - Resets after : `4.0`

- message_delete_multiple
    - Endpoint : `/channels/{channel_id}/messages/bulk-delete`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `1`
    - Resets after : `3.0`

- message_delete
    - Endpoint : `/channels/{channel_id}/messages/{message_id}`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `3`
    - Resets after : `1.0`
    - Notes : Applicable for messages posted by the bot or which are younger than 2 weeks. Has sub-limits.

- message_delete_b2wo
    - Endpoint : `/channels/{channel_id}/messages/{message_id}`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `30`
    - Resets after : `120.0`
    - Notes : Applicable for messages which are not posted by the bot and are older than 2 weeks. Has sub-limits.

- message_get
    - Endpoint : `/channels/{channel_id}/messages/{message_id}`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `5`
    - Resets after : `5.0`

- message_edit
    - Endpoint : `/channels/{channel_id}/messages/{message_id}`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `5`
    - Resets after : `4.0`

- message_ack
    - Endpoint : `/channels/{channel_id}/messages/{message_id}/ack`
    - Method : `POST`
    - Required auth : `user`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`

- message_crosspost
    - Endpoint : `/channels/{channel_id}/messages/{message_id}/crosspost`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `10`
    - Resets after : `3600.0`

- message_interaction
    - Endpoint : `/channels/{channel_id}/messages/{message_id}/interaction-data`
    - Method : `GET`
    - Required auth : `user`
    - Limiter : `UN`
    - Limit : `UN`
    - Resets after : `UN`

- reaction_clear
    - Endpoint : `/channels/{channel_id}/messages/{message_id}/reactions`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `1`
    - Resets after : `0.25`

- reaction_delete_emoji
    - Endpoint : `/channels/{channel_id}/messages/{message_id}/reactions/{reaction}`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `1`
    - Resets after : `0.25`

- reaction_user_get_chunk
    - Endpoint : `/channels/{channel_id}/messages/{message_id}/reactions/{reaction}`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- reaction_delete_own
    - Endpoint : `/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `1`
    - Resets after : `0.25`

- reaction_add
    - Endpoint : `/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me`
    - Method : `PUT`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `1`
    - Resets after : `0.25`

- reaction_delete
    - Endpoint : `/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/{user_id}`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `1`
    - Resets after : `0.25`

- message_suppress_embeds
    - Endpoint : `/channels/{channel_id}/messages/{message_id}/suppress-embeds`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `3`
    - Resets after : `1`

- thread_create_from_message
    - Endpoint : `/channels/{channel_id}/messages/{message_id}/threads`
    - Method : `POST`
    - Required auth : `UN`
    - Limiter : `GLOBAL`
    - Limit : `50`
    - Resets after : `300.0`

- permission_overwrite_delete
    - Endpoint : `/channels/{channel_id}/permissions/{overwrite_id}`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `10`
    - Resets after : `15.0`

- permission_overwrite_create
    - Endpoint : `/channels/{channel_id}/permissions/{overwrite_id}`
    - Method : `PUT`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `10`
    - Resets after : `15.0`

- channel_pin_get_all
    - Endpoint : `/channels/{channel_id}/pins`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `1`
    - Resets after : `5`

- channel_pin_ack
    - Endpoint : `/channels/{channel_id}/pins/ack`
    - Method : `POST`
    - Required auth : `user`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Untested.

- message_unpin
    - Endpoint : `/channels/{channel_id}/pins/{message_id}`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `5`
    - Resets after : `4`

- message_pin
    - Endpoint : `/channels/{channel_id}/pins/{message_id}`
    - Method : `PUT`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `5`
    - Resets after : `4`

- channel_group_user_get_all
    - Endpoint : `/channels/{channel_id}/recipients/`
    - Method : `GET`
    - Required auth : `user`
    - Limiter : `channel_id`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Untested.

- channel_group_user_delete
    - Endpoint : `/channels/{channel_id}/recipients/{user_id}`
    - Method : `DELETE`
    - Required auth : `user`
    - Limiter : `channel_id`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Untested.

- channel_group_user_add
    - Endpoint : `/channels/{channel_id}/recipients/{user_id}`
    - Method : `PUT`
    - Required auth : `user`
    - Limiter : `channel_id`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Untested.

- thread_leave
    - Endpoint : `/channels/{channel_id}/thread-members/@me`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `5`
    - Resets after : `5.0`

- thread_user_get_all
    - Endpoint : `/channels/{channel_id}/thread-members`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `10`
    - Resets after : `10.0`

- thread_join
    - Endpoint : `/channels/{channel_id}/thread-members/@me`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `5`
    - Resets after : `5.0`

- thread_user_delete
    - Endpoint : `/channels/{channel_id}/thread-members/{user_id}`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `5`
    - Resets after : `5.0`

- thread_user_add
    - Endpoint : `/channels/{channel_id}/thread-members/{user_id}`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `5`
    - Resets after : `5.0`

- thread_self_settings_edit
    - Endpoint : `/channels/{channel_id}/thread-members/@me/settings`
    - Method : `PATCH`
    - Required auth : `user`
    - Limiter : `GLOBAL`
    - Limit : `4`
    - Resets after : `60.0`

- thread_create
    - Endpoint : `/channels/{channel_id}/threads`
    - Method : `POST`
    - Required auth : `UN`
    - Limiter : `GLOBAL`
    - Limit : `50`
    - Resets after : `300.0`

- channel_thread_get_chunk_active
    - Endpoint : `/channels/{channel_id}/threads/active`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- channel_thread_get_chunk_archived_private
    - Endpoint : `/channels/{channel_id}/threads/archived/private`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- channel_thread_get_chunk_archived_public
    - Endpoint : `/channels/{channel_id}/threads/archived/public`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- typing
    - Endpoint : `/channels/{channel_id}/typing`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `5`
    - Resets after : `5.0`

- channel_thread_get_chunk_self_archived
    - Endpoint : `/channels/{channel_id}/users/@me/threads/archived/private`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- webhook_get_all_channel
    - Endpoint : `/channels/{channel_id}/webhooks`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- webhook_create
    - Endpoint : `/channels/{channel_id}/webhooks`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `channel_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- discovery_stage_get_all
    - Endpoint : `/discovery`
    - Method : `GET`
    - Required auth : `UN`
    - Limiter : `UN`
    - Limit : `UN`
    - Resets after : `UN`
    - Notes : Untested. `DiscordException Not Found (404): 404: Not Found`

- discovery_category_get_all
    - Endpoint : `/discovery/categories`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `10`
    - Resets after : `120.0`

- discovery_validate_term
    - Endpoint : `/discovery/valid-term`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `10`
    - Resets after : `10.0`

- client_gateway_hooman
    - Endpoint : `/gateway`
    - Method : `GET`
    - Required auth : `user`
    - Limiter : `GLOBAL`
    - Limit : `UN`
    - Resets after : `UN`
    - Notes : Untested.

- client_gateway_bot
    - Endpoint : `/gateway/bot`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `2`
    - Resets after : `5`

- discovery_guild_get_all
    - Endpoint : `/guild-discovery`
    - Method : `GET`
    - Required auth : `UN`
    - Limiter : `UN`
    - Limit : `UN`
    - Resets after : `UN`
    - Notes : Untested. `DiscordException Not Found (404): 404: Not Found`

- guild_create
    - Endpoint : `/guilds`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- guild_delete
    - Endpoint : `/guilds/{guild_id}`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- guild_get
    - Endpoint : `/guilds/{guild_id}`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- guild_edit
    - Endpoint : `/guilds/{guild_id}`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- guild_ack
    - Endpoint : `/guilds/{guild_id}/ack`
    - Method : `POST`
    - Required auth : `user`
    - Limiter : `GLOBAL`
    - Limit : `UN`
    - Resets after : `UN`
    - Notes : Untested.

- audit_log_get_chunk
    - Endpoint : `/guilds/{guild_id}/audit-logs`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- guild_ban_get_all
    - Endpoint : `/guilds/{guild_id}/bans`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- guild_ban_delete
    - Endpoint : `/guilds/{guild_id}/bans/{user_id}`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- guild_ban_get
    - Endpoint : `/guilds/{guild_id}/bans/{user_id}`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- guild_ban_add
    - Endpoint : `/guilds/{guild_id}/bans/{user_id}`
    - Method : `PUT`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- guild_channel_get_all
    - Endpoint : `/guilds/{guild_id}/channels`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- channel_move
    - Endpoint : `/guilds/{guild_id}/channels`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- channel_create
    - Endpoint : `/guilds/{guild_id}/channels`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- guild_discovery_delete_subcategory
    - Endpoint : `/guilds/{guild_id}/discovery-categories/{category_id}`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- guild_discovery_add_subcategory
    - Endpoint : `/guilds/{guild_id}/discovery-categories/{category_id}`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- guild_discovery_get
    - Endpoint : `/guilds/{guild_id}/discovery-metadata`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- guild_discovery_edit
    - Endpoint : `/guilds/{guild_id}/discovery-metadata`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- guild_embed_get
    - Endpoint : `/guilds/{guild_id}/embed`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Deprecated. Works on v6, v7.

- guild_embed_edit
    - Endpoint : `/guilds/{guild_id}/embed`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Deprecated. Works on v6, v7.

- guild.embed_url
    - Endpoint : `/guilds/{guild_id}/embed.png`
    - Method : `GET`
    - Required auth : `N/A`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`
    - Notes : Deprecated. Works on v6, v7.

- emoji_guild_get_all
    - Endpoint : `/guilds/{guild_id}/emojis`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- emoji_create
    - Endpoint : `/guilds/{guild_id}/emojis`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `50`
    - Resets after : `3600.0`
    - Notes : Creating an emoji with the same name of an existing one has a different rate limit.
              Please don't do that.

- emoji_delete
    - Endpoint : `/guilds/{guild_id}/emojis`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `1`
    - Resets after : `2.0`

- emoji_get
    - Endpoint : `/guilds/{guild_id}/emojis/{emoji_id}`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- emoji_edit
    - Endpoint : `/guilds/{guild_id}/emojis/{emoji_id}`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `1`
    - Resets after : `2.0`

- integration_get_all
    - Endpoint : `/guilds/{guild_id}/integrations`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- integration_create
    - Endpoint : `/guilds/{guild_id}/integrations`
    - Method : `POST`
    - Required auth : `UN`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Untested.

- integration_delete
    - Endpoint : `/guilds/{guild_id}/integrations/{integration_id}`
    - Method : `DELETE`
    - Required auth : `UN`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Untested.

- integration_edit
    - Endpoint : `/guilds/{guild_id}/integrations/{integration_id}`
    - Method : `PATCH`
    - Required auth : `UN`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Untested.

- integration_edit
    - Endpoint : `/guilds/{guild_id}/integrations/{integration_id}/sync`
    - Method : `POST`
    - Required auth : `UN`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Untested.

- invite_get_all_guild
    - Endpoint : `/guilds/{guild_id}/invites`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- verification_screen_get
    - Endpoint : `/guilds/{guild_id}/member-verification`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- verification_screen_edit
    - Endpoint : `/guilds/{guild_id}/member-verification`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- guild_user_get_chunk
    - Endpoint : `/guilds/{guild_id}/members`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `10`
    - Resets after : `10.0`

- client_guild_profile_edit
    - Endpoint : `/guilds/{guild_id}/members/@me`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `1`
    - Resets after : `1.0`

- client_guild_profile_nick_edit
    - Endpoint : `/guilds/{guild_id}/members/@me/nick`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `1`
    - Resets after : `1.0`

- guild_user_delete
    - Endpoint : `/guilds/{guild_id}/members/{user_id}`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `5`
    - Resets after : `1.0`

- guild_user_get
    - Endpoint : `/guilds/{guild_id}/members/{user_id}`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `5`
    - Resets after : `1.0`

- user_guild_profile_edit, user_move
    - Endpoint : `/guilds/{guild_id}/members/{user_id}`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `10`
    - Resets after : `10.0`

- guild_user_add
    - Endpoint : `/guilds/{guild_id}/members/{user_id}`
    - Method : `PUT`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `10`
    - Resets after : `10.0`

- guild_user_search
    - Endpoint : `/guilds/{guild_id}/members/search`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `10`
    - Resets after : `10.0`

- user_role_delete
    - Endpoint : `/guilds/{guild_id}/members/{user_id}/roles/{role_id}`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `10`
    - Resets after : `10.0`

- user_role_add
    - Endpoint : `/guilds/{guild_id}/members/{user_id}/roles/{role_id}`
    - Method : `PUT`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `10`
    - Resets after : `10.0`

- guild_preview_get
    - Endpoint : `/guilds/{guild_id}/preview`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `5`
    - Resets after : `5.0`

- guild_prune_estimate
    - Endpoint : `/guilds/{guild_id}/prune`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- guild_prune
    - Endpoint : `/guilds/{guild_id}/prune`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- guild_voice_region_get_all
    - Endpoint : `/guilds/{guild_id}/regions`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- guild_role_get_all
    - Endpoint : `/guilds/{guild_id}/roles`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- role_move
    - Endpoint : `/guilds/{guild_id}/roles`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- role_create
    - Endpoint : `/guilds/{guild_id}/roles`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `250`
    - Resets after : `172800.0`

- role_delete
    - Endpoint : `/guilds/{guild_id}/roles/{role_id}`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- role_edit
    - Endpoint : `/guilds/{guild_id}/roles/{role_id}`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `1000`
    - Resets after : `86400.0`

- sticker_guild_get_all
    - Endpoint : `/guilds/{guild_id}/stickers`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- sticker_guild_create
    - Endpoint : `/guilds/{guild_id}/stickers`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `50`
    - Resets after : `3600.0`

- sticker_guild_edit
    - Endpoint : `/guilds/{guild_id}/stickers/{sticker_id}`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `1`
    - Resets after : `2.0`

- sticker_guild_delete
    - Endpoint : `/guilds/{guild_id}/stickers/{sticker_id}`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `1`
    - Resets after : `2.0`

- sticker_guild_get
    - Endpoint : `/guilds/{guild_id}/stickers/{sticker_id}`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- guild_thread_get_all_active
    - Endpoint : `/guilds/{guild_id}/threads/active`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- vanity_invite_get
    - Endpoint : `/guilds/{guild_id}/vanity-url`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- vanity_invite_edit
    - Endpoint : `/guilds/{guild_id}/vanity-url`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `10`
    - Resets after : `60.0`

- voice_state_client_edit
    - Endpoint : `/guilds/{guild_id}/voice-states/@me`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : GLOBAL
    - Limit : 15
    - Resets after : `5.0`

- voice_state_user_edit
    - Endpoint : `/guilds/{guild_id}/voice-states/@me`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : GLOBAL
    - Limit : `5`
    - Resets after : `5.0`

- welcome_screen_get
    - Endpoint : `/guilds/{guild_id}/welcome-screen`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- welcome_screen_edit
    - Endpoint : `/guilds/{guild_id}/welcome-screen`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `100`
    - Resets after : `86400.0`

- webhook_get_all_guild
    - Endpoint : `/guilds/{guild_id}/webhooks`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `guild_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- guild_widget_get
    - Endpoint : `/guilds/{guild_id}/widget.json`
    - Method : `GET`
    - Required auth : `N/A`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- guild.widget_url
    - Endpoint : `/guilds/{guild_id}/widget.png`
    - Method : `GET`
    - Required auth : `N/A`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- hypesquad_house_leave
    - Endpoint : `/hypesquad/online`
    - Method : `DELETE`
    - Required auth : `user`
    - Limiter : `GLOBAL`
    - Limit : `UN`
    - Resets after : `UN`
    - Notes : Untested.

- hypesquad_house_change
    - Endpoint : `/hypesquad/online`
    - Method : `POST`
    - Required auth : `user`
    - Limiter : `GLOBAL`
    - Limit : `UN`
    - Resets after : `UN`
    - Notes : Untested.

- interaction_response_message_create
    - Endpoint : `/interactions/{interaction_id}/{interaction_token}/callback`
    - Method : `POST`
    - Required auth : `N/A`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- invite_delete
    - Endpoint : `/invites/{invite_code}`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- invite_get
    - Endpoint : `/invites/{invite_code}`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `250`
    - Resets after : `6.0`

- client_application_get
    - Endpoint : `/oauth2/applications/@me`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`

- bulk_ack
    - Endpoint : `/read-states/ack-bulk`
    - Method : `POST`
    - Required auth : `user`
    - Limiter : `GLOBAL`
    - Limit : `UN`
    - Resets after : `UN`
    - Notes : Untested.

- stage_get_all
    - Endpoint : `/stage-instances`
    - Method : `GET`
    - Required auth : `user`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`
    - Notes : `DiscordException Forbidden (403), code=20001: Bots cannot use this endpoint`

- stage_create
    - Endpoint : `/stage-instances`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `100`
    - Resets after : `86400.0`

- stage_get
    - Endpoint : `/stage-instances/{channel_id}`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- stage_delete
    - Endpoint : `/stage-instances/{channel_id}`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `100`
    - Resets after : `86400.0`

- stage_edit
    - Endpoint : `/stage-instances/{channel_id}`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `5`
    - Resets after : `60.0`

- sticker_pack_get_all
    - Endpoint : `/sticker-packs`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- sticker_get
    - Endpoint : `/stickers/{sticker_id}`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `5`
    - Resets after : `2.0`

- eula_get
    - Endpoint : `/store/eulas/{eula_id}`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`

- user_info_get
    - Endpoint : `/users/@me`
    - Method : `GET`
    - Required auth : `bearer`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`

- client_user_get
    - Endpoint : `/users/@me`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`

- client_edit
    - Endpoint : `/users/@me`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `2`
    - Resets after : `600.0`

- user_achievement_get_all
    - Endpoint : `/users/@me/applications/{application_id}/achievements`
    - Method : `GET`
    - Required auth : `bearer`
    - Limiter : `GLOBAL`
    - Limit : `2`
    - Resets after : `5.0`
    - Notes : Untested.

- user_achievement_update
    - Endpoint : `/users/{user_id}/applications/{application_id}/achievements/{achievement_id}`
    - Method : `PUT`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `5`
    - Resets after : `5.0`

- channel_private_get_all
    - Endpoint : `/users/@me/channels`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`

- channel_private_create
    - Endpoint : `/users/@me/channels`
    - Method : `POST`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- client_connection_get_all
    - Endpoint : `/users/@me/connections`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`

- user_connection_get_all
    - Endpoint : `/users/@me/connections`
    - Method : `GET`
    - Required auth : `bearer`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`

- guild_get_all
    - Endpoint : `/users/@me/guilds`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `1`
    - Resets after : `1.0`

- user_guild_get_all
    - Endpoint : `/users/@me/guilds`
    - Method : `GET`
    - Required auth : `bearer`
    - Limiter : `GLOBAL`
    - Limit : `1`
    - Resets after : `1.0`

- guild_leave
    - Endpoint : `/users/@me/guilds/{guild_id}`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- relationship_friend_request
    - Endpoint : `/users/@me/relationships`
    - Method : `POST`
    - Required auth : `user`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Untested.

- relationship_delete
    - Endpoint : `/users/@me/relationships/{user_id}`
    - Method : `DELETE`
    - Required auth : `user`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Untested.

- relationship_create
    - Endpoint : `/users/@me/settings`
    - Method : `PUT`
    - Required auth : `user`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Untested.

- client_settings_get
    - Endpoint : `/users/@me/settings`
    - Method : `GET`
    - Required auth : `user`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Untested.

- client_settings_edit
    - Endpoint : `/users/@me/settings`
    - Method : `PATCH`
    - Required auth : `user`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Untested.

- user_get
    - Endpoint : `/users/{user_id}`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `30`
    - Resets after : `30.0`

- channel_group_create
    - Endpoint : `/users/{user_id}/channels`
    - Method : `POST`
    - Required auth : `user`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Untested.

- user_get_profile
    - Endpoint : `users/{user_id}/profile`
    - Method : `GET`
    - Required auth : `user`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`
    - Notes : Untested.

- voice_region_get_all
    - Endpoint : `/voice/regions`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `GLOBAL`
    - Limit : `OPT`
    - Resets after : `OPT`

- interaction_followup_message_create
    - Endpoint : `webhooks/{application_id}/{interaction_token}`
    - Method : `POST`
    - Required auth : `N/A`
    - Limiter : `interaction_id`
    - Limit : `5`
    - Resets after : `2.0`

- interaction_response_message_delete
    - Endpoint : `webhooks/{application_id}/{interaction_token}/messages/@original`
    - Method : `DELETE`
    - Required auth : `N/A`
    - Limiter : `interaction_id`
    - Limit : `5`
    - Resets after : `2.0`

- interaction_response_message_get
    - Endpoint : `webhooks/{application_id}/{interaction_token}/messages/@original`
    - Method : `GET`
    - Required auth : `N/A`
    - Limiter : `interaction_id`
    - Limit : `5`
    - Resets after : `2.0`

- interaction_response_message_edit
    - Endpoint : `webhooks/{application_id}/{interaction_token}/messages/@original`
    - Method : `PATCH`
    - Required auth : `N/A`
    - Limiter : `interaction_id`
    - Limit : `5`
    - Resets after : `2.0`

- interaction_followup_message_delete
    - Endpoint : `webhooks/{application_id}/{interaction_token}/messages/{message_id}`
    - Method : `DELETE`
    - Required auth : `N/A`
    - Limiter : `interaction_id`
    - Limit : `5`
    - Resets after : `2.0`

- interaction_followup_message_get
    - Endpoint : `webhooks/{application_id}/{interaction_token}/messages/{message_id}`
    - Method : `GET`
    - Required auth : `N/A`
    - Limiter : `interaction_id`
    - Limit : `5`
    - Resets after : `2.0`

- interaction_followup_message_edit
    - Endpoint : `webhooks/{application_id}/{interaction_token}/messages/{message_id}`
    - Method : `PATCH`
    - Required auth : `N/A`
    - Limiter : `interaction_id`
    - Limit : `5`
    - Resets after : `2.0`

- webhook_delete
    - Endpoint : `/webhooks/{webhook_id}`
    - Method : `DELETE`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- webhook_get
    - Endpoint : `/webhooks/{webhook_id}`
    - Method : `GET`
    - Required auth : `bot`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- webhook_edit
    - Endpoint : `/webhooks/{webhook_id}`
    - Method : `PATCH`
    - Required auth : `bot`
    - Limiter : `webhook_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- webhook_delete_token
    - Endpoint : `/webhooks/{webhook_id}/{webhook_token}`
    - Method : `DELETE`
    - Required auth : `N/A`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- webhook_get_token
    - Endpoint : `/webhooks/{webhook_id}/{webhook_token}`
    - Method : `GET`
    - Required auth : `N/A`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`

- webhook_edit_token
    - Endpoint : `/webhooks/{webhook_id}/{webhook_token}`
    - Method : `PATCH`
    - Required auth : `N/A`
    - Limiter : `webhook_id`
    - Limit : `OPT`
    - Resets after : `OPT`

- webhook_message_create
    - Endpoint : `/webhooks/{webhook_id}/{webhook_token}`
    - Method : `POST`
    - Required auth : `N/A`
    - Limiter : `webhook_id`
    - Limit : `5`
    - Resets after : `2.0`

- webhook_message_delete
    - Endpoint : `/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}`
    - Method : `DELETE`
    - Required auth : `N/A`
    - Limiter : `webhook_id`
    - Limit : `5`
    - Resets after : `2.0`

- webhook_message_get
    - Endpoint : `/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}`
    - Method : `GET`
    - Required auth : `N/A`
    - Limiter : `webhook_id`
    - Limit : `5`
    - Resets after : `2.0`

- webhook_message_edit
    - Endpoint : `/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}`
    - Method : `PATCH`
    - Required auth : `N/A`
    - Limiter : `webhook_id`
    - Limit : `5`
    - Resets after : `2.0`
"""
GROUP_REACTION_MODIFY = RateLimitGroup(LIMITER_CHANNEL)
GROUP_PIN_MODIFY = RateLimitGroup(LIMITER_CHANNEL)
GROUP_USER_MODIFY = RateLimitGroup(LIMITER_GUILD) # both has the same endpoint
GROUP_USER_ROLE_MODIFY = RateLimitGroup(LIMITER_GUILD)
GROUP_WEBHOOK_EXECUTE = RateLimitGroup(LIMITER_WEBHOOK)
GROUP_INTERACTION_EXECUTE = RateLimitGroup(LIMITER_INTERACTION)
GROUP_APPLICATION_COMMAND_CREATE = RateLimitGroup()
GROUP_APPLICATION_COMMAND_DELETE = RateLimitGroup()
GROUP_APPLICATION_COMMAND_EDIT = RateLimitGroup()
GROUP_PERMISSION_OVERWRITE_MODIFY = RateLimitGroup(LIMITER_CHANNEL)
GROUP_THREAD_CREATE = RateLimitGroup()
GROUP_THREAD_ACTION = RateLimitGroup()

oauth2_token = RateLimitGroup(optimistic=True)
application_get = RateLimitGroup(optimistic=True) # untested
achievement_get_all = RateLimitGroup()
achievement_create = RateLimitGroup()
achievement_delete = RateLimitGroup()
achievement_get = RateLimitGroup()
achievement_edit = RateLimitGroup()
application_command_global_get_all = RateLimitGroup.unlimited()
application_command_global_delete = RateLimitGroup()
application_command_global_create = RateLimitGroup()
application_command_global_update_multiple = RateLimitGroup()
application_command_global_get = RateLimitGroup.unlimited()
application_command_global_edit = RateLimitGroup()
application_command_guild_get_all = RateLimitGroup.unlimited()
application_command_guild_update_multiple = RateLimitGroup(LIMITER_GUILD)
application_command_permission_get_all_guild = RateLimitGroup.unlimited()
application_command_guild_delete = RateLimitGroup(LIMITER_GUILD)
application_command_guild_create = RateLimitGroup(LIMITER_GUILD)
application_command_guild_get = RateLimitGroup.unlimited()
application_command_guild_edit = RateLimitGroup(LIMITER_GUILD)
application_command_permission_get = RateLimitGroup.unlimited()
application_command_permission_edit = RateLimitGroup()
application_get_all_detectable = RateLimitGroup(optimistic=True)
client_logout = RateLimitGroup() # untested
channel_delete = RateLimitGroup.unlimited()
channel_group_leave = RateLimitGroup.unlimited() # untested; same as channel_delete?
channel_edit = RateLimitGroup(LIMITER_CHANNEL)
channel_group_edit = RateLimitGroup(LIMITER_CHANNEL, optimistic=True) # untested; same as channel_edit?
channel_directory_counts = RateLimitGroup(LIMITER_CHANNEL, optimistic=True) # untested; same as channel_edit?
channel_directory_get_all = RateLimitGroup(LIMITER_CHANNEL, optimistic=True) # untested; same as channel_edit?
channel_directory_search = RateLimitGroup(LIMITER_CHANNEL, optimistic=True) # untested; same as channel_edit?
channel_follow = RateLimitGroup(LIMITER_CHANNEL, optimistic=True)
greet = RateLimitGroup(optimistic=True) # untested
invite_get_all_channel = RateLimitGroup(LIMITER_CHANNEL, optimistic=True)
invite_create = RateLimitGroup()
message_get_chunk = RateLimitGroup(LIMITER_CHANNEL)
message_create = RateLimitGroup(LIMITER_CHANNEL)
message_delete_multiple = RateLimitGroup(LIMITER_CHANNEL)
message_delete = RateLimitGroup(LIMITER_CHANNEL)
message_delete_b2wo = RateLimitGroup(LIMITER_CHANNEL)
message_get = RateLimitGroup(LIMITER_CHANNEL)
message_edit = RateLimitGroup(LIMITER_CHANNEL)
message_ack = RateLimitGroup(optimistic=True) # untested
message_crosspost = RateLimitGroup(LIMITER_CHANNEL)
message_interaction = RateLimitGroup(optimistic=True) # untested
reaction_clear = GROUP_REACTION_MODIFY
reaction_delete_emoji = GROUP_REACTION_MODIFY
reaction_user_get_chunk = RateLimitGroup(LIMITER_CHANNEL, optimistic=True)
reaction_delete_own = GROUP_REACTION_MODIFY
reaction_add = GROUP_REACTION_MODIFY
reaction_delete = GROUP_REACTION_MODIFY
message_suppress_embeds = RateLimitGroup()
thread_create_from_message = GROUP_THREAD_CREATE
permission_overwrite_delete = GROUP_PERMISSION_OVERWRITE_MODIFY
permission_overwrite_create = GROUP_PERMISSION_OVERWRITE_MODIFY
channel_pin_get_all = RateLimitGroup()
channel_pin_ack = RateLimitGroup(optimistic=True) # untested
message_unpin = GROUP_PIN_MODIFY
message_pin = GROUP_PIN_MODIFY
channel_group_user_get_all = RateLimitGroup(LIMITER_CHANNEL, optimistic=True) # untested
channel_group_user_delete = RateLimitGroup(LIMITER_CHANNEL, optimistic=True) # untested
channel_group_user_add = RateLimitGroup(LIMITER_CHANNEL, optimistic=True) # untested
thread_user_get_all = RateLimitGroup()
thread_join = GROUP_THREAD_ACTION
thread_leave = GROUP_THREAD_ACTION
thread_user_add = GROUP_THREAD_ACTION
thread_user_delete = GROUP_THREAD_ACTION
thread_self_settings_edit = RateLimitGroup()
thread_create = GROUP_THREAD_CREATE
typing = RateLimitGroup(LIMITER_CHANNEL)
channel_thread_get_chunk_active = RateLimitGroup.unlimited()
channel_thread_get_chunk_archived_private = RateLimitGroup.unlimited()
channel_thread_get_chunk_archived_public = RateLimitGroup.unlimited()
channel_thread_get_chunk_self_archived = RateLimitGroup.unlimited()
webhook_get_all_channel = RateLimitGroup(LIMITER_CHANNEL, optimistic=True)
webhook_create = RateLimitGroup(LIMITER_CHANNEL, optimistic=True)
discovery_category_get_all = RateLimitGroup()
discovery_stage_get_all = RateLimitGroup(optimistic=True) # untested, not yet added
discovery_validate_term = RateLimitGroup()
client_gateway_hooman = RateLimitGroup()
client_gateway_bot = RateLimitGroup()
discovery_guild_get_all = RateLimitGroup(optimistic=True) # untested, not yet added
guild_create = RateLimitGroup.unlimited()
guild_delete = RateLimitGroup.unlimited()
guild_get = RateLimitGroup(LIMITER_GUILD, optimistic=True)
guild_edit = RateLimitGroup(LIMITER_GUILD, optimistic=True)
guild_ack = RateLimitGroup() # untested
audit_log_get_chunk = RateLimitGroup(LIMITER_GUILD, optimistic=True)
guild_ban_get_all = RateLimitGroup(LIMITER_GUILD, optimistic=True)
guild_ban_delete = RateLimitGroup(LIMITER_GUILD, optimistic=True)
guild_ban_get = RateLimitGroup(LIMITER_GUILD, optimistic=True)
guild_ban_add = RateLimitGroup(LIMITER_GUILD, optimistic=True)
guild_channel_get_all = RateLimitGroup(LIMITER_GUILD, optimistic=True)
channel_move = RateLimitGroup(LIMITER_GUILD, optimistic=True)
channel_create = RateLimitGroup(LIMITER_GUILD, optimistic=True)
guild_discovery_delete_subcategory = RateLimitGroup(LIMITER_GUILD, optimistic=True)
guild_discovery_add_subcategory = RateLimitGroup(LIMITER_GUILD, optimistic=True)
guild_discovery_get = RateLimitGroup(LIMITER_GUILD, optimistic=True)
guild_discovery_edit = RateLimitGroup(LIMITER_GUILD, optimistic=True)
guild_embed_get = RateLimitGroup(LIMITER_GUILD, optimistic=True) # deprecated
guild_embed_edit = RateLimitGroup(LIMITER_GUILD, optimistic=True) # deprecated
emoji_guild_get_all = RateLimitGroup(LIMITER_GUILD, optimistic=True)
emoji_create = RateLimitGroup()
emoji_delete = RateLimitGroup()
emoji_get = RateLimitGroup(LIMITER_GUILD, optimistic=True)
emoji_edit = RateLimitGroup()
integration_get_all = RateLimitGroup(LIMITER_GUILD, optimistic=True)
integration_create = RateLimitGroup(optimistic=True) # untested
integration_delete = RateLimitGroup(optimistic=True) # untested
integration_edit = RateLimitGroup(optimistic=True) # untested
integration_sync = RateLimitGroup(optimistic=True) # untested
invite_get_all_guild = RateLimitGroup(LIMITER_GUILD, optimistic=True)
verification_screen_get = RateLimitGroup(LIMITER_GUILD, optimistic=True)
verification_screen_edit = RateLimitGroup(LIMITER_GUILD, optimistic=True)
guild_user_get_chunk = RateLimitGroup(LIMITER_GUILD)
client_guild_profile_edit = RateLimitGroup()
client_guild_profile_nick_edit = RateLimitGroup()
guild_user_delete = RateLimitGroup(LIMITER_GUILD)
guild_user_get = RateLimitGroup(LIMITER_GUILD)
user_guild_profile_edit = GROUP_USER_MODIFY
user_move = GROUP_USER_MODIFY
guild_user_add = RateLimitGroup(LIMITER_GUILD)
guild_user_search = RateLimitGroup(LIMITER_GUILD)
user_role_delete = GROUP_USER_ROLE_MODIFY
user_role_add = GROUP_USER_ROLE_MODIFY
guild_preview_get = RateLimitGroup()
guild_prune_estimate = RateLimitGroup(LIMITER_GUILD, optimistic=True)
guild_prune = RateLimitGroup(LIMITER_GUILD, optimistic=True)
guild_voice_region_get_all = RateLimitGroup(LIMITER_GUILD, optimistic=True)
guild_role_get_all = RateLimitGroup(LIMITER_GUILD, optimistic=True)
role_move = RateLimitGroup(LIMITER_GUILD, optimistic=True)
role_create = RateLimitGroup(LIMITER_GUILD)
role_delete = RateLimitGroup(LIMITER_GUILD, optimistic=True)
role_edit = RateLimitGroup(LIMITER_GUILD)
sticker_guild_get_all = RateLimitGroup.unlimited()
sticker_guild_create = RateLimitGroup()
sticker_guild_edit = RateLimitGroup()
sticker_guild_delete = RateLimitGroup()
sticker_guild_get = RateLimitGroup.unlimited()
guild_thread_get_all_active = RateLimitGroup.unlimited()
vanity_invite_get = RateLimitGroup.unlimited()
vanity_invite_edit = RateLimitGroup()
voice_state_client_edit = RateLimitGroup()
voice_state_user_edit = RateLimitGroup.unlimited() # untested
welcome_screen_get = RateLimitGroup(LIMITER_GUILD, optimistic=True)
welcome_screen_edit = RateLimitGroup(LIMITER_GUILD)
webhook_get_all_guild = RateLimitGroup(LIMITER_GUILD, optimistic=True)
guild_widget_get = RateLimitGroup.unlimited()
hypesquad_house_leave = RateLimitGroup() # untested
hypesquad_house_change = RateLimitGroup() # untested
interaction_response_message_create = RateLimitGroup.unlimited()
invite_delete = RateLimitGroup.unlimited()
invite_get = RateLimitGroup()
client_application_get = RateLimitGroup(optimistic=True)
bulk_ack = RateLimitGroup(optimistic=True) # untested
stage_get_all = RateLimitGroup.unlimited()
stage_create = RateLimitGroup()
stage_get = RateLimitGroup()
stage_delete = RateLimitGroup()
stage_edit = RateLimitGroup()
sticker_pack_get_all = RateLimitGroup.unlimited()
sticker_get = RateLimitGroup()
eula_get = RateLimitGroup(optimistic=True)
user_info_get = RateLimitGroup(optimistic=True)
client_user_get = RateLimitGroup(optimistic=True)
client_edit = RateLimitGroup()
user_achievement_get_all = RateLimitGroup() # untested; has expected global rate limit
user_achievement_update = RateLimitGroup()
channel_private_get_all = RateLimitGroup(optimistic=True)
channel_private_create = RateLimitGroup.unlimited()
client_connection_get_all = RateLimitGroup(optimistic=True)
user_connection_get_all = RateLimitGroup(optimistic=True)
guild_get_all = RateLimitGroup()
user_guild_get_all = RateLimitGroup()
guild_leave = RateLimitGroup.unlimited()
relationship_friend_request = RateLimitGroup(optimistic=True) # untested
relationship_delete = RateLimitGroup(optimistic=True) # untested
relationship_create = RateLimitGroup(optimistic=True) # untested
client_settings_get = RateLimitGroup(optimistic=True) # untested
client_settings_edit = RateLimitGroup(optimistic=True) # untested
user_get = RateLimitGroup()
channel_group_create = RateLimitGroup(optimistic=True) # untested
user_get_profile = RateLimitGroup(optimistic=True) # untested
voice_region_get_all = RateLimitGroup(optimistic=True)
interaction_followup_message_create = GROUP_INTERACTION_EXECUTE
interaction_response_message_delete = GROUP_INTERACTION_EXECUTE
interaction_response_message_get = GROUP_INTERACTION_EXECUTE
interaction_response_message_edit = GROUP_INTERACTION_EXECUTE
interaction_followup_message_delete = GROUP_INTERACTION_EXECUTE
interaction_followup_message_get = GROUP_INTERACTION_EXECUTE
interaction_followup_message_edit = GROUP_INTERACTION_EXECUTE
webhook_delete = RateLimitGroup.unlimited()
webhook_get = RateLimitGroup.unlimited()
webhook_edit = RateLimitGroup(LIMITER_WEBHOOK, optimistic=True)
webhook_delete_token = RateLimitGroup.unlimited()
webhook_get_token = RateLimitGroup.unlimited()
webhook_edit_token = RateLimitGroup(LIMITER_WEBHOOK, optimistic=True)
webhook_message_create = GROUP_WEBHOOK_EXECUTE
webhook_message_edit = GROUP_WEBHOOK_EXECUTE
webhook_message_get = GROUP_WEBHOOK_EXECUTE
webhook_message_delete = GROUP_WEBHOOK_EXECUTE

# Alternative static versions
STATIC_MESSAGE_DELETE_SUB = StaticRateLimitGroup(5, 5.0, LIMITER_CHANNEL)
static_message_delete = (STATIC_MESSAGE_DELETE_SUB, StaticRateLimitGroup(3, 1.0, LIMITER_CHANNEL))
static_message_delete_b2wo = (STATIC_MESSAGE_DELETE_SUB, StaticRateLimitGroup(30, 120.0, LIMITER_CHANNEL))


# Status
status_incident_unresolved = RateLimitGroup.unlimited()
status_maintenance_active = RateLimitGroup.unlimited()
status_maintenance_upcoming = RateLimitGroup.unlimited()
