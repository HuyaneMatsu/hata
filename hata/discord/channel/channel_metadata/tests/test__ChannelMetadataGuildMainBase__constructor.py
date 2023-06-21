import vampytest

from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..guild_main_base import ChannelMetadataGuildMainBase


def _assert_fields_set(channel_metadata):
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildMainBase)
    
    vampytest.assert_instance(channel_metadata.parent_id, int)
    vampytest.assert_instance(channel_metadata.name, str)
    vampytest.assert_instance(channel_metadata._cache_permission, dict, nullable = True)
    vampytest.assert_instance(channel_metadata.permission_overwrites, dict, nullable = True)
    vampytest.assert_instance(channel_metadata.position, int)


def test__ChannelMetadataGuildMainBase__new__0():
    """
    Tests whether ``ChannelMetadataGuildMainBase.__new__`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202209170009
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170011, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    
    channel_metadata = ChannelMetadataGuildMainBase(
        parent_id = parent_id,
        name = name,
        permission_overwrites = permission_overwrites,
        position = position,
    )
    _assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.parent_id, parent_id)
    vampytest.assert_eq(channel_metadata.name, name)
    vampytest.assert_eq(
        channel_metadata.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in permission_overwrites},
    )
    vampytest.assert_eq(channel_metadata.position, position)


def test__ChannelMetadataGuildMainBase__new__1():
    """
    Tests whether ``ChannelMetadataGuildMainBase.__new__`` works as intended.
    
    Case: no fields given.
    """
    channel_metadata = ChannelMetadataGuildMainBase()
    _assert_fields_set(channel_metadata)


def test__ChannelMetadataGuildMainBase__from_keyword_parameters__0():
    """
    Tests whether ``ChannelMetadataGuildMainBase.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202304110010
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202304110011, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
    }
    channel_metadata = ChannelMetadataGuildMainBase.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(channel_metadata.parent_id, parent_id)
    vampytest.assert_eq(channel_metadata.name, name)
    vampytest.assert_eq(
        channel_metadata.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in permission_overwrites},
    )
    vampytest.assert_eq(channel_metadata.position, position)


def test__ChannelMetadataGuildMainBase__from_keyword_parameters__1():
    """
    Tests whether ``ChannelMetadataGuildMainBase.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataGuildMainBase.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})


def test__ChannelMetadataGuildMainBase__create_empty():
    """
    Tests whether ``ChannelMetadataGuildMainBase._create_empty`` works as intended.
    """
    channel_metadata = ChannelMetadataGuildMainBase._create_empty()
    _assert_fields_set(channel_metadata)
