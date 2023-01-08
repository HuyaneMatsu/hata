__all__ = ('ReactionDeleteEvent',)

from ...permission.permission import PERMISSION_MASK_MANAGE_MESSAGES


from .add import ReactionAddEvent


class ReactionDeleteEvent(ReactionAddEvent):
    """
    Represents a processed `MESSAGE_REACTION_REMOVE` dispatch event.
    
    Attributes
    ----------
    message : ``Message``
        The message from what the reaction was removed.
    emoji : ``Emoji``
        The removed emoji.
    user : ``ClientUserBase``
        The user who's reaction was removed.
    
    Class Attributes
    ----------------
    DELETE_REACTION_OK : `int` = `0`
        Returned by ``.delete_reaction_with`` when the client has permission to execute the reaction remove. Not
        applicable on ``ReactionDeleteEvent``.
    DELETE_REACTION_PERM : `int` = `1`
        Returned by ``.delete_reaction_with`` when the client has no permission to execute the reaction remove.
    DELETE_REACTION_NOT_ADDED : `int` = `2`
        Returned by ``.delete_reaction_with`` when the client has permission to execute the reaction remove, but
        it cannot, because the reaction is not added on the respective message.
    """
    __slots__ = ()
    
    def delete_reaction_with(self, client):
        """
        Removes the added reaction. Because the event is ``ReactionDeleteEvent``, it will not remove any reaction, but
        only check the permissions.
        
        Parameters
        ----------
        client : ``Client``
            The client, who will execute the action.
        
        Returns
        -------
        result : `int`
            The identifier number of the action what will be executed.
            
            Can be one of the following:
            +---------------------------+-------+
            | Respective name           | Value |
            +===========================+=======+
            | DELETE_REACTION_PERM      | 1     |
            +---------------------------+-------+
            | DELETE_REACTION_NOT_ADDED | 2     |
            +---------------------------+-------+
        """
        if self.message.channel.cached_permissions_for(client) & PERMISSION_MASK_MANAGE_MESSAGES:
            result = self.DELETE_REACTION_NOT_ADDED
        else:
            result = self.DELETE_REACTION_PERM
        
        return result
