__all__ = (
    'create_button', 'create_channel_select', 'create_mentionable_select', 'create_role_select', 'create_row',
    'create_string_select', 'create_text_input', 'create_user_select'
)

from .component import Component, ComponentType


def create_button(
    label = ...,
    emoji = ...,
    *,
    custom_id = ...,
    enabled = ...,
    style = ...,
    url = ...,
):
    """
    Creates a new button component.
    
    Parameters
    -----------
    label : `None`, `str`, Optional
        Label of the component.
    
    emoji : `None`, ``Emoji``, Optional
        Emoji of the button if applicable.
    
    custom_id : `None`, `str`, Optional (Keyword only)
        Custom identifier to detect which button was clicked by the user.
        
        > Mutually exclusive with the `url` field.
    
    enabled : `bool`, Optional (Keyword only)
        Whether the button is enabled.
    
    style : `None`, ``ButtonStyle``, `int`, Optional (Keyword only)
        The button's style.
    
    url : `None`, `str`, Optional (Keyword only)
        Url to redirect to when clicking on the button.
        
        > Mutually exclusive with the `custom_id` field.
    
    Returns
    -------
    button : ``Component``
    
    Raises
    ------
    TypeError
        - If a parameter's type is incorrect.
    ValueError
        - If a parameter's value is incorrect.
        - `url` and `custom_id` are mutually exclusive.
    """
    return Component(
        ComponentType.button,
        button_style = style,
        custom_id = custom_id,
        label = label,
        enabled = enabled,
        emoji = emoji,
        url = url,
    )


def create_row(
    *components,
):
    """
    Creates a row component from the given components.
    
    Parameters
    ----------
    *components : `None`, `iterable` of ``Component``
        Sub components.
    
    Returns
    -------
    row : ``Component``
    
    Raises
    ------
    TypeError
        - If a parameter's type is incorrect.
    """
    return Component(
        ComponentType.row,
        components = components,
    )


def create_string_select(
    options,
    custom_id = ...,
    *,
    enabled = ...,
    placeholder = ...,
    max_values = ...,
    min_values = ...,
):
    """
    Creates a new string select.
    
    Parameters
    ----------
    options : `None` or `iterable` of ``StringSelectOption``
        Options of the select.
    
    custom_id : `None`, `str`, Optional
        Custom identifier to detect which component was used by the user.
    
    enabled : `bool`, Optional (Keyword only)
        Whether the button is enabled.
    
    placeholder : `None`, `str`, Optional (Keyword only)
        Placeholder text of the select.
    
    max_values : `int`, Optional (Keyword only)
        The maximal amount of options to select.
        
    min_values : `int`, Optional (Keyword only)
        The minimal amount of options to select.
    
    Returns
    -------
    string_select : ``Component``
    
    Raises
    ------
    TypeError
        - If a parameter's type is incorrect.
    ValueError
        - If a parameter's value is incorrect.
    """
    return Component(
        ComponentType.string_select,
        custom_id = custom_id,
        enabled = enabled,
        options = options,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
    )


def create_text_input(
    label = ...,
    *,
    custom_id = ...,
    max_length = ...,
    min_length = ...,
    placeholder = ...,
    required = ...,
    style = ...,
    value = ...,
):
    """
    Creates a new text input.
    
    Attributes
    ----------
    label : `None`, `str`, Optional
        Label of the component.
    
    custom_id : `None`, `str`, Optional (Keyword only)
        Custom identifier to detect which text input was clicked by the user.
        
        If not given, is autogenerated form the `label` parameter.
    
    max_length : `int`, Optional (Keyword only)
        The maximal length of the inputted text.
    
    min_length : `int`, Optional (Keyword only)
        The minimal length of the inputted text.
    
    placeholder : `None`, `str`, Optional (Keyword only)
        Placeholder text of the select.
    
    required : `None`, `bool`, Optional (Keyword only)
        Whether the field is required to be fulfilled.
        
        If not given, or given as `None`, will default to `True` if `min_length` is defined as higher than `0`.
    
    style : `None`, ``TextInputStyle``, `int`, Optional (Keyword only)
        The text input's style.
    
    value : `None`, `str`, Optional (Keyword only)
        The text input's default value.
    
    Returns
    -------
    text_input : ``Component``
    
    Raises
    ------
    TypeError
        - If a parameter's type is incorrect.
    ValueError
        - If a parameter's value is incorrect.
    """
    return Component(
        ComponentType.text_input,
        custom_id = custom_id,
        label = label,
        max_length = max_length,
        min_length = min_length,
        placeholder = placeholder,
        required = required,
        text_input_style = style,
        value = value,
    )


