import vampytest

from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..guild_store import ChannelMetadataGuildStore


def test__ChannelMetadataGuildStore__repr():
    """
    Tests whether ``.ChannelMetadataGuildStore.__repr__`` works as intended.
    """
    parent_id = 202209170118
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170119, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    nsfw = True
    
    channel_metadata = ChannelMetadataGuildStore(
        parent_id = parent_id,
        name = name,
        permission_overwrites = permission_overwrites,
        position = position,
        nsfw = nsfw,
    )
    
    vampytest.assert_instance(repr(channel_metadata), str)


def test__ChannelMetadataGuildStore__hash():
    """
    Tests whether ``.ChannelMetadataGuildStore.__hash__`` works as intended.
    """
    parent_id = 202209180096
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209180097, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    nsfw = True
    
    channel_metadata = ChannelMetadataGuildStore(
        parent_id = parent_id,
        name = name,
        permission_overwrites = permission_overwrites,
        position = position,
        nsfw = nsfw,
    )
    
    vampytest.assert_instance(hash(channel_metadata), int)


def test__ChannelMetadataGuildStore__eq():
    """
    Tests whether ``.ChannelMetadataGuildStore.__eq__`` works as intended.
    """
    parent_id = 202209170120
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170121, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    nsfw = True
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'nsfw': nsfw,
    }
    channel_metadata = ChannelMetadataGuildStore(**keyword_parameters)
    
    vampytest.assert_eq(channel_metadata, channel_metadata)
    vampytest.assert_ne(channel_metadata, object())
    
    for field_name, field_value in (
        ('parent_id', 202209170122),
        ('name', 'Okuu'),
        (
            'permission_overwrites',
            [
                PermissionOverwrite(202209170123, target_type = PermissionOverwriteTargetType.role)
            ],
        ),
        ('position', 6),
        ('nsfw', False),
    ):
        test_channel_metadata = ChannelMetadataGuildStore(**{**keyword_parameters, field_name: field_value})
        
        vampytest.assert_ne(channel_metadata, test_channel_metadata)
