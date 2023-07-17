__all__ = ('OnboardingMode',)

from ...bases import Preinstance as P, PreinstancedBase


class OnboardingMode(PreinstancedBase):
    """
    Onboarding mode.
    
    Attributes
    ----------
    name : `str`
        The default name of the onboarding mode.
    value : `int`
        The discord side identifier value of the onboarding mode.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``OnboardingMode``) items
        Stores the predefined ``OnboardingMode``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The onboarding mode' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the onboarding mode.
    
    Every predefined onboarding mode can be accessed as class attribute as well:
    
    +-------------------------------+---------------------------+-------+
    | Class attribute name          | name                      | value |
    +===============================+===========================+=======+
    | default                       | default                   | 0     |
    +-------------------------------+---------------------------+-------+
    | advanced                      | advanced                  | 1     |
    +-------------------------------+---------------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    
    default = P(0, 'default')
    advanced = P(1, 'advanced')
