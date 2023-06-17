__all__ = ()

from scarletio import include_with_callback, set_docs

from .utils import timestamp_to_datetime


def entity_id_parser_factory(field_key):
    """
    Returns a new entity id parser.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    
    Returns
    -------
    parser : `FunctionType`
    """
    def parser(data):
        """
        Parses out an entity id field from the given data.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Entity data.
        
        Returns
        -------
        entity_id : `int`
        """
        nonlocal field_key
            
        entity_id = data.get(field_key, None)
        if (entity_id is None):
            entity_id = 0
        else:
            entity_id = int(entity_id)
        
        return entity_id
    
    return parser


def entity_id_array_parser_factory(field_key):
    """
    Returns a new entity id array parser.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    
    Returns
    -------
    parser : `FunctionType`
    """
    def parser(data):
        """
        Parses out an entity id field from the given data.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Entity data.
        
        Returns
        -------
        entity_id_array : `None`, `tuple` of `int`
        """
        nonlocal field_key
                
        entity_id_array = data.get(field_key, None)
        if (entity_id_array is None) or (not entity_id_array):
            entity_id_array = None
        else:
            entity_id_array = tuple(sorted(int(entity_id) for entity_id in entity_id_array))
        
        return entity_id_array
    
    return parser


def preinstanced_parser_factory(
    field_key, preinstanced_type, default_value, *, include = None, include_default_attribute_name = None
):
    """
    Returns a new preinstanced object parser.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    
    preinstanced_type : ``PreinstancedBase``
        The preinstanced type to use.
    
    default_value : `instance<preinstanced_type>`, `object`
        The default value to use if the key is not present.
    
    include : `None`, `str` = `None`, Optional (Keyword only)
        The type's name to include `preinstanced_type` with.
        Should be used when `preinstanced_type` cannot be resolved initially.
    
    include_default_attribute_name : `None`, `str` = `None`, Optional (Keyword only)
        If `preinstanced_type` is included meaning `default_value` cannot be initially defined for this reason, with
        this parameter it is possible to define which attribute of `preinstanced_type` should be pulled.
    
    Returns
    -------
    parser : `FunctionType`
    """
    def parser(data):
        """
        Parses out a preinstanced field from the given data.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Entity data.
        
        Returns
        -------
        preinstanced : ``PreinstancedBase``
        """
        nonlocal field_key
        nonlocal default_value
        nonlocal preinstanced_type
        
        try:
            value = data[field_key]
        except KeyError:
            preinstanced = default_value
        else:
            preinstanced = preinstanced_type.get(value)
        
        return preinstanced
    
    if (include is not None):
        @include_with_callback(include)
        def include_object_type(value):
            nonlocal preinstanced_type
            nonlocal default_value
            nonlocal include_default_attribute_name
            
            preinstanced_type = value
            
            if (include_default_attribute_name is not None):
                default_value = getattr(preinstanced_type, include_default_attribute_name)
    
    return parser


def preinstanced_array_parser_factory(field_key, preinstanced_type, *, include = None):
    """
    Returns a new preinstanced array parser.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
        
    preinstanced_type : ``PreinstancedBase``
        The preinstanced type to use.

    include : `None`, `str` = `None`, Optional (Keyword only)
        The type's name to include `preinstanced_type` with.
        Should be used when `preinstanced_type` cannot be resolved initially.
    
    Returns
    -------
    parser : `FunctionType`
    """
    def parser(data):
        """
        Parses out a preinstanced field from the given data.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Entity data.
        
        Returns
        -------
        preinstanced_array : `None`, `tuple` of ``PreinstancedBase``
        """
        nonlocal field_key
        nonlocal preinstanced_type
        
        value_array = data.get(field_key, None)
        if (value_array is None) or (not value_array):
            preinstanced_array = None
        else:
            preinstanced_array = tuple(sorted(preinstanced_type.get(value) for value in value_array))
        
        return preinstanced_array
    
    
    if (include is not None):
        @include_with_callback(include)
        def include_object_type(value):
            nonlocal preinstanced_type
            preinstanced_type = value
    
    return parser


def bool_parser_factory(field_key, default_value):
    """
    Returns a `bool` parser.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    default_value : `bool`
        The default value to use if the key is not present.
    
    Returns
    -------
    parser : `FunctionType`
    """
    return _field_parser_factory(field_key, default_value)


def float_parser_factory(field_key, default_value):
    """
    Returns an `float` parser.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    default_value : `float`
        The default value to use if the key is not present.
    
    Returns
    -------
    parser : `FunctionType`
    """
    return _field_parser_factory(field_key, default_value)


