import vampytest

from ....guild import VoiceRegion
from ....permission import PermissionOverwrite, PermissionOverwriteTargetType

from .. import ChannelMetadataGuildVoiceBase


def test__ChannelMetadataGuildVoiceBase__repr():
    """
    Tests whether ``.ChannelMetadataGuildVoiceBase.__repr__`` works as intended.
    """
    parent_id = 202209170140
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170141, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'bitrate': bitrate,
        'region': region,
        'user_limit': user_limit,
    }
    channel_metadata = ChannelMetadataGuildVoiceBase(keyword_parameters)
    
    vampytest.assert_instance(repr(channel_metadata), str)


def test__ChannelMetadataGuildVoiceBase__eq():
    """
    Tests whether ``.ChannelMetadataGuildVoiceBase.__eq__`` works as intended.
    """
    parent_id = 202209170142
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170143, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'bitrate': bitrate,
        'region': region,
        'user_limit': user_limit,
    }
    channel_metadata = ChannelMetadataGuildVoiceBase(keyword_parameters)
    
    vampytest.assert_eq(channel_metadata, channel_metadata)
    vampytest.assert_ne(channel_metadata, object())
    
    for field_name, field_value in (
        ('parent_id', 202209170144),
        ('name', 'Okuu'),
        (
            'permission_overwrites',
            [
                PermissionOverwrite(202209170146, target_type = PermissionOverwriteTargetType.role)
            ],
        ),
        ('position', 6),
        ('bitrate', 60000),
        ('region', VoiceRegion.india),
        ('user_limit', 5),
    ):
        test_channel_metadata = ChannelMetadataGuildVoiceBase({**keyword_parameters, field_name: field_value})
        
        vampytest.assert_ne(channel_metadata, test_channel_metadata)
