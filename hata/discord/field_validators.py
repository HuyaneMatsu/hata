__all__ = ()

from datetime import datetime as DateTime

from scarletio import include_with_callback

from .bases import maybe_snowflake
from .preconverters import (
    preconvert_bool, preconvert_int_options, preconvert_preinstanced_type, preconvert_snowflake, preconvert_str
)
from .utils import is_url



def field_validator_factory(field_name):
    """
    Returns an any field validator. Allows base types.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(field_value):
        """
        Validates the given field.
        
        > This function is generated.
        
        Parameters
        ----------
        field_value : object
            The field value to validate.
        
        Returns
        -------
        field_value : `object`
        """
        nonlocal field_name
        
        if (field_value is not None):
            if isinstance(field_value, str):
                if not field_value:
                    field_value = None
            
            elif isinstance(field_value, (int, float)):
                pass
            
            else:
                raise TypeError(
                    f'`field_name` can be any basic type, like `None`, `str`, `int`, `float`, got '
                    f'{field_value.__class__.__name__}; {field_value!r}.'
                )
            
        return field_value
    
    return validator


def entity_id_validator_factory(field_name, entity_type = None, *, include = None):
    """
    Returns an entity id validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    
    entity_type : `None`, ``DiscordEntity`` = `None`, Optional
        The accepted entity's type.
    
    
    include : `None`, `str` = `None`, Optional (Keyword only)
        The object's name to include `entity_type` with. Should be used when `entity_type` cannot be resolved initially.
    
    Returns
    -------
    validator : `FunctionType`
    """
    if (entity_type is None) and (include is None):
        def validator(entity_id):
            """
            Validates the given entity identifier.
            
            > This function is generated.
            
            Parameters
            ----------
            entity_id : `int`
                The entity's identifier.
            
            Returns
            -------
            entity_id : `int`
                The entity's identifier.
            
            Raises
            ------
            TypeError
                - If `entity_id`'s type is incorrect.
            """
            return preconvert_snowflake(entity_id, field_name)
    
    else:
        def validator(entity_id):
            """
            Validates the given entity identifier.
            
            > This function is generated.
            
            Parameters
            ----------
            entity_id : `None`, `entity_type`, `int`
                The entity or it's identifier.
            
            Returns
            -------
            entity_id : `int`
                The entity's identifier.
            
            Raises
            ------
            TypeError
                - If `entity_id`'s type is incorrect.
            """
            nonlocal field_name
            nonlocal entity_type
            
            if entity_id is None:
                processed_entity_id = 0
            
            elif isinstance(entity_id, entity_type):
                processed_entity_id = entity_id.id
            
            else:
                processed_entity_id = maybe_snowflake(entity_id)
                if processed_entity_id is None:
                    raise TypeError(
                        f'`{field_name}` can be `int`, `{entity_type.__name__}`, `int`, got '
                        f'{entity_id.__class__.__name__}; {entity_id!r}.'
                    )
            
            return processed_entity_id
    
    
    if (include is not None):
        @include_with_callback(include)
        def include_entity_type(value):
            nonlocal entity_type
            entity_type = value
    
    
    return validator


def entity_id_array_validator_factory(field_name, entity_type, *, include = None):
    """
    Returns an entity id array validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    
    entity_type : `type` with `{id}`
        The accepted entity's type.
    
    include : `None`, `str` = `None`, Optional (Keyword only)
        The object's name to include `entity_type` with. Should be used when `entity_type` cannot be resolved initially.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(entity_id_array):
        """
        Validates the given entity identifier.
        
        > This function is generated.
        
        Parameters
        ----------
        entity_id_array : `None`, `iterable` of (`int`, `entity_type`) items
            the entity or it's identifier.
        
        Returns
        -------
        entity_id_array : `None`, `tuple` of `int`
            The entity's identifier.
        
        Raises
        ------
        TypeError
            - If `entity_id_array`'s type is incorrect.
            - If an element of `entity_id_array` has incorrect type.
        """
        nonlocal field_name
        nonlocal entity_type
        
        if entity_id_array is None:
            return None
        
        if (getattr(entity_id_array, '__iter__', None) is None):
            raise TypeError(
                f'`{field_name}` can be `None`, `iterable` of (`int`, `{entity_type.__name__}`), '
                f'got {entity_id_array.__class__.__name__}; {entity_id_array!r}.'
            )
        
        entity_id_array_processed = None
        
        for applied_tag_id in entity_id_array:
            if isinstance(applied_tag_id, entity_type):
                 applied_tag_id_processed = applied_tag_id.id
            
            else:
                applied_tag_id_processed = maybe_snowflake(applied_tag_id)
                if applied_tag_id_processed is None:
                    raise TypeError(
                        f'`{field_name}` can contain `int`, `{entity_type.__name__}` elements, got '
                        f'{applied_tag_id.__class__.__name__}; {applied_tag_id!r}; entity_id_array={entity_id_array!r}.'
                    )
            
            if entity_id_array_processed is None:
                entity_id_array_processed = set()
            
            entity_id_array_processed.add(applied_tag_id_processed)
        
        if entity_id_array_processed is None:
            return None
        
        return tuple(sorted(entity_id_array_processed))
    
    
    if (include is not None):
        @include_with_callback(include)
        def include_entity_type(value):
            nonlocal entity_type
            entity_type = value
    
    
    return validator


