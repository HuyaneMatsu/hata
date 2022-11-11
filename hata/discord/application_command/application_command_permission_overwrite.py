__all__ = ('ApplicationCommandPermissionOverwrite',)

from scarletio import RichAttributeErrorBaseType

from ..channel import Channel
from ..core import CHANNELS, ROLES
from ..role import Role, create_partial_role_from_id
from ..user import ClientUserBase, create_partial_user_from_id

from .preinstanced import ApplicationCommandPermissionOverwriteTargetType


APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_USER = ApplicationCommandPermissionOverwriteTargetType.user
APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_ROLE = ApplicationCommandPermissionOverwriteTargetType.role
APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_CHANNEL = ApplicationCommandPermissionOverwriteTargetType.channel


def _validate_application_command_target(target):
    """
    Validates the given application command's input target.
    
    Parameters
    ----------
    target : ``ClientUserBase``, ``Role``, ``Channel``, `tuple` ((``ClientUserBase``, ``Role``, \
            ``Channel``, `str` (`'Role'`, `'role'`, `'User'`, `'user'`, `'Channel'`, `'channel'`)), `int`)
        The target entity of the application command permission overwrite.
    
    Returns
    -------
    target_type : ``ApplicationCommandPermissionOverwriteTargetType``
        The target entity's type.
    
    target_id : `int`
        The represented entity's identifier.
    
    Raises
    ------
    TypeError
        - If `target` was not given as any of the expected types & values.
    """
    # GOTO
    while True:
        if isinstance(target, Role):
            target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_ROLE
            target_id = target.id
            target_lookup_failed = False
            break
        
        if isinstance(target, ClientUserBase):
            target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_USER
            target_id = target.id
            target_lookup_failed = False
            break
        
        if isinstance(target, Channel):
            target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_CHANNEL
            target_id = target.id
            target_lookup_failed = False
            break
        
        if isinstance(target, tuple) and len(target) == 2:
            target_maybe, target_id_maybe = target
            
            if isinstance(target_maybe, type):
                if issubclass(target_maybe, Role):
                    target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_ROLE
                elif issubclass(target_maybe, ClientUserBase):
                    target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_USER
                elif issubclass(target_maybe, Channel):
                    target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_CHANNEL
                else:
                    target_lookup_failed = True
                    break
            
            elif isinstance(target_maybe, str):
                if target_maybe in ('Role', 'role'):
                    target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_ROLE
                elif target_maybe in ('User', 'user'):
                    target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_USER
                elif target_maybe in ('Channel', 'channel'):
                    target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_CHANNEL
                else:
                    target_lookup_failed = True
                    break
            
            else:
                target_lookup_failed = True
                break
            
            if type(target_id_maybe) is int:
                target_id = target_id_maybe
            elif isinstance(target_id_maybe, int):
                target_id = int(target_id_maybe)
            else:
                target_lookup_failed = True
                break
            
            target_lookup_failed = False
            break
        
        target_lookup_failed = True
        break
    
    if target_lookup_failed:
        raise TypeError(
            f'`target` can be `{Role.__name__}`, `{ClientUserBase.__name__}`, `{Channel.__name__}`, '
            f'`tuple` ((`{Role.__name__}`, `{ClientUserBase.__name__}`, `{Channel.__name__}`, `str` '
            f'(`\'Role\'`, `\'role\'`, `\'User\'`, `\'user\'`, `\'Channel\'`, `\'channel\'`)), `int`), '
            f'got {target.__class__.__name__}: {target!r}.'
        )
    
    return target_type, target_id


