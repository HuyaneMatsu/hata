from datetime import datetime as DateTime

import vampytest

from ..guild_thread_announcements import ChannelMetadataGuildThreadAnnouncements

from .test__ChannelMetadataGuildThreadAnnouncements__constructor import _assert_fields_set


def test__ChannelMetadataGuildThreadAnnouncements__copy():
    """
    Tests whether ``ChannelMetadataGuildThreadAnnouncements.copy` works as intended.
    """
    name = 'alice'
    parent_id = 202304120061
    created_at = DateTime(2016, 4, 4)
    archived = False
    archived_at = DateTime(2017, 4, 4)
    auto_archive_after = 3600
    open_ = True
    owner_id = 202304120062
    slowmode = 30
    
    channel_metadata = ChannelMetadataGuildThreadAnnouncements(
        name = name,
        parent_id = parent_id,
        created_at = created_at,
        archived = archived,
        archived_at = archived_at,
        auto_archive_after = auto_archive_after,
        open = open_,
        owner_id = owner_id,
        slowmode = slowmode,
    )
    
    copy = channel_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildThreadAnnouncements__copy_with__0():
    """
    Tests whether ``ChannelMetadataGuildThreadAnnouncements.copy_with` works as intended.
    
    Case: No fields.
    """
    name = 'alice'
    parent_id = 202304120063
    created_at = DateTime(2016, 4, 4)
    archived = False
    archived_at = DateTime(2017, 4, 4)
    auto_archive_after = 3600
    open_ = True
    owner_id = 202304120064
    slowmode = 30
    
    channel_metadata = ChannelMetadataGuildThreadAnnouncements(
        name = name,
        parent_id = parent_id,
        created_at = created_at,
        archived = archived,
        archived_at = archived_at,
        auto_archive_after = auto_archive_after,
        open = open_,
        owner_id = owner_id,
        slowmode = slowmode,
    )
    
    copy = channel_metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildThreadAnnouncements__copy_with__1():
    """
    Tests whether ``ChannelMetadataGuildThreadAnnouncements.copy_with` works as intended.
    
    Case: All fields.
    """
    old_name = 'alice'
    old_parent_id = 202304120065
    old_created_at = DateTime(2016, 4, 4)
    old_archived = False
    old_archived_at = DateTime(2017, 4, 4)
    old_auto_archive_after = 3600
    old_open = True
    old_owner_id = 202304120066
    old_slowmode = 30
    
    new_name = 'emotion'
    new_parent_id = 202304120067
    new_created_at = DateTime(2016, 4, 5)
    new_archived = True
    new_archived_at = DateTime(2017, 4, 5)
    new_auto_archive_after = 604800
    new_open = False
    new_owner_id = 202304120068
    new_slowmode = 31
    
    
    channel_metadata = ChannelMetadataGuildThreadAnnouncements(
        name = old_name,
        parent_id = old_parent_id,
        created_at = old_created_at,
        archived = old_archived,
        archived_at = old_archived_at,
        auto_archive_after = old_auto_archive_after,
        open = old_open,
        owner_id = old_owner_id,
        slowmode = old_slowmode,
    )
    
    copy = channel_metadata.copy_with(
        name = new_name,
        parent_id = new_parent_id,
        created_at = new_created_at,
        archived = new_archived,
        archived_at = new_archived_at,
        auto_archive_after = new_auto_archive_after,
        open = new_open,
        owner_id = new_owner_id,
        slowmode = new_slowmode,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.parent_id, new_parent_id)
    vampytest.assert_eq(copy._created_at, new_created_at)
    vampytest.assert_eq(copy.archived, new_archived)
    vampytest.assert_eq(copy.archived_at, new_archived_at)
    vampytest.assert_eq(copy.auto_archive_after, new_auto_archive_after)
    vampytest.assert_eq(copy.open, new_open)
    vampytest.assert_eq(copy.owner_id, new_owner_id)
    vampytest.assert_eq(copy.slowmode, new_slowmode)


def test__ChannelMetadataGuildThreadAnnouncements__copy_with_keyword_parameters__0():
    """
    Tests whether ``ChannelMetadataGuildThreadAnnouncements.copy_with_keyword_parameters` works as intended.
    
    Case: No fields.
    """
    name = 'alice'
    parent_id = 202304120069
    created_at = DateTime(2016, 4, 4)
    archived = False
    archived_at = DateTime(2017, 4, 4)
    auto_archive_after = 3600
    open_ = True
    owner_id = 202304120070
    slowmode = 30
    
    channel_metadata = ChannelMetadataGuildThreadAnnouncements(
        name = name,
        parent_id = parent_id,
        created_at = created_at,
        archived = archived,
        archived_at = archived_at,
        auto_archive_after = auto_archive_after,
        open = open_,
        owner_id = owner_id,
        slowmode = slowmode,
    )
    
    keyword_parameters = {}
    copy = channel_metadata.copy_with_keyword_parameters(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildThreadAnnouncements__copy_with_keyword_parameters__1():
    """
    Tests whether ``ChannelMetadataGuildThreadAnnouncements.copy_with_keyword_parameters` works as intended.
    
    Case: All fields.
    """
    old_name = 'alice'
    old_parent_id = 202304120071
    old_created_at = DateTime(2016, 4, 4)
    old_archived = False
    old_archived_at = DateTime(2017, 4, 4)
    old_auto_archive_after = 3600
    old_open = True
    old_owner_id = 202304120072
    old_slowmode = 30
    
    new_name = 'emotion'
    new_parent_id = 202304120073
    new_created_at = DateTime(2016, 4, 5)
    new_archived = True
    new_archived_at = DateTime(2017, 4, 5)
    new_auto_archive_after = 604800
    new_open = False
    new_owner_id = 202304120074
    new_slowmode = 31
    
    channel_metadata = ChannelMetadataGuildThreadAnnouncements(
        name = old_name,
        parent_id = old_parent_id,
        created_at = old_created_at,
        archived = old_archived,
        archived_at = old_archived_at,
        auto_archive_after = old_auto_archive_after,
        open = old_open,
        owner_id = old_owner_id,
        slowmode = old_slowmode,
    )
    
    keyword_parameters = {
        'name': new_name,
        'parent_id': new_parent_id,
        'created_at': new_created_at,
        'archived': new_archived,
        'archived_at': new_archived_at,
        'auto_archive_after': new_auto_archive_after,
        'open': new_open,
        'owner_id': new_owner_id,
        'slowmode': new_slowmode,
    }
    
    copy = channel_metadata.copy_with_keyword_parameters(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.parent_id, new_parent_id)
    vampytest.assert_eq(copy._created_at, new_created_at)
    vampytest.assert_eq(copy.archived, new_archived)
    vampytest.assert_eq(copy.archived_at, new_archived_at)
    vampytest.assert_eq(copy.auto_archive_after, new_auto_archive_after)
    vampytest.assert_eq(copy.open, new_open)
    vampytest.assert_eq(copy.owner_id, new_owner_id)
    vampytest.assert_eq(copy.slowmode, new_slowmode)
