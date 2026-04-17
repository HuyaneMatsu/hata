from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..guild_thread_announcements import ChannelMetadataGuildThreadAnnouncements


def test__ChannelMetadataGuildThreadAnnouncements__repr():
    """
    Tests whether ``.ChannelMetadataGuildThreadAnnouncements.__repr__`` works as intended.
    """
    parent_id = 202209180030
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14, tzinfo = TimeZone.utc)
    archived = True
    archived_at = DateTime(2021, 5, 14, tzinfo = TimeZone.utc)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180031
    slowmode = 60
    
    channel_metadata = ChannelMetadataGuildThreadAnnouncements(
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



def test__ChannelMetadataGuildThreadAnnouncements__hash():
    """
    Tests whether ``.ChannelMetadataGuildThreadAnnouncements.__hash__`` works as intended.
    """
    parent_id = 202209180102
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14, tzinfo = TimeZone.utc)
    archived = True
    archived_at = DateTime(2021, 5, 14, tzinfo = TimeZone.utc)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180103
    slowmode = 60
    
    channel_metadata = ChannelMetadataGuildThreadAnnouncements(
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


def test__ChannelMetadataGuildThreadAnnouncements__eq():
    """
    Tests whether ``.ChannelMetadataGuildThreadAnnouncements.__eq__`` works as intended.
    """
    parent_id = 202209180032
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14, tzinfo = TimeZone.utc)
    archived = True
    archived_at = DateTime(2021, 5, 14, tzinfo = TimeZone.utc)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180033
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
    channel_metadata = ChannelMetadataGuildThreadAnnouncements(**keyword_parameters)
    
    vampytest.assert_eq(channel_metadata, channel_metadata)
    vampytest.assert_ne(channel_metadata, object())
    
    for field_name, field_value in (
        ('parent_id', 202209180034),
        ('name', 'Okuu'),
        ('created_at', DateTime(2020, 9, 9, tzinfo = TimeZone.utc)),
        ('archived', False),
        ('archived_at', DateTime(2021, 9, 9, tzinfo = TimeZone.utc)),
        ('auto_archive_after', 3600),
        ('open', False),
        ('owner_id', 202209180035),
        ('slowmode', 69),
    ):
        test_channel_metadata = ChannelMetadataGuildThreadAnnouncements(**{**keyword_parameters, field_name: field_value})
        
        vampytest.assert_ne(channel_metadata, test_channel_metadata)
