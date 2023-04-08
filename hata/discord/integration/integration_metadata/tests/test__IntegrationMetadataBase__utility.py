import vampytest

from ..base import IntegrationMetadataBase

from .test__IntegrationMetadataBase__constructor import _assert_fields_set


def test__IntegrationMetadataBase__copy():
    """
    Tests whether ``IntegrationMetadataBase.copy`` works as intended.
    """
    integration_metadata = IntegrationMetadataBase()
    copy = integration_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, integration_metadata)
    vampytest.assert_is_not(copy, integration_metadata)


def test__IntegrationMetadataBase__copy_with__0():
    """
    Tests whether ``IntegrationMetadataBase.copy_with`` works as intended.
    
    Case: No fields given.
    """
    integration_metadata = IntegrationMetadataBase()
    copy = integration_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, integration_metadata)
    vampytest.assert_is_not(copy, integration_metadata)


def test__IntegrationMetadataBase__copy_with_keyword_parameters__0():
    """
    Tests whether ``IntegrationMetadataBase.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    integration_metadata = IntegrationMetadataBase()
    copy = integration_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, integration_metadata)
    vampytest.assert_is_not(copy, integration_metadata)
