__all__ = ('bind',)

from collections import OrderedDict

from scarletio import RichAttributeErrorBaseType, WeakItemDictionary, WeakKeyDictionary, copy_docs


def bind(bind_to, bind_with, name, *, weak=False, weak_cache_size=0):
    """
    A cool hata features, that lets you bind object to existing one.
    
    Parameters
    ----------
    bind_to : `type`
        The type to bind to.
    bind_with : `type`
        The type to bind with.
    name : `str`
        The name of the binding.
    weak : `bool`, Optional (Keyword only) = `False`
        Whether double weak binding should be implemented.
    weak_cache_size : `int`, Optional (Keyword only) = `0`
        Whether double weak binding should have binding cache. Can be useful when binding requires accessing outer
        resources (like database).
    
    Raises
    ------
    TypeError
        - If `bind_to` is not a type.
        - If `bind_to`-s do not support weakreferencing.
        - If `bind_to` has already an attribute named `name`.
        - If `bind_with` is not weakreferable, but `weak` binding is created.
        - If `weak_cache_size` is not `int`.
    
    Examples
    --------
    Generic binder:
    
    ```py
    from hata import ClientUserBase, bind
    
    class Inventory:
        def __init__(self, parent_self):
            self.user_id = parent_self.id
            self.inventory = []
        
        def add_item(self, name):
            self.inventory.append(name)
        
        def give_user(self, item, recipient):
            self.inventory.remove(item)
            recipient.inventory.add_item(item)
    
    bind(ClientUserBase, Inventory, 'inventory')
    
    # Usage:
    user.inventory.add_item('cake')
    ```
    
    Descriptor binder:
    
    ```py
    from hata import ClientUserBase, bind
    
    class ValueBinder:
        def __init__(self, parent_self):
            self.value = 10
        
        def __get__(self, instance, type_):
            return self.value
        
        def __set__(self, instance, value):
            self.value = value
    
    bind(ClientUserBase, ValueBinder, 'value')
    
    # Usage:
    user.inventory_size += 10
    ```
    
    Descriptor binders are familiar ot normal descriptors, except, they are created per object and not per class.
    
    Sometimes you want to clear extra binders with default values. For this you might want to define the `__bool__`
    method.
    
    ```py
    DEFAULT_VALUE = 10
    
    class ValueBinder:
        def __init__(self, parent_self):
            self.value = DEFAULT_VALUE
        
        def __get__(self, instance, type_):
            return self.value
        
        def __set__(self, instance, value):
            self.value = value
        
        def __bool__(self):
            return (self.value != DEFAULT_VALUE)
    
    
    bind(ClientUserBase, ValueBinder, 'value')
    
    # Usage
    ClientUserBase.value.clear()
    ```
    
    A more advanced concept is reloading modules, which use bindings. For this define `__getstate__` and the
    `__setstate__` magic methods.
    
    > Also defining `__bool__` is not required, but recommended.
    
    ```py
    class Inventory:
        def __init__(self, parent_self):
            self.user_id = parent_self.id
            self.inventory = []
        
        def add_item(self, name):
            self.inventory.append(name)
        
        def give_user(self, item, recipient):
            self.inventory.remove(item)
            recipient.inventory.add_item(item)
        
        def __getstate__(self):
            return (self.user_id, self.inventory)
        
        def __setstate(self, state):
            self.user_id, self.inventory = state
    
    bind(ClientUserBase, Inventory, 'inventory')
    ```
    """
    if not isinstance(bind_to, type):
        raise TypeError(
            f'`bind_to` can be `type`, got {bind_to.__class__.__name__}; {bind_to!r}.'
        )
    
    name_space = bind_to.__dict__
    if ('__weakref__' in name_space) or ('__slots__' not in name_space):
        raise TypeError(
            f'`bind_to`-s must support weakreferencing, got {bind_to!r}.'
        )
    
    
    if weak:
        binded_name_space = bind_with.__dict__
        if ('__weakref__' in binded_name_space) or ('__slots__' not in binded_name_space):
            raise TypeError(
                f'`bind_with`-s must support weakreferencing for weak binding, got {bind_with!r}.'
            )
    
    if hasattr(bind_to, name):
        old_binder = getattr(bind_to, name)
        if not isinstance(old_binder, ObjectBinderBase):
            raise TypeError(
                f'`bind_to` already has an attribute named, as bind_to = {bind_to!r}, name = {name!r}.'
            )
    
    else:
        old_binder = None
    
    if not isinstance(weak_cache_size, int):
        raise TypeError(
            f'`weak_cache_size` can be `int`, got {weak_cache_size.__class__.__name__}; {weak_cache_size!r}.'
        )
    
    is_descriptor = getattr(bind_with, '__get__', None) is not None
    if weak:
        if is_descriptor:
            new_binder = DescriptorObjectWeakBinder(name, bind_with, weak_cache_size)
        else:
            new_binder = GenericObjectWeakBinder(name, bind_with, weak_cache_size)
    else:
        if is_descriptor:
            new_binder = DescriptorObjectBinder(name, bind_with)
        else:
            new_binder = GenericObjectBinder(name, bind_with)
    
    if (
        (old_binder is not None) and
        old_binder.supports_state_transfer and
        new_binder.supports_state_transfer and
        (old_binder.get_type_key() == new_binder.get_type_key())
    ):
        new_binder.set_states(old_binder.get_states(bind_to))
    
    setattr(bind_to, name, new_binder)


