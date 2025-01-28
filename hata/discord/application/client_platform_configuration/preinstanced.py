__all__ = ('LabelType', 'ReleasePhase',)

from ...bases import Preinstance as P, PreinstancedBase


class LabelType(PreinstancedBase, value_type = int):
    """
    Represents a embedded activity's label's type.
    
    Attributes
    ----------
    name : `str`
        The name of the label's type.
    
    value : `int`
        The identifier value the label's type.
    
    Type Attributes
    ---------------
    Every predefined label's type can be accessed as type attribute as well:
    
    +-----------------------+-----------+-------+
    | Type attribute name   | Name      | Value |
    +=======================+===========+=======+
    | none                  | none      | 0     |
    +-----------------------+-----------+-------+
    | new                   | new       | 1     |
    +-----------------------+-----------+-------+
    | updated               | updated   | 2     |
    +-----------------------+-----------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none')
    new = P(1, 'new')
    updated = P(2, 'updated')


class ReleasePhase(PreinstancedBase, value_type = str):
    """
    Represents the release phase of an embedded activity on a platform.
    
    Attributes
    ----------
    name : `str`
        The name of the release phase.
    
    value : `str`
        The Discord side identifier value of the platform.
    
    Type Attributes
    ---------------
    Every predefined release phase can also be accessed as type attribute:
    
    +-----------------------+---------------+---------------+
    | Type attribute name   | name          | value         |
    +=======================+===============+===============+
    | global_launch         | global launch | global_launch |
    +-----------------------+---------------+---------------+
    """
    __slots__ = ()

    # predefined
    global_launch = P('global_launch', 'global launch')


ReleasePhase.INSTANCES[''] = ReleasePhase.global_launch
