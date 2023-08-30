import vampytest

from ....localization import Locale

from ..metadata import ApplicationRoleConnectionMetadata
from ..preinstanced import ApplicationRoleConnectionMetadataType

from .test__ApplicationRoleConnectionMetadata__constructor import _assert_fields_set


def test__ApplicationRoleConnectionMetadata__copy():
    """
    Tests whether ``ApplicationRoleConnectionMetadata.copy`` works as intended.
    """
    description = 'komeiji'
    description_localizations = {
        Locale.german: 'hartmann',
    }
    key = 'heart'
    name = 'koishi'
    name_localizations = {
        Locale.german: 'satori',
    }
    metadata_type = ApplicationRoleConnectionMetadataType.integer_greater_or_equal
    
    metadata = ApplicationRoleConnectionMetadata(
        description = description,
        description_localizations = description_localizations,
        key = key,
        name = name,
        name_localizations = name_localizations,
        metadata_type = metadata_type,
    )
    
    copy = metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, metadata)
    vampytest.assert_eq(copy, metadata)


def test__ApplicationRoleConnectionMetadata__copy_with__0():
    """
    Tests whether ``ApplicationRoleConnectionMetadata.copy_with`` works as intended.
    
    Case: No parameters given.
    """
    description = 'komeiji'
    description_localizations = {
        Locale.german: 'hartmann',
    }
    key = 'heart'
    name = 'koishi'
    name_localizations = {
        Locale.german: 'satori',
    }
    metadata_type = ApplicationRoleConnectionMetadataType.integer_greater_or_equal
    
    metadata = ApplicationRoleConnectionMetadata(
        description = description,
        description_localizations = description_localizations,
        key = key,
        name = name,
        name_localizations = name_localizations,
        metadata_type = metadata_type,
    )
    
    copy = metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, metadata)
    vampytest.assert_eq(copy, metadata)


def test__ApplicationRoleConnectionMetadata__copy_with__1():
    """
    Tests whether ``ApplicationRoleConnectionMetadata.copy_with`` works as intended.
    
    Case: No parameters given.
    """
    old_description = 'komeiji'
    new_description = 'komeiji'
    old_description_localizations = {
        Locale.german: 'hartmann',
    }
    new_description_localizations = {
        Locale.danish: 'hartmann',
    }
    old_key = 'heart'
    new_key = 'heart'
    old_name = 'koishi'
    new_name = 'koishi'
    old_name_localizations = {
        Locale.german: 'satori',
    }
    new_name_localizations = {
        Locale.danish: 'satori',
    }
    old_metadata_type = ApplicationRoleConnectionMetadataType.integer_greater_or_equal
    new_metadata_type = ApplicationRoleConnectionMetadataType.integer_less_or_equal
    
    metadata = ApplicationRoleConnectionMetadata(
        description = old_description,
        description_localizations = old_description_localizations,
        key = old_key,
        name = old_name,
        name_localizations = old_name_localizations,
        metadata_type = old_metadata_type,
    )
    
    copy = metadata.copy_with(
        description = new_description,
        description_localizations = new_description_localizations,
        key = new_key,
        name = new_name,
        name_localizations = new_name_localizations,
        metadata_type = new_metadata_type,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, metadata)
    
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.description_localizations, new_description_localizations)
    vampytest.assert_eq(copy.key, new_key)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.name_localizations, new_name_localizations)
    vampytest.assert_is(copy.type, new_metadata_type)
