# -*- coding: utf-8 -*-
__all__ = ('BaseMethodDescriptor', 'KeepType', 'KeyedReferer', 'RemovedDescriptor', 'WeakCallable', 'WeakKeyDictionary',
    'WeakMap', 'WeakReferer', 'WeakValueDictionary', 'alchemy_incendiary', 'any_to_any', 'cached_property',
    'imultidict', 'istr', 'is_weakreferable', 'list_difference', 'methodize', 'module_property', 'modulize', 'multidict',
    'name_property', 'weakmethod', )

from types import \
    MethodType              as method, \
    FunctionType            as function, \
    MappingProxyType        as mapping_proxy, \
    GetSetDescriptorType    as getset_descriptor, \
    ModuleType              as module

NoneType = type(None)

import sys

try:
    from _weakref import ref as WeakrefType
except ImportError:
    from weakref import ref as WeakrefType

class RemovedDescriptor(object):
    """
    A descriptor, what can be used to overwrite a class's attribute, what should be inherited anyways.
    
    Attributes
    ----------
    name : `str` or `None`
        The name of the attribute. Set when the class is finalizing.
    """
    __slots__ = ('name',)
    def __init__(self,):
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, type_):
        name = self.name
        if name is None:
            raise RuntimeError(f'{self.__class__.__name__} is not initialized correctly yet.')
        
        if obj is None:
            error_message = f'type object {type_.__name__!r} has no attribute {name!r}'
        else:
            error_message = f'{obj.__class__.__name__!r} object has no attribute {name!r}'
        
        raise AttributeError(error_message)
    
    def __set__(self, obj, value):
        name = self.name
        if name is None:
            raise RuntimeError(f'{self.__class__.__name__} is not initialized correctly yet.')
        
        raise AttributeError(name)
    
    def __delete__(self, obj):
        name = self.name
        if name is None:
            raise RuntimeError(f'{self.__class__.__name__} is not initialized correctly yet.')
        
        raise AttributeError(name)

DOCS_ENABLED = (RemovedDescriptor.__doc__ is not None)


class doc_property(object):
    """
    Property to return the class's docs if called from class, else the given object.
    """
    __slots__ = ()
    def __init__(self):
        """
        Creates a new docs property.
        """
    
    def __get__(self, obj, type_):
        if obj is None:
            return type_.__class_doc__
        else:
            return obj.__instance_doc__
    
    def __set__(self, obj, value):
        raise AttributeError('can\'t set attribute')
    
    def __delete__(self, obj):
        raise AttributeError('can\'t delete attribute')


class name_property(object):
    """
    Property to return the class's name if called from the respective class.
    
    Attributes
    ----------
    class_name : `str`
        The class's name.
    fget : `callable`
        Callable what's return will be returned, when called from an instance.
    """
    __slots__ = ('class_name', 'fget')
    def __init__(self, name, fget):
        """
        Creates a new docs property.
        """
        self.class_name = name
        self.fget = fget
    
    def __get__(self, obj, type_):
        if obj is None:
            return type_.class_name
        else:
            return self.fget(obj)
    
    def __set__(self, obj, value):
        raise AttributeError('can\'t set attribute')
    
    def __delete__(self, obj):
        raise AttributeError('can\'t delete attribute')


def any_to_any(container1, container2):
    """
    Returns whether any value of `container1` is in `container2` as well.
    
    Parameters
    ----------
    container1 : `iterable-container`
        Any iterable container.
    container2 : `iterable-container`
        Any iterable container.

    Returns
    -------
    contains : `bool`
    """
    for value in container1:
        if value in container2:
            return True
    
    return False

def where(container, key):
    """
    Returns the first element from the given container on what `key` returns `True`.
    
    Parameters
    ----------
    container : `iterable-container`
        Any iterable container.
    key : `function`
        Function used to determine whether an element of `container` meets our expectations.
    
    Returns
    -------
    value : `Any`
        An element of `container`.
    
    Raises
    ------
    LookupError
        On non of the elements was `true` returned by they `key.
    """
    for value in container:
        if key(value):
            break
    else:
        raise LookupError(key)
    
    return value

def relative_index(list_, value):
    """
    Returns on which the given `value` would be inserted into the given list.
    
    Parameters
    ----------
    list_ : `list` of `Any`
        The list o which value would be inserted.
    value : `Any`
        The value what would be inserted.
    
    Returns
    -------
    relative_index : `int`
    """
    bot = 0
    top = len(list_)
    
    while True:
        if bot < top:
            half = (bot+top)>>1
            if list_[half] < value:
                bot = half+1
            else:
                top = half
            continue
        return bot

def change_on_switch(list_, value, new_position, key=None):
    """
    Calculates the changes if the given `value` would be moved to an another position.
    
    Parameters
    ----------
    list_ : `list` of `Any`
        The list on what the changes will be calculated.
    value : `Any`
        The object, what would be moved.
    new_position : `int`
        The new position of the value.
    key : `None` or `callable`
        A special callable what would be used to used to build each element of the result.
    
    Returns
    -------
    result : `list` of (`tuple` (`int`, `Any`)) or `callable` returns
        The changed positions.
    
    Raises
    ------
    ValueError
        The given `value` is not in the list.
    """
    ln = len(list_)
    
    old_position = relative_index(list_, value)
    if (old_position == ln) or (list_[old_position] != value):
        raise ValueError(f'{value!r} is not in the {list_.__class__.__name__}.')
    
    if new_position >= ln:
        new_position = ln-1
    elif new_position < 0:
        new_position = 0
    
    result = []
    if new_position == old_position:
        return result
    
    if new_position < old_position:
        index = new_position
        limit = old_position
        change = +1
    
    else:
        index = old_position+1
        limit = new_position+1
        change = -1
    
    while True:
        actual = list_[index]
        index += 1
        
        position = index+change
        if key is None:
            element = (actual, position)
        else:
            element = key(actual, position)
        
        result.append(element)
        
        if index == limit:
            break
        
        continue
    
    if key is None:
        element = (value, new_position)
    else:
        element = key(value, new_position)
    
    if change > 0:
        result.index(0, element)
    else:
        result.append(element)
    
    return result


class KeepType(object):
    """
    A decorator, what can be used to add features to an already existing class, by defining a new one, what will extend
    the old one's functionality.
    
    Note, that already existing attributes will not be overwritten and neither of the followingly named attributes
    either:
        - `__name__`
        - `__qualname__`
        - `__weakref__`
        - `__dict__`
        - `__slots__`
    
    Attributes
    ----------
    old_class : `type` instance
        The old class to extend.
    
    Class Attributes
    ----------------
    _ignored_attr_names : `set` of `str`
        Attribute names to ignore when extending.
    """
    __slots__ = ('old_class',)
    _ignored_attr_names = {'__name__', '__qualname__', '__weakref__', '__dict__', '__slots__', '__module__'}
    
    def __new__(cls, old_class, *, new_class=None):
        """
        Creates a new ``KeepType`` instance with given `old_class` to extend. Can be used as a decorator if `new_class`
        parameter is not given.
        
        Parameters
        ----------
        old_class : `type` instance
            The old class to extend.
        new_class : `None` or `type` instance, Optional
            The new class to extend the old class's functionality with.
        
        Returns
        -------
        obj : ``KeepType`` or `type` instance
            If only `old_class` attribute is given, then returns itself enabling using it as a decorator, but if
            `new_class` is given as well, then returns the extended `old_class`.
        """
        self = object.__new__(cls)
        self.old_class = old_class
        
        if new_class is None:
            return self
        
        return self(new_class)
    
    def __call__(self, new_class):
        """
        Calls the ``KeepType`` extending it's old ``.old_class`` with the new given `new_class`.
        
        Parameters
        ----------
        new_class : `type` instance
            The new class to extend the old class's functionality with.
        
        Returns
        -------
        old_class : `type` instance
            The extended old class.
        """
        old_class = self.old_class
        ignored_attr_names = self._ignored_attr_names
        for name in dir(new_class):
            if name in ignored_attr_names:
                continue
            
            attr = getattr(new_class, name)
            if hasattr(object, name) and (attr is getattr(object, name)):
                continue
            
            setattr(old_class, name, attr)
        
        return old_class

_spaceholder = object()


class _multidict_items(object):
    """
    ``multidict`` item iterator.
    
    Attributes
    ----------
    _parent : ``multidict``
        The parent multidict.
    """
    __slots__ = ('_parent',)
    def __init__(self, parent):
        """
        Creates a new ``multidict`` item iterator.
        
        Parameters
        ----------
        parent : ``multidict``
            The parent multidict.
        """
        self._parent = parent
    
    def __len__(self):
        """Returns the respective ``multidict``'s length."""
        return len(self._parent)
    
    def __iter__(self):
        """
        Iterates over the respective ``multidict``'s items.
        
        This method is a generator.
        
        Yields
        -------
        item : `tuple` (`Any`, `Any`)
            Items of the respective multidict as `key` - `value` pairs.
        """
        for key, values in dict.items(self._parent):
            for value in values:
                yield key, value
    
    def __contains__(self, item):
        """Returns whether the respective multidict contains the given item."""
        key, value = item
        parent = self._parent
        try:
            values = parent[key]
        except KeyError:
            return False
        return value in values


class _multidict_values(object):
    """
    ``multidict`` value iterator.
    
    Attributes
    ----------
    _parent : ``multidict``
        The parent multidict.
    """
    __slots__ = ('_parent',)
    def __init__(self, parent):
        """
        Creates a new ``multidict`` value iterator.
        
        Parameters
        ----------
        parent : ``multidict``
            The parent multidict.
        """
        self._parent = parent
    
    def __len__(self):
        """Returns the respective ``multidict``'s length."""
        return len(self._parent)
    
    def __iter__(self):
        """
        Iterates over the respective ``multidict``'s values.
        
        This method is a generator.
        
        Yields
        -------
        value : `Any`
            Values of the respective multidict.
        """
        for values in dict.values(self._parent):
            yield from values
    
    def __contains__(self, value):
        """Returns whether the respective multidict contains the given value."""
        for values in dict.values(self._parent):
            if value in values:
                return True
        return False
    
class multidict(dict):
    """
    Dictionary subclass, which can hold multiple values bound to a single key.
    """
    __slots__ = ()
    def __init__(self, iterable=None):
        """
        Creates a new ``multidict`` instance.
        
        Parameters
        ----------
        iterable : `None` or `iterable`, Optional
            Iterable to update the created multidict initially.
            
            Can be given as one of the following:
                - ``multidict`` instance.
                - `dict` instance.
                - `iterable` of `key` - `value` pairs.
        """
        dict.__init__(self)
        
        if (iterable is None) or (not iterable):
            return
        
        getitem = dict.__getitem__
        setitem = dict.__setitem__
        
        if isinstance(iterable, multidict):
            for key, values in dict.items(iterable):
                setitem(self, key, values.copy())
        
        elif isinstance(iterable, dict):
            for key, value in iterable.items():
                setitem(self, key, [value])
        
        else:
            for key, value in iterable:
                try:
                    values = getitem(self, key)
                except KeyError:
                    setitem(self, key, [value])
                else:
                    values.append(value)
    
    def __getitem__(self, key):
        """
        Returns the multidict's `value` for the given `key`. If the `key` has more values, then returns the 0th of
        them.
        """
        return dict.__getitem__(self, key)[0]
    
    def __setitem__(self, key, value):
        """Adds the given `key` - `value` pair to the multidict."""
        try:
            line = dict.__getitem__(self, key)
        except KeyError:
            dict.__setitem__(self, key, [value])
        else:
            if value not in line:
                line.append(value)
    
    def __delitem__(self, key):
        """
        Removes the `value` for the given `key` from the multidict. If the `key` has more values, then removes only
        the 0th of them.
        """
        my_list = dict.__getitem__(self, key)
        if len(my_list) == 1:
            dict.__delitem__(self, key)
        else:
            del my_list[0]
    
    def extend(self, mapping):
        """
        Extends the multidict with the given `mapping`'s items.
        
        Parameters
        ----------
        mapping : `Any`
            Any mapping type, what has `.items` attribute.
        """
        getitem = dict.__getitem__
        setitem = dict.__setitem__
        for key, value in mapping.items():
            try:
                values = getitem(self, key)
            except KeyError:
                setitem(self, key, [value])
            else:
                if value not in values:
                    values.append(value)
    
    def get_all(self, key, default=None):
        """
        Returns all the values matching the given `key`.
        
        Parameters
        ----------
        key : `Any`
            The `key` to match.
        default : `Any`, Optional
            Default value to return if `key` is not present in the multidict. Defaults to `None`.
        
        Returns
        -------
        values : `default or `list` of `Any`
            The values for the given `key` if present.
        """
        try:
            return dict.__getitem__(self, key).copy()
        except KeyError:
            return default
    
    def get_one(self, key, default=None):
        """
        Returns the 0th value matching the given `key`.
        
        Parameters
        ----------
        key : `Any`
            The key to match.
        default : `Any`, Optional
            Default value to return if `key` is not present in the multidict. Defaults to `None`.
        
        Returns
        -------
        value : `default` or `Any`
            The value for the given key if present.
        """
        try:
            values =  dict.__getitem__(self, key)
        except KeyError:
            return default
        else:
            return values[0]
    
    get = get_one
    
    def setdefault(self, key, default=None):
        """
        Returns the value for the given `key`.
        
        If the `key` is not present in the multidict, then set's the given `default` value as it.
        
        Parameters
        ----------
        key : `Any`
            The key to match.
        default : `Any`, Optional
            Default value to set and return if `key` is not present in the multidict.
        
        Returns
        -------
        value : `default` or `Any`
            The first value for which `key` matched, or `default` if none.
        """
        try:
            values = dict.__getitem__(self, key)
        except KeyError:
            pass
        else:
            return values[0]
        
        dict.__setitem__(self, key, [default])
        return default
    
    def pop_all(self, key, default=_spaceholder):
        """
        Removes all the values from the multidict which the given `key` matched.
        
        Parameters
        ----------
        key : `Any`
            The key to match.
        default : `Any`, Optional
            Default value to return if `key` is not present in the multidict.
        
        Returns
        -------
        values : `default` or `list` of `Any`
            The matched values. If `key` is not present, but `default` value is given, then returns that.
        
        Raises
        ------
        KeyError
            if `key` is not present in the multidict and `default` value is not given either.
        """
        try:
            return dict.pop(self, key)
        except KeyError:
            if default is not _spaceholder:
                return default
            raise
    
    def pop_one(self, key, default=_spaceholder):
        """
        Removes the first value from the multidict, which matches the given `key`.
        
        Parameters
        ----------
        key : `Any`
            The key to match.
        default : `Any`, Optional
            Default value to return if `key` is not present in the multidict.
        
        Returns
        -------
        value : `default` or `list` of `Any`
            The 0th matched value. If `key` is not present, but `default` value is given, then returns that.
        
        raises
        ------
        KeyError
            if `key` is not present in the multidict and `default` value is not given either.
        """
        try:
            values =  dict.__getitem__(self, key)
        except KeyError:
            if default is not _spaceholder:
                return default
            raise
        else:
            value = values.pop(0)
            if not values:
                dict.__delitem__(self, key)
            
            return value
    
    pop = pop_one   
    
    # inheritable:
    def copy(self):
        """
        Copies the multidict.
        
        Returns
        -------
        new : ``multidict`` instance
            The new multidict.
        """
        new = dict.__new__(type(self))
        setitem = dict.__setitem__
        for key, values in dict.items(self):
            setitem(new, key, values.copy())
        
        return new
    
    def items(self):
        """
        Returns an item iterator for the multidict.
        
        Returns
        -------
        items : ``_multidict_items``
        """
        return _multidict_items(self)
    
    def values(self):
        """
        Returns a value iterator for the multidict.
        
        Returns
        -------
        items : ``_multidict_values``
        """
        return _multidict_values(self)
    
    def __repr__(self):
        """Returns the multidict's representation."""
        result = [
            self.__class__.__name__,
            '({',
                ]
        
        if self:
            for key, value in self.items():
                result.append(repr(key))
                result.append(': ')
                result.append(repr(value))
                result.append(', ')
            
            result[-1] = '})'
        else:
            result.append('})')
        
        return ''.join(result)
    
    __str__ = __repr__

    def kwargs(self):
        """
        Converts the multidict to `**kwargs`-able dictionary. If a `key` has more values, then always returns the last
        value for it.
        
        Returns
        -------
        result : `dict` of (`Any`, `Any`) items
        """
        result = {}
        for key, values in dict.items(self):
            result[key] = values[-1]
        
        return result
    
    update = RemovedDescriptor()
    
