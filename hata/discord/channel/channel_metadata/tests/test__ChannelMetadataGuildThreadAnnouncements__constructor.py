from datetime import datetime as DateTime

import vampytest

from ..guild_thread_announcements import ChannelMetadataGuildThreadAnnouncements


def assert_fields_set(channel_metadata):    
    vampytest.assert_instance(channel_metadata.parent_id, int)
    vampytest.assert_instance(channel_metadata.name, str)
    vampytest.assert_instance(channel_metadata._permission_cache, dict, nullable = True)
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
    created_at = DateTime(2020, 5, 14)
    archived = True
    archived_at = DateTime(2021, 5, 14)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180019
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
    channel_metadata = ChannelMetadataGuildThreadAnnouncements(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildThreadAnnouncements)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)
    
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
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataGuildThreadAnnouncements(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildThreadAnnouncements)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)


def test__ChannelMetadataGuildThreadAnnouncements__create_empty():
    """
    Tests whether ``ChannelMetadataGuildThreadAnnouncements._create_empty`` works as intended.
    """
    channel_metadata = ChannelMetadataGuildThreadAnnouncements._create_empty()
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildThreadAnnouncements)
    
    assert_fields_set(channel_metadata)



def test__ChannelMetadataGuildThreadAnnouncements__precreate__0():
    """
    Tests whether ``ChannelMetadataGuildThreadAnnouncements.precreate`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202209180020
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14)
    archived = True
    archived_at = DateTime(2021, 5, 14)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180021
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
    
    channel_metadata = ChannelMetadataGuildThreadAnnouncements.precreate(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildThreadAnnouncements)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.parent_id, parent_id)
    vampytest.assert_eq(channel_metadata.name, name)
    vampytest.assert_eq(channel_metadata._created_at, created_at)
    vampytest.assert_eq(channel_metadata.archived, archived)
    vampytest.assert_eq(channel_metadata.archived_at, archived_at)
    vampytest.assert_eq(channel_metadata.auto_archive_after, auto_archive_after)
    vampytest.assert_eq(channel_metadata.open, open_)
    vampytest.assert_eq(channel_metadata.owner_id, owner_id)
    vampytest.assert_eq(channel_metadata.slowmode, slowmode)


def test__ChannelMetadataGuildThreadAnnouncements__precreate__1():
    """
    Tests whether ``ChannelMetadataGuildThreadAnnouncements.precreate`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataGuildThreadAnnouncements.precreate(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildThreadAnnouncements)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)
