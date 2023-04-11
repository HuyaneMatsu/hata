from datetime import datetime as DateTime

import vampytest

from ..guild_thread_private import ChannelMetadataGuildThreadPrivate


def test__ChannelMetadataGuildThreadPrivate__repr():
    """
    Tests whether ``.ChannelMetadataGuildThreadPrivate.__repr__`` works as intended.
    """
    parent_id = 202209180048
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14)
    archived = True
    archived_at = DateTime(2021, 5, 14)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180049
    slowmode = 60
    invitable = True
    
    channel_metadata = ChannelMetadataGuildThreadPrivate(
        parent_id = parent_id,
        name = name,
        created_at = created_at,
        archived = archived,
        archived_at = archived_at,
        auto_archive_after = auto_archive_after,
        open = open_,
        owner_id = owner_id,
        slowmode = slowmode,
        invitable = invitable,
    )
    
    vampytest.assert_instance(repr(channel_metadata), str)


def test__ChannelMetadataGuildThreadPrivate__hash():
    """
    Tests whether ``.ChannelMetadataGuildThreadPrivate.__hash__`` works as intended.
    """
    parent_id = 202209180106
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14)
    archived = True
    archived_at = DateTime(2021, 5, 14)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180107
    slowmode = 60
    invitable = True
    
    channel_metadata = ChannelMetadataGuildThreadPrivate(
        parent_id = parent_id,
        name = name,
        created_at = created_at,
        archived = archived,
        archived_at = archived_at,
        auto_archive_after = auto_archive_after,
        open = open_,
        owner_id = owner_id,
        slowmode = slowmode,
        invitable = invitable,
    )
    
    vampytest.assert_instance(hash(channel_metadata), int)


def test__ChannelMetadataGuildThreadPrivate__eq():
    """
    Tests whether ``.ChannelMetadataGuildThreadPrivate.__eq__`` works as intended.
    """
    parent_id = 202209180050
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14)
    archived = True
    archived_at = DateTime(2021, 5, 14)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180051
    slowmode = 60
    invitable = True
    
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
        'invitable': invitable,
    }
    channel_metadata = ChannelMetadataGuildThreadPrivate(**keyword_parameters)
    
    vampytest.assert_eq(channel_metadata, channel_metadata)
    vampytest.assert_ne(channel_metadata, object())
    
    for field_name, field_value in (
        ('parent_id', 202209180052),
        ('name', 'Okuu'),
        ('created_at', DateTime(2020, 9, 9)),
        ('archived', False),
        ('archived_at', DateTime(2021, 9, 9)),
        ('auto_archive_after', 3600),
        ('open', False),
        ('owner_id', 202209180053),
        ('slowmode', 69),
        ('invitable', False),
    ):
        test_channel_metadata = ChannelMetadataGuildThreadPrivate(**{**keyword_parameters, field_name: field_value})
        
        vampytest.assert_ne(channel_metadata, test_channel_metadata)
