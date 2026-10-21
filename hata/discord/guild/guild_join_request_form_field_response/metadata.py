__all__ = (
    'GuildJoinRequestFormFieldResponseMetadataBase', 'GuildJoinRequestFormFieldResponseMetadataChoiceSingle',
    'GuildJoinRequestFormFieldResponseMetadataBooleanTerms', 'GuildJoinRequestFormFieldResponseMetadataTextInput',
)


from scarletio import RichType

from ...bases import PlaceHolder


class GuildJoinRequestFormFieldResponseMetadataBase(metaclass = RichType, rich_type_feature_flags = ~0):
    __slots__ = ()
    
    accepted = PlaceHolder(
        False,
        """
        Whether the terms have been accepted.
        
        Returns
        -------
        accepted : `bool`
        """,
    )
    
    terms = PlaceHolder(
        None,
        """
        The accepted terms.
        
        Returns
        -------
        terms : `None | tuple<str>`
        """,
    )
    
    placeholder = PlaceHolder(
        None,
        """
        Placeholder text show inside the input.
        
        Returns
        -------
        placeholder : `None | str`
        """,
    )
    
    value = PlaceHolder(
        None,
        """
        The value inputted by the user.
        
        Returns
        -------
        value : `None | str`
        """,
    )
    
    choice_index = PlaceHolder(
        -1,
        """
        The choice's index selected by the user. `-1` if the user did not chose anything.
        
        Returns
        -------
        choice_index : `int`
        """,
    )
    
    choices = PlaceHolder(
        None,
        """
        The offered choices.
        
        Returns
        -------
        choices : `None | tuple<str>`
        """,
    )


class GuildJoinRequestFormFieldResponseMetadataBooleanTerms(GuildJoinRequestFormFieldResponseMetadataBase):
    """
    Attributes
    ----------
    accepted : `bool`
        Whether the terms have been accepted.
    
    terms : `None | tuple<str>`
        The accepted terms.
    """
    __slots__ = ('accepted', 'terms')


class GuildJoinRequestFormFieldResponseMetadataTextInput(GuildJoinRequestFormFieldResponseMetadataBase):
    """
    Attributes
    ----------
    placeholder : `None | str`
        Placeholder text show inside the input.
    
    value : `None | str`
        The value inputted by the user.
    """
    __slots__ = ('placeholder', 'value')


class GuildJoinRequestFormFieldResponseMetadataChoiceSingle(GuildJoinRequestFormFieldResponseMetadataBase):
    """
    Attributes
    ----------
    choice_index : `int`
        The choice's index selected by the user. `-1` if the user did not chose anything.
    
    choices : `None | tuple<str>`
        The offered choices.
    """
    __slots__ = ('choice_index', 'choices')
