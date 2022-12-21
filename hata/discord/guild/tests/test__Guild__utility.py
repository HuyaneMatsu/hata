import vampytest

from ...emoji import Emoji
from ...sticker import Sticker, StickerFormat

from ..emoji_counts import EmojiCounts
from ..guild import Guild
from ..guild_premium_perks import GuildPremiumPerks, TIER_0, TIER_MAX
from ..preinstanced import GuildFeature, NsfwLevel
from ..sticker_counts import StickerCounts


def test__Guild__nsfw__0():
    """
    Tests whether `Guild.nsfw` returns the correct value.
    
    Case: `NsfwLevel.safe`.
    """
    nsfw_level = NsfwLevel.safe
    guild = Guild.precreate(202208270000, nsfw_level = nsfw_level)
    
    vampytest.assert_eq(guild.nsfw, nsfw_level.nsfw)


def test__Guild__nsfw__1():
    """
    Tests whether `Guild.nsfw` returns the correct value.
    
    Case: `NsfwLevel.explicit`.
    """
    nsfw_level = NsfwLevel.explicit
    guild = Guild.precreate(202208270001, nsfw_level = nsfw_level)
    
    vampytest.assert_eq(guild.nsfw, nsfw_level.nsfw)


def test__Guild__has_feature():
    """
    Tests whether ``Guild.has_feature`` works as intended.
    """
    feature = GuildFeature.animated_icon
    for guild, expected_output in (
        (Guild.precreate(202212190038, features = []), False),
        (Guild.precreate(202212200020, features = [GuildFeature.animated_banner]), False),
        (Guild.precreate(202212200021, features = [feature]), True),
        (Guild.precreate(202212200022, features = [GuildFeature.animated_banner, feature]), True),
    ):
        vampytest.assert_eq(guild.has_feature(feature), expected_output)


def test__Guild__premium_perks():
    """
    Tests whether ``Guild.premium_perks`` works as intended.
    """
    premium_tier = 2
    
    guild = Guild.precreate(202212190039, premium_tier = premium_tier)
    premium_perks = guild.premium_perks
    vampytest.assert_instance(premium_perks, GuildPremiumPerks)
    vampytest.assert_eq(premium_perks.tier, premium_tier)


def test__Guild__emoji_limit():
    """
    Tests whether ``Guild.emoji_limit`` works as intended.
    """
    for guild, expected_value in (
        (Guild.precreate(202212200000, premium_tier = 0), TIER_0.emoji_limit),
        (Guild.precreate(202212200001, premium_tier = TIER_MAX.tier), TIER_MAX.emoji_limit),
        (Guild.precreate(202212200002, premium_tier = 1, features = [GuildFeature.more_emoji]), 200),
        (
            Guild.precreate(202212200003, premium_tier = TIER_MAX.tier, features = [GuildFeature.more_emoji]),
            TIER_MAX.emoji_limit,
        ),
    ):
        vampytest.assert_eq(guild.emoji_limit, expected_value)


def test__Guild__bitrate_limit():
    """
    Tests whether ``Guild.bitrate_limit`` works as intended.
    """
    for guild, expected_value in (
        (Guild.precreate(202212200004, premium_tier = 0), TIER_0.bitrate_limit),
        (Guild.precreate(202212200005, premium_tier = TIER_MAX.tier), TIER_MAX.bitrate_limit),
        (Guild.precreate(202212200006, premium_tier = 1, features = [GuildFeature.vip_voice_regions]), 128000),
        (
            Guild.precreate(202212200007, premium_tier = TIER_MAX.tier, features = [GuildFeature.vip_voice_regions]),
            TIER_MAX.bitrate_limit,
        ),
    ):
        vampytest.assert_eq(guild.bitrate_limit, expected_value)


def test__Guild__upload_limit():
    """
    Tests whether ``Guild.upload_limit`` works as intended.
    """
    for guild, expected_value in (
        (Guild.precreate(202212200008, premium_tier = 0), TIER_0.upload_limit),
        (Guild.precreate(202212200009, premium_tier = TIER_MAX.tier), TIER_MAX.upload_limit),
    ):
        vampytest.assert_eq(guild.upload_limit, expected_value)


def test__Guild__sticker_limit():
    """
    Tests whether ``Guild.sticker_limit`` works as intended.
    """
    for guild, expected_value in (
        (Guild.precreate(202212200010, premium_tier = 0), TIER_0.sticker_limit),
        (Guild.precreate(202212200011, premium_tier = TIER_MAX.tier), TIER_MAX.sticker_limit),
        (Guild.precreate(202212200012, premium_tier = 1, features = [GuildFeature.more_sticker]), 30),
        (
            Guild.precreate(202212200013, premium_tier = TIER_MAX.tier, features = [GuildFeature.more_sticker]),
            TIER_MAX.sticker_limit,
        ),
    ):
        vampytest.assert_eq(guild.sticker_limit, expected_value)


def test__Guild__emoji_counts():
    """
    Tests whether ``Guild.emoji_counts`` works as intended.
    """
    emoji_0 = Emoji.precreate(202212200014)
    emoji_1 = Emoji.precreate(202212200015, animated = True, managed = True)
    
    guild = Guild.precreate(202212200016)
    guild.emojis[emoji_0.id] = emoji_0
    guild.emojis[emoji_1.id] = emoji_1
    
    emoji_counts = guild.emoji_counts
    vampytest.assert_instance(emoji_counts, EmojiCounts)
    vampytest.assert_eq(emoji_counts.normal_static, 1)
    vampytest.assert_eq(emoji_counts.managed_animated, 1)
    

def test__Guild__sticker_counts():
    """
    Tests whether ``Guild.sticker_counts`` works as intended.
    """
    sticker_0 = Sticker.precreate(202212200017, format = StickerFormat.png)
    sticker_1 = Sticker.precreate(202212200018, format = StickerFormat.apng)
    
    guild = Guild.precreate(202212200019)
    guild.stickers[sticker_0.id] = sticker_0
    guild.stickers[sticker_1.id] = sticker_1
    
    sticker_counts = guild.sticker_counts
    vampytest.assert_instance(sticker_counts, StickerCounts)
    vampytest.assert_eq(sticker_counts.static, 1)
    vampytest.assert_eq(sticker_counts.animated, 1)


def test__Guild__iter_features():
    """
    Tests whether ``Guild.iter_features`` works as intended.
    """
    for guild, expected_output in (
        (
            Guild.precreate(202212200033, features = []),
            [],
        ), (
            Guild.precreate(202212200022, features = [GuildFeature.animated_banner, GuildFeature.animated_icon]),
            [GuildFeature.animated_banner, GuildFeature.animated_icon],
        ),
    ):
        vampytest.assert_eq([*guild.iter_features()], expected_output)
