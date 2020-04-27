# -*- coding: utf-8 -*-
from ..backend.dereaddons_local import _spaceholder
from .others import id_to_time

class DiscordEntityMeta(type):
    def __new__(cls, class_name, class_parents, class_attributes, immortal=False):
        final_slots = set()
        
        parent_count = len(class_parents)
        if parent_count > 0:
            parent = class_parents[0]
            final_slots.update(getattr(parent,'__slots__',()))
            
            #Sublasses might miss hash!
            if class_attributes.get('__hash__', None) is None:
                class_attributes['__hash__'] = parent.__hash__
            
            # Remove weakref to avoid error
            try:
                final_slots.remove('__weakref__')
            except KeyError:
                pass
            
            index = 1
            while index < parent_count:
                parent = class_parents[index]
                final_slots.update(getattr(parent,f'_{parent.__name__}__slots',()))
                index +=1
        
        final_slots.update(class_attributes.get('__slots__',()))
        
        if immortal:
            for parent in class_parents:
                if hasattr(parent,'__weakref__'):
                    break
            else:
                final_slots.add('__weakref__')
        
        class_attributes['__slots__'] = tuple(sorted(final_slots))
        
        return type.__new__(cls, class_name, class_parents, class_attributes)

class DiscordEntity(object, metaclass = DiscordEntityMeta):
    __slots__ = ('id', )
    
    @property
    def created_at(self):
        return id_to_time(self.id)
    
    def __hash__(self):
        return self.id
    
    def __gt__(self, other):
        if type(self) is type(other):
            return self.id > other.id
        
        return NotImplemented
    
    def __ge__(self, other):
        if type(self) is type(other):
            return self.id >= other.id
        
        return NotImplemented
    
    def __eq__(self, other):
        if type(self) is type(other):
            return self.id == other.id
        
        return NotImplemented
    
    def __ne__(self, other):
        if type(self) is type(other):
            return self.id != other.id
        
        return NotImplemented
    
    def __le__(self, other):
        if type(self) is type(other):
            return self.id <= other.id
        
        return NotImplemented
    
    def __lt__(self, other):
        if type(self) is type(other):
            return self.id < other.id
        
        return NotImplemented

class FlagGetDescriptor(object):
    __slots__ = ('shift', )
    def __init__(self, shift):
        self.shift = shift
    
    def __get__(self, instance, type_=None):
        if instance is None:
            return self
        else:
            return (instance>>self.shift)&1
    
    def __call__(self, value):
        return (value>>self.shift)&1
    
    def __set__(self, obj, value):
        raise AttributeError('can\'t set attribute')
    
    def __delete__(self, obj):
        raise AttributeError('can\'t delete attribute')

class ReverseFlagGetDescriptor(FlagGetDescriptor):
    def __get__(self, instance, type_=None):
        if instance is None:
            return self
        else:
            return ((instance>>self.shift)&1)^1
    
    def __call__(self, value):
        return ((value>>self.shift)&1)^1

class FlagEnabler(object):
    __slots__ = ('instance', 'shift')
    
    def __call__(self):
        instance = self.instance
        shift = self.shift
        return int.__new__(type(instance),(instance|(1<<self.shift)))

class FlagEnableDescriptor(FlagGetDescriptor):
    def __get__(self, instance, type_=None):
        if instance is None:
            return self
        else:
            result = FlagEnabler()
            result.instance = instance
            result.shift = self.shift
            return result

class FlagDisabler(object):
    __slots__ = ('instance', 'shift')
    
    def __call__(self):
        instance = self.instance
        shift = self.shift
        if (instance>>shift)&1:
            return int.__new__(type(instance),(instance^(1<<shift)))
        else:
            return instance

class FlagDisableDescriptor(FlagGetDescriptor):
    def __get__(self, instance, type_=None):
        if instance is None:
            return self
        else:
            result = FlagDisabler()
            result.instance = instance
            result.shift = self.shift
            return result

