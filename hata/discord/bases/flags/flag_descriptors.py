__all__ = ('FlagDescriptor',)

from scarletio import RichAttributeErrorBaseType, copy_docs


NAME_UNKNOWN = '<unknown>'


class FlagDescriptorBase(RichAttributeErrorBaseType):
    """
    Base flag descriptor.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Raises `NotImplementedError`.
        """
        raise NotImplementedError
    
    
    def _build_cannot_exception(self, action):
        """
        Builds a "cannot" exception to be raised.
        
        Parameters
        ----------
        action : `str`
            The action that cannot be executed.
        
        Returns
        -------
        exception : `AttributeError`
        """
        return AttributeError(f'Cannot {action} `{self.type_name}.{self.flag_name}`.')
    
    
    def __get__(self, instance, instance_type):
        """
        Gets the field with the conversion.
        If accessed as a type attribute returns itself.
        
        Parameters
        ----------
        instance : `None | FlagBase`
            Instance to set the fields to.
        
        instance_type : ``FlagMeta``
            The instance's type.
        
        Returns
        -------
        value : `bool | self`
        """
        if instance is None:
            return self
        
        return False
    
    
    def __set__(self, instance, value):
        """
        Sets the field.
        
        Parameters
        ----------
        instance : `FlagBase`
            Instance to set the fields to.
        
        value : `object`
            The value to set.
        
        Raises
        ------
        AttributeError
        """
        raise self._build_cannot_exception('set')
    
    
    def __delete__(self, instance):
        """
        Deletes the field.
        
        Parameters
        ----------
        instance : `FlagBase`
            Instance to set the fields to.
        
        Raises
        ------
        AttributeError
        """
        raise self._build_cannot_exception('delete')
    
    
    def __repr__(self):
        """Returns the flag descriptor's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # name
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        # shift
        repr_parts.append(', shift = ')
        repr_parts.append(repr(self.shift))
        
        # deprecation
        deprecation = self.deprecation
        if (deprecation is not None):
            repr_parts.append(', deprecation = ')
            repr_parts.append(repr(deprecation))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two flag descriptors are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # mask
        if self.mask != other.mask:
            return False
        
        # flag_name
        if self.flag_name != other.flag_name:
            return False
        
        # shift
        if self.shift != other.shift:
            return False
        
        # type_name
        if self.type_name != other.type_name:
            return False
        
        # deprecation
        if self.deprecation != other.deprecation:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the flag descriptor's hash value."""
        hash_value = 0
        
        # mask
        hash_value ^= self.mask
        
        # flag_name
        hash_value ^= hash(self.flag_name)
        
        # shift
        hash_value ^= hash(self.shift)
        
        # type_name
        hash_value ^= hash(self.type_name)
        
        # deprecation
        deprecation = self.deprecation
        if (deprecation is not None):
            hash_value ^= hash(deprecation)
        
        return hash_value
    
    
    @property
    def flag_name(self):
        """
        Returns the flag's name.
        
        Returns
        -------
        flag_name : `str`
        """
        return NAME_UNKNOWN
    
    
    @property
    def type_name(self):
        """
        Returns the flag's type's name.
        
        Returns
        -------
        type_name : `str`
        """
        return NAME_UNKNOWN
    
    
    @property
    def mask(self):
        """
        Returns the flag's mask.
        
        Returns
        -------
        mask : `int`
        """
        return 0
    
    
    @property
    def shift(self):
        """
        Returns the flag's bit shift.
        
        Returns
        -------
        shift : `int`
        """
        return 0
    
    
    @property
    def name(self):
        """
        Returns the flags full name.
        
        Returns
        -------
        name : `str`
        """
        return f'{self.type_name}.{self.flag_name}'
    
    
    @property
    def deprecation(self):
        """
        Returns deprecation notice of this flag if available.
        
        Returns
        -------
        deprecation : `None | FlagDeprecation`
        """
        return None


