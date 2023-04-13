from datetime import datetime as DateTime

import vampytest

from ..guild_thread_private import ChannelMetadataGuildThreadPrivate

from .test__ChannelMetadataGuildThreadPrivate__constructor import _assert_fields_set


def test__ChannelMetadataGuildThreadPrivate__copy():
    """
    Tests whether ``ChannelMetadataGuildThreadPrivate.copy` works as intended.
    """
    name = 'alice'
    parent_id = 202304120075
    created_at = DateTime(2016, 4, 4)
    archived = False
    archived_at = DateTime(2017, 4, 4)
    auto_archive_after = 3600
    open_ = True
    owner_id = 202304120076
    slowmode = 30
    invitable = False
    
    channel_metadata = ChannelMetadataGuildThreadPrivate(
        name = name,
        parent_id = parent_id,
        created_at = created_at,
        archived = archived,
        archived_at = archived_at,
        auto_archive_after = auto_archive_after,
        open = open_,
        owner_id = owner_id,
        slowmode = slowmode,
        invitable = invitable,
    )
    
    copy = channel_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildThreadPrivate__copy_with__0():
    """
    Tests whether ``ChannelMetadataGuildThreadPrivate.copy_with` works as intended.
    
    Case: No fields.
    """
    name = 'alice'
    parent_id = 202304120077
    created_at = DateTime(2016, 4, 4)
    archived = False
    archived_at = DateTime(2017, 4, 4)
    auto_archive_after = 3600
    open_ = True
    owner_id = 202304120078
    slowmode = 30
    invitable = False
    
    channel_metadata = ChannelMetadataGuildThreadPrivate(
        name = name,
        parent_id = parent_id,
        created_at = created_at,
        archived = archived,
        archived_at = archived_at,
        auto_archive_after = auto_archive_after,
        open = open_,
        owner_id = owner_id,
        slowmode = slowmode,
        invitable = invitable,
    )
    
    copy = channel_metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildThreadPrivate__copy_with__1():
    """
    Tests whether ``ChannelMetadataGuildThreadPrivate.copy_with` works as intended.
    
    Case: All fields.
    """
    old_name = 'alice'
    old_parent_id = 202304120079
    old_created_at = DateTime(2016, 4, 4)
    old_archived = False
    old_archived_at = DateTime(2017, 4, 4)
    old_auto_archive_after = 3600
    old_open = True
    old_owner_id = 202304120080
    old_slowmode = 30
    old_invitable = False
    
    new_name = 'emotion'
    new_parent_id = 202304120081
    new_created_at = DateTime(2016, 4, 5)
    new_archived = True
    new_archived_at = DateTime(2017, 4, 5)
    new_auto_archive_after = 604800
    new_open = False
    new_owner_id = 202304120082
    new_slowmode = 31
    new_invitable = True
    
    
    channel_metadata = ChannelMetadataGuildThreadPrivate(
        name = old_name,
        parent_id = old_parent_id,
        created_at = old_created_at,
        archived = old_archived,
        archived_at = old_archived_at,
        auto_archive_after = old_auto_archive_after,
        open = old_open,
        owner_id = old_owner_id,
        slowmode = old_slowmode,
        invitable = old_invitable,
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
        invitable = new_invitable,
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
    vampytest.assert_eq(copy.invitable, new_invitable)


def test__ChannelMetadataGuildThreadPrivate__copy_with_keyword_parameters__0():
    """
    Tests whether ``ChannelMetadataGuildThreadPrivate.copy_with_keyword_parameters` works as intended.
    
    Case: No fields.
    """
    name = 'alice'
    parent_id = 202304120083
    created_at = DateTime(2016, 4, 4)
    archived = False
    archived_at = DateTime(2017, 4, 4)
    auto_archive_after = 3600
    open_ = True
    owner_id = 202304120084
    slowmode = 30
    invitable = False
    
    channel_metadata = ChannelMetadataGuildThreadPrivate(
        name = name,
        parent_id = parent_id,
        created_at = created_at,
        archived = archived,
        archived_at = archived_at,
        auto_archive_after = auto_archive_after,
        open = open_,
        owner_id = owner_id,
        slowmode = slowmode,
        invitable = invitable,
    )
    
    keyword_parameters = {}
    copy = channel_metadata.copy_with_keyword_parameters(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildThreadPrivate__copy_with_keyword_parameters__1():
    """
    Tests whether ``ChannelMetadataGuildThreadPrivate.copy_with_keyword_parameters` works as intended.
    
    Case: All fields.
    """
    old_name = 'alice'
    old_parent_id = 202304120085
    old_created_at = DateTime(2016, 4, 4)
    old_archived = False
    old_archived_at = DateTime(2017, 4, 4)
    old_auto_archive_after = 3600
    old_open = True
    old_owner_id = 202304120086
    old_slowmode = 30
    old_invitable = False
    
    new_name = 'emotion'
    new_parent_id = 202304120087
    new_created_at = DateTime(2016, 4, 5)
    new_archived = True
    new_archived_at = DateTime(2017, 4, 5)
    new_auto_archive_after = 604800
    new_open = False
    new_owner_id = 202304120088
    new_slowmode = 31
    new_invitable = True
    
    channel_metadata = ChannelMetadataGuildThreadPrivate(
        name = old_name,
        parent_id = old_parent_id,
        created_at = old_created_at,
        archived = old_archived,
        archived_at = old_archived_at,
        auto_archive_after = old_auto_archive_after,
        open = old_open,
        owner_id = old_owner_id,
        slowmode = old_slowmode,
        invitable = old_invitable,
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
        'invitable': new_invitable,
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
    vampytest.assert_eq(copy.invitable, new_invitable)
