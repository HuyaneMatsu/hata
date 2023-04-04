__all__ = ('VoiceChannelEffectAnimationType',)

from ...bases import Preinstance as P, PreinstancedBase


class VoiceChannelEffectAnimationType(PreinstancedBase):
    """
    Voice channel effect animation type.
    
    Attributes
    ----------
    name : `str`
        The default name of the voice channel effect animation type.
    value : `int`
        The discord side identifier value of the voice channel effect animation type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``VoiceChannelEffectAnimationType``) items
        Stores the predefined ``VoiceChannelEffectAnimationType``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The voice channel effect animation type' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the voice channel effect animation type.
    
    Every predefined voice channel effect animation type can be accessed as class attribute as well:
    
    +-----------------------------------+---------------------------+-------+
    | Class attribute name              | Name                      | Value |
    +===================================+===========================+=======+
    | premium                           | premium                   | 0     |
    +-----------------------------------+---------------------------+-------+
    | basic                             | basic                     | 1     |
    +-----------------------------------+---------------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    premium = P(0, 'premium')
    basic = P(1, 'basic')