class FlagDescriptor(FlagDescriptorBase):
    """
    A simple descriptors that can be assigned at type body and translated to an actually functioning descriptor at
    creation.
    
    Attributes
    ----------
    shift : `int`
        The represented bit by its shift.
    
    deprecation : `None | FlagDeprecation`
        Deprecation notice for this flag.
    """
    __slots__ = ('deprecation', 'shift',)
    
    def __new__(cls, shift, *, deprecation = None):
        """
        Creates a new flag descriptor.
        
        Parameters
        ----------
        shift : `int`
            The represented bit by its shift.
        
        deprecation : `None | FlagDeprecation` = `None`, Optional (Keyword only)
            Deprecation notice for this flag.
        """
        # Do not set deprecation if not allowed.
        if (deprecation is not None) and (not deprecation.allowed):
            deprecation = None
        
        self = object.__new__(cls)
        self.deprecation = deprecation
        self.shift = shift
        return self
    
    
    @property
    @copy_docs(FlagDescriptorBase.mask)
    def mask(self):
        return 1 << self.shift


class FlagBitDescriptor(FlagDescriptorBase):
    """
    Flag bit descriptor.
    
    Attributes
    ----------
    flag_name : `str`
        The flag's name.
    
    mask : `int`
        Bit mask created from ``.shift``.
    
    shift : `int`
        The represented bit by its shift.
    
    type_name : `str`
        The type's name the descriptor is under.
    """
    __slots__ = ('flag_name', 'mask', 'shift', 'type_name')
    
    def __new__(cls, shift, type_name, flag_name):
        """
        Creates a new bit descriptor.
        
        Attributes
        ----------
        flag_name : `str`
            The flag's name.
        
        shift : `int`
            The represented bit by its shift.
        
        type_name : `str`
            The type's name the descriptor is under.
        """
        self = object.__new__(cls)
        self.flag_name = flag_name
        self.mask = 1 << shift
        self.shift = shift
        self.type_name = type_name
        return self
    
    
    @copy_docs(FlagDescriptorBase.__get__)
    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        
        return True if instance & self.mask else False


class FlagBitDescriptorDeprecated(FlagBitDescriptor):
    """
    Flag bit descriptor.
    
    Attributes
    ----------
    deprecation : `FlagDeprecation`
        Deprecation notice for this flag.
    
    flag_name : `str`
        The flag's name.
    
    mask : `int`
        Bit mask created from ``.shift``.
    
    shift : `int`
        The represented bit by its shift.
    
    type_name : `str`
        The type's name the descriptor is under.
    """
    __slots__ = ('deprecation',)
    
    def __new__(cls, shift, type_name, flag_name, deprecation):
        """
        Creates a new bit descriptor.
        
        Attributes
        ----------
        flag_name : `str`
            The flag's name.
        
        shift : `int`
            The represented bit by its shift.
        
        type_name : `str`
            The type's name the descriptor is under.
        
        deprecation : `FlagDeprecation`
            Deprecation notice for this flag.
        """
        self = FlagBitDescriptor.__new__(cls, shift, type_name, flag_name)
        self.deprecation = deprecation
        return self
    
    
    @copy_docs(FlagDescriptorBase.__get__)
    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        
        self.deprecation.trigger(self.type_name, self.flag_name, 3)
        return True if instance & self.mask else False


class FlagBitDescriptorReversed(FlagBitDescriptor):
    """
    Flag bit descriptor that reverses its return value.
    
    Attributes
    ----------
    flag_name : `str`
        The flag's name.
    
    mask : `int`
        Bit mask created from ``.shift``.
    
    shift : `int`
        The represented bit by its shift.
    
    type_name : `str`
        The type's name the descriptor is under.
    """
    __slots__ = ()
    
    @copy_docs(FlagDescriptorBase.__get__)
    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        
        return False if instance & self.mask else True


class FlagBitDescriptorReversedDeprecated(FlagBitDescriptorDeprecated, FlagBitDescriptorReversed):
    """
    Flag bit descriptor that reverses its return value.
    
    Attributes
    ----------
    deprecation : `FlagDeprecation`
        Deprecation notice for this flag.
    
    flag_name : `str`
        The flag's name.
    
    mask : `int`
        Bit mask created from ``.shift``.
    
    shift : `int`
        The represented bit by its shift.
    
    type_name : `str`
        The type's name the descriptor is under.
    """
    __slots__ = ()
    
    @copy_docs(FlagDescriptorBase.__get__)
    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        
        self.deprecation.trigger(self.type_name, self.flag_name, 3)
        return False if instance & self.mask else True