def int_parser_factory(field_key, default_value):
    """
    Returns an `int` parser.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    default_value : `int`
        The default value to use if the key is not present.
    
    Returns
    -------
    parser : `FunctionType`
    """
    return _field_parser_factory(field_key, default_value)


def int_postprocess_parser_factory(field_key, default_value, postprocessor):
    """
    Returns an `int` parser. with a postprocessor function applied to it.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    default_value : `int`
        The default value to use if the key is not present.
    postprocessor : `callable`
        Postprocessor to call on the field.
    
    Returns
    -------
    parser : `FunctionType`
    """
    def parser(data):
        """
        Parses out an integer from the given payload.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Entity data.
        
        Returns
        -------
        field_value : `int`
        """
        nonlocal field_key
        nonlocal default_value
        nonlocal postprocessor
        
        value = data.get(field_key, None)
        if (value is None):
            value = default_value
        else:
            value = postprocessor(value)
        
        return value
    
    return parser


def flag_parser_factory(field_key, flag_type, *, default_value = ...):
    """
    Returns a `flag` parser.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    flag_type : `type`
        The type of the flag to return.
    default_value : `instance<flag_type>`, Optional (Keyword only)
        Default value to return if `None` is received.
    
    Returns
    -------
    parser : `FunctionType`
    """
    if default_value is ...:
        default_value = flag_type()
    
    def parser(data):
        """
        Parses out an flag from the given payload.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Entity data.
        
        Returns
        -------
        field_value : `instance<flag_type>`
        """
        nonlocal default_value
        nonlocal field_key
        nonlocal flag_type
        
        value = data.get(field_key, None)
        if (value is None):
            value = default_value
        else:
            value = flag_type(value)
        
        return value
    
    return parser


def nullable_flag_parser_factory(field_key, flag_type):
    """
    Returns a nullable `flag` parser.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    flag_type : `type`
        The type of the flag to return.
    
    Returns
    -------
    parser : `FunctionType`
    """
    def parser(data):
        """
        Parses out a nullable flag from the given payload.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Entity data.
        
        Returns
        -------
        field_value : `None`, `instance<flag_type>`
        """
        nonlocal field_key
        nonlocal flag_type
        
        value = data.get(field_key, None)
        if (value is not None):
            value = flag_type(value)
        
        return value
    
    return parser



def negated_bool_parser_factory(field_key, default_value):
    """
    Returns a negated `bool` parser.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    default_value : `bool`
        The default value to use if the key is not present.
    
    Returns
    -------
    parser : `FunctionType`
    """
    def parser(data):
        """
        Parses out a `bool` from the given payload as returns it as negated.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Entity data.
        
        Returns
        -------
        field_value : `bool`
        """
        nonlocal field_key
        nonlocal default_value
        
        value = data.get(field_key, None)
        if value is None:
            value = default_value
        else:
            value = not value
        
        return value
    
    return parser


def nullable_date_time_parser_factory(field_key):
    """
    Returns a new nullable date time parser.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    
    Returns
    -------
    parser : `FunctionType`
    """
    def parser(data):
        """
        Parses out a date time from the given payload.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Entity data.
        
        Returns
        -------
        field_value : `None`, `DateTime`
        """
        timestamp = data.get(field_key, None)
        if (timestamp is not None):
            return timestamp_to_datetime(timestamp)
    
    
    return parser


def force_string_parser_factory(field_key):
    """
    Returns a new forced string parser.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    
    Returns
    -------
    parser : `FunctionType`
    """
    def parser(data):
        """
        Parses out a string from the given payload.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Entity data.
        
        Returns
        -------
        field_value : `str`
        """
        nonlocal field_key
        
        field_value = data.get(field_key, None)
        if (field_value is None):
            field_value = ''
        
        return field_value
    
    return parser


def field_parser_factory(field_key):
    """
    Returns a field parser. This parser 1:1 returns the parsed value.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    
    Returns
    -------
    parser : `FunctionType`
    """
    def parser(data):
        """
        Parses out any value from the given payload.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Entity data.
        
        Returns
        -------
        field_value : `object`
        """
        nonlocal field_key
        
        field_value = data.get(field_key, None)
        if (field_value is not None) and isinstance(field_value, str) and (not field_value):
            field_value = None
        
        return field_value
    
    return parser


