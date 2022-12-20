import vampytest

from ..guild_premium_perks import GuildPremiumPerks, TIER_0, TIER_1, TIER_2, TIER_3


@vampytest.call_with(TIER_0)
@vampytest.call_with(TIER_1)
@vampytest.call_with(TIER_2)
@vampytest.call_with(TIER_3)
def test__GuildPremiumPerks__attributes(perk):
    """
    Tests whether ``GuildPremiumPerks``-s have their attributes assigned correctly.
    
    Parameters
    ----------
    perk : ``GuildPremiumPerks``
        The perk to check out.
    """
    vampytest.assert_instance(perk, GuildPremiumPerks)
    vampytest.assert_instance(perk.concurrent_activities, int)
    vampytest.assert_instance(perk.emoji_limit, int)
    vampytest.assert_instance(perk.features, tuple, nullable = True)
    vampytest.assert_instance(perk.screen_share_frame_rate, int)
    vampytest.assert_instance(perk.screen_share_resolution, str)
    vampytest.assert_instance(perk.sound_limit, int)
    vampytest.assert_instance(perk.sticker_limit, int)
    vampytest.assert_instance(perk.bitrate_limit, int)
    vampytest.assert_instance(perk.tier, int)
    vampytest.assert_instance(perk.upload_limit, int)



@vampytest.call_with(TIER_0, [])
@vampytest.call_with(TIER_1, [*TIER_1.features])
def test__GuildPremiumPerks__iter_features(perk, expected_features):
    """
    Tests whether ``GuildPremiumPerks.iter_features`` works as intended.
    
    Parameters
    ----------
    perk : ``GuildPremiumPerks``
        The perk to check out.
    expected_features : `list` of ``GuildFeature``
        The expected features yielded by `.iter_features`.
    """
    vampytest.assert_eq([*perk.iter_features()], expected_features)


@vampytest.call_with(TIER_0)
def test__GuildPremiumPerks__iter_features(perk):
    """
    Tests whether ``GuildPremiumPerks.__repr__`` works as intended.
    
    Parameters
    ----------
    perk : ``GuildPremiumPerks``
        The perk to check out.
    """
    vampytest.assert_instance(repr(perk), str)
