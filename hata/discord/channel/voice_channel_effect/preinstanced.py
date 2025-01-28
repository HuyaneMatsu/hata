__all__ = ('VoiceChannelEffectAnimationType',)

from ...bases import Preinstance as P, PreinstancedBase


class VoiceChannelEffectAnimationType(PreinstancedBase, value_type = int):
    """
    Voice channel effect animation type.
    
    Attributes
    ----------
    name : `str`
        The default name of the voice channel effect animation type.
    
    value : `int`
        The discord side identifier value of the voice channel effect animation type.
    
    Type Attributes
    ---------------
    Every predefined voice channel effect animation type can be accessed as type attribute as well:
    
    +-----------------------------------+---------------------------+-------+
    | Type attribute name               | Name                      | Value |
    +===================================+===========================+=======+
    | premium                           | premium                   | 0     |
    +-----------------------------------+---------------------------+-------+
    | basic                             | basic                     | 1     |
    +-----------------------------------+---------------------------+-------+
    """
    __slots__ = ()
    
    # predefined
    premium = P(0, 'premium')
    basic = P(1, 'basic')
