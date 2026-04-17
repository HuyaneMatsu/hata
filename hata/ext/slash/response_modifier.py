__all__ = ()

from scarletio import RichAttributeErrorBaseType

from ...discord.allowed_mentions import AllowedMentionProxy
from ...discord.message import MessageFlag
from ...discord.message.message_builder.conversions import CONVERSION_ALLOWED_MENTIONS, CONVERSION_FLAGS
from ...discord.preconverters import preconvert_bool


MESSAGE_FLAG_VALUE_SHOW_FOR_INVOKING_USER_ONLY = MessageFlag().update_by_keys(invoking_user_only = True)


def _validate_show_for_invoking_user_only(show_for_invoking_user_only):
    """
    Validates the given `show_for_invoking_user_only` value.
    
    Parameters
    ----------
    show_for_invoking_user_only : `bool`
        The `show_for_invoking_user_only` value to validate.
    
    Returns
    -------
    show_for_invoking_user_only : `None` or `bool`
        The validated `show_for_invoking_user_only` value.
    
    Raises
    ------
    TypeError
        If `show_for_invoking_user_only` was not given as `bool`.
    """
    show_for_invoking_user_only = preconvert_bool(show_for_invoking_user_only, 'show_for_invoking_user_only')
    
    return show_for_invoking_user_only


def _validate_allowed_mentions(allowed_mentions):
    """
    Validates the given `allowed_mentions` parameter.
    
    Parameters
    ----------
    allowed_mentions : `None`, `str`, ``UserBase``, ``Role``, ``AllowedMentionProxy``, \
            `list` of (`str`, ``UserBase``, ``Role`` )
         Which user or role can the response message ping (or everyone).
    
    Returns
    -------
    allowed_mention_proxy : ``AllowedMentionProxy``
    """
    if allowed_mentions is None:
        allowed_mention_proxy = AllowedMentionProxy()
    elif isinstance(allowed_mentions, AllowedMentionProxy):
        allowed_mention_proxy = allowed_mentions.copy()
    elif isinstance(allowed_mentions, list):
        allowed_mention_proxy = AllowedMentionProxy(*allowed_mentions)
    else:
        allowed_mention_proxy = AllowedMentionProxy(allowed_mentions)
    
    return allowed_mention_proxy


def _validate_wait_for_acknowledgement(wait_for_acknowledgement):
    """
    Validates the given `wait_for_acknowledgement` value.
    
    Parameters
    ----------
    wait_for_acknowledgement : `bool`
        The `wait_for_acknowledgement` value to validate.
    
    Returns
    -------
    wait_for_acknowledgement : `None` or `bool`
        The validated `wait_for_acknowledgement` value.
    
    Raises
    ------
    TypeError
        If `wait_for_acknowledgement` was not given as `bool`.
    """
    wait_for_acknowledgement = preconvert_bool(wait_for_acknowledgement, 'wait_for_acknowledgement')
    
    return wait_for_acknowledgement


