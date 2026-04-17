from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..guild_thread_announcements import ChannelMetadataGuildThreadAnnouncements


def _assert_fields_set(channel_metadata):
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildThreadAnnouncements)
    
    vampytest.assert_instance(channel_metadata.parent_id, int)
    vampytest.assert_instance(channel_metadata.name, str)
    vampytest.assert_instance(channel_metadata._cache_permission, dict, nullable = True)
    vampytest.assert_instance(channel_metadata._created_at, DateTime, nullable = True)
    vampytest.assert_instance(channel_metadata.archived, bool)
    vampytest.assert_instance(channel_metadata.archived_at, DateTime, nullable = True)
    vampytest.assert_instance(channel_metadata.auto_archive_after, int)
    vampytest.assert_instance(channel_metadata.open, bool)
    vampytest.assert_instance(channel_metadata.owner_id, int)
    vampytest.assert_instance(channel_metadata.slowmode, int)
    vampytest.assert_instance(channel_metadata.thread_users, dict, nullable = True)


def test__ChannelMetadataGuildThreadAnnouncements__new__0():
    """
    Tests whether ``ChannelMetadataGuildThreadAnnouncements.__new__`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202209180018
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14, tzinfo = TimeZone.utc)
    archived = True
    archived_at = DateTime(2021, 5, 14, tzinfo = TimeZone.utc)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180019
    slowmode = 60
    
    channel_metadata = ChannelMetadataGuildThreadAnnouncements(
        parent_id = parent_id,
        name = name,
        created_at = created_at,
        archived = archived,
        archived_at = archived_at,
        auto_archive_after = auto_archive_after,
        open = open_,
        owner_id = owner_id,
        slowmode = slowmode,
    )
    _assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.parent_id, parent_id)
    vampytest.assert_eq(channel_metadata.name, name)
    vampytest.assert_eq(channel_metadata._created_at, created_at)
    vampytest.assert_eq(channel_metadata.archived, archived)
    vampytest.assert_eq(channel_metadata.archived_at, archived_at)
    vampytest.assert_eq(channel_metadata.auto_archive_after, auto_archive_after)
    vampytest.assert_eq(channel_metadata.open, open_)
    vampytest.assert_eq(channel_metadata.owner_id, owner_id)
    vampytest.assert_eq(channel_metadata.slowmode, slowmode)


def test__ChannelMetadataGuildThreadAnnouncements__new__1():
    """
    Tests whether ``ChannelMetadataGuildThreadAnnouncements.__new__`` works as intended.
    
    Case: no fields given.
    """
    channel_metadata = ChannelMetadataGuildThreadAnnouncements()
    _assert_fields_set(channel_metadata)


def test__ChannelMetadataGuildThreadAnnouncements__from_keyword_parameters__0():
    """
    Tests whether ``ChannelMetadataGuildThreadAnnouncements.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202304110018
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14, tzinfo = TimeZone.utc)
    archived = True
    archived_at = DateTime(2021, 5, 14, tzinfo = TimeZone.utc)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202304110019
    slowmode = 60
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'created_at': created_at,
        'archived': archived,
        'archived_at': archived_at,
        'auto_archive_after': auto_archive_after,
        'open': open_,
        'owner_id': owner_id,
        'slowmode': slowmode,
    }
    channel_metadata = ChannelMetadataGuildThreadAnnouncements.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(channel_metadata.parent_id, parent_id)
    vampytest.assert_eq(channel_metadata.name, name)
    vampytest.assert_eq(channel_metadata._created_at, created_at)
    vampytest.assert_eq(channel_metadata.archived, archived)
    vampytest.assert_eq(channel_metadata.archived_at, archived_at)
    vampytest.assert_eq(channel_metadata.auto_archive_after, auto_archive_after)
    vampytest.assert_eq(channel_metadata.open, open_)
    vampytest.assert_eq(channel_metadata.owner_id, owner_id)
    vampytest.assert_eq(channel_metadata.slowmode, slowmode)


def test__ChannelMetadataGuildThreadAnnouncements__from_keyword_parameters__1():
    """
    Tests whether ``ChannelMetadataGuildThreadAnnouncements.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataGuildThreadAnnouncements.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})


def test__ChannelMetadataGuildThreadAnnouncements__create_empty():
    """
    Tests whether ``ChannelMetadataGuildThreadAnnouncements._create_empty`` works as intended.
    """
    channel_metadata = ChannelMetadataGuildThreadAnnouncements._create_empty()
    _assert_fields_set(channel_metadata)
