from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..guild_thread_base import ChannelMetadataGuildThreadBase


def test__ChannelMetadataGuildThreadBase__repr():
    """
    Tests whether ``.ChannelMetadataGuildThreadBase.__repr__`` works as intended.
    """
    parent_id = 202209180008
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14, tzinfo = TimeZone.utc)
    archived = True
    archived_at = DateTime(2021, 5, 14, tzinfo = TimeZone.utc)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180015
    slowmode = 60
    
    channel_metadata  = ChannelMetadataGuildThreadBase(
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
    
    vampytest.assert_instance(repr(channel_metadata), str)


def test__ChannelMetadataGuildThreadBase__hash():
    """
    Tests whether ``.ChannelMetadataGuildThreadBase.__hash__`` works as intended.
    """
    parent_id = 202209180104
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14, tzinfo = TimeZone.utc)
    archived = True
    archived_at = DateTime(2021, 5, 14, tzinfo = TimeZone.utc)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180105
    slowmode = 60
    
    channel_metadata  = ChannelMetadataGuildThreadBase(
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
    
    vampytest.assert_instance(hash(channel_metadata), int)


def test__ChannelMetadataGuildThreadBase__eq():
    """
    Tests whether ``.ChannelMetadataGuildThreadBase.__eq__`` works as intended.
    """
    parent_id = 202209180009
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14, tzinfo = TimeZone.utc)
    archived = True
    archived_at = DateTime(2021, 5, 14, tzinfo = TimeZone.utc)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180016
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
    channel_metadata = ChannelMetadataGuildThreadBase(**keyword_parameters)
    
    vampytest.assert_eq(channel_metadata, channel_metadata)
    vampytest.assert_ne(channel_metadata, object())
    
    for field_name, field_value in (
        ('parent_id', 202209180010),
        ('name', 'Okuu'),
        ('created_at', DateTime(2020, 9, 9, tzinfo = TimeZone.utc)),
        ('archived', False),
        ('archived_at', DateTime(2021, 9, 9, tzinfo = TimeZone.utc)),
        ('auto_archive_after', 3600),
        ('open', False),
        ('owner_id', 202209180017),
        ('slowmode', 69),
    ):
        test_channel_metadata = ChannelMetadataGuildThreadBase(**{**keyword_parameters, field_name: field_value})
        
        vampytest.assert_ne(channel_metadata, test_channel_metadata)
