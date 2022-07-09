__all__ = ('MessageInteraction',)

from scarletio import include

from ..bases import DiscordEntity
from ..user import User


InteractionType = include('InteractionType')


class MessageInteraction(DiscordEntity):
    """
    Sent with a ``Message``, when the it is a response to an ``InteractionEvent``.
    
    Attributes
    ----------
    id : `int`
        The interaction's identifier.
    name : `str`
        The invoked interaction's name.
    type : ``InteractionType``
        The interaction's type.
    sub_command_name_stack : `None`, `tuple` of `str`
        The sub-command-group and sub-command names.
    user : ``ClientUserBase``
        Who invoked the interaction.
    """
    __slots__ = ('name', 'type', 'sub_command_name_stack', 'user')
    
    def __new__(cls, data, guild_id):
        """
        Creates a new ``MessageInteraction`` from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message interaction data.
        guild_id : `int`
            The respective message's guild's identifier.
        """
        full_name = data.get('name', None)
        if full_name is None:
            name = ''
            sub_command_name_stack = None
        
        else:
            name_split = full_name.split(' ')
            
            name_split_length = len(name_split)
            if name_split_length == 1:
                name = name_split[0]
                sub_command_name_stack = None
            
            elif name_split_length > 1:
                name = name_split[0]
                sub_command_name_stack = tuple(name_split[1:])
            
            else:
                name = ''
                sub_command_name_stack = None
        
        self = object.__new__(cls)
        self.id = int(data['id'])
        self.name = name
        self.sub_command_name_stack = sub_command_name_stack
        self.type = InteractionType.get(data['type'])
        self.user = User.from_data(data['user'], data.get('member', None), guild_id)
        
        return self
    
    
    def __repr__(self):
        """Returns the message interaction's representation."""
        repr_parts = ['<', self.__class__.__name__, ' id=', repr(self.id), ', type=']
        
        interaction_type = self.type
        repr_parts.append(interaction_type.name)
        repr_parts.append(' (')
        repr_parts.append(repr(interaction_type.value))
        repr_parts.append(')')
        
        repr_parts.append(', name=')
        repr_parts.append(repr(self.name))
        
        sub_command_name_stack = self.sub_command_name_stack
        if (sub_command_name_stack is not None):
            repr_parts.append(', sub_command_name_stack=')
            repr_parts.append(repr(sub_command_name_stack))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @property
    def joined_name(self):
        """
        Returns the joined name of the message interaction.
        
        Returns
        -------
        joined_name : `str`
        """
        name = self.name
        sub_command_name_stack = self.sub_command_name_stack
        if (sub_command_name_stack is None):
            return name
        
        return ' '.join([name, *sub_command_name_stack])
    
    
    def to_data(self):
        """
        Tries to convert the message interaction back to json serializable dictionary.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`)
        """
        return {
            'id': str(self.id),
            'name': self.joined_name,
            'type': self.type.value,
            'user': self.user.to_data()
        }
