import vampytest

from ..guild_base import ChannelMetadataGuildBase

from .test__ChannelMetadataGuildBase__constructor import _assert_fields_set


def test__ChannelMetadataGuildBase__copy():
    """
    Tests whether ``ChannelMetadataGuildBase.copy` works as intended.
    """
    name = 'alice'
    parent_id = 202304120040
    
    channel_metadata = ChannelMetadataGuildBase(
        name = name,
        parent_id = parent_id,
    )
    
    copy = channel_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildBase__copy_with__0():
    """
    Tests whether ``ChannelMetadataGuildBase.copy_with` works as intended.
    
    Case: No fields.
    """
    name = 'alice'
    parent_id = 202304120041
    
    channel_metadata = ChannelMetadataGuildBase(
        name = name,
        parent_id = parent_id,
    )
    
    copy = channel_metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildBase__copy_with__1():
    """
    Tests whether ``ChannelMetadataGuildBase.copy_with` works as intended.
    
    Case: All fields.
    """
    old_name = 'alice'
    old_parent_id = 202304120042
    
    new_name = 'emotion'
    new_parent_id = 202304120043
    
    channel_metadata = ChannelMetadataGuildBase(
        name = old_name,
        parent_id = old_parent_id,
    )
    
    copy = channel_metadata.copy_with(
        name = new_name,
        parent_id = new_parent_id,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.parent_id, new_parent_id)


def test__ChannelMetadataGuildBase__copy_with_keyword_parameters__0():
    """
    Tests whether ``ChannelMetadataGuildBase.copy_with_keyword_parameters` works as intended.
    
    Case: No fields.
    """
    name = 'alice'
    parent_id = 202304120044
    
    channel_metadata = ChannelMetadataGuildBase(
        name = name,
        parent_id = parent_id,
    )
    
    keyword_parameters = {}
    copy = channel_metadata.copy_with_keyword_parameters(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildBase__copy_with_keyword_parameters__1():
    """
    Tests whether ``ChannelMetadataGuildBase.copy_with_keyword_parameters` works as intended.
    
    Case: All fields.
    """
    old_name = 'alice'
    old_parent_id = 202304120045
    
    new_name = 'emotion'
    new_parent_id = 202304120046
    
    channel_metadata = ChannelMetadataGuildBase(
        name = old_name,
        parent_id = old_parent_id,
    )
    
    keyword_parameters = {
        'name': new_name,
        'parent_id': new_parent_id,
    }
    
    copy = channel_metadata.copy_with_keyword_parameters(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.parent_id, new_parent_id)
