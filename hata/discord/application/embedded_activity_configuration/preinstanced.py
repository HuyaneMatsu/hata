__all__ = ('OrientationLockState', 'PlatformType',)

from ...bases import Preinstance as P, PreinstancedBase


class OrientationLockState(PreinstancedBase):
    """
    Represents a embedded activity's orientation lock state.
    
    Attributes
    ----------
    name : `str`
        The name of the orientation lock state.
    value : `int`
        The identifier value the orientation lock state.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``OrientationLockState``) items
        Stores the predefined orientation lock states. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The orientation lock states' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the orientation lock states.
    
    Every predefined orientation lock state can be accessed as class attribute as well:
    
    +-----------------------+-----------+-------+
    | Class attribute name  | Name      | Value |
    +=======================+===========+=======+
    | none                  | none      | 0     |
    +-----------------------+-----------+-------+
    | unlocked              | unlocked  | 1     |
    +-----------------------+-----------+-------+
    | portrait              | portrait  | 2     |
    +-----------------------+-----------+-------+
    | landscape             | landscape | 3     |
    +-----------------------+-----------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none')
    unlocked = P(1, 'unlocked')
    portrait = P(2, 'portrait')
    landscape = P(3, 'landscape')


class PlatformType(PreinstancedBase):
    """
    Represents a supported platform by an embedded activity.
    
    Attributes
    ----------
    value : `str`
        The Discord side identifier value of the platform.
    name : `str`
        The name of the platform type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``PlatformType``) items
        Stores the predefined platform types. This container is accessed when converting Discord side platform type's
        value to it's wrapper side representation.
    VALUE_TYPE : `type` = `str`
        The platform types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the platform types.
    
    Every predefined platform type can also be accessed as class attribute:
    
    +-----------------------+---------------+-----------+
    | Class attribute name  | name          | value     |
    +=======================+===============+===========+
    | android               | android       | android   |
    +-----------------------+---------------+-----------+
    | ios                   | ios           | ios       |
    +-----------------------+---------------+-----------+
    | web                   | web           | web       |
    +-----------------------+---------------+-----------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    
    __slots__ = ()

    # predefined
    android = P('android', 'android')
    ios = P('ios', 'ios')
    web = P('web', 'web')


PlatformType.INSTANCES[''] = PlatformType.web
