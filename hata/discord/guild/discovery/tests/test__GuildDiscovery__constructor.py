from datetime import datetime as DateTime

import vampytest

from ...discovery_category import DiscoveryCategory

from ..discovery import GuildDiscovery


def _check_is_every_field_set(discovery):
    """
    Asserts whether all fields are set of the given discovery.
    
    Parameters
    ----------
    discovery : ``GuildDiscovery``
        The guild discovery instance to check.
    """
    vampytest.assert_instance(discovery, GuildDiscovery)
    vampytest.assert_instance(discovery.application_actioned, DateTime, nullable = True)
    vampytest.assert_instance(discovery.application_requested, DateTime, nullable = True)
    vampytest.assert_instance(discovery.emoji_discovery, bool)
    vampytest.assert_instance(discovery.keywords, tuple, nullable = True)
    vampytest.assert_instance(discovery.primary_category, DiscoveryCategory)
    vampytest.assert_instance(discovery.sub_categories, tuple, nullable = True)


def test__DiscoveryCategory__new__0():
    """
    Tests whether ``GuildDiscovery.__new__`` works as intended.
    
    Case: No fields given.
    """
    discovery = GuildDiscovery()
    _check_is_every_field_set(discovery)


def test__DiscoveryCategory__new__1():
    """
    Tests whether ``GuildDiscovery.__new__`` works as intended.
    
    Case: All fields given.
    """
    application_actioned = DateTime(2016, 5, 4)
    application_requested = DateTime(2017, 6, 4)
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
    _check_is_every_field_set(discovery)
    
    vampytest.assert_eq(discovery.application_actioned, application_actioned)
    vampytest.assert_eq(discovery.application_requested, application_requested)
    vampytest.assert_eq(discovery.emoji_discovery, emoji_discovery)
    vampytest.assert_eq(discovery.keywords, tuple(keywords))
    vampytest.assert_is(discovery.primary_category, primary_category)
    vampytest.assert_eq(discovery.sub_categories, tuple(sub_categories))