def create_user_select(
    custom_id = ...,
    *,
    default_values = ...,
    enabled = ...,
    placeholder = ...,
    max_values = ...,
    min_values = ...,
):
    """
    Creates a new user select.
    
    Parameters
    ----------
    custom_id : `None`, `str`, Optional
        Custom identifier to detect which component was used by the user.
    
    default_values : `None | iterable<ClientUserBase | EntitySelectDefaultValue | tuple>`, Optional (Keyword only)
        Entities presented in the select by default.
    
    enabled : `bool`, Optional (Keyword only)
        Whether the button is enabled.
    
    placeholder : `None`, `str`, Optional (Keyword only)
        Placeholder text of the select.
    
    max_values : `int`, Optional (Keyword only)
        The maximal amount of options to select.
        
    min_values : `int`, Optional (Keyword only)
        The minimal amount of options to select.
    
    Returns
    -------
    user_select : ``Component``
    
    Raises
    ------
    TypeError
        - If a parameter's type is incorrect.
    ValueError
        - If a parameter's value is incorrect.
    """
    return Component(
        ComponentType.user_select,
        custom_id = custom_id,
        default_values = default_values,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
    )


def create_role_select(
    custom_id = ...,
    *,
    default_values = ...,
    enabled = ...,
    placeholder = ...,
    max_values = ...,
    min_values = ...,
):
    """
    Creates a new role select.
    
    Parameters
    ----------
    custom_id : `None`, `str`, Optional
        Custom identifier to detect which component was used by the user.
    
    default_values : `None | iterable<Role | EntitySelectDefaultValue | tuple>`, Optional (Keyword only)
        Entities presented in the select by default.
    
    enabled : `bool`, Optional (Keyword only)
        Whether the button is enabled.
    
    placeholder : `None`, `str`, Optional (Keyword only)
        Placeholder text of the select.
    
    max_values : `int`, Optional (Keyword only)
        The maximal amount of options to select.
        
    min_values : `int`, Optional (Keyword only)
        The minimal amount of options to select.
    
    Returns
    -------
    role_select : ``Component``
    
    Raises
    ------
    TypeError
        - If a parameter's type is incorrect.
    ValueError
        - If a parameter's value is incorrect.
    """
    return Component(
        ComponentType.role_select,
        custom_id = custom_id,
        default_values = default_values,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
    )


def create_mentionable_select(
    custom_id = ...,
    *,
    default_values = ...,
    enabled = ...,
    placeholder = ...,
    max_values = ...,
    min_values = ...,
):
    """
    Creates a new mentionable (user & role) select.
    
    Parameters
    ----------
    custom_id : `None`, `str`, Optional
        Custom identifier to detect which component was used by the user.
    
    default_values : `None | iterable<ClientUserBase | Role | EntitySelectDefaultValue | tuple>` \
            , Optional (Keyword only)
        Entities presented in the select by default.
    
    enabled : `bool`, Optional (Keyword only)
        Whether the button is enabled.
    
    placeholder : `None`, `str`, Optional (Keyword only)
        Placeholder text of the select.
    
    max_values : `int`, Optional (Keyword only)
        The maximal amount of options to select.
        
    min_values : `int`, Optional (Keyword only)
        The minimal amount of options to select.
    
    Returns
    -------
    mentionable_select : ``Component``
    
    Raises
    ------
    TypeError
        - If a parameter's type is incorrect.
    ValueError
        - If a parameter's value is incorrect.
    """
    return Component(
        ComponentType.mentionable_select,
        custom_id = custom_id,
        default_values = default_values,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
    )


def create_channel_select(
    custom_id = ...,
    *,
    channel_types = ...,
    default_values = ...,
    enabled = ...,
    placeholder = ...,
    max_values = ...,
    min_values = ...,
):
    """
    Creates a new channel (user & role) select.
    
    Parameters
    ----------
    custom_id : `None`, `str`, Optional
        Custom identifier to detect which component was used by the user.
    
    channel_types : `None`, `tuple` of (``ChannelType``, `int`), Optional (Keyword only)
        The allowed channel types by the select.
    
    default_values : `None | iterable<ClientUserBase | Channel | EntitySelectDefaultValue | tuple>` \
            , Optional (Keyword only)
        Entities presented in the select by default.
    
    enabled : `bool`, Optional (Keyword only)
        Whether the button is enabled.
    
    placeholder : `None`, `str`, Optional (Keyword only)
        Placeholder text of the select.
    
    max_values : `int`, Optional (Keyword only)
        The maximal amount of options to select.
        
    min_values : `int`, Optional (Keyword only)
        The minimal amount of options to select.
    
    Returns
    -------
    channel_select : ``Component``
    
    Raises
    ------
    TypeError
        - If a parameter's type is incorrect.
    ValueError
        - If a parameter's value is incorrect.
    """
    return Component(
        ComponentType.channel_select,
        channel_types = channel_types,
        custom_id = custom_id,
        default_values = default_values,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
    )
