import vampytest

from ....permission import PermissionOverwrite, PermissionOverwriteTargetType

from ..guild_category import ChannelMetadataGuildCategory


def test__ChannelMetadataGuildCategory__repr():
    """
    Tests whether ``.ChannelMetadataGuildCategory.__repr__`` works as intended.
    """
    parent_id = 202209170045
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170046, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
    }
    channel_metadata = ChannelMetadataGuildCategory(keyword_parameters)
    
    vampytest.assert_instance(repr(channel_metadata), str)


def test__ChannelMetadataGuildCategory__hash():
    """
    Tests whether ``.ChannelMetadataGuildCategory.__hash__`` works as intended.
    """
    parent_id = 202209180085
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209180086, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
    }
    channel_metadata = ChannelMetadataGuildCategory(keyword_parameters)
    
    vampytest.assert_instance(hash(channel_metadata), int)


def test__ChannelMetadataGuildCategory__eq():
    """
    Tests whether ``.ChannelMetadataGuildCategory.__eq__`` works as intended.
    """
    parent_id = 202209170047
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170048, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
    }
    channel_metadata = ChannelMetadataGuildCategory(keyword_parameters)
    
    vampytest.assert_eq(channel_metadata, channel_metadata)
    vampytest.assert_ne(channel_metadata, object())
    
    for field_name, field_value in (
        ('parent_id', 202209170049),
        ('name', 'Okuu'),
        (
            'permission_overwrites',
            [
                PermissionOverwrite(202209170050, target_type = PermissionOverwriteTargetType.role)
            ],
        ),
        ('position', 6),
    ):
        test_channel_metadata = ChannelMetadataGuildCategory({**keyword_parameters, field_name: field_value})
        
        vampytest.assert_ne(channel_metadata, test_channel_metadata)
