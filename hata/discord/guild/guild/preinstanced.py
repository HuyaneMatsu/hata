__all__ = (
    'ExplicitContentFilterLevel', 'GuildFeature', 'HubType', 'MfaLevel', 'MessageNotificationLevel', 'NsfwLevel',
    'VerificationLevel'
)

from warnings import warn

from scarletio import class_property, copy_docs, export

from ...bases import Preinstance as P, PreinstancedBase


class VerificationLevel(PreinstancedBase, value_type = int):
    """
    Represents Discord's verification level.
    
    Attributes
    ----------
    name : `str`
        The default name of the verification level.
    
    value : `int`
        The discord side identifier value of the verification level.
    
    Type Attributes
    ---------------
    Every predefined verification level can be accessed as type attribute as well:
    
    +-----------------------+-----------+-------+
    | Type attribute name   | name      | value |
    +=======================+===========+=======+
    | none                  | none      | 0     |
    +-----------------------+-----------+-------+
    | low                   | low       | 1     |
    +-----------------------+-----------+-------+
    | medium                | medium    | 2     |
    +-----------------------+-----------+-------+
    | high                  | high      | 3     |
    +-----------------------+-----------+-------+
    | extreme               | extreme   | 4     |
    +-----------------------+-----------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    low = P(1, 'low')
    medium = P(2, 'medium')
    high = P(3, 'high')
    extreme = P(4, 'extreme')



class ExplicitContentFilterLevel(PreinstancedBase, value_type = int):
    """
    Represents Discord's explicit_content filter level.
    
    Attributes
    ----------
    name : `str`
        The default name of the explicit content filter level.
    
    value : `int`
        The Discord side identifier value of the explicit content filter level.
    
    Class Attributes
    ----------------
    Every predefined explicit content filter level is also stored as a type attribute:
    
    +-----------------------+-----------+-------+
    | Type attribute name   | name      | value |
    +=======================+===========+=======+
    | disabled              | disabled  | 0     |
    +-----------------------+-----------+-------+
    | no_role               | no_role   | 1     |
    +-----------------------+-----------+-------+
    | everyone              | everyone  | 2     |
    +-----------------------+-----------+-------+
    """
    __slots__ = ()
    
    # predefined
    disabled = P(0, 'disabled')
    no_role = P(1, 'no_role')
    everyone = P(2, 'everyone')


@export
class GuildFeature(PreinstancedBase, value_type = str):
    """
    Repents an attached features of guilds.
    
    Attributes
    ----------
    name : `str`
        The guild feature's name.
    
    value : `str`
        The Discord side identifier value of the guild feature.
    
    Type Attributes
    ---------------
    Every predefined guild feature can be accessed as type attribute as well:
    
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | Type attribute name                           | name                                          | value                                                     |
    +===============================================+===============================================+===========================================================+
    | activity_list_disabled                        | activity list disabled                        | ACTIVITY_FEED_DISABLED_BY_USER                            |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | activity_list_enabled                         | activity list enabled                         | ACTIVITY_FEED_ENABLED_BY_USER                             |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | application_command_permissions_v2            | application command permissions v2            | APPLICATION_COMMAND_PERMISSIONS_V2                        |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | animated_banner                               | animated banner                               | ANIMATED_BANNER                                           |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | animated_icon                                 | animated icon                                 | ANIMATED_ICON                                             |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | announcement_channels                         | announcement channels                         | NEWS                                                      |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | attachment_size_limit_100_mb                  | attachment size limit 100 mb                  | MAX_FILE_SIZE_100_MB                                      |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | attachment_size_limit_50_mb                   | attachment size limit 50 mb                   | MAX_FILE_SIZE_50_MB                                       |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | audio_bitrate_128_kbps                        | audio bitrate 128 kbps                        | AUDIO_BITRATE_128_KBPS                                    |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | audio_bitrate_256_kbps                        | audio bitrate 256 kbps                        | AUDIO_BITRATE_256_KBPS                                    |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | audio_bitrate_384_kbps                        | audio bitrate 384 kbps                        | AUDIO_BITRATE_384_KBPS                                    |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | auto_moderation_enabled                       | auto moderation enabled                       | AUTO_MODERATION                                           |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | auto_moderation_trigger_user_profile          | auto moderation trigger user profile          | AUTOMOD_TRIGGER_USER_PROFILE                              |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | badge                                         | badge                                         | GUILD_TAGS                                                |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | banner                                        | banner                                        | BANNER                                                    |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | burst_reactions                               | burst reactions                               | BURST_REACTIONS                                           |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | channel_banners                               | channel banners                               | CHANNEL_BANNER                                            |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | channel_highlights                            | channel highlights                            | CHANNEL_HIGHLIGHTS                                        |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | channel_highlights_disabled                   | channel highlights disabled                   | CHANNEL_HIGHLIGHTS_DISABLED                               |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | channel_icon_emojis_generated                 | channel icon emojis generated                 | CHANNEL_ICON_EMOJIS_GENERATED                             |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | clyde_disabled                                | clyde disabled                                | CLYDE_DISABLED                                            |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | clyde_enabled                                 | clyde enabled                                 | CLYDE_ENABLED                                             |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | commerce                                      | commerce                                      | COMMERCE                                                  |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | community_experiment_large_gated              | community experiment large gated              | COMMUNITY_EXP_LARGE_GATED                                 |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | community_experiment_medium                   | community experiment medium                   | COMMUNITY_EXP_MEDIUM                                      |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | creator_accepted_new_terms                    | creator accepted new terms                    | CREATOR_ACCEPTED_NEW_TERMS                                |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | creator_store_page                            | creator store page                            | CREATOR_STORE_PAGE                                        |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | creator_monetizable                           | creator monetizable                           | CREATOR_MONETIZABLE                                       |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | creator_monetizable_disabled                  | creator monetizable disabled                  | CREATOR_MONETIZABLE_DISABLED                              |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | creator_monetizable_owner_onboarding          | creator monetizable owner onboarding          | CREATOR_MONETIZABLE_PENDING_NEW_OWNER_ONBOARDING          |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | creator_monetizable_premium_service           | creator monetizable premium service           | CREATOR_MONETIZABLE_WHITEGLOVE                            |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | creator_monetizable_restricted                | creator monetizable restricted                | CREATOR_MONETIZABLE_RESTRICTED                            |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | creator_monetizable_temporarily               | creator monetizable temporarily               | CREATOR_MONETIZABLE_PROVISIONAL                           |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | community                                     | community                                     | COMMUNITY                                                 |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | developer_support_guild                       | developer support guild                       | DEVELOPER_SUPPORT_SERVER                                  |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | discoverable                                  | discoverable                                  | DISCOVERABLE                                              |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | discoverable_disabled                         | discoverable disabled                         | DISCOVERABLE_DISABLED                                     |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | discoverable_enabled_before                   | discoverable enabled before                   | ENABLED_DISCOVERABLE_BEFORE                               |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | embedded_activities_experiment                | embedded activities experiment                | EXPOSED_TO_ACTIVITIES_WTP_EXPERIMENT                      |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | embedded_activities_had_early_access          | embedded activities had early access          | HAD_EARLY_ACTIVITIES_ACCESS                               |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | featurable                                    | featurable                                    | FEATURABLE                                                |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | guests_enabled                                | guests enabled                                | GUESTS_ENABLED                                            |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | guide_screen_enabled                          | guide screen enabled                          | GUILD_SERVER_GUIDE                                        |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | has_directory_entry                           | has directory entry                           | HAS_DIRECTORY_ENTRY                                       |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | home_deprecation                              | home deprecation                              | GUILD_HOME_DEPRECATION_OVERRIDE                           |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | home_override                                 | home override                                 | GUILD_HOME_OVERRIDE                                       |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | home_test                                     | home test                                     | GUILD_HOME_TEST                                           |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | hub                                           | hub                                           | HUB                                                       |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | internal_employee_only                        | internal employee only                        | INTERNAL_EMPLOYEE_ONLY                                    |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | invite_splash                                 | invite splash                                 | INVITE_SPLASH                                             |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | invites_disabled                              | invites disabled                              | INVITES_DISABLED                                          |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | levelless_boosting                            | levelless boosting                            | TIERLESS_BOOSTING                                         |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | levelless_boosting_system_messages            | levelless boosting system messages            | TIERLESS_BOOSTING_SYSTEM_MESSAGE                          |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | linked_to_hub                                 | linked to hub                                 | LINKED_TO_HUB                                             |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | marketplaces_connection_roles                 | marketplaces connection roles                 | MARKETPLACES_CONNECTION_ROLES                             |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | member_list_disabled                          | member list disabled                          | MEMBER_LIST_DISABLED                                      |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | moderation_survey_reports                     | moderation survey reports                     | REPORT_TO_MOD_SURVEY                                      |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | moderation_experience_non_community_enabled   | moderation experience non community enabled   | ENABLED_MODERATION_EXPERIENCE_FOR_NON_COMMUNITY           |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | monetization_enabled                          | monetization enabled                          | MONETIZATION_ENABLED                                      |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | more_emoji                                    | more emoji                                    | MORE_EMOJI                                                |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | more_sticker                                  | more sticker                                  | MORE_STICKERS                                             |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | new_thread_permissions                        | new thread permissions                        | NEW_THREAD_PERMISSIONS                                    |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | onboarding_enabled                            | onboarding enabled                            | GUILD_ONBOARDING                                          |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | onboarding_ever_enabled                       | onboarding ever enabled                       | GUILD_ONBOARDING_EVER_ENABLED                             |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | onboarding_has_prompts                        | onboarding has prompts                        | GUILD_ONBOARDING_HAS_PROMPTS                              |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | partnered                                     | partnered                                     | PARTNERED                                                 |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | preview_enabled                               | preview enabled                               | PREVIEW_ENABLED                                           |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | private_threads                               | private threads                               | PRIVATE_THREADS                                           |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | public                                        | public                                        | PUBLIC                                                    |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | public_disabled                               | public disabled                               | PUBLIC_DISABLED                                           |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | raid_alerts_disabled                          | raid alerts disabled                          | RAID_ALERTS_DISABLED                                      |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | raid_alerts_enabled                           | raid alerts enabled                           | RAID_ALERTS_ENABLED                                       |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | raid_alerts_non_community                     | raid alerts non community                     | NON_COMMUNITY_RAID_ALERTS                                 |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | relay_enabled                                 | relay enabled                                 | RELAY_ENABLED                                             |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | role_colors_enhanced                          | role colors enhanced                          | ENHANCED_ROLE_COLORS                                      |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | role_icons                                    | role icons                                    | ROLE_ICONS                                                |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | role_subscriptions_enabled                    | role subscriptions enabled                    | ROLE_SUBSCRIPTIONS_ENABLED                                |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | role_subscriptions_purchasable                | role subscriptions purchasable                | ROLE_SUBSCRIPTIONS_AVAILABLE_FOR_PURCHASE                 |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | soundboard_enabled                            | soundboard enabled                            | SOUNDBOARD                                                |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | shard                                         | shard                                         | SHARD                                                     |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | stage_channel_150_viewers                     | stage channel 150 viewers                     | STAGE_CHANNEL_VIEWERS_150                                 |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | stage_channel_300_viewers                     | stage channel 300 viewers                     | STAGE_CHANNEL_VIEWERS_300                                 |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | stage_channel_50_viewers                      | stage channel 50 viewers                      | STAGE_CHANNEL_VIEWERS_50                                  |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | summaries_disabled_by_user                    | summaries disabled by user                    | SUMMARIES_DISABLED_BY_USER                                |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | summaries_enabled                             | summaries enabled                             | SUMMARIES_ENABLED                                         |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | summaries_enabled_by_user                     | summaries enabled by user                     | SUMMARIES_ENABLED_BY_USER                                 |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | summaries_enabled_global_access               | summaries enabled global access               | SUMMARIES_ENABLED_GA                                      |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | text_in_stage_enabled                         | text in stage enabled                         | TEXT_IN_STAGE_ENABLED                                     |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | text_in_voice_enabled                         | text in voice enabled                         | TEXT_IN_VOICE_ENABLED                                     |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | thread_archive_seven_day                      | thread archive seven day                      | SEVEN_DAY_THREAD_ARCHIVE                                  |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | thread_archive_three_day                      | thread archive three day                      | THREE_DAY_THREAD_ARCHIVE                                  |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | threads_enabled                               | threads enabled                               | THREADS_ENABLED                                           |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | threads_enabled_testing                       | threads enabled testing                       | THREADS_ENABLED_TESTING                                   |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | thread_limit_increased                        | thread limit increased                        | INCREASED_THREAD_LIMIT                                    |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | ticket_events_enabled                         | ticket events enabled                         | TICKETED_EVENTS_ENABLED                                   |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | users_screen_enabled                          | users screen enabled                          | MEMBER_PROFILES                                           |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | vanity_invite                                 | vanity invite                                 | VANITY_URL                                                |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | verification_manual_approval                  | verification manual approval                  | MEMBER_VERIFICATION_MANUAL_APPROVAL                       |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | verification_screen_enabled                   | verification screen enabled                   | MEMBER_VERIFICATION_GATE_ENABLED                          |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | verified                                      | verified                                      | VERIFIED                                                  |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | video_bitrate_enhanced                        | video bitrate enhanced                        | VIDEO_BITRATE_ENHANCED                                    |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | video_quality_1080_px_60_fps                  | video quality 1080 px 60 fps                  | VIDEO_QUALITY_1080_60FPS                                  |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | video_quality_720_px_60_fps                   | video quality 720 px 60 fps                   | VIDEO_QUALITY_720_60FPS                                   |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | vip_voice_regions                             | vip voice regions                             | VIP_REGIONS                                               |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | web_page                                      | web page                                      | GUILD_WEB_PAGE_VANITY_URL                                 |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    | welcome_screen_enabled                        | welcome screen enabled                        | WELCOME_SCREEN_ENABLED                                    |
    +-----------------------------------------------+-----------------------------------------------+-----------------------------------------------------------+
    """
    __slots__ = ()
    
    
    @copy_docs(PreinstancedBase.__new__)
    def __new__(cls, value, name = None):
        if name is None:
            name = value.casefold().replace('_', ' ')
        
        return PreinstancedBase.__new__(cls, value, name)
    
    
    # predefined
    activity_list_disabled = P('ACTIVITY_FEED_DISABLED_BY_USER', 'activity list disabled')
    activity_list_enabled = P('ACTIVITY_FEED_ENABLED_BY_USER', 'activity list enabled')
    application_command_permissions_v2 = P('APPLICATION_COMMAND_PERMISSIONS_V2', 'application command permissions v2')
    animated_banner = P('ANIMATED_BANNER', 'animated banner')
    animated_icon = P('ANIMATED_ICON', 'animated icon')
    announcement_channels = P('NEWS', 'announcement channels')
    attachment_size_limit_100_mb = P('MAX_FILE_SIZE_100_MB', 'attachment size limit 100 mb')
    attachment_size_limit_50_mb = P('MAX_FILE_SIZE_50_MB', 'attachment size limit 50 mb')
    audio_bitrate_128_kbps = ('AUDIO_BITRATE_128_KBPS', 'audio bitrate 128 kbps')
    audio_bitrate_256_kbps = ('AUDIO_BITRATE_256_KBPS', 'audio bitrate 256 kbps')
    audio_bitrate_384_kbps = ('AUDIO_BITRATE_384_KBPS', 'audio bitrate 384 kbps')
    auto_moderation_enabled = P('AUTO_MODERATION', 'auto moderation enabled')
    auto_moderation_trigger_user_profile = P('AUTOMOD_TRIGGER_USER_PROFILE', 'auto moderation trigger user profile')
    badge = P('GUILD_TAGS', 'badge')
    banner = P('BANNER', 'banner')
    burst_reactions = P('BURST_REACTIONS', 'burst reactions')
    channel_banners = P('CHANNEL_BANNER', 'channel banners')
    channel_highlights = P('CHANNEL_HIGHLIGHTS', 'channel highlights')
    channel_highlights_disabled = P('CHANNEL_HIGHLIGHTS_DISABLED', 'channel highlights disabled')
    channel_icon_emojis_generated = P('CHANNEL_ICON_EMOJIS_GENERATED', 'channel icon emojis generated')
    clyde_disabled = P('CLYDE_DISABLED', 'clyde disabled')
    clyde_enabled = P('CLYDE_ENABLED', 'clyde enabled')
    commerce = P('COMMERCE', 'commerce')
    community_experiment_large_gated = P('COMMUNITY_EXP_LARGE_GATED', 'community experiment large gated')
    community_experiment_medium = P('COMMUNITY_EXP_MEDIUM', 'community experiment medium')
    creator_accepted_new_terms = P('CREATOR_ACCEPTED_NEW_TERMS', 'creator accepted new terms')
    creator_store_page = P('CREATOR_STORE_PAGE', 'creator store page')
    creator_monetizable = P('CREATOR_MONETIZABLE', 'creator monetizable')
    creator_monetizable_disabled = P('CREATOR_MONETIZABLE_DISABLED', 'creator monetizable disabled')
    creator_monetizable_owner_onboarding = P(
        'CREATOR_MONETIZABLE_PENDING_NEW_OWNER_ONBOARDING', 'creator monetizable owner onboarding'
    )
    creator_monetizable_premium_service = P('CREATOR_MONETIZABLE_WHITEGLOVE', 'creator monetizable premium service')
    creator_monetizable_restricted = P('CREATOR_MONETIZABLE_RESTRICTED', 'creator monetizable restricted')
    creator_monetizable_temporarily = P('CREATOR_MONETIZABLE_PROVISIONAL', 'creator monetizable temporarily')
    community = P('COMMUNITY', 'community')
    developer_support_guild = P('DEVELOPER_SUPPORT_SERVER', 'developer support guild')
    discoverable = P('DISCOVERABLE', 'discoverable')
    discoverable_disabled = P('DISCOVERABLE_DISABLED', 'discoverable disabled')
    embedded_activities_experiment = P('EXPOSED_TO_ACTIVITIES_WTP_EXPERIMENT', 'embedded activities experiment')
    embedded_activities_had_early_access = P('HAD_EARLY_ACTIVITIES_ACCESS', 'embedded activities had early access')
    discoverable_enabled_before = P('ENABLED_DISCOVERABLE_BEFORE', 'discoverable enabled before')
    featurable = P('FEATURABLE', 'featurable')
    guests_enabled = P('GUESTS_ENABLED', 'guests enabled')
    guide_screen_enabled = P('GUILD_SERVER_GUIDE', 'guide screen enabled')
    has_directory_entry = P('HAS_DIRECTORY_ENTRY', 'has directory entry')
    home_deprecation = P('GUILD_HOME_DEPRECATION_OVERRIDE', 'home deprecation')
    home_override = P('GUILD_HOME_OVERRIDE', 'home override')
    home_test = P('GUILD_HOME_TEST', 'home test')
    hub = P('HUB', 'hub')
    internal_employee_only = P('INTERNAL_EMPLOYEE_ONLY', 'internal employee only')
    invite_splash = P('INVITE_SPLASH', 'invite splash')
    invites_disabled = P('INVITES_DISABLED', 'invites disabled')
    levelless_boosting = P('TIERLESS_BOOSTING', 'levelless boosting')
    levelless_boosting_system_messages = P('TIERLESS_BOOSTING_SYSTEM_MESSAGE', 'levelless boosting system messages')
    linked_to_hub = P('LINKED_TO_HUB', 'linked to hub')
    marketplaces_connection_roles = P('MARKETPLACES_CONNECTION_ROLES', 'marketplaces connection roles')
    member_list_disabled = P('MEMBER_LIST_DISABLED', 'member list disabled')
    moderation_survey_reports = P('REPORT_TO_MOD_SURVEY', 'moderation survey reports')
    moderation_experience_non_community_enabled = P(
        'ENABLED_MODERATION_EXPERIENCE_FOR_NON_COMMUNITY',
        'moderation experience non community enabled',
    )
    monetization_enabled = P('MONETIZATION_ENABLED', 'monetization enabled')
    more_emoji = P('MORE_EMOJI', 'more emoji')
    more_sticker = P('MORE_STICKERS', 'more sticker')
    new_thread_permissions = P('NEW_THREAD_PERMISSIONS', 'new thread permissions')
    onboarding_enabled = P('GUILD_ONBOARDING', 'onboarding enabled')
    onboarding_ever_enabled  = P('GUILD_ONBOARDING_EVER_ENABLED', 'onboarding ever enabled')
    onboarding_has_prompts  = P('GUILD_ONBOARDING_HAS_PROMPTS', 'onboarding has prompts')
    partnered = P('PARTNERED', 'partnered')
    preview_enabled = P('PREVIEW_ENABLED', 'preview enabled')
    private_threads = P('PRIVATE_THREADS', 'private threads')
    public = P('PUBLIC', 'public')
    public_disabled = P('PUBLIC_DISABLED', 'public disabled')
    raid_alerts_disabled = P('RAID_ALERTS_DISABLED', 'raid alerts disabled')
    raid_alerts_enabled = P('RAID_ALERTS_ENABLED', 'raid alerts enabled')
    raid_alerts_non_community = P('NON_COMMUNITY_RAID_ALERTS', 'raid alerts non community')
    relay_enabled = P('RELAY_ENABLED', 'relay enabled')
    role_colors_enhanced = P('ENHANCED_ROLE_COLORS', 'role colors enhanced')
    role_icons = P('ROLE_ICONS', 'role icons')
    role_subscriptions_enabled = P('ROLE_SUBSCRIPTIONS_ENABLED', 'role subscriptions enabled')
    role_subscriptions_purchasable = P('ROLE_SUBSCRIPTIONS_AVAILABLE_FOR_PURCHASE', 'role subscriptions purchasable')
    soundboard_enabled = P('SOUNDBOARD', 'soundboard enabled')
    shard = P('SHARD', 'shard')
    stage_channel_150_viewers = P('STAGE_CHANNEL_VIEWERS_150', 'stage channel 150 viewers')
    stage_channel_300_viewers = P('STAGE_CHANNEL_VIEWERS_300', 'stage channel 300 viewers')
    stage_channel_50_viewers = P('STAGE_CHANNEL_VIEWERS_50', 'stage channel 50 viewers')
    summaries_disabled_by_user = P('SUMMARIES_DISABLED_BY_USER', 'summaries disabled by user')
    summaries_enabled = P('SUMMARIES_ENABLED', 'summaries enabled')
    summaries_enabled_by_user = P('SUMMARIES_ENABLED_BY_USER', 'summaries enabled by user')
    summaries_enabled_global_access = P('SUMMARIES_ENABLED_GA', 'summaries enabled global access')
    text_in_stage_enabled = P('TEXT_IN_STAGE_ENABLED', 'text in stage enabled')
    text_in_voice_enabled = P('TEXT_IN_VOICE_ENABLED', 'text in voice enabled')
    thread_archive_seven_day = P('SEVEN_DAY_THREAD_ARCHIVE', 'thread archive seven day')
    thread_archive_three_day = P('THREE_DAY_THREAD_ARCHIVE', 'thread archive three day')
    threads_enabled = P('THREADS_ENABLED', 'threads enabled')
    threads_enabled_testing = P('THREADS_ENABLED_TESTING', 'threads enabled testing')
    thread_limit_increased = P('INCREASED_THREAD_LIMIT', 'thread limit increased')
    ticket_events_enabled = P('TICKETED_EVENTS_ENABLED', 'ticket events enabled')
    users_screen_enabled = P('MEMBER_PROFILES', 'users screen enabled')
    vanity_invite = P('VANITY_URL', 'vanity invite')
    verification_manual_approval = P('MEMBER_VERIFICATION_MANUAL_APPROVAL', 'verification manual approval')
    verification_screen_enabled = P('MEMBER_VERIFICATION_GATE_ENABLED', 'verification screen enabled')
    verified = P('VERIFIED', 'verified')
    video_bitrate_enhanced = P('VIDEO_BITRATE_ENHANCED', 'video bitrate enhanced')
    video_quality_1080_px_60_fps = P('VIDEO_QUALITY_1080_60FPS', 'video quality 1080 px 60 fps')
    video_quality_720_px_60_fps = P('VIDEO_QUALITY_720_60FPS', 'video quality 720 px 60 fps')
    vip_voice_regions = P('VIP_REGIONS', 'vip voice regions')
    web_page = P('GUILD_WEB_PAGE_VANITY_URL', 'web page')
    welcome_screen_enabled = P('WELCOME_SCREEN_ENABLED', 'welcome screen enabled')


    @class_property
    def role_subscription_purchasable(cls):
        """
        Deprecated and will be removed in 2026 jan. Use `.role_subscriptions_purchasable` instead.
        """
        warn(
            (
                f'`{cls.__name__}.role_subscription_purchasable` is deprecated and will be removed in 2026 Jan. '
                f'Use `.role_subscriptions_purchasable` instead.'
            ),
            FutureWarning,
            stacklevel = 3,
        )
        return cls.role_subscriptions_purchasable






class NsfwLevel(PreinstancedBase, value_type = int):
    """
    Represents a guild's nsfw level.
    
    Attributes
    ----------
    name : `str`
        The name of the nsfw filter level.
    
    value : `int`
        The identifier value the nsfw filter level
    
    Type Attributes
    ---------------
    Every predefined nsfw level can be accessed as type attribute as well:
    
    +-----------------------+-------------------+-------+-------+
    | Type attribute name   | Name              | Value | nsfw  |
    +=======================+===================+=======+=======+
    | none                  | none              | 0     | False |
    +-----------------------+-------------------+-------+-------+
    | explicit              | explicit          | 1     | True  |
    +-----------------------+-------------------+-------+-------+
    | safe                  | safe              | 2     | False |
    +-----------------------+-------------------+-------+-------+
    | age_restricted        | age_restricted    | 3     | True  |
    +-----------------------+-------------------+-------+-------+
    """
    __slots__ = ('nsfw', )
    
    def __new__(cls, value, name = None, nsfw = True):
        """
        Creates a new nsfw level instance.
        
        Parameters
        ----------
        value : `int`
            The value of the nsfw level.
        
        name : `None | str` = `None`, Optional
            The nsfw level name.
        
        nsfw : `bool` = `False`, Optional
            Whether the nsfw level refers to being actually nsfw.
        """
        self = PreinstancedBase.__new__(cls, value, name)
        self.nsfw = nsfw
        return self
    
    
    @copy_docs(PreinstancedBase._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts):
        repr_parts.append(', nsfw = ')
        repr_parts.append(repr(self.nsfw))
    
    
    none = P(0, 'none', False)
    explicit = P(1, 'explicit', True)
    safe = P(2, 'safe', False)
    age_restricted = P(3, 'age_restricted', True)


class MessageNotificationLevel(PreinstancedBase, value_type = int):
    """
    Represents the message notification level of a ``Guild``.
    Only used to represents its default message notification level.
    
    Attributes
    ----------
    name : `str`
        The default name of the message notification level.
    
    value : `int`
        The Discord side identifier value of the message notification level.
    
    Type Attributes
    ---------------
    Each predefined message notification level can also be accessed as a type attribute:
    
    +-----------------------+---------------+-------+
    | Type attribute name   | name          | value |
    +=======================+===============+=======+
    | all_messages          | all messages  | 0     |
    +-----------------------+---------------+-------+
    | only_mentions         | only mentions | 1     |
    +-----------------------+---------------+-------+
    | no_message            | no messages   | 2     |
    +-----------------------+---------------+-------+
    | none                  | none          | 3     |
    +-----------------------+---------------+-------+
    """
    __slots__ = ()
    
    # predefined
    all_messages = P(0, 'all messages')
    only_mentions = P(1, 'only mentions')
    no_messages = P(2, 'no messages')
    none = P(3, 'none')


class MfaLevel(PreinstancedBase, value_type = int):
    """
    Represents Discord's Multi-Factor Authentication's levels.
    
    Attributes
    ----------
    name : `str`
        The default name of the mfa level.
    
    value : `int`
        The Discord side identifier value of the Mfa level.
    
    Type Attributes
    ----------------
    Each predefined mfa can also be accessed as type attribute:
    
    +-----------------------+-----------+-------+
    | Type attribute name   | name      | value |
    +=======================+===========+=======+
    | none                  | none      | 0     |
    +-----------------------+-----------+-------+
    | elevated              | elevated  | 1     |
    +-----------------------+-----------+-------+
    """
    __slots__ = ()
    
    # Predefined
    none = P(0, 'none')
    elevated = P(1, 'elevated')


class VerificationFieldPlatform(PreinstancedBase, value_type = str):
    """
    Represents the verification field platform of a verification screen.
    
    Attributes
    ----------
    name : `str`
        The name of the verification field platform.
    
    value : `str`
        The Discord side identifier value of the verification field platform.
    
    Type Attributes
    ---------------
    Every predefined verification field platform can be accessed as type attribute as well:
    
    +-----------------------+-----------+-----------+
    | Type attribute name   | Name      | Value     |
    +=======================+===========+===========+
    | email                 | email     | email     |
    +-----------------------+-----------+-----------+
    | phone                 | phone     | phone     |
    +-----------------------+-----------+-----------+
    """
    __slots__ = ()
    
    email = P('email', 'email')
    phone = P('phone', 'phone')


class HubType(PreinstancedBase, value_type = int):
    """
    Represents Discord's guild's hub type.
    
    Attributes
    ----------
    name : `str`
        The default name of the hub type
    
    value : `int`
        The Discord side identifier value of the hub type
    
    Type Attributes
    ----------------
    Each predefined hub type can also be accessed as type attribute:
    
    +-----------------------+---------------+-------+
    | Type attribute name   | name          | value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | high_school           | high school   | 1     |
    +-----------------------+---------------+-------+
    | college               | college       | 2     |
    +-----------------------+---------------+-------+
    """
    __slots__ = ()
    
    # Predefined
    none = P(0, 'none')
    high_school = P(1, 'high school')
    college = P(2, 'college')
