__all__ = ('ApplicationRoleConnectionMetadataType', 'ApplicationRoleConnectionValueType')

from ...bases import Preinstance as P, PreinstancedBase
from ...utils import datetime_to_timestamp, timestamp_to_datetime_soft


class ApplicationRoleConnectionValueType(PreinstancedBase):
    """
    Type information for application role connection metadata values'.
    
    > This type is wrapper side only.
    
    Attributes
    ----------
    name : `str`
        The name of the value type.
    value : `int`
        The identifier of the value type.
    deserializer : `FunctionType`
        Function used to deserialize values.
    serializer : `FunctionType`
        Function used to serialize values.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationRoleConnectionValueType``) items
        Stores the created value type instances.
    VALUE_TYPE : `type` = `int`
        The value types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the value types.
    
    Every predefined value type can be accessed as class attribute as well:
    +---------------------------+---------------------------+-------+
    | Class attribute name      | name                      | value |
    +===========================+===========================+=======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | integer                   | integer                   | 1     |
    +---------------------------+---------------------------+-------+
    | datetime                  | datetime                  | 2     |
    +---------------------------+---------------------------+-------+
    | boolean                   | boolean                   | 3     |
    +---------------------------+---------------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ('deserializer', 'serializer')
    

    @classmethod
    def _from_value(cls, value):
        """
        Creates a new application role connection value type with the given value.
        
        Parameters
        ----------
        value : `int`
            The application role connection value type's identifier value.
        
        Returns
        -------
        self : ``ApplicationRoleConnectionValueType``
            The created instance.
        """
        self = object.__new__(cls)
        self.name = cls.DEFAULT_NAME
        self.value = value
        self.deserializer = cls.none.deserializer
        self.serializer = cls.none.serializer
        
        return self
    
    
    def __init__(self, value, name, deserializer, serializer):
        """
        Creates an ``ApplicationRoleConnectionValueType`` and stores it at the class's `.INSTANCES` class
        attribute as well.
        
        Parameters
        ----------
        value : `int`
            The identifier value of the application role connection value type.
        name : `str`
            The default name of the application role connection value type.
        deserializer : `FunctionType`
            Function used to deserialize values.
        serializer : `FunctionType`
            Function used to serialize values.
        """
        self.value = value
        self.name = name
        self.deserializer = deserializer
        self.serializer = serializer
        
        self.INSTANCES[value] = self
    
    
    # predefined
    none = P(
        0,
        'none',
        (lambda value: value),
        (lambda value: value),
    )
    integer = P(
        1,
        'integer',
        (lambda value: int(value) if value.isdecimal() else None),
        (lambda value: format(value, 'd')),
    )
    datetime = P(
        2,
        'datetime',
        timestamp_to_datetime_soft,
        datetime_to_timestamp,
    )
    boolean = P(
        3,
        'boolean',
        (lambda value: {'0': False, '1': True}.get(value, None)),
        (lambda value: '1' if value else '0'),
    )


class ApplicationRoleConnectionMetadataType(PreinstancedBase):
    """
    Represents an application role connection type.
    
    Attributes
    ----------
    name : `str`
        The name of the application role connection type.
    value : `int`
        The Discord side identifier value of the application role connection type.
    value_type : ``ApplicationRoleConnectionValueType``
        Additional information describing the metadata's value's type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationRoleConnectionMetadataType``) items
        Stores the created application role connection type instances. This container is accessed when translating a
        Discord application role connection type's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The application role connection types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the application role connection types.
    
    Every predefined application role connection type can be accessed as class attribute as well:
    +---------------------------+---------------------------+-------+---------------+
    | Class attribute name      | name                      | value | value type    |
    +===========================+===========================+=======+===============+
    | none                      | none                      | 0     | none          |
    +---------------------------+---------------------------+-------+---------------+
    | integer_less_or_equal     | integer less or equal     | 1     | integer       |
    +---------------------------+---------------------------+-------+---------------+
    | integer_greater_or_equal  | integer greater or equal  | 2     | integer       |
    +---------------------------+---------------------------+-------+---------------+
    | integer_equal             | integer equal             | 3     | integer       |
    +---------------------------+---------------------------+-------+---------------+
    | integer_not_equal         | integer not equal         | 4     | integer       |
    +---------------------------+---------------------------+-------+---------------+
    | datetime_less_or_equal    | datetime less or equal    | 5     | datetime      |
    +---------------------------+---------------------------+-------+---------------+
    | datetime_greater_or_equal | datetime greater or equal | 6     | datetime      |
    +---------------------------+---------------------------+-------+---------------+
    | boolean_equal             | boolean equal             | 7     | boolean       |
    +---------------------------+---------------------------+-------+---------------+
    | boolean_not_equal         | boolean not equal         | 8     | boolean       |
    +---------------------------+---------------------------+-------+---------------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ('value_type',)
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new application role connection metadata type with the given value.
        
        Parameters
        ----------
        value : `int`
            The application role connection metadata type's identifier value.
        
        Returns
        -------
        self : ``ApplicationRoleConnectionMetadataType``
            The created instance.
        """
        self = object.__new__(cls)
        self.name = cls.DEFAULT_NAME
        self.value = value
        self.value_type = ApplicationRoleConnectionValueType.none
        
        return self
    
    
    def __init__(self, value, name, value_type):
        """
        Creates an ``ApplicationRoleConnectionMetadataType`` and stores it at the class's `.INSTANCES` class
        attribute as well.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the application role connection metadata type.
        name : `str`
            The default name of the application role connection metadata type.
        value_type : ``ApplicationRoleConnectionValueType``
            Additional information describing the metadata's value's type.
        """
        self.value = value
        self.name = name
        self.value_type = value_type
        
        self.INSTANCES[value] = self
    
    # predefined
    none = P(0, 'none', ApplicationRoleConnectionValueType.none)
    integer_less_or_equal = P(1, 'integer less or equal', ApplicationRoleConnectionValueType.integer)
    integer_greater_or_equal = P(2, 'integer greater or equal', ApplicationRoleConnectionValueType.integer)
    integer_equal = P(3, 'integer equal', ApplicationRoleConnectionValueType.integer)
    integer_not_equal = P(4, 'integer not equal', ApplicationRoleConnectionValueType.integer)
    datetime_less_or_equal = P(5, 'datetime less or equal', ApplicationRoleConnectionValueType.datetime)
    datetime_greater_or_equal = P(6, 'datetime not equal', ApplicationRoleConnectionValueType.datetime)
    boolean_equal = P(7, 'boolean equal', ApplicationRoleConnectionValueType.boolean)
    boolean_not_equal = P(8, 'boolean not equal', ApplicationRoleConnectionValueType.boolean)
