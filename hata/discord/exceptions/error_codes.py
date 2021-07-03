__all__ = ()


__doc__ = """
The possible json error codes received from Discord HTTP API requests.

These are the following:

+---------------------------------------------------+-----------+-------+
| Respective name                                   | Value     | Notes |
+===================================================+===========+=======+
| unknown_account                                   | 10001     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_application                               | 10002     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_channel                                   | 10003     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_guild                                     | 10004     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_integration                               | 10005     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_invite                                    | 10006     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_member                                    | 10007     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_message                                   | 10008     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_overwrite                                 | 10009     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_provider                                  | 10010     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_role                                      | 10011     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_token                                     | 10012     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_user                                      | 10013     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_emoji                                     | 10014     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_webhook                                   | 10015     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_webhook_service                           | 10016     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_session                                   | 10020     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_approval_form                             | 10023     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_ban                                       | 10026     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_SKU                                       | 10027     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_store_listing                             | 10028     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_entitlement                               | 10029     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_team                                      | 10030     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_lobby                                     | 10031     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_branch                                    | 10032     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_store_directory_layout                    | 10033     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_redistributable                           | 10036     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_gift_code                                 | 10038     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_team_member                               | 10040     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_guild_template                            | 10057     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_discovery_category                        | 10059     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_sticker                                   | 10060     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_interaction                               | 10062     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_application_command                       | 10063     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_voice_state                               | 10065     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_application_command_permissions           | 10066     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_stage                                     | 10067     | -     |
+---------------------------------------------------+-----------+-------+
| unknown_guild_member_verification_form            | 10068     | -     |
+---------------------------------------------------+-----------+-------+
| bots_not_allowed                                  | 20001     | -     |
+---------------------------------------------------+-----------+-------+
| only_bots_allowed                                 | 20002     | -     |
+---------------------------------------------------+-----------+-------+
| RPC_proxy_disallowed                              | 20003     | -     |
+---------------------------------------------------+-----------+-------+
| explicit_content                                  | 20009     | -     |
+---------------------------------------------------+-----------+-------+
| account_scheduled_for_deletion                    | 20011     | -     |
+---------------------------------------------------+-----------+-------+
| user_not_authorized_for_application               | 20012     | -     |
+---------------------------------------------------+-----------+-------+
| account_disabled                                  | 20013     | -     |
+---------------------------------------------------+-----------+-------+
| rate_limit_slowmode                               | 20016     | -     |
+---------------------------------------------------+-----------+-------+
| team_ownership_required                           | 20018     | -     |
+---------------------------------------------------+-----------+-------+
| rate_limit_announcement_message_edit              | 20022     | -     |
+---------------------------------------------------+-----------+-------+
| under_minimum_age                                 | 20024     | -     |
+---------------------------------------------------+-----------+-------+
| rate_limit_channel_write                          | 20028     | -     |
+---------------------------------------------------+-----------+-------+
| name_contains_disallowed_word                     | 20031     | -     |
+---------------------------------------------------+-----------+-------+
| guild_subscription_level_too_low                  | 20035     | -     |
+---------------------------------------------------+-----------+-------+
| max_guilds                                        | 30001     | 100   |
+---------------------------------------------------+-----------+-------+
| max_friends                                       | 30001     | 10000 |
+---------------------------------------------------+-----------+-------+
| max_pins                                          | 30003     | 50    |
+---------------------------------------------------+-----------+-------+
| max_recipients                                    | 30004     | 10    |
+---------------------------------------------------+-----------+-------+
| max_roles                                         | 30005     | 250   |
+---------------------------------------------------+-----------+-------+
| max_used_usernames                                | 30006     | -     |
+---------------------------------------------------+-----------+-------+
| max_webhooks                                      | 30007     | 10    |
+---------------------------------------------------+-----------+-------+
| max_emojis                                        | 30008     | -     |
+---------------------------------------------------+-----------+-------+
| max_reactions                                     | 30010     | 20    |
+---------------------------------------------------+-----------+-------+
| max_channels                                      | 30013     | 500   |
+---------------------------------------------------+-----------+-------+
| max_attachments                                   | 30015     | 10    |
+---------------------------------------------------+-----------+-------+
| max_invites                                       | 30016     | 1000  |
+---------------------------------------------------+-----------+-------+
| max_animated_emojis                               | 30018     | -     |
+---------------------------------------------------+-----------+-------+
| max_guild_members                                 | 30019     | -     |
+---------------------------------------------------+-----------+-------+
| max_application_game_SKUs                         | 30021     | -     |
+---------------------------------------------------+-----------+-------+
| max_teams                                         | 30023     | -     |
+---------------------------------------------------+-----------+-------+
| max_companies                                     | 30025     | -     |
+---------------------------------------------------+-----------+-------+
| not_enough_guild_members                          | 30029     | -     |
+---------------------------------------------------+-----------+-------+
| max_guild_discovery_category                      | 30030     | 5     |
+---------------------------------------------------+-----------+-------+
| guild_has_template                                | 30031     | -     |
+---------------------------------------------------+-----------+-------+
| max_application_commands                          | 30032     | 50    |
+---------------------------------------------------+-----------+-------+
| max_thread_participants                           | 30033     | -     |
+---------------------------------------------------+-----------+-------+
| max_bans                                          | 30035     | -     |
+---------------------------------------------------+-----------+-------+
| max_ban_fetches                                   | 30037     | -     |
+---------------------------------------------------+-----------+-------+
| unauthorized                                      | 40001     | -     |
+---------------------------------------------------+-----------+-------+
| email_verification_required                       | 40002     | -     |
+---------------------------------------------------+-----------+-------+
| rate_limit_private_channel_opening                | 40003     | -     |
+---------------------------------------------------+-----------+-------+
| send_message_temporarily_disabled                 | 40004     | -     |
+---------------------------------------------------+-----------+-------+
| request_too_large                                 | 40005     | -     |
+---------------------------------------------------+-----------+-------+
| feature_disabled                                  | 40006     | -     |
+---------------------------------------------------+-----------+-------+
| user_banned                                       | 40007     | -     |
+---------------------------------------------------+-----------+-------+
| connection_rewoked                                | 40012     | -     |
+---------------------------------------------------+-----------+-------+
| user_in_team                                      | 40024     | -     |
+---------------------------------------------------+-----------+-------+
| team_members_must_be_verified                     | 40026     | -     |
+---------------------------------------------------+-----------+-------+
| team_invitation_accepted                          | 40027     | -     |
+---------------------------------------------------+-----------+-------+
| delete_account_transfer_team_ownership            | 40028     | -     |
+---------------------------------------------------+-----------+-------+
| user_not_connected_to_voice                       | 40032     | -     |
+---------------------------------------------------+-----------+-------+
| message_crossposted                               | 40033     | -     |
+---------------------------------------------------+-----------+-------+
| user_identity_verification_processing             | 40035     | -     |
+---------------------------------------------------+-----------+-------+
| user_identity_verification_succeeded              | 40036     | -     |
+---------------------------------------------------+-----------+-------+
| application_name_used                             | 40041     | -     |
+---------------------------------------------------+-----------+-------+
| missing_access                                    | 50001     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_account_type                              | 50002     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_action_for_private_channel                | 50003     | -     |
+---------------------------------------------------+-----------+-------+
| widget_disabled                                   | 50004     | -     |
+---------------------------------------------------+-----------+-------+
| cannot_edit_message_of_other_user                 | 50005     | -     |
+---------------------------------------------------+-----------+-------+
| cannot_create_empty_message                       | 50006     | -     |
+---------------------------------------------------+-----------+-------+
| cannot_message_user                               | 50007     | -     |
+---------------------------------------------------+-----------+-------+
| cannot_send_message_to_non_text_channel           | 50008     | -     |
+---------------------------------------------------+-----------+-------+
| channel_verification_level_too_high               | 50009     | -     |
+---------------------------------------------------+-----------+-------+
| oauth2_application_has_no_bot                     | 50010     | -     |
+---------------------------------------------------+-----------+-------+
| oauth2_application_limit_reached                  | 50011     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_oauth2_state                              | 50012     | -     |
+---------------------------------------------------+-----------+-------+
| missing_permissions                               | 50013     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_token                                     | 50014     | -     |
+---------------------------------------------------+-----------+-------+
| note_too_long                                     | 50015     | -     |
+---------------------------------------------------+-----------+-------+
| bulk_delete_amount_out_of_range                   | 50016     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_MFA_level                                 | 50017     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_password                                  | 50018     | -     |
+---------------------------------------------------+-----------+-------+
| cannot_pin_message_in_different_channel           | 50019     | -     |
+---------------------------------------------------+-----------+-------+
| invite_code_invalid_or_taken                      | 50020     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_action_for_system_message                 | 50021     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_phone_number                              | 50022     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_client_id                                 | 50023     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_action_for_this_channel_type              | 50024     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_oauth2_access_token                       | 50025     | -     |
+---------------------------------------------------+-----------+-------+
| missing_oauth2_scope                              | 50026     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_webhook_token                             | 50027     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_role                                      | 50028     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_recipients                                | 50033     | -     |
+---------------------------------------------------+-----------+-------+
| bulk_delete_message_too_old                       | 50034     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_form_body                                 | 50035     | -     |
+---------------------------------------------------+-----------+-------+
| cannot_add_user_to_guild_where_bot_is_not_in      | 50036     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_sticker_sent                              | 50081     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_action_for_archived_thread                | 50083     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_thread_notification_setting               | 50084     | -     |
+---------------------------------------------------+-----------+-------+
| before_value_earlier_than_creation_time           | 50085     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_API_version                               | 50041     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_asset                                     | 50046     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_application_name                          | 50050     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_gift_redemption_owned                     | 50051     | -     |
+---------------------------------------------------+-----------+-------+
| cannot_self_redeem_this_gift                      | 50054     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_message_type                              | 50068     | -     |
+---------------------------------------------------+-----------+-------+
| payment_source_required_to_redeem_gift            | 50070     | -     |
+---------------------------------------------------+-----------+-------+
| cannot_delete_community_channel                   | 50074     | -     |
+---------------------------------------------------+-----------+-------+
| invalid_gift_redemption_subscription_managed      | 100021    | -     |
+---------------------------------------------------+-----------+-------+
| invalid_gift_redemption_subscription_incompatible | 100023    | -     |
+--------------------------------pa-------------------+-----------+-------+
| invalid_gift_redemption_invoice_open              | 100024    | -     |
+---------------------------------------------------+-----------+-------+
| MFA_enabled                                       | 60001     | -     |
+---------------------------------------------------+-----------+-------+
| MFA_disabled                                      | 60002     | -     |
+---------------------------------------------------+-----------+-------+
| MFA_required                                      | 60003     | -     |
+---------------------------------------------------+-----------+-------+
| MFA_unverified                                    | 60004     | -     |
+---------------------------------------------------+-----------+-------+
| MFA_invalid_secret                                | 60005     | -     |
+---------------------------------------------------+-----------+-------+
| MFA_invalid_ticket                                | 60006     | -     |
+---------------------------------------------------+-----------+-------+
| MFA_invalid_code                                  | 60008     | -     |
+---------------------------------------------------+-----------+-------+
| MFA_invalid_session                               | 60009     | -     |
+---------------------------------------------------+-----------+-------+
| phone_number_unable_to_send                       | 70003     | -     |
+---------------------------------------------------+-----------+-------+
| relationship_incoming_disabled                    | 80000     | -     |
+---------------------------------------------------+-----------+-------+
| relationship_incoming_blocked                     | 80001     | -     |
+---------------------------------------------------+-----------+-------+
| relationship_invalid_target_bot                   | 80002     | -     |
+---------------------------------------------------+-----------+-------+
| relationship_invalid_target_self                  | 80003     | -     |
+---------------------------------------------------+-----------+-------+
| relationship_invalid_discord_tag                  | 80004     | -     |
+---------------------------------------------------+-----------+-------+
| reaction_blocked                                  | 90001     | -     |
+---------------------------------------------------+-----------+-------+
| authentication_required                           | 100029    | -     |
+---------------------------------------------------+-----------+-------+
| listing_already_joined                            | 120000    | -     |
+---------------------------------------------------+-----------+-------+
| listing_too_many_member                           | 120001    | -     |
+---------------------------------------------------+-----------+-------+
| listing_join_blocked                              | 120002    | -     |
+---------------------------------------------------+-----------+-------+
| resource_overloaded                               | 130000    | -     |
+---------------------------------------------------+-----------+-------+
| stage_already_open                                | 150006    | -     |
+---------------------------------------------------+-----------+-------+
| message_has_thread                                | 160004    | -     |
+---------------------------------------------------+-----------+-------+
| thread_locked                                     | 160005    | -     |
+---------------------------------------------------+-----------+-------+
| max_active_threads                                | 160006    | -     |
+---------------------------------------------------+-----------+-------+
| max_active_announcement_threads                   | 160007    | -     |
+---------------------------------------------------+-----------+-------+
"""
unknown_account = 10001
unknown_application = 10002
unknown_channel = 10003
unknown_guild = 10004
unknown_integration = 10005
unknown_invite = 10006
unknown_member = 10007
unknown_message = 10008
unknown_overwrite = 10009
unknown_provider = 10010
unknown_role = 10011
unknown_token = 10012
unknown_user = 10013
unknown_emoji = 10014
unknown_webhook = 10015
unknown_webhook_service = 10016
unknown_session = 10020
unknown_approval_form = 10023
unknown_ban = 10026
unknown_SKU = 10027
unknown_store_listing = 10028
unknown_entitlement = 10029
unknown_team = 10030
unknown_lobby = 10031
unknown_branch = 10032
unknown_store_directory_layout = 10033
unknown_redistributable = 10036
unknown_gift_code = 10038
unknown_team_member = 10040
unknown_guild_template = 10057
unknown_discovery_category = 10059
unknown_sticker = 10060
unknown_interaction = 10062
unknown_application_command = 10063
unknown_voice_state = 10065
unknown_application_command_permissions = 10066
unknown_stage = 10067
unknown_guild_member_verification_form = 10068

