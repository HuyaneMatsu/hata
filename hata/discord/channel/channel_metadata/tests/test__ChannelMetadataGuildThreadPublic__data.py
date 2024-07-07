from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..flags import ChannelFlag

from ..guild_thread_public import ChannelMetadataGuildThreadPublic

from .test__ChannelMetadataGuildThreadPublic__constructor import _assert_fields_set


def test__ChannelMetadataGuildThreadPublic__from_data():
    """
    Tests whether ``ChannelMetadataGuildThreadPublic.from_data` works as intended.
    """
    parent_id = 202209180058
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14, tzinfo = TimeZone.utc)
    archived = True
    archived_at = DateTime(2021, 5, 14, tzinfo = TimeZone.utc)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180059
    slowmode = 60
    applied_tag_ids = [202209180072]
    flags = ChannelFlag(1)
    
    channel_metadata = ChannelMetadataGuildThreadPublic.from_data({
        'parent_id': str(parent_id),
        'name': name,
        'owner_id': str(owner_id),
        'rate_limit_per_user': slowmode,
        'applied_tags': [str(forum_tag_id) for forum_tag_id in applied_tag_ids],
        'flags': int(flags),
        'thread_metadata': {
            'create_timestamp': datetime_to_timestamp(created_at),
            'archived': archived,
            'archive_timestamp': datetime_to_timestamp(archived_at),
            'auto_archive_duration': auto_archive_after // 60,
            'locked': not open_,
        }
    })
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
    vampytest.assert_eq(channel_metadata.applied_tag_ids, tuple(applied_tag_ids))
    vampytest.assert_eq(channel_metadata.flags, flags)


