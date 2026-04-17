__all__ = ('OnboardingPromptType',)

from scarletio import export

from ...bases import Preinstance as P, PreinstancedBase


@export
class OnboardingPromptType(PreinstancedBase, value_type = int):
    """
    The type of an onboarding prompt.
    
    Attributes
    ----------
    name : `str`
        The name of the onboarding prompt type.
    
    value : `int`
        The identifier value the onboarding prompt type.
    
    Type Attributes
    ---------------
    Every predefined onboarding prompt type can be accessed as type attribute as well:
    
    +-----------------------------------+-----------------------------------+-------+
    | Type attribute name               | Name                              | Value |
    +===================================+===================================+=======+
    | multiple_choice                   | multiple choice                   | 0     |
    +-----------------------------------+-----------------------------------+-------+
    | dropdown                          | dropdown                          | 1     |
    +-----------------------------------+-----------------------------------+-------+
    """
    __slots__ = ()
    
    multiple_choice = P(0, 'multiple choice')
    dropdown = P(1, 'dropdown')
