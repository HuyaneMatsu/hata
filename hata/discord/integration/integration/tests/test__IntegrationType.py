import vampytest

from ...integration_metadata import IntegrationMetadataBase

from ..preinstanced import IntegrationType


def _assert_fields_set(integration_type):
    """
    Asserts whether every field are set of the given integration type.
    
    Parameters
    ----------
    integration_type : ``IntegrationType``
        The instance to test.
    """
    vampytest.assert_instance(integration_type, IntegrationType)
    vampytest.assert_instance(integration_type.name, str)
    vampytest.assert_instance(integration_type.value, IntegrationType.VALUE_TYPE)
    vampytest.assert_subtype(integration_type.metadata_type, IntegrationMetadataBase)


@vampytest.call_from(IntegrationType.INSTANCES.values())
def test__IntegrationType__instances(instance):
    """
    Tests whether ``IntegrationType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``IntegrationType``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__IntegrationType__new__min_fields():
    """
    Tests whether ``IntegrationType.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 'koishi'
    
    try:
        output = IntegrationType(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, value)
        vampytest.assert_is(output.metadata_type, IntegrationMetadataBase)
        vampytest.assert_is(IntegrationType.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del IntegrationType.INSTANCES[value]
        except KeyError:
            pass
