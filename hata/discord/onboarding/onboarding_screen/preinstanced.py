__all__ = ('OnboardingMode',)

from ...bases import Preinstance as P, PreinstancedBase


class OnboardingMode(PreinstancedBase, value_type = int):
    """
    Onboarding mode.
    
    Attributes
    ----------
    name : `str`
        The default name of the onboarding mode.
    
    value : `int`
        The discord side identifier value of the onboarding mode.
    
    Type Attributes
    ---------------
    Every predefined onboarding mode can be accessed as type attribute as well:
    
    +-------------------------------+---------------------------+-------+
    | Type attribute name           | name                      | value |
    +===============================+===========================+=======+
    | default                       | default                   | 0     |
    +-------------------------------+---------------------------+-------+
    | advanced                      | advanced                  | 1     |
    +-------------------------------+---------------------------+-------+
    """
    __slots__ = ()
    
    default = P(0, 'default')
    advanced = P(1, 'advanced')