def _field_parser_factory(field_key, default_value):
    """
    Returns an `object` parser. If the parsed object is `None` returns the given `default_value`.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    default_value : `object`
        The default value to use if the key is not present.
    
    Returns
    -------
    parser : `FunctionType`
    """
    def parser(data):
        """
        Parses out a nullable field from the given payload.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Entity data.
        
        Returns
        -------
        field_value : `int`
        """
        nonlocal field_key
        nonlocal default_value
        
        value = data.get(field_key, None)
        if (value is None):
            value = default_value
        
        return value
    
    return parser



def nullable_string_parser_factory(field_key):
    """
    Returns a nullable string parser.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    
    Returns
    -------
    parser : `FunctionType`
    """
    def parser(data):
        """
        Parses out a string from the given payload.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Entity data.
        
        Returns
        -------
        field_value : `str`
        """
        nonlocal field_key
        
        field_value = data.get(field_key, None)
        if (field_value is not None) and (not field_value):
            field_value = None
        
        return field_value
    
    return parser


def nullable_sorted_array_parser_factory(field_key):
    """
    Returns a nullable sorted object array parser.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    
    Returns
    -------
    parser : `FunctionType`
    """
    def parser(data):
        """
        Parses out a nullable sorted object array from the given payload.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Entity data.
        
        Returns
        -------
        sorted_array : `None`, `tuple` of `object`
        """
        nonlocal field_key
        
        raw_object_array = data.get(field_key, None)
        if (raw_object_array is None) or (not raw_object_array):
            object_array = None
        else:
            object_array = tuple(sorted(raw_object_array))
        
        return object_array
    
    return parser


def nullable_entity_array_parser_factory(field_key, entity_type, *, include = None):
    """
    Returns a new nullable entity array parser.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    entity_type : `type` with `{from_data}`
        Entity's type.
    include : `None`, `str` = `None`, Optional (Keyword only)
        The name to include `entity_type` with. Should be used when `entity_type` cannot be resolved initially.
    
    Returns
    -------
    parser : `FunctionType`
    """
    def parser(data):
        """
        Parses out a nullable entity array from the given payload.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Entity data.
        
        Returns
        -------
        entity_array : `None`, `tuple` of `instance<entity_type>`
        """
        nonlocal field_key
        nonlocal entity_type
        
        entity_data_array = data.get(field_key, None)
        if (entity_data_array is None) or (not entity_data_array):
            entity_array = None
        else:
            entity_array = tuple(sorted(entity_type.from_data(entity_data) for entity_data in entity_data_array))
        
        return entity_array
    
    
    if (include is not None):
        @include_with_callback(include)
        def include_object_type(value):
            nonlocal entity_type
            entity_type = value
    
    return parser


def nullable_entity_parser_factory(field_key, entity_type):
    """
    Returns an nullable entity parser.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    entity_type : `type` with `{from_data}`
        Entity's type.
    
    Returns
    -------
    parser : `FunctionType`
    """
    return default_entity_parser_factory(field_key, entity_type, default = None)


def default_entity_parser_factory(field_key, entity_type, *, default = ..., default_factory = ...):
    """
    Returns an entity parser with default return value.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    
    entity_type : `type` with `{from_data}`
        Entity's type.
    
    default : `object`, Optional (Keyword only)
        Default value to return if the entity is missing from the payload.
        
        Mutually exclusive with `default_factory` and at least one of them is required.
    
    default_factory : `() -> object`, Optional (Keyword only)
        Default value factory to call when the entity is missing from the payload.
        
        Mutually exclusive with `default` and at least one of them is required.
    
    Returns
    -------
    parser : `(dict<str, object>) -> instance<entity_type> | default | return<default_factory>`
    """
    if default is ... and default_factory is ...:
        raise TypeError(
            f'Either `default` or `default_factory` are required.'
        )
    
    if default is not ... and default_factory is not ...:
        raise TypeError(
            f'`default` and `default_factory` are mutually exclusive. '
            f'Got default = {default!r}, default_factory = {default_factory!r}.'
        )
    
    
    if default is not ...:
        def parser(data):
            nonlocal default
            nonlocal field_key
            nonlocal entity_type
            
            entity_data = data.get(field_key, None)
            if entity_data is None:
                entity = default
            else:
                entity = entity_type.from_data(entity_data)
            
            return entity
    
    else:
        def parser(data):
            nonlocal default_factory
            nonlocal field_key
            nonlocal entity_type
            
            entity_data = data.get(field_key, None)
            if entity_data is None:
                entity = default_factory()
            else:
                entity = entity_type.from_data(entity_data)
            
            return entity
    
    
    set_docs(
        parser,
        """
        Parses out an entity from the given payload.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Entity data.
        
        Returns
        -------
        entity_array : `None`, `instance<entity_type>`
        """
    )
    
    return parser


