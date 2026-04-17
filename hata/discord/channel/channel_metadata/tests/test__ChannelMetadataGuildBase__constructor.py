import vampytest

from ..guild_base import ChannelMetadataGuildBase


def _assert_fields_set(channel_metadata):
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildBase)
    
    vampytest.assert_instance(channel_metadata.parent_id, int)
    vampytest.assert_instance(channel_metadata.name, str)
    vampytest.assert_instance(channel_metadata._cache_permission, dict, nullable = True)


def test__ChannelMetadataGuildBase__new__0():
    """
    Tests whether ``ChannelMetadataGuildBase.__new__`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202209160023
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataGuildBase(
        parent_id = parent_id,
        name = name,
    )
    
    _assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.parent_id, parent_id)
    vampytest.assert_eq(channel_metadata.name, name)


def test__ChannelMetadataGuildBase__new__1():
    """
    Tests whether ``ChannelMetadataGuildBase.__new__`` works as intended.
    
    Case: no fields given.
    """
    channel_metadata = ChannelMetadataGuildBase()
    _assert_fields_set(channel_metadata)


def test__ChannelMetadataGuildBase__from_keyword_parameters__0():
    """
    Tests whether ``ChannelMetadataGuildBase.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202304110002
    name = 'Armelyrics'
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
    }
    channel_metadata = ChannelMetadataGuildBase.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(channel_metadata.parent_id, parent_id)
    vampytest.assert_eq(channel_metadata.name, name)


def test__ChannelMetadataGuildBase__from_keyword_parameters__1():
    """
    Tests whether ``ChannelMetadataGuildBase.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataGuildBase.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})


def test__ChannelMetadataGuildBase__create_empty():
    """
    Tests whether ``ChannelMetadataGuildBase._create_empty`` works as intended.
    """
    channel_metadata = ChannelMetadataGuildBase._create_empty()
    _assert_fields_set(channel_metadata)
