import vampytest

from .. import ChannelMetadataGuildBase


def assert_fields_set(channel_metadata):    
    vampytest.assert_instance(channel_metadata.parent_id, int)
    vampytest.assert_instance(channel_metadata.name, str)
    vampytest.assert_instance(channel_metadata._permission_cache, dict, nullable = True)


def test__ChannelMetadataGuildBase__new__0():
    """
    Tests whether ``ChannelMetadataGuildBase.__new__`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202209160023
    name = 'Armelyrics'
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
    }
    channel_metadata = ChannelMetadataGuildBase(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildBase)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.parent_id, parent_id)
    vampytest.assert_eq(channel_metadata.name, name)


def test__ChannelMetadataGuildBase__new__1():
    """
    Tests whether ``ChannelMetadataGuildBase.__new__`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataGuildBase(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildBase)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)


def test__ChannelMetadataGuildBase__create_empty():
    """
    Tests whether ``ChannelMetadataGuildBase._create_empty`` works as intended.
    """
    channel_metadata = ChannelMetadataGuildBase._create_empty()
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildBase)
    
    assert_fields_set(channel_metadata)



def test__ChannelMetadataGuildBase__precreate__0():
    """
    Tests whether ``ChannelMetadataGuildBase.precreate`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202209160024
    name = 'Armelyrics'
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name
    }
    
    channel_metadata = ChannelMetadataGuildBase.precreate(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildBase)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.parent_id, parent_id)
    vampytest.assert_eq(channel_metadata.name, name)


def test__ChannelMetadataGuildBase__precreate__1():
    """
    Tests whether ``ChannelMetadataGuildBase.precreate`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataGuildBase.precreate(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildBase)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)