class imultidict(multidict):
    """
    ``multidict`` subclass, what can be used to hold http headers.
    
    It's keys ignore casing.
    """
    __slots__ = ()
    def __init__(self, iterable=None):
        """
        Creates a new ``imultidict`` instance.
        
        Parameters
        ----------
        iterable : `None` or `iterable`, Optional
            Iterable to update the created multidict initially.
            
            Can be given as one of the following:
                - ``multidict`` instance.
                - `dict` instance.
                - `iterable` of `key` - `value` pairs.
        """
        dict.__init__(self)
        
        if (iterable is None) or (not iterable):
            return
        
        getitem = dict.__getitem__
        setitem = dict.__setitem__
        
        if type(iterable) is type(self):
            for key, values in dict.items(iterable):
                setitem(self, key, values.copy())
        
        elif isinstance(iterable, multidict):
            for key, values in dict.items(iterable):
                setitem(self, istr(key), values.copy())
        
        elif isinstance(iterable, dict):
            for key, value in iterable.items():
                key = istr(key)
                setitem(self, key, [value])
        
        else:
            for key, value in iterable:
                key = istr(key)
                try:
                    values = getitem(self, key)
                except KeyError:
                    setitem(self, key, [value])
                else:
                    values.append(value)
    
    def __getitem__(self, key):
        """
        Returns the multidict's `value` for the given `key`. If the `key` has more values, then returns the 0th of
        them.
        """
        key = istr(key)
        return dict.__getitem__(self, key)[0]
    
    def __setitem__(self, key, value):
        """Adds the given `key` - `value` pair to the multidict."""
        key = istr(key)
        multidict.__setitem__(self, key, value)
    
    def __delitem__(self, key):
        """
        Removes the `value` for the given `key` from the multidict. If the `key` has more values, then removes only
        the 0th of them.
        """
        key = istr(key)
        multidict.__delitem__(self, key)
    
    def extend(self, mapping):
        """
        Extends the multidict titled with the given `mapping`'s items.
        
        Parameters
        ----------
        mapping : `Any`
            Any mapping type, what has `.items` attribute.
        """
        getitem = dict.__getitem__
        setitem = dict.__setitem__               
        for key, value in mapping.items():
            key = istr(key)
            try:
                values = getitem(self, key)
            except KeyError:
                setitem(self, key, [value])
            else:
                if value not in values:
                    values.append(value)
    
    def get_all(self, key, default=None):
        """
        Returns all the values matching the given `key`.
        
        Parameters
        ----------
        key : `Any`
            The `key` to match.
        default : `Any`, Optional
            Default value to return if `key` is not present in the multidict. Defaults to `None`.
        
        Returns
        -------
        values : `default or `list` of `Any`
            The values for the given `key` if present.
        """
        key = istr(key)
        return multidict.get_all(self, key, default)
    
    def get_one(self, key, default=None):
        """
        Returns the 0th value matching the given `key`.
        
        Parameters
        ----------
        key : `Any`
            The key to match.
        default : `Any`, Optional
            Default value to return if `key` is not present in the multidict. Defaults to `None`.
        
        Returns
        -------
        value : `default` or `Any`
            The value for the given key if present.
        """
        key = istr(key)
        return multidict.get_one(self, key, default)
    
    get = get_one
    
    def setdefault(self, key, default=None):
        """
        Returns the value for the given `key`.
        
        If the `key` is not present in the multidict, then set's the given `default` value as it.
        
        Parameters
        ----------
        key : `Any`
            The key to match.
        default : `Any`, Optional
            Default value to set and return if `key` is not present in the multidict.
        
        Returns
        -------
        value : `default` or `Any`
            The first value for which `key` matched, or `default` if none.
        """
        key = istr(key)
        return multidict.setdefault(self, key, default)
    
    def pop_all(self, key, default=_spaceholder):
        """
        Removes all the values from the multidict which the given `key` matched.
        
        Parameters
        ----------
        key : `Any`
            The key to match.
        default : `Any`, Optional
            Default value to return if `key` is not present in the multidict.
        
        Returns
        -------
        values : `default` or `list` of `Any`
            The matched values. If `key` is not present, but `default` value is given, then returns that.
        
        Raises
        ------
        KeyError
            if `key` is not present in the multidict and `default` value is not given either.
        """
        key = istr(key)
        return multidict.pop_all(self, key, default)

    def pop_one(self, key, default=_spaceholder):
        """
        Removes the first value from the multidict, which matches the given `key`.
        
        Parameters
        ----------
        key : `Any`
            The key to match.
        default : `Any`, Optional
            Default value to return if `key` is not present in the multidict.
        
        Returns
        -------
        value : `default` or `list` of `Any`
            The 0th matched value. If `key` is not present, but `default` value is given, then returns that.
        
        raises
        ------
        KeyError
            if `key` is not present in the multidict and `default` value is not given either.
        """
        key = istr(key)
        return multidict.pop_one(self, key, default)
    
    pop = pop_one


class istr(str):
    """
    Strings, which have their casing ignored.
    
    Attributes
    ----------
    _casefold : `str`
        Casefolded version of the string.
    """
    __slots__ = '_casefold'
    def __new__(cls, value='', encoding=sys.getdefaultencoding(), errors='strict'):
        """
        Return an string which ignores casing. If object is not provided, returns the empty string. Otherwise, the
        behavior of ``istr`` depends on whether encoding or errors is given, as follows.
        
        If neither encoding nor errors is given, `istr(object)` returns `object.__str__()`, which is the "informal" or
        nicely printable string representation of object. For string objects, this is `string`. If object does not have
        a `__str__()` method, then `istr()` falls back to returning `repr(object)`.
        
        If at least one of encoding or errors is given, object should be a `bytes-like` object. In this case, if object
        is a `byte-like` object, then `istr(bytes, encoding, errors)` is equivalent to `bytes.decode(encoding, errors)`.
        Otherwise, the bytes object underlying the buffer object is obtained before calling `bytes.decode()`.
        
        Passing a `bytes-like` object to ``istr`` without the encoding or errors arguments falls under the first case
        of returning the informal string representation.
        
        Parameters
        ----------
        value : `Any`, Optional
            The value, what is representation or encoded version is returned.
        encoding : `str`, Optional
            Encoding to use when decoding a `bytes-like`.
        errors : `str`, Optional
            May be given to set a different error handling scheme when decoding from `bytes-like`. The default `errors`
            value is `'strict'`, meaning that encoding errors raise a `UnicodeError`. Other possible values are
            `'ignore'`, `'replace'`, `'xmlcharrefreplace'`, `'backslashreplace'` and any other name registered via
            `codecs.register_error()`.
        
        Returns
        -------
        self : ``istr``
        """
        if type(value) is cls:
            return value
        
        if isinstance(value,(bytes, bytearray, memoryview)):
            value = str(value, encoding, errors)
        elif isinstance(value, str):
            pass
        else:
            value = str(value)
        
        self = str.__new__(cls, value)
        self._casefold = str.casefold(value)
        return self
    
    def __hash__(self):
        """Returns the string's hash value."""
        return hash(self._casefold)
    
    def __eq__(self, other):
        """Returns whether the two strings are equal."""
        other_type = other.__class__
        if other_type is type(self):
            other_value = other._casefold
        elif other_type is str:
            other_value = other.casefold()
        elif issubclass(other, str):
            other_value = str.casefold(other)
        else:
            return NotImplemented
        
        return (self._casefold == other_value)


def list_difference(list1, list2):
    """
    Returns the difference of the two given lists.
    
    Parameters
    ----------
    list1 : `None`, `list`, `set`
        The first list, what's inclusive elements should go into the return's zero-th element.
    list2 : `None`, `list`, `set`
        The second list, what's inclusive elements should go into the return's one-th element.
    
    Returns
    -------
    difference : `tuple` (`list` of `Any`, `list` of `Any`)
        A tuple containing the inclusive element of the given parameters.
    
    Notes
    -----
    `list1` and `list2` should be given as sorted lists, but `None` and `set` instances are also accepted.
    """
    difference = ([], [])
    
    if list1 is None:
        if list2 is None:
            return difference
        else:
            difference[1].extend(list2)
            return difference
    else:
        if list2 is None:
            difference[0].extend(list1)
            return difference
    
    if isinstance(list1, set):
        list1 = sorted(list1)
    if isinstance(list2, set):
        list2 = sorted(list2)
        
    ln1 = len(list1)
    ln2 = len(list2)
    index1 = 0
    index2 = 0

    #some quality python here again *cough*
    while True:
        if index1 == ln1:
            while True:
                if index2 == ln2:
                    break
                value2 = list2[index2]
                difference[1].append(value2)
                index2 += 1

            break
        if index2 == ln2:
            while True:
                if index1 == ln1:
                    break
                value1 = list1[index1]
                difference[0].append(value1)
                index1 += 1

            break
        
        value1 = list1[index1]
        value2 = list2[index2]
        if value1 < value2:
            difference[0].append(value1)
            index1 += 1
            continue
        if value1 > value2:
            difference[1].append(value2)
            index2 += 1
            continue
        if value1 != value2:
            difference[0].append(value1)
            difference[1].append(value2)
        index1 += 1
        index2 += 1
    
    return difference

class cached_property(object):
    """
    Cached property, what can be used as a method decorator. It operates almost like python's `@property`, but it puts
    the result of the method to the respective instance's `_cache`, preferably type `dict` attribute.
    
    Attributes
    ----------
    fget : `function`
        Getter method of the cached property.
    name : `str`
        The name of the cached property.
    """
    __slots__ = ('fget', 'name',)
    
    def __new__(cls, fget):
        """
        Creates a new cached property instance with the given getter.
        
        Parameters
        ----------
        fget : `function`
            Getter method of the cached property.

        Raises
        ------
        TypeError
            If `fget` has no name or it's name is not `str` instance.
        """
        name = getattr(fget, '__name__', None)
        
        name_type = name.__class__
        if name_type is NoneType:
            name_type_correct = False
        elif name_type is str:
            name_type_correct = True
        elif issubclass(name_type, str):
            name = str(name)
            name_type_correct = True
        else:
            name_type_correct = False
        
        if not name_type_correct:
            raise TypeError(f'`fget` has no attribute or has, but non string attribute `__name__`, got '
                f'{name_type.__name__}.')
        
        self = object.__new__(cls)
        self.fget = fget
        self.name = name
        return self
    
    def __get__(self, obj, type_):
        if obj is None:
            return self
        
        value = obj._cache.get(self.name, _spaceholder)
        if value is _spaceholder:
            value = self.fget(obj)
            obj._cache[self.name] = value
        
        return value
    
    def __set__(self, obj, value):
        raise AttributeError('can\'t set attribute')
    
    def __delete__(self, obj):
        raise AttributeError('can\'t delete attribute')

class alchemy_incendiary(object):
    """
    Function wrapper familiar to `functools.partial`.
    
    Used by hata to run functions inside of executors.
    
    Attributes
    ----------
    args : `tuple` of `Any`
        Arguments to call `func` with.
    func : `callable`
        The function to call.
    kwargs : `None` of `dict` of (`str`, `Any`) items
        Keyword arguments to call func with if applicable.
    """
    __slots__ = ('args', 'func', 'kwargs',)
    def __init__(self, func, args, kwargs=None):
        """
        Creates a new `alchemy_incendiary` instance with the given parameters.
        
        Parameters
        ----------
        func : `callable`
            The function to call.
        args : `tuple` of `Any`
            Arguments to call `func` with.
        kwargs : `None` of `dict` of (`str`, `Any`) items, Optional
            Keyword arguments to call func with if applicable.
        """
        self.func = func
        self.args = args
        self.kwargs = kwargs
    
    def __call__(self):
        """
        Calls the ``alchemy_incendiary``'s inner function with t's arguments and keyword arguments.
        
        Returns
        -------
        result : `Any`
            The returned value by ``.func``.
        
        Raises
        ------
        BaseException
            The raised exception by ``.func``.
        """
        kwargs = self.kwargs
        if kwargs is None:
            return self.func(*self.args)
        
        return self.func(*self.args, **kwargs)

