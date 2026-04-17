__all__ = ('VerificationScreenStepType',)

from scarletio import copy_docs

from ...bases import Preinstance as P, PreinstancedBase


class VerificationScreenStepType(PreinstancedBase, value_type = str):
    """
    Represents a type of a ``VerificationScreenStep``.

    Attributes
    ----------
    name : `str`
        The verification screen step type's name.
    
    value : `str`
        The Discord side identifier value of the verification step types.
    
    Type Attributes
    ---------------
    Every predefined verification screen step type can be accessed as type attribute as well:
    
    +-----------------------+-------------------+-------------------+
    | Type attribute name   | Name              | Value             |
    +=======================+===================+===================+
    | none                  | none              |                   |
    +-----------------------+-------------------+-------------------+
    | rules                 | rules             | TERMS             |
    +-----------------------+-------------------+-------------------+
    | text_input            | text input        | TEXT_INPUT        |
    +-----------------------+-------------------+-------------------+
    | paragraph             | paragraph         | PARAGRAPH         |
    +-----------------------+-------------------+-------------------+
    | multiple_choices      | multiple choices  | MULTIPLE_CHOICES  |
    +-----------------------+-------------------+-------------------+
    | verification          | verification      | VERIFICATION      |
    +-----------------------+-------------------+-------------------+
    """
    __slots__ = ()
    
    @copy_docs(PreinstancedBase.__new__)
    def __new__(cls, value, name = None):
        if name is None:
            name = value.lower().replace('_', ' ')
        
        return PreinstancedBase.__new__(cls, value, name)
    
    
    none = P('', 'none')
    rules = P('TERMS', 'rules')
    text_input = P('TEXT_INPUT', 'text input')
    paragraph = P('PARAGRAPH', 'paragraph')
    multiple_choices = P('MULTIPLE_CHOICES', 'multiple_choices')
    verification = P('VERIFICATION', 'verification',)
