__all__ = ('GuildJoinRequestFormFieldTextInputStyle', 'GuildJoinRequestFormFieldType')

from scarletio import copy_docs

from ...bases import Preinstance as P, PreinstancedBase


class GuildJoinRequestFormFieldType(PreinstancedBase, value_type = str):
    """
    Represents the type of a ``GuildJoinRequestFormFieldResponse``.
    
    Attributes
    ----------
    name : `str`
        Name.
    
    value : `str`
        Discord side identifier.
    
    Type Attributes
    ---------------
    Every predefined instance can also be accessed
    
    +-----------------------+-----------------------+-------------------+
    | Type attribute name   | Name                  | Value             |
    +=======================+=======================+===================+
    | none                  | none                  | -                 |
    +-----------------------+-----------------------+-------------------+
    | boolean_terms         | boolean terms         | TERMS             |
    +-----------------------+-----------------------+-------------------+
    | choice_single         | choice single         | MULTIPLE_CHOICE   |
    +-----------------------+-----------------------+-------------------+
    | text_input_short      | text input short      | TEXT_INPUT        |
    +-----------------------+-----------------------+-------------------+
    | text_input_paragraph  | text input paragraph  | PARAGRAPH         |
    +-----------------------+-----------------------+-------------------+
    """
    __slots__ = ()
    
    @copy_docs(PreinstancedBase.__new__)
    def __new__(cls, value, name = None):
        if name is None:
            name = value.caefold().replace('_', ' ')
        
        return PreinstancedBase.__new__(cls, value, name)
    
    none = P('', 'none')
    boolean_terms = P('TERMS', 'boolean terms')
    text_input_short = P('TEXT_INPUT', 'text input short')
    text_input_paragraph = P('PARAGRAPH', 'text input paragraph')
    choice_single = P('MULTIPLE_CHOICE', 'choice single')


class GuildJoinRequestFormFieldTextInputStyle(PreinstancedBase, value_type = int):
    """
    Represents the text display stale of ``GuildJoinRequestFormFieldResponse``-s.
    
    Attributes
    ----------
    name : `str`
        Name.
    
    value : `int`
        Internal identifier.
    
    Type Attributes
    ---------------
    Every predefined instance can also be accessed
    
    +-----------------------+-----------+-------+
    | Type attribute name   | Name      | Value |
    +=======================+===========+=======+
    | short                 | short     | 0     |
    +-----------------------+-----------+-------+
    | paragraph             | paragraph | 1     |
    +-----------------------+-----------+-------+
    """
    __slots__ = ()
    
    short = P(0, 'short')
    paragraph = P(1, 'paragraph')
