__all__ = ()

from scarletio import include

from ...emoji import Emoji

from .constants import (
    COMPONENT_CUSTOM_ID_LENGTH_MAX, COMPONENT_LABEL_LENGTH_MAX, COMPONENT_MAX_LENGTH_MAX, COMPONENT_MAX_LENGTH_MIN,
    COMPONENT_MIN_LENGTH_MAX, COMPONENT_MIN_LENGTH_MIN, COMPONENT_OPTION_LENGTH_MAX, COMPONENT_OPTION_LENGTH_MIN,
    COMPONENT_OPTION_MAX_VALUES_MAX, COMPONENT_OPTION_MAX_VALUES_MIN, COMPONENT_OPTION_MIN_VALUES_MAX,
    COMPONENT_OPTION_MIN_VALUES_MIN, COMPONENT_SUB_COMPONENT_LIMIT, COMPONENT_TITLE_LENGTH_MAX,
    COMPONENT_TITLE_LENGTH_MIN
)
from .preinstanced import ComponentType


ComponentSelectOption = include('ComponentSelectOption')
ComponentBase = include('ComponentBase')

COMPONENT_TYPE_ROW = ComponentType.row


def _debug_component_components(components):
    """
    Checks whether given `component.components` value is correct.
    
    Parameters
    ----------
    components : `None` or (`list`, `tuple`) of ``ComponentBase``
        Sub-components.
    
    Raises
    ------
    AssertionError
        - If `components`'s length is out of the expected range [0:5].
        - If `components` is neither `None`, `tuple`, `list`.
        - If `components` contains a non ``ComponentBase``.
    """
    if (components is None):
        pass
    elif isinstance(components, (tuple, list)):
        if (len(components) > COMPONENT_SUB_COMPONENT_LIMIT):
            raise AssertionError(
                f'`component.components` can have maximum 5 sub-components, got '
                f'{len(components)}; {components!r}.'
            )
        
        for component in components:
            if not isinstance(component, ComponentBase):
                raise AssertionError(
                    f'`component` can be `{ComponentBase.__name__}`, got '
                    f'{component.__class__.__name__}.'
                )
            
            if component.type is COMPONENT_TYPE_ROW:
                raise AssertionError(
                    f'Cannot add `{COMPONENT_TYPE_ROW}` type as sub components, got '
                    f'{component!r}.'
                )
    else:
        raise AssertionError(
            f'`components` can be `None`, `tuple`, `list`, got '
            f'{components.__class__.__name__}; {components!r}.'
        )


def _debug_component_custom_id(custom_id):
    """
    Checks whether given `component.custom_id` value is correct.
    
    Parameters
    ----------
    custom_id : `None`, `str`
        Custom identifier to detect which button was clicked by the user.
    
    Raises
    ------
    AssertionError
        - If `custom_id` was not given neither as `None`, `str`.
        - If `custom_id`'s length is over `100`.
    """
    if (custom_id is None):
        pass
    elif isinstance(custom_id, str):
        custom_id_length = len(custom_id)
        if custom_id_length == 0:
            raise AssertionError(
                f'`custom_id` is not nullable.'
            )
        
        if custom_id_length > COMPONENT_CUSTOM_ID_LENGTH_MAX:
            raise AssertionError(
                f'`custom_id`\'s max length is {COMPONENT_CUSTOM_ID_LENGTH_MAX!r}, got '
                f'{len(custom_id)!r}; {custom_id!r}.'
            )
    else:
        raise AssertionError(
            f'`custom_id` can be `None`, `str`, got {custom_id.__class__.__name__}; {custom_id!r}.'
        )


def _debug_component_emoji(emoji):
    """
    Checks whether the given `component.emoji` value is correct.
    
    Parameters
    ----------
    emoji : `None`, ``Emoji``
        Emoji of the button if applicable.
    
    Raises
    ------
    AssertionError
        If `emoji` was not given as ``Emoji``.
    """
    if emoji is None:
        pass
    elif isinstance(emoji, Emoji):
        pass
    else:
        raise AssertionError(f'`emoji` can be `{Emoji.__name__}`, got '
            f'{emoji.__class__.__name__}')


def _debug_component_label(label):
    """
    Checks whether the given `component.label` value is correct.
    
    Parameters
    ----------
    label : `None`, `str`
        Label of the component.
    
    Raises
    ------
    AssertionError
        - If `label` was not given neither as `None` nor as `int`.
        - If `label`'s length is over `80`.
    """
    if label is None:
        pass
    elif isinstance(label, str):
        if len(label) > COMPONENT_LABEL_LENGTH_MAX:
            raise AssertionError(
                f'`label`\'s max length can be {COMPONENT_LABEL_LENGTH_MAX!r}, got '
                f'{len(label)!r}; {label!r}.'
            )
    else:
        raise AssertionError(
            f'`label` can be `None`, `str`, got {label.__class__.__name__}; {label!r}.'
        )

    