def preinstanced_validator_factory(field_name, preinstanced_type):
    """
    Returns a preinstanced validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    preinstanced_type : ``PreinstancedBase``
        The accepted preinstanced type.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(preinstanced):
        """
        Validates the given preinstanced object.
        
        > This function is generated.
        
        Parameters
        ----------
        preinstanced : ``PreinstancedBase``, `instance<PreinstancedBase.VALUE_TYPE>`
            The preinstanced object or it's value.
        
        Returns
        -------
        preinstanced : ``PreinstancedBase``
        
        Raises
        ------
        TypeError
            - If `preinstanced`'s type is incorrect.
        """
        nonlocal field_name
        nonlocal preinstanced_type
        
        return preconvert_preinstanced_type(preinstanced, field_name, preinstanced_type)
    
    return validator


def nullable_preinstanced_validator_factory(field_name, preinstanced_type, default):
    """
    Returns a nullable preinstanced validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    preinstanced_type : ``PreinstancedBase``
        The accepted preinstanced type.
    default : `instance<preinstanced_type>`
        The default value to use if `None` is given.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(preinstanced):
        """
        Validates the given preinstanced object.
        
        > This function is generated.
        
        Parameters
        ----------
        preinstanced : `None`, ``PreinstancedBase``, `instance<PreinstancedBase.VALUE_TYPE>`
            The preinstanced object or it's value.
        
        Returns
        -------
        preinstanced : ``PreinstancedBase``
        
        Raises
        ------
        TypeError
            - If `preinstanced`'s type is incorrect.
        """
        nonlocal default
        nonlocal field_name
        nonlocal preinstanced_type
        
        if preinstanced is None:
            return default
        
        return preconvert_preinstanced_type(preinstanced, field_name, preinstanced_type)
    
    return validator