class ResponseModifier(RichAttributeErrorBaseType):
    """
    Modifies values returned and yielded to command coroutine processor.
    
    Attributes
    ----------
    allowed_mentions : `None`, ``AllowedMentionProxy``
         Which user or role can the response message ping (or everyone).
    wait_for_acknowledgement : `bool`
        Whether acknowledge tasks should be ensure asynchronously.
    show_for_invoking_user_only : `None`, `bool`
        Whether the response message should only be shown for the invoking user.
    """
    __slots__ = ('allowed_mentions', 'wait_for_acknowledgement', 'show_for_invoking_user_only',)
    
    def __new__(cls, keyword_parameters):
        """
        Creates a new request modifiers from additionally defined
        
        Parameters
        ----------
        keyword_parameters : `dict<str, object>`
            Additional keyword parameters.
        
        Returns
        -------
        self : `None` / ``ResponseModifier``
            Returns `None` if there are no request modifiers specified.
        
        Raises
        ------
        TypeError
            If a parameter's type is incorrect.
        ValueError
            If a parameter's value is incorrect.
        """
        if keyword_parameters:
            parameters_found = False
            
            try:
                allowed_mentions = keyword_parameters.pop('allowed_mentions')
            except KeyError:
                allowed_mentions = None
            else:
                allowed_mentions = _validate_allowed_mentions(allowed_mentions)
                parameters_found = True
            
            try:
                show_for_invoking_user_only = keyword_parameters.pop('show_for_invoking_user_only')
            except KeyError:
                show_for_invoking_user_only = None
            else:
                show_for_invoking_user_only = _validate_show_for_invoking_user_only(show_for_invoking_user_only)
                parameters_found = True
            
            try:
                wait_for_acknowledgement = keyword_parameters.pop('wait_for_acknowledgement')
            except KeyError:
                wait_for_acknowledgement = None
            else:
                wait_for_acknowledgement = _validate_wait_for_acknowledgement(wait_for_acknowledgement)
                parameters_found = True
            
            if parameters_found:
                self = object.__new__(cls)
                self.allowed_mentions = allowed_mentions
                self.wait_for_acknowledgement = wait_for_acknowledgement
                self.show_for_invoking_user_only = show_for_invoking_user_only
            else:
                self = None
        else:
            self = None
        
        return self
    
    
    def apply_to_creation(self, interaction_response):
        """
        Applies the response creation modifiers to the given parameters.
        
        Parameters
        ----------
        interaction_response : ``InteractionResponse``
            Interaction response to apply self to.
        """
        self._apply_to_shared(interaction_response)
        
        show_for_invoking_user_only = self.show_for_invoking_user_only
        if (show_for_invoking_user_only is not None):
            # This is a nested + nested field, so passing it as False does nothing.
            interaction_response._setter_field(
                CONVERSION_FLAGS,
                (MESSAGE_FLAG_VALUE_SHOW_FOR_INVOKING_USER_ONLY if show_for_invoking_user_only else False),
            )
    
    
    def apply_to_edition(self, interaction_response):
        """
        Applies the response edition modifiers to the given parameters.
        
        Parameters
        ----------
        interaction_response : ``InteractionResponse``
            Interaction response to apply self to.
        """
        self._apply_to_shared(interaction_response)
    
    
    def _apply_to_shared(self, interaction_response):
        """
        Applies creation and edition modifiers to the given parameters.
        
        Parameters
        ----------
        interaction_response : ``InteractionResponse``
            Interaction response to apply self to.
        """
        allowed_mentions = self.allowed_mentions
        if (allowed_mentions is not None):
            for _ in interaction_response._try_pull_field_value(CONVERSION_ALLOWED_MENTIONS):
                break
            else:
                interaction_response._setter_field(
                    CONVERSION_ALLOWED_MENTIONS,
                    allowed_mentions,
                )
    
    
    def __repr__(self):
        """Returns the parameter modifier's representation."""
        repr_parts = ['<', type(self).__name__]
        
        
        allowed_mentions = self.allowed_mentions
        if (allowed_mentions is not None):
            repr_parts.append(' allowed_mentions = ')
            repr_parts.append(repr(allowed_mentions))
            
            field_added = True
        
        else:
            field_added = False
        
        
        show_for_invoking_user_only = self.show_for_invoking_user_only
        if (show_for_invoking_user_only is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' show_for_invoking_user_only = ')
            repr_parts.append(repr(show_for_invoking_user_only))
        
        

        wait_for_acknowledgement = self.wait_for_acknowledgement
        if (wait_for_acknowledgement is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' wait_for_acknowledgement = ')
            repr_parts.append(repr(wait_for_acknowledgement))
        
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the parameter modifier's hash value."""
        hash_value = 0
        
        allowed_mentions = self.allowed_mentions
        if (allowed_mentions is not None):
            hash_value ^= hash(allowed_mentions)
        
        show_for_invoking_user_only = self.show_for_invoking_user_only
        if (show_for_invoking_user_only is not None):
            hash_value ^= show_for_invoking_user_only

        wait_for_acknowledgement = self.wait_for_acknowledgement
        if (wait_for_acknowledgement is not None):
            hash_value ^= wait_for_acknowledgement << 4
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two parameter modifiers are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.allowed_mentions != other.allowed_mentions:
            return False
        
        if self.wait_for_acknowledgement != other.wait_for_acknowledgement:
            return False
        
        if self.show_for_invoking_user_only != other.show_for_invoking_user_only:
            return False
        
        return True


def get_show_for_invoking_user_only_of(response_modifier):
    """
    Gets the `show_for_invoking_user_only` value of the given response modifier.
    
    Parameters
    ----------
    response_modifier : `None`, ``ResponseModifier``
        The respective response modifier if any,
    
    Returns
    -------
    show_for_invoking_user_only : `bool`
    """
    if response_modifier is None:
        show_for_invoking_user_only = False
    else:
        show_for_invoking_user_only = response_modifier.show_for_invoking_user_only
        if show_for_invoking_user_only is None:
            show_for_invoking_user_only = False
    
    return show_for_invoking_user_only


def get_show_for_invoking_user_only_from(interaction_response, response_modifier):
    """
    Gets the `show_for_invoking_user_only` value from the given parameters from the given response modifier if not
    present.
    
    Parameters
    ----------
    interaction_response : ``InteractionResponse``
        Interaction response to pull from.
    response_modifier : `None`, ``ResponseModifier``
        The respective response modifier if any,
    
    Returns
    -------
    show_for_invoking_user_only : `bool`
    """
    for value in interaction_response._try_pull_field_value(CONVERSION_FLAGS):
        return (True if value & MESSAGE_FLAG_VALUE_SHOW_FOR_INVOKING_USER_ONLY else False)
    
    return  get_show_for_invoking_user_only_of(response_modifier)


def get_wait_for_acknowledgement_of(response_modifier):
    """
    Gets the `wait_for_acknowledgement` value of the given response modifier.
    
    Parameters
    ----------
    wait_for_acknowledgement : `None`, ``ResponseModifier``
        The respective response modifier if any,
    
    Returns
    -------
    wait_for_acknowledgement : `bool`
    """
    if response_modifier is None:
        wait_for_acknowledgement = False
    else:
        wait_for_acknowledgement = response_modifier.wait_for_acknowledgement
    
    return wait_for_acknowledgement
