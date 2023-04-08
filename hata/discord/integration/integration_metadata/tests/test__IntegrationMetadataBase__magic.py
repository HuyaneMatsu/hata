import vampytest

from ..base import IntegrationMetadataBase


def test__IntegrationMetadataBase__repr():
    """
    Tests whether ``IntegrationMetadataBase.__new__`` works as intended.
    
    Case: All fields given.
    """
    integration_metadata = IntegrationMetadataBase()
    
    vampytest.assert_instance(repr(integration_metadata), str)


def test__IntegrationMetadataBase__eq():
    """
    Tests whether ``IntegrationMetadataBase.__eq__`` works as intended.
    """
    keyword_parameters = {}
    
    integration_metadata = IntegrationMetadataBase(**keyword_parameters)
    
    vampytest.assert_eq(integration_metadata, integration_metadata)
    vampytest.assert_ne(integration_metadata, object())
    
    for field_name, field_value in ():
        integration_metadata_test = IntegrationMetadataBase(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(integration_metadata, integration_metadata_test)


def test__IntegrationMetadataBase__hash():
    """
    Tests whether ``IntegrationMetadataBase.__hash__`` works as intended.
    
    Case: All fields given.
    """
    integration_metadata = IntegrationMetadataBase()
    
    vampytest.assert_instance(hash(integration_metadata), int)
