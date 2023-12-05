__all__ = ('LabelType', 'ReleasePhase',)

from ...bases import Preinstance as P, PreinstancedBase


class LabelType(PreinstancedBase):
    """
    Represents a embedded activity's label's type.
    
    Attributes
    ----------
    name : `str`
        The name of the label's type.
    value : `int`
        The identifier value the label's type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``LabelType``) items
        Stores the predefined label's types. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The label's types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the label's types.
    
    Every predefined label's type can be accessed as class attribute as well:
    
    +-----------------------+-----------+-------+
    | Class attribute name  | Name      | Value |
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


class ReleasePhase(PreinstancedBase):
    """
    Represents the release phase of an embedded activity on a platform.
    
    Attributes
    ----------
    value : `str`
        The Discord side identifier value of the platform.
    name : `str`
        The name of the release phase.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ReleasePhase``) items
        Stores the predefined release phases. This container is accessed when converting Discord side release phase's
        value to it's wrapper side representation.
    VALUE_TYPE : `type` = `str`
        The release phases' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the release phases.
    
    Every predefined release phase can also be accessed as class attribute:
    
    +-----------------------+---------------+---------------+
    | Class attribute name  | name          | value         |
    +=======================+===============+===============+
    | global_launch         | global launch | global_launch |
    +-----------------------+---------------+---------------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    
    __slots__ = ()

    # predefined
    global_launch = P('global_launch', 'global launch')


ReleasePhase.INSTANCES[''] = ReleasePhase.global_launch
