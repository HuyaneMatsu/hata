import vampytest

from ..base import ApplicationCommandOptionMetadataBase

from .test__ApplicationCommandOptionMetadataBase__constructor import _asert_fields_set


def test__ApplicationCommandOptionMetadataBase__copy():
    """
    Tests whether ``ApplicationCommandOptionMetadataBase.copy`` works as intended.
    """
    option_metadata = ApplicationCommandOptionMetadataBase({
    })
    copy = option_metadata.copy()
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(option_metadata, copy)


def test__ApplicationCommandOptionMetadataBase__copy_with__0():
    """
    Tests whether ``ApplicationCommandOptionMetadataBase.copy_with`` works as intended.
    
    Case: no parameters.
    """ 
    option_metadata = ApplicationCommandOptionMetadataBase({
    })
    copy = option_metadata.copy_with({})
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
    
    vampytest.assert_eq(option_metadata, copy)


def test__ApplicationCommandOptionMetadataBase__copy_with__1():
    """
    Tests whether ``ApplicationCommandOptionMetadataBase.copy_with`` works as intended.
    
    Case: All field given
    """
    option_metadata = ApplicationCommandOptionMetadataBase({
    })
    
    copy = option_metadata.copy_with({
    })
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(option_metadata, copy)
