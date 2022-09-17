import vampytest

from ....guild import VoiceRegion
from ....permission import PermissionOverwrite, PermissionOverwriteTargetType

from .. import ChannelMetadataGuildStage


def test__ChannelMetadataGuildStage__repr():
    """
    Tests whether ``.ChannelMetadataGuildStage.__repr__`` works as intended.
    """
    parent_id = 202209170140
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170185, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    topic = 'crimson'
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'bitrate': bitrate,
        'region': region,
        'user_limit': user_limit,
        'topic': topic,
    }
    channel_metadata = ChannelMetadataGuildStage(keyword_parameters)
    
    vampytest.assert_instance(repr(channel_metadata), str)


def test__ChannelMetadataGuildStage__eq():
    """
    Tests whether ``.ChannelMetadataGuildStage.__eq__`` works as intended.
    """
    parent_id = 202209170142
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170186, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    topic = 'crimson'
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'bitrate': bitrate,
        'region': region,
        'user_limit': user_limit,
        'topic': topic,
    }
    channel_metadata = ChannelMetadataGuildStage(keyword_parameters)
    
    vampytest.assert_eq(channel_metadata, channel_metadata)
    vampytest.assert_ne(channel_metadata, object())
    
    for field_name, field_value in (
        ('parent_id', 202209170187),
        ('name', 'Okuu'),
        (
            'permission_overwrites',
            [
                PermissionOverwrite(202209170188, target_type = PermissionOverwriteTargetType.role)
            ],
        ),
        ('position', 6),
        ('bitrate', 60000),
        ('region', VoiceRegion.india),
        ('user_limit', 5),
        ('topic', 'sky')
    ):
        test_channel_metadata = ChannelMetadataGuildStage({**keyword_parameters, field_name: field_value})
        
        vampytest.assert_ne(channel_metadata, test_channel_metadata)