class SubCheckType(type):
    """
    Metaclass, which can be used for subclass checks. It's type instances should implement a `.__subclasses__`
    class attribute, which contain's all of it's "subclasses".
    """
    def __instancecheck__(cls, instance):
        """Returns whether the given instance's type is a subclass of the respective type."""
        return (type(instance) in cls.__subclasses__)

    def __subclasscheck__(cls, klass):
        """Returns whether the given type is a subclass of the respective type."""
        return (klass in cls.__subclasses__)

class MethodLike(metaclass=SubCheckType):
    """
    Base class for methods.
    
    Class Attributes
    ----------------
    __subclasses__ : `set` of `type`
        Registered method types.
    __reserved_argcount__ : `int` = `1`
        The amount of reserved arguments by a method subclass.
    """
    __subclasses__ = {method}
    __slots__ = ()
    def __init_subclass__(cls):
        cls.__subclasses__.add(cls)
    
    __reserved_argcount__ = 1
    
    @classmethod
    def get_reserved_argcount(cls, instance):
        """
        Returns the given `instance`'s reserved argcount.
        
        Parameters
        ----------
        instance : `method-like`
            A method like object.
        
        Returns
        -------
        reserved_argcount : `int`
            Reserved argcount of the given method like.
        
        Raises
        ------
        TypeError
            If `instance` is not given as a `method-like`.
        """
        instance_type = instance.__class__
        reserved_argcount = getattr(instance_type, '__reserved_argcount__', -1)
        if reserved_argcount != -1:
            return reserved_argcount
        
        if instance_type in cls.__subclasses__:
            return cls.__reserved_argcount__
        
        raise TypeError(f'Expected a method like, got {instance_type.__name__}.')

class basemethod(MethodLike):
    """
    A `method-like`, which always passes to it's function the respective type and an instance. The instance might be
    given as `None` if used as a classmethod.
    
    Attributes
    ----------
    __base__ : `Any`
        The instance from where the method was called from. Might be `None` if used as a classmethod.
    __func__ : `function`
        The method's function to call.
    __self__ : `type`
        The class from where the method was called from.
    
    Class Attributes
    ----------------
    __reserved_argcount__ : `int` = `2`
        The amount of reserved arguments by basemethods.
    """
    __slots__ = ('__base__', '__func__', '__self__', )
    __reserved_argcount__ = 2
    
    def __init__(self, func, cls, base):
        """
        Creates a new basemethod with the given parameters.
        
        Parameters
        ----------
        func : `function`
            The method's function to call.
        cls : `type`
            The class from where the method was called from.
        base : `Any`
            The instance from where the method was called from. Can be given as `None` as well.
        """
        self.__base__ = base
        self.__func__ = func
        self.__self__ = cls
    
    def __call__(self, *args, **kwargs):
        """
        Calls the basemethod with the given parameters.
        
        Parameters
        ----------
        *args : Arguments
            Arguments to call the internal function with.
        **kwargs : Keyword arguments
            Keyword arguments to call the internal function with.
        
        Returns
        -------
        result : `Any`
            The object returned by the internal function.
        
        Raises
        ------
        BaseException
            Exception raised by the internal function.
        """
        return self.__func__(self.__self__, self.__base__, *args, **kwargs)
    
    def __getattr__(self,name):
        return getattr(self.__func__, name)
    
    __class_doc__ = None
    
    @property
    def __instance__doc__(self):
        """
        Returns the ``basemethod``'s internal function's docstring.
        
        Returns
        -------
        docstring : `None` or `str`
        """
        return self.__func__.__doc__
    
    __doc__ = doc_property()

class BaseMethodDescriptor(object):
    """
    Descriptor, which can be used as a decorator to wrap a function to a basemethod.
    
    Attributes
    ----------
    fget : `function`
        The wrapped function.
    """
    __slots__ = ('fget',)
    def __init__(self, fget):
        """
        Creates a new ``BaseMethodDescriptor`` instance with the given parameter.
        
        Parameters
        ----------
        fget : `function`
            The function to wrap.
        """
        self.fget = fget
    
    def __get__(self, obj, type_):
        return basemethod(self.fget, type_, obj)
    
    def __set__(self, obj, value):
        raise AttributeError('can\'t set attribute')
    
    def __delete__(self, obj):
        raise AttributeError('can\'t delete attribute')

# This 2 type can be function
wrapper_descriptor = type(object.__ne__)
method_descriptor = type(object.__format__)

DO_NOT_MODULIZE_TYPES = [mapping_proxy, getset_descriptor, ]

if wrapper_descriptor is not function:
    DO_NOT_MODULIZE_TYPES.append(wrapper_descriptor)

if method_descriptor is not function:
    DO_NOT_MODULIZE_TYPES.append(method_descriptor)

DO_NOT_MODULIZE_TYPES = tuple(DO_NOT_MODULIZE_TYPES)

del mapping_proxy
del getset_descriptor
del wrapper_descriptor
del method_descriptor

def _modulize_function(old, globals_, source_module, module_name, module_path):
    """
    Changes the given function's scopes and qualname if they were defined inside of a modulized class.
    
    Parameters
    ----------
    old : `function`
        A function present inside of a modulized class.
    globals_ : `dict` of (`str`, `Any`)
        Global variables of the respective module.
    source_module : `module`
        The module, where the modulized class was defined.
    module_name : `str`
        The newly created module's name.
    module_path : `str`
        The newly created module's path.

    Returns
    -------
    new : `function`
        Newly recreated function if applicable.
    """
    if old.__module__ != source_module:
        return old
    
    new = function(old.__code__, globals_, old.__name__, old.__defaults__, old.__closure__)
    new.__module__ = module_path
    qualname = old.__qualname__
    if (qualname is not None) and (len(qualname) > len(module_name)) and qualname[len(module_name)] =='.' and \
            qualname.startswith(module_name):
        new.__qualname__ = qualname[len(module_name)+1:]
    
    return new

def _modulize_type(klass, globals_, source_module, module_name, module_path):
    """
    Changes the given class's scopes and qualname if they were defined inside of a modulized class.
    
    Parameters
    ----------
    klass : `type`
        A class present inside of a modulized class.
    globals_ : `dict` of (`str`, `Any`)
        Global variables of the respective module.
    source_module : `module`
        The module, where the modulized class was defined.
    module_name : `str`
        The newly created module's name.
    module_path : `str`
        The newly created module's path.
    """
    if klass.__module__ != source_module:
        return
    
    qualname = klass.__qualname__
    if (qualname is None) or (len(qualname) <= len(module_name)) or qualname[len(module_name)] != '.' \
            or not qualname.startswith(module_name):
        return
    
    klass.__qualname__ = qualname[len(module_name)+1:]
    klass.__module__ = module_path
    
    for name in dir(klass):
        value = getattr(klass, name)
        
        value_type = value.__class__
        if value_type is function:
            value = _modulize_function(value, globals_, source_module, module_name, module_path)
            setattr(klass, name, value)
        
        if issubclass(value_type, type):
            _modulize_type(value, globals_, source_module, module_name, module_path)

def modulize(klass):
    """
    Transforms the given class to a module.
    
    Every functions and classes defined inside of given class, which are also present at transformation as well, will
    have their global scope modified.
    
    Parameters
    ----------
    klass : `type`
        The class to transform to module.
    
    Returns
    -------
    result_module : `module`
        The created module object.
    
    Raises
    ------
    TypeError
        If `klass` is not given as `type` instance.
    """
    if not isinstance(klass, type):
        raise TypeError('Only types can be modulized.')
    
    source_module = klass.__module__
    module_name = klass.__name__
    module_path = f'{klass.__module__}.{module_name}'
    try:
        result_module = sys.modules['module_path']
    except KeyError:
        result_module = module(module_path)
        sys.modules[module_path] = result_module
        globals_ = result_module.__dict__
        globals_['__builtins__'] = __builtins__
    else:
        globals_ = result_module.__dict__
        collected_names = []
        for name in globals_.keys():
            if name.startswith('__') and name.endswith('__'):
                continue
            
            collected_names.append(name)
        
        for name in collected_names:
            del globals_[name]
        
        globals_['__doc__'] = None
    
    for name in type.__dir__(klass):
        if name.startswith('__') and name.endswith('__') and name != '__doc__':
            continue
        
        value = type.__getattribute__(klass, name)
        value_type = type(value)
        if value_type in DO_NOT_MODULIZE_TYPES:
            continue
        
        if value_type is function:
            value = _modulize_function(value, globals_, source_module, module_name, module_path)
        
        if issubclass(value_type, type):
            _modulize_type(value, globals_, source_module, module_name, module_path)
        
        module.__setattr__(result_module, name, value)
    
    return result_module

class methodize(object):
    """
    Wraps a type to as a method, allowing instancing it with it's parent instance object passed by default.
    
    Attributes
    ----------
    klass : `type`
        The type to instance as a method.
    """
    __slots__ = ('klass',)
    def __init__(self, klass):
        """
        Creates a new ``methodize`` instance with the given class.
        
        Parameters
        ----------
        klass : `type`
             The type to instance as a method.
        """
        self.klass = klass
    
    def __get__(self, obj, type_):
        klass = self.klass
        if obj is None:
            return klass
        
        return method(klass, obj)
    
    def __set__(self, obj, value):
        raise AttributeError('can\'t set attribute')
    
    def __delete__(self, obj):
        raise AttributeError('can\'t delete attribute')

def copy_func(old):
    """
    Copies the given function.
    
    Parameters
    ----------
    old : `function`
        The function to copy.
    
    Returns
    -------
    new : `functions`
        The new created function.
    """
    new = function(old.__code__, old.__globals__, name=old.__name__, argdefs=old.__defaults__, closure=old.__closure__)
    new.__kwdefaults__ = old.__kwdefaults__
    return new

class sortedlist(list):
    """
    An auto sorted list.
    
    Attributes
    ----------
    _reversed : `bool`
        Whether the list is reversed.
    """
    __slots__ = ('_reversed', )
    
    __setitem__ = RemovedDescriptor()
    insert = RemovedDescriptor()
    sort = RemovedDescriptor()
    __add__ = RemovedDescriptor()
    __radd__ = RemovedDescriptor()
    __iadd__ = RemovedDescriptor()
    __mul__ = RemovedDescriptor()
    __rmul__ = RemovedDescriptor()
    __imul__ = RemovedDescriptor()
    append = RemovedDescriptor()
    
    def __init__(self, iterable=None, reverse=False):
        """
        Creates a new ``sortedlist`` instance with the given parameters.
        
        Parameters
        ----------
        it : `None` or `iterable`, Optional
            An iterable to extend the created list with.
        reverse : `bool`, Optional
            Whether the created list should be reversed sorted.
        """
        self._reversed = reverse
        if (iterable is not None):
            self.extend(iterable)
            list.sort(self, reverse=reverse)
    
    def __repr__(self):
        """Returns the sortedlist's representation."""
        result = [self.__class__.__name__, '([']
        
        limit = len(self)
        if limit:
            index = 0
            while True:
                element = self[index]
                index +=1
                result.append(repr(element))
                
                if index == limit:
                    break
                
                result.append(', ')
                continue
        
        result.append('], reversed=')
        result.append(repr(self._reversed))
        result.append(')')
        
        return ''.join(result)
    
    def __getstate__(self):
        return self._reversed
    
    def __setstate__(self, state):
        self._reversed = state
    
    def _get_reverse(self):
        return self._reversed
    
    def _set_reverse(self, value):
        if self._reversed == value:
            return
        self._reversed = value
        list.reverse(self)
    
    reverse = property(_get_reverse, _set_reverse)
    del _get_reverse, _set_reverse
    
    if DOCS_ENABLED:
        reverse.__doc__ = (
    """
    A get-set descriptor to check or set how the sortedlist sorted.
    """)
    
    def add(self, value):
        """
        Adds a new value to the sortedlist.
        
        Parameters
        ----------
        value : `Any`
            The value to insert to the sortedlist.
        """
        index = self.relative_index(value)
        if index == len(self):
            # If the the index is at the end, then we just list append it.
            list.append(self, value)
            return
        
        element = self[index]
        if element == value:
            # If the element is same as the current, we overwrite it.
            list.__setitem__(self, index, value)
            return
        
        # No more special cases, simply list insert it
        list.insert(self, index, value)
        return
    
    def remove(self, value):
        """
        Removes the given value from the sortedlist.
        
        If the value is not in the list will not raise.
        
        Parameters
        ----------
        value : `Any`
            The value to remove.
        """
        index = self.relative_index(value)
        if index == len(self):
            # The element is not at self, leave
            return
        
        element = self[index]
        if element != value:
            # The element is different as the already added one att the correct position, leave.
            return
        
        # No more special case, remove it.
        list.__delitem__(self, index)
    
    def extend(self, iterable):
        """
        Extends the sortedlist with the given iterable object.
        
        Parameters
        ----------
        iterable : `iterable`
            Iterable object to extend the sortedlist with.
        """
        ln = len(self)
        insert = list.insert
        bot = 0
        if self._reversed:
            if type(self) is not type(iterable):
                other = sorted(iterable, reverse=True)
            elif not iterable._reversed:
                other = reversed(iterable)
            for value in iterable:
                top = ln
                while True:
                    if bot < top:
                        half = (bot+top)>>1
                        if self[half] > value:
                            bot = half+1
                        else:
                            top = half
                        continue
                    break
                insert(self, bot, value)
                ln +=1
        else:
            if type(self) is not type(iterable):
                other = sorted(iterable)
            elif iterable._reversed:
                other = reversed(iterable)
            for value in iterable:
                top = ln
                while True:
                    if bot < top:
                        half = (bot+top)>>1
                        if self[half] < value:
                            bot = half+1
                        else:
                            top = half
                        continue
                    break
                insert(self, bot, value)
                ln += 1
    
    def __contains__(self, value):
        """Returns whether the sortedlist contains the given value."""
        index = self.relative_index(value)
        if index == len(self):
            return False
        
        if self[index] == value:
            return True
        
        return False
    
    def index(self, value):
        """Returns the index of the given value inside of the sortedlist."""
        index = self.relative_index(value)
        if index == len(self) or self[index] != value:
            raise ValueError(f'{value!r} is not in the {self.__class__.__name__}.')
        return index
    
    def relative_index(self, value):
        """
        Returns the relative index of the given value if it would be inside of the sortedlist.
        
        Parameters
        ----------
        value : `Any`
            The object's what's relative index is returned.
        
        Returns
        -------
        .relative_index : `bool`
            The index where the given value would be inserted or should be inside of the sortedlist.
        """
        bot = 0
        top = len(self)
        if self._reversed:
            while True:
                if bot < top:
                    half = (bot+top)>>1
                    if self[half] > value:
                        bot = half+1
                    else:
                        top = half
                    continue
                break
        else:
            while True:
                if bot < top:
                    half = (bot+top)>>1
                    if self[half] < value:
                        bot = half+1
                    else:
                        top = half
                    continue
                break
        return bot
    
    def keyed_relative_index(self, value, key):
        """
        Returns the relative index of the given value if it would be inside of the sortedlist.
        
        Parameters
        ----------
        value : `Any`
            The object's what's relative index is returned.
        key : `callable`
            A function that serves as a key for the sort comparison.
        
        Returns
        -------
        .relative_index : `bool`
            The index where the given value would be inserted or should be inside of the sortedlist.
        """
        bot = 0
        top = len(self)
        if self._reversed:
            while True:
                if bot < top:
                    half = (bot+top)>>1
                    if key(self[half]) > value:
                        bot = half+1
                    else:
                        top = half
                    continue
                break
        else:
            while True:
                if bot < top:
                    half = (bot+top)>>1
                    if key(self[half]) < value:
                        bot = half+1
                    else:
                        top = half
                    continue
                break
        return bot
    
    def copy(self):
        """
        Copies the sortedlist.
        
        Returns
        -------
        new : ``sortedlist``
        """
        new = list.__new__(type(self))
        new._reversed = self._reversed
        list.extend(new, self)
        return new
    
    def resort(self):
        """
        Resorts the sortedlist.
        """
        list.sort(self, reverse=self._reversed)
    
    def get(self, value, key, default=None):
        """
        Gets an element from the sortedlist, what passed trough `key` equals to the given value.
        
        Parameters
        ----------
        value : `Any`
            The value to search in the sortedlist.
        key : `callable`
            A function that serves as a key for the sort comparison.
        default : `Any`, Optional
            Default value to returns if no matching element was present. Defaults to `None`.
        
        Returns
        -------
        element : `Any` or `default`
            The matched element or the `default` value if not found.
        """
        index = self.keyed_relative_index(value, key)
        if index == len(self):
            return default
        
        element = self[index]
        if key(element) == value:
            return element
        
        return default
    
    def pop(self, value, key, default=None):
        """
        Gets and removes element from the sortedlist, what's is passed trough `key` equals to the given value.
        
        Parameters
        ----------
        value : `Any`
            The value to search in the sortedlist.
        key : `callable`
            A function that serves as a key for the sort comparison.
        default : `Any`, Optional
            Default value to returns if no matching element was present. Defaults to `None`.
        
        Returns
        -------
        element : `Any` or `default`
            The matched element or the `default` value if not found.
        """
        index = self.keyed_relative_index(value, key)
        if index == len(self):
            return default
        
        element = self[index]
        if key(element) == value:
            del self[index]
            return element
        
        return default

