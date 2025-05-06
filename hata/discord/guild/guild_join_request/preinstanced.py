__all__ = ('GuildJoinRequestStatus',)

from scarletio import copy_docs

from ...bases import Preinstance as P, PreinstancedBase


class GuildJoinRequestStatus(PreinstancedBase, value_type = str):
    """
    Represents the status of a ``GuildJoinRequest``.
    
    Attributes
    ----------
    name : `str`
        The name of the guild join request status.
    
    value : `str`
        The Discord side identifier value of the guild join request status.
    
    Type Attributes
    ---------------
    Every predefined guild join request status can be accessed as type attribute as well:
    
    +-----------------------+-----------+-----------+
    | Type attribute name   | Name      | Value     |
    +=======================+===========+===========+
    | approved              | approved  | APPROVED  |
    +-----------------------+-----------+-----------+
    | pending               | pending   | PENDING   |
    +-----------------------+-----------+-----------+
    | rejected              | rejected  | REJECTED  |
    +-----------------------+-----------+-----------+
    | started               | started   | STARTED   |
    +-----------------------+-----------+-----------+
    """
    __slots__ = ()
    
    @copy_docs(PreinstancedBase.__new__)
    def __new__(cls, value, name = None):
        if name is None:
            name = value.lower().replace('_', ' ')
        
        return PreinstancedBase.__new__(cls, value, name)
    
    approved = P('APPROVED', 'approved')
    pending = P('PENDING', 'pending')
    rejected = P('REJECTED', 'rejected')
    started = P('STARTED', 'started')
