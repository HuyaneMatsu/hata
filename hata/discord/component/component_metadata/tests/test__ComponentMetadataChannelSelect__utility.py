import vampytest

from ....channel import ChannelType
from ....guild import Guild

from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType

from ..channel_select import ComponentMetadataChannelSelect

from .test__ComponentMetadataChannelSelect__constructor import _assert_fields_set


def test__ComponentMetadataChannelSelect__clean_copy():
    """
    Tests whether ``ComponentMetadataChannelSelect.clean_copy`` works as intended.
    """
    guild_id = 202505030014
    guild = Guild.precreate(guild_id)
    
    channel_types = [ChannelType.private]
    custom_id = 'oriental'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202505030015)]
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    required = True
    
    component_metadata = ComponentMetadataChannelSelect(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        channel_types = channel_types,
        default_values = default_values,
        required = required,
    )
    copy = component_metadata.clean_copy(guild)
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataChannelSelect__copy():
    """
    Tests whether ``ComponentMetadataChannelSelect.copy`` works as intended.
    """
    channel_types = [ChannelType.private]
    custom_id = 'oriental'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130013)]
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    required = True
    
    component_metadata = ComponentMetadataChannelSelect(
        channel_types = channel_types,
        custom_id = custom_id,
        default_values = default_values,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        required = required,
    )
    copy = component_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataChannelSelect__copy_with__no_fields():
    """
    Tests whether ``ComponentMetadataChannelSelect.copy_with`` works as intended.
    
    Case: No fields.
    """
    channel_types = [ChannelType.private]
    custom_id = 'oriental'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130014)]
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    required = True
    
    component_metadata = ComponentMetadataChannelSelect(
        channel_types = channel_types,
        custom_id = custom_id,
        default_values = default_values,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        required = required,
    )
    copy = component_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataChannelSelect__copy_with__all_fields():
    """
    Tests whether ``ComponentMetadataChannelSelect.copy_with`` works as intended.
    
    Case: All fields.
    """
    old_channel_types = [ChannelType.private]
    old_custom_id = 'oriental'
    old_default_values = [
        EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130015),
    ]
    old_enabled = False
    old_max_values = 10
    old_min_values = 9
    old_placeholder = 'swing'
    old_required = True
    
    new_channel_types = [ChannelType.guild_text, ChannelType.guild_voice]
    new_custom_id = 'uta'
    new_default_values = [
        EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130016),
        EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130017),
    ]
    new_enabled = True
    new_max_values = 11
    new_min_values = 8
    new_placeholder = 'kotoba'
    new_required = False
    
    component_metadata = ComponentMetadataChannelSelect(
        channel_types = old_channel_types,
        custom_id = old_custom_id,
        default_values = old_default_values,
        enabled = old_enabled,
        max_values = old_max_values,
        min_values = old_min_values,
        placeholder = old_placeholder,
        required = old_required,
    )
    copy = component_metadata.copy_with(
        channel_types = new_channel_types,
        custom_id = new_custom_id,
        default_values = new_default_values,
        enabled = new_enabled,
        max_values = new_max_values,
        min_values = new_min_values,
        placeholder = new_placeholder,
        required = new_required,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.channel_types, tuple(new_channel_types))
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.default_values, tuple(new_default_values))
    vampytest.assert_eq(copy.enabled, new_enabled)
    vampytest.assert_eq(copy.max_values, new_max_values)
    vampytest.assert_eq(copy.min_values, new_min_values)
    vampytest.assert_eq(copy.placeholder, new_placeholder)
    vampytest.assert_eq(copy.required, new_required)


def test__ComponentMetadataChannelSelect__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataChannelSelect.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields.
    """
    channel_types = [ChannelType.private]
    custom_id = 'oriental'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130018)]
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    required = True
    
    component_metadata = ComponentMetadataChannelSelect(
        channel_types = channel_types,
        custom_id = custom_id,
        default_values = default_values,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        required = required,
    )
    copy = component_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataChannelSelect__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataChannelSelect.copy_with_keyword_parameters`` works as intended.
    
    Case: All fields.
    """
    old_channel_types = [ChannelType.private]
    old_custom_id = 'oriental'
    old_default_values = [
        EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130019),
    ]
    old_enabled = False
    old_max_values = 10
    old_min_values = 9
    old_placeholder = 'swing'
    old_required = True
    
    new_channel_types = [ChannelType.guild_text, ChannelType.guild_voice]
    new_custom_id = 'uta'
    new_default_values = [
        EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130020),
        EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130021),
    ]
    new_enabled = True
    new_max_values = 11
    new_min_values = 8
    new_placeholder = 'kotoba'
    new_required = False
    
    component_metadata = ComponentMetadataChannelSelect(
        channel_types = old_channel_types,
        custom_id = old_custom_id,
        default_values = old_default_values,
        enabled = old_enabled,
        max_values = old_max_values,
        min_values = old_min_values,
        placeholder = old_placeholder,
        required = old_required,
    )
    copy = component_metadata.copy_with_keyword_parameters({
        'channel_types': new_channel_types,
        'custom_id': new_custom_id,
        'default_values': new_default_values,
        'enabled': new_enabled,
        'max_values': new_max_values,
        'min_values': new_min_values,
        'placeholder': new_placeholder,
        'required': new_required,
    })
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.channel_types, tuple(new_channel_types))
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.default_values, tuple(new_default_values))
    vampytest.assert_eq(copy.enabled, new_enabled)
    vampytest.assert_eq(copy.max_values, new_max_values)
    vampytest.assert_eq(copy.min_values, new_min_values)
    vampytest.assert_eq(copy.placeholder, new_placeholder)
    vampytest.assert_eq(copy.required, new_required)
    


def _iter_options__iter_contents():
    channel_types = [ChannelType.private]
    custom_id = 'oriental'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202505030000)]
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    required = True
    
    yield (
        {},
        [],
    )
    
    yield (
        {
            'channel_types': channel_types,
            'custom_id': custom_id,
            'default_values': default_values,
            'enabled': enabled,
            'max_values': max_values,
            'min_values': min_values,
            'placeholder': placeholder,
            'required': required,
        },
        [],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__ComponentMetadataChannelSelect__iter_contents(keyword_parameters):
    """
    Tests whether ``ComponentMetadataChannelSelect.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<str>`
    """
    component_metadata = ComponentMetadataChannelSelect(**keyword_parameters)
    output = [*component_metadata.iter_contents()]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output
