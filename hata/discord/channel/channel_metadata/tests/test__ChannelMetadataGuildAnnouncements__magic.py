import vampytest

from ....permission import PermissionOverwrite, PermissionOverwriteTargetType

from ..guild_announcements import ChannelMetadataGuildAnnouncements


def test__ChannelMetadataGuildAnnouncements__repr():
    """
    Tests whether ``.ChannelMetadataGuildAnnouncements.__repr__`` works as intended.
    """
    parent_id = 202209170246
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170247, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    default_thread_auto_archive_after = 86400
    default_thread_slowmode = 60
    nsfw = True
    slowmode = 30
    topic = 'rin'
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'default_thread_auto_archive_after': default_thread_auto_archive_after,
        'default_thread_slowmode': default_thread_slowmode,
        'nsfw': nsfw,
        'slowmode': slowmode,
        'topic': topic,
    }
    channel_metadata = ChannelMetadataGuildAnnouncements(keyword_parameters)
    
    vampytest.assert_instance(repr(channel_metadata), str)


def test__ChannelMetadataGuildAnnouncements__hash():
    """
    Tests whether ``.ChannelMetadataGuildAnnouncements.__hash__`` works as intended.
    """
    parent_id = 202209180082
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209180083, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    default_thread_auto_archive_after = 86400
    default_thread_slowmode = 60
    nsfw = True
    slowmode = 30
    topic = 'rin'
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'default_thread_auto_archive_after': default_thread_auto_archive_after,
        'default_thread_slowmode': default_thread_slowmode,
        'nsfw': nsfw,
        'slowmode': slowmode,
        'topic': topic,
    }
    channel_metadata = ChannelMetadataGuildAnnouncements(keyword_parameters)
    
    vampytest.assert_instance(hash(channel_metadata), int)


def test__ChannelMetadataGuildAnnouncements__eq():
    """
    Tests whether ``.ChannelMetadataGuildAnnouncements.__eq__`` works as intended.
    """
    parent_id = 202209170248
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170249, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    default_thread_auto_archive_after = 86400
    default_thread_slowmode = 60
    nsfw = True
    slowmode = 30
    topic = 'rin'
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'default_thread_auto_archive_after': default_thread_auto_archive_after,
        'default_thread_slowmode': default_thread_slowmode,
        'nsfw': nsfw,
        'slowmode': slowmode,
        'topic': topic,
    }
    channel_metadata = ChannelMetadataGuildAnnouncements(keyword_parameters)
    
    vampytest.assert_eq(channel_metadata, channel_metadata)
    vampytest.assert_ne(channel_metadata, object())
    
    for field_name, field_value in (
        ('parent_id', 202209170250),
        ('name', 'Okuu'),
        (
            'permission_overwrites',
            [
                PermissionOverwrite(202209170251, target_type = PermissionOverwriteTargetType.role)
            ],
        ),
        ('position', 6),
        ('default_thread_auto_archive_after', 3600),
        ('default_thread_slowmode', 69),
        ('nsfw', False),
        ('slowmode', slowmode),
        ('topic', 'orin')
    ):
        test_channel_metadata = ChannelMetadataGuildAnnouncements({**keyword_parameters, field_name: field_value})
        
        vampytest.assert_ne(channel_metadata, test_channel_metadata)
