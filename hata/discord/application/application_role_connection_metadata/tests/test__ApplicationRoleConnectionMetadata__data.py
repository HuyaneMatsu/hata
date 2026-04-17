import vampytest

from ....localization import Locale

from ..metadata import ApplicationRoleConnectionMetadata
from ..preinstanced import ApplicationRoleConnectionMetadataType

from .test__ApplicationRoleConnectionMetadata__constructor import _assert_fields_set


def test__ApplicationRoleConnectionMetadata__from_data():
    """
    Tests whether ``ApplicationRoleConnectionMetadata.from_data`` works as intended.
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
    
    data = {
        'description': description,
        'description_localizations': {key.value: value for key, value in description_localizations.items()},
        'key': key,
        'name': name,
        'name_localizations': {key.value: value for key, value in name_localizations.items()},
        'type': metadata_type.value,
    }
    
    metadata = ApplicationRoleConnectionMetadata.from_data(data)
    _assert_fields_set(metadata)
    
    vampytest.assert_eq(metadata.description, description)
    vampytest.assert_eq(metadata.description_localizations, description_localizations)
    vampytest.assert_eq(metadata.key, key)
    vampytest.assert_eq(metadata.name, name)
    vampytest.assert_eq(metadata.name_localizations, name_localizations)
    vampytest.assert_is(metadata.type, metadata_type)


def test__ApplicationRoleConnectionMetadata__to_data():
    """
    Tests whether ``ApplicationRoleConnectionMetadata.to_data`` works as intended.
    
    Case: Include defaults.
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
    
    expected_data = {
        'description': description,
        'description_localizations': {key.value: value for key, value in description_localizations.items()},
        'key': key,
        'name': name,
        'name_localizations': {key.value: value for key, value in name_localizations.items()},
        'type': metadata_type.value,
    }
    
    vampytest.assert_eq(
        metadata.to_data(defaults = True),
        expected_data,
    )
