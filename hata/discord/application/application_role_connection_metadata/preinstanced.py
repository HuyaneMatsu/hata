__all__ = ('ApplicationRoleConnectionMetadataType', 'ApplicationRoleConnectionValueType')

from ...bases import Preinstance as P, PreinstancedBase
from ...utils import datetime_to_timestamp, timestamp_to_datetime_soft


class ApplicationRoleConnectionValueType(PreinstancedBase, value_type = int):
    """
    Type information for application role connection metadata values'.
    
    > This type is wrapper side only.
    
    Attributes
    ----------
    deserializer : `FunctionType`
        Function used to deserialize values.
    
    name : `str`
        The name of the value type.
    
    serializer : `FunctionType`
        Function used to serialize values.
    
    value : `int`
        The identifier of the value type.
    
    Type Attributes
    ---------------
    Every predefined value type can be accessed as type attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Type attribute name       | name                      | value |
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
    __slots__ = ('deserializer', 'serializer')
    
    DESERIALIZER_DEFAULT = lambda value: value
    SERIALIZER_DEFAULT = DESERIALIZER_DEFAULT
    
    def __new__(cls, value, name = None, deserializer = None, serializer = None):
        """
        Creates an application role connection value type.
        
        Parameters
        ----------
        value : `int`
            The identifier value of the application role connection value type.
        
        name : `None | str` = `None`, Optional
            The default name of the application role connection value type.
        
        deserializer : `None | FunctionType` = `None`, Optional
            Function used to deserialize values.
        
        serializer : `None | FunctionType` = `None`, Optional
            Function used to serialize values.
        """
        if deserializer is None:
            deserializer = cls.DESERIALIZER_DEFAULT
        
        if serializer is None:
            serializer = cls.SERIALIZER_DEFAULT
        
        self = PreinstancedBase.__new__(cls, value, name)
        self.deserializer = deserializer
        self.serializer = serializer
        return self
    
    
    # predefined
    none = P(
        0,
        'none',
        DESERIALIZER_DEFAULT,
        SERIALIZER_DEFAULT,
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


class ApplicationRoleConnectionMetadataType(PreinstancedBase, value_type = int):
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
    
    Type Attributes
    ---------------
    Every predefined application role connection type can be accessed as type attribute as well:
    
    +---------------------------+---------------------------+-------+---------------+
    | Type attribute name       | name                      | value | value type    |
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
    __slots__ = ('value_type',)
    
    def __new__(cls, value, name = None, value_type = None):
        """
        Creates an application role connection metadata type.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the application role connection metadata type.
        
        name : `str`
            The default name of the application role connection metadata type.
        
        value_type : `None | ApplicationRoleConnectionValueType` = `None`, Optional
            Additional information describing the metadata's value's type.
        """
        if value_type is None:
            value_type = ApplicationRoleConnectionValueType.none
        
        self = PreinstancedBase.__new__(cls, value, name)
        self.value_type = value_type
        return self
    
    
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
