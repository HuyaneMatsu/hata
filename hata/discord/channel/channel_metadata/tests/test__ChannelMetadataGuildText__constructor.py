import vampytest

from ....permission import PermissionOverwrite, PermissionOverwriteTargetType

from ..guild_text import ChannelMetadataGuildText


def assert_fields_set(channel_metadata):
    vampytest.assert_instance(channel_metadata.parent_id, int)
    vampytest.assert_instance(channel_metadata.name, str)
    vampytest.assert_instance(channel_metadata._permission_cache, dict, nullable = True)
    vampytest.assert_instance(channel_metadata.permission_overwrites, dict, nullable = True)
    vampytest.assert_instance(channel_metadata.position, int)
    vampytest.assert_instance(channel_metadata.default_thread_auto_archive_after, int)
    vampytest.assert_instance(channel_metadata.default_thread_slowmode, int)
    vampytest.assert_instance(channel_metadata.nsfw, bool)
    vampytest.assert_instance(channel_metadata.slowmode, int)
    vampytest.assert_instance(channel_metadata.topic, str, nullable = True)


def test__ChannelMetadataGuildText__new__0():
    """
    Tests whether ``ChannelMetadataGuildText.__new__`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202209170212
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170213, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    default_thread_auto_archive_after = 86400
    default_thread_slowmode = 60
    nsfw = True
    slowmode = 30
    topic = 'rin'
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'default_thread_auto_archive_after': default_thread_auto_archive_after,
        'default_thread_slowmode': default_thread_slowmode,
        'nsfw': nsfw,
        'slowmode': slowmode,
        'topic': topic,
    }
    channel_metadata = ChannelMetadataGuildText(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildText)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)
    
    
    vampytest.assert_eq(channel_metadata.parent_id, parent_id)
    vampytest.assert_eq(channel_metadata.name, name)
    vampytest.assert_eq(
        channel_metadata.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in permission_overwrites},
    )
    vampytest.assert_eq(channel_metadata.position, position)
    vampytest.assert_eq(channel_metadata.default_thread_auto_archive_after, default_thread_auto_archive_after)
    vampytest.assert_eq(channel_metadata.default_thread_slowmode, default_thread_slowmode)
    vampytest.assert_eq(channel_metadata.nsfw, nsfw)
    vampytest.assert_eq(channel_metadata.slowmode, slowmode)
    vampytest.assert_eq(channel_metadata.topic, topic)


def test__ChannelMetadataGuildText__new__1():
    """
    Tests whether ``ChannelMetadataGuildText.__new__`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataGuildText(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildText)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)


def test__ChannelMetadataGuildText__create_empty():
    """
    Tests whether ``ChannelMetadataGuildText._create_empty`` works as intended.
    """
    channel_metadata = ChannelMetadataGuildText._create_empty()
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildText)
    
    assert_fields_set(channel_metadata)



def test__ChannelMetadataGuildText__precreate__0():
    """
    Tests whether ``ChannelMetadataGuildText.precreate`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202209170214
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170215, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    default_thread_auto_archive_after = 86400
    default_thread_slowmode = 60
    nsfw = True 
    slowmode = 30
    topic = 'rin'
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'default_thread_auto_archive_after': default_thread_auto_archive_after,
        'default_thread_slowmode': default_thread_slowmode,
        'nsfw': nsfw,
        'slowmode': slowmode,
        'topic': topic,
    }
    
    channel_metadata = ChannelMetadataGuildText.precreate(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildText)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.parent_id, parent_id)
    vampytest.assert_eq(channel_metadata.name, name)
    vampytest.assert_eq(
        channel_metadata.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in permission_overwrites},
    )
    vampytest.assert_eq(channel_metadata.position, position)
    vampytest.assert_eq(channel_metadata.default_thread_auto_archive_after, default_thread_auto_archive_after)
    vampytest.assert_eq(channel_metadata.default_thread_slowmode, default_thread_slowmode)
    vampytest.assert_eq(channel_metadata.nsfw, nsfw)
    vampytest.assert_eq(channel_metadata.slowmode, slowmode)
    vampytest.assert_eq(channel_metadata.topic, topic)


def test__ChannelMetadataGuildText__precreate__1():
    """
    Tests whether ``ChannelMetadataGuildText.precreate`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataGuildText.precreate(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildText)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)