def is_weakreferable(object_):
    """
    Returns whether the given object is weakreferable.
    
    Parameters
    ----------
    object_ : `Any`
        The object to check.
    
    Returns
    -------
    is_weakreferable : `bool`
    """
    slots = getattr(type(object_), '__slots__', None)
    if (slots is not None) and ('__weakref__' in slots):
        return True
    
    if hasattr(object_, '__dict__'):
        return True
    
    return False

# Test for pypy bug:
# https://foss.heptapod.net/pypy/pypy/issues/3239
class dummy_init_tester:
    def __new__(cls, value):
        return object.__new__(cls)
    __init__ = object.__init__

try:
    dummy_init_tester(None)
except TypeError:
    NEEDS_DUMMY_INIT = True
else:
    NEEDS_DUMMY_INIT = False

class WeakHasher(object):
    """
    Object to store unhashable weakreferences.
    
    Attributes
    ----------
    _hash : `int`
        The hash of the respective reference.
    reference : ``WeakReferer`` instance
        A dead reference to hash.
    """
    __slots__ = ('_hash', 'reference',)
    def __init__(self, reference):
        """
        Creates a new ``WeakHasher`` instance from the given reference.
        
        Parameters
        ----------
        reference : ``WeakReferer`` instance
            A dead reference to hash.
        """
        self._hash = object.__hash__(reference)
        self.reference = reference
    
    def __hash__(self):
        """Returns the ``WeakHasher``'s hash value."""
        return self._hash
    
    def __eq__(self, other):
        """Returns whether the two ``WeakHasher``-s are the same."""
        self_reference = self.reference
        if self_reference is other:
            return True
        
        if type(self) is not type(other):
            return NotImplemented
        
        return (self.reference is other.reference)
    
    def __repr__(self):
        """Returns the ``WeakHasher``'s representation."""
        return f'{self.__class__.__name__}({self.reference!r})'
    
    def __getattr__(self, name):
        """Returns the attribute of the ``WeakHasher``'s reference."""
        return getattr(self.reference, name)


def add_to_pending_removals(container, reference):
    """
    Adds the given weakreference to the given set.
    
    Parameters
    ----------
    container : `Any`
        The parent object, which is iterating right now, so it's items cannot be removed.
    reference : ``WeakReferer`` instance
        The weakreference to add to the set.
    """
    try:
        hash(reference)
    except TypeError:
        reference = WeakHasher(reference)
    
    pending_removals = container._pending_removals
    if pending_removals is None:
        container._pending_removals = pending_removals = set()
    
    pending_removals.add(reference)


# speedup builtin stuff, Cpython is welcome
class WeakReferer(WeakrefType):
    """
    Weakreferences to an object.
    
    After calling it returns the referenced object or `None` if already dead.
    """
    __slots__ = ()
    if NEEDS_DUMMY_INIT:
        def __init__(self, *args, **kwargs):
            pass
    else:
        __init__ = object.__init__

class KeyedReferer(WeakReferer):
    """
    Weakreferences an object with a key, what can be used to identify it.
    
    Attributes
    ----------
    key : `Any`
        Key to identify the weakreferenced object.
    """
    __slots__ = ('key', )
    def __new__(cls, obj, callback, key, ):
        """
        Creates a new ``KeyedReferer`` instance with the given parameters.
        
        Parameters
        ----------
        obj : `Any`
            The object to weakreference.
        callback : `Any`
            Callback running when the object is garbage collected.
        key : `Any`
            Key to identify the weakreferenced object.
        """
        self = WeakReferer.__new__(cls, obj, callback)
        self.key = key
        return self

class WeakCallable(WeakReferer):
    """
    Weakreferences a callable object.
    
    When the object is called, calls the weakreferenced object if not yet collected.
    """
    __slots__ = ()
    def __call__(self, *args, **kwargs):
        """
        Calls the weakreferenced object if not yet collected.
        
        Parameters
        ----------
        *args : Arguments
            Arguments to call the weakreferenced callable with.
        **kwargs : Keyword arguments
            Keyword arguments to call the weakreferenced callable with..
        
        Returns
        -------
        result : `Any`
            The returned value by the referenced object. Returns `None` if the object is already collected.
        
        Raises
        ------
        BaseException
            Raised exception by the referenced callable.
        """
        self = WeakReferer.__call__(self)
        if self is None:
            return
        
        return self(*args, **kwargs)
    
    def is_alive(self):
        """
        Returns whether the ``WeakCallable`` is still alive (the referred object by it is not collected yet.)
        
        Returns
        -------
        is_alive : `bool`
        """
        return (WeakReferer.__call__(self) is not None)

class weakmethod(WeakReferer, MethodLike):
    """
    A method like, what weakreferences it's object not blocking it from being garbage collected.
    
    Attributes
    ----------
    __func__ : `callable`
        The function to call as a method.
    
    Class Attributes
    ----------------
    __reserved_argcount__ : `int` = `1`
        The amount of reserved arguments by weakmethod.
    """
    __slots__ = ('__func__',)
    __reserved_argcount__ = 1
    
    def __new__(cls, obj, func, callback=None):
        """
        Creates a new ``weakmethod`` instance with the given parameter.
        
        Parameters
        ----------
        obj : `Any`
            The object to weakreference and pass to `func`.
        func : `callable`
            The function to call as a method.
        callback : `Any`, Optional
            Callback running when the object is garbage collected.
        """
        self = WeakReferer.__new__(cls, obj, callback)
        self.__func__ = func
        return self
    
    @property
    def __self__(self):
        """
        Returns the weakreferenced object by the ``weakmethod`` or `None`if it was already garbage collected.
        
        Returns
        -------
        obj : `Any`
            The weakreferenced object if not yet garbage collected. Defaults to `None`.
        """
        return WeakReferer.__call__(self)
    
    def __call__(self, *args, **kwargs):
        """
        Calls the weakmethod object's function with it's object if not yet collected.
        
        Parameters
        ----------
        *args : Arguments
            Arguments to call the function with.
        **kwargs : Keyword arguments
            Keyword arguments to call the function with.
        
        Returns
        -------
        result : `Any`
            The returned value by the function. Returns `None` if the object is already collected.
        
        Raises
        ------
        BaseException
            Raised exception by the function.
        """
        obj = WeakReferer.__call__(self)
        if obj is None:
            return
        
        return self.__func__(obj, *args, **kwargs)
    
    def is_alive(self):
        """
        Returns whether the ``weakmethod``'s object is still alive (the referred object by it is not collected yet.)
        
        Returns
        -------
        is_alive : `bool`
        """
        return (WeakReferer.__call__(self) is not None)
    
    def __getattr__(self, name):
        return getattr(self.__func__, name)
    
    @classmethod
    def from_method(cls, method_, callback=None):
        """
        Creates a new ``weakmethod`` instance from the given `method`.
        
        Parameters
        ----------
        method_ : `method`
            The method tu turn into ``weakmethod``.
        callback : `Any`, Optional
            Callback running when the respective object is garbage collected.
        """
        self = WeakReferer.__new__(cls, method_.__self__, callback)
        self.__func__ = method_.__func__
        return self


class _WeakValueDictionaryCallback(object):
    """
    Callback used by ``WeakValueDictionary``-s and by ``HybridValueDictionary``-s.
    
    Attributes
    ----------
    _parent : ``WeakReferer`` to (``WeakValueDictionary`` or ``HybridValueDictionary``)
        The parent weak or hybrid value dictionary.
    """
    __slots__ = ('_parent', )
    def __new__(cls, parent):
        """
        Creates a new ``_WeakValueDictionaryCallback`` instance bound to the given ``WeakValueDictionary`` or
        ``HybridValueDictionary`` instance.
        
        Parameters
        ----------
        parent : ``WeakValueDictionary`` or ``HybridValueDictionary``
            The parent weak or hybrid value dictionary.
        """
        parent = WeakReferer(parent)
        self = object.__new__(cls)
        self._parent = parent
        return self
    
    def __call__(self, reference):
        """
        Called when a value of the respective weak or hybrid value dictionary is garbage collected.
        
        Parameters
        ----------
        reference : ``KeyedReferer``
            Weakreference to the respective object.
        """
        parent = self._parent()
        if parent is None:
            return
        
        if parent._iterating:
            add_to_pending_removals(parent, reference)
        else:
            try:
                dict.__delitem__(parent, reference.key)
            except KeyError:
                pass


class _HybridValueDictionaryKeyIterator(object):
    """
    Key iterator for ``HybridValueDictionary``-s.
    
    Attributes
    ----------
    _parent : ``WeakReferer`` to ``HybridValueDictionary``
        The parent hybrid value dictionary.
    """
    __slots__ = ('_parent',)
    def __init__(self, parent):
        """
        Creates a new ``_HybridValueDictionaryKeyIterator`` instance bound to the given ``HybridValueDictionary``.
        
        Parameters
        ----------
        parent : ``HybridValueDictionary``
            The parent hybrid value dictionary.
        """
        self._parent = parent
    
    def __iter__(self):
        """
        Iterates over a hybrid value dictionary's keys.
        
        This method is a generator.
        
        Yields
        ------
        key : `Any`
        """
        parent = self._parent
        parent._iterating += 1
        
        try:
            for key, (value_weakreferable, value_or_reference) in dict.items(parent):
                if value_weakreferable and (value_or_reference() is None):
                    add_to_pending_removals(parent, value_or_reference)
                    continue
                
                yield key
                continue
        
        finally:
            parent._iterating -= 1
            parent._commit_removals()
    
    def __contains__(self, contains_key):
        """Returns whether the respective ``HybridValueDictionary`` contains the given key."""
        return (contains_key in self._parent)
    
    def __len__(self):
        """Returns the respective ``HybridValueDictionary``'s length."""
        return len(self._parent)


