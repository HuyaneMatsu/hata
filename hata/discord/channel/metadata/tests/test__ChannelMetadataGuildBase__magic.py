import vampytest

from .. import ChannelMetadataGuildBase


def test__ChannelMetadataGuildBase__repr():
    """
    Tests whether ``.ChannelMetadataGuildBase.__repr__`` works as intended.
    """
    parent_id = 202209170006
    name = 'Armelyrics'
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
    }
    channel_metadata = ChannelMetadataGuildBase(keyword_parameters)
    
    vampytest.assert_instance(repr(channel_metadata), str)


def test__ChannelMetadataGuildBase__hash():
    """
    Tests whether ``.ChannelMetadataGuildBase.__hash__`` works as intended.
    """
    parent_id = 202209180084
    name = 'Armelyrics'
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
    }
    channel_metadata = ChannelMetadataGuildBase(keyword_parameters)
    
    vampytest.assert_instance(hash(channel_metadata), int)


def test__ChannelMetadataGuildBase__eq():
    """
    Tests whether ``.ChannelMetadataGuildBase.__eq__`` works as intended.
    """
    parent_id = 202209170007
    name = 'Armelyrics'
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
    }
    channel_metadata = ChannelMetadataGuildBase(keyword_parameters)
    
    vampytest.assert_eq(channel_metadata, channel_metadata)
    vampytest.assert_ne(channel_metadata, object())
    
    for field_name, field_value in (
        ('parent_id', 202209170008),
        ('name', 'Okuu'),
    ):
        test_channel_metadata = ChannelMetadataGuildBase({**keyword_parameters, field_name: field_value})
        
        vampytest.assert_ne(channel_metadata, test_channel_metadata)
