import vampytest

from ....user import User

from .. import ChannelMetadataPrivateBase


def assert_fields_set(channel_metadata):
    vampytest.assert_instance(channel_metadata.users, list)
    

def test__ChannelMetadataPrivateBase__new__0():
    """
    Tests whether ``ChannelMetadataPrivateBase.__new__`` works as intended.
    
    Case: all fields given.
    """
    users = [User.precreate(202209150005)]
    
    
    keyword_parameters = {'users': users}
    
    channel_metadata = ChannelMetadataPrivateBase(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivateBase)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.users, users)


def test__ChannelMetadataPrivateBase__new__1():
    """
    Tests whether ``ChannelMetadataPrivateBase.__new__`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataPrivateBase(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivateBase)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)


def test__ChannelMetadataPrivateBase__create_empty():
    """
    Tests whether ``ChannelMetadataPrivateBase._create_empty`` works as intended.
    """
    channel_metadata = ChannelMetadataPrivateBase._create_empty()
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivateBase)
    
    assert_fields_set(channel_metadata)


def test__ChannelMetadataPrivateBase__precreate__0():
    """
    Tests whether ``ChannelMetadataPrivateBase.precreate`` works as intended.
    
    Case: all fields given.
    """
    users = [User.precreate(202209150006)]
    
    keyword_parameters = {'users': users}
    
    channel_metadata = ChannelMetadataPrivateBase.precreate(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivateBase)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.users, users)


def test__ChannelMetadataPrivateBase__precreate__1():
    """
    Tests whether ``ChannelMetadataPrivateBase.precreate`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataPrivateBase.precreate(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivateBase)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)
