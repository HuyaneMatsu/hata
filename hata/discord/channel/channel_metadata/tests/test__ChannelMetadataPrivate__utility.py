import vampytest

from ....user import User

from ..private import ChannelMetadataPrivate

from .test__ChannelMetadataPrivate__constructor import _assert_fields_set


def test__ChannelMetadataPrivate__copy():
    """
    Tests whether ``ChannelMetadataPrivate.copy` works as intended.
    """
    users = [User.precreate(202304120009)]
    
    channel_metadata = ChannelMetadataPrivate(
        users = users,
    )
    
    copy = channel_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataPrivate__copy_with__0():
    """
    Tests whether ``ChannelMetadataPrivate.copy_with` works as intended.
    
    Case: No fields.
    """
    users = [User.precreate(202304120010)]
    
    channel_metadata = ChannelMetadataPrivate(
        users = users,
    )
    
    copy = channel_metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataPrivate__copy_with__1():
    """
    Tests whether ``ChannelMetadataPrivate.copy_with` works as intended.
    
    Case: All fields.
    """
    old_users = [User.precreate(202304120011)]
    new_users = [User.precreate(202304120012), User.precreate(202304120013)]
    
    channel_metadata = ChannelMetadataPrivate(
        users = old_users,
    )
    
    copy = channel_metadata.copy_with(
        users = new_users,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy.users, new_users)


def test__ChannelMetadataPrivate__copy_with_keyword_parameters__0():
    """
    Tests whether ``ChannelMetadataPrivate.copy_with_keyword_parameters` works as intended.
    
    Case: No fields.
    """
    users = [User.precreate(202304120014)]
    
    channel_metadata = ChannelMetadataPrivate(
        users = users,
    )
    
    keyword_parameters = {}
    copy = channel_metadata.copy_with_keyword_parameters(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataPrivate__copy_with_keyword_parameters__1():
    """
    Tests whether ``ChannelMetadataPrivate.copy_with_keyword_parameters` works as intended.
    
    Case: All fields.
    """
    old_users = [User.precreate(202304120015)]
    new_users = [User.precreate(202304120016), User.precreate(202304120017)]
    
    channel_metadata = ChannelMetadataPrivate(
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
