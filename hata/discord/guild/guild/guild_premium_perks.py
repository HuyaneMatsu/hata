__all__ = ()

from scarletio import RichAttributeErrorBaseType

from .preinstanced import GuildFeature


class GuildPremiumPerks(RichAttributeErrorBaseType):
    """
    Represents the premium perk that a user gets for each boost tier.
    
    Attributes
    ----------
    bitrate_limit : `int`
        The maximal bit rate usable in voice channel.
    concurrent_activities : `int`
        The maximal amount of concurrent embedded activities. Set as `0` if unlimited.
    emoji_limit : `int`
        The maximal amount of emojis.
    features : `None`, `tuple` of ``GuildFeature``
        The guild features acquired with the premium tier.
    screen_share_frame_rate : `int`
        The maximal frame rate usable when screen sharing.
    screen_share_resolution : `str`
        The maximal screen resolution's name when screen sharing.
    sound_limit : `int`
        The maximal amount of sound board sounds.
    sticker_limit : `int`
        The maximal amount of stickers the guild can have.
    tier : `int`
        The premium tier's level.
    upload_limit : `int`
        The maximal upload limit in bytes.
    """
    __slots__ = (
        'bitrate_limit', 'concurrent_activities', 'emoji_limit', 'features', 'screen_share_frame_rate',
        'screen_share_resolution', 'sound_limit', 'sticker_limit', 'tier', 'upload_limit', 
    )
    
    def __new__(
        cls,
        bitrate_limit,
        concurrent_activities,
        emoji_limit,
        features,
        screen_share_frame_rate,
        screen_share_resolution,
        sound_limit,
        sticker_limit,
        tier,
        upload_limit,
    ):
        """
        Creates a new guild premium tier perk.
        
        Parameters
        ----------
        bitrate_limit : `int`
            The maximal bit rate usable in voice channel.
        concurrent_activities : `int`
            The maximal amount of concurrent embedded activities. Set as `0` if unlimited.
        emoji_limit : `int`
            The maximal amount of emojis.
        features : `None`, `tuple` of ``GuildFeature``
            The guild features acquired with the premium tier.
        screen_share_frame_rate : `int`
            The maximal frame rate usable when screen sharing.
        screen_share_resolution : `str`
            The maximal screen resolution's name when screen sharing.
        sound_limit : `int`
            The maximal amount of sound board sounds.
        sticker_limit : `int`
            The maximal amount of stickers the guild can have.
        tier : `int`
            The premium tier's level.
        upload_limit : `int`
            The maximal upload limit in bytes.
        """
        self = object.__new__(cls)
        self.bitrate_limit = bitrate_limit
        self.concurrent_activities = concurrent_activities
        self.emoji_limit = emoji_limit
        self.features = features
        self.screen_share_frame_rate = screen_share_frame_rate
        self.screen_share_resolution = screen_share_resolution
        self.sound_limit = sound_limit
        self.sticker_limit = sticker_limit
        self.tier = tier
        self.upload_limit = upload_limit
        return self
    
    
    def __repr__(self):
        """Returns the guild premium perk's representation."""
        return f'{self.__class__.__name__} tier = {self.tier!r}>'
    
    
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


TIER_0 = GuildPremiumPerks(
    96000,
    2,
    50,
    None,
    30,
    '720p',
    8,
    5,
    0,
    26214400,
)


TIER_1 = GuildPremiumPerks(
    128000,
    3,
    100,
    (
        GuildFeature.animated_icon,
        GuildFeature.invite_splash,
    ),
    60,
    '720p',
    24,
    15,
    1,
    8388608,
)


TIER_2 = GuildPremiumPerks(
    256000,
    5,
    150,
    (
        GuildFeature.animated_icon,
        GuildFeature.banner,
        GuildFeature.invite_splash,
        GuildFeature.role_icons,
    ),
    60,
    '1080p',
    36,
    30,
    2,
    52428800,
)


TIER_3 = GuildPremiumPerks(
    384000,
    0,
    250,
    (
        GuildFeature.animated_banner,
        GuildFeature.animated_icon,
        GuildFeature.banner,
        GuildFeature.invite_splash,
        GuildFeature.role_icons,
        GuildFeature.vanity_invite,
    ),
    60,
    '1080p',
    48,
    60,
    3,
    104857600,
)


TIERS = {
    0: TIER_0,
    1: TIER_1,
    2: TIER_2,
    3: TIER_3,
}

TIER_MAX = TIER_3
