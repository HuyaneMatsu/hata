__all__ = ('InteractionComponentMetadataRadioGroup',)

from scarletio import copy_docs, include

from .text_input import InteractionComponentMetadataTextInput


ComponentType = include('ComponentType')


class InteractionComponentMetadataRadioGroup(InteractionComponentMetadataTextInput):
    """
    Interaction component metadata representing a radio group component.
    
    Attributes
    ----------
    custom_id : `None | str`
        Custom identifier to detect which component was clicked (or used) by the user.
    
    value : `None | str`
        The component's value defined by the user.
    """
    __slots__ = ()
    
    @copy_docs(InteractionComponentMetadataTextInput.iter_custom_ids_and_values)
    def iter_custom_ids_and_values(self):
        custom_id = self.custom_id
        if (custom_id is not None):
            yield (custom_id, ComponentType.radio_group, self.value)
