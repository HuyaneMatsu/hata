from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..guild_thread_base import ChannelMetadataGuildThreadBase

from .test__ChannelMetadataGuildThreadBase__constructor import _assert_fields_set


def test__ChannelMetadataGuildThreadBase__copy():
    """
    Tests whether ``ChannelMetadataGuildThreadBase.copy` works as intended.
    """
    name = 'alice'
    parent_id = 202304120047
    created_at = DateTime(2016, 4, 4, tzinfo = TimeZone.utc)
    archived = False
    archived_at = DateTime(2017, 4, 4, tzinfo = TimeZone.utc)
    auto_archive_after = 3600
    open_ = True
    owner_id = 202304120048
    slowmode = 30
    
    channel_metadata = ChannelMetadataGuildThreadBase(
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


def test__ChannelMetadataGuildThreadBase__copy_with__0():
    """
    Tests whether ``ChannelMetadataGuildThreadBase.copy_with` works as intended.
    
    Case: No fields.
    """
    name = 'alice'
    parent_id = 202304120049
    created_at = DateTime(2016, 4, 4, tzinfo = TimeZone.utc)
    archived = False
    archived_at = DateTime(2017, 4, 4, tzinfo = TimeZone.utc)
    auto_archive_after = 3600
    open_ = True
    owner_id = 202304120050
    slowmode = 30
    
    channel_metadata = ChannelMetadataGuildThreadBase(
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


def test__ChannelMetadataGuildThreadBase__copy_with__1():
    """
    Tests whether ``ChannelMetadataGuildThreadBase.copy_with` works as intended.
    
    Case: All fields.
    """
    old_name = 'alice'
    old_parent_id = 202304120051
    old_created_at = DateTime(2016, 4, 4, tzinfo = TimeZone.utc)
    old_archived = False
    old_archived_at = DateTime(2017, 4, 4, tzinfo = TimeZone.utc)
    old_auto_archive_after = 3600
    old_open = True
    old_owner_id = 202304120052
    old_slowmode = 30
    
    new_name = 'emotion'
    new_parent_id = 202304120053
    new_created_at = DateTime(2016, 4, 5, tzinfo = TimeZone.utc)
    new_archived = True
    new_archived_at = DateTime(2017, 4, 5, tzinfo = TimeZone.utc)
    new_auto_archive_after = 604800
    new_open = False
    new_owner_id = 202304120054
    new_slowmode = 31
    
    
    channel_metadata = ChannelMetadataGuildThreadBase(
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


def test__ChannelMetadataGuildThreadBase__copy_with_keyword_parameters__0():
    """
    Tests whether ``ChannelMetadataGuildThreadBase.copy_with_keyword_parameters` works as intended.
    
    Case: No fields.
    """
    name = 'alice'
    parent_id = 202304120055
    created_at = DateTime(2016, 4, 4, tzinfo = TimeZone.utc)
    archived = False
    archived_at = DateTime(2017, 4, 4, tzinfo = TimeZone.utc)
    auto_archive_after = 3600
    open_ = True
    owner_id = 202304120056
    slowmode = 30
    
    channel_metadata = ChannelMetadataGuildThreadBase(
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


def test__ChannelMetadataGuildThreadBase__copy_with_keyword_parameters__1():
    """
    Tests whether ``ChannelMetadataGuildThreadBase.copy_with_keyword_parameters` works as intended.
    
    Case: All fields.
    """
    old_name = 'alice'
    old_parent_id = 202304120057
    old_created_at = DateTime(2016, 4, 4, tzinfo = TimeZone.utc)
    old_archived = False
    old_archived_at = DateTime(2017, 4, 4, tzinfo = TimeZone.utc)
    old_auto_archive_after = 3600
    old_open = True
    old_owner_id = 202304120058
    old_slowmode = 30
    
    new_name = 'emotion'
    new_parent_id = 202304120059
    new_created_at = DateTime(2016, 4, 5, tzinfo = TimeZone.utc)
    new_archived = True
    new_archived_at = DateTime(2017, 4, 5, tzinfo = TimeZone.utc)
    new_auto_archive_after = 604800
    new_open = False
    new_owner_id = 202304120060
    new_slowmode = 31
    
    channel_metadata = ChannelMetadataGuildThreadBase(
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
