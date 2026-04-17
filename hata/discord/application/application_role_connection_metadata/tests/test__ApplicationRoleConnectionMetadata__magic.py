import vampytest

from ....localization import Locale

from ..metadata import ApplicationRoleConnectionMetadata
from ..preinstanced import ApplicationRoleConnectionMetadataType


def test__ApplicationRoleConnectionMetadata__repr():
    """
    Tests whether ``ApplicationRoleConnectionMetadata.__repr__`` works as intended.
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
    
    vampytest.assert_instance(repr(metadata), str)


def test__ApplicationRoleConnectionMetadata__hash():
    """
    Tests whether ``ApplicationRoleConnectionMetadata.__hash__`` works as intended.
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
    
    vampytest.assert_instance(hash(metadata), int)


def test__ApplicationRoleConnectionMetadata__eq():
    """
    Tests whether ``ApplicationRoleConnectionMetadata.__eq__`` works as intended.
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
    
    keyword_parameters = {
        'description': description,
        'description_localizations': description_localizations,
        'key': key,
        'name': name,
        'name_localizations': name_localizations,
        'metadata_type': metadata_type,
    }
    
    metadata = ApplicationRoleConnectionMetadata(**keyword_parameters)
    vampytest.assert_eq(metadata, metadata)
    vampytest.assert_ne(metadata, object())
    
    for field_name, field_value in (
        ('description', 'septette'),
        ('description_localizations', None),
        ('key', 'for_the'),
        ('name', 'dead princess'),
        ('name_localizations', None),
        ('metadata_type', ApplicationRoleConnectionMetadataType.integer_less_or_equal),
    ):
        test_metadata = ApplicationRoleConnectionMetadata(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(metadata, test_metadata)