def _debug_component_title(title):
    """
    Checks whether the given `component.title` value is correct.
    
    Parameters
    ----------
    title : `None`, `str`
        Title of the component.
    
    Raises
    ------
    AssertionError
        - If `title` was not given neither as `None` nor as `int`.
        - If `title`'s length is out of the expected range.
    """
    if title is None:
        raise AssertionError(
            f'`title`\'s is not nullable.'
        )
        
    elif isinstance(title, str):
        title_length = len(title)
        
        if title_length < COMPONENT_TITLE_LENGTH_MIN:
            raise AssertionError(
                f'`title`\'s minimal length is {COMPONENT_TITLE_LENGTH_MIN!r}, got {title_length!r}; {title!r}.'
            )
        
        if title_length > COMPONENT_TITLE_LENGTH_MAX:
            raise AssertionError(
                f'`title`\'s maximal length is {COMPONENT_TITLE_LENGTH_MAX!r}, got {title_length!r}; {title!r}.'
            )
    
    else:
        raise AssertionError(
            f'`title` can be `None`, `str`, got {title.__class__.__name__}; {title!r}.'
        )


def _debug_component_enabled(enabled):
    """
    Checks whether the given `component.enabled` value is correct.
    
    Parameters
    ----------
    enabled : `bool`
        Whether the button is enabled.
    
    Raises
    ------
    AssertionError
        If `enabled` was not given as `bool`.
    """
    if not isinstance(enabled, bool):
        raise AssertionError(
            f'`enabled` can be `bool`, got {enabled.__class__.__name__}; {enabled!r}.'
        )


def _debug_component_url(url):
    """
    Checks whether the given `component.url` value is correct.
    
    Parameters
    ----------
    url : `None`, `str`
        Url to redirect to when clicking on a button.
    
    Raises
    ------
    AssertionError
        If `url` was not given neither as `None`, `str`.
    """
    if url is None:
        pass
    elif isinstance(url, str):
        pass
    else:
        raise AssertionError(
            f'`url` can be `None`, `str`, got {url.__class__.__name__}; {url!r}.'
        )


def _debug_component_select_option_value(value):
    """
    Checks whether the given `component_option.value` value is correct.
    
    Parameters
    ----------
    value : `str`
        A component option's value.
    
    Raises
    ------
    AssertionError
        If `value` was not given as `str`.
    """
    if not isinstance(value, str):
        raise AssertionError(
            f'`value` can be `str`, got {value.__class__.__name__}; {value!r}.'
        )


def _debug_component_initial_value(value):
    """
    Checks whether the given `component_option.value` value is correct.
    
    Parameters
    ----------
    value : `str`
        A component option's value.
    
    Raises
    ------
    AssertionError
        If `value` was not given as `str`.
    """
    if not isinstance(value, str):
        raise AssertionError(
            f'`value` can be `str`, got {value.__class__.__name__}; {value!r}.'
        )


def _debug_component_description(description):
    """
    Checks whether the given `component_option.description` value is correct.
    
    Parameters
    ----------
    description : `None`, `str`
        A component option's description.
    
    Raises
    ------
    AssertionError
        If `description` was not given neither as `None`, `str`.
    """
    if description is None:
        pass
    elif isinstance(description, str):
        pass
    else:
        raise AssertionError(
            f'`description` can be `None`, `str`, got {description.__class__.__name__}; {description!r}.'
        )


def _debug_component_default(default):
    """
    Checks whether the given `component_option.default` value is correct.
    
    Parameters
    ----------
    default : `bool`
        Whether this component option is the default one.
    
    Raises
    ------
    AssertionError
        If `default` was not given as `bool`.
    """
    if not isinstance(default, bool):
        raise AssertionError(
            f'`default` can be `bool`, got {default.__class__.__name__}; {default!r}.'
        )


def _debug_component_options(options):
    """
    Checks whether given `component.options` value is correct.
    
    Parameters
    ----------
    options : `None` or (`list`, `tuple`) of ``ComponentSelectOption``
        Sub-options.
    
    Raises
    ------
    AssertionError
        - If `options` is neither `None`, `tuple`, `list`.
        - If `options` contains a non ``ComponentSelectOption``.
        - If `options`'s length is out of the expected [1:25] range.
    """
    if options is None:
        option_length = 0
    elif isinstance(options, (tuple, list)):
        for option in options:
            if not isinstance(option, ComponentSelectOption):
                raise AssertionError(
                    f'`option` can be `{ComponentSelectOption.__name__}`, got '
                    f'{option.__class__.__name__}, {option!r}.'
                )
        
        option_length = len(options)
    else:
        raise AssertionError(
            f'`options` can be `None`, `tuple`, `list`, got {options.__class__.__name__}; {options!r}.'
        )
    
    if (option_length < COMPONENT_OPTION_LENGTH_MIN) or (option_length > COMPONENT_OPTION_LENGTH_MAX):
        raise AssertionError(
            f'`options`\'s length can be in range '
            f'[{COMPONENT_OPTION_LENGTH_MIN}:{COMPONENT_OPTION_LENGTH_MAX}], got {option_length}; {options!r}.'
        )


