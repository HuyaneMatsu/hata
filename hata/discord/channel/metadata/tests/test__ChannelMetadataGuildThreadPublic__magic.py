from datetime import datetime as DateTime

import vampytest

from ...flags import ChannelFlag

from .. import ChannelMetadataGuildThreadPublic


def test__ChannelMetadataGuildThreadPublic__repr():
    """
    Tests whether ``.ChannelMetadataGuildThreadPublic.__repr__`` works as intended.
    """
    parent_id = 202209180065
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14)
    archived = True
    archived_at = DateTime(2021, 5, 14)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180066
    slowmode = 60
    applied_tag_ids = [202209180080]
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
    channel_metadata = ChannelMetadataGuildThreadPublic(keyword_parameters)
    
    vampytest.assert_instance(repr(channel_metadata), str)


def test__ChannelMetadataGuildThreadPublic__hash():
    """
    Tests whether ``.ChannelMetadataGuildThreadPublic.__hash__`` works as intended.
    """
    parent_id = 202209180108
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14)
    archived = True
    archived_at = DateTime(2021, 5, 14)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180109
    slowmode = 60
    applied_tag_ids = [202209180110]
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
    channel_metadata = ChannelMetadataGuildThreadPublic(keyword_parameters)
    
    vampytest.assert_instance(hash(channel_metadata), int)


def test__ChannelMetadataGuildThreadPublic__eq():
    """
    Tests whether ``.ChannelMetadataGuildThreadPublic.__eq__`` works as intended.
    """
    parent_id = 202209180067
    name = 'Armelyrics'
    created_at = DateTime(2020, 5, 14)
    archived = True
    archived_at = DateTime(2021, 5, 14)
    auto_archive_after = 86400
    open_ = True
    owner_id = 202209180068
    slowmode = 60
    applied_tag_ids = [202209180081]
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
    channel_metadata = ChannelMetadataGuildThreadPublic(keyword_parameters)
    
    vampytest.assert_eq(channel_metadata, channel_metadata)
    vampytest.assert_ne(channel_metadata, object())
    
    for field_name, field_value in (
        ('parent_id', 202209180069),
        ('name', 'Okuu'),
        ('created_at', DateTime(2020, 9, 9)),
        ('archived', False),
        ('archived_at', DateTime(2021, 9, 9)),
        ('auto_archive_after', 3600),
        ('open', False),
        ('owner_id', 202209180069),
        ('slowmode', 69),
        ('applied_flag_ids', None),
        ('flags', ChannelFlag(6)),
    ):
        test_channel_metadata = ChannelMetadataGuildThreadPublic({**keyword_parameters, field_name: field_value})
        
        vampytest.assert_ne(channel_metadata, test_channel_metadata)
