from datetime import datetime as DateTime

import vampytest

from .... utils import datetime_to_timestamp

from .. import ChannelMetadataGuildThreadBase

from .test__ChannelMetadataGuildThreadBase__constructor import assert_fields_set


def test__ChannelMetadataGuildThreadBase__from_data():
    """
    Tests whether ``ChannelMetadataGuildThreadBase.from_data` works as intended.
    """
    parent_id = 202209180002
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14)
    archived = True
    archived_at = DateTime(2021, 5, 14)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180013
    slowmode = 60
    
    channel_metadata = ChannelMetadataGuildThreadBase.from_data({
        'parent_id': str(parent_id),
        'name': name,
        'owner_id': str(owner_id),
        'rate_limit_per_user': slowmode,
        'thread_metadata': {
            'create_timestamp': datetime_to_timestamp(created_at),
            'archived': archived,
            'archive_timestamp': datetime_to_timestamp(archived_at),
            'auto_archive_duration': auto_archive_after // 60,
            'locked': not open_,
        }
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildThreadBase)
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


def test__ChannelMetadataGuildThreadBase__to_data():
    """
    Tests whether ``ChannelMetadataGuildThreadBase.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    parent_id = 202209180003
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14)
    archived = True
    archived_at = DateTime(2021, 5, 14)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180014
    slowmode = 60
    
    channel_metadata = ChannelMetadataGuildThreadBase({
        'parent_id': parent_id,
        'name': name,
        'created_at': created_at,
        'archived': archived,
        'archived_at': archived_at,
        'auto_archive_after': auto_archive_after,
        'open': open_,
        'owner_id': owner_id,
        'slowmode': slowmode,
    })
    
    data = channel_metadata.to_data(defaults = True, include_internals = True)
    
    vampytest.assert_eq(
        data,
        {
            'parent_id': str(parent_id),
            'name': name,
            'owner_id': str(owner_id),
            'rate_limit_per_user': slowmode,
            'thread_metadata': {
                'create_timestamp': datetime_to_timestamp(created_at),
                'archived': archived,
                'archive_timestamp': datetime_to_timestamp(archived_at),
                'auto_archive_duration': auto_archive_after // 60,
                'locked': not open_,
            }
        },
    )


def test__ChannelMetadataGuildThreadBase__update_attributes():
    """
    Tests whether ``ChannelMetadataGuildThreadBase._update_attributes`` works as intended.
    """
    old_parent_id = 202209180004
    new_parent_id = 202209180005
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_archived = True
    new_archived = False
    old_archived_at = DateTime(2021, 5, 14)
    new_archived_at = DateTime(2021, 9, 9)
    old_auto_archive_after = 86400
    new_auto_archive_after = 3600
    old_open = True
    new_open = False
    old_slowmode = 60
    new_slowmode = 69
    
    channel_metadata = ChannelMetadataGuildThreadBase({
        'parent_id': old_parent_id,
        'name': old_name,
        'archived': old_archived,
        'archived_at': old_archived_at,
        'auto_archive_after': old_auto_archive_after,
        'open': old_open,
        'slowmode': old_slowmode,
    })
    
    channel_metadata._update_attributes({
        'parent_id': str(new_parent_id),
        'name': new_name,
        'rate_limit_per_user': new_slowmode,
        'thread_metadata': {
            'archived': new_archived,
            'archive_timestamp': datetime_to_timestamp(new_archived_at),
            'auto_archive_duration': new_auto_archive_after // 60,
            'locked': not new_open,
        }
    })
    
    vampytest.assert_eq(channel_metadata.parent_id, new_parent_id)
    vampytest.assert_eq(channel_metadata.name, new_name)
    vampytest.assert_eq(channel_metadata.archived, new_archived)
    vampytest.assert_eq(channel_metadata.archived_at, new_archived_at)
    vampytest.assert_eq(channel_metadata.auto_archive_after, new_auto_archive_after)
    vampytest.assert_eq(channel_metadata.open, new_open)
    vampytest.assert_eq(channel_metadata.slowmode, new_slowmode)


def test__ChannelMetadataGuildThreadBase__difference_update_attributes():
    """
    Tests whether ``ChannelMetadataGuildThreadBase._difference_update_attributes`` works as intended.
    """
    old_parent_id = 202209180006
    new_parent_id = 202209170007
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_archived = True
    new_archived = False
    old_archived_at = DateTime(2021, 5, 14)
    new_archived_at = DateTime(2021, 9, 9)
    old_auto_archive_after = 86400
    new_auto_archive_after = 3600
    old_open = True
    new_open = False
    old_slowmode = 60
    new_slowmode = 69
    
    channel_metadata = ChannelMetadataGuildThreadBase({
        'parent_id': str(old_parent_id),
        'name': old_name,
        'archived': old_archived,
        'archived_at': old_archived_at,
        'auto_archive_after': old_auto_archive_after,
        'open': old_open,
        'slowmode': old_slowmode,
    })
    
    old_attributes = channel_metadata._difference_update_attributes({
        'parent_id': str(new_parent_id),
        'name': new_name,
        'rate_limit_per_user': new_slowmode,
        'thread_metadata': {
            'archived': new_archived,
            'archive_timestamp': datetime_to_timestamp(new_archived_at),
            'auto_archive_duration': new_auto_archive_after // 60,
            'locked': not new_open,
        }
    })

    vampytest.assert_eq(channel_metadata.parent_id, new_parent_id)
    vampytest.assert_eq(channel_metadata.name, new_name)
    vampytest.assert_eq(channel_metadata.archived, new_archived)
    vampytest.assert_eq(channel_metadata.archived_at, new_archived_at)
    vampytest.assert_eq(channel_metadata.auto_archive_after, new_auto_archive_after)
    vampytest.assert_eq(channel_metadata.open, new_open)
    vampytest.assert_eq(channel_metadata.slowmode, new_slowmode)
    
    vampytest.assert_in('parent_id', old_attributes)
    vampytest.assert_in('name', old_attributes)
    vampytest.assert_in('archived', old_attributes)
    vampytest.assert_in('archived_at', old_attributes)
    vampytest.assert_in('auto_archive_after', old_attributes)
    vampytest.assert_in('open', old_attributes)
    vampytest.assert_in('slowmode', old_attributes)
    
    vampytest.assert_eq(old_attributes['parent_id'], old_parent_id)
    vampytest.assert_eq(old_attributes['name'], old_name)
    vampytest.assert_eq(old_attributes['archived'], old_archived)
    vampytest.assert_eq(old_attributes['archived_at'], old_archived_at)
    vampytest.assert_eq(old_attributes['auto_archive_after'], old_auto_archive_after)
    vampytest.assert_eq(old_attributes['open'], old_open)
    vampytest.assert_eq(old_attributes['slowmode'], old_slowmode)


def test__ChannelMetadataGuildThreadBase__from_partial_data():
    """
    Tests whether ``ChannelMetadataGuildThreadBase._from_partial_data`` works as intended.
    """
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataGuildThreadBase._from_partial_data({
        'name': name,
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildThreadBase)
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.name, name)
