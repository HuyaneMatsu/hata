import vampytest

from ..base import IntegrationMetadataBase


def _check_all_fields_set(integration_metadata):
    """
    Tests whether all attributes of an ``IntegrationMetadataBase`` are set.
    
    Parameters
    ----------
    integration_metadata : ``IntegrationMetadataBase``
        The integration detail to check out.
    """
    vampytest.assert_instance(integration_metadata, IntegrationMetadataBase)
        

def test__IntegrationMetadataBase__new_0():
    """
    Tests whether ``IntegrationMetadataBase.__new__`` works as intended.
    
    Case: No fields given.
    """
    keyword_parameters = {}
    
    integration_metadata = IntegrationMetadataBase(keyword_parameters)
    _check_all_fields_set(integration_metadata)
    vampytest.assert_eq(keyword_parameters, {})


def test__IntegrationMetadataBase__create_empty():
    """
    Tests whether ``IntegrationMetadataBase._create_empty`` works as intended.
    """
    integration_metadata = IntegrationMetadataBase._create_empty()
    _check_all_fields_set(integration_metadata)
