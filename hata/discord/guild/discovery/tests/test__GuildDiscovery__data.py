from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ...discovery_category import DiscoveryCategory

from ..discovery import GuildDiscovery

from .test__GuildDiscovery__constructor import _check_is_every_field_set


def test__DiscoveryCategory__from_data():
    """
    Tests whether ``GuildDiscovery.from_data`` works as intended.
    """
    application_actioned = DateTime(2016, 5, 4)
    application_requested = DateTime(2017, 6, 4)
    emoji_discovery = True
    keywords = ['kisaki']
    primary_category = DiscoveryCategory.music
    sub_categories = [DiscoveryCategory.other]
    
    data = {
        'partner_actioned_timestamp': datetime_to_timestamp(application_actioned),
        'partner_application_timestamp': datetime_to_timestamp(application_requested),
        'emoji_discoverability_enabled': emoji_discovery,
        'keywords': keywords,
        'primary_category_id': primary_category.value,
        'category_ids': [sub_category.value for sub_category in sub_categories],
    }
    
    discovery = GuildDiscovery.from_data(data)
    _check_is_every_field_set(discovery)
    
    vampytest.assert_eq(discovery.application_actioned, application_actioned)
    vampytest.assert_eq(discovery.application_requested, application_requested)
    vampytest.assert_eq(discovery.emoji_discovery, emoji_discovery)
    vampytest.assert_eq(discovery.keywords, tuple(keywords))
    vampytest.assert_is(discovery.primary_category, primary_category)
    vampytest.assert_eq(discovery.sub_categories, tuple(sub_categories))


def test__DiscoveryCategory__to_data():
    """
    Tests whether ``GuildDiscovery.__new__`` works as intended.
    
    Case: include defaults and internals.
    """
    application_actioned = DateTime(2016, 5, 4)
    application_requested = DateTime(2017, 6, 4)
    emoji_discovery = True
    keywords = ['kisaki']
    primary_category = DiscoveryCategory.music
    sub_categories = [DiscoveryCategory.other]
    
    data = {
        'partner_actioned_timestamp': datetime_to_timestamp(application_actioned),
        'partner_application_timestamp': datetime_to_timestamp(application_requested),
        'emoji_discoverability_enabled': emoji_discovery,
        'keywords': keywords,
        'primary_category_id': primary_category.value,
        'category_ids': [sub_category.value for sub_category in sub_categories],
    }
    
    discovery = GuildDiscovery.from_data(data)
    _check_is_every_field_set(discovery)
    
    vampytest.assert_eq(discovery.application_actioned, application_actioned)
    vampytest.assert_eq(discovery.application_requested, application_requested)
    vampytest.assert_eq(discovery.emoji_discovery, emoji_discovery)
    vampytest.assert_eq(discovery.keywords, tuple(keywords))
    vampytest.assert_is(discovery.primary_category, primary_category)
    vampytest.assert_eq(discovery.sub_categories, tuple(sub_categories))
