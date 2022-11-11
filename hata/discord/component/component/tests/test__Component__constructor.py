import vampytest

from ...component_metadata import ComponentMetadataBase

from ..component import Component
from ..preinstanced import ComponentType


def _check_is_all_field_set(component):
    """
    Checks whether all fields of the component are set.
    
    Parameters
    ----------
    component : ``Component``
        The component to check
    """
    vampytest.assert_instance(component, Component)
    vampytest.assert_instance(component.type, ComponentType)
    vampytest.assert_instance(component.metadata, ComponentMetadataBase)


def test__Component__new():
    """
    Tests whether ``Component.__new__`` works as intended.
    """
    component_type = ComponentType.button
    custom_id = 'chen'
    
    component = Component(component_type, custom_id = custom_id)
    _check_is_all_field_set(component)
    vampytest.assert_is(component.type, component_type)
    vampytest.assert_eq(component.custom_id, custom_id)
