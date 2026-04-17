__all__ = ()

from ..place_holder import PlaceHolder

from .preinstance import Preinstance


def _get_direct_type_parent(meta_type, type_parents):
    """
    Gets the direct parent from the given parents.
    
    Parameters
    ----------
    meta_type : `type`
        The type that is being instantiated.
    
    type_parents : `tuple<type>`
        The type's parents.
    
    Returns
    -------
    type_parent : `None | type`
    """
    if type_parents:
        type_parent = type_parents[0]
        if not isinstance(type_parent, meta_type):
            type_parent = None
    else:
        type_parent = None
    
    return type_parent


def _pop_items_to_post_instantiate(type_attributes):
    """
    Pops the items from the type's attributes that should be instantiated after the type is created.
    
    Parameters
    ----------
    type_attributes : `dict<str, object>`
        The defined attributes of the type.
    
    Returns
    -------
    to_post_instantiate : `list<(str, Preinstance)>`
    """
    to_post_instantiate = []
    
    for attribute_name, attribute_value in type_attributes.items():
        if isinstance(attribute_value, Preinstance):
            to_post_instantiate.append((attribute_name, attribute_value))
    
    for item in to_post_instantiate:
        del type_attributes[item[0]]
    
    return to_post_instantiate



def _get_name_default(type_parent, name_default):
    """
    Gets the default name to use for post created instances.
    
    Parameters
    ----------
    type_parent : `None | type`
        Parent type.
    
    name_default : `str | ...`
        The passed name default.
    
    Returns
    -------
    name_default : `str`
    
    Raises
    ------
    TypeError
    """
    if (name_default is not ...):
        if (type(name_default) is not str):
            raise TypeError(f'`name_default` can be only `str`, got {type(name_default).__name__}')
    
    elif (type_parent is not None):
        name_default = type_parent.NAME_DEFAULT
    
    else:
        name_default = 'UNDEFINED'
    
    return name_default


def _identify_value_type(type_parent, base_type, value_type):
    """
    Identifies the value type.
    
    Parameters
    ----------
    type_parent : `None | type`
        Parent type.
    
    base_type : `bool`
        Whether the currently created type is a base type.
    
    value_type : `type | ...`
        The passed value type.
    
    Returns
    -------
    value_type : `type<NoneType | int | str>`
    
    Raises
    ------
    RuntimeError
    TypeError
    """
    if (
        (value_type is ...) and
        (not base_type) and
        (
            (type_parent is None) or
            (type_parent.VALUE_TYPE is type(None))
        )
    ):
        raise RuntimeError(
            '`value_type` must be given if `base_type = False` (so by default) '
            'and if non of its parents defined it.',
        )
    
    while True:
        if value_type is ...:
            if type_parent is None:
                value_type = type(None)
            else:
                value_type = type_parent.VALUE_TYPE
            break
        
        if value_type is int:
            break
        
        if value_type is str:
            break
        
        raise TypeError(
            f'`value_type` not supported. Can be `int` or `str`; got {value_type.__name__}.'
        )
    
    
    if (
        (value_type is not ...) and
        (type_parent is not None) and
        (type_parent.VALUE_TYPE is not type(None)) and
        (value_type is not type_parent.VALUE_TYPE)
    ):
        raise TypeError(
            f'`value_type` cannot diverge from parent\'s; '
            f'got value_type = {value_type.__name__}; type_parent.value_type = {type_parent.VALUE_TYPE.__name__}.'
        )
    
    return value_type


def _get_value_default(value_type):
    """
    Gets the default value of the given type.
    
    Parameters
    ----------
    value_type : `type<NoneType | int | str>`
        The value's type.
    
    Returns
    -------
    value_default : `None | int | str`
    """
    if value_type is type(None):
        value_default = None
    
    elif value_type is int:
        value_default = 0
    
    elif value_type is str:
        value_default = ''
    
    else:
        value_default = None
    
    return value_default


def _get_and_validate_slots(type_attributes):
    """
    Gets the slots from the type attributes and validates them.
    If missing inserts empty slots.
    
    Parameters
    ----------
    type_attributes : `dict<str, object>`
        The type attributes of the created type.
    
    Returns
    -------
    slots : `tuple<str>`
    
    Raises
    ------
    TypeError
    """
    try:
        slots = type_attributes['__slots__']
    except KeyError:
        slots = ()
        type_attributes['__slots__'] = slots
    else:
        if not isinstance(slots, tuple):
            raise TypeError(
                f'Slots can be `tuple<str>`; got {type(slots).__name__}; slots = {slots!r}.'
            )
        
        for element in slots:
            if type(element) is not str:
                raise TypeError(
                    f'Slots elements can be `str`; got {type(element).__name__}; slots = {slots!r}.'
                )
    
    return slots