bots_not_allowed = 20001
only_bots_allowed = 20002
RPC_proxy_disallowed = 20003
explicit_content = 20009
account_scheduled_for_deletion = 20011
user_not_authorized_for_application = 20012
account_disabled = 20013
rate_limit_slowmode = 20016
team_ownership_required = 20018
rate_limit_announcement_message_edit = 20022
under_minimum_age = 20024
rate_limit_channel_write = 20028
name_contains_disallowed_word = 20031
guild_subscription_level_too_low = 20035

max_guilds = 30001 # 100
max_friends = 30001 # 10000
max_pins = 30003 # 50
max_recipients = 30004 # 10
max_roles = 30005 # 250
max_used_usernames = 30006
max_webhooks = 30007 # 10
max_emojis = 30008
max_reactions = 30010 # 20
max_channels = 30013 # 500
max_attachments = 30015 # 10
max_invites = 30016 # 1000
max_animated_emojis = 30018
max_guild_members = 30019
max_application_game_SKUs = 30021
max_teams = 30023
max_companies = 30025
not_enough_guild_members = 30029
max_guild_discovery_category = 30030 # 5
guild_has_template = 30031
max_application_commands = 30032
max_thread_participants = 30033
max_bans = 30035
max_ban_fetches = 30037

unauthorized = 40001
email_verification_required = 40002
rate_limit_private_channel_opening = 40003
send_message_temporarily_disabled = 40004
request_too_large = 40005
feature_disabled = 40006
user_banned = 40007
connection_rewoked = 40012
user_in_team = 40024
team_members_must_be_verified = 40026
team_invitation_accepted = 40027
delete_account_transfer_team_ownership = 40028
user_not_connected_to_voice = 40032
message_crossposted = 40033
user_identity_verification_processing = 40035
user_identity_verification_succeeded = 40036
application_name_used = 40041

