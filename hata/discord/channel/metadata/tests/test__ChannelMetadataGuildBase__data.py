import vampytest

from .. import ChannelMetadataGuildBase

from .test__ChannelMetadataGuildBase__constructor import assert_fields_set


def test__ChannelMetadataGuildBase__from_data():
    """
    Tests whether ``ChannelMetadataGuildBase.from_data` works as intended.
    """
    parent_id = 202209170000
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataGuildBase.from_data({
        'parent_id': str(parent_id),
        'name': name,
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildBase)
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.parent_id, parent_id)
    vampytest.assert_eq(channel_metadata.name, name)


def test__ChannelMetadataGuildBase__to_data():
    """
    Tests whether ``ChannelMetadataGuildBase.to_data`` works as intended.
    """
    parent_id = 202209170001
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataGuildBase({
        'parent_id': parent_id,
        'name': name,
    })
    
    data = channel_metadata.to_data()
    
    vampytest.assert_eq(
        data,
        {
            'parent_id': str(parent_id),
            'name': name,
        },
    )


def test__ChannelMetadataGuildBase__update_attributes():
    """
    Tests whether ``ChannelMetadataGuildBase._update_attributes`` works as intended.
    """
    old_parent_id = 202209170002
    new_parent_id = 202209170003
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    
    channel_metadata = ChannelMetadataGuildBase({
        'parent_id': old_parent_id,
        'name': old_name,
    })
    
    channel_metadata._update_attributes({
        'parent_id': str(new_parent_id),
        'name': new_name,
    })
    
    vampytest.assert_eq(channel_metadata.parent_id, new_parent_id)
    vampytest.assert_eq(channel_metadata.name, new_name)


def test__ChannelMetadataGuildBase__difference_update_attributes():
    """
    Tests whether ``ChannelMetadataGuildBase._difference_update_attributes`` works as intended.
    """
    old_parent_id = 202209170004
    new_parent_id = 202209170005
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    
    channel_metadata = ChannelMetadataGuildBase({
        'parent_id': str(old_parent_id),
        'name': old_name,
    })
    
    old_attributes = channel_metadata._difference_update_attributes({
        'parent_id': str(new_parent_id),
        'name': new_name,
    })

    vampytest.assert_eq(channel_metadata.parent_id, new_parent_id)
    vampytest.assert_eq(channel_metadata.name, new_name)
    
    vampytest.assert_in('parent_id', old_attributes)
    vampytest.assert_in('name', old_attributes)
    
    vampytest.assert_eq(old_attributes['parent_id'], old_parent_id)
    vampytest.assert_eq(old_attributes['name'], old_name)


def test__ChannelMetadataGuildBase__from_partial_data():
    """
    Tests whether ``ChannelMetadataGuildBase._from_partial_data`` works as intended.
    """
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataGuildBase._from_partial_data({
        'name': name,
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildBase)
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.name, name)