def preinstanced_array_validator_factory(field_name, preinstanced_type):
    """
    Returns a new preinstanced array validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    preinstanced_type : ``PreinstancedBase``
        The accepted preinstanced type.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(preinstanced_array):
        """
        Validates the given preinstanced object.
        
        > This function is generated.
        
        Parameters
        ----------
        preinstanced_array : `None`, `iterable` of (``PreinstancedBase``, `instance<PreinstancedBase.VALUE_TYPE>`)
            The preinstanced objects or their value.
        
        Returns
        -------
        preinstanced_array : `None`, `tuple` of ``PreinstancedBase``
        
        Raises
        ------
        TypeError
            - If `preinstanced`'s type is incorrect.
        """
        nonlocal field_name
        nonlocal preinstanced_type
        
        if preinstanced_array is None:
            return None
        
        if isinstance(preinstanced_array, preinstanced_type):
            return (preinstanced_array, )
        
        if isinstance(preinstanced_array, preinstanced_type.VALUE_TYPE):
            return (preinstanced_type.get(preinstanced_array), )
        
        if getattr(preinstanced_array, '__iter__', None) is None:
            raise TypeError(
                f'{field_name} can be `None` or `iterable`, got '
                f'{preinstanced_array.__class__.__name__}; {preinstanced_array!r}.'
            )
        
        unique_elements = None
        
        for preinstanced in preinstanced_array:
            if isinstance(preinstanced, preinstanced_type):
                pass
            
            elif isinstance(preinstanced, preinstanced_type.VALUE_TYPE):
                preinstanced = preinstanced_type.get(preinstanced)
            
            else:
                raise TypeError(
                    f'`{field_name}` elements can be `{preinstanced_type.__name__}`, '
                    f'`{preinstanced_type.VALUE_TYPE.__name__}`, '
                    f'got {preinstanced.__class__.__name__}; {preinstanced!r}.'
                )
            
            if unique_elements is None:
                unique_elements = set()
            
            unique_elements.add(preinstanced)
        
        if unique_elements is None:
            return None
        
        return tuple(sorted(unique_elements))
    
    return validator


def int_conditional_validator_factory(field_name, default_value, condition_check, condition_message):
    """
    Returns a new `int` with condition validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    default_value : `int`
        The default to return.
    condition_check : `callable`
        The condition which needs to pass.
    condition_message : `str`
        Condition message to use when building the error message.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(integer):
        """
        Validates the given integer value.
        
        > This function is generated.
        
        Parameters
        ----------
        integer : `int`
            The integer to validate.
        
        Returns
        -------
        integer : `int`
        
        Raises
        ------
        TypeError
            - If `integer` is not `int`.
        ValueError
            - If `integer` is not any of the expected options.
        """
        nonlocal condition_check
        nonlocal default_value
        nonlocal condition_message
        nonlocal field_name
        
        if integer is None:
            integer = default_value
        
        else:
            if not isinstance(integer, int):
                raise TypeError(
                    f'`{field_name}` can be `int`, got {integer.__class__.__name__}; {integer!r}.'
                )
            
            if not condition_check(integer):
                raise ValueError(
                    f'`{field_name}` must be {condition_message}, got {integer!r}.'
                )
        
        return integer
    
    return validator


def flag_validator_factory(field_name, flag_type):
    """
    Returns a new `int` with condition validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    flag_type : `type`
        The flag type to use.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(flag):
        """
        Validates the given flag.
        
        > This function is generated.
        
        Parameters
        ----------
        integer : `None`, `int`, `instance<flag_type>`
            The flag to validate.
        
        Returns
        -------
        integer : `instance<flag_type>`
        
        Raises
        ------
        TypeError
            - If `flag` is not `int`.
        ValueError
            - If `flag` is not any of the expected options.
        """
        nonlocal field_name
        nonlocal flag_type
        
        if flag is None:
            flag = flag_type()
        
        elif isinstance(flag, flag_type):
            pass
        
        elif isinstance(flag, int):
            flag = flag_type(flag)
        
        else:
            raise TypeError(
                f'`{field_name}` can be `None`, `int`, `{flag_type.__name__}`, '
                f'got {flag.__class__.__name__}; {flag!r}.'
            )
    
        return flag
    
    return validator


def int_options_validator_factory(field_name, field_options):
    """
    Returns a `int` with options validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    field_options : `frozenset` of `int`
        The allowed values.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(integer):
        """
        Validates the given integer value.
        
        > This function is generated.
        
        Parameters
        ----------
        integer : `int`
            The integer to validate.
        
        Returns
        -------
        integer : `int`
        
        Raises
        ------
        TypeError
            - If `integer` is not `int`.
        ValueError
            - If `integer` is not any of the expected options.
        """
        nonlocal field_name
        nonlocal field_options
    
        return preconvert_int_options(integer, field_name, field_options)
    
    return validator


