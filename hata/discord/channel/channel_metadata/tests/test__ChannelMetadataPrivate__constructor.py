import vampytest

from ....user import User

from ..private import ChannelMetadataPrivate


def _assert_fields_set(channel_metadata):
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivate)
    
    vampytest.assert_instance(channel_metadata.users, list)


def test__ChannelMetadataPrivate__new__0():
    """
    Tests whether ``ChannelMetadataPrivate.__new__`` works as intended.
    
    Case: all fields given.
    """
    users = [User.precreate(202209160000)]
    
    channel_metadata = ChannelMetadataPrivate(
        users = users,
    )
    _assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.users, users)


def test__ChannelMetadataPrivate__new__1():
    """
    Tests whether ``ChannelMetadataPrivate.__new__`` works as intended.
    
    Case: no fields given.
    """
    channel_metadata = ChannelMetadataPrivate()
    _assert_fields_set(channel_metadata)


def test__ChannelMetadataPrivate__from_keyword_parameters__0():
    """
    Tests whether ``ChannelMetadataPrivate.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    users = [User.precreate(202304110026)]
    
    keyword_parameters = {
        'users': users,
    }
    
    channel_metadata = ChannelMetadataPrivate.from_keyword_parameters(keyword_parameters)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(channel_metadata.users, users)


def test__ChannelMetadataPrivate__from_keyword_parameters__1():
    """
    Tests whether ``ChannelMetadataPrivate.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataPrivate.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})


def test__ChannelMetadataPrivate__create_empty():
    """
    Tests whether ``ChannelMetadataPrivate._create_empty`` works as intended.
    """
    channel_metadata = ChannelMetadataPrivate._create_empty()
    _assert_fields_set(channel_metadata)
