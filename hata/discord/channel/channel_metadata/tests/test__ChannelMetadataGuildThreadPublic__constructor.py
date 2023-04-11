from datetime import datetime as DateTime

import vampytest

from ..flags import ChannelFlag

from ..guild_thread_public import ChannelMetadataGuildThreadPublic


def _assert_fields_set(channel_metadata):
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildThreadPublic)
    
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
    vampytest.assert_instance(channel_metadata.applied_tag_ids, tuple, nullable = True)
    vampytest.assert_instance(channel_metadata.flags, ChannelFlag)


def test__ChannelMetadataGuildThreadPublic__new__0():
    """
    Tests whether ``ChannelMetadataGuildThreadPublic.__new__`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202209180054
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14)
    archived = True
    archived_at = DateTime(2021, 5, 14)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180055
    slowmode = 60
    applied_tag_ids = [202209180070]
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


def test__ChannelMetadataGuildThreadPublic__new__1():
    """
    Tests whether ``ChannelMetadataGuildThreadPublic.__new__`` works as intended.
    
    Case: no fields given.
    """
    channel_metadata = ChannelMetadataGuildThreadPublic()
    _assert_fields_set(channel_metadata)


def test__ChannelMetadataGuildThreadPublic__from_keyword_parameters__0():
    """
    Tests whether ``ChannelMetadataGuildThreadPublic.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202209180054
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14)
    archived = True
    archived_at = DateTime(2021, 5, 14)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180055
    slowmode = 60
    applied_tag_ids = [202209180070]
    flags = ChannelFlag(1)
    
    
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
        'applied_tag_ids': applied_tag_ids,
        'flags': flags,
    }
    channel_metadata = ChannelMetadataGuildThreadPublic.from_keyword_parameters(keyword_parameters)
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
    vampytest.assert_eq(channel_metadata.applied_tag_ids, tuple(applied_tag_ids))
    vampytest.assert_eq(channel_metadata.flags, flags)


def test__ChannelMetadataGuildThreadPublic__from_keyword_parameters__1():
    """
    Tests whether ``ChannelMetadataGuildThreadPublic.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataGuildThreadPublic.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})


def test__ChannelMetadataGuildThreadPublic__create_empty():
    """
    Tests whether ``ChannelMetadataGuildThreadPublic._create_empty`` works as intended.
    """
    channel_metadata = ChannelMetadataGuildThreadPublic._create_empty()
    _assert_fields_set(channel_metadata)
