__all__ = ('VerificationScreenStepType',)

from ...bases import Preinstance as P, PreinstancedBase


class VerificationScreenStepType(PreinstancedBase):
    """
    Represents a type of a ``VerificationScreenStep``.

    Attributes
    ----------
    name : `str`
        The verification screen step type's name.
    value : `str`
        The Discord side identifier value of the verification step types.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``VerificationScreenStepType``) items
        Stores the predefined ``VerificationScreenStepType``-s.
    VALUE_TYPE : `type` = `str`
        The verification screen steps' values' type.
    DEFAULT_NAME : `str` = `''`
        The default name of the verification screen step types. New verification screen step types have their name
        generated from their value, so it is not applicable for them.
    
    Every predefined verification screen step type can be accessed as class attribute as well:
    
    +-----------------------+-------------------+-------------------+
    | Class attribute names | Name              | Value             |
    +=======================+===================+===================+
    | none                  | none              | -                 |
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
    INSTANCES = {}
    VALUE_TYPE = str
    DEFAULT_NAME = ''
    
    __slots__ = ()
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new verification screen type with the given value.
        
        Parameters
        ----------
        value : `str`
            The verification screen type's identifier value.
        
        Returns
        -------
        self : ``VerificationScreenStepType``
            The verification screen type.
        """
        self = object.__new__(cls)
        self.value = value
        self.name = value.lower().replace('_', ' ')
        self.INSTANCES[value] = self
        return self
    
    
    def __repr__(self):
        """Returns the representation of the verification screen type."""
        return f'{self.__class__.__name__}(value={self.value!r})'
    
    
    none = P('', 'none')
    rules = P('TERMS', 'rules')
    text_input = P('TEXT_INPUT', 'text input')
    paragraph = P('PARAGRAPH', 'paragraph')
    multiple_choices = P('MULTIPLE_CHOICES', 'multiple_choices')
    verification = P('VERIFICATION', 'verification',)
