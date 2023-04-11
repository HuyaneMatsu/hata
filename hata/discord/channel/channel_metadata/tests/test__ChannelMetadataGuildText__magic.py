import vampytest

from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..guild_text import ChannelMetadataGuildText


def test__ChannelMetadataGuildText__repr():
    """
    Tests whether ``.ChannelMetadataGuildText.__repr__`` works as intended.
    """
    parent_id = 202209170225
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170226, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    default_thread_auto_archive_after = 86400
    default_thread_slowmode = 60
    nsfw = True
    slowmode = 30
    topic = 'rin'
    
    channel_metadata = ChannelMetadataGuildText(
        parent_id = parent_id,
        name = name,
        permission_overwrites = permission_overwrites,
        position = position,
        default_thread_auto_archive_after = default_thread_auto_archive_after,
        default_thread_slowmode = default_thread_slowmode,
        nsfw = nsfw,
        slowmode = slowmode,
        topic = topic,
    )
    
    vampytest.assert_instance(repr(channel_metadata), str)


def test__ChannelMetadataGuildText__hash():
    """
    Tests whether ``.ChannelMetadataGuildText.__hash__`` works as intended.
    """
    parent_id = 202209180098
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209180099, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    default_thread_auto_archive_after = 86400
    default_thread_slowmode = 60
    nsfw = True
    slowmode = 30
    topic = 'rin'
    
    channel_metadata = ChannelMetadataGuildText(
        parent_id = parent_id,
        name = name,
        permission_overwrites = permission_overwrites,
        position = position,
        default_thread_auto_archive_after = default_thread_auto_archive_after,
        default_thread_slowmode = default_thread_slowmode,
        nsfw = nsfw,
        slowmode = slowmode,
        topic = topic,
    )
    
    vampytest.assert_instance(hash(channel_metadata), int)


def test__ChannelMetadataGuildText__eq():
    """
    Tests whether ``.ChannelMetadataGuildText.__eq__`` works as intended.
    """
    parent_id = 202209170227
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170228, target_type = PermissionOverwriteTargetType.user)
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
    channel_metadata = ChannelMetadataGuildText(**keyword_parameters)
    
    vampytest.assert_eq(channel_metadata, channel_metadata)
    vampytest.assert_ne(channel_metadata, object())
    
    for field_name, field_value in (
        ('parent_id', 202209170229),
        ('name', 'Okuu'),
        (
            'permission_overwrites',
            [
                PermissionOverwrite(202209170230, target_type = PermissionOverwriteTargetType.role)
            ],
        ),
        ('position', 6),
        ('default_thread_auto_archive_after', 3600),
        ('default_thread_slowmode', 69),
        ('nsfw', False),
        ('slowmode', 31),
        ('topic', 'orin')
    ):
        test_channel_metadata = ChannelMetadataGuildText(**{**keyword_parameters, field_name: field_value})
        
        vampytest.assert_ne(channel_metadata, test_channel_metadata)