class FlagMeta(type):
    __default_type = NotImplemented
    def __new__(cls, class_name, class_parents, class_attributes, access_keyword=None, enable_keyword=None, disable_keyword=None,
            baseclass=False):
        
        if baseclass:
            if (not class_parents) or (not issubclass(class_parents[0],int)):
                raise TypeError(f'`{class_name}` is not derived directly from `int`.')
            
            class_keys = class_attributes.get('__keys__',_spaceholder)
            if class_keys is NotImplemented:
                pass
            elif class_keys is _spaceholder:
                class_attributes['__keys__'] = NotImplemented
            else:
                raise TypeError(f'`{class_name}` has `__keys__` defined and not as `NotImplemented`.')
            
            # do not care about the leftover
            
            return type.__new__(cls, class_name, class_parents, class_attributes)
        
        # Python has no GOTO, so lets insert one
        while True:
            if class_parents:
                parent = class_parents[0]
                if (type(parent) is FlagMeta) and parent.__keys__ is NotImplemented:
                    break
            
            raise TypeError(f'`{class_name}` is not derived directly from a `{cls.__name__}` base instance.')
        
        # Validate keys
        try:
            keys = class_attributes['__keys__']
        except KeyError:
            raise TypeError(f'`{class_name}` did not define `__keys__` attribute.') from None
        
        if (type(keys) is not dict):
            raise TypeError(f'`__keys__` defined as non `dict`: `{keys.__class__.__name__}`.')
        
        for name, shift in keys.items():
            if (type(name) is not str):
                raise TypeError(f'`__keys__`\'s keys should be `str` instances, meanwhile got at least 1 non `str`: {name!r}.')
            
            if (type(shift) is not int):
                raise TypeError(f'`__keys__`\'s values should be `int` instances, meanwhile got at least 1 non `int`: {shift!r}.')
            
            if shift < 0 or shift > 63:
                raise TypeError(f'`__keys__`\' values must be between 0 and 63, got: {shift!r}')
        
        class_attributes.setdefault('__new__', int.__new__)
        
        getter = parent.__getter_class__
        enabler = parent.__enabler_class__
        disabler = parent.__disabler_class__
        
        # Add properties
        for name, shift in keys.items():
            if access_keyword is None:
                access_name = name
            else:
                access_name = f'{access_keyword}_{name}'
            
            class_attributes[access_name] = getter(shift)
            
            if (enable_keyword is not None):
                class_attributes[f'{enable_keyword}_{name}'] = enabler(shift)
            
            if (disable_keyword is not None):
                class_attributes[f'{disable_keyword}_{name}'] = disabler(shift)
        
        return type.__new__(cls, class_name, class_parents, class_attributes)

class FlagBase(int, metaclass = FlagMeta, baseclass=True):
    __slots__ = ()
    __keys__ = NotImplemented
    
    __getter_class__ = FlagGetDescriptor
    __enabler_class__ = FlagEnableDescriptor
    __disabler_class__ = FlagDisableDescriptor
    
    def __new__(self, base=None):
        raise NotImplementedError
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self!s})'
    
    def __getitem__(self,key):
        return (self>>self.__keys__[key])&1
    
    def keys(self):
        for name, shift in self.__keys__.items():
            if (self>>shift)&1:
                yield name
    
    __iter__ = keys
    
    def values(self):
        for shift in self.__keys__.values():
            if (self>>shift)&1:
                yield shift
    
    def items(self):
        for name, shift in self.__keys__.items():
            yield name, (self>>shift)&1
    
    def __contains__(self,key):
        try:
            position=self.__keys__[key]
        except KeyError:
            return 0
        
        return (self>>position)&1
    
    def is_subset(self,other):
        return (self&other)==self
    
    def is_superset(self,other):
        return (self|other)==self
    
    def is_strict_subset(self,other):
        return self!=other and (self&other)==self
    
    def is_strict_superset(self,other):
        return self!=other and (self|other)==self
    
    __ge__ = is_superset
    __gt__ = is_strict_superset
    __lt__ = is_strict_subset
    __le__ = is_subset
    
    def update_by_keys(self,**kwargs):
        new=self
        for key, value in kwargs.items():
            try:
                shift=self.__keys__[key]
            except KeyError as err:
                err.args=(f'Invalid key:{key!r}.',)
                raise
            
            if value:
                new|=(1<<shift)
            else:
                if (new>>shift)&1:
                    new^=(1<<shift)
        
        return int.__new__(type(self),new)


class ReverseFlagBase(FlagBase, baseclass=True):
    __getter_class__ = ReverseFlagGetDescriptor
    __enabler_class__ = FlagDisableDescriptor
    __disabler_class__ = FlagEnableDescriptor
    
    def __getitem__(self,key):
        return ((self>>self.__keys__[key])&1)^1
    
    def keys(self):
        for name, shift in self.__keys__.items():
            if ((self>>shift)&1)^1:
                yield name
    
    __iter__ = keys
    
    def values(self):
        for shift in self.__keys__.values():
            if ((self>>shift)&1)^1:
                yield shift
    
    def items(self):
        for name, shift in self.__keys__.items():
            yield name, ((self>>shift)&1)^1
    
    def __contains__(self,key):
        try:
            position=self.__keys__[key]
        except KeyError:
            return 0
        
        return ((self>>position)&1)^1
    
    def is_subset(self,other):
        return (self|other)==self
    
    def is_superset(self,other):
        return (self&other)==self
    
    def is_strict_subset(self,other):
        return self!=other and (self|other)==self
    
    def is_strict_superset(self,other):
        return self!=other and (self&other)==self
    
    __ge__ = is_superset
    __gt__ = is_strict_superset
    __lt__ = is_strict_subset
    __le__ = is_subset
    
    def update_by_keys(self,**kwargs):
        new=self
        for key, value in kwargs.items():
            try:
                shift=self.__keys__[key]
            except KeyError as err:
                err.args=(f'Invalid key:{key!r}.',)
                raise
            
            if value:
                if (new>>shift)&1:
                    new^=(1<<shift)
            else:
                new|=(1<<shift)
        
        return int.__new__(type(self),new)