class _HybridValueDictionaryValueIterator(object):
    """
    Value iterator for ``HybridValueDictionary``-s.
    
    Attributes
    ----------
    _parent : ``WeakReferer`` to ``HybridValueDictionary``
        The parent hybrid value dictionary.
    """
    __slots__ = ('_parent',)
    def __init__(self, parent):
        """
        Creates a new ``_HybridValueDictionaryValueIterator`` instance bound to the given ``HybridValueDictionary``.
        
        Parameters
        ----------
        parent : ``HybridValueDictionary``
            The parent hybrid value dictionary.
        """
        self._parent = parent
    
    def __iter__(self):
        """
        Iterates over a hybrid value dictionary's values.
        
        This method is a generator.
        
        Yields
        ------
        value : `Any`
        """
        parent = self._parent
        parent._iterating += 1
        
        try:
            for value_weakreferable, value_or_reference in dict.values(parent):
                if value_weakreferable:
                    value = value_or_reference()
                    if value is None:
                        add_to_pending_removals(parent, value_or_reference)
                        continue
                else:
                    value = value_or_reference
                
                yield value
                continue
        
        finally:
            parent._iterating -=1
            parent._commit_removals()
    
    def __contains__(self, contains_value):
        """Returns whether the respective ``HybridValueDictionary`` contains the given value."""
        parent = self._parent
        for value_weakreferable, value_or_reference in dict.values(parent):
            if value_weakreferable:
                value = value_or_reference()
                if value is None:
                    add_to_pending_removals(parent, value_or_reference)
                    continue
            else:
                value = value_or_reference
            
            if value == contains_value:
                result = True
                break
        else:
            result = False
        
        parent._commit_removals()
        
        return result
    
    def __len__(self):
        """Returns the respective ``HybridValueDictionary``'s length."""
        return len(self._parent)


class _HybridValueDictionaryItemIterator(object):
    """
    Item iterator for ``HybridValueDictionary``-s.
    
    Attributes
    ----------
    _parent : ``WeakReferer`` to ``HybridValueDictionary``
        The parent hybrid value dictionary.
    """
    __slots__ = ('_parent',)
    def __init__(self, parent):
        """
        Creates a new ``_HybridValueDictionaryItemIterator`` instance bound to the given ``HybridValueDictionary``.
        
        Parameters
        ----------
        parent : ``HybridValueDictionary``
            The parent hybrid value dictionary.
        """
        self._parent = parent
    
    def __iter__(self):
        """
        Iterates over a hybrid value dictionary's items.
        
        This method is a generator.
        
        Yields
        ------
        item : `tuple` (`Any`, `Any`)
        """
        parent = self._parent
        parent._iterating += 1
        
        try:
            for key, (value_weakreferable, value_or_reference) in dict.items(parent):
                if value_weakreferable:
                    value = value_or_reference()
                    if value is None:
                        add_to_pending_removals(parent, value_or_reference)
                        continue
                else:
                    value = value_or_reference
                
                yield key, value
                continue
        
        finally:
            parent._iterating -= 1
            parent._commit_removals()
    
    def __contains__(self, contains_item):
        """Returns whether the respective ``HybridValueDictionary`` contains the given item."""
        if not isinstance(contains_item, tuple):
            return False
        
        if len(contains_item) != 2:
            return False
        
        parent = self._parent
        contains_key, contains_value = contains_item
        
        value_pair = dict.get(parent, contains_key)
        if value_pair is None:
            return False
        
        value_weakreferable, value_or_reference = value_pair
        if value_weakreferable:
            value = value_or_reference()
            if value is None:
                if parent._iterating:
                    add_to_pending_removals(parent, value_or_reference)
                else:
                    dict.__delitem__(parent, contains_key)
                
                return False
        else:
            value = value_or_reference
        
        return (value == contains_value)
    
    def __len__(self):
        """Returns the respective ``HybridValueDictionary``'s length."""
        return len(self._parent)


class HybridValueDictionary(dict):
    """
    Hybrid value dictionaries store their's values weakly referenced if applicable.
    
    Attributes
    ----------
    _pending_removals : `None` or `set` of (``KeyedReferer`` or ``WeakHasher``)
        Pending removals of the hybrid value dictionary if applicable.
    _iterating : `int`
        Whether the hybrid value dictionary is iterating and how much times.
    _callback : ``_WeakValueDictionaryCallback``
        Callback added to the ``HybridValueDictionary``'s weak elements.
    
    Class Attributes
    ----------------
    MAX_RERP_ELEMENT_LIMIT : `int` = `50`
        The maximal amount of items to render by ``.__repr__``.
    
    Notes
    -----
    ``HybridValueDictionary`` instances are weakreferable.
    """
    __slots__ = ('__weakref__', '_pending_removals', '_iterating', '_callback')
    
    MAX_RERP_ELEMENT_LIMIT = 50
    
    def _commit_removals(self):
        """
        Commits the pending removals of the hybrid value dictionary if applicable.
        """
        if self._iterating:
            return
        
        pending_removals = self._pending_removals
        if pending_removals is None:
            return
        
        self._pending_removals = None
        
        for value_reference in pending_removals:
            key = value_reference.key
            try:
                value_pair = dict.__getitem__(self, key)
            except KeyError:
                continue
            
            value_weakreferable, value_or_reference = value_pair
            if (not value_weakreferable):
                continue
            
            if (value_or_reference is not value_reference):
                continue
            
            try:
                dict.__delitem__(self, key)
            except KeyError:
                pass
    
    # __class__ -> same
    
    def __contains__(self, contains_key):
        """Returns whether the hybrid value dictionary contains the given key."""
        value_pair = dict.get(self, contains_key, None)
        if value_pair is None:
            return False
        
        value_weakreferable, value_or_reference = value_pair
        
        if value_weakreferable:
            if value_or_reference() is None:
                if self._iterating:
                    add_to_pending_removals(self, value_or_reference)
                else:
                    dict.__delitem__(self, contains_key)
                
                return False
        
        return True
    
    # __delattr__ -> same
    # __delitem__ -> same
    # __dir__ -> same
    # __doc__ -> same
    # __eq__ -> same
    # __format__ -> same
    # __ge__ -> same
    # __getattribute__ -> same
    
    def __getitem__(self, key):
        """Gets the value of the hybrid value dictionary which matches the given key."""
        value_weakreferable, value_or_reference = dict.__getitem__(self, key)
        if value_weakreferable:
            value = value_or_reference()
            if value is None:
                if self._iterating:
                    add_to_pending_removals(self, value_or_reference)
                else:
                    dict.__delitem__(self, key)
                
                raise KeyError(key)
        else:
            value = value_or_reference
        
        return value
    
    # __gt__ -> same
    # __hash__ -> same
    
    def __init__(self, iterable=None):
        """
        Creates a new ``HybridValueDictionary`` instance from the given iterable.
        
        Parameters
        ----------
        iterable : `iterable`, Optional
            Iterable to update the created dictionary with.
        """
        self._pending_removals = None
        self._iterating = 0
        self._callback = _WeakValueDictionaryCallback(self)
        if (iterable is not None):
            self.update(iterable)
    
    # __init_subclass__ -> same
    
    def __iter__(self):
        """Returns a ``_HybridValueDictionaryKeyIterator`` iterating over the hybrid value dictionary's keys."""
        return iter(_HybridValueDictionaryKeyIterator(self))
    
    # __le__ -> same
    
    def __len__(self):
        """Returns the length of the hybrid value dictionary."""
        length = dict.__len__(self)
        pending_removals = self._pending_removals
        if (pending_removals is not None):
            length -= len(pending_removals)
        
        return length
    
    # __lt__ -> same
    # __ne__ -> same
    # __new__ -> same
    # __reduce__ -> we do not care
    # __reduce_ex__ -> we do not care
    
    def __repr__(self):
        """Returns the representation of the hybrid value dictionary."""
        result = [self.__class__.__name__, '({']
        if len(self):
            limit = self.MAX_RERP_ELEMENT_LIMIT
            collected = 0
            for key, (value_weakreferable, value_or_reference) in dict.items(self):
                if value_weakreferable:
                    value = value_or_reference()
                    if value is None:
                        add_to_pending_removals(self, value_or_reference)
                        continue
                else:
                    value = value_or_reference
                
                result.append(repr(key))
                result.append(': ')
                result.append(repr(value))
                result.append(', ')
                
                collected += 1
                if collected != limit:
                    continue
                
                leftover = len(self) - collected
                if leftover:
                    result.append('...}, ')
                    result.append(str(leftover))
                    result.append(' truncated)')
                else:
                    result[-1] = '})'
                break
            else:
                result[-1] = '})'
            
            self._commit_removals()
        else:
            result.append('})')
        
        return ''.join(result)
    
    #__setattr__ -> same
    
    def __setitem__(self, key, value):
        """Adds the given `key` - `value` pair to the hybrid value dictionary."""
        if is_weakreferable(value):
            value_weakreferable = True
            value_or_reference = KeyedReferer(value, self._callback, key)
        else:
            value_weakreferable = False
            value_or_reference = value
        
        dict.__setitem__(self, key, (value_weakreferable, value_or_reference), )
    
    # __sizeof__ -> same
    
    __str__ = __repr__
    
    # __subclasshook__ -> same
    
    def clear(self):
        """
        Clears the hybrid value dictionary.
        """
        dict.clear(self)
        self._pending_removals = None
    
    def copy(self):
        """
        Copies the hybrid value dictionary.
        
        Returns
        -------
        new : ``HybridValueDictionary``
        """
        new = dict.__new__(type(self))
        new._iterating = 0
        new._pending_removals = None
        callback = _WeakValueDictionaryCallback(new)
        new._callback = callback
        
        for key, (value_weakreferable, value_or_reference) in dict.items(self):
            if value_weakreferable:
                value = value_or_reference()
                if (value is None):
                    add_to_pending_removals(self, value_or_reference)
                    continue
                
                value_or_reference = KeyedReferer(value, callback, key)
            
            dict.__setitem__(new, key, (value_weakreferable, value_or_reference))
            continue
        
        self._commit_removals()
        
        return new
    
    def get(self, key, default=None):
        """
        Gets the value of the hybrid value dictionary which matches the given key.
        
        Parameters
        ----------
        key : `Any`
            A key to match.
        default : `Any`, Optional
            Default value to return if the given `key` could not be matched. Defaults to `None`.
        
        Returns
        -------
        value : `Any` or `default`
            The key's matched value. If no value was matched returns the `default` value.
        """
        value_pair = dict.get(self, key, default)
        if value_pair is default:
            return default
        
        value_weakreferable, value_or_reference = value_pair
        
        if value_weakreferable:
            value = value_or_reference()
            if value is None:
                if self._iterating:
                    add_to_pending_removals(self, value_or_reference)
                else:
                    dict.__delitem__(self, key)
                
                return default
        else:
            value = value_or_reference
        
        return value
    
    def items(self):
        """
        Returns item iterator for the hybrid value dictionary.
        
        Returns
        -------
        item_iterator : ``_HybridValueDictionaryItemIterator``
        """
        return _HybridValueDictionaryItemIterator(self)
    
    def keys(self):
        """
        Returns key iterator for the hybrid value dictionary.
        
        Returns
        -------
        key_iterator : ``_HybridValueDictionaryKeyIterator``
        """
        return _HybridValueDictionaryKeyIterator(self)
    
    # Need goto for better code-style
    def pop(self, key, default=_spaceholder):
        """
        Pops the value of the hybrid value dictionary which matches the given key.
        
        Parameters
        ----------
        key : `Any`
            A key to match.
        default : `Any`, Optional
            Default value to return if the given `key` could not be matched.
        
        Returns
        -------
        value : `Any` or `default`
            The key's matched value. If no value was matched and `default` value is given, then returns that.
        
        Raises
        ------
        KeyError
            If `key` could not be matched and `default` value is was not given either.
        """
        value_pair = dict.pop(self, key, _spaceholder)
        
        if (value_pair is not default):
            value_weakreferable, value_or_reference = value_pair
            
            if (not value_weakreferable):
                return value_or_reference
            
            value = value_or_reference()
            if (value is not None):
                return value
        
        if default is _spaceholder:
            raise KeyError(key)
        
        return default
    
    def popitem(self):
        """
        Pops an item of the hybrid value dictionary.
        
        Returns
        -------
        item : `tuple` (`Any`, `Any`)
        
        Raises
        ------
        KeyError
            If the hybrid value dictionary is empty.
        """
        while dict.__len__(self):
            key, (value_weakreferable, value_or_reference) = dict.popitem(self)
            if value_weakreferable:
                value = value_or_reference()
                if value is None:
                    continue
            else:
                value = value_or_reference
                
            return key, value
        
        raise KeyError('popitem(): dictionary is empty.')
    
    def setdefault(self, key, default=None):
        """
        Returns the value for the given `key`.
        
        If the `key` is not present in the hybrid value dictionary, then set's the given `default` value as it.
        
        Parameters
        ----------
        key : `Any`
            The key to match.
        default : `Any`, Optional
            Default value to set and return if `key` is not present in the hybrid value dictionary.
        
        Returns
        -------
        value : `default` or `Any`
            The matched value, or `default` if none.
        """
        value_pair = dict.get(self, key, None)
        if (value_pair is not None):
            value_weakreferable, value_or_reference = value_pair
            if (not value_weakreferable):
                return value_or_reference
            
            value = value_or_reference()
            if (value is not None):
                return value
        
        self[key] = default
        return default
    
    def update(self, iterable):
        """
        Updates the hybrid value dictionary with the given iterable's elements.
        
        Parameters
        ----------
        iterable : `iterable`
            Iterable to extend the hybrid value dictionary with.
            
            Can be given as an object, which:
            - supports `.items` iterator.
            - supports `.keys` and `.__getitem__`.
            - is `iterable` and each iteration returns a sequence with 2 elements.
        
        Raises
        ------
        TypeError
            The given `iterable` is not `iterable`.
        ValueError
            The the given `iterable` sot supports neither `.items` or (`.keys` and `.__getitem__`) and one of it's
            element's length is not `2`.
        """
        iterable_type = iterable.__class__
        if hasattr(iterable_type, 'items'):
            for key, value in iterable.items():
                self[key] = value
            return
        
        if hasattr(iterable_type, 'keys') and hasattr(iterable_type, '__getitem__'):
            for key in iterable.keys():
                value = iterable[key]
                self[key] = value
            return
        
        if hasattr(iterable_type, '__iter__'):
            index = - 1
            for item in iterable:
                index += 1
                
                try:
                    iterator = iter(item)
                except TypeError:
                    raise TypeError(f'Cannot convert dictionary update sequence element #{index} to a sequence.') \
                        from None
                
                try:
                    key = next(iterator)
                except StopIteration:
                    raise ValueError(f'Dictionary update sequence element #{index} has length {0}; 2 is required.') \
                        from None
                
                try:
                    value = next(iterator)
                except StopIteration:
                    raise ValueError(f'Dictionary update sequence element #{index} has length {1}; 2 is required.') \
                        from None
                
                try:
                    next(iterator)
                except StopIteration:
                    self[key] = value
                    continue
                
                length = 3
                for _ in iterator:
                    length += 1
                    if length > 9000:
                        break
                
                if length > 9000:
                    length = 'OVER 9000!'
                else:
                    length = repr(length)
                
                raise ValueError(f'Dictionary update sequence element #{index} has length {length}; 2 is required.')
            return
        
        raise TypeError(f'{iterable_type.__name__!r} object is not iterable.')
    
    def values(self):
        """
        Returns value iterator for the hybrid value dictionary.
        
        Returns
        -------
        value_iterator : ``_HybridValueDictionaryValueIterator``
        """
        return _HybridValueDictionaryValueIterator(self)


