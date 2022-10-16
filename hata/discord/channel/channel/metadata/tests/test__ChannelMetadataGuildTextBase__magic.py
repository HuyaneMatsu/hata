import vampytest

from .....permission import PermissionOverwrite, PermissionOverwriteTargetType

from ..guild_text_base import ChannelMetadataGuildTextBase


def test__ChannelMetadataGuildTextBase__repr():
    """
    Tests whether ``.ChannelMetadataGuildTextBase.__repr__`` works as intended.
    """
    parent_id = 202209170206
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170207, target_type = PermissionOverwriteTargetType.user)
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
    channel_metadata = ChannelMetadataGuildTextBase(keyword_parameters)
    
    vampytest.assert_instance(repr(channel_metadata), str)


def test__ChannelMetadataGuildTextBase__hash():
    """
    Tests whether ``.ChannelMetadataGuildTextBase.__hash__`` works as intended.
    """
    parent_id = 202209180100
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209180101, target_type = PermissionOverwriteTargetType.user)
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
    channel_metadata = ChannelMetadataGuildTextBase(keyword_parameters)
    
    vampytest.assert_instance(hash(channel_metadata), int)


def test__ChannelMetadataGuildTextBase__eq():
    """
    Tests whether ``.ChannelMetadataGuildTextBase.__eq__`` works as intended.
    """
    parent_id = 202209170208
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170209, target_type = PermissionOverwriteTargetType.user)
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
    channel_metadata = ChannelMetadataGuildTextBase(keyword_parameters)
    
    vampytest.assert_eq(channel_metadata, channel_metadata)
    vampytest.assert_ne(channel_metadata, object())
    
    for field_name, field_value in (
        ('parent_id', 2022091702010),
        ('name', 'Okuu'),
        (
            'permission_overwrites',
            [
                PermissionOverwrite(202209170211, target_type = PermissionOverwriteTargetType.role)
            ],
        ),
        ('position', 6),
        ('default_thread_auto_archive_after', 3600),
        ('default_thread_slowmode', 69),
        ('nsfw', False),
        ('slowmode', slowmode),
        ('topic', 'orin')
    ):
        test_channel_metadata = ChannelMetadataGuildTextBase({**keyword_parameters, field_name: field_value})
        
        vampytest.assert_ne(channel_metadata, test_channel_metadata)
