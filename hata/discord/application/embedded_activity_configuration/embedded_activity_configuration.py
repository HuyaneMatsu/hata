__all__ = ('EmbeddedActivityConfiguration',)

from scarletio import RichAttributeErrorBaseType

from .fields import (
    parse_age_gated, parse_client_platform_configurations, parse_content_security_policy_exceptions_exist,
    parse_default_orientation_lock_state, parse_default_tablet_orientation_lock_state, parse_position,
    parse_preview_video_asset_id, put_age_gated, put_client_platform_configurations,
    put_content_security_policy_exceptions_exist, put_default_orientation_lock_state,
    put_default_tablet_orientation_lock_state, put_position, put_preview_video_asset_id,
    validate_age_gated, validate_client_platform_configurations, validate_content_security_policy_exceptions_exist,
    validate_default_orientation_lock_state, validate_default_tablet_orientation_lock_state, validate_position,
    validate_preview_video_asset_id
)
from .preinstanced import OrientationLockState


class EmbeddedActivityConfiguration(RichAttributeErrorBaseType):
    """
    Represents an embedded activity's configuration.
    
    Attributes
    ----------
    age_gated : `bool`
        Whether an age gate warning should show up for the using before using the activity.
    client_platform_configurations : `None | dict<PlatformType, ClientPlatformConfiguration>`
        The embedded activity's configuration for each platform.
    content_security_policy_exceptions_exist : `bool`
        Whether the activity has content security exceptions, this includes that the activity's developers may see
        your ip.
    default_orientation_lock_state : ``OrientationLockState``
        The activity's default orientation lock state.
    default_tablet_orientation_lock_state : ``OrientationLockState``
        The activity's default orientation lock state for tablets.
    position : `int`
        The activity's position in the embedded activity listing.
    preview_video_asset_id : `int`
        The activity's preview asset's identifier.
    """
    __slots__ = (
        'age_gated', 'client_platform_configurations', 'content_security_policy_exceptions_exist',
        'default_orientation_lock_state', 'default_tablet_orientation_lock_state', 'position', 'preview_video_asset_id'
    )
    
    def __new__(
        cls,
        *,
        age_gated = ...,
        client_platform_configurations = ...,
        content_security_policy_exceptions_exist = ...,
        default_orientation_lock_state = ...,
        default_tablet_orientation_lock_state = ...,
        position = ...,
        preview_video_asset_id = ...,
    ):
        """
        Creates a new embedded activity's configuration.
        
        Parameters
        ----------
        age_gated : `bool`, Optional (Keyword only)
            Whether an age gate warning should show up for the using before using the activity.
        client_platform_configurations : `None | dict<PlatformType | int, ClientPlatformConfiguration>` \
                , Optional (Keyword only)
            The embedded activity's configuration for each platform.
        content_security_policy_exceptions_exist : `bool`, Optional (Keyword only)
            Whether the activity has content security exceptions, this includes that the activity's developers may see
            your ip.
        default_orientation_lock_state : `OrientationLockState | int`, Optional (Keyword only)
            The activity's default orientation lock state.
        default_tablet_orientation_lock_state : `OrientationLockState | int`, Optional (Keyword only)
            The activity's default orientation lock state for tablets.
        position : `int`, Optional (Keyword only)
            The activity's position in the embedded activity listing.
        preview_video_asset_id : `int`, Optional (Keyword only)
            The activity's preview asset's identifier.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        """
        # age_gated
        if age_gated is ...:
            age_gated = False
        else:
            age_gated = validate_age_gated(age_gated)
        
        # client_platform_configurations
        if client_platform_configurations is ...:
            client_platform_configurations = None
        else:
            client_platform_configurations = validate_client_platform_configurations(client_platform_configurations)
        
        # content_security_policy_exceptions_exist
        if content_security_policy_exceptions_exist is ...:
            content_security_policy_exceptions_exist = False
        else:
            content_security_policy_exceptions_exist = validate_content_security_policy_exceptions_exist(
                content_security_policy_exceptions_exist
            )
        
        # default_orientation_lock_state
        if default_orientation_lock_state is ...:
            default_orientation_lock_state = OrientationLockState.none
        else:
            default_orientation_lock_state = validate_default_orientation_lock_state(default_orientation_lock_state)
        
        # default_tablet_orientation_lock_state
        if default_tablet_orientation_lock_state is ...:
            default_tablet_orientation_lock_state = OrientationLockState.none
        else:
            default_tablet_orientation_lock_state = validate_default_tablet_orientation_lock_state(
                default_tablet_orientation_lock_state
            )
        
        # position
        if position is ...:
            position = 0
        else:
            position = validate_position(position)
        
        # preview_video_asset_id
        if preview_video_asset_id is ...:
            preview_video_asset_id = 0
        else:
            preview_video_asset_id = validate_preview_video_asset_id(preview_video_asset_id)
        
        # Construct
        self = object.__new__(cls)
        self.age_gated = age_gated
        self.client_platform_configurations = client_platform_configurations
        self.content_security_policy_exceptions_exist = content_security_policy_exceptions_exist
        self.default_orientation_lock_state = default_orientation_lock_state
        self.default_tablet_orientation_lock_state = default_tablet_orientation_lock_state
        self.position = position
        self.preview_video_asset_id = preview_video_asset_id
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a embedded activity configuration from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Client platform configuration data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.age_gated = parse_age_gated(data)
        self.client_platform_configurations = parse_client_platform_configurations(data)
        self.content_security_policy_exceptions_exist = parse_content_security_policy_exceptions_exist(data)
        self.default_orientation_lock_state = parse_default_orientation_lock_state(data)
        self.default_tablet_orientation_lock_state = parse_default_tablet_orientation_lock_state(data)
        self.position = parse_position(data)
        self.preview_video_asset_id = parse_preview_video_asset_id(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serializes the embedded activity configuration.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields of their default value should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_age_gated(self.age_gated, data, defaults)
        put_client_platform_configurations(self.client_platform_configurations, data, defaults)
        put_content_security_policy_exceptions_exist(self.content_security_policy_exceptions_exist, data, defaults)
        put_default_orientation_lock_state(self.default_orientation_lock_state, data, defaults)
        put_default_tablet_orientation_lock_state(self.default_tablet_orientation_lock_state, data, defaults)
        put_position(self.position, data, defaults)
        put_preview_video_asset_id(self.preview_video_asset_id, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the embedded activity configuration's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        field_added = False
        
        # age_gated
        age_gated = self.age_gated
        if age_gated:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' age_gated = ')
            repr_parts.append(repr(age_gated))
        
        # client_platform_configurations
        client_platform_configurations = self.client_platform_configurations
        if client_platform_configurations is not None:
            items = sorted(client_platform_configurations.items())
            length = len(items)
            
            # length should not be 0
            if length:
                if field_added:
                    repr_parts.append(',')
                else:
                    field_added = True
                
                repr_parts.append(' client_platform_configurations = {')
                
                index = 0
                while True:
                    platform, client_configuration = items[index]
                    
                    repr_parts.append(platform.name)
                    repr_parts.append(' ~ ')
                    repr_parts.append(repr(platform.value))
                    repr_parts.append(': ')
                    repr_parts.append(repr(client_configuration))
                    
                    index += 1
                    if index == length:
                        break
                    
                    repr_parts.append(', ')
                    continue
        
        # content_security_policy_exceptions_exist
        content_security_policy_exceptions_exist = self.content_security_policy_exceptions_exist
        if content_security_policy_exceptions_exist:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' content_security_policy_exceptions_exist = ')
            repr_parts.append(repr(content_security_policy_exceptions_exist))
        
        # default_orientation_lock_state
        default_orientation_lock_state = self.default_orientation_lock_state
        if default_orientation_lock_state is not OrientationLockState.none:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' default_orientation_lock_state = ')
            repr_parts.append(default_orientation_lock_state.name)
            repr_parts.append(' ~ ')
            repr_parts.append(repr(default_orientation_lock_state.value))
        
        # default_tablet_orientation_lock_state
        default_tablet_orientation_lock_state = self.default_tablet_orientation_lock_state
        if default_tablet_orientation_lock_state is not OrientationLockState.none:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' default_tablet_orientation_lock_state = ')
            repr_parts.append(default_tablet_orientation_lock_state.name)
            repr_parts.append(' ~ ')
            repr_parts.append(repr(default_tablet_orientation_lock_state.value))
        
        # position
        position = self.position
        if position:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' position = ')
            repr_parts.append(repr(position))
        
        # preview_video_asset_id
        preview_video_asset_id = self.preview_video_asset_id
        if preview_video_asset_id:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' preview_video_asset_id = ')
            repr_parts.append(repr(preview_video_asset_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two embedded activity configurations are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # age_gated
        if self.age_gated != other.age_gated:
            return False
        
        # client_platform_configurations
        if self.client_platform_configurations != other.client_platform_configurations:
            return False
        
        # content_security_policy_exceptions_exist
        if self.content_security_policy_exceptions_exist != other.content_security_policy_exceptions_exist:
            return False
        
        # default_orientation_lock_state
        if self.default_orientation_lock_state is not other.default_orientation_lock_state:
            return False
        
        # default_tablet_orientation_lock_state
        if self.default_tablet_orientation_lock_state is not other.default_tablet_orientation_lock_state:
            return False
        
        # position
        if self.position != other.position:
            return False
        
        # preview_video_asset_id
        if self.preview_video_asset_id != other.preview_video_asset_id:
            return False
        
        return True
    

    def __hash__(self):
        """Returns the embedded activity configuration's hash value."""
        hash_value = 0
        
        # age_gated
        hash_value ^= self.age_gated
        
        # client_platform_configurations
        client_platform_configurations = self.client_platform_configurations
        if (client_platform_configurations is not None):
            for platform, client_configuration in client_platform_configurations.items():
                hash_value ^= hash(platform) & hash(client_configuration)
        
        # content_security_policy_exceptions_exist
        hash_value ^= self.content_security_policy_exceptions_exist << 4
        
        # default_orientation_lock_state
        hash_value ^= hash(self.default_orientation_lock_state) << 8
        
        # default_tablet_orientation_lock_state
        hash_value ^= hash(self.default_tablet_orientation_lock_state) << 12
        
        # position
        hash_value ^= self.position << 16
        
        # preview_video_asset_id
        hash_value ^= self.preview_video_asset_id
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the embedded activity configuration.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.age_gated = self.age_gated
        client_platform_configurations = self.client_platform_configurations
        if (client_platform_configurations is not None):
            client_platform_configurations = {
                platform: client_configuration.copy()
                for platform, client_configuration in client_platform_configurations.items()
            }
        new.client_platform_configurations = client_platform_configurations
        new.content_security_policy_exceptions_exist = self.content_security_policy_exceptions_exist
        new.default_orientation_lock_state = self.default_orientation_lock_state
        new.default_tablet_orientation_lock_state = self.default_tablet_orientation_lock_state
        new.position = self.position
        new.preview_video_asset_id = self.preview_video_asset_id
        return new
    
    
    def copy_with(
        self,
        *,
        age_gated = ...,
        client_platform_configurations = ...,
        content_security_policy_exceptions_exist = ...,
        default_orientation_lock_state = ...,
        default_tablet_orientation_lock_state = ...,
        position = ...,
        preview_video_asset_id = ...,
    ):
        """
        Copies the embedded activity configuration with the given fields.
        
        Parameters
        ----------
        age_gated : `bool`, Optional (Keyword only)
            Whether an age gate warning should show up for the using before using the activity.
        client_platform_configurations : `None | dict<PlatformType, ClientPlatformConfiguration>` \
                , Optional (Keyword only)
            The embedded activity's configuration for each platform.
        content_security_policy_exceptions_exist : `bool`, Optional (Keyword only)
            Whether the activity has content security exceptions, this includes that the activity's developers may see
            your ip.
        default_orientation_lock_state : `OrientationLockState | int`, Optional (Keyword only)
            The activity's default orientation lock state.
        default_tablet_orientation_lock_state : `OrientationLockState | int`, Optional (Keyword only)
            The activity's default orientation lock state for tablets.
        position : `int`, Optional (Keyword only)
            The activity's position in the embedded activity listing.
        preview_video_asset_id : `int`, Optional (Keyword only)
            The activity's preview asset's identifier.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        """
        # age_gated
        if age_gated is ...:
            age_gated = self.age_gated
        else:
            age_gated = validate_age_gated(age_gated)
        
        # client_platform_configurations
        if client_platform_configurations is ...:
            client_platform_configurations = self.client_platform_configurations
            if (client_platform_configurations is not None):
                client_platform_configurations = {
                    platform: client_configuration.copy()
                    for platform, client_configuration in client_platform_configurations.items()
                }
        else:
            client_platform_configurations = validate_client_platform_configurations(client_platform_configurations)
        
        # content_security_policy_exceptions_exist
        if content_security_policy_exceptions_exist is ...:
            content_security_policy_exceptions_exist = self.content_security_policy_exceptions_exist
        else:
            content_security_policy_exceptions_exist = validate_content_security_policy_exceptions_exist(
                content_security_policy_exceptions_exist
            )
        
        # default_orientation_lock_state
        if default_orientation_lock_state is ...:
            default_orientation_lock_state = self.default_orientation_lock_state
        else:
            default_orientation_lock_state = validate_default_orientation_lock_state(default_orientation_lock_state)
        
        # default_tablet_orientation_lock_state
        if default_tablet_orientation_lock_state is ...:
            default_tablet_orientation_lock_state = self.default_tablet_orientation_lock_state
        else:
            default_tablet_orientation_lock_state = validate_default_tablet_orientation_lock_state(
                default_tablet_orientation_lock_state
            )
        
        # position
        if position is ...:
            position = self.position
        else:
            position = validate_position(position)
        
        # preview_video_asset_id
        if preview_video_asset_id is ...:
            preview_video_asset_id = self.preview_video_asset_id
        else:
            preview_video_asset_id = validate_preview_video_asset_id(preview_video_asset_id)
        
        # Construct
        new = object.__new__(type(self))
        new.age_gated = age_gated
        new.client_platform_configurations = client_platform_configurations
        new.content_security_policy_exceptions_exist = content_security_policy_exceptions_exist
        new.default_orientation_lock_state = default_orientation_lock_state
        new.default_tablet_orientation_lock_state = default_tablet_orientation_lock_state
        new.position = position
        new.preview_video_asset_id = preview_video_asset_id
        return new
    
    
    def iter_supported_platforms(self):
        """
        Iterates over the supported platforms of the activity.
        
        This method is a generator.
        
        Yields
        ------
        platform : ``PlatformType`` 
        """
        client_platform_configurations = self.client_platform_configurations
        if (client_platform_configurations is not None):
            yield from client_platform_configurations.keys()
    
    
    def get_client_platform_configuration(self, platform):
        """
        Gets the client configuration for the given platform.
        
        Parameters
        ----------
        platform : `PlatformType | str`
            The platform to get the configuration for.
        
        Returns
        -------
        configuration : `None | ClientPlatformConfiguration`
        """
        client_platform_configurations = self.client_platform_configurations
        if (client_platform_configurations is not None):
            return client_platform_configurations.get(platform, None)
