from datetime import datetime as DateTime

import vampytest

from ....emoji import Emoji

from ...activity_assets import ActivityAssets
from ...activity_party import ActivityParty
from ...activity_secrets import ActivitySecrets
from ...activity_timestamps import ActivityTimestamps

from ..base import ActivityMetadataBase
from ..flags import ActivityFlag
from ..preinstanced import HangType

from .test__ActivityMetadataBase__constructor import _assert_fields_set


def test__ActivityMetadataBase__placeholders():
    """
    Tests whether ``ActivityMetadataBase``'s placeholders work as intended.
    """
    activity_metadata = ActivityMetadataBase()
    vampytest.assert_instance(activity_metadata.application_id, int)
    vampytest.assert_instance(activity_metadata.assets, ActivityAssets, nullable = True)
    vampytest.assert_instance(activity_metadata.buttons, tuple, nullable = True)
    vampytest.assert_instance(activity_metadata.created_at, DateTime, nullable = True)
    vampytest.assert_instance(activity_metadata.details, str, nullable = True)
    vampytest.assert_instance(activity_metadata.details_url, str, nullable = True)
    vampytest.assert_instance(activity_metadata.emoji, Emoji, nullable = True)
    vampytest.assert_instance(activity_metadata.flags, ActivityFlag)
    vampytest.assert_instance(activity_metadata.hang_type, HangType)
    vampytest.assert_instance(activity_metadata.id, int)
    vampytest.assert_instance(activity_metadata.name, str)
    vampytest.assert_instance(activity_metadata.party, ActivityParty, nullable = True)
    vampytest.assert_instance(activity_metadata.secrets, ActivitySecrets, nullable = True)
    vampytest.assert_instance(activity_metadata.session_id, str, nullable = True)
    vampytest.assert_instance(activity_metadata.state, str, nullable = True)
    vampytest.assert_instance(activity_metadata.state_url, str, nullable = True)
    vampytest.assert_instance(activity_metadata.sync_id, str, nullable = True)
    vampytest.assert_instance(activity_metadata.timestamps, ActivityTimestamps, nullable = True)
    vampytest.assert_instance(activity_metadata.url, str, nullable = True)
    

def test__ActivityMetadataBase__copy():
    """
    Tests whether ``ActivityMetadataBase.copy`` works as intended.
    """
    activity_metadata = ActivityMetadataBase()
    
    copy = activity_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, activity_metadata)
    
    vampytest.assert_eq(copy, activity_metadata)


def test__ActivityMetadataBase__copy_with__no_fields():
    """
    Tests whether ``ActivityMetadataBase.copy_with`` works as intended.
    
    Case: No fields given.
    """
    activity_metadata = ActivityMetadataBase()
    
    copy = activity_metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, activity_metadata)
    
    vampytest.assert_eq(copy, activity_metadata)


def test__ActivityMetadataBase__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ActivityMetadataBase.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    activity_metadata = ActivityMetadataBase()
    
    copy = activity_metadata.copy_with_keyword_parameters({})
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, activity_metadata)
    
    vampytest.assert_eq(copy, activity_metadata)