class _WeakValueDictionaryKeyIterator(object):
    """
    Key iterator for ``WeakValueDictionary``-s.
    
    Attributes
    ----------
    _parent : ``WeakReferer`` to ``WeakValueDictionary``
        The parent weak value dictionary.
    """
    __slots__ = ('_parent',)
    def __init__(self, parent):
        """
        Creates a new ``_WeakValueDictionaryKeyIterator`` instance bound to the given ``WeakValueDictionary``.
        
        Parameters
        ----------
        parent : ``WeakValueDictionary``
            The parent weak value dictionary.
        """
        self._parent = parent
    
    def __iter__(self):
        """
        Iterates over a weak value dictionary's keys.
        
        This method is a generator.
        
        Yields
        ------
        key : `Any`
        """
        parent = self._parent
        parent._iterating += 1
        
        try:
            for key, value_reference in dict.items(parent):
                if (value_reference() is None):
                    add_to_pending_removals(parent, value_reference)
                    continue
                
                yield key
                continue
        
        finally:
            parent._iterating -= 1
            parent._commit_removals()
    
    def __contains__(self, key):
        """Returns whether the respective ``WeakValueDictionary`` contains the given key."""
        return (key in self._parent)
    
    def __len__(self):
        """Returns the respective ``WeakValueDictionary``'s length."""
        return len(self._parent)


class _WeakValueDictionaryValueIterator(object):
    """
    Value iterator for ``WeakValueDictionary``-s.
    
    Attributes
    ----------
    _parent : ``WeakReferer`` to ``WeakValueDictionary``
        The parent weak value dictionary.
    """
    __slots__ = ('_parent',)
    def __init__(self, parent):
        """
        Creates a new ``_WeakValueDictionaryValueIterator`` instance bound to the given ``WeakValueDictionary``.
        
        Parameters
        ----------
        parent : ``WeakValueDictionary``
            The parent weak value dictionary.
        """
        self._parent = parent
    
    def __iter__(self):
        """
        Iterates over a weak value dictionary's values.
        
        This method is a generator.
        
        Yields
        ------
        value : `Any`
        """
        parent = self._parent
        parent._iterating += 1
        
        try:
            for value_reference in dict.values(parent):
                value = value_reference()
                if (value is None):
                    add_to_pending_removals(parent, value_reference)
                    continue
                
                yield value
                continue
        
        finally:
            parent._iterating -= 1
            parent._commit_removals()
    
    def __contains__(self, contains_value):
        """Returns whether the respective ``WeakValueDictionary`` contains the given value."""
        parent = self._parent
        for value_reference in dict.values(parent):
            value = value_reference()
            if (value is None):
                add_to_pending_removals(parent, value_reference)
                continue
            
            if value == contains_value:
                result = True
                break
        
        else:
            result = False
        
        parent._commit_removals()
        
        return result
    
    def __len__(self):
        """Returns the respective ``WeakValueDictionary``'s length."""
        return len(self._parent)


class _WeakValueDictionaryItemIterator(object):
    """
    Item iterator for ``WeakValueDictionary``-s.
    
    Attributes
    ----------
    _parent : ``WeakReferer`` to ``WeakValueDictionary``
        The parent weak value dictionary.
    """
    __slots__ = ('_parent',)
    def __init__(self, parent):
        """
        Creates a new ``_WeakValueDictionaryItemIterator`` instance bound to the given ``WeakValueDictionary``.
        
        Parameters
        ----------
        parent : ``WeakValueDictionary``
            The parent weak value dictionary.
        """
        self._parent = parent
    
    def __iter__(self):
        """
        Iterates over a weak value dictionary's items.
        
        This method is a generator.
        
        Yields
        ------
        item : `tuple` (`Any`, `Any`)
        """
        parent = self._parent
        parent._iterating += 1
        
        try:
            for key, value_reference in dict.items(parent):
                value = value_reference()
                if (value is None):
                    add_to_pending_removals(parent, value_reference)
                    continue
                
                yield key, value
                continue
        
        finally:
            parent._iterating -= 1
            parent._commit_removals()
    
    def __contains__(self, contains_item):
        """Returns whether the respective ``WeakValueDictionary`` contains the given item."""
        if not isinstance(contains_item, tuple):
            return False
        
        if len(contains_item) != 2:
            return False
        
        parent = self._parent
        
        contains_key, contains_value = contains_item
        
        value_reference = dict.get(parent, contains_key)
        if value_reference is None:
            return False
        
        value = value_reference()
        if value is None:
            if parent._iterating:
                add_to_pending_removals(parent, value_reference)
            else:
                dict.__delitem__(parent, contains_key)
            
            return False
        
        return (value == contains_value)
    
    def __len__(self):
        """Returns the respective ``WeakValueDictionary``'s length."""
        return len(self._parent)


class WeakValueDictionary(dict):
    """
    Weak value dictionary, which stores it's values weakly referenced.
    
    Attributes
    ----------
    _pending_removals : `None` or `set` of (``KeyedReferer`` or ``WeakHasher``)
        Pending removals of the weak value dictionary if applicable.
    _iterating : `int`
        Whether the weak value dictionary is iterating and how much times.
    _callback : ``_WeakValueDictionaryCallback``
        Callback added to the ``WeakValueDictionary``'s weak values.
    
    Class Attributes
    ----------------
    MAX_RERP_ELEMENT_LIMIT : `int` = `50`
        The maximal amount of items to render by ``.__repr__``.
    
    Notes
    -----
    ``WeakValueDictionary`` instances are weakreferable.
    """
    __slots__ = ('__weakref__', '_pending_removals', '_iterating', '_callback')
    
    MAX_RERP_ELEMENT_LIMIT = 50
    
    def _commit_removals(self):
        """
        Commits the pending removals of the weak value dictionary if applicable.
        """
        if self._iterating:
            return
        
        pending_removals = self._pending_removals
        if pending_removals is None:
            return
        
        self._pending_removals = None
        
        for value_reference in pending_removals:
            key = value_reference.key
            try:
                actual_value_reference = dict.__getitem__(self, key)
            except KeyError:
                continue
            
            if (actual_value_reference is not value_reference):
                continue
            
            try:
                dict.__delitem__(self, key)
            except KeyError:
                pass
    
    # __class__ -> same
    
    def __contains__(self, key):
        """Returns whether the weak value dictionary contains the given key."""
        value_reference = dict.get(self, key, None)
        if value_reference is None:
            return False
        
        value = value_reference()
        if (value is not None):
            return True
        
        if self._iterating:
            add_to_pending_removals(self, value_reference)
        else:
            dict.__delitem__(self, key)
        
        return False
    
    # __delattr__ -> same
    # __delitem__ -> same
    # __dir__ -> same
    # __doc__ -> same
    # __eq__ -> same
    # __format__ -> same
    # __ge__ -> same
    # __getattribute__ -> same
    
    def __getitem__(self, key):
        """Gets the value of the weak value dictionary which matches the given key."""
        value_reference = dict.__getitem__(self, key)
        value = value_reference()
        if (value is not None):
            return value
        
        if self._iterating:
            add_to_pending_removals(self, value_reference)
        else:
            dict.__delitem__(self, key)
        
        raise KeyError(key)
    
    # __gt__ -> same
    # __hash__ -> same
    
    def __init__(self, iterable=None):
        """
        Creates a new ``WeakValueDictionary`` instance from the given iterable.
        
        Parameters
        ----------
        iterable : `iterable`, Optional
            Iterable to update the created dictionary with.
        """
        self._pending_removals = None
        self._iterating = 0
        self._callback = _WeakValueDictionaryCallback(self)
        if (iterable is not None):
            self.update(iterable)
    
    # __init_subclass__ -> same
    
    def __iter__(self):
        """Returns a ``_WeakValueDictionaryKeyIterator`` iterating over the weak value dictionary's keys."""
        return iter(_WeakValueDictionaryKeyIterator(self))
    
    # __le__ -> same
    
    def __len__(self):
        """Returns the length of the weak value dictionary."""
        length = dict.__len__(self)
        pending_removals = self._pending_removals
        if (pending_removals is not None):
            length -= len(pending_removals)
        
        return length
    
    # __lt__ -> same
    # __ne__ -> same
    # __new__ -> same
    # __reduce__ -> we do not care
    # __reduce_ex__ -> we do not care
    
    def __repr__(self):
        """Returns the representation of the weak value dictionary."""
        result = [self.__class__.__name__, '({']
        
        if len(self):
            limit = self.MAX_RERP_ELEMENT_LIMIT
            collected = 0
            for key, value_reference in dict.items(self):
                value = value_reference()
                if (value is None):
                    add_to_pending_removals(self, value_reference)
                    continue
                
                result.append(repr(key))
                result.append(': ')
                result.append(repr(value))
                result.append(', ')
                
                collected +=1
                if collected != limit:
                    continue
                
                leftover = len(self) - collected
                if leftover:
                    result.append('...}, ')
                    result.append(str(leftover))
                    result.append(' truncated)')
                else:
                    result[-1] = '})'
                break
            else:
                result[-1] = '})'
            
            self._commit_removals()
        else:
            result.append('})')
        
        return ''.join(result)
    
    #__setattr__ -> same
    
    def __setitem__(self, key, value):
        """Adds the given `key` - `value` pair to the weak value dictionary."""
        dict.__setitem__(self, key, KeyedReferer(value, self._callback, key))
    
    # __sizeof__ -> same
    
    __str__ = __repr__
    
    # __subclasshook__ -> same
    
    def clear(self):
        """
        Clears the weak value dictionary.
        """
        dict.clear(self)
        self._pending_removals = None
    
    def copy(self):
        """
        Copies the weak value dictionary.
        
        Returns
        -------
        new : ``WeakValueDictionary``
        """
        new = dict.__new__(type(self))
        new._pending_removals = None
        callback = _WeakValueDictionaryCallback(new)
        new._callback = callback
        
        for key, value_reference in dict.items(self):
            value = value_reference()
            if value is None:
                add_to_pending_removals(self, value_reference)
                continue
            
            dict.__setitem__(new, key, KeyedReferer(value, callback, key))
            continue
        
        self._commit_removals()
        
        return new
    
    def get(self, key, default=None):
        """
        Gets the value of the weak value dictionary which matches the given key.
        
        Parameters
        ----------
        key : `Any`
            A key to match.
        default : `Any`, Optional
            Default value to return if the given `key` could not be matched. Defaults to `None`.
        
        Returns
        -------
        value : `Any` or `default`
            The key's matched value. If no value was matched returns the `default` value.
        """
        value_reference = dict.get(self, key, default)
        if value_reference is default:
            return default
        
        value = value_reference()
        if (value is not None):
            return value
        
        if self._iterating:
            add_to_pending_removals(self, value_reference)
        else:
            dict.__delitem__(self, key)
        
        return default
    
    def items(self):
        """
        Returns item iterator for the weak value dictionary.
        
        Returns
        -------
        item_iterator : ``_WeakValueDictionaryItemIterator``
        """
        return _WeakValueDictionaryItemIterator(self)
    
    def keys(self):
        """
        Returns key iterator for the weak value dictionary.
        
        Returns
        -------
        key_iterator : ``_WeakValueDictionaryKeyIterator``
        """
        return _WeakValueDictionaryKeyIterator(self)
    
    def pop(self, key, default=_spaceholder):
        """
        Pops the value of the weak value dictionary which matches the given key.
        
        Parameters
        ----------
        key : `Any`
            A key to match.
        default : `Any`, Optional
            Default value to return if the given `key` could not be matched.
        
        Returns
        -------
        value : `Any` or `default`
            The key's matched value. If no value was matched and `default` value is given, then returns that.
        
        Raises
        ------
        KeyError
            If `key` could not be matched and `default` value is was not given either.
        """
        value_reference = dict.pop(self, key, _spaceholder)
        if (value_reference is not _spaceholder):
            value = value_reference()
            if (value is not None):
                return value
        
        if default is _spaceholder:
            raise KeyError(key)
        
        return default
    
    def popitem(self):
        """
        Pops an item of the weak value dictionary.
        
        Returns
        -------
        item : `tuple` (`Any`, `Any`)
        
        Raises
        ------
        KeyError
            If the weak value dictionary is empty.
        """
        while dict.__len__(self):
            key, value_reference = dict.popitem(self)
            value = value_reference()
            if (value is not None):
                return key, value
            
            continue
        
        raise KeyError('popitem(): dictionary is empty.')
    
    def setdefault(self, key, default):
        """
        Returns the value for the given `key`.
        
        If the `key` is not present in the weak value dictionary, then set's the given `default` value as it.
        
        Parameters
        ----------
        key : `Any`
            The key to match.
        default : `Any`, Optional
            Default value to set and return if `key` is not present in the weak value dictionary.
        
        Returns
        -------
        value : `default` or `Any`
            The matched value, or `default` if none.
        """
        value_reference = dict.get(self, key, _spaceholder)
        if (value_reference is not _spaceholder):
            value = value_reference()
            if (value is not None):
                return value
        
        self[key] = default
        return default
    
    def update(self, iterable):
        """
        Updates the weak value dictionary with the given iterable's elements.
        
        Parameters
        ----------
        iterable : `iterable`
            Iterable to extend the weak value dictionary with.
            
            Can be given as an object, which:
            - supports `.items` iterator.
            - supports `.keys` and `.__getitem__`.
            - is `iterable` and each iteration returns a sequence with 2 elements.
        
        Raises
        ------
        TypeError
            The given `iterable` is not `iterable`.
        ValueError
            The the given `iterable` sot supports neither `.items` or (`.keys` and `.__getitem__`) and one of it's
            element's length is not `2`.
        """
        iterable_type = iterable.__class__
        if hasattr(iterable_type, 'items'):
            for key, value in iterable.items():
                self[key] = value
            return
        
        if hasattr(iterable_type, 'keys') and hasattr(iterable_type, '__getitem__'):
            for key in iterable.keys():
                value = iterable[key]
                self[key] = value
            return
        
        if hasattr(iterable_type, '__iter__'):
            index = -1
            for item in iterable:
                index += 1
                
                try:
                    iterator = iter(item)
                except TypeError:
                    raise TypeError(f'Cannot convert dictionary update sequence element #{index} to a sequence.') \
                        from None
                
                try:
                    key = next(iterator)
                except StopIteration:
                    raise ValueError(f'Dictionary update sequence element #{index} has length {0}; 2 is required.') \
                        from None
                
                try:
                    value = next(iterator)
                except StopIteration:
                    raise ValueError(f'Dictionary update sequence element #{index} has length {1}; 2 is required.') \
                        from None
                
                try:
                    next(iterator)
                except StopIteration:
                    self[key] = value
                    continue
                
                length = 3
                for _ in iterator:
                    length += 1
                    if length > 9000:
                        break
                
                if length > 9000:
                    length = 'OVER 9000!'
                else:
                    length = repr(length)
                
                raise ValueError(f'Dictionary update sequence element #{index} has length {length}; 2 is required.')
            return
        
        raise TypeError(f'{iterable_type.__name__!r} object is not iterable')
    
    def values(self):
        """
        Returns value iterator for the weak value dictionary.
        
        Returns
        -------
        value_iterator : ``_WeakValueDictionaryValueIterator``
        """
        return _WeakValueDictionaryValueIterator(self)