def bool_validator_factory(field_name):
    """
    Returns a new `bool` validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(boolean):
        """
        Validates the given boolean value.
        
        > This function is generated.
        
        Parameters
        ----------
        boolean : `bool`
            The boolean to validate.
        
        Returns
        -------
        boolean : `int`
        
        Raises
        ------
        TypeError
            - If `boolean` is not `bool`.
        """
        nonlocal field_name
    
        return preconvert_bool(boolean, field_name)
    
    return validator


def nullable_date_time_validator_factory(field_name):
    """
    Returns a new nullable `DateTime` validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(date_time):
        """
        Validates the given date time value.
        
        > This function is generated.
        
        Parameters
        ----------
        date_time : `None`, `DateTime`
            The date time to validate.
        
        Returns
        -------
        date_time : `None`, `DateTime`
        
        Raises
        ------
        TypeError
            - If `date_time` is not `None`, `DateTime`.
        """
        nonlocal field_name
        
        if (date_time is not None) and (not isinstance(date_time, DateTime)):
            raise TypeError(
                f'`{field_name} can be `None`, `{DateTime.__name__}`, '
                f'got {date_time.__class__.__name__}; {date_time!r}.'
            )
        
        return date_time
    
    return validator


def force_string_validator_factory(field_name, length_min, length_max):
    """
    Returns an enforced string validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    length_min : `int`
        The minimal allowed string length.
    length_max : `int`
        The maximal allowed string length.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(string):
        """
        Validates the given string.
        
        > This function is generated.
        
        Parameters
        ----------
        string : `None`, `str`
            The string to validate.
        
        Returns
        -------
        string : `str`
                
        Raises
        ------
        TypeError
            - If `string` is not `None`, `str`.
        ValueError
            - If `string`'s length is out of the expected range.
        """
        nonlocal field_name
        nonlocal length_min
        nonlocal length_max
        
        if (string is None):
            string = ''
        else:
            string = preconvert_str(string, field_name, length_min, length_max)
        
        return string
    
    return validator



def nullable_string_validator_factory(field_name, length_min, length_max):
    """
    Returns a nullable string validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    length_min : `int`
        The minimal allowed string length.
    length_max : `int`
        The maximal allowed string length.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(string):
        """
        Validates the given string.
        
        > This function is generated.
        
        Parameters
        ----------
        string : `None`, `str`
            The string to validate.
        
        Returns
        -------
        string : `None`, `str`
                
        Raises
        ------
        TypeError
            - If `string` is not `None`, `str`.
        ValueError
            - If `string`'s length is out of the expected range.
        """
        nonlocal field_name
        nonlocal length_min
        nonlocal length_max
        
        if (string is not None):
            string = preconvert_str(string, field_name, length_min, length_max)
            if (not string):
                string = None
        
        return string
    
    return validator


def nullable_string_array_validator_factory(field_name):
    """
    Returns a nullable string array validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(string_array):
        """
        Validates the given string array.
        
        > This function is generated.
        
        Parameters
        ----------
        string_array : `None`, `iterable` of `str`
            The string to validate.
        
        Returns
        -------
        string_array : `None`, `str`
                
        Raises
        ------
        TypeError
            - If `string_array` is not `None`, `iterable` of `str`.
        """
        nonlocal field_name
        
        if (string_array is None):
            return None
        
        if isinstance(string_array, str):
            return (string_array, )
        
        if getattr(string_array, '__iter__', None) is None:
            raise TypeError(
                f'`{field_name}` can be `None`, `iterable` of `str`, got '
                f'{string_array.__class__.__name__}; {string_array!r}.'
            )
        
        processed_values = None
        
        for string in string_array:
            if not isinstance(string, str):
                raise TypeError(
                    f'`{field_name}` elements can be `str`, got '
                    f'{string.__class__.__name__}; {string!r}; {field_name}={string_array!r}.'
                )
            
            if (processed_values is None):
                processed_values = []
            
            processed_values.append(string)
        
        if processed_values is not None:
            processed_values.sort()
            return tuple(processed_values)
    
    return validator


def url_optional_validator_factory(field_name):
    """
    Returns an optional url validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(url):
        """
        Validates the given string.
        
        > This function is generated.
        
        Parameters
        ----------
        url : `None`, `str`
            The url to validate.
        
        Returns
        -------
        string : `None`, `str`
                
        Raises
        ------
        TypeError
            - If `url` is not `None`, `str`.
        ValueError
            - If `url` is not an url.
        """
        nonlocal field_name
        
        if (url is not None):
            if not isinstance(url, str):
                raise TypeError(
                    f'`{field_name}` can be `None`, `str`, got {url.__class__.__name__}; {url!r}.'
                )
            
            if url:
                if not is_url(url):
                    raise ValueError(
                        f'`{field_name}` is not a valid url, got {url!r}.'
                    )
            
            else:
                url = None
        
        return url
    
    return validator


