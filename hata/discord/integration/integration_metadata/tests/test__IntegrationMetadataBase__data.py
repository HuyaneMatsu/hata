import vampytest

from ..base import IntegrationMetadataBase

from .test__IntegrationMetadataBase__constructor import _assert_fields_set


def test__IntegrationMetadataBase__from_data__0():
    """
    Tests whether ``IntegrationMetadataBase.from_data`` works as intended.
    
    Case: non-discord integration.
    """
    data = {}
    
    integration_metadata = IntegrationMetadataBase.from_data(data)
    
    _assert_fields_set(integration_metadata)


def test__IntegrationMetadataBase__to_data():
    """
    Tests whether ``IntegrationMetadataBase.to_data`` works as intended.
    
    Case: defaults.
    """
    integration_metadata = IntegrationMetadataBase()
    
    expected_data = {}
    
    vampytest.assert_eq(
        integration_metadata.to_data(
            defaults = True,
        ),
        expected_data,
    )
