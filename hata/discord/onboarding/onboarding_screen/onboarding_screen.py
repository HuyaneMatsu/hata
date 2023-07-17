__all__ = ('OnboardingScreen',)

from scarletio import RichAttributeErrorBaseType

from ...channel import ChannelType, create_partial_channel_from_id
from ...core import GUILDS
from ...precreate_helpers import process_precreate_parameters_and_raise_extra

from .fields import (
    parse_default_channel_ids, parse_enabled, parse_guild_id, parse_mode, parse_prompts, put_default_channel_ids_into,
    put_enabled_into, put_guild_id_into, put_mode_into, put_prompts_into, validate_default_channel_ids,
    validate_enabled, validate_guild_id, validate_mode, validate_prompts
)
from .preinstanced import OnboardingMode


PRECREATE_FIELDS = {
    'default_channel_ids': ('default_channel_ids', validate_default_channel_ids),
    'default_channels': ('default_channel_ids', validate_default_channel_ids),
    'enabled': ('enabled', validate_enabled),
    'guild_id': ('guild_id', validate_guild_id),
    'guild': ('guild_id', validate_guild_id),
    'mode': ('mode', validate_mode),
    'prompts': ('prompts', validate_prompts),
}


class OnboardingScreen(RichAttributeErrorBaseType):
    """
    Represents a guild onboarding screen.
    
    Attributes
    ----------
    default_channel_ids : `None`, `tuple` of `int`
        The channels' identifiers that new members get opted into automatically.
    enabled : `bool`
        Whether onboarding is enabled.
    guild_id : `int`
        The guild's identifier the onboarding screen is part of.
    mode : ``OnboardingMode``
        Onboarding mode.
    prompts : `None`, `tuple` of ``OnboardingPrompt``
        The prompts shown during onboarding and in customize community.
    """
    __slots__ = ('default_channel_ids', 'enabled', 'guild_id', 'mode', 'prompts')
    
    def __new__(cls, *, default_channel_ids = ..., enabled = ..., mode = ..., prompts = ...):
        """
        Creates an onboarding screen instance from the given parameters.
        
        Parameters
        ----------
        default_channel_ids : `None`, `iterable` of (`int`, ``Channel``), Optional (Keyword only)
            The channels' identifiers that new members get opted into automatically.
        enabled : `bool`, Optional (Keyword only)
            Whether onboarding is enabled.
        mode : ``OnboardingMode``, `int`, Optional (Keyword only)
            Onboarding mode.
        prompts : `None`, `iterable` of ``OnboardingPrompt``, Optional (Keyword only)
            The prompts shown during onboarding and in customize community.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # default_channel_ids
        if default_channel_ids is ...:
            default_channel_ids = None
        else:
            default_channel_ids = validate_default_channel_ids(default_channel_ids)
        
        # enabled
        if enabled is ...:
            enabled = True
        else:
            enabled = validate_enabled(enabled)
        
        # mode
        if mode is ...:
            mode = OnboardingMode.default
        else:
            mode = validate_mode(mode)
        
        # prompts
        if prompts is ...:
            prompts = None
        else:
            prompts = validate_prompts(prompts)
        
        # Construct
        self = object.__new__(cls)
        self.default_channel_ids = default_channel_ids
        self.enabled = enabled
        self.guild_id = 0
        self.mode = mode
        self.prompts = prompts
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new onboarding screen instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Auto moderation rule trigger metadata payload.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.default_channel_ids = parse_default_channel_ids(data)
        self.enabled = parse_enabled(data)
        self.guild_id = parse_guild_id(data)
        self.mode = parse_mode(data)
        self.prompts = parse_prompts(data)
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the onboarding screen to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default fields should be included as well.
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields (like id-s) should be included.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_default_channel_ids_into(self.default_channel_ids, data, defaults)
        put_enabled_into(self.enabled, data, defaults)
        put_mode_into(self.mode, data, defaults)
        put_prompts_into(self.prompts, data, defaults, include_internals = include_internals)
        
        if include_internals:
            put_guild_id_into(self.guild_id, data, defaults)
        
        return data
    
    
    def __repr__(self):
        """Returns the onboarding screen's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        guild_id = self.guild_id
        if guild_id:
            repr_parts.append(' guild_id = ')
            repr_parts.append(repr(guild_id))
            repr_parts.append(',')
        
        repr_parts.append(' enabled = ')
        repr_parts.append(repr(self.enabled))
        
        default_channel_ids = self.default_channel_ids
        if (default_channel_ids is not None):
            repr_parts.append(', default_channel_ids = [')
            
            index = 0
            length = len(default_channel_ids)
            
            while True:
                channel_id = default_channel_ids[index]
                index += 1
                
                repr_parts.append(repr(channel_id))
                
                if index == length:
                    break
                
                repr_parts.append(', ')
            
            repr_parts.append(']')
        
        # mode
        mode = self.mode
        repr_parts.append(', mode = ')
        repr_parts.append(mode.name)
        repr_parts.append(' ~ ')
        repr_parts.append(str(mode))
        
        # prompts
        prompts = self.prompts
        if (prompts is not None):
            repr_parts.append(', prompts = [')
            
            index = 0
            length = len(prompts)
            
            while True:
                prompt = prompts[index]
                index += 1
                
                repr_parts.append(repr(prompt))
                
                if index == length:
                    break
                
                repr_parts.append(', ')
            
            repr_parts.append(']')
        
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two onboarding screen's are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.default_channel_ids != other.default_channel_ids:
            return False
        
        if self.enabled != other.enabled:
            return False
        
        # guild_id
        # ignore, internal
        
        if self.mode is not other.mode:
            return False
        
        if self.prompts != other.prompts:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the onboarding screen's hash value ."""
        hash_value = 0
        
        # default_channel_id
        default_channel_ids = self.default_channel_ids
        if (default_channel_ids is not None):
            hash_value ^= len(default_channel_ids)
            
            for channel_id in default_channel_ids:
                hash_value ^= channel_id
        
        # enabled
        hash_value ^= self.enabled << 4
        
        # guild_id
        # Ignore it
        
        # mode
        hash_value ^= self.mode.value << 11
        
        # prompts
        prompts = self.prompts
        if (prompts is not None):
            hash_value ^= len(prompts) << 5
            
            hash_value ^= hash(prompts)
            hash_value ^= (1 << 12)
        
        return hash_value
    
    
    @classmethod
    def precreate(cls, **keyword_parameters):
        """
        Precreates an onboarding screen. Since they are not cached, this method just a ``.__new__`` alternative.
        
        Parameters
        ----------
        **keyword_parameters : Keyword parameters
            Additional parameters defining how the option's fields should be set.
        
        Other Parameters
        ----------------
        default_channel_ids : `None`, `iterable` of (`int`, ``Channel``), Optional (Keyword only)
            The channels' identifiers that new members get opted into automatically.
        default_channels : `None`, `iterable` of (`int`, ``Channel``), Optional (Keyword only)
            Alternative of `default_channel_ids`.
        enabled : `bool`, Optional (Keyword only)
            Whether onboarding is enabled.
        guild : `int`, ``Guild``, Optional (Keyword only)
            Alternative of `guild_id`.
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The guild's identifier the onboarding screen is part of.
        mode : ``OnboardingMode``, `int`, Optional (Keyword only)
            Onboarding mode.
        prompts : `None`, `iterable` of ``OnboardingPrompt``, Optional (Keyword only)
            The prompts shown during onboarding and in customize community.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        # Construct
        
        self = object.__new__(cls)
        self.default_channel_ids = None
        self.enabled = True
        self.guild_id = 0
        self.mode = OnboardingMode.default
        self.prompts = None
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
    
    
    def copy(self):
        """
        Copies the onboarding screen.
        
        Returns
        -------
        new : `instance<cls>`
        """
        new = object.__new__(type(self))
        
        default_channel_ids = self.default_channel_ids
        if (default_channel_ids is not None):
            default_channel_ids = (*default_channel_ids,)
        new.default_channel_ids = default_channel_ids
        
        new.enabled = self.enabled
        new.guild_id = 0
        new.mode = self.mode
        
        prompts = self.prompts
        if (prompts is not None):
            prompts = (*(prompt.copy() for prompt in prompts),)
        new.prompts = prompts
        
        return new
    
    
    def copy_with(self, *, default_channel_ids = ..., enabled = ..., mode = ..., prompts = ...):
        """
        Copies the onboarding screen with the given screen.
        
        Parameters
        ----------
        default_channel_ids : `None`, `iterable` of (`int`, ``Channel``), Optional (Keyword only)
            The channels' identifiers that new members get opted into automatically.
        enabled : `bool`, Optional (Keyword only)
            Whether onboarding is enabled.
        mode : ``OnboardingMode``, `int`, Optional (Keyword only)
            Onboarding mode.
        prompts : `None`, `iterable` of ``OnboardingPrompt``, Optional (Keyword only)
            The prompts shown during onboarding and in customize community.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # default_channel_ids
        if default_channel_ids is ...:
            default_channel_ids = self.default_channel_ids
            if (default_channel_ids is not None):
                default_channel_ids = (*default_channel_ids,)
        else:
            default_channel_ids = validate_default_channel_ids(default_channel_ids)
        
        # enabled
        if enabled is ...:
            enabled = self.enabled
        else:
            enabled = validate_enabled(enabled)
        
        # mode
        if mode is ...:
            mode = self.mode
        else:
            mode = validate_mode(mode)
        
        # prompts
        if prompts is ...:
            prompts = self.prompts
            if (prompts is not None):
                prompts = (*(prompt.copy() for prompt in prompts),)
        else:
            prompts = validate_prompts(prompts)
        
        new = object.__new__(type(self))
        new.default_channel_ids = default_channel_ids
        new.enabled = enabled
        new.guild_id = 0
        new.mode = mode
        new.prompts = prompts
        return new
    
    
    @property
    def default_channels(self):
        """
        Returns the default channels that new get opted into automatically.
        
        Returns
        -------
        default_channels : `None`, `tuple` of ``Channel``
        """
        default_channel_ids = self.default_channel_ids
        if default_channel_ids is None:
            default_channels = None
        else:
            default_channels = (*(
                create_partial_channel_from_id(channel_id, ChannelType.unknown, 0) for channel_id in default_channel_ids
            ),)
        
        return default_channels
    
    
    def iter_default_channel_ids(self):
        """
        Iterates over the default channels that new get opted into automatically.
        
        This method is an iterable generator.
        
        Yields
        ------
        default_channel_id : `int`
        """
        default_channel_ids = self.default_channel_ids
        if (default_channel_ids is not None):
            yield from default_channel_ids
    
    
    def iter_default_channels(self):
        """
        Iterates over the default channels that new get opted into automatically.
        
        This method is an iterable generator.
        
        Yields
        ------
        default_channel : ``Channel``
        """
        for channel_id in self.iter_default_channel_ids():
            yield create_partial_channel_from_id(channel_id, ChannelType.unknown, 0)
    
    
    @property
    def guild(self):
        """
        Returns the onboarding screen's owner guild identifier. If the guild is not cached then returns `None`.
        
        Returns
        -------
        guild : `None`, ``Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS[guild_id]
    
    
    def iter_prompts(self):
        """
        Iterates over the prompts that are shown during onboarding and in customize community.
        
        This method is an iterable generator.
        
        Yields
        ------
        prompt : ``OnboardingPrompt``
        """
        prompts = self.prompts
        if (prompts is not None):
            yield from prompts