class _WeakKeyDictionaryCallback(object):
    """
    Callback used by ``WeakKeyDictionary``-s.
    
    Attributes
    ----------
    _parent : ``WeakReferer`` to ``WeakValueDictionary``
        The parent weak key dictionary.
    """
    __slots__ = ('_parent', )
    def __new__(cls, parent):
        """
        Creates a new ``_WeakKeyDictionaryCallback`` instance bound to the given ``WeakKeyDictionary`` instance.
        
        Parameters
        ----------
        parent : ``WeakKeyDictionary``
            The parent weak key dictionary.
        """
        parent = WeakReferer(parent)
        self = object.__new__(cls)
        self._parent = parent
        return self
    
    def __call__(self, reference):
        """
        Called when a key of the respective weak key dictionary is garbage collected.
        
        Parameters
        ----------
        reference : ``WeakReferer``
            Weakreference to the respective object.
        """
        parent = self._parent()
        if parent is None:
            return
        
        if parent._iterating:
            add_to_pending_removals(parent, reference)
        else:
            try:
                dict.__delitem__(parent, reference)
            except KeyError:
                pass



class _WeakKeyDictionaryKeyIterator(object):
    """
    Key iterator for ``WeakKeyDictionary``-s.
    
    Attributes
    ----------
    _parent : ``WeakReferer`` to ``WeakKeyDictionary``
        The parent weak key dictionary.
    """
    __slots__ = ('_parent',)
    def __init__(self, parent):
        """
        Creates a new ``_WeakKeyDictionaryKeyIterator`` instance bound to the given ``WeakKeyDictionary``.
        
        Parameters
        ----------
        parent : ``WeakKeyDictionary``
            The parent weak key dictionary.
        """
        self._parent = parent
    
    def __iter__(self):
        """
        Iterates over a weak key dictionary's keys.
        
        This method is a generator.
        
        Yields
        ------
        key : `Any`
        """
        parent = self._parent
        parent._iterating += 1
        
        try:
            for key_reference in dict.keys(parent):
                key = key_reference()
                if (key is None):
                    add_to_pending_removals(parent, key_reference)
                    continue
                
                yield key
                continue
        
        finally:
            parent._iterating -= 1
            parent._commit_removals()
    
    def __contains__(self, contains_key):
        """Returns whether the respective ``WeakKeyDictionary`` contains the given key."""
        return (contains_key in self._parent)
    
    def __len__(self):
        """Returns the respective ``WeakKeyDictionary``'s length."""
        return len(self._parent)


class _WeakKeyDictionaryValueIterator(object):
    """
    Value iterator for ``WeakKeyDictionary``-s.
    
    Attributes
    ----------
    _parent : ``WeakReferer`` to ``WeakKeyDictionary``
        The parent weak key dictionary.
    """
    __slots__ = ('_parent',)
    def __init__(self, parent):
        """
        Creates a new ``_WeakKeyDictionaryValueIterator`` instance bound to the given ``WeakKeyDictionary``.
        
        Parameters
        ----------
        parent : ``WeakKeyDictionary``
            The parent weak key dictionary.
        """
        self._parent = parent
    
    def __iter__(self):
        """
        Iterates over a weak key dictionary's values.
        
        This method is a generator.
        
        Yields
        ------
        value : `Any`
        """
        parent = self._parent
        parent._iterating += 1
        
        try:
            for key_reference, value in dict.items(parent):
                if (key_reference() is None):
                    add_to_pending_removals(parent, key_reference)
                    continue
                
                yield value
                continue
        
        finally:
            parent._iterating -= 1
            parent._commit_removals()
    
    def __contains__(self, contains_value):
        """Returns whether the respective ``WeakKeyDictionary`` contains the given value."""
        parent = self._parent
        
        for key_reference, value in dict.items(parent):
            if (key_reference() is None):
                add_to_pending_removals(parent, key_reference)
                continue
            
            if value == contains_value:
                result = True
                break
        
        else:
            result = False
        
        parent._commit_removals()
        
        return result
    
    def __len__(self):
        """Returns the respective ``WeakKeyDictionary``'s length."""
        return len(self._parent)


class _WeakKeyDictionaryItemIterator(object):
    """
    Item iterator for ``WeakKeyDictionary``-s.
    
    Attributes
    ----------
    _parent : ``WeakReferer`` to ``WeakKeyDictionary``
        The parent weak key dictionary.
    """
    __slots__ = ('_parent',)
    def __init__(self, parent):
        """
        Creates a new ``_WeakKeyDictionaryItemIterator`` instance bound to the given ``WeakKeyDictionary``.
        
        Parameters
        ----------
        parent : ``WeakKeyDictionary``
            The parent weak key dictionary.
        """
        self._parent = parent
    
    def __iter__(self):
        """
        Iterates over a weak key dictionary's items.
        
        This method is a generator.
        
        Yields
        ------
        item : `tuple` (`Any`, `Any`)
        """
        parent = self._parent
        parent._iterating += 1
        
        try:
            for key_reference, value in dict.items(parent):
                key = key_reference()
                if (key is None):
                    add_to_pending_removals(parent, key_reference)
                    continue
                
                yield key, value
                continue
        
        finally:
            parent._iterating -= 1
            parent._commit_removals()
    
    def __contains__(self, contains_item):
        """Returns whether the respective ``WeakKeyDictionary`` contains the given item."""
        if not isinstance(contains_item, tuple):
            return False
        
        if len(contains_item) != 2:
            return False
        
        contains_key, contains_value = contains_item
        
        try:
            contains_key_reference = WeakReferer(contains_key)
        except TypeError:
            return False
        
        value = dict.get(self._parent, contains_key_reference)
        if value is None:
            return False
        
        return (value == contains_value)
    
    def __len__(self):
        """Returns the respective ``WeakKeyDictionary``'s length."""
        return len(self._parent)

class WeakKeyDictionary(dict):
    """
    Weak key dictionary, which stores it's keys weakly referenced.
    
    Attributes
    ----------
    _pending_removals : `None` or `set` of ``WeakReferer``
        Pending removals of the weak key dictionary if applicable.
    _iterating : `int`
        Whether the weak key dictionary is iterating and how much times.
    _callback : ``_WeakValueDictionaryCallback``
        Callback added to the ``WeakKeyDictionary``'s weak keys.
    
    Class Attributes
    ----------------
    MAX_RERP_ELEMENT_LIMIT : `int` = `50`
        The maximal amount of items to render by ``.__repr__``.
    
    Notes
    -----
    ``WeakKeyDictionary`` instances are weakreferable.
    """
    __slots__ = ('__weakref__', '_pending_removals', '_iterating', '_callback')
    
    MAX_RERP_ELEMENT_LIMIT = 50
    
    def _commit_removals(self):
        """
        Commits the pending removals of the weak key dictionary if applicable.
        """
        if self._iterating:
            return
        
        pending_removals = self._pending_removals
        if pending_removals is None:
            return
        
        self._pending_removals = None
        
        for key_reference in pending_removals:
            try:
                dict.__delitem__(self, key_reference)
            except KeyError:
                return
    
    # __class__ -> same
    
    def __contains__(self, key):
        """Returns whether the weak key dictionary contains the given key."""
        try:
            key = WeakReferer(key)
        except TypeError:
            return False
        
        return dict.__contains__(self, key)
    
    # __delattr__ -> same
    
    def __delitem__(self, key):
        """Deletes the value of the weak key dictionary which matches the given key."""
        dict.__delitem__(self, WeakReferer(key))
    
    # __dir__ -> same
    # __doc__ -> same
    # __eq__ -> same
    # __format__ -> same
    # __ge__ -> same
    # __getattribute__ -> same
    
    def __getitem__(self, key):
        """Gets the value of the weak key dictionary which matches the given key."""
        return dict.__getitem__(self, WeakReferer(key))
    
    # __gt__ -> same
    # __hash__ -> same
    
    def __init__(self, iterable=None):
        """
        Creates a new ``WeakKeyDictionary`` instance from the given iterable.
        
        Parameters
        ----------
        iterable : `iterable`, Optional
            Iterable to update the created dictionary with.
        """
        self._pending_removals = None
        self._iterating = 0
        self._callback = _WeakKeyDictionaryCallback(self)
        if (iterable is not None):
            self.update(iterable)
    
    # __init_subclass__ -> same
    
    def __iter__(self):
        """Returns a ``_WeakKeyDictionaryKeyIterator`` iterating over the weak key dictionary's keys."""
        return iter(_WeakKeyDictionaryKeyIterator(self))
    
    # __le__ -> same
    
    def __len__(self):
        """Returns the length of the weak key dictionary."""
        length = dict.__len__(self)
        pending_removals = self._pending_removals
        if (pending_removals is not None):
            length -= len(pending_removals)
        
        return length
    
    # __lt__ -> same
    # __ne__ -> same
    # __new__ -> same
    # __reduce__ -> we do not care
    # __reduce_ex__ -> we do not care
    
    def __repr__(self):
        """Returns the representation of the weak key dictionary."""
        result = [self.__class__.__name__, '({']
        
        if len(self):
            limit = self.MAX_RERP_ELEMENT_LIMIT
            collected = 0
            for key_reference, value in dict.items(self):
                key = key_reference()
                if (key is None):
                    add_to_pending_removals(self, key_reference)
                    continue
                
                result.append(repr(key))
                result.append(': ')
                result.append(repr(value))
                result.append(', ')
                
                collected += 1
                if collected != limit:
                    continue
                
                leftover = len(self) - collected
                if leftover:
                    result.append('...}, ')
                    result.append(str(leftover))
                    result.append(' truncated)')
                else:
                    result[-1] = '})'
                break
            else:
                result[-1] = '})'
            
            self._commit_removals()
            
        else:
            result.append('})')
        
        return ''.join(result)
    
    #__setattr__ -> same
    
    def __setitem__(self, key, value):
        """Adds the given `key` - `value` pair to the weak key dictionary."""
        dict.__setitem__(self, WeakReferer(key, self._callback), value)
    
    # __sizeof__ -> same
    
    __str__ = __repr__
    
    # __subclasshook__ -> same
    
    def clear(self):
        """
        Clears the weak key dictionary.
        """
        dict.clear(self)
        self._pending_removals = None
    
    def copy(self):
        """
        Copies the weak key dictionary.
        
        Returns
        -------
        new : ``WeakValueDictionary``
        """
        new = dict.__new__(type(self))
        new._pending_removals = None
        callback = _WeakKeyDictionaryCallback(new)
        new._callback = callback
        
        for key_reference, value in dict.items(self):
            key = key_reference()
            if key is None:
                add_to_pending_removals(self, key_reference)
                continue
            
            dict.__setitem__(new, WeakReferer(key, callback), value)
            continue
        
        self._commit_removals()
        
        return new
    
    def get(self, key, default=None):
        """
        Gets the value of the weak key dictionary which matches the given key.
        
        Parameters
        ----------
        key : `Any`
            A key to match.
        default : `Any`, Optional
            Default value to return if the given `key` could not be matched. Defaults to `None`.
        
        Returns
        -------
        value : `Any` or `default`
            The key's matched value. If no value was matched returns the `default` value.
        """
        return dict.get(self, WeakReferer(key), default)
    
    def items(self):
        """
        Returns item iterator for the weak key dictionary.
        
        Returns
        -------
        item_iterator : ``_WeakKeyDictionaryItemIterator``
        """
        return _WeakKeyDictionaryItemIterator(self)
    
    def keys(self):
        """
        Returns key iterator for the weak key dictionary.
        
        Returns
        -------
        key_iterator : ``_WeakKeyDictionaryKeyIterator``
        """
        return _WeakKeyDictionaryKeyIterator(self)
    
    def pop(self, key, default=_spaceholder):
        """
        Pops the value of the weak key dictionary which matches the given key.
        
        Parameters
        ----------
        key : `Any`
            A key to match.
        default : `Any`, Optional
            Default value to return if the given `key` could not be matched.
        
        Returns
        -------
        value : `Any` or `default`
            The key's matched value. If no value was matched and `default` value is given, then returns that.
        
        Raises
        ------
        KeyError
            If `key` could not be matched and `default` value is was not given either.
        """
        try:
            key_reference = WeakReferer(key)
        except TypeError:
            raise KeyError(key) from None
        
        value = dict.pop(self, key_reference, _spaceholder)
        if (value is not _spaceholder):
            return value
        
        if default is _spaceholder:
            raise KeyError(key)
        
        return default
    
    def popitem(self):
        """
        Pops an item of the key value dictionary.
        
        Returns
        -------
        item : `tuple` (`Any`, `Any`)
        
        Raises
        ------
        KeyError
            If the weak key dictionary is empty.
        """
        while dict.__len__(self):
            key_reference, value = dict.popitem(self)
            key = key_reference()
            
            if (key is not None):
                return key, value
            
            if self._iterating:
                add_to_pending_removals(self, key_reference)
            else:
                dict.__delitem__(self, key_reference)
            
            continue
        
        raise KeyError('popitem(): dictionary is empty.')
    
    def setdefault(self, key, default=None):
        """
        Returns the value for the given `key`.
        
        If the `key` is not present in the weak key dictionary, then set's the given `default` value as it.
        
        Parameters
        ----------
        key : `Any`
            The key to match.
        default : `Any`, Optional
            Default value to set and return if `key` is not present in the weak value dictionary.
        
        Returns
        -------
        value : `default` or `Any`
            The matched value, or `default` if none.
        """
        value = dict.get(self, key, _spaceholder)
        if (value is not _spaceholder):
            return value
        
        self[key] = default
        return default
    
    def update(self, iterable):
        """
        Updates the weak key dictionary with the given iterable's elements.
        
        Parameters
        ----------
        iterable : `iterable`
            Iterable to extend the weak key dictionary with.
            
            Can be given as an object, which:
            - supports `.items` iterator.
            - supports `.keys` and `.__getitem__`.
            - is `iterable` and each iteration returns a sequence with 2 elements.
        
        Raises
        ------
        TypeError
            The given `iterable` is not `iterable`.
        ValueError
            The the given `iterable` sot supports neither `.items` or (`.keys` and `.__getitem__`) and one of it's
            element's length is not `2`.
        """
        iterable_type = iterable.__class__
        if hasattr(iterable_type, 'items'):
            for key, value in iterable.items():
                self[key] = value
            return
        
        if hasattr(iterable_type, 'keys') and hasattr(iterable_type, '__getitem__'):
            for key in iterable.keys():
                value = iterable[key]
                self[key] = value
            return
        
        if hasattr(iterable_type, '__iter__'):
            index = -1
            for item in iterable:
                index += 1
                
                try:
                    iterator=iter(item)
                except TypeError:
                    raise TypeError(f'Cannot convert dictionary update sequence element #{index} to a sequence.') \
                        from None
                
                try:
                    key = next(iterator)
                except StopIteration:
                    raise ValueError(f'Dictionary update sequence element #{index} has length {0}; 2 is required.') \
                        from None
                
                try:
                    value = next(iterator)
                except StopIteration:
                    raise ValueError(f'Dictionary update sequence element #{index} has length {1}; 2 is required.') \
                        from None
                
                try:
                    next(iterator)
                except StopIteration:
                    self[key] = value
                    continue
                
                length = 3
                for _ in iterator:
                    length += 1
                    if length > 9000:
                        break
                
                if length > 9000:
                    length='OVER 9000!'
                else:
                    length=repr(length)
                
                raise ValueError(f'Dictionary update sequence element #{index} has length {length}; 2 is required.')
            return
        
        raise TypeError(f'{iterable_type.__name__!r} object is not iterable')
    
    def values(self):
        """
        Returns value iterator for the weak key dictionary.
        
        Returns
        -------
        value_iterator : ``_WeakKeyDictionaryValueIterator``
        """
        return _WeakKeyDictionaryValueIterator(self)


