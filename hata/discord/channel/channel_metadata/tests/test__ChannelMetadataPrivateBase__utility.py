import vampytest

from ....user import User

from ..private_base import ChannelMetadataPrivateBase

from .test__ChannelMetadataPrivateBase__constructor import _assert_fields_set


def test__ChannelMetadataPrivateBase__copy():
    """
    Tests whether ``ChannelMetadataPrivateBase.copy` works as intended.
    """
    users = [User.precreate(202304120000)]
    
    channel_metadata = ChannelMetadataPrivateBase(
        users = users,
    )
    
    copy = channel_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataPrivateBase__copy_with__0():
    """
    Tests whether ``ChannelMetadataPrivateBase.copy_with` works as intended.
    
    Case: No fields.
    """
    users = [User.precreate(202304120001)]
    
    channel_metadata = ChannelMetadataPrivateBase(
        users = users,
    )
    
    copy = channel_metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataPrivateBase__copy_with__1():
    """
    Tests whether ``ChannelMetadataPrivateBase.copy_with` works as intended.
    
    Case: All fields.
    """
    old_users = [User.precreate(202304120002)]
    new_users = [User.precreate(202304120003), User.precreate(202304120004)]
    
    channel_metadata = ChannelMetadataPrivateBase(
        users = old_users,
    )
    
    copy = channel_metadata.copy_with(
        users = new_users,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy.users, new_users)


def test__ChannelMetadataPrivateBase__copy_with_keyword_parameters__0():
    """
    Tests whether ``ChannelMetadataPrivateBase.copy_with_keyword_parameters` works as intended.
    
    Case: No fields.
    """
    users = [User.precreate(202304120005)]
    
    channel_metadata = ChannelMetadataPrivateBase(
        users = users,
    )
    
    keyword_parameters = {}
    copy = channel_metadata.copy_with_keyword_parameters(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataPrivateBase__copy_with_keyword_parameters__1():
    """
    Tests whether ``ChannelMetadataPrivateBase.copy_with_keyword_parameters` works as intended.
    
    Case: All fields.
    """
    old_users = [User.precreate(202304120006)]
    new_users = [User.precreate(202304120007), User.precreate(202304120008)]
    
    channel_metadata = ChannelMetadataPrivateBase(
        users = old_users,
    )
    
    keyword_parameters = {
        'users': new_users,
    }
    
    copy = channel_metadata.copy_with_keyword_parameters(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(copy.users, new_users)
