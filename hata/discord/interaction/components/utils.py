__all__ = ('create_auto_custom_id', 'create_component')

from base64 import b85encode as to_base85
from os import urandom as random_bytes

from scarletio import export

from .component_button import ComponentButton
from .component_dynamic import ComponentDynamic
from .component_row import ComponentRow
from .component_select import ComponentSelect
from .component_text_input import ComponentTextInput
from .preinstanced import ButtonStyle, ComponentType, TextInputStyle


@export
def create_auto_custom_id():
    """
    Creates a random custom identifier for components.
    
    Returns
    -------
    custom_id : `str`
        The created custom id.
    """
    return to_base85(random_bytes(64)).decode()


COMPONENT_TYPE_TO_STYLE = {
    ComponentType.row: None,
    ComponentType.button: ButtonStyle,
    ComponentType.select: None,
    ComponentType.text_input: TextInputStyle,
}

COMPONENT_TYPE_VALUE_TO_TYPE = {
    ComponentType.row.value: ComponentRow,
    ComponentType.button.value: ComponentButton,
    ComponentType.select.value: ComponentSelect,
    ComponentType.text_input.value: ComponentTextInput,
}

@export
def create_component(component_data):
    """
    Creates a component from the given component data.
    
    Parameters
    ----------
    component_data : `dict` of (`str`, `Any`)
        Component data.
    
    Returns
    -------
    component : ``ComponentBase``
        the created component instance.
    """
    return COMPONENT_TYPE_VALUE_TO_TYPE.get(component_data['type'], ComponentDynamic).from_data(component_data)
