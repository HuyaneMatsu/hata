__all__ = ('OrientationLockState', 'PlatformType',)

from ...bases import Preinstance as P, PreinstancedBase


class OrientationLockState(PreinstancedBase, value_type = int):
    """
    Represents a embedded activity's orientation lock state.
    
    Attributes
    ----------
    name : `str`
        The name of the orientation lock state.
    
    value : `int`
        The identifier value the orientation lock state.
    
    Type Attributes
    ---------------
    Every predefined orientation lock state can be accessed as type attribute as well:
    
    +-----------------------+-----------+-------+
    | Type attribute name   | Name      | Value |
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
    __slots__ = ()
    
    none = P(0, 'none')
    unlocked = P(1, 'unlocked')
    portrait = P(2, 'portrait')
    landscape = P(3, 'landscape')


class PlatformType(PreinstancedBase, value_type = str):
    """
    Represents a supported platform by an embedded activity.
    
    Attributes
    ----------
    name : `str`
        The name of the platform type.
    
    value : `str`
        The Discord side identifier value of the platform.
    
    Type Attributes
    ---------------
    Every predefined platform type can also be accessed as type attribute:
    
    +-----------------------+---------------+-----------+
    | Type attribute name   | name          | value     |
    +=======================+===============+===========+
    | android               | android       | android   |
    +-----------------------+---------------+-----------+
    | ios                   | ios           | ios       |
    +-----------------------+---------------+-----------+
    | web                   | web           | web       |
    +-----------------------+---------------+-----------+
    """
    __slots__ = ()

    # predefined
    android = P('android', 'android')
    ios = P('ios', 'ios')
    web = P('web', 'web')


PlatformType.INSTANCES[''] = PlatformType.web
