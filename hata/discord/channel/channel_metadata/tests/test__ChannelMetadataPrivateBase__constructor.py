import vampytest

from ....user import User

from ..private_base import ChannelMetadataPrivateBase


def _assert_fields_set(channel_metadata):
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivateBase)
    
    vampytest.assert_instance(channel_metadata.users, list)
    

def test__ChannelMetadataPrivateBase__new__0():
    """
    Tests whether ``ChannelMetadataPrivateBase.__new__`` works as intended.
    
    Case: all fields given.
    """
    users = [User.precreate(202209150005)]
    
    channel_metadata = ChannelMetadataPrivateBase(
        users = users,
    )
    _assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.users, users)


def test__ChannelMetadataPrivateBase__new__1():
    """
    Tests whether ``ChannelMetadataPrivateBase.__new__`` works as intended.
    
    Case: no fields given.
    """
    channel_metadata = ChannelMetadataPrivateBase()
    _assert_fields_set(channel_metadata)


def test__ChannelMetadataPrivateBase__from_keyword_parameters__0():
    """
    Tests whether ``ChannelMetadataPrivateBase.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    users = [User.precreate(202304110027)]
    
    keyword_parameters = {
        'users': users,
    }
    
    channel_metadata = ChannelMetadataPrivateBase.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(channel_metadata.users, users)


def test__ChannelMetadataPrivateBase__from_keyword_parameters__1():
    """
    Tests whether ``ChannelMetadataPrivateBase.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataPrivateBase.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})


def test__ChannelMetadataPrivateBase__create_empty():
    """
    Tests whether ``ChannelMetadataPrivateBase._create_empty`` works as intended.
    """
    channel_metadata = ChannelMetadataPrivateBase._create_empty()
    _assert_fields_set(channel_metadata)
