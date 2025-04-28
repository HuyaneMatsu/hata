import vampytest

from ..guild_boost_perks import GuildBoostPerks, LEVEL_0, LEVEL_1, LEVEL_2, LEVEL_3


@vampytest.call_with(LEVEL_0)
@vampytest.call_with(LEVEL_1)
@vampytest.call_with(LEVEL_2)
@vampytest.call_with(LEVEL_3)
def test__GuildBoostPerks__attributes(perk):
    """
    Tests whether ``GuildBoostPerks``-s have their attributes assigned correctly.
    
    Parameters
    ----------
    perk : ``GuildBoostPerks``
        The perk to check out.
    """
    vampytest.assert_instance(perk, GuildBoostPerks)
    vampytest.assert_instance(perk.attachment_size_limit, int)
    vampytest.assert_instance(perk.concurrent_activities, int)
    vampytest.assert_instance(perk.emoji_limit, int)
    vampytest.assert_instance(perk.features, tuple, nullable = True)
    vampytest.assert_instance(perk.level, int)
    vampytest.assert_instance(perk.screen_share_frame_rate, int)
    vampytest.assert_instance(perk.screen_share_resolution, str)
    vampytest.assert_instance(perk.sound_limit, int)
    vampytest.assert_instance(perk.sticker_limit, int)
    vampytest.assert_instance(perk.bitrate_limit, int)


@vampytest.call_with(LEVEL_0, [])
@vampytest.call_with(LEVEL_1, [*LEVEL_1.features])
def test__GuildBoostPerks__iter_features(perk, expected_features):
    """
    Tests whether ``GuildBoostPerks.iter_features`` works as intended.
    
    Parameters
    ----------
    perk : ``GuildBoostPerks``
        The perk to check out.
    expected_features : `list` of ``GuildFeature``
        The expected features yielded by `.iter_features`.
    """
    vampytest.assert_eq([*perk.iter_features()], expected_features)


@vampytest.call_with(LEVEL_0)
def test__GuildBoostPerks__repr(perk):
    """
    Tests whether ``GuildBoostPerks.__repr__`` works as intended.
    
    Parameters
    ----------
    perk : ``GuildBoostPerks``
        The perk to check out.
    """
    vampytest.assert_instance(repr(perk), str)