def _debug_component_placeholder(placeholder):
    """
    Checks whether the given `component_option.placeholder` value is correct.
    
    Parameters
    ----------
    placeholder : `None`, `str`
        The placeholder text of a component select.
    
    Raises
    ------
    AssertionError
        - If `placeholder` is neither `None` nor `str`.
    """
    if placeholder is None:
        pass
    elif isinstance(placeholder, str):
        pass
    else:
        raise AssertionError(
            f'`placeholder` can be `None`, `str`, got {placeholder.__class__.__name__}; {placeholder!r}.'
        )


def _debug_component_min_values(min_values):
    """
    Checks whether the given `component_option.min_values` value is correct.
    
    Parameters
    ----------
    min_values : `int`
        The min values of a component select.
    
    Raises
    ------
    AssertionError
        - If `min_values` was not given as `int`.
        - If `min_values`'s is out of range [0:15].
    """
    if not isinstance(min_values, int):
        raise AssertionError(
            f'`min_values` can be `int`, got {min_values.__class__.__name__}; {min_values!r}.'
        )
    
    if (min_values < COMPONENT_OPTION_MIN_VALUES_MIN) or (min_values > COMPONENT_OPTION_MIN_VALUES_MAX):
        raise AssertionError(
            f'`min_values` can be in range '
            f'[{COMPONENT_OPTION_MIN_VALUES_MIN}:{COMPONENT_OPTION_MAX_VALUES_MIN}], got {min_values!r}.'
        )


def _debug_component_max_values(max_values):
    """
    Checks whether the given `component_option.max_values` value is correct.
    
    Parameters
    ----------
    max_values : `int`
        The max values of a component select.
    
    Raises
    ------
    AssertionError
        - If `max_values` was not given as `int`.
        - If `max_values`'s is out of range [1:25].
    """
    if not isinstance(max_values, int):
        raise AssertionError(
            f'`max_values` can be `int`, got {max_values.__class__.__name__}; {max_values!r}.'
        )

    if (max_values < COMPONENT_OPTION_MAX_VALUES_MIN) or (max_values > COMPONENT_OPTION_MAX_VALUES_MAX):
        raise AssertionError(
            f'`max_values` can be in range '
            f'[{COMPONENT_OPTION_MAX_VALUES_MIN}:{COMPONENT_OPTION_MAX_VALUES_MAX}], got {max_values!r}.'
        )


def _debug_component_max_length(max_length):
    """
    Checks whether the given `component_text_input.max_length` value is correct.
    
    Parameters
    ----------
    max_length : `int`
        The max values of a component select.
    
    Raises
    ------
    AssertionError
        - If `max_length` was not given as `int`.
        - If `man_length`'s is out of the expected range.
    """
    if not isinstance(max_length, int):
        raise AssertionError(
            f'`max_length` can be `int`, got {max_length.__class__.__name__}; {max_length!r}.'
        )

    if (max_length < COMPONENT_MAX_LENGTH_MIN) or (max_length > COMPONENT_MAX_LENGTH_MAX):
        raise AssertionError(
            f'`max_length` can be in range '
            f'[{COMPONENT_MAX_LENGTH_MIN}:{COMPONENT_MAX_LENGTH_MAX}], got {max_length!r}.'
        )


def _debug_component_min_length(min_length):
    """
    Checks whether the given `component_text_input.min_length` value is correct.
    
    Parameters
    ----------
    min_length : `int`
        The max values of a component select.
    
    Raises
    ------
    AssertionError
        - If `min_length` was not given as `int`.
        - If `min_length`'s is out of the expected range.
    """
    if not isinstance(min_length, int):
        raise AssertionError(
            f'`min_length` can be `int`, got {min_length.__class__.__name__}; {min_length!r}.'
        )

    if (min_length < COMPONENT_MIN_LENGTH_MIN) or (min_length > COMPONENT_MIN_LENGTH_MAX):
        raise AssertionError(
            f'`min_length` can be in range '
            f'[{COMPONENT_MIN_LENGTH_MIN}:{COMPONENT_MIN_LENGTH_MAX}], got {min_length!r}.'
        )


def _debug_component_required(required):
    """
    Checks whether the given `component_text_input.required` value is correct.
    
    Parameters
    ----------
    required : `bool`
        Whether this component text input is required.
    
    Raises
    ------
    AssertionError
        If `required` was not given neither as `None`, `bool`.
    """
    if (required is not None) and (not isinstance(required, bool)):
        raise AssertionError(
            f'`required` can be `None`, `bool`, got {required.__class__.__name__}; {required!r}.'
        )


def _debug_component_text_input_value(value):
    """
    Checks whether the given `component_text_input.value` value is correct.
    
    Parameters
    ----------
    value : `None`, `str`
        The default value of the text input.
    
    Raises
    ------
    AssertionError
        If `value` was not given neither as `None`, `str`.
    """
    if (value is not None) and (not isinstance(value, str)):
        raise AssertionError(
            f'`value` can be `None`, `str`, got {value.__class__.__name__}; {value!r}.'
        )

