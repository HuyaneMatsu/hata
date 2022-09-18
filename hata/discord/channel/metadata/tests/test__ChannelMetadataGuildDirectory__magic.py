import vampytest

from ....permission import PermissionOverwrite, PermissionOverwriteTargetType

from .. import ChannelMetadataGuildDirectory


def test__ChannelMetadataGuildDirectory__repr():
    """
    Tests whether ``.ChannelMetadataGuildDirectory.__repr__`` works as intended.
    """
    parent_id = 202209170066
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170067, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
    }
    channel_metadata = ChannelMetadataGuildDirectory(keyword_parameters)
    
    vampytest.assert_instance(repr(channel_metadata), str)


def test__ChannelMetadataGuildDirectory__hash():
    """
    Tests whether ``.ChannelMetadataGuildDirectory.__hash__`` works as intended.
    """
    parent_id = 202209180087
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209180088, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
    }
    channel_metadata = ChannelMetadataGuildDirectory(keyword_parameters)
    
    vampytest.assert_instance(hash(channel_metadata), int)


def test__ChannelMetadataGuildDirectory__eq():
    """
    Tests whether ``.ChannelMetadataGuildDirectory.__eq__`` works as intended.
    """
    parent_id = 202209170047
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170068, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
    }
    channel_metadata = ChannelMetadataGuildDirectory(keyword_parameters)
    
    vampytest.assert_eq(channel_metadata, channel_metadata)
    vampytest.assert_ne(channel_metadata, object())
    
    for field_name, field_value in (
        ('parent_id', 202209170069),
        ('name', 'Okuu'),
        (
            'permission_overwrites',
            [
                PermissionOverwrite(202209170070, target_type = PermissionOverwriteTargetType.role)
            ],
        ),
        ('position', 6),
    ):
        test_channel_metadata = ChannelMetadataGuildDirectory({**keyword_parameters, field_name: field_value})
        
        vampytest.assert_ne(channel_metadata, test_channel_metadata)
