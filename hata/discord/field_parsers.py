__all__ = ()

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
        data : `dict` of (`str`, `Any`) items
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
        data : `dict` of (`str`, `Any`) items
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


def preinstanced_parser_factory(field_key, preinstanced_type, default_value):
    """
    Returns a new preinstanced object parser.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    preinstanced_type : ``PreinstancedBase``
        The preinstanced type to use.
    default_value : `instance<preinstanced_type>`, `Any`
        The default value to use if the key is not present.
    
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
        data : `dict` of (`str`, `Any`) items
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
    
    return parser


def preinstanced_array_parser_factory(field_key, preinstanced_type):
    """
    Returns a new preinstanced array parser.
    
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    preinstanced_type : ``PreinstancedBase``
        The preinstanced type to use.
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
        data : `dict` of (`str`, `Any`) items
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
    
    return parser


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
    def parser(data):
        """
        Parses out an integer from the given payload.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
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
        data : `dict` of (`str`, `Any`) items
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


def flag_parser_factory(field_key, flag_type):
    """
    Returns a `flag` parser.
    
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
        Parses out an flag from the given payload.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Entity data.
        
        Returns
        -------
        field_value : `instance<flag_type>`
        """
        nonlocal field_key
        nonlocal flag_type
        
        value = data.get(field_key, None)
        if (value is None):
            value = flag_type()
        else:
            value = flag_type(value)
        
        return value
    
    return parser


def bool_parser_factory(field_key, default_value):
    """
    Returns a new `bool` parser.
    
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
        Parses out an integer from the given payload.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Entity data.
        
        Returns
        -------
        field_value : `bool`
        """
        nonlocal field_key
        nonlocal default_value
        
        return data.get(field_key, default_value)
    
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
        data : `dict` of (`str`, `Any`) items
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
        data : `dict` of (`str`, `Any`) items
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


def nullable_string_parser_factory(field_key):
    """
    Returns a new nullable string parser.
    
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
        data : `dict` of (`str`, `Any`) items
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


def nullable_entity_array_parser_factory(field_key, entity_type):
    """
    Returns a new nullable entity array parser.
    
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
    def parser(data):
        """
        Parses out a nullable entity array from the given payload.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
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
    
    return parser


def nullable_entity_parser_factory(field_key, entity_type):
    """
    Returns a new nullable entity parser.
    
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
    return default_entity_parser_factory(field_key, entity_type, None)


def default_entity_parser_factory(field_key, entity_type, default):
    """
    Returns a new entity parser with default return value.
    
    Parameters
    ----------
    field_key : `str`
        The field's key used in payload.
    entity_type : `type` with `{from_data}`
        Entity's type.
    default : `object`
        Default value to return if the entity is missing from the payload.
    
    Returns
    -------
    parser : `FunctionType`
    """
    def parser(data):
        """
        Parses out a nullable entity from the given payload.
        
        > This function is generated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Entity data.
        
        Returns
        -------
        entity_array : `None`, `instance<entity_type>`
        """
        nonlocal default
        nonlocal field_key
        nonlocal entity_type
        
        entity_data = data.get(field_key, None)
        if entity_data is None:
            entity = default
        else:
            entity = entity_type.from_data(entity_data)
        
        return entity
    
    return parser
