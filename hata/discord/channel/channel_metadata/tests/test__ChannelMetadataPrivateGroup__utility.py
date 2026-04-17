import vampytest

from ....bases import Icon, IconType
from ....user import User

from ..private_group import ChannelMetadataPrivateGroup

from .test__ChannelMetadataPrivateGroup__constructor import _assert_fields_set


def test__ChannelMetadataPrivateGroup__copy():
    """
    Tests whether ``ChannelMetadataPrivateGroup.copy` works as intended.
    """
    users = [User.precreate(202304120018)]
    application_id = 202304120019
    icon = Icon(IconType.static, 1)
    name = 'alice'
    owner_id = 202304120020
    
    channel_metadata = ChannelMetadataPrivateGroup(
        users = users,
        icon = icon,
        application_id = application_id,
        name = name,
        owner_id = owner_id,
    )
    
    copy = channel_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataPrivateGroup__copy_with__no_fields():
    """
    Tests whether ``ChannelMetadataPrivateGroup.copy_with` works as intended.
    
    Case: No fields.
    """
    users = [User.precreate(202304120021)]
    application_id = 202304120022
    icon = Icon(IconType.static, 1)
    name = 'alice'
    owner_id = 202304120023
    
    channel_metadata = ChannelMetadataPrivateGroup(
        users = users,
        application_id = application_id,
        icon = icon,
        name = name,
        owner_id = owner_id,
    )
    
    copy = channel_metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataPrivateGroup__copy_with__all_fields():
    """
    Tests whether ``ChannelMetadataPrivateGroup.copy_with` works as intended.
    
    Case: All fields.
    """
    old_users = [User.precreate(202304120024)]
    old_application_id = 202304120025
    old_icon = Icon(IconType.static, 1)
    old_name = 'alice'
    old_owner_id = 202304120002
    
    new_users = [User.precreate(202304120026), User.precreate(202304120027)]
    new_application_id = 202304120028
    new_icon = Icon(IconType.static, 2)
    new_name = 'emotion'
    new_owner_id = 202304120029
    
    channel_metadata = ChannelMetadataPrivateGroup(
        users = old_users,
        application_id = old_application_id,
        icon = old_icon,
        name = old_name,
        owner_id = old_owner_id,
    )
    
    copy = channel_metadata.copy_with(
        users = new_users,
        application_id = new_application_id,
        icon = new_icon,
        name = new_name,
        owner_id = new_owner_id,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy.users, new_users)
    vampytest.assert_eq(copy.application_id, new_application_id)
    vampytest.assert_eq(copy.icon, new_icon)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.owner_id, new_owner_id)


def test__ChannelMetadataPrivateGroup__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ChannelMetadataPrivateGroup.copy_with_keyword_parameters` works as intended.
    
    Case: No fields.
    """
    users = [User.precreate(202304120030)]
    application_id = 202304120031
    icon = Icon(IconType.static, 1)
    name = 'alice'
    owner_id = 202304120032
    
    channel_metadata = ChannelMetadataPrivateGroup(
        users = users,
        application_id = application_id,
        icon = icon,
        name = name,
        owner_id = owner_id,
    )
    
    keyword_parameters = {}
    copy = channel_metadata.copy_with_keyword_parameters(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataPrivateGroup__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``ChannelMetadataPrivateGroup.copy_with_keyword_parameters` works as intended.
    
    Case: All fields.
    """
    old_users = [User.precreate(202304120033)]
    old_application_id = 202304120034
    old_icon = Icon(IconType.static, 1)
    old_name = 'alice'
    old_owner_id = 202304120035
    
    new_users = [User.precreate(202304120036), User.precreate(202304120037)]
    new_application_id = 202304120038
    new_icon = Icon(IconType.static, 2)
    new_name = 'emotion'
    new_owner_id = 202304120039
    
    channel_metadata = ChannelMetadataPrivateGroup(
        users = old_users,
        application_id = old_application_id,
        icon = old_icon,
        name = old_name,
        owner_id = old_owner_id,
    )
    
    keyword_parameters = {
        'users': new_users,
        'application_id': new_application_id,
        'icon': new_icon,
        'name': new_name,
        'owner_id': new_owner_id,
    }
    
    copy = channel_metadata.copy_with_keyword_parameters(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(copy.users, new_users)
    vampytest.assert_eq(copy.application_id, new_application_id)
    vampytest.assert_eq(copy.icon, new_icon)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.owner_id, new_owner_id)