def functional_parser_factory(field_key, function, *, include = None):
    """
    Returns a functional parser.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    
    function : `FunctionType`
        Function to call with the received field value.
    
    include : `None`, `str` = `None`, Optional (Keyword only)
        The function's name to include `function` with. Should be used when `function` cannot be resolved initially.
    
    Returns
    -------
    parser : `FunctionType`
    """
    def parser(data):
        """
        Parses out a field from the given `data`. IF anything is received calls the specified function on it.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Entity data.
        
        Returns
        -------
        field_value : `None`, `object`
        """
        nonlocal field_key
        nonlocal function
        
        return function(data[field_key])
    
    
    if (include is not None):
        @include_with_callback(include)
        def include_object_type(value):
            nonlocal function
            function = value
    
    
    return parser


def nullable_functional_parser_factory(field_key, function, *, include = None):
    """
    Returns a functional parser with default return value.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    
    function : `FunctionType`
        Function to call with the received field value.
    
    include : `None`, `str` = `None`, Optional (Keyword only)
        The function's name to include `function` with. Should be used when `function` cannot be resolved initially.
    
    Returns
    -------
    parser : `FunctionType`
    """
    def parser(data):
        """
        Parses out a field from the given `data`. If anything is received calls the specified function on it.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Entity data.
        
        Returns
        -------
        field_value : `None`, `object`
        """
        nonlocal field_key
        nonlocal function
        
        field_value = data.get(field_key, None)
        if (field_value is not None):
            field_value = function(field_value)
        
        return field_value
    
    
    if (include is not None):
        @include_with_callback(include)
        def include_object_type(value):
            nonlocal function
            function = value
    
    
    return parser


def nullable_functional_array_parser_factory(field_key, function, *, do_sort = False, include = None, sort_key = None):
    """
    Returns a functional array parser with default return value.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    
    function : `FunctionType`
        Function to call with the received field value.
    
    include : `None`, `str` = `None`, Optional (Keyword only)
        The function's name to include `function` with. Should be used when `function` cannot be resolved initially.
    
    do_sort : `bool`
        Whether the output should be sorted.
    
    sort_key : `FunctionType`
        Sort key used to sort the entity.
    
    Returns
    -------
    parser : `FunctionType`
    """
    if do_sort:
        def parser(data):
            nonlocal field_key
            nonlocal function
            nonlocal sort_key
            
            field_values = data.get(field_key, None)
            if (field_values is None) or (not field_values):
                value = None
            else:
                value = tuple(sorted((function(field_value) for field_value in field_values), key = sort_key))
            
            return value
    else:
        def parser(data):
            nonlocal field_key
            nonlocal function
            
            field_values = data.get(field_key, None)
            if (field_values is None) or (not field_values):
                value = None
            else:
                value = (*(function(field_value) for field_value in field_values),)
            
            return value
            
    set_docs(
        parser,
        """
        Parses out a field from the given `data`.
        If anything is received calls the specified function on each of its elements.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Entity data.
        
        Returns
        -------
        field_value : `None`, `tuple` of `object`
        """
    )
    
    if (include is not None):
        @include_with_callback(include)
        def include_object_type(value):
            nonlocal function
            function = value
    
    
    return parser


def nullable_object_array_parser_factory(field_key, object_type, *, include = None):
    """
    Returns a new nullable object array parser.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    
    object_type : `type` with `{from_data}`
        Object's type.
    
    include : `None`, `str` = `None`, Optional (Keyword only)
        The name to include `object_type` with. Should be used when `object_type` cannot be resolved initially.
    
    Returns
    -------
    parser : `FunctionType`
    """
    def parser(data):
        """
        Parses out a nullable object array from the given payload.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Entity data.
        
        Returns
        -------
        object_array : `None`, `tuple` of `instance<object_type>`
        """
        nonlocal field_key
        nonlocal object_type
        
        object_data_array = data.get(field_key, None)
        if (object_data_array is None) or (not object_data_array):
            object_array = None
        else:
            object_array = (*(object_type.from_data(object_data) for object_data in object_data_array),)
        
        return object_array
    
    
    if (include is not None):
        @include_with_callback(include)
        def include_object_type(value):
            nonlocal object_type
            object_type = value
    
    
    return parser
