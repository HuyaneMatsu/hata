import vampytest

from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..guild_main_base import ChannelMetadataGuildMainBase


def test__ChannelMetadataGuildMainBase__repr():
    """
    Tests whether ``.ChannelMetadataGuildMainBase.__repr__`` works as intended.
    """
    parent_id = 202209170023
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170025, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
    }
    channel_metadata = ChannelMetadataGuildMainBase(keyword_parameters)
    
    vampytest.assert_instance(repr(channel_metadata), str)



def test__ChannelMetadataGuildMainBase__hash():
    """
    Tests whether ``.ChannelMetadataGuildMainBase.__hash__`` works as intended.
    """
    parent_id = 202209180092
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209180093, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
    }
    channel_metadata = ChannelMetadataGuildMainBase(keyword_parameters)
    
    vampytest.assert_instance(hash(channel_metadata), int)


def test__ChannelMetadataGuildMainBase__eq():
    """
    Tests whether ``.ChannelMetadataGuildMainBase.__eq__`` works as intended.
    """
    parent_id = 202209170024
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170026, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
    }
    channel_metadata = ChannelMetadataGuildMainBase(keyword_parameters)
    
    vampytest.assert_eq(channel_metadata, channel_metadata)
    vampytest.assert_ne(channel_metadata, object())
    
    for field_name, field_value in (
        ('parent_id', 202209170027),
        ('name', 'Okuu'),
        (
            'permission_overwrites',
            [
                PermissionOverwrite(202209170028, target_type = PermissionOverwriteTargetType.role)
            ],
        ),
        ('position', 6),
    ):
        test_channel_metadata = ChannelMetadataGuildMainBase({**keyword_parameters, field_name: field_value})
        
        vampytest.assert_ne(channel_metadata, test_channel_metadata)