def url_required_validator_factory(field_name):
    """
    Returns a required url validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(url):
        """
        Validates the given string.
        
        > This function is generated.
        
        Parameters
        ----------
        url : `None`, `str`
            The url to validate.
        
        Returns
        -------
        string : `None`, `str`
                
        Raises
        ------
        TypeError
            - If `url` is not `None`, `str`.
        ValueError
            - If `url` is not an url.
        """
        nonlocal field_name
        
        if (url is not None) and not isinstance(url, str):
            if not isinstance(url, str):
                raise TypeError(
                    f'`{field_name}` can be `None`, `str`, got {url.__class__.__name__}; {url!r}.'
                )
        
        if (url is None) or (not url):
            if not isinstance(url, str):
                raise ValueError(
                    f'`{field_name}` cannot be empty, got {type(url).__name__}; {url!r}.'
                )
        
        if not is_url(url):
            raise ValueError(
                f'`{field_name}` is not a valid url, got {url!r}.'
            )
        
        return url
    
    return validator


def url_array_optional_validator_factory(field_name):
    """
    Returns an optional url array validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(url_array):
        """
        Validates the given string.
        
        > This function is generated.
        
        Parameters
        ----------
        url_array : `None`, `str`, `iterable` of `str`
            The url array to validate.
        
        Returns
        -------
        url_array : `None`, `str`
                
        Raises
        ------
        TypeError
            - If `url` is not `None`, `str`, `iterable` of `str`
        ValueError
            - If an `url` is not an url.
        """
        nonlocal field_name
        
        if (url_array is None):
            return None
        
        if isinstance(url_array, str):
            if not is_url(url_array):
                raise ValueError(
                    f'`{field_name}` is not a valid url, got {url_array!r}.'
                )
            
            return (url_array, )
        
        if getattr(url_array, '__iter__', None) is None:
            raise TypeError(
                f'`{field_name}` can be `None`, `iterable` of `str`, got '
                f'{url_array.__class__.__name__}; {url_array!r}.'
            )
        
        processed_values = None
        
        for url in url_array:
            if not isinstance(url, str):
                raise TypeError(
                    f'`{field_name}` elements can be `str`, got '
                    f'{url.__class__.__name__}; {url!r}; {field_name}={url_array!r}.'
                )
            
            if not is_url(url):
                raise ValueError(
                    f'`{field_name}` element is not a valid url, got {url!r}; {field_name}={url_array!r}.'
                )
            
            if (processed_values is None):
                processed_values = []
            
            processed_values.append(url)
        
        if processed_values is not None:
            processed_values.sort()
            return tuple(processed_values)
    
    return validator


