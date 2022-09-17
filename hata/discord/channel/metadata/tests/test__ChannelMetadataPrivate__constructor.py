import vampytest

from ....user import User

from .. import ChannelMetadataPrivate


def assert_fields_set(channel_metadata):
    vampytest.assert_instance(channel_metadata.users, list)


def test__ChannelMetadataPrivate__new__0():
    """
    Tests whether ``ChannelMetadataPrivate.__new__`` works as intended.
    
    Case: all fields given.
    """
    users = [User.precreate(202209160000)]
    
    
    keyword_parameters = {'users': users}
    
    channel_metadata = ChannelMetadataPrivate(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivate)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.users, users)


def test__ChannelMetadataPrivate__new__1():
    """
    Tests whether ``ChannelMetadataPrivate.__new__`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataPrivate(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivate)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)


def test__ChannelMetadataPrivate__create_empty():
    """
    Tests whether ``ChannelMetadataPrivate._create_empty`` works as intended.
    """
    channel_metadata = ChannelMetadataPrivate._create_empty()
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivate)
    
    assert_fields_set(channel_metadata)


def test__ChannelMetadataPrivate__precreate__0():
    """
    Tests whether ``ChannelMetadataPrivate.precreate`` works as intended.
    
    Case: all fields given.
    """
    users = [User.precreate(202209160001)]
    
    keyword_parameters = {'users': users}
    
    channel_metadata = ChannelMetadataPrivate.precreate(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivate)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.users, users)


def test__ChannelMetadataPrivate__precreate__1():
    """
    Tests whether ``ChannelMetadataPrivate.precreate`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataPrivate.precreate(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivate)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)
