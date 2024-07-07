from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..flags import ChannelFlag
from ..guild_thread_public import ChannelMetadataGuildThreadPublic

from .test__ChannelMetadataGuildThreadPublic__constructor import _assert_fields_set


def test__ChannelMetadataGuildThreadPublic__copy():
    """
    Tests whether ``ChannelMetadataGuildThreadPublic.copy` works as intended.
    """
    name = 'alice'
    parent_id = 202304120089
    created_at = DateTime(2016, 4, 4, tzinfo = TimeZone.utc)
    archived = False
    archived_at = DateTime(2017, 4, 4, tzinfo = TimeZone.utc)
    auto_archive_after = 3600
    open_ = True
    owner_id = 202304120090
    slowmode = 30
    applied_tag_ids = [202304120091, 202304120092]
    flags = ChannelFlag(1)
    
    channel_metadata = ChannelMetadataGuildThreadPublic(
        name = name,
        parent_id = parent_id,
        created_at = created_at,
        archived = archived,
        archived_at = archived_at,
        auto_archive_after = auto_archive_after,
        open = open_,
        owner_id = owner_id,
        slowmode = slowmode,
        applied_tag_ids = applied_tag_ids,
        flags = flags,
    )
    
    copy = channel_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildThreadPublic__copy_with__0():
    """
    Tests whether ``ChannelMetadataGuildThreadPublic.copy_with` works as intended.
    
    Case: No fields.
    """
    name = 'alice'
    parent_id = 202304120093
    created_at = DateTime(2016, 4, 4, tzinfo = TimeZone.utc)
    archived = False
    archived_at = DateTime(2017, 4, 4, tzinfo = TimeZone.utc)
    auto_archive_after = 3600
    open_ = True
    owner_id = 202304120094
    slowmode = 30
    applied_tag_ids = [202304120095, 202304120096]
    flags = ChannelFlag(1)
    
    channel_metadata = ChannelMetadataGuildThreadPublic(
        name = name,
        parent_id = parent_id,
        created_at = created_at,
        archived = archived,
        archived_at = archived_at,
        auto_archive_after = auto_archive_after,
        open = open_,
        owner_id = owner_id,
        slowmode = slowmode,
        applied_tag_ids = applied_tag_ids,
        flags = flags,
    )
    
    copy = channel_metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildThreadPublic__copy_with__1():
    """
    Tests whether ``ChannelMetadataGuildThreadPublic.copy_with` works as intended.
    
    Case: All fields.
    """
    old_name = 'alice'
    old_parent_id = 202304120097
    old_created_at = DateTime(2016, 4, 4, tzinfo = TimeZone.utc)
    old_archived = False
    old_archived_at = DateTime(2017, 4, 4, tzinfo = TimeZone.utc)
    old_auto_archive_after = 3600
    old_open = True
    old_owner_id = 202304120098
    old_slowmode = 30
    old_applied_tag_ids = [202304120099, 202304120100]
    old_flags = ChannelFlag(1)
    
    new_name = 'emotion'
    new_parent_id = 202304120101
    new_created_at = DateTime(2016, 4, 5, tzinfo = TimeZone.utc)
    new_archived = True
    new_archived_at = DateTime(2017, 4, 5, tzinfo = TimeZone.utc)
    new_auto_archive_after = 604800
    new_open = False
    new_owner_id = 202304120102
    new_slowmode = 31
    new_applied_tag_ids = [202304120103]
    new_flags = ChannelFlag(2)
    
    
    channel_metadata = ChannelMetadataGuildThreadPublic(
        name = old_name,
        parent_id = old_parent_id,
        created_at = old_created_at,
        archived = old_archived,
        archived_at = old_archived_at,
        auto_archive_after = old_auto_archive_after,
        open = old_open,
        owner_id = old_owner_id,
        slowmode = old_slowmode,
        applied_tag_ids = old_applied_tag_ids,
        flags = old_flags,
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
        applied_tag_ids = new_applied_tag_ids,
        flags = new_flags,
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
    vampytest.assert_eq(copy.applied_tag_ids, tuple(new_applied_tag_ids))
    vampytest.assert_eq(copy.flags, new_flags)


def test__ChannelMetadataGuildThreadPublic__copy_with_keyword_parameters__0():
    """
    Tests whether ``ChannelMetadataGuildThreadPublic.copy_with_keyword_parameters` works as intended.
    
    Case: No fields.
    """
    name = 'alice'
    parent_id = 202304120104
    created_at = DateTime(2016, 4, 4, tzinfo = TimeZone.utc)
    archived = False
    archived_at = DateTime(2017, 4, 4, tzinfo = TimeZone.utc)
    auto_archive_after = 3600
    open_ = True
    owner_id = 202304120105
    slowmode = 30
    applied_tag_ids = [202304120106, 202304120107]
    flags = ChannelFlag(1)
    
    channel_metadata = ChannelMetadataGuildThreadPublic(
        name = name,
        parent_id = parent_id,
        created_at = created_at,
        archived = archived,
        archived_at = archived_at,
        auto_archive_after = auto_archive_after,
        open = open_,
        owner_id = owner_id,
        slowmode = slowmode,
        applied_tag_ids = applied_tag_ids,
        flags = flags,
    )
    
    keyword_parameters = {}
    copy = channel_metadata.copy_with_keyword_parameters(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildThreadPublic__copy_with_keyword_parameters__1():
    """
    Tests whether ``ChannelMetadataGuildThreadPublic.copy_with_keyword_parameters` works as intended.
    
    Case: All fields.
    """
    old_name = 'alice'
    old_parent_id = 202304120108
    old_created_at = DateTime(2016, 4, 4, tzinfo = TimeZone.utc)
    old_archived = False
    old_archived_at = DateTime(2017, 4, 4, tzinfo = TimeZone.utc)
    old_auto_archive_after = 3600
    old_open = True
    old_owner_id = 202304120109
    old_slowmode = 30
    old_applied_tag_ids = [202304120110, 202304120111]
    old_flags = ChannelFlag(1)
    
    new_name = 'emotion'
    new_parent_id = 202304120112
    new_created_at = DateTime(2016, 4, 5, tzinfo = TimeZone.utc)
    new_archived = True
    new_archived_at = DateTime(2017, 4, 5, tzinfo = TimeZone.utc)
    new_auto_archive_after = 604800
    new_open = False
    new_owner_id = 202304120113
    new_slowmode = 31
    new_applied_tag_ids = [202304120114]
    new_flags = ChannelFlag(2)
    
    channel_metadata = ChannelMetadataGuildThreadPublic(
        name = old_name,
        parent_id = old_parent_id,
        created_at = old_created_at,
        archived = old_archived,
        archived_at = old_archived_at,
        auto_archive_after = old_auto_archive_after,
        open = old_open,
        owner_id = old_owner_id,
        slowmode = old_slowmode,
        applied_tag_ids = old_applied_tag_ids,
        flags = old_flags,
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
        'applied_tag_ids': new_applied_tag_ids,
        'flags': new_flags,
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
    vampytest.assert_eq(copy.applied_tag_ids, tuple(new_applied_tag_ids))
    vampytest.assert_eq(copy.flags, new_flags)