class _WeakMapCallback(object):
    """
    Callback used by ``WeakMap``-s.
    
    Attributes
    ----------
    _parent : ``WeakReferer`` to ``WeakMap``
        The parent weak map.
    """
    __slots__ = ('_parent', )
    def __new__(cls, parent):
        """
        Creates a new ``_WeakMapCallback`` instance bound to the given ``WeakMap`` instance.
        
        Parameters
        ----------
        parent : ``WeakMap``
            The parent weak map.
        """
        parent = WeakReferer(parent)
        self = object.__new__(cls)
        self._parent = parent
        return self
    
    def __call__(self, reference):
        """
        Called when an element of the respective weak map is garbage collected.
        
        Parameters
        ----------
        reference : ``WeakReferer``
            Weakreference to the respective object.
        """
        parent = self._parent()
        if parent is None:
            return
        
        if parent._iterating:
            add_to_pending_removals(parent, reference)
        else:
            try:
                dict.__delitem__(parent, reference)
            except KeyError:
                pass


class _WeakMapIterator(object):
    """
    Iterator for ``WeakKeyDictionary``-s.
    
    Attributes
    ----------
    _parent : ``WeakReferer`` to ``WeakMap``
        The parent weak map.
    """
    __slots__ = ('_parent', )
    def __init__(self, parent):
        """
        Creates a new ``_WeakMapIterator`` instance bound to the given ``WeakMap``.
        
        Parameters
        ----------
        parent : ``WeakMap``
            The parent weak map.
        """
        self._parent = parent
    
    def __iter__(self):
        """
        Iterates over a weak map.
        
        This method is a generator.
        
        Yields
        ------
        key : `Any`
        """
        parent = self._parent
        parent._iterating += 1
        
        try:
            for reference in dict.__iter__(parent):
                key = reference()
                if (key is None):
                    add_to_pending_removals(parent, reference)
                    continue
                
                yield key
                continue
        
        finally:
            parent._iterating -= 1
            parent._commit_removals()
    
    def __contains__(self, key):
        """Returns whether the respective ``WeakMap`` contains the given key."""
        return (key in self._parent)
    
    def __len__(self):
        """Returns the respective ``WeakMap``'s length."""
        return len(self._parent)


class WeakMap(dict):
    """
    Weak map is a mix of weak dictionaries and weak sets. Can be used to retrieve an already existing weakreferenced
    value from itself.
    
    Attributes
    ----------
    _pending_removals : `None` or `set` of ``WeakReferer``
        Pending removals of the weak map if applicable.
    _iterating : `int`
        Whether the weak map is iterating and how much times.
    _callback : ``_WeakMapCallback``
        Callback added to the ``WeakMap``'s weak keys.
    
    Class Attributes
    ----------------
    MAX_RERP_ELEMENT_LIMIT : `int` = `50`
        The maximal amount of items to render by ``.__repr__``.
    
    Notes
    -----
    ``WeakMap`` instances are weakreferable.
    """
    __slots__ = ('__weakref__', '_pending_removals', '_iterating', '_callback')
    
    MAX_RERP_ELEMENT_LIMIT = 50
    
    def _commit_removals(self):
        """
        Commits the pending removals of the weak map if applicable.
        """
        if self._iterating:
            return
        
        pending_removals = self._pending_removals
        if pending_removals is None:
            return
        
        for reference in pending_removals:
            try:
                dict.__delitem__(self, reference)
            except KeyError:
                pass
        
        self._pending_removals = None
    
    # __class__ -> same
    
    def __contains__(self, key):
        """Returns whether the weak map contains the given key."""
        try:
            reference = WeakReferer(key)
        except TypeError:
            return False
        
        return dict.__contains__(self, reference)
    
    # __delattr__ -> same
    
    def __delitem__(self, key):
        """Deletes the given key from the weak map"""
        try:
            reference = WeakReferer(key)
        except TypeError:
            raise KeyError(key) from None
        
        try:
            dict.__delitem__(self, reference)
        except KeyError as err:
            err.args=(key,)
            raise
    
    # __dir__ -> same
    # __doc__ -> same
    # __eq__ > same
    # __format__ -> same
    # __ge__ -> same
    # __getattribute__ -> same
    
    def __getitem__(self, key):
        """Gets the already existing key from the weak map, which matches the given one."""
        try:
            reference = WeakReferer(key)
        except TypeError:
            raise KeyError(key) from None
        
        return dict.__getitem__(self, reference)
    
    # __gt__ -> same
    # __hash__ -> same
    
    def __init__(self, iterable=None):
        """
        Creates a new ``WeakMap`` instance from the given iterable.
        
        Parameters
        ----------
        iterable : `iterable`, Optional
            Iterable to update the created map with.
        """
        self._pending_removals = None
        self._iterating = 0
        self._callback = _WeakMapCallback(self)
        if (iterable is not None):
            self.update(iterable)
    
    # __init_subclass__ -> same
    
    def __iter__(self):
        """Returns a ``_WeakMapIterator`` iterating over the weak map's keys."""
        return iter(_WeakMapIterator(self))
    
    # __le__ -> same
    
    def __len__(self):
        """Returns the length of the weak map."""
        length = dict.__len__(self)
        pending_removals = self._pending_removals
        if (pending_removals is not None):
            length -= len(pending_removals)
        
        return length
    
    # __lt__ -> same
    # __ne__ -> same
    # __new__ -> same
    # __reduce__ -> we do not care
    # __reduce_ex__ -> we do not care
    
    def __repr__(self):
        """Returns the weak map's representation."""
        result = [self.__class__.__name__, '({']
        if len(self):
            limit = self.MAX_RERP_ELEMENT_LIMIT
            collected = 0
            
            for reference in dict.__iter__(self):
                key = reference()
                if (key is None):
                    add_to_pending_removals(self, reference)
                    continue
                
                result.append(repr(key))
                result.append(', ')
                
                collected +=1
                if collected != limit:
                    continue
                
                leftover = len(self) - collected
                if leftover:
                    result.append('...}, ')
                    result.append(str(leftover))
                    result.append(' truncated)')
                else:
                    result[-1] = '})'
                break
            else:
                result[-1] = '})'
            
            self._commit_removals()
        else:
            result.append('})')
        
        return ''.join(result)
    
    # __setattr__ -> same
    __setitem__ = RemovedDescriptor()
    # __sizeof__ -> same
    
    __str__ = __repr__
    
    # __subclasshook__ -> same
    
    def clear(self):
        """
        Clear's the weak map.
        """
        dict.clear(self)
        self._pending_removals = None
    
    def copy(self):
        """
        Copies the weak map.
        
        Returns
        -------
        new : ``WeakMap``
        """
        new = dict.__new__(type(self))
        new._iterating = False
        new._pending_removals = None
        new._callback = callback = _WeakMapCallback(new)
        
        for reference in dict.__iter__(self):
            key = reference()
            if (key is None):
                add_to_pending_removals(self, reference)
                continue
            
            reference = WeakReferer(key, callback)
            dict.__setitem__(new, reference, reference)
            continue
        
        self._commit_removals()
        
        return new
    
    def get(self, key, default=None):
        """
        Gets the key of the weak map, which matches the given one.
        
        Parameters
        ----------
        key : `Any`
            A key to match.
        default : `Any`, Optional
            Default value to return if the given `key` could not be matched. Defaults to `None`.
        
        Returns
        -------
        real_key : `Any` or `default`
            The matched key. If no key was matched returns the `default` value.
        """
        try:
            reference = WeakReferer(key)
        except TypeError:
            return default
        
        real_reference = dict.get(self, reference, reference)
        if real_reference is reference:
            return default
        
        real_key = real_reference()
        if (real_key is not None):
            return real_key
        
        if self._iterating:
            add_to_pending_removals(self, real_reference)
        else:
            dict.__delitem__(self, real_reference)
        
        return default
    
    items = RemovedDescriptor()
    keys = RemovedDescriptor()
    
    def pop(self, key, default=_spaceholder):
        """
        Pops a key from the weak map which matches the given one.
        
        Parameters
        ----------
        key : `Any`
            A key to match.
        default : `Any`, Optional
            Default value to return if the given `key` could not be matched.
        
        Returns
        -------
        real_key : `Any` or `default`
            The matched key. If no key was matched and `default` value is given, then returns that.
        
        Raises
        ------
        KeyError
            If `key` could not be matched and `default` value is was not given either.
        """
        try:
            reference = WeakReferer(key)
        except TypeError:
            pass
        else:
            real_reference = dict.pop(self, reference, _spaceholder)
            if (real_reference is not _spaceholder):
                real_key = real_reference()
                if (real_key is not None):
                    return real_key
                
                if self._iterating:
                    add_to_pending_removals(self, real_reference)
                else:
                    dict.__delitem__(self, real_reference)
        
        if default is _spaceholder:
            raise KeyError(key)
        
        return default
    
    popitem = RemovedDescriptor()
    setdefault = RemovedDescriptor()
    update = RemovedDescriptor()
    values = RemovedDescriptor()
    
    def set(self, key):
        """
        Sets a key to the ``WeakMap`` and then returns it. If they given key is already present in the ``WeakMap``,
        returns that instead.
        
        Parameters
        ----------
        key : `Any`
            A key to match.
        
        Returns
        -------
        real_key : `Any`
            The matched key, or the given one.
        """
        reference = WeakReferer(key, self._callback)
        real_reference = dict.get(self, reference, None)
        if (real_reference is not None):
            real_key = real_reference()
            if (real_key is not None):
                return real_key
        
        dict.__setitem__(self, reference, reference)
        return key

class module_property(object):
    """
    Instead of defining a  `.__module__` attribute as `property`, define it as `module_property` to avoid getter issues,
    when calling from class.
    
    Attributes
    ----------
    fget : `func`
        Getter used when calling the module from instance.
    module : `str`
        The module where the `module_property` was created.
    """
    __slots__ = ('fget', 'module', )
    def __new__(cls, fget):
        module = getattr(fget, '__module__', None)
        if module is None:
            module = cls.__module__
        elif type(module) is str:
            module = module
        elif isinstance(module, str):
            module = str(module)
        else:
            module = cls.__module__
        
        self = object.__new__(cls)
        self.fget = fget
        self.module = module
        return self
    
    def __get__(self, obj, type_):
        if obj is None:
            return self.module
        
        return self.fget()
    
    def __set__(self, obj, module):
        if module is None:
            module = self.__module__
        elif type(module) is str:
            module = module
        elif isinstance(module, str):
            module = str(module)
        else:
            module = self.__module__
        
        self.module = module
    
    def __delete__(self, obj):
        raise AttributeError('can\'t delete attribute')

del WeakrefType
del dummy_init_tester