class ApplicationCommandPermissionOverwrite(RichAttributeErrorBaseType):
    """
    Represents an application command's allow/disallow overwrite for the given entity.
    
    Attributes
    ----------
    allow : `bool`
        Whether the respective command is allowed for the represented entity.
    
    target_id : `int`
        The represented entity's identifier.
    
    target_type : ``ApplicationCommandPermissionOverwriteTargetType``
        The target entity's type.
    """
    __slots__ = ('allow', 'target_id', 'target_type')
    
    def __new__(cls, target, allow):
        """
        Creates a new ``ApplicationCommandPermission`` with the given parameters.
        
        Parameters
        ----------
        target : ``ClientUserBase``, ``Role``, ``Channel``, `tuple` ((``ClientUserBase``, ``Role``, \
                ``Channel``, `str` (`'Role'`, `'role'`, `'User'`, `'user'`, `'Channel'`, `'channel'`)), `int`)
            The target entity of the application command permission overwrite.
            
            The expected type & value might be pretty confusing, but the target was it to allow relaxing creation.
            To avoid confusing, here is a list of the expected structures:
            
            - ``Role``
            - ``ClientUserBase``
            - ``Channel``
            - `tuple` (``Role``, `int`)
            - `tuple` (``ClientUserBase``, `int`)
            - `tuple` (``Channel``, `int`)
            - `tuple` (`'Role'`, `int`)
            - `tuple` (`'role'`, `int`)
            - `tuple` (`'User'`, `int`)
            - `tuple` (`'user'`, `int`)
            - `tuple` (`'Channel'`, `int`)
            - `tuple` (`'channel'`, `int`)
        
        allow : `bool`
            Whether the respective application command should be enabled for the respective entity.
        
        Raises
        ------
        TypeError
            - If `target` was not given as any of the expected types & values.
        AssertionError
            - If `allow` was not given as `bool`.
        """
        # allow
        if __debug__:
            if not isinstance(allow, bool):
                raise AssertionError(
                    f'`allow` can be `bool`, got {allow.__class__.__name__}; {allow!r}.'
                )
        
        # target_id & target_type
        target_type, target_id = _validate_application_command_target(target)
        
        self = object.__new__(cls)
        self.allow = allow
        self.target_id = target_id
        self.target_type = target_type
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new ``ApplicationCommandPermissionOverwrite`` from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            The received application command permission overwrite data.
        
        Returns
        -------
        self : ``ApplicationCommandPermission``
            The created application command option.
        """
        # allow
        allow = data['permission']
        
        # target_id
        target_id = int(data['id'])
        
        # target_type
        target_type = ApplicationCommandPermissionOverwriteTargetType.get(data['type'])
        
        self = object.__new__(cls)
        self.allow = allow
        self.target_id = target_id
        self.target_type = target_type
        return self
    
    
    def to_data(self):
        """
        Converts the application command permission overwrite to a json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        
        # allow
        data['permission'] = self.allow
        
        # target_id
        data['id'] = self.target_id
        
        # target_type
        data['type'] = self.target_type.value
        
        return data
    
    
    @property
    def target(self):
        """
        Returns the application command overwrite's target entity.
        
        Returns
        -------
        target : `None`, ``Role``, ``ClientUserBase``, ``Channel``
        """
        target_type = self.target_type
        target_id = self.target_id
        
        if target_type is APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_ROLE:
            target = create_partial_role_from_id(target_id)
        
        elif target_type is APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_USER:
            target = create_partial_user_from_id(target_id)
        
        elif target_type is APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_CHANNEL:
            target = CHANNELS.get(target_id)
        
        else:
            target = None
        
        return target
    
    
    def __repr__(self):
        """Returns the application command permission overwrite's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # Primary fields: `.target_type`, `.target_id`
        repr_parts.append(' target_type=')
        repr_parts.append(self.target_type.name)
        
        repr_parts.append(', target_id=')
        repr_parts.append(repr(self.target_id))
        
        # Secondary fields: `.allow`
        repr_parts.append(', allow=')
        repr_parts.append(repr(self.allow))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two application command overwrites are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # allow
        if self.allow != other.allow:
            return False
        
        # target_id
        if self.target_id != other.target_id:
            return False
        
        # target_type
        if self.target_type is not other.target_type:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the application command permission overwrite's hash value."""
        hash_value = 0
        
        # allow
        hash_value ^= self.allow << 8
        
        # target_id
        hash_value ^= self.target_id
        
        # target_type
        hash_value ^= self.target_type.value
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the application command permission overwrite.
        
        Returns
        -------
        new : ``ApplicationCommandPermissionOverwrite``
        """
        new = object.__new__(type(self))
        
        # allow
        new.allow = self.allow
        
        # target_id
        new.target_id = self.target_id
        
        # target_type
        new.target_type = self.target_type
        
        return new
    
    
    def __gt__(self, other):
        """Returns whether self is greater than other."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_type_value = self.target_type.value
        other_type_value = other.target_type.value
        
        if self_type_value > other_type_value:
            return True
        
        if self_type_value < other_type_value:
            return False
        
        if self_type_value == APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_ROLE.value:
            self_target_id = self.target_id
            other_target_id = other.target_id
            
            self_role = ROLES.get(self_target_id, None)
            other_role = ROLES.get(other_target_id, None)
            if self_role is None:
                if other_role is None:
                    return (self_target_id > other_target_id)
                else:
                    return False
            else:
                if other_role is None:
                    return True
                else:
                    return (self_role > other_role)
        
        if self_type_value == APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_USER.value:
            return (self.target_id > other.target_id)
        
        if self_type_value == APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_CHANNEL.value:
            self_target_id = self.target_id
            other_target_id = other.target_id
            
            self_channel = CHANNELS.get(self_target_id, None)
            other_channel = CHANNELS.get(other_target_id, None)
            if self_channel is None:
                if other_channel is None:
                    return (self_target_id > other_target_id)
                else:
                    return False
            else:
                if other_channel is None:
                    return True
                else:
                    return (self_channel.name > other_channel.name)
        
        # Should not happen
        return False
    
    
    def __lt__(self, other):
        """Returns whether self is greater than other."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_type_value = self.target_type.value
        other_type_value = other.target_type.value
        
        if self_type_value > other_type_value:
            return False
        
        if self_type_value < other_type_value:
            return True
        
        if self_type_value == APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_ROLE.value:
            self_target_id = self.target_id
            other_target_id = other.target_id
            
            self_role = ROLES.get(self_target_id, None)
            other_role = ROLES.get(other_target_id, None)
            if self_role is None:
                if other_role is None:
                    return (self_target_id < other_target_id)
                else:
                    return True
            else:
                if other_role is None:
                    return False
                else:
                    return (self_role < other_role)
        
        if self_type_value == APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_USER.value:
            return (self.target_id < other.target_id)
        
        if self_type_value == APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_CHANNEL.value:
            self_target_id = self.target_id
            other_target_id = other.target_id
            
            self_channel = CHANNELS.get(self_target_id, None)
            other_channel = CHANNELS.get(other_target_id, None)
            if self_channel is None:
                if other_channel is None:
                    return (self_target_id < other_target_id)
                else:
                    return True
            else:
                if other_channel is None:
                    return False
                else:
                    return (self_channel.name < other_channel.name)
        
        # Should not happen
        return True
    
    
    def copy_with(self, **keyword_parameters):
        """
        Copies the application command permission overwrite with modifying the given parameters inside of it.
        
        Parameters
        ----------
        **keyword_parameters : Keyword parameters
            The attributes to change.
        
        Other Parameters
        ----------------
        allow : `bool`
            Whether the respective application command should be enabled for the respective entity.
        
        target : ``ClientUserBase``, ``Role``, ``Channel``, `tuple` ((``ClientUserBase``, ``Role``, \
                ``Channel``, `str` (`'Role'`, `'role'`, `'User'`, `'user'`, `'Channel'`, `'channel'`)), `int`)
            The target entity of the application command permission overwrite.
        
        Returns
        -------
        new : ``ApplicationCommandPermissionOverwrite``
            the newly created application command permission overwrite.
        
        Raises
        ------
        TypeError
            - If `target` was not given as any of the expected types & values.
            - If extra parameters were given.
        AssertionError
            - If `allow` was not given as `bool`.
        """
        # allow
        try:
            allow = keyword_parameters.pop('allow')
        except KeyError:
            allow = self.allow
        else:
            if __debug__:
                if not isinstance(allow, bool):
                    raise AssertionError(
                        f'`allow` can be `bool`, got {allow.__class__.__name__}; {allow!r}.'
                    )
        
        # target_id & target_type
        try:
            target = keyword_parameters.pop('target')
        except KeyError:
            target_id = self.target_id
            target_type = self.target_type
        else:
            target_type, target_id = _validate_application_command_target(target)
        
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused parameters: {keyword_parameters!r}.'
            )
        
        new = object.__new__(type(self))
        new.allow = allow
        new.target_id = target_id
        new.target_type = target_type
        return new