class ObjectBinderBase(RichAttributeErrorBaseType):
    """
    Object binder.
    
    Attributes
    ----------
    name : `str`
        The field's name.
    relations : ``WeakKeyDictionary``
        The binding relation mapping.
    supports_clearing : `bool`
        Whether clearing the bound objects is supported.
    supports_state_transfer : `bool`
        Whether the bound objects support state transfer.
    type : `type`
        The binded class.
    
    Class Attributes
    ----------------
    RELATIONSHIP_CONTAINER_TYPE : `type` = ``WeakKeyDictionary``
        The type which holds the relations.
    """
    __slots__ = ('name', 'relations', 'supports_clearing', 'supports_state_transfer', 'type')
    
    RELATIONSHIP_CONTAINER_TYPE = WeakKeyDictionary
    
    def __new__(cls, name, type_):
        """
        Creates a new object binder instance.
        
        Parameters
        ----------
        name : `str`
            The field's name.
        type_ : `type`
            The binded class.
        """
        bool_method = getattr(type_, '__bool__', None)
        if (bool_method is None):
            supports_clearing = False
        else:
            supports_clearing = True
        
        get_state_method = getattr(type_, '__getstate__', None)
        set_state_method = getattr(type_, '__setstate__', None)
        if (get_state_method is None) or (set_state_method is None):
            supports_state_transfer = False
        else:
            supports_state_transfer = True
        
        self = object.__new__(cls)
        self.relations = cls.RELATIONSHIP_CONTAINER_TYPE()
        self.name = name
        self.type = type_
        
        self.supports_clearing = supports_clearing
        self.supports_state_transfer = supports_state_transfer
        
        return self
    
    
    def __get__(self, instance, type_):
        """
        Gets the field's value.
        
        Parameters
        ----------
        instance : `Any`
            The instance itself.
        type_ : `type`
            The instance's type.
        
        Returns
        -------
        value : `self` / `Any`
            Returns itself if called from class.
        """
        if (instance is None):
            return self
    
    
    def __set__(self, instance, value):
        """
        Sets the value to the instance.
        
        Parameters
        ----------
        instance : `Any`
            The parent instance to set the value to.
        value : `Any`
            The value to set.
        
        Raises
        ------
        AttributeError
            Read only attribute.
        """
        raise AttributeError(f'Read only attribute: {self.name!r}.')
    
    
    def __delete__(self, instance):
        """
        Deletes the value of the instance.
        
        Parameters
        ----------
        instance : `Any`
            The parent instance to delete the attribute of.
        
        Raises
        ------
        AttributeError
            Cannot delete attribute.
        """
        raise AttributeError(f'Cannot delete attribute: {self.name!r}.')
    
    
    def __repr__(self):
        """Returns the object binder representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append(', type = ')
        repr_parts.append(repr(self.type))
        
        length = len(self.relations)
        if length:
            repr_parts.append(', length = ')
            repr_parts.append(repr(length))
        
        supports_clearing = self.supports_clearing
        if supports_clearing:
            repr_parts.append(', supports_clearing = ')
            repr_parts.append(repr(supports_clearing))
        
        supports_state_transfer = self.supports_state_transfer
        if supports_state_transfer:
            repr_parts.append(', supports_state_transfer = ')
            repr_parts.append(repr(supports_state_transfer))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def clear(self):
        """
        Clears the bound objects.
        
        Only those objects are cleared, which return `False` from their `__bool__` method.
        
        Returns
        -------
        cleared : `int`
            The amount of objects freed.
        """
        if not self.supports_clearing:
            return 0
        
        relations = self.relations
        to_clear = []
        
        for key, value in relations.items():
            if not value:
                to_clear.append(key)
        
        for key in to_clear:
            del relations[key]
        
        return len(to_clear)
    
    
    def get_type_key(self):
        """
        Returns the type key of the object binder.
        
        It is used when transferring down states to match types.
        
        Returns
        -------
        type_key : `tuple` ((`None`, `str`), (`None`, `str`))
        """
        type_ = self.type
        return getattr(type_, '__module__', None), getattr(type_, '__name__', None)
    
    
    def iter_true_items(self):
        """
        Iterates over all non empty bound objects & keys.
        
        This method is an iterable generator.
        
        Yields
        ------
        key : `Any`
            Objects to bound to.
        value : ``.type``
            The bound object.
        """
        if self.supports_clearing:
            for key, value in self.relations.items():
                if value:
                    yield key, value
        
        else:
            yield from self.relations.items()
    
    
    def get_states(self, type_):
        """
        Gets the given object's states if applicable for the given `type_` instances.
        
        Returns
        -------
        states : `list` of `tuple` (`Any`, `Any`)
        """
        states = []
        if self.supports_state_transfer:
            get_state = self.type.__getstate__
            
            for key, value in self.iter_true_items():
                if not isinstance(key, type_):
                    continue
                
                state = get_state(value)
                states.append((key, state))
        
        return states
    
    
    def set_states(self, states):
        """
        Sets states of an another binder to this one.
        
        Parameters
        ----------
        states : `list` of `tuple` (`Any`, `Any`)
        """
        if self.supports_state_transfer:
            type_ = self.type
            set_state = type_.__setstate__
            relations = self.relations
            
            for key, state in states:
                value = object.__new__(type_)
                set_state(value, state)
                
                relations[key] = value


@copy_docs(ObjectBinderBase)
class GenericObjectBinder(ObjectBinderBase):
    __slots__ = ()
    
    @copy_docs(ObjectBinderBase.__get__)
    def __get__(self, instance, type_):
        if instance is None:
            return self
        
        try:
            bind_object = self.relations[instance]
        except KeyError:
            bind_object = self.type(instance)
            self.relations[instance] = bind_object
        
        return bind_object


class DescriptorObjectBinder(ObjectBinderBase):
    """
    Object binder for descriptors-likes.
    
    Attributes
    ----------
    relations : ``WeakKeyDictionary``
        The binding relation mapping.
    name : `str`
        The field's name.
    type : `type`
        The binded class.
    fdel : `None`, `Any`
        Deleter function if applicable.
    fget : `None`, `Any`
        Getter function if applicable.
    fset : `None`, `Any`
        Setter function if applicable.
    
    Class Attributes
    ----------------
    RELATIONSHIP_CONTAINER_TYPE : `type` = ``WeakKeyDictionary``
        The type which holds the relations.
    """
    __slots__ = ('fdel', 'fget', 'fset')
    
    @copy_docs(ObjectBinderBase.__new__)
    def __new__(cls, name, type_):
        self = ObjectBinderBase.__new__(cls, name, type_)
        self.fdel = getattr(type_, '__delete__', None)
        self.fget = getattr(type_, '__get__')
        self.fset = getattr(type_, '__set__', None)
        return self
    
    
    @copy_docs(ObjectBinderBase.__get__)
    def __get__(self, instance, type_):
        if instance is None:
            return self
        
        try:
            bind_object = self.relations[instance]
        except KeyError:
            bind_object = self.type(instance)
            self.relations[instance] = bind_object
        
        return self.fget(bind_object, instance, type_)
    
    
    @copy_docs(ObjectBinderBase.__get__)
    def __set__(self, instance, value):
        fset = self.fset
        if fset is None:
            raise AttributeError(f'Read only attribute: {self.name!r}.')
        
        try:
            bind_object = self.relations[instance]
        except KeyError:
            bind_object = self.type(instance)
            self.relations[instance] = bind_object
        
        return fset(bind_object, instance, value)
    
    
    @copy_docs(ObjectBinderBase.__delete__)
    def __delete__(self, instance):
        fdel = self.fdel
        if fdel is None:
            raise AttributeError(f'Cannot delete attribute: {self.name!r}.')
        
        try:
            bind_object = self.relations[instance]
        except KeyError:
            bind_object = self.type(instance)
            self.relations[instance] = bind_object
        
        return fdel(bind_object, instance)



def _cache_bind(cache, cache_size, bind_object):
    """
    Caches the given bind object if applicable.
    
    Parameters
    ----------
    cache : `None`, `OrderedDict`
        Cache if applicable.
    cache_size : `int`
        The maximal size of the cache.
    bind_object : `Any`
        The bind object to cache.
    """
    if (cache is not None):
        if bind_object in cache:
            cache.move_to_end(bind_object)
        
        else:
            cache[bind_object] = bind_object
            
            if len(cache) >= cache_size:
                del cache[next(iter(cache))]


class GenericObjectWeakBinder(GenericObjectBinder):
    """
    Object binder.
    
    Attributes
    ----------
    name : `str`
        The field's name.
    relations : ``WeakKeyDictionary``
        The binding relation mapping.
    supports_clearing : `bool`
        Whether clearing the bound objects is supported.
    supports_state_transfer : `bool`
        Whether the bound objects support state transfer.
    type : `type`
        The binded class.
    
    cache : `None`, ``OrderedDict``
        Cache dictionary, to avoid repeated initializing.
    cache_size : `int`
        The maximal size of the cache.
    
    Class Attributes
    ----------------
    RELATIONSHIP_CONTAINER_TYPE : `type` = ``WeakItemDictionary``
        The type which holds the relations.
    """
    __slots__ = ('cache', 'cache_size',)
    
    RELATIONSHIP_CONTAINER_TYPE = WeakItemDictionary
    
    def __new__(cls, name, type_, cache_size):
        """
        Creates a new object binder instance.
        
        Parameters
        ----------
        name : `str`
            The field's name.
        type_ : `type`
            The binded class.
        cache_size : `int`
            The maximal size of the cache.
        """
        if cache_size > 0:
            cache = OrderedDict()
        else:
            cache = None
        
        self = GenericObjectBinder.__new__(cls, name, type_)
        
        self.cache = cache
        self.cache_size = cache_size
        
        return self
    
    
    @copy_docs(GenericObjectBinder.__get__)
    def __get__(self, instance, type_):
        bind_object = GenericObjectBinder.__get__(self, instance, type_)
        if (bind_object is not self):
            _cache_bind(self.cache, self.cache_size, bind_object)
        
        return bind_object


class DescriptorObjectWeakBinder(DescriptorObjectBinder):
    """
    Object binder for descriptors-likes.
    
    Attributes
    ----------
    relations : ``WeakKeyDictionary``
        The binding relation mapping.
    name : `str`
        The field's name.
    type : `type`
        The binded class.
    fdel : `None`, `Any`
        Deleter function if applicable.
    fget : `None`, `Any`
        Getter function if applicable.
    fset : `None`, `Any`
        Setter function if applicable.
    
    cache : `None`, ``OrderedDict``
        Cache dictionary, to avoid repeated initializing.
    cache_size : `int`
        The maximal size of the cache.
    
    Class Attributes
    ----------------
    RELATIONSHIP_CONTAINER_TYPE : `type` = ``WeakItemDictionary``
        The type which holds the relations.
    """
    __slots__ = GenericObjectWeakBinder.__slots__
    
    RELATIONSHIP_CONTAINER_TYPE = GenericObjectWeakBinder.RELATIONSHIP_CONTAINER_TYPE
    
    @copy_docs(GenericObjectWeakBinder.__new__)
    def __new__(cls, name, type_, cache_size):
        if cache_size > 0:
            cache = OrderedDict()
        else:
            cache = None
        
        self = DescriptorObjectBinder.__new__(cls, name, type_)
        
        self.cache = cache
        self.cache_size = cache_size
        
        return self
    
    
    @copy_docs(DescriptorObjectBinder.__get__)
    def __get__(self, instance, type_):
        bind_object = DescriptorObjectBinder.__get__(self, instance, type_)
        if (bind_object is not self):
            _cache_bind(self.cache, self.cache_size, bind_object)
        
        return bind_object