def nullable_entity_array_validator_factory(field_name, entity_type):
    """
    Returns a nullable entity array validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    entity_type : `type`
        The allowed entity type.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(entity_array):
        """
        Validates the given nullable entity array field.
        
        Parameters
        ----------
        entity_array : `None`, `iterable` of `instance<entity_type>`
            The entity array to validate.
        
        Returns
        -------
        entity_array : `None`, `tuple` of `instance<entity_type>`
        
        Raises
        ------
        TypeError
            - If `entity_array` is not `None`, `iterable` of `entity_type`.
        """
        nonlocal field_name
        nonlocal entity_type
        
        if entity_array is None:
            return None
        
        if (getattr(entity_array, '__iter__', None) is None):
            raise TypeError(
                f'`{field_name}` can be `None`, `iterable` of `{entity_type.__name__}`, got '
                f'{entity_array.__class__.__name__}; {entity_array!r}.'
            )
            
        entity_array_processed = None
        
        for entity in entity_array:
            if not isinstance(entity, entity_type):
                raise TypeError(
                    f'`{field_name}` can contain `{entity_type.__name__}` elements, got '
                    f'{entity.__class__.__name__}; {entity!r}; entity_array = {entity_array!r}.'
                )
            
            if (entity_array_processed is None):
                entity_array_processed = set()
            
            entity_array_processed.add(entity)
        
        if (entity_array_processed is not None):
            entity_array_processed = tuple(sorted(entity_array_processed))
        
        return entity_array_processed
    
    return validator


def nullable_entity_validator_factory(field_name, entity_type):
    """
    Returns a nullable entity validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    entity_type : `type`
        The allowed entity type.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(entity):
        """
        Validates the given nullable entity field.
        
        Parameters
        ----------
        entity : `None`, `instance<entity_type>`
            The entity to validate.
        
        Returns
        -------
        entity : `None`,  `instance<entity_type>`
        
        Raises
        ------
        TypeError
            - If `entity` is not `None`, ``entity_type``.
        """
        nonlocal field_name
        nonlocal entity_type
        
        if (entity is not None) and (not isinstance(entity, entity_type)):
            raise TypeError(
                f'`{field_name}` can be `None`, `{entity_type.__name__}`, got {entity.__class__.__name__}; {entity!r}.'
            )
        
        return entity
    
    return validator


def nullable_entity_conditional_validator_factory(
    field_name, entity_type, condition_check, condition_message, *, include = None
):
    """
    Returns a nullable entity validator with a condition validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    
    entity_type : `type`
        The allowed entity type.
    
    condition_check : `callable`
        The condition which needs to pass.
    
    condition_message : `str`
        Condition message to use when building the error message.
    
    include : `None`, `str` = `None`, Optional (Keyword only)
        The name to include `entity_type` with. Should be used when `entity_type` cannot be resolved initially.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(entity):
        """
        Validates the given nullable entity field.
        
        Parameters
        ----------
        entity : `None`, `instance<entity_type>`
            The entity to validate.
        
        Returns
        -------
        entity : `None`,  `instance<entity_type>`
        
        Raises
        ------
        TypeError
            - If `entity` is not `None`, ``entity_type``.
        """
        nonlocal field_name
        nonlocal entity_type
        nonlocal condition_check
        nonlocal condition_message
        
        if (entity is not None):
            if (not isinstance(entity, entity_type)):
                raise TypeError(
                    f'`{field_name}` can be `None`, `{entity_type.__name__}`, got '
                    f'{entity.__class__.__name__}; {entity!r}.'
                )
            
            if not condition_check(entity):
                raise ValueError(
                    f'`{field_name}` must be {condition_message}, got {entity!r}.'
                )
            
        return entity
    
    
    if (include is not None):
        @include_with_callback(include)
        def include_object_type(value):
            nonlocal entity_type
            entity_type = value
    
    
    return validator


def default_entity_validator(field_name, entity_type, default_value):
    """
    Returns a defaulted entity validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    entity_type : `type`
        The allowed entity type.
    default_value : `object`
        The default value to return if `None` is received.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(entity):
        """
        Validates the given nullable entity field.
        
        Parameters
        ----------
        entity : `None`, `instance<entity_type>`
            The entity to validate.
        
        Returns
        -------
        entity : `None`,  `instance<entity_type>`
        
        Raises
        ------
        TypeError
            - If `entity` is not `None`, ``entity_type``.
        """
        nonlocal default_value
        nonlocal field_name
        nonlocal entity_type
        
        if (entity is None):
            entity = default_value
        
        elif isinstance(entity, entity_type):
            pass
        
        else:
            raise TypeError(
                f'`{field_name}` can be `None`, `{entity_type.__name__}`, got {entity.__class__.__name__}; {entity!r}.'
            )
        
        return entity
    
    return validator



