from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...discovery_category import DiscoveryCategory

from ..discovery import GuildDiscovery


def test__DiscoveryCategory__repr():
    """
    Tests whether ``GuildDiscovery.__repr__`` works as intended.
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
    vampytest.assert_instance(repr(discovery), str)


def test__DiscoveryCategory__hash():
    """
    Tests whether ``GuildDiscovery.__hash__`` works as intended.
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
    vampytest.assert_instance(hash(discovery), int)


def test__DiscoveryCategory__eq():
    """
    Tests whether ``GuildDiscovery.__eq__`` works as intended.
    """
    application_actioned = DateTime(2016, 5, 4, tzinfo = TimeZone.utc)
    application_requested = DateTime(2017, 6, 4, tzinfo = TimeZone.utc)
    emoji_discovery = True
    keywords = ['kisaki']
    primary_category = DiscoveryCategory.music
    sub_categories = [DiscoveryCategory.other]
    
    keyword_parameters = {
        'application_actioned': application_actioned,
        'application_requested': application_requested,
        'emoji_discovery': emoji_discovery,
        'keywords': keywords,
        'primary_category': primary_category,
        'sub_categories': sub_categories,
    }
    
    discovery = GuildDiscovery(**keyword_parameters)
    vampytest.assert_eq(discovery, discovery)
    vampytest.assert_ne(discovery, object())
    
    for field_name, field_value in (
        ('application_actioned', None),
        ('application_requested', None),
        ('emoji_discovery', False),
        ('keywords', None),
        ('primary_category', DiscoveryCategory.gaming),
        ('sub_categories', None),
    ):
        test_discovery = GuildDiscovery(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(discovery, test_discovery)
