__all__ = ('bind',)

from scarletio import WeakKeyDictionary, copy_docs


def bind(bind_to, bind_with, name):
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
    
    Raises
    ------
    TypeError
        - If `bind_to` is not a type.
        - If `bind_to`-s do not support weakreferencing.
        - If `bind_to` has already an attribute named `name`.
    
    Examples
    --------
    Generic binder:
    ```py
    from hata import ClientUserBase, bind
    
    class Inventory(object):
        def __init__(self, parent_self):
            self.user = parent_self
            self.inv = []
        
        def add_item(self, name):
            self.inv.append(name)
        
        def give_user(self, item, recipient):
            del self.inv[self.inv.index(item)]
            recipient.inventory.add_item(item)
    
    bind(ClientUserBase, Inventory, 'inventory')
    
    # Usage:
    user.inventory.add_item('cake')
    ```
    
    Descriptor binder:
    ```py
    from hata import ClientUserBase, bind
    
    class InventorySize(object):
        def __init__(self, parent_self):
            self.value = 10
        
        def __get__(self, instance, type_):
            return self.value
        
        def __set__(self, instance, value):
            self.value = value
    
    bind(ClientUserBase, InventorySize, 'inventory_size')
    
    # Usage:
    user.inventory_size += 10
    ```
    Descriptor binders are familiar ot normal descriptors, except, they are created per object and not per class.
    
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
    
    if hasattr(bind_to, name):
        raise TypeError(
            f'`bind_to` already has an attribute named, as bind_to={bind_to!r}, name={name!r}.'
        )
    
    if (getattr(bind_with, '__get__', None) is not None):
        binder = DescriptorObjectBinder(name, bind_with)
    else:
        binder = GenericObjectBinder(name, bind_with)
    
    setattr(bind_to, name, binder)


class ObjectBinderBase:
    """
    Object binder.
    
    Attributes
    ----------
    cache : ``WeakKeyDictionary``
        The binding relation mapping.
    name : `str`
        The filed's name.
    type : `type`
        The binded class.
    """
    __slots__ = ('cache', 'name', 'type',)
    
    def __new__(cls, name, type_):
        """
        Creates a new object binder instance.
        
        Parameters
        ----------
        name : `str`
            The filed's name.
        type_ : `type`
            The binded class.
        """
        self = object.__new__(cls)
        self.cache = WeakKeyDictionary()
        self.name = name
        self.type = type_
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
    

class GenericObjectBinder(ObjectBinderBase):
    __slots__ = ()
    
    @copy_docs(ObjectBinderBase.__get__)
    def __get__(self, instance, type_):
        if instance is None:
            return self
        
        try:
            bind_object = self.cache[instance]
        except KeyError:
            bind_object = self.type(instance)
            self.cache[instance] = bind_object
        
        return bind_object


class DescriptorObjectBinder(ObjectBinderBase):
    """
    Object binder for descriptors-likes.
    
    Attributes
    ----------
    cache : ``WeakKeyDictionary``
        The binding relation mapping.
    name : `str`
        The filed's name.
    type : `type`
        The binded class.
    fdel : `None`, `Any`
        Deleter function if applicable.
    fget : `None`, `Any`
        Getter function if applicable.
    fset : `None`, `Any`
        Setter function if applicable.
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
            bind_object = self.cache[instance]
        except KeyError:
            bind_object = self.type(instance)
            self.cache[instance] = bind_object
        
        return self.fget(bind_object, instance, type_)
    
    
    @copy_docs(ObjectBinderBase.__get__)
    def __set__(self, instance, value):
        fset = self.fset
        if fset is None:
            raise AttributeError(f'Read only attribute: {self.name!r}.')
        
        try:
            bind_object = self.cache[instance]
        except KeyError:
            bind_object = self.type(instance)
            self.cache[instance] = bind_object
        
        return fset(bind_object, instance, value)
    
    
    @copy_docs(ObjectBinderBase.__delete__)
    def __delete__(self, instance):
        fdel = self.fdel
        if fdel is None:
            raise AttributeError(f'Cannot delete attribute: {self.name!r}.')
        
        try:
            bind_object = self.cache[instance]
        except KeyError:
            bind_object = self.type(instance)
            self.cache[instance] = bind_object
        
        return fdel(bind_object, instance)
