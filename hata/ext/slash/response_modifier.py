__all__ = ()

from scarletio import RichAttributeErrorBaseType

from ...discord.allowed_mentions import AllowedMentionProxy
from ...discord.preconverters import preconvert_bool


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
    
    def __new__(cls, kwargs):
        """
        Creates a new request modifiers from additionally defined
        
        Parameters
        ----------
        kwargs : `dict` of (`str`, `Any`) items
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
        if kwargs:
            parameters_found = False
            
            try:
                allowed_mentions = kwargs.pop('allowed_mentions')
            except KeyError:
                allowed_mentions = None
            else:
                allowed_mentions = _validate_allowed_mentions(allowed_mentions)
                parameters_found = True
            
            try:
                show_for_invoking_user_only = kwargs.pop('show_for_invoking_user_only')
            except KeyError:
                show_for_invoking_user_only = None
            else:
                show_for_invoking_user_only = _validate_show_for_invoking_user_only(show_for_invoking_user_only)
                parameters_found = True
            
            try:
                wait_for_acknowledgement = kwargs.pop('wait_for_acknowledgement')
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
    
    
    def apply_to_creation(self, parameters):
        """
        Applies the response creation modifiers to the given parameters.
        
        Parameters
        ----------
        parameters : `dict` of (`str`, `Any`) items
            Request parameters.
        """
        self._apply_to_shared(parameters)
        
        show_for_invoking_user_only = self.show_for_invoking_user_only
        if (show_for_invoking_user_only is not None):
            parameters.setdefault('show_for_invoking_user_only', show_for_invoking_user_only)
    
    
    def apply_to_edition(self, parameters):
        """
        Applies the response edition modifiers to the given parameters.
        
        Parameters
        ----------
        parameters : `dict` of (`str`, `Any`) items
            Request parameters.
        """
        self._apply_to_shared(parameters)
    
    
    def _apply_to_shared(self, parameters):
        """
        Applies creation and edition modifiers to the given parameters.
        
        Parameters
        ----------
        parameters : `dict` of (`str`, `Any`) items
            Request parameters.
        """
        allowed_mentions = self.allowed_mentions
        if (allowed_mentions is not None):
            parameters.setdefault('allowed_mentions', allowed_mentions)
    
    
    def __repr__(self):
        """Returns the parameter modifier's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        
        allowed_mentions = self.allowed_mentions
        if (allowed_mentions is None):
            field_added = False
            repr_parts.append(' allowed_mentions=')
            repr_parts.append(repr(allowed_mentions))
        
        else:
            field_added = True
        
        
        show_for_invoking_user_only = self.show_for_invoking_user_only
        if (show_for_invoking_user_only is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' show_for_invoking_user_only=')
            repr_parts.append(repr(show_for_invoking_user_only))
        
        

        wait_for_acknowledgement = self.wait_for_acknowledgement
        if (wait_for_acknowledgement is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' wait_for_acknowledgement=')
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


def get_show_for_invoking_user_only_from(parameters, response_modifier):
    """
    Gets the `show_for_invoking_user_only` value from the given parameters from the given response modifier if not
    present.
    
    Parameters
    ----------
    parameters : `dict` of (`str`, `Any` items
        Request parameters.
    response_modifier : `None`, ``ResponseModifier``
        The respective response modifier if any,
    
    Returns
    -------
    show_for_invoking_user_only : `bool`
    """
    try:
        show_for_invoking_user_only = parameters['show_for_invoking_user_only']
    except KeyError:
        show_for_invoking_user_only = get_show_for_invoking_user_only_of(response_modifier)
    
    return show_for_invoking_user_only


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


DUMMY_DICT = {}

def un_map_pack_response_creation_modifier(response_modifier):
    """
    Returns an un-map-packer to the given response modifier for message creation endpoints.
    
    Parameters
    ----------
    response_modifier : `None`, ``ResponseModifier``
        The response modifier to un-map-pack if any.
    
    Returns
    -------
    un_map_packer : `dict`
    
    Notes
    -----
    We could have use ``un_map_pack``, but dictionaries are just faster.
    """
    if response_modifier is None:
        return DUMMY_DICT
    
    dictionary = {}
    response_modifier.apply_to_creation(dictionary)
    return dictionary


def un_map_pack_response_edition_modifier(response_modifier):
    """
    Returns an un-map-packer to the given response modifier for message edition endpoints.
    
    Parameters
    ----------
    response_modifier : `None`, ``ResponseModifier``
        The response modifier to un-map-pack if any.
    
    Returns
    -------
    un_map_packer : `dict`
    
    Notes
    -----
    We could have use ``un_map_pack``, but dictionaries are just faster.
    """
    if response_modifier is None:
        return DUMMY_DICT
    
    dictionary = {}
    response_modifier.apply_to_edition(dictionary)
    return dictionary
