__all__ = ('InteractionComponentMetadataRoleSelect',)

from scarletio import copy_docs, include

from .string_select import InteractionComponentMetadataStringSelect


ComponentType = include('ComponentType')


class InteractionComponentMetadataRoleSelect(InteractionComponentMetadataStringSelect):
    """
    Interaction component metadata representing a role select component.
    
    Attributes
    ----------
    custom_id : `None | str`
        Custom identifier to detect which component was clicked (or used) by the user.
    
    values : `None | str`
        The component's values defined by the user.
    """
    __slots__ = ()

    @copy_docs(InteractionComponentMetadataStringSelect.iter_custom_ids_and_values)
    def iter_custom_ids_and_values(self):
        custom_id = self.custom_id
        if (custom_id is not None):
            yield (custom_id, ComponentType.role_select, self.values)