missing_access = 50001
invalid_account_type = 50002
invalid_action_for_private_channel = 50003
widget_disabled = 50004
cannot_edit_message_of_other_user = 50005
cannot_create_empty_message = 50006
cannot_message_user = 50007
cannot_send_message_to_non_text_channel = 50008
channel_verification_level_too_high = 50009
oauth2_application_has_no_bot = 50010
oauth2_application_limit_reached = 50011
invalid_oauth2_state = 50012
missing_permissions = 50013
invalid_token = 50014
note_too_long = 50015
bulk_delete_amount_out_of_range = 50016
invalid_MFA_level = 50017
invalid_password = 50018
cannot_pin_message_in_different_channel = 50019
invite_code_invalid_or_taken = 50020
invalid_action_for_system_message = 50021
invalid_phone_number = 50022
invalid_client_id = 50023
invalid_action_for_this_channel_type = 50024
invalid_oauth2_access_token = 50025
missing_oauth2_scope = 50026
invalid_webhook_token = 50027
invalid_role = 50028
invalid_recipients = 50033
bulk_delete_message_too_old = 50034
invalid_form_body = 50035
cannot_add_user_to_guild_where_bot_is_not_in = 50036
invalid_API_version = 50041
invalid_asset = 50046
invalid_application_name = 50050
invalid_gift_redemption_owned = 50051
cannot_self_redeem_this_gift = 50054
invalid_message_type = 50068
payment_source_required_to_redeem_gift = 50070
cannot_delete_community_channel = 50074
invalid_sticker_sent = 50081
invalid_gift_redemption_subscription_managed = 100021
invalid_gift_redemption_subscription_incompatible = 100023
invalid_gift_redemption_invoice_open = 100024
invalid_action_for_archived_thread = 50083
invalid_thread_notification_setting = 50084
before_value_earlier_than_creation_time = 50085

MFA_enabled = 60001
MFA_disabled = 60002
MFA_required = 60003
MFA_unverified = 60004
MFA_invalid_secret = 60005
MFA_invalid_ticket = 60006
MFA_invalid_code = 60008
MFA_invalid_session = 60009

phone_number_unable_to_send = 70003

relationship_incoming_disabled = 80000
relationship_incoming_blocked = 80001
relationship_invalid_target_bot = 80002
relationship_invalid_target_self = 80003
relationship_invalid_discord_tag = 80004

reaction_blocked = 90001

authentication_required = 100029

listing_already_joined = 120000
listing_too_many_member = 120001
listing_join_blocked = 120002

resource_overloaded = 130000

stage_already_open = 150006

message_has_thread = 160004
thread_locked = 160005
max_active_threads = 160006
max_active_announcement_threads = 160007
