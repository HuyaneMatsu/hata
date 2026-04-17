import vampytest

from ..parameter import ApplicationCommandOptionMetadataParameter

from .test__ApplicationCommandOptionMetadataParameter__constructor import _asert_fields_set


def test__ApplicationCommandOptionMetadataParameter__copy():
    """
    Tests whether ``ApplicationCommandOptionMetadataParameter.copy`` works as intended.
    """
    required = True
    
    option_metadata = ApplicationCommandOptionMetadataParameter(
        required = required,
    )
    copy = option_metadata.copy()
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(option_metadata, copy)


def test__ApplicationCommandOptionMetadataParameter__copy_with__0():
    """
    Tests whether ``ApplicationCommandOptionMetadataParameter.copy_with`` works as intended.
    
    Case: no parameters.
    """
    required = True
    
    option_metadata = ApplicationCommandOptionMetadataParameter(
        required = required,
    )
    copy = option_metadata.copy_with()
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(option_metadata, copy)


def test__ApplicationCommandOptionMetadataParameter__copy_with__1():
    """
    Tests whether ``ApplicationCommandOptionMetadataParameter.copy_with`` works as intended.
    
    Case: All field given
    """
    old_required = True
    
    new_required = False
    
    option_metadata = ApplicationCommandOptionMetadataParameter(
        required = old_required,
    )
    
    copy = option_metadata.copy_with(
        required = new_required,
    )
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(copy.required, new_required)


def test__ApplicationCommandOptionMetadataParameter__copy_with_keyword_parameters__0():
    """
    Tests whether ``ApplicationCommandOptionMetadataParameter.copy_with_keyword_parameters`` works as intended.
    
    Case: no parameters.
    """
    required = True
    
    option_metadata = ApplicationCommandOptionMetadataParameter(
        required = required,
    )
    copy = option_metadata.copy_with_keyword_parameters({})
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(option_metadata, copy)


def test__ApplicationCommandOptionMetadataParameter__copy_with_keyword_parameters__1():
    """
    Tests whether ``ApplicationCommandOptionMetadataParameter.copy_with_keyword_parameters`` works as intended.
    
    Case: All field given
    """
    old_required = True
    
    new_required = False
    
    option_metadata = ApplicationCommandOptionMetadataParameter(
        required = old_required,
    )
    
    copy = option_metadata.copy_with_keyword_parameters({
        'required': new_required,
    })
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(copy.required, new_required)