def test__ChannelMetadataGuildThreadPublic__to_data():
    """
    Tests whether ``ChannelMetadataGuildThreadPublic.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    parent_id = 202209180060
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14, tzinfo = TimeZone.utc)
    archived = True
    archived_at = DateTime(2021, 5, 14, tzinfo = TimeZone.utc)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180061
    slowmode = 60
    applied_tag_ids = [202209180073]
    flags = ChannelFlag(1)
    
    channel_metadata = ChannelMetadataGuildThreadPublic(
        parent_id = parent_id,
        name = name,
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
    
    data = channel_metadata.to_data(defaults = True, include_internals = True)
    
    vampytest.assert_eq(
        data,
        {
            'parent_id': str(parent_id),
            'name': name,
            'owner_id': str(owner_id),
            'rate_limit_per_user': slowmode,
            'applied_tags': [str(forum_tag_id) for forum_tag_id in applied_tag_ids],
            'flags': int(flags),
            'thread_metadata': {
                'create_timestamp': datetime_to_timestamp(created_at),
                'archived': archived,
                'archive_timestamp': datetime_to_timestamp(archived_at),
                'auto_archive_duration': auto_archive_after // 60,
                'locked': not open_,
            }
        },
    )


def test__ChannelMetadataGuildThreadPublic__update_attributes():
    """
    Tests whether ``ChannelMetadataGuildThreadPublic._update_attributes`` works as intended.
    """
    old_parent_id = 202209180061
    new_parent_id = 202209180062
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_archived = True
    new_archived = False
    old_archived_at = DateTime(2021, 5, 14, tzinfo = TimeZone.utc)
    new_archived_at = DateTime(2021, 9, 9, tzinfo = TimeZone.utc)
    old_auto_archive_after = 86400
    new_auto_archive_after = 3600
    old_open = True
    new_open = False
    old_slowmode = 60
    new_slowmode = 69
    old_applied_tag_ids = [202209180074]
    new_applied_tag_ids = [202209180075, 202209180076]
    old_flags = ChannelFlag(1)
    new_flags = ChannelFlag(6)
    
    channel_metadata = ChannelMetadataGuildThreadPublic(
        parent_id = str(old_parent_id),
        name = old_name,
        archived = old_archived,
        archived_at = old_archived_at,
        auto_archive_after = old_auto_archive_after,
        open = old_open,
        slowmode = old_slowmode,
        applied_tag_ids = old_applied_tag_ids,
        flags = old_flags,
    )
    
    channel_metadata._update_attributes({
        'parent_id': str(new_parent_id),
        'name': new_name,
        'rate_limit_per_user': new_slowmode,
        'applied_tags': [str(forum_tag_id) for forum_tag_id in new_applied_tag_ids],
        'flags': int(new_flags),
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
    vampytest.assert_eq(channel_metadata.applied_tag_ids, tuple(new_applied_tag_ids))
    vampytest.assert_eq(channel_metadata.flags, new_flags)


def test__ChannelMetadataGuildThreadPublic__difference_update_attributes():
    """
    Tests whether ``ChannelMetadataGuildThreadPublic._difference_update_attributes`` works as intended.
    """
    old_parent_id = 202209180063
    new_parent_id = 202209180064
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_archived = True
    new_archived = False
    old_archived_at = DateTime(2021, 5, 14, tzinfo = TimeZone.utc)
    new_archived_at = DateTime(2021, 9, 9, tzinfo = TimeZone.utc)
    old_auto_archive_after = 86400
    new_auto_archive_after = 3600
    old_open = True
    new_open = False
    old_slowmode = 60
    new_slowmode = 69
    old_applied_tag_ids = [202209180077]
    new_applied_tag_ids = [202209180078, 202209180079]
    old_flags = ChannelFlag(1)
    new_flags = ChannelFlag(6)
    
    channel_metadata = ChannelMetadataGuildThreadPublic(
        parent_id = str(old_parent_id),
        name = old_name,
        archived = old_archived,
        archived_at = old_archived_at,
        auto_archive_after = old_auto_archive_after,
        open = old_open,
        slowmode = old_slowmode,
        applied_tag_ids = old_applied_tag_ids,
        flags = old_flags,
    )
    
    old_attributes = channel_metadata._difference_update_attributes({
        'parent_id': str(new_parent_id),
        'name': new_name,
        'rate_limit_per_user': new_slowmode,
        'applied_tags': [str(forum_tag_id) for forum_tag_id in new_applied_tag_ids],
        'flags': int(new_flags),
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
    vampytest.assert_eq(channel_metadata.applied_tag_ids, tuple(new_applied_tag_ids))
    vampytest.assert_eq(channel_metadata.flags, new_flags)
    
    vampytest.assert_in('parent_id', old_attributes)
    vampytest.assert_in('name', old_attributes)
    vampytest.assert_in('archived', old_attributes)
    vampytest.assert_in('archived_at', old_attributes)
    vampytest.assert_in('auto_archive_after', old_attributes)
    vampytest.assert_in('open', old_attributes)
    vampytest.assert_in('slowmode', old_attributes)
    vampytest.assert_in('applied_tag_ids', old_attributes)
    vampytest.assert_in('flags', old_attributes)
    
    vampytest.assert_eq(old_attributes['parent_id'], old_parent_id)
    vampytest.assert_eq(old_attributes['name'], old_name)
    vampytest.assert_eq(old_attributes['archived'], old_archived)
    vampytest.assert_eq(old_attributes['archived_at'], old_archived_at)
    vampytest.assert_eq(old_attributes['auto_archive_after'], old_auto_archive_after)
    vampytest.assert_eq(old_attributes['open'], old_open)
    vampytest.assert_eq(old_attributes['slowmode'], old_slowmode)
    vampytest.assert_eq(old_attributes['applied_tag_ids'], tuple(old_applied_tag_ids))
    vampytest.assert_eq(old_attributes['flags'], old_flags)


def test__ChannelMetadataGuildThreadPublic__from_partial_data():
    """
    Tests whether ``ChannelMetadataGuildThreadPublic._from_partial_data`` works as intended.
    """
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataGuildThreadPublic._from_partial_data({
        'name': name,
    })
    _assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.name, name)
