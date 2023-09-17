from datetime import datetime as DateTime

import vampytest

from ....bases import Icon
from ....emoji import Emoji

from ..flags import ChannelFlag
from ..preinstanced import ForumLayout, SortOrder, VideoQualityMode, VoiceRegion

from ..base import ChannelMetadataBase


def test__ChannelMetadataBase__place_holders():
    """
    Tests whether all placeholder of ``ChannelMetadataBase`` works as intended.
    """
    channel_metadata = ChannelMetadataBase()
    
    vampytest.assert_instance(channel_metadata.application_id, int)
    vampytest.assert_instance(channel_metadata.applied_tag_ids, tuple, nullable = True)
    vampytest.assert_instance(channel_metadata.archived, bool)
    vampytest.assert_instance(channel_metadata.archived_at, DateTime, nullable = True)
    vampytest.assert_instance(channel_metadata.auto_archive_after, int)
    vampytest.assert_instance(channel_metadata.available_tags, tuple, nullable = True)
    vampytest.assert_instance(channel_metadata.bitrate, int)
    vampytest.assert_instance(channel_metadata.default_forum_layout, ForumLayout)
    vampytest.assert_instance(channel_metadata.default_sort_order, SortOrder)
    vampytest.assert_instance(channel_metadata.default_thread_auto_archive_after, int)
    vampytest.assert_instance(channel_metadata.default_thread_reaction, Emoji, nullable = True)
    vampytest.assert_instance(channel_metadata.flags, ChannelFlag)
    vampytest.assert_instance(channel_metadata.icon, Icon)
    vampytest.assert_instance(channel_metadata.invitable, bool)
    vampytest.assert_instance(channel_metadata.name, str)
    vampytest.assert_instance(channel_metadata.nsfw, bool)
    vampytest.assert_instance(channel_metadata.open, bool)
    vampytest.assert_instance(channel_metadata.owner_id, int)
    vampytest.assert_instance(channel_metadata.parent_id, int)
    vampytest.assert_instance(channel_metadata.permission_overwrites, dict, nullable = True)
    vampytest.assert_instance(channel_metadata.position, int)
    vampytest.assert_instance(channel_metadata.region, VoiceRegion)
    vampytest.assert_instance(channel_metadata.slowmode, int)
    vampytest.assert_instance(channel_metadata.thread_users, dict, nullable = True)
    vampytest.assert_instance(channel_metadata.status, str, nullable = True)
    vampytest.assert_instance(channel_metadata.topic, str, nullable = True)
    vampytest.assert_instance(channel_metadata.user_limit, int)
    vampytest.assert_instance(channel_metadata.video_quality_mode, VideoQualityMode)
