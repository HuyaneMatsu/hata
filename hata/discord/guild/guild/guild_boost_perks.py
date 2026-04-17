__all__ = ()

from warnings import warn

from scarletio import RichAttributeErrorBaseType

from .preinstanced import GuildFeature


class GuildBoostPerks(RichAttributeErrorBaseType):
    """
    Represents the boost perk that a user gets for each boost level.
    
    Attributes
    ----------
    attachment_size_limit : `int`
        The maximal size in bytes of each attachment that can be uploaded to the guild's channels.
    
    bitrate_limit : `int`
        The maximal bit rate usable in voice channel.
    
    concurrent_activities : `int`
        The maximal amount of concurrent embedded activities. Set as `0` if unlimited.
    
    emoji_limit : `int`
        The maximal amount of emojis.
    
    features : `None`, `tuple` of ``GuildFeature``
        The guild features acquired with the boost level.
    
    level : `int`
        The boost perks' level.
    
    screen_share_frame_rate : `int`
        The maximal frame rate usable when screen sharing.
    
    screen_share_resolution : `str`
        The maximal screen resolution's name when screen sharing.
    
    soundboard_sound_limit : `int`
        The maximal amount of sound board sounds.
    
    stage_channel_viewer_limit : `int`
        The amount of viewers the stage channels can have in the guild.
    
    sticker_limit : `int`
        The maximal amount of stickers the guild can have.
    """
    __slots__ = (
        'attachment_size_limit', 'bitrate_limit', 'concurrent_activities', 'emoji_limit', 'features', 'level',
        'screen_share_frame_rate', 'screen_share_resolution', 'soundboard_sound_limit', 'stage_channel_viewer_limit',
        'sticker_limit'
    )
    
    def __new__(
        cls,
        attachment_size_limit,
        bitrate_limit,
        concurrent_activities,
        emoji_limit,
        features,
        level,
        screen_share_frame_rate,
        screen_share_resolution,
        soundboard_sound_limit,
        stage_channel_viewer_limit,
        sticker_limit,
    ):
        """
        Creates a new guild boost perks instance.
        
        Parameters
        ----------
        attachment_size_limit : `int`
            The maximal size in bytes of each attachment that can be uploaded to the guild's channels.
        
        bitrate_limit : `int`
            The maximal bit rate usable in voice channel.
        
        concurrent_activities : `int`
            The maximal amount of concurrent embedded activities. Set as `0` if unlimited.
        
        emoji_limit : `int`
            The maximal amount of emojis.
        
        features : `None`, `tuple<GuildFeature>`
            The guild features acquired with the boost level.
        
        level : `int`
            The boost perks' level.
        
        screen_share_frame_rate : `int`
            The maximal frame rate usable when screen sharing.
        
        screen_share_resolution : `str`
            The maximal screen resolution's name when screen sharing.
        
        soundboard_sound_limit : `int`
            The maximal amount of sound board sounds.
        
        stage_channel_viewer_limit : `int`
            The amount of viewers the stage channels can have in the guild.
        
        sticker_limit : `int`
            The maximal amount of stickers the guild can have.
        """
        self = object.__new__(cls)
        self.attachment_size_limit = attachment_size_limit
        self.bitrate_limit = bitrate_limit
        self.concurrent_activities = concurrent_activities
        self.emoji_limit = emoji_limit
        self.features = features
        self.level = level
        self.screen_share_frame_rate = screen_share_frame_rate
        self.screen_share_resolution = screen_share_resolution
        self.soundboard_sound_limit = soundboard_sound_limit
        self.stage_channel_viewer_limit = stage_channel_viewer_limit
        self.sticker_limit = sticker_limit
        return self
    
    
    def __repr__(self):
        """Returns the guild premium perk's representation."""
        return f'{type(self).__name__} level = {self.level!r}>'
    
    
    def iter_features(self):
        """
        Iterates over the features of the guild premium perk.
        
        This method is an iterable generator.
        
        Yields
        ------
        feature : ``GuildFeature``
        """
        features = self.features
        if (features is not None):
            yield from features
    
    
    @property
    def upload_limit(self):
        """
        Deprecated and will be removed in 2025 November. Please use `.attachment_size_limit` instead.
        """
        warn(
            (
                f'`{type(self).__name__}.upload_limit` is deprecated and will be removed in 2025 November. '
                f'Please use `.attachment_size_limit` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        return self.boost_perks.attachment_size_limit
    
    
    @property
    def tier(self):
        """
        Deprecated and will be removed in 2025 November. Please use `.level` instead.
        """
        warn(
            (
                f'`{type(self).__name__}.tier` is deprecated and will be removed in 2025 November. '
                f'Please use `.level` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        return self.premium_perks.level


LEVEL_0 = GuildBoostPerks(
    8388608,
    96000,
    2,
    50,
    None,
    0,
    30,
    '720p',
    8,
    50,
    5,
)


LEVEL_1 = GuildBoostPerks(
    26214400,
    128000,
    3,
    100,
    (
        GuildFeature.icon_animated,
        GuildFeature.invite_splash,
    ),
    1,
    60,
    '720p',
    24,
    50,
    15,
)


LEVEL_2 = GuildBoostPerks(
    52428800,
    256000,
    5,
    150,
    (
        GuildFeature.banner,
        GuildFeature.icon_animated,
        GuildFeature.invite_splash,
        GuildFeature.role_icons,
    ),
    2,
    60,
    '1080p',
    36,
    150,
    30,
)


LEVEL_3 = GuildBoostPerks(
    104857600,
    384000,
    0,
    250,
    (
        GuildFeature.banner,
        GuildFeature.banner_animated,
        GuildFeature.icon_animated,
        GuildFeature.invite_splash,
        GuildFeature.invite_vanity_url,
        GuildFeature.role_icons,
    ),
    3,
    60,
    '1080p',
    48,
    300,
    60,
)


LEVELS = {
    0: LEVEL_0,
    1: LEVEL_1,
    2: LEVEL_2,
    3: LEVEL_3,
}

LEVEL_MAX = LEVEL_3