def _set_slot_place_holders(type_attributes, type_parent, slots, name_default, value_default):
    """
    Sets slot placeholders to type attributes if required.
    
    Parameters
    ----------
    type_attributes : `dict<str, object>`
        The type attributes of the created type.
    
    type_parent : `None | type`
        Parent type.
    
    slots : `tuple<str>`
        The defined slots of the type.
    
    name_default : `str`
        The default name to use.
    
    value_default : `int | str`
        The default value to use.
    """
    if (type_parent is not None):
        return
    
    if 'name' not in slots:
        type_attributes['name'] = PlaceHolder(name_default)
    
    if 'value' not in slots:
        type_attributes['value'] = PlaceHolder(value_default)


def _inherit_hash_function(type_attributes, type_parent):
    """
    Inherits the parent's hash method of the parent type if required.
    
    Parameters
    ----------
    type_attributes : `dict<str, object>`
        The type attributes of the created type.
    
    type_parent : `None | type`
        Parent type.
    """
    if (type_parent is None) or ('__hash__' in type_attributes.keys()):
        return
    
    type_attributes['__hash__'] = type_parent.__hash__


class PreinstancedMeta(type):
    """
    Meta-type for preinstanced instances.
    """
    def __new__(
        cls,
        type_name,
        type_parents,
        type_attributes,
        *,
        base_type = False,
        name_default = ...,
        value_type = ...,
    ):
        """
        Creates a preinstanced type.
        
        Parameters
        ----------
        type_name : `str`
            The created type's name.
        
        type_parents : `tuple` of `type`
            The parents of the creates type.
        
        type_attributes : `dict<str, object>`
            The type attributes of the created type.
        
        base_type : `bool` = `False`, Optional (Keyword only)
            Whether a base type is being created.
        
        name_default : `str`, Optional (Keyword only)
            Default name to use for preinstanced objects.
        
        value_type : `int | str`, Optional (Keyword only)
            The instance's value's type.
        
        Returns
        -------
        type : `instance<cls>`
        """
        type_parent = _get_direct_type_parent(cls, type_parents)
        
        if (type_parent is not None) and (type_parent.INSTANCES is not NotImplemented):
            raise RuntimeError(
                f'Cannot inherit from a non-base {PreinstancedMeta.__name__} type.'
            )
        
        name_default = _get_name_default(type_parent, name_default)
        value_type = _identify_value_type(type_parent, base_type, value_type)
        value_default = _get_value_default(value_type)
        
        to_post_instantiate = _pop_items_to_post_instantiate(type_attributes)
        
        # add attributes
        type_attributes['INSTANCES'] = NotImplemented if base_type else {}
        type_attributes['VALUE_TYPE'] = type(None) if (value_type is ...) else value_type
        type_attributes['NAME_DEFAULT'] = name_default
        type_attributes['VALUE_DEFAULT'] = value_default
        
        slots = _get_and_validate_slots(type_attributes)
        _set_slot_place_holders(type_attributes, type_parent, slots, name_default, value_default)
        _inherit_hash_function(type_attributes, type_parent)
        
        type_ = type.__new__(cls, type_name, type_parents, type_attributes)
        
        # add instances
        for attribute_name, attribute_value in to_post_instantiate:
            setattr(
                type_,
                attribute_name,
                type_(
                    attribute_value.value,
                    attribute_value.name,
                    *attribute_value.positional_parameters,
                    **attribute_value.keyword_parameters,
                ),
            )
        
        return type_
    
    
    def __call__(cls, value = None, name = None, *positional_parameters, **keyword_parameters):
        """
        Creates a new preinstanced instance if allowed and stores it.
        
        Parameters
        ----------
        value : `None | .VALUE_TYPE` = `None`, Optional
            The value of the preinstanced object.
        
        name : `None | str` = `None`, Optional
            The object's name.
        
        *positional_parameters : Positional parameters
            Additional positional parameters to create the instance with.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters to create the instance with.
        
        Raises
        ------
        NotImplementedError
        TypeError
        """
        INSTANCES = cls.INSTANCES
        if INSTANCES is NotImplemented:
            raise NotImplementedError(
                f'Base types cannot be instantiated; type = {cls.__name__}.'
            )
        
        if value is None:
            value = cls.VALUE_DEFAULT
        
        try:
            return INSTANCES[value]
        except KeyError:
            pass
        
        new = cls.__new__(cls, value, name, *positional_parameters, **keyword_parameters)
        INSTANCES[value] = new
        return new
