__all__ = ('OnboardingPromptType',)

from scarletio import export

from ...bases import Preinstance as P, PreinstancedBase


@export
class OnboardingPromptType(PreinstancedBase):
    """
    The type of an onboarding prompt.
    
    Attributes
    ----------
    name : `str`
        The name of the onboarding prompt type.
    value : `int`
        The identifier value the onboarding prompt type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``OnboardingPromptType``) items
        Stores the predefined ``OnboardingPromptType``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The application command option types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the onboarding prompt types.
    
    Every predefined onboarding prompt type can be accessed as class attribute as well:
    
    +-----------------------------------+-----------------------------------+-------+
    | Class attribute name              | Name                              | Value |
    +===================================+===================================+=======+
    | multiple_choice                   | multiple choice                   | 0     |
    +-----------------------------------+-----------------------------------+-------+
    | dropdown                          | dropdown                          | 1     |
    +-----------------------------------+-----------------------------------+-------+
    """
    __slots__ = ()
    
    INSTANCES = {}
    VALUE_TYPE = int
    
    
    multiple_choice = P(0, 'multiple choice')
    dropdown = P(1, 'dropdown')
