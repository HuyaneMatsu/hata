from datetime import datetime as DateTime

import vampytest

from .... utils import datetime_to_timestamp

from .. import ChannelMetadataGuildThreadPrivate

from .test__ChannelMetadataGuildThreadPrivate__constructor import assert_fields_set


def test__ChannelMetadataGuildThreadPrivate__from_data():
    """
    Tests whether ``ChannelMetadataGuildThreadPrivate.from_data` works as intended.
    """
    parent_id = 202209180040
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14)
    archived = True
    archived_at = DateTime(2021, 5, 14)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180041
    slowmode = 60
    invitable = True
    
    channel_metadata = ChannelMetadataGuildThreadPrivate.from_data({
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
            'invitable': invitable,
        }
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildThreadPrivate)
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
    vampytest.assert_eq(channel_metadata.invitable, invitable)


def test__ChannelMetadataGuildThreadPrivate__to_data():
    """
    Tests whether ``ChannelMetadataGuildThreadPrivate.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    parent_id = 202209180042
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14)
    archived = True
    archived_at = DateTime(2021, 5, 14)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180043
    slowmode = 60
    invitable = True
    
    channel_metadata = ChannelMetadataGuildThreadPrivate({
        'parent_id': parent_id,
        'name': name,
        'created_at': created_at,
        'archived': archived,
        'archived_at': archived_at,
        'auto_archive_after': auto_archive_after,
        'open': open_,
        'owner_id': owner_id,
        'slowmode': slowmode,
        'invitable': invitable,
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
                'invitable': invitable,
            }
        },
    )


def test__ChannelMetadataGuildThreadPrivate__update_attributes():
    """
    Tests whether ``ChannelMetadataGuildThreadPrivate._update_attributes`` works as intended.
    """
    old_parent_id = 202209180044
    new_parent_id = 202209180045
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
    old_invitable = True
    new_invitable = False
    
    channel_metadata = ChannelMetadataGuildThreadPrivate({
        'parent_id': old_parent_id,
        'name': old_name,
        'archived': old_archived,
        'archived_at': old_archived_at,
        'auto_archive_after': old_auto_archive_after,
        'open': old_open,
        'slowmode': old_slowmode,
        'invitable': old_invitable,
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
            'invitable': new_invitable,
        }
    })
    
    vampytest.assert_eq(channel_metadata.parent_id, new_parent_id)
    vampytest.assert_eq(channel_metadata.name, new_name)
    vampytest.assert_eq(channel_metadata.archived, new_archived)
    vampytest.assert_eq(channel_metadata.archived_at, new_archived_at)
    vampytest.assert_eq(channel_metadata.auto_archive_after, new_auto_archive_after)
    vampytest.assert_eq(channel_metadata.open, new_open)
    vampytest.assert_eq(channel_metadata.slowmode, new_slowmode)
    vampytest.assert_eq(channel_metadata.invitable, new_invitable)


def test__ChannelMetadataGuildThreadPrivate__difference_update_attributes():
    """
    Tests whether ``ChannelMetadataGuildThreadPrivate._difference_update_attributes`` works as intended.
    """
    old_parent_id = 202209180046
    new_parent_id = 202209180047
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
    old_invitable = True
    new_invitable = False
    
    channel_metadata = ChannelMetadataGuildThreadPrivate({
        'parent_id': str(old_parent_id),
        'name': old_name,
        'archived': old_archived,
        'archived_at': old_archived_at,
        'auto_archive_after': old_auto_archive_after,
        'open': old_open,
        'slowmode': old_slowmode,
        'invitable': old_invitable,
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
            'invitable': new_invitable,
        }
    })

    vampytest.assert_eq(channel_metadata.parent_id, new_parent_id)
    vampytest.assert_eq(channel_metadata.name, new_name)
    vampytest.assert_eq(channel_metadata.archived, new_archived)
    vampytest.assert_eq(channel_metadata.archived_at, new_archived_at)
    vampytest.assert_eq(channel_metadata.auto_archive_after, new_auto_archive_after)
    vampytest.assert_eq(channel_metadata.open, new_open)
    vampytest.assert_eq(channel_metadata.slowmode, new_slowmode)
    vampytest.assert_eq(channel_metadata.invitable, new_invitable)
    
    vampytest.assert_in('parent_id', old_attributes)
    vampytest.assert_in('name', old_attributes)
    vampytest.assert_in('archived', old_attributes)
    vampytest.assert_in('archived_at', old_attributes)
    vampytest.assert_in('auto_archive_after', old_attributes)
    vampytest.assert_in('open', old_attributes)
    vampytest.assert_in('slowmode', old_attributes)
    vampytest.assert_in('invitable', old_attributes)
    
    vampytest.assert_eq(old_attributes['parent_id'], old_parent_id)
    vampytest.assert_eq(old_attributes['name'], old_name)
    vampytest.assert_eq(old_attributes['archived'], old_archived)
    vampytest.assert_eq(old_attributes['archived_at'], old_archived_at)
    vampytest.assert_eq(old_attributes['auto_archive_after'], old_auto_archive_after)
    vampytest.assert_eq(old_attributes['open'], old_open)
    vampytest.assert_eq(old_attributes['slowmode'], old_slowmode)
    vampytest.assert_eq(old_attributes['invitable'], old_invitable)


def test__ChannelMetadataGuildThreadPrivate__from_partial_data():
    """
    Tests whether ``ChannelMetadataGuildThreadPrivate._from_partial_data`` works as intended.
    """
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataGuildThreadPrivate._from_partial_data({
        'name': name,
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildThreadPrivate)
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.name, name)
