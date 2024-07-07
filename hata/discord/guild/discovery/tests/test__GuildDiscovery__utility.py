from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...discovery_category import DiscoveryCategory

from ..discovery import GuildDiscovery

from .test__GuildDiscovery__constructor import _check_is_every_field_set


def test__GuildDiscovery__new__copy():
    """
    Tests whether ``GuildDiscovery.copy`` works as intended.
    """
    application_actioned = DateTime(2016, 5, 4, tzinfo = TimeZone.utc)
    application_requested = DateTime(2017, 6, 4, tzinfo = TimeZone.utc)
    emoji_discovery = True
    keywords = ['kisaki']
    primary_category = DiscoveryCategory.music
    sub_categories = [DiscoveryCategory.other]
    
    discovery = GuildDiscovery(
        application_actioned = application_actioned,
        application_requested = application_requested,
        emoji_discovery = emoji_discovery,
        keywords = keywords,
        primary_category = primary_category,
        sub_categories = sub_categories,
    )
    copy = discovery.copy()
    _check_is_every_field_set(copy)
    
    vampytest.assert_eq(discovery, copy)
    vampytest.assert_is_not(discovery, copy)


def test__GuildDiscovery__new__copy_with__0():
    """
    Tests whether ``GuildDiscovery.copy_with`` works as intended.
    
    Case: No fields given.
    """
    application_actioned = DateTime(2016, 5, 4, tzinfo = TimeZone.utc)
    application_requested = DateTime(2017, 6, 4, tzinfo = TimeZone.utc)
    emoji_discovery = True
    keywords = ['kisaki']
    primary_category = DiscoveryCategory.music
    sub_categories = [DiscoveryCategory.other]
    
    discovery = GuildDiscovery(
        application_actioned = application_actioned,
        application_requested = application_requested,
        emoji_discovery = emoji_discovery,
        keywords = keywords,
        primary_category = primary_category,
        sub_categories = sub_categories,
    )
    copy = discovery.copy_with()
    _check_is_every_field_set(copy)
    
    vampytest.assert_eq(discovery, copy)
    vampytest.assert_is_not(discovery, copy)


def test__GuildDiscovery__new__copy_with__1():
    """
    Tests whether ``GuildDiscovery.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_application_actioned = DateTime(2016, 5, 4, tzinfo = TimeZone.utc)
    new_application_actioned = DateTime(2016, 5, 9, tzinfo = TimeZone.utc)
    old_application_requested = DateTime(2017, 6, 4, tzinfo = TimeZone.utc)
    new_application_requested = DateTime(2017, 6, 9, tzinfo = TimeZone.utc)
    old_emoji_discovery = True
    new_emoji_discovery = False
    old_keywords = ['kisaki']
    new_keywords = ['nasca']
    old_primary_category = DiscoveryCategory.music
    new_primary_category = DiscoveryCategory.gaming
    old_sub_categories = [DiscoveryCategory.other]
    new_sub_categories = [DiscoveryCategory.art, DiscoveryCategory.memes]
    
    discovery = GuildDiscovery(
        application_actioned = old_application_actioned,
        application_requested = old_application_requested,
        emoji_discovery = old_emoji_discovery,
        keywords = old_keywords,
        primary_category = old_primary_category,
        sub_categories = old_sub_categories,
    )
    copy = discovery.copy_with(
        application_actioned = new_application_actioned,
        application_requested = new_application_requested,
        emoji_discovery = new_emoji_discovery,
        keywords = new_keywords,
        primary_category = new_primary_category,
        sub_categories = new_sub_categories,
    )
    _check_is_every_field_set(copy)
    
    vampytest.assert_is_not(discovery, copy)
    
    vampytest.assert_eq(copy.application_actioned, new_application_actioned)
    vampytest.assert_eq(copy.application_requested, new_application_requested)
    vampytest.assert_eq(copy.emoji_discovery, new_emoji_discovery)
    vampytest.assert_eq(copy.keywords, tuple(new_keywords))
    vampytest.assert_is(copy.primary_category, new_primary_category)
    vampytest.assert_eq(copy.sub_categories, tuple(new_sub_categories))


def test__GuildDiscovery__iter_keywords():
    """
    Asserts whether ``GuildDiscovery.iter_keywords`` works as intended.
    """
    for input_value, expected_output in (
        (None, []),
        (['a'], ['a']),
        (['a', 'b'], ['a', 'b']),
    ):
        discovery = GuildDiscovery(keywords = input_value)
        vampytest.assert_eq(expected_output, [*discovery.iter_keywords()])


def test__GuildDiscovery__iter_sub_categories():
    """
    Asserts whether ``GuildDiscovery.iter_sub_categories`` works as intended.
    """
    for input_value, expected_output in (
        (None, []),
        ([DiscoveryCategory.art], [DiscoveryCategory.art]),
        ([DiscoveryCategory.art, DiscoveryCategory.memes], [DiscoveryCategory.art, DiscoveryCategory.memes]),
    ):
        discovery = GuildDiscovery(sub_categories = input_value)
        vampytest.assert_eq(expected_output, [*discovery.iter_sub_categories()])
