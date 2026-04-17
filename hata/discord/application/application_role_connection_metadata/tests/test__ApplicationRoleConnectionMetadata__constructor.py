import vampytest

from ....localization import Locale

from ..metadata import ApplicationRoleConnectionMetadata
from ..preinstanced import ApplicationRoleConnectionMetadataType


def _assert_fields_set(metadata):
    """
    Asserts whether every attributes are check of the given application role connection metadata,
    """
    vampytest.assert_instance(metadata, ApplicationRoleConnectionMetadata)
    vampytest.assert_instance(metadata.description, str, nullable = True)
    vampytest.assert_instance(metadata.description_localizations, dict, nullable = True)
    vampytest.assert_instance(metadata.key, str)
    vampytest.assert_instance(metadata.name, str)
    vampytest.assert_instance(metadata.name_localizations, dict, nullable = True)
    vampytest.assert_instance(metadata.type, ApplicationRoleConnectionMetadataType)


def test__ApplicationRoleConnectionMetadata__new__0():
    """
    Tests whether ``ApplicationRoleConnectionMetadata.__new__`` works as intended.
    
    Case: Minimal parameters.
    """
    name = 'koishi'
    metadata_type = ApplicationRoleConnectionMetadataType.integer_greater_or_equal
    
    metadata = ApplicationRoleConnectionMetadata(name, metadata_type)
    _assert_fields_set(metadata)
    
    vampytest.assert_eq(metadata.description, name)
    vampytest.assert_is(metadata.description_localizations, None)
    vampytest.assert_eq(metadata.key, name)
    vampytest.assert_eq(metadata.name, name)
    vampytest.assert_is(metadata.name_localizations, None)
    vampytest.assert_is(metadata.type, metadata_type)


def test__ApplicationRoleConnectionMetadata__new__1():
    """
    Tests whether ``ApplicationRoleConnectionMetadata.__new__`` works as intended.
    
    Case: All parameters.
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
    _assert_fields_set(metadata)
    
    vampytest.assert_eq(metadata.description, description)
    vampytest.assert_eq(metadata.description_localizations, description_localizations)
    vampytest.assert_eq(metadata.key, key)
    vampytest.assert_eq(metadata.name, name)
    vampytest.assert_eq(metadata.name_localizations, name_localizations)
    vampytest.assert_is(metadata.type, metadata_type)