def entity_validator_factory(field_name, entity_type):
    """
    Returns an entity validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    entity_type : `type`
        The allowed entity type.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(entity):
        """
        Validates the given nullable entity field.
        
        Parameters
        ----------
        entity : `None`, `instance<entity_type>`
            The entity to validate.
        
        Returns
        -------
        entity : `None`,  `instance<entity_type>`
        
        Raises
        ------
        TypeError
            - If `entity` is not `None`, ``entity_type``.
        """
        nonlocal field_name
        nonlocal entity_type
        
        if not isinstance(entity, entity_type):
            raise TypeError(
                f'`{field_name}` can be `None`, `{entity_type.__name__}`, got {entity.__class__.__name__}; {entity!r}.'
            )
        
        return entity
    
    return validator


def nullable_object_array_validator_factory(field_name, object_type, *, include = None):
    """
    Returns a nullable object array validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    
    object_type : `type`
        The allowed object type.
    
    include : `None`, `str` = `None`, Optional (Keyword only)
        The object's name to include `entity_type` with. Should be used when `entity_type` cannot be resolved initially.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(object_array):
        """
        Validates the given nullable object array field.
        
        Parameters
        ----------
        object_array : `None`, `iterable` of `instance<object_type>`
            The object array to validate.
        
        Returns
        -------
        object_array : `None`, `tuple` of `instance<object_type>`
        
        Raises
        ------
        TypeError
            - If `object_array` is not `None`, `iterable` of `object_type`.
        """
        nonlocal field_name
        nonlocal object_type
        
        if object_array is None:
            return None
        
        if (getattr(object_array, '__iter__', None) is None):
            raise TypeError(
                f'`{field_name}` can be `None`, `iterable` of `{object_type.__name__}`, got '
                f'{object_array.__class__.__name__}; {object_array!r}.'
            )
            
        object_array_processed = None
        
        for object in object_array:
            if not isinstance(object, object_type):
                raise TypeError(
                    f'`{field_name}` can contain `{object_type.__name__}` elements, got '
                    f'{object.__class__.__name__}; {object!r}; object_array = {object_array!r}.'
                )
            
            if (object_array_processed is None):
                object_array_processed = []
            
            object_array_processed.append(object)
        
        if (object_array_processed is not None):
            object_array_processed = tuple(object_array_processed)
        
        return object_array_processed
    
    
    if (include is not None):
        @include_with_callback(include)
        def include_object_type(value):
            nonlocal object_type
            object_type = value
    
    
    return validator


def nullable_entity_dictionary_validator_factory(field_name, entity_type):
    """
    Returns a nullable object array validator.
    
    Parameters
    ----------
    field_name : `str`
        The field's name.
    
    entity_type : `type<DiscordEntity>`
        The allowed entity type.
    
    Returns
    -------
    validator : `FunctionType`
    """
    def validator(field_value):
        """
        Validates the given nullable entity dictionary field.
        
        Parameters
        ----------
        field_value : `None`, `iterable` of `instance<entity_type>`, `dict` of (`int`, `entity_type`) items
            The field value to validate
        
        Returns
        -------
        entity_dictionary : `None`, `dict` of `instance<entity_type>`
        
        Raises
        ------
        TypeError
            - If `field_value`'s or it's elements type is incorrect.
        """
        nonlocal field_name
        nonlocal entity_type
        
        validated = None
        
        if field_value is not None:
            if isinstance(field_value, dict):
                iterator = iter(field_value.values())
            
            elif (getattr(field_value, '__iter__', None) is not None):
                iterator = iter(field_value)
            
            else:
                raise TypeError(
                    f'`{field_name}` can be `None`, `dict` of (`int`, `{entity_type.__name__}`) items, `iterable` of '
                    f'`{entity_type.__name__}` items, got {field_value.__class__.__name__}; {field_value!r}.'
                )
            
            for element in iterator:
                if not isinstance(element, entity_type):
                    raise TypeError(
                        f'`{field_name}` elements can be `{entity_type.__name__}`, got {element.__class__.__name__}; '
                        f'{element!r}; {field_name} = {field_value!r}.'
                    )
                
                if (validated is None):
                    validated = {}
                
                validated[element.id] = element
        
        return validated
    
    return validator
