# -*- coding: utf-8 -*-
__all__ = ('BaseMethodDescriptor', 'KeepType', 'KeyedReferer', 'RemovedDescriptor', 'WeakCallable', 'WeakKeyDictionary',
    'WeakMap', 'WeakReferer', 'WeakValueDictionary', 'alchemy_incendiary', 'any_to_any', 'cached_property',
    'isweakreferable', 'listdifference', 'methodize', 'module_property', 'modulize', 'multidict', 'multidict_titled',
    'titledstr', 'weakmethod', )

from types import \
    MethodType              as method, \
    FunctionType            as function, \
    MappingProxyType        as mappingproxy, \
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
    A descriptor, what can be used to overwrite a classe's attribute, what sould be inherited anyways.
    
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
    
    def __get__(self, obj, objtype):
        name = self.name
        if name is None:
            raise RuntimeError(f'{self.__class__.__name__} is not initialized correctly yet.')
        
        if obj is None:
            error_message = f'type object {objtype.__name__!r} has no attribute {name!r}'
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

def any_to_any(v1, v2):
    for v in v1:
        if v in v2:
            return True
    return False

class autoposlist(list):
    """
    Represents an autopositioned list.
    """
    __slots__ = ()
    
    extend = RemovedDescriptor()
    __add__ = RemovedDescriptor()
    __iadd__ = RemovedDescriptor()
    __radd__ = RemovedDescriptor()
    __mul__ = RemovedDescriptor()
    __imul__ = RemovedDescriptor()
    __rmul__ = RemovedDescriptor()
    __setitem__ = RemovedDescriptor()
    insert = RemovedDescriptor()
    reverse = RemovedDescriptor()
    
    def __init__(self):
        list.__init__(self)
    
    def append(self,value):
        """
        Adds the given element to the list.
        
        Parameters
        ----------
        value : `Any`
        """
        list.insert(self,self.relative_index(value),value)
    
    def relative_index(self, value):
        """
        Retunrs on which the given `value` would be inserted into the list.
        
        Parameters
        ----------
        value : `Any`
        
        Returns
        -------
        relative_index : `int`
        """
        bot = 0
        top = len(self)
        
        while True:
            if bot < top:
                half = (bot+top)>>1
                if self[half] < value:
                    bot = half+1
                else:
                    top = half
                continue
            return bot
    
    def index(self, value):
        """
        Returns the exact index of the given `value`, or `-1` if it is not in the list.
        
        Parameters
        ----------
        value : `Any`
            Any object with `.position` attribute.
        
        Returns
        -------
        index : `int`
        
        Raises
        ------
        ValueError
            The given `value` is not in the list.
        """
        index = self.relative_index(value)
        if (index == len(self)) or (self[index] != value):
            raise ValueError(f'{value!r} is not in the {self.__class__.__name__}.')
        
        return index
    
    def remove(self, value):
        """
        Removes the given value from the list.
        
        Parameters
        ----------
        value : `Any`
            Any object with `.position` attribute.
        
        Notes
        -----
        if the given `value` is not in the list, `ValueError` will not be raised.
        """
        index = self.relative_index(value)
        if (index != len(self)) and (self[index] == value):
            del self[index]
    
    def __contains__(self, value):
        """Returns whether the given value is in the list."""
        return (self.index(value) != -1)
    
    def change_on_switch(self, value, new_position, key=None):
        """
        Calcualtes the changes if the given `value` would be moved to an another position.
        
        Parameters
        ----------
        value : `Any`
            The object, whatt would be moved.
        new_position : `int`
            The new position of the value.
        key : `None` or `callable`
            A special callable what would be used to used to build each element of the result.
        
        Returns
        -------
        result : `list` of (`tuple` (`int`, `Any`)) or `callable` returns
            The changed positons.
        
        Raises
        ------
        ValueError
            The given `value` is not in the list.
        """
        ln=len(self)
        
        old_position = self.relative_index(value)
        if (old_position == ln) or (self[old_position] != value):
            raise ValueError(f'{value!r} is not in the {self.__class__.__name__}.')
        
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
            actual = self[index]
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

def where(self, key):
    for value in self:
        if key(value):
            break
    else:
        raise LookupError(key)
    
    return value

class KeepType(object):
    __slots__ = ('old_class')
    _ignored_attr_names = {'__name__', '__qualname__', '__weakref__', '__dict__', '__slots__'}
    
    def __new__(cls, old_class, *, new_class=None):
        self = object.__new__(cls)
        self.old_class = old_class
        
        if new_class is None:
            return self
        
        return self(new_class)
    
    def __call__(self, new_class):
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

_spaceholder=object()

class _multidict_items:
    __slots__=('_parent',)
    def __init__(self,parent):
        self._parent=parent
    def __len__(self):
        return len(self._parent)
    def __iter__(self):
        for key, values in dict.items(self._parent):
            for value in values:
                yield key,value
    
    def __contains__(self,item):
        parent=self._parent
        try:
            values=parent[item[0]]
        except KeyError:
            return False
        return item[1] in values

class _multidict_values:
    __slots__ = _multidict_items.__slots__
    __init__  = _multidict_items.__init__
    __len__   = _multidict_items.__len__
    def __iter__(self):
        for values in dict.values(self._parent):
            yield from values
    def __contains__(self,value):
        for values in dict.values(self._parent):
            if value in values:
                return True
        return False
    
class multidict(dict):
    __slots__=()
    def __init__(self,iterable=None):
        if not iterable:
            dict.__init__(self)
            return
        if isinstance(iterable,multidict):
            dict.__init__(self,iterable)
            return
        dict.__init__(self)
        getitem=dict.__getitem__
        setitem=dict.__setitem__
        if isinstance(iterable,dict):
            for key,value in iterable.items():
                setitem(self,key,[value])
            return
        for key,value in iterable:
            try:
                getitem(self,key).append(value)
            except KeyError:
                setitem(self,key,[value])
        
    def __getitem__(self,key):
        return dict.__getitem__(self,key)[0]
    
    def __setitem__(self,key,value):
        try:
            line=dict.__getitem__(self,key)
            if value not in line:
                line.append(value)
        except KeyError:
            dict.__setitem__(self,key,[value])
            
    def __delitem__(self,key):
        my_list=dict.__getitem__(self,key)
        if len(my_list)==1:
            dict.__delitem__(self,key)
        else:
            del my_list[0]

    def extend(self,mapping):
        getitem=dict.__getitem__
        setitem=dict.__setitem__
        for key,value in mapping.items():
            try:
                line=getitem(self,key)
                if value not in line:
                    line.append(value)
            except KeyError:
                setitem(self,key,[value])
    
    
    def getall(self,key,default=None):
        try:
            return dict.__getitem__(self,key)
        except KeyError:
            return default
        
    def getone(self,key,default=None):
        try:
            return dict.__getitem__(self,key)[0]
        except KeyError:
            return default
        
    get=getone
        
    def setdefault(self,key,default=None):
        try:
            return dict.__getitem__(self,key)[0]
        except KeyError:
            pass
        dict.__setitem__(self,key,[default])
        return default

    def popall(self,key,default=_spaceholder):
        try:
            return dict.pop(self,key)
        except KeyError:
            if default is not _spaceholder:
                return default
            raise

    def popone(self,key,default=_spaceholder):
        try:
            return dict.__getitem__(self,key).pop(0)
        except KeyError:
            if default is not _spaceholder:
                return default
            raise
        
    pop=popone   
    
    #inheritable:
    def copy(self):
        new=dict.__new__(type(self))
        setitem=dict.__setitem__
        for key,values in dict.items(self):
            setitem(new,key,values.copy())
        return new
    
    def items(self):
        return _multidict_items(self)
    
    def values(self):
        return _multidict_values(self)
    
    def __repr__(self):
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
            
            result[-1]='})'
        else:
            result.append('})')
        
        return ''.join(result)
    
    __str__=__repr__

    def kwargs(self):
        result={}
        for key,value in dict.items(self):
            result[key]=value[-1]
        return result

class multidict_titled(multidict):
    __slots__=()
    def __init__(self,iterable=None):
        if not iterable:
            return dict.__init__(self)
        if type(iterable)==type(self):
            dict.__init__(self,iterable)
            return
        dict.__init__(self)
        getitem=dict.__getitem__
        setitem=dict.__setitem__
        if isinstance(iterable,multidict):
            for key,value in iterable:
                setitem(self,key.title(),value)
            return
        if isinstance(iterable,dict):
            for key,value in iterable.items():
                setitem(self,key,[value])
            return
        for key,value in iterable:
            key=key.title()
            try:
                getitem(self,key).append(value)
            except KeyError:
                setitem(self,key,[value])
        
    def __getitem__(self,key):
        key=key.title()
        return dict.__getitem__(self,key)[0]
    
    def __setitem__(self,key,value):
        key=key.title()
        multidict.__setitem__(self,key,value)
        
    def __delitem__(self,key):
        key=key.title()
        multidict.__delitem__(self,key)
        
    def extend(self,mapping):
        getitem=dict.__getitem__
        setitem=dict.__setitem__               
        for key,value in mapping.items():
            key=key.title()
            try:
                line=getitem(self,key)
                if value not in line:
                    line.append(value)
            except KeyError:
                setitem(self,key,[value])
    
    def getall(self,key,default=None):
        key=key.title()
        return multidict.getall(self,key,default)
    
    def getone(self,key,default=None):
        key=key.title()
        return multidict.getone(self,key,default)
    
    get=getone
    
    def setdefault(self,key,default=None):
        key=key.title()
        return multidict.setdefault(self,key,default)

    def popall(self,key,default=_spaceholder):
        key=key.title()
        return multidict.popall(self,key,default)

    def popone(self,key,default=_spaceholder):
        key=key.title()
        return multidict.popone(self,key,default)

    pop=popone
    
class titledstr(str):
    def __new__(cls,value='',encoding=sys.getdefaultencoding(),errors='strict'):
        if type(value) is cls:
            return value
        if isinstance(value,(bytes, bytearray, memoryview)):
            val=str(value,encoding,errors)
        elif isinstance(value,str):
            pass
        else:
            value=str(value)
        value=value.title()
        return str.__new__(cls,value)
    
    def title(self):
        return self

def listdifference(list1,list2):
    result=([],[])
    
    if list1 is None:
        if list2 is None:
            return result
        else:
            result[1].extend(list2)
            return result
    else:
        if list2 is None:
            result[0].extend(list1)
            return result
    
    if isinstance(list1,set):
        list1=sorted(list1)
    if isinstance(list2,set):
        list2=sorted(list2)
        
    ln1=len(list1)
    ln2=len(list2)
    index1=index2=0

    #some quality python here again *cough*
    while True:
        if index1==ln1:
            while True:
                if index2==ln2:
                    break
                value2=list2[index2]
                result[1].append(value2)
                index2+=1

            break
        if index2==ln2:
            while True:
                if index1==ln1:
                    break
                value1=list1[index1]
                result[0].append(value1)
                index1+=1

            break
         
        value1=list1[index1]
        value2=list2[index2]
        if value1<value2:
            result[0].append(value1)
            index1=index1+1
            continue
        if value1>value2:
            result[1].append(value2)
            index2=index2+1
            continue
        if value1!=value2:
            result[0].append(value1)
            result[1].append(value2)
        index1=index1+1
        index2=index2+1

    return result

class code_line(object):
    __slots__=('_back','text',)
    def __init__(self,text,back):
        self.text=text
        self._back=back
    def __str__(self):
        return self.text
    @property
    def asinline(self):
        return '    '*self._back+self.text

class comment_line(object):
    __slots__=('text',)
    def __init__(self,text):
        self.text=text
    def __str__(self):
        return self.text
    @property
    def asinline(self):
        return self

class code_multyline(object):
    __slots__=('_back','lines',)
    def __init__(self,lines,back):
        self.lines=lines
        self._back=back
    def __str__(self):
        return '\n'.join(self.lines)
    @property
    def asinline(self):
        back=self._back
        if back:
            backtext='    '*back
            return '\n'.join([backtext+line for line in self.lines])
        else:
            return '\n'.join(self.lines)

class code(object):
    __slots__=('_back_state','_list',)
    def __init__(self,back=0):
        self._list=[]
        self._back_state=back
    def append(self,text,backstate=0):
        if not text:
            return
        if text.lstrip()[0]=='#':
            self._list.append(comment_line(text))
        else:
            self._list.append(code_line(text,self._back_state+backstate))
    def go_in(self,count=1):
        self._back_state+=count
    def go_out(self,count=1):
        self._back_state-=count
    def __repr__(self):
        return f'<{self.__class__.__name__} object length={self._list.__len__()}>'
    def __str__(self):
        return '\n'.join([line.asinline for line in self._list])
    def compile(self,filename='',globalz=None,imports=tuple()):
        localz=locals()
        exec(compile(self.__str__(),f'<{filename}>','exec',optimize=2),globalz,localz)
        if type(imports) is str:
            return localz[imports]
        else:
            return tuple(localz[import_] for import_ in imports)
     
    def dedent(self):
        for line in self._list:
            line._back-=1
    def indent(self):
        for line in self._list:
            line._back+=1
    #nocopy
    def __add__(self,other):
        #if type(self) is not type(other):
        #    raise TypeError
        new=self.__new__(type(self))
        self_list=self._list
        other_list=other._list
        new._list=new_list=self_list+other_list
        push=self._back_state-other.D_back
        if push:
            start=self_list.__len__()
            end=start+other_list.__len__()
            for index in range(start,end,1):
                line=new_list[index]
                if type(line)==code_line:
                    line._back+=push
            new._back_state=other._back_state+push
        else:
            new._back_state=other._back_state
        return new
    #nocopy
    def __iadd__(self,other):
        #if type(self) is not type(other):
        #    raise TypeError
        self_list=self._list
        other_list=other._list
        push=self._back_state-other.D_back
        if push:
            start=self_list.__len__()
            self_list.extend(other_list)
            end=start+other_list.__len__()
            for index in range(start,end,1):
                line=self_list[index]
                if type(line)==code_line:
                    line._back+=push
            self._back_state=other._back_state+push
        else:
            self_list.extend(other_list)
            self._back_state=other._back_state
        return self
    @property
    def D_back(self):
        for line in self._list:
            if type(line) is code_line:
                return line._back
    def extend(self,lines,backstate=0):
        for line in lines:
            self.append(line,backstate)

class cached_property(object):
    __slots__=('fget', 'name',)
    #Use as a class method decorator.  It operates almost exactly like
    #the Python `@property` decorator, but it puts the result of the
    #method it decorates into the instance dict after the first call,
    #effectively replacing the function it decorates with an instance
    #variable.
    def __new__(cls, fget):
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
    
    def __get__(self, obj, objtype):
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
    __slots__=('args', 'func', 'kwargs',)
    def __init__(self,func,args,kwargs=None):
        self.func   = func
        self.args   = args
        self.kwargs = kwargs
    
    def __call__(self):
        kwargs=self.kwargs
        if kwargs is None:
            return self.func(*self.args)
        
        return self.func(*self.args,**kwargs)

class SubCheckType(type):
    def __instancecheck__(cls,instance):
        return (type(instance) in cls.__subclasses__)

    def __subclasscheck__(cls,klass):
        return (klass in cls.__subclasses__)

class MethodLike(metaclass=SubCheckType):
    __subclasses__={method}
    __slots__=()
    def __init_subclass__(cls):
        cls.__subclasses__.add(cls)
    
    __reserved_argcount__=1
    
    @classmethod
    def get_reserved_argcount(cls,instance):
        klass=type(instance)
        reserved_argcount=getattr(klass,'__reserved_argcount__',-1)
        if reserved_argcount!=-1:
            return reserved_argcount
        
        if klass in cls.__subclasses__:
            return cls.__reserved_argcount__

        raise TypeError(f'Expected a method like, got {instance!r}')

class basemethod(MethodLike):
    __slots__ = ('__base__', '__func__', '__self__', )
    __reserved_argcount__=2
    
    def __init__(self, func, cls, base):
        self.__base__ = base
        self.__func__ = func
        self.__self__ = cls
    
    def __call__(self, *args, **kwargs):
        return self.__func__(self.__self__, self.__base__, *args, **kwargs)
    
    def __getattr__(self,name):
        return getattr(self.__func__,name)
    
    @property
    def __doc__(self):
        return self.__func__.__doc__

class BaseMethodDescriptor(object):
    __slots__=('fget',)
    def __init__(self, fget):
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

DO_NOT_MODULIZE_TYPES = [mappingproxy, getset_descriptor, ]

if wrapper_descriptor is not function:
    DO_NOT_MODULIZE_TYPES.append(wrapper_descriptor)

if method_descriptor is not function:
    DO_NOT_MODULIZE_TYPES.append(method_descriptor)

DO_NOT_MODULIZE_TYPES = tuple(DO_NOT_MODULIZE_TYPES)

del mappingproxy
del getset_descriptor
del wrapper_descriptor
del method_descriptor

def _modulize_function(old, globals_, source_module, module_name, module_path):
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
    if not isinstance(klass,type):
        raise TypeError('Only types can be modulized')
    
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
        if name.startswith('__') and name.endswith('__') and name!='__doc__':
            continue
        
        value = type.__getattribute__(klass,name)
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
    __slots__=('klass',)
    def __init__(self,klass):
        self.klass = klass
    
    def __get__(self, obj, type_):
        klass = self.klass
        if obj is None:
            return klass
        
        return method(klass, obj)
    
    def __set__(self, obj, value):
        raise AttributeError('can\'t set attribute')
    
    def __delete__(self,obj):
        raise AttributeError('can\'t delete attribute')

class sortedlist(list):
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
    
    def __init__(self,it=None,reverse=False):
        self._reversed=reverse
        if (it is not None):
            self.extend(it)
            list.sort(self,reverse=reverse)
    
    def __repr__(self):
        result=[self.__class__.__name__,'([']
        
        limit=len(self)
        if limit:
            index=0
            while True:
                element=self[index]
                index=index+1
                result.append(repr(element))
                
                if index==limit:
                    break
                
                result.append(', ')
                continue
        
        result.append('], reversed=')
        result.append(repr(self._reversed))
        result.append(')')
        
        return ''.join(result)
    
    def __getstate__(self):
        return self._reversed
    
    def __setstate__(self,state):
        self._reversed=state
    
    def _get_reverse(self):
        return self._reversed
    def _set_reverse(self,value):
        if self._reversed==value:
            return
        self._reversed=value
        list.reverse(self)
    
    reverse=property(_get_reverse,_set_reverse)
    del _get_reverse,_set_reverse
    
    def add(self,value):
        index=self.relativeindex(value)
        if index==len(self):
            # If the the index is at the end, then we just list append it.
            list.append(self,value)
            return
        
        element=self[index]
        if element==value:
            # If the element is same as the current, we overwrite it.
            list.__setitem__(self,index,value)
            return
        
        # No more special cases, simply list insert it
        list.insert(self,index,value)
        return
    
    def remove(self, value):
        index=self.relativeindex(value)
        if index==len(self):
            # The element is not at self, leave
            return
        
        element=self[index]
        if element!=value:
            # The element is different as the already added one att the
            # correct position, leave.
            return
        
        # No more speccial case, remove it.
        list.__delitem__(self,index)
    
    def extend(self,other):
        ln=len(self)
        insert=list.insert
        bot=0
        if self._reversed:
            if type(self) is not type(other):
                other=sorted(other,reverse=True)
            elif not other._reversed:
                other=reversed(other)
            for value in other:
                top=ln
                while True:
                    if bot<top:
                        half=(bot+top)>>1
                        if self[half]>value:
                            bot=half+1
                        else:
                            top=half
                        continue
                    break
                insert(self,bot,value)
                ln+=1
        else:
            if type(self) is not type(other):
                other=sorted(other)
            elif other._reversed:
                other=reversed(other)
            for value in other:
                top=ln
                while True:
                    if bot<top:
                        half=(bot+top)>>1
                        if self[half]<value:
                            bot=half+1
                        else:
                            top=half
                        continue
                    break
                insert(self,bot,value)
                ln+=1
    
    def __contains__(self,value):
        index=self.relativeindex(value)
        if index==len(self):
            return False
        
        if self[index]==value:
            return True
        
        return False
    
    def index(self,value):
        index=self.relativeindex(value)
        if index==len(self) or self[index]!=value:
            raise ValueError(f'{value!r} is not in the {self.__class__.__name__}')
        return index
    
    def relativeindex(self,value):
        bot=0
        top=len(self)
        if self._reversed:
            while True:
                if bot<top:
                    half=(bot+top)>>1
                    if self[half]>value:
                        bot=half+1
                    else:
                        top=half
                    continue
                break
        else:
            while True:
                if bot<top:
                    half=(bot+top)>>1
                    if self[half]<value:
                        bot=half+1
                    else:
                        top=half
                    continue
                break
        return bot
    
    def keyedrelativeindex(self, value, key):
        bot=0
        top=len(self)
        if self._reversed:
            while True:
                if bot<top:
                    half=(bot+top)>>1
                    if key(self[half])>value:
                        bot=half+1
                    else:
                        top=half
                    continue
                break
        else:
            while True:
                if bot<top:
                    half=(bot+top)>>1
                    if key(self[half])<value:
                        bot=half+1
                    else:
                        top=half
                    continue
                break
        return bot
    
    def copy(self):
        new=list.__new__(type(self))
        new._reversed=self._reversed
        list.extend(new,self)
        return new
    
    def resort(self):
        list.sort(self,reverse=self._reversed)
    
    def get(self, value, key, default=None):
        index = self.keyedrelativeindex(value, key)
        if index==len(self):
            return default
        
        object_ = self[index]
        if key(object_)==value:
            return object_
        
        return default
    
    def pop(self, value, key, default=None):
        index = self.keyedrelativeindex(value, key)
        if index==len(self):
            return default
        
        object_ = self[index]
        if key(object_)==value:
            del self[index]
            return object_
        
        return default

def isweakreferable(object_):
    slots=getattr(type(object_), '__slots__',None)
    if (slots is not None) and ('__weakref__' in slots):
        return True
    
    if hasattr(object_,'__dict__'):
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

# speedup builtin stuff, Cpython is welcome
class WeakReferer(WeakrefType):
    __slots__ = ()
    if NEEDS_DUMMY_INIT:
        def __init__(self, *args, **kwargs):
            pass
    else:
        __init__ = object.__init__

class KeyedReferer(WeakReferer):
    __slots__ = ('key', )
    def __new__(cls, obj, callback, key, ):
        self = WeakReferer.__new__(cls, obj, callback)
        self.key=key
        return self

class WeakCallable(WeakReferer):
    __slots__ = ()
    def __call__(self, *args, **kwargs):
        self = WeakReferer.__call__(self)
        if self is None:
            return
        
        return self(*args, **kwargs)
    
    def is_alive(self):
        return (WeakReferer.__call__(self) is not None)

class weakmethod(WeakReferer, MethodLike):
    __slots__ = ('__func__')
    __reserved_argcount__ = 1
    
    def __new__(cls, obj, func, callback=None):
        self = WeakReferer.__new__(cls, obj, callback)
        self.__func__ = func
        return self
    
    @property
    def __self__(self):
        return WeakReferer.__call__(self)
    
    def __call__(self, *args, **kwargs):
        obj = WeakReferer.__call__(self)
        if obj is None:
            return
        return self.__func__(obj, *args, **kwargs)
    
    def is_alive(self):
        return (WeakReferer.__call__(self) is not None)
    
    def __getattr__(self,name):
        return getattr(self.__func__, name)
    
    @classmethod
    def from_method(cls, method_, callback=None):
        self = WeakReferer.__new__(cls, method_.__self__, callback)
        self.__func__ = method_.__func__
        return self

class _WeakValueDictionaryCallback(object):
    __slots__ = ('_parent', )
    def __new__(cls, parent):
        parent = WeakReferer(parent)
        self=object.__new__(cls)
        self._parent = parent
        return self
    
    def __call__(self, reference):
        parent = self._parent()
        if parent is None:
            return
        
        if parent._iterating:
            parent._pending_removals.add(reference)
        else:
            try:
                dict.__delitem__(parent, reference.key)
            except KeyError:
                pass

class _HybridValueDictionaryKeyIterator(object):
    __slots__ = ('_parent',)
    def __init__(self, parent):
        self._parent = parent
    
    def __iter__(self):
        parent = self._parent
        parent._iterating +=1
        pending_removals = parent._pending_removals
        
        try:
            for key, (value_weakreferable, value_or_reference) in dict.items(parent):
                if value_weakreferable and (value_or_reference() is None):
                    pending_removals.add(value_or_reference)
                    continue
                
                yield key
                continue
        
        finally:
            parent._iterating -=1
            parent._commit_removals()
    
    def __contains__(self, contains_key):
        return (contains_key in self._parent)
    
    def __len__(self):
        return len(self._parent)

class _HybridValueDictionaryValueIterator(object):
    __slots__ = ('_parent',)
    def __init__(self, parent):
        self._parent = parent
    
    def __iter__(self):
        parent = self._parent
        parent._iterating +=1
        pending_removals = parent._pending_removals
        
        try:
            for key, (value_weakreferable, value_or_reference) in dict.items(parent):
                if value_weakreferable:
                    value = value_or_reference()
                    if value is None:
                        pending_removals.add(value_or_reference)
                        continue
                else:
                    value = value_or_reference
                
                yield value
                continue
        
        finally:
            parent._iterating -=1
            parent._commit_removals()
    
    def __contains__(self, contains_value):
        parent = self._parent
        pending_removals = parent._pending_removals
        for key, (value_weakreferable, value_or_reference) in dict.items(parent):
            if value_weakreferable:
                value = value_or_reference()
                if value is None:
                    pending_removals.add(value_or_reference)
                    continue
            else:
                value = value_or_reference
            
            if value == contains_value:
                result=True
                break
        else:
            result=False
        
        parent._commit_removals()
        
        return result
    
    def __len__(self):
        return len(self._parent)

class _HybridValueDictionaryItemIterator(object):
    __slots__ = ('_parent',)
    def __init__(self, parent):
        self._parent = parent
    
    def __iter__(self):
        parent = self._parent
        parent._iterating +=1
        pending_removals = parent._pending_removals
        
        try:
            for key, (value_weakreferable, value_or_reference) in dict.items(parent):
                if value_weakreferable:
                    value = value_or_reference()
                    if value is None:
                        pending_removals.add(key)
                        continue
                else:
                    value = value_or_reference
                
                yield key, value
                continue
        
        finally:
            parent._iterating -=1
            parent._commit_removals()
    
    def __contains__(self, contains_item):
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
                    parent._pending_removals.add(value_or_reference)
                else:
                    dict.__delitem__(parent, contains_key)
                
                return False
        else:
            value = value_or_reference
        
        return (value == contains_value)
    
    def __len__(self):
        return len(self._parent)

class HybridValueDictionary(dict):
    __slots__ = ('__weakref__', '_pending_removals', '_iterating', '_callback')
    
    MAX_RERP_ELEMENT_LIMIT  = 50
    
    def _commit_removals(self):
        if self._iterating:
            return
        
        pending_removals = self._pending_removals
        while pending_removals:
            value_reference = pending_removals.pop()
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
        value_pair = dict.get(self, contains_key, None)
        if value_pair is None:
            return False
        
        value_weakreferable, value_or_reference = value_pair
        
        if value_weakreferable:
            if value_or_reference() is None:
                if self._iterating:
                    self._pending_removals.add(value_or_reference)
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
        value_weakreferable, value_or_reference = dict.__getitem__(self, key)
        if value_weakreferable:
            value = value_or_reference()
            if value is None:
                if self._iterating:
                    self._pending_removals.add(value_or_reference)
                else:
                    dict.__delitem__(self, key)
                
                raise KeyError(key)
        else:
            value = value_or_reference
        
        return value
    
    # __gt__ -> same
    # __hash__ -> same
    
    def __init__(self,iterable=None):
        self._pending_removals = set()
        self._iterating = 0
        self._callback = _WeakValueDictionaryCallback(self)
        if (iterable is not None):
            self.update(iterable)
    
    # __init_subclass__ -> same
    
    def __iter__(self):
        return iter(_HybridValueDictionaryKeyIterator(self))
    
    # __le__ -> same
    
    def __len__(self):
        return dict.__len__(self) - len(self._pending_removals)
    
    # __lt__ -> same
    # __ne__ -> same
    # __new__ -> same
    # __reduce__ -> we do not care
    # __redue_ex__ -> we do not care
    
    def __repr__(self):
        result = [self.__class__.__name__,'({']
        pending_removals = self._pending_removals
        if dict.__len__(self) - len(pending_removals):
            limit = self.MAX_RERP_ELEMENT_LIMIT
            collected = 0
            for key, (value_weakreferable, value_or_reference) in dict.items(self):
                if value_weakreferable:
                    value = value_or_reference()
                    if value is None:
                        pending_removals.add(value_or_reference)
                        continue
                else:
                    value = value_or_reference
                
                result.append(repr(key))
                result.append(': ')
                result.append(repr(value))
                result.append(', ')
                
                collected +=1
                if collected != limit:
                    continue
                
                leftover = dict.__len__(self) - len(pending_removals) - collected
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
        if isweakreferable(value):
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
        dict.clear(self)
        self._pending_removals.clear()
    
    def copy(self):
        new = dict.__new__(type(self))
        new._iterating = 0
        new._pending_removals = set()
        callback = _WeakValueDictionaryCallback(new)
        new._callback = callback
        
        pending_removals = self._pending_removals
        
        for key, (value_weakreferable, value_or_reference) in dict.items(self):
            if value_weakreferable:
                value = value_or_reference()
                if (value is None):
                    pending_removals.add(value_or_reference)
                    continue
                
                value_or_reference = KeyedReferer(value, callback, key)
            
            dict.__setitem__(new, key, (value_weakreferable, value_or_reference))
            continue
        
        self._commit_removals()
        
        return new
    
    def get(self, key, default=None):
        value_pair = dict.get(self, key, default)
        if value_pair is default:
            return default
        
        value_weakreferable, value_or_reference = value_pair
        
        if value_weakreferable:
            value = value_or_reference()
            if value is None:
                if self._iterating:
                    self._pending_removals.add(value_or_reference)
                else:
                    dict.__delitem__(self, key)
                
                return default
        else:
            value = value_or_reference
        
        return value
    
    def items(self):
        return _HybridValueDictionaryItemIterator(self)
    
    def keys(self):
        return _HybridValueDictionaryKeyIterator(self)
    
    # need goto for better codestyle
    def pop(self, key, default=_spaceholder):
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
    
    def update(self, other):
        if hasattr(type(other), 'items'):
            for key, value in other.items():
                self[key] = value
            return
        
        if hasattr(type(other), 'keys') and hasattr(type(other), '__getitem__'):
            for key in other.keys():
                value = other[key]
                self[key] = value
            return
        
        if hasattr(type(other), '__iter__'):
            index = -1
            for item in other:
                index = index+1
                
                try:
                    iterator=iter(item)
                except TypeError:
                    raise TypeError(f'Cannot convert dictionary update sequence element #{index} to a sequence.') from None
                
                try:
                    key = next(iterator)
                except StopIteration:
                    raise ValueError(f'Dictionary update sequence element #{index} has length {0}; 2 is required.') from None
                
                try:
                    value = next(iterator)
                except StopIteration:
                    raise ValueError(f'Dictionary update sequence element #{index} has length {1}; 2 is required.') from None
                
                try:
                    next(iterator)
                except StopIteration:
                    self[key]=value
                    continue
                
                length = 3
                for _ in iterator:
                    length +=1
                    if length>9000:
                        break
                
                if length>9000:
                    length='OVER 9000!'
                else:
                    length=repr(length)
                
                raise ValueError(f'Dictionary update sequence element #{index} has length {length}; 2 is required.')
            return
        
        raise TypeError(f'{other.__class__.__name__!r} object is not iterable')
    
    def values(self):
        return _HybridValueDictionaryValueIterator(self)

class _WeakValueDictionaryKeyIterator(object):
    __slots__ = ('_parent',)
    def __init__(self, parent):
        self._parent = parent
    
    def __iter__(self):
        parent = self._parent
        parent._iterating +=1
        pending_removals = parent._pending_removals
        
        try:
            for key, value_reference in dict.items(parent):
                if (value_reference() is None):
                    pending_removals.add(value_reference)
                    continue
                
                yield key
                continue
        
        finally:
            parent._iterating -=1
            parent._commit_removals()
    
    def __contains__(self, key):
        return (key in self._parent)
    
    def __len__(self):
        return len(self._parent)

class _WeakValueDictionaryValueIterator(object):
    __slots__ = ('_parent',)
    def __init__(self, parent):
        self._parent = parent
    
    def __iter__(self):
        parent = self._parent
        parent._iterating +=1
        pending_removals = parent._pending_removals
        
        try:
            for key, value_reference in dict.items(parent):
                value = value_reference()
                if (value is None):
                    pending_removals.add(value_reference)
                    continue
                
                yield value
                continue
        
        finally:
            parent._iterating -=1
            parent._commit_removals()
    
    def __contains__(self, contains_value):
        parent = self._parent
        pending_removals = parent._pending_removals
        for key, value_reference in dict.items(parent):
            value = value_reference()
            if (value is None):
                pending_removals.add(value_reference)
                continue
            
            if value == contains_value:
                result = True
                break
        
        else:
            result = False
        
        parent._commit_removals()
        
        return result
    
    def __len__(self):
        return len(self._parent)

class _WeakValueDictionaryItemIterator(object):
    __slots__ = ('_parent',)
    def __init__(self,parent):
        self._parent = parent
    
    def __iter__(self):
        parent = self._parent
        parent._iterating +=1
        pending_removals = parent._pending_removals
        
        try:
            for key, value_reference in dict.items(parent):
                value = value_reference()
                if (value is None):
                    pending_removals.add(value_reference)
                    continue
                
                yield key, value
                continue
        
        finally:
            parent._iterating -=1
            parent._commit_removals()
    
    def __contains__(self, contains_item):
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
                parent._pending_removals.add(value_reference)
            else:
                dict.__delitem__(parent, contains_key)
            
            return False
        
        return (value == contains_value)
    
    def __len__(self):
        return len(self._parent)

class WeakValueDictionary(dict):
    __slots__ = ('__weakref__', '_pending_removals', '_iterating', '_callback')
    
    MAX_RERP_ELEMENT_LIMIT  = 50
    
    def _commit_removals(self):
        if self._iterating:
            return
        
        pending_removals = self._pending_removals
        while pending_removals:
            value_reference = pending_removals.pop()
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
        value_reference = dict.get(self, key, None)
        if value_reference is None:
            return False
        
        value = value_reference()
        if (value is not None):
            return True
        
        if self._iterating:
            self._pending_removals.add(value_reference)
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
        value_reference = dict.__getitem__(self, key)
        value = value_reference()
        if (value is not None):
            return value
        
        if self._iterating:
            self._pending_removals.add(value_reference)
        else:
            dict.__delitem__(self, key)
        
        raise KeyError(key)
    
    # __gt__ -> same
    # __hash__ -> same
    
    def __init__(self, iterable=None):
        self._pending_removals=set()
        self._iterating=0
        self._callback = _WeakValueDictionaryCallback(self)
        if (iterable is not None):
            self.update(iterable)
    
    # __init_subclass__ -> same
    
    def __iter__(self):
        return iter(_WeakValueDictionaryKeyIterator(self))
    
    # __le__ -> same
    
    def __len__(self):
        return dict.__len__(self) - len(self._pending_removals)
    
    # __lt__ -> same
    # __ne__ -> same
    # __new__ -> same
    # __reduce__ -> we do not care
    # __redue_ex__ -> we do not care
    
    def __repr__(self):
        result = [self.__class__.__name__, '({']
        
        pending_removals = self._pending_removals
        if dict.__len__(self) - len(pending_removals):
            limit = self.MAX_RERP_ELEMENT_LIMIT
            collected = 0
            for key, value_reference in dict.items(self):
                value = value_reference()
                if (value is None):
                    pending_removals.add(value_reference)
                    continue
                
                result.append(repr(key))
                result.append(': ')
                result.append(repr(value))
                result.append(', ')
                
                collected +=1
                if collected != limit:
                    continue
                
                leftover = dict.__len__(self) - len(pending_removals) - collected
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
        dict.__setitem__(self, key, KeyedReferer(value, self._callback, key))
    
    # __sizeof__ -> same
    
    __str__ = __repr__
    
    # __subclasshook__ -> same
    
    def clear(self):
        dict.clear(self)
        self._pending_removals.clear()
    
    def copy(self):
        new = dict.__new__(type(self))
        new._pending_removals = set()
        callback = _WeakValueDictionaryCallback(new)
        new._callback = callback
        
        pending_removals = self._pending_removals
        
        for key, value_reference in dict.items(self):
            value = value_reference()
            if value is None:
                pending_removals.add(value_reference)
                continue
            
            dict.__setitem__(new, key, KeyedReferer(value, callback, key))
            continue
        
        self._commit_removals()
        
        return new
    
    def get(self, key, default=None):
        value_reference = dict.get(self, key, default)
        if value_reference is default:
            return default
        
        value = value_reference()
        if (value is not None):
            return value
        
        if self._iterating:
            self._pending_removals.add(value_reference)
        else:
            dict.__delitem__(self, key)
        
        return default
    
    def items(self):
        return _WeakValueDictionaryItemIterator(self)
    
    def keys(self):
        return _WeakValueDictionaryKeyIterator(self)
    
    def pop(self, key, default=_spaceholder):
        value_reference = dict.pop(self, key, _spaceholder)
        if (value_reference is not _spaceholder):
            value = value_reference()
            if (value is not None):
                return value
        
        if default is _spaceholder:
            raise KeyError(key)
        
        return default
    
    def popitem(self):
        while dict.__len__(self):
            key, value_reference = dict.popitem(self)
            value = value_reference()
            if (value is not None):
                return key, value
            
            continue
        
        raise KeyError('popitem(): dictionary is empty.')
    
    def setdefault(self, key, default):
        value_reference = dict.get(self, key, _spaceholder)
        if (value_reference is not _spaceholder):
            value = value_reference()
            if (value is not None):
                return value
        
        self[key] = default
        return default
    
    def update(self, other):
        if hasattr(type(other), 'items'):
            for key, value in other.items():
                self[key] = value
            return
        
        if hasattr(type(other), 'keys') and hasattr(type(other), '__getitem__'):
            for key in other.keys():
                value = other[key]
                self[key] = value
            return
        
        if hasattr(type(other), '__iter__'):
            index = -1
            for item in other:
                index = index+1
                
                try:
                    iterator=iter(item)
                except TypeError:
                    raise TypeError(f'Cannot convert dictionary update sequence element #{index} to a sequence.') from None
                
                try:
                    key = next(iterator)
                except StopIteration:
                    raise ValueError(f'Dictionary update sequence element #{index} has length {0}; 2 is required.') from None
                
                try:
                    value = next(iterator)
                except StopIteration:
                    raise ValueError(f'Dictionary update sequence element #{index} has length {1}; 2 is required.') from None
                
                try:
                    next(iterator)
                except StopIteration:
                    self[key] = value
                    continue
                
                length = 3
                for _ in iterator:
                    length +=1
                    if length>9000:
                        break
                
                if length>9000:
                    length='OVER 9000!'
                else:
                    length=repr(length)
                
                raise ValueError(f'Dictionary update sequence element #{index} has length {length}; 2 is required.')
            return
        
        raise TypeError(f'{other.__class__.__name__!r} object is not iterable')
    
    def values(self):
        return _WeakValueDictionaryValueIterator(self)

class _WeakKeyDictionaryCallback(object):
    __slots__ = ('_parent', )
    def __new__(cls, parent):
        parent = WeakReferer(parent)
        self=object.__new__(cls)
        self._parent = parent
        return self
    
    def __call__(self, reference):
        parent = self._parent()
        if parent is None:
            return
        
        if parent._iterating:
            parent._pending_removals.add(reference)
        else:
            try:
                dict.__delitem__(parent, reference)
            except KeyError:
                pass

class _WeakKeyDictionaryKeyIterator(object):
    __slots__ = ('_parent',)
    def __init__(self,parent):
        self._parent = parent
    
    def __iter__(self):
        parent = self._parent
        parent._iterating +=1
        pending_removals = parent._pending_removals
        
        try:
            for key_reference in dict.keys(parent):
                key = key_reference()
                if (key is None):
                    pending_removals.add(key_reference)
                    continue
                
                yield key
                continue
        
        finally:
            parent._iterating -=1
            parent._commit_removals()
    
    def __contains__(self, contains_key):
        return (contains_key in self._parent)
    
    def __len__(self):
        return len(self._parent)

class _WeakKeyDictionaryValueIterator(object):
    __slots__ = ('_parent',)
    def __init__(self,parent):
        self._parent = parent
    
    def __iter__(self):
        parent = self._parent
        parent._iterating +=1
        pending_removals = parent._pending_removals
        
        try:
            for key_reference, value in dict.items(parent):
                if (key_reference() is None):
                    pending_removals.add(key_reference)
                    continue
                
                yield value
                continue
        
        finally:
            parent._iterating -=1
            parent._commit_removals()
    
    def __contains__(self, contains_value):
        parent = self._parent
        pending_removals = parent._pending_removals
        for key_reference, value in dict.items(parent):
            if (key_reference() is None):
                pending_removals.add(key_reference)
                continue
            
            if value == contains_value:
                result = True
                break
        
        else:
            result = False
        
        parent._commit_removals()
        
        return result
    
    def __len__(self):
        return len(self._parent)

class _WeakKeyDictionaryItemIterator(object):
    __slots__ = ('_parent',)
    def __init__(self,parent):
        self._parent = parent
    
    def __iter__(self):
        parent = self._parent
        parent._iterating +=1
        pending_removals = parent._pending_removals
        
        try:
            for key_reference, value in dict.items(parent):
                key = key_reference()
                if (key is None):
                    pending_removals.add(key_reference)
                    continue
                
                yield key, value
                continue
        
        finally:
            parent._iterating -=1
            parent._commit_removals()
    
    def __contains__(self, contains_item):
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
        return len(self._parent)

class WeakKeyDictionary(dict):
    __slots__ = ('__weakref__', '_pending_removals', '_iterating', '_callback')
    
    MAX_RERP_ELEMENT_LIMIT  = 50
    
    def _commit_removals(self):
        if self._iterating:
            return
        
        pending_removals = self._pending_removals
        while pending_removals:
            key_reference = pending_removals.pop()
            
            try:
                dict.__delitem__(self, key_reference)
            except KeyError:
                return
        
    # __class__ -> same
    
    def __contains__(self, key):
        try:
            key = WeakReferer(key)
        except TypeError:
            return False
        
        return dict.__contains__(self, key)
    
    # __delattr__ -> same
    
    def __delitem__(self, key):
        dict.__delitem__(self, WeakReferer(key))
    
    # __dir__ -> same
    # __doc__ -> same
    # __eq__ -> same
    # __format__ -> same
    # __ge__ -> same
    # __getattribute__ -> same

    def __getitem__(self, key):
        return dict.__getitem__(self, WeakReferer(key))
    
    # __gt__ -> same
    # __hash__ -> same
    
    def __init__(self,iterable=None):
        self._pending_removals=set()
        self._iterating=0
        self._callback = _WeakKeyDictionaryCallback(self)
        if iterable is None:
            return
        
        self.update(iterable)
        return
    
    # __init_subclass__ -> same
    
    def __iter__(self):
        return iter(_WeakKeyDictionaryKeyIterator(self))
    
    # __le__ -> same
    
    def __len__(self):
        return dict.__len__(self) - len(self._pending_removals)
    
    # __lt__ -> same
    # __ne__ -> same
    # __new__ -> same
    # __reduce__ -> we do not care
    # __redue_ex__ -> we do not care
    
    def __repr__(self):
        result = [self.__class__.__name__, '({']
        
        pending_removals = self._pending_removals
        if dict.__len__(self) - len(pending_removals):
            limit = self.MAX_RERP_ELEMENT_LIMIT
            collected = 0
            for key_reference, value in dict.items(self):
                key = key_reference()
                if (key is None):
                    pending_removals.add(key_reference)
                    continue
                
                result.append(repr(key))
                result.append(': ')
                result.append(repr(value))
                result.append(', ')
                
                collected +=1
                if collected != limit:
                    continue
                
                leftover = dict.__len__(self) - len(pending_removals) - collected
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
        dict.__setitem__(self, WeakReferer(key, self._callback), value)
    
    # __sizeof__ -> same
    
    __str__ = __repr__
    
    # __subclasshook__ -> same
    
    def clear(self):
        dict.clear(self)
        self._pending_removals.clear()
    
    def copy(self):
        new = dict.__new__(type(self))
        new._pending_removals = set()
        callback = _WeakKeyDictionaryCallback(new)
        new._callback = callback
        
        pending_removals = self._pending_removals
        
        for key_reference, value in dict.items(self):
            key = key_reference()
            if key is None:
                pending_removals.add(key_reference)
                continue
            
            dict.__setitem__(new, WeakReferer(key, callback), value)
            continue
        
        self._commit_removals()
        
        return new
    
    def get(self, key, default=None):
        return dict.get(self, WeakReferer(key), default)
    
    def items(self):
        return _WeakKeyDictionaryItemIterator(self)
    
    def keys(self):
        return _WeakKeyDictionaryKeyIterator(self)
    
    def pop(self, key, default=_spaceholder):
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
        while dict.__len__(self):
            key_reference, value = dict.popitem(self)
            key = key_reference()
            
            if (key is not None):
                return key, value
            
            if self._iterating:
                self._pending_removals.add(key_reference)
            else:
                dict.__delitem__(self, key_reference)
            
            continue
        
        raise KeyError('popitem(): dictionary is empty.')
    
    def setdefault(self, key, default=None):
        value = dict.get(self, key, _spaceholder)
        if (value is not _spaceholder):
            return value
        
        self[key] = default
        return default
    
    def update(self, other):
        if hasattr(type(other), 'items'):
            for key, value in other.items():
                self[key] = value
            return
        
        if hasattr(type(other), 'keys') and hasattr(type(other), '__getitem__'):
            for key in other.keys():
                value = other[key]
                self[key] = value
            return
        
        if hasattr(type(other),'__iter__'):
            index = -1
            for item in other:
                index = index+1
                
                try:
                    iterator=iter(item)
                except TypeError:
                    raise TypeError(f'Cannot convert dictionary update sequence element #{index} to a sequence.') from None
                
                try:
                    key = next(iterator)
                except StopIteration:
                    raise ValueError(f'Dictionary update sequence element #{index} has length {0}; 2 is required.') from None
                
                try:
                    value = next(iterator)
                except StopIteration:
                    raise ValueError(f'Dictionary update sequence element #{index} has length {1}; 2 is required.') from None
                
                try:
                    next(iterator)
                except StopIteration:
                    self[key] = value
                    continue
                
                length = 3
                for _ in iterator:
                    length +=1
                    if length>9000:
                        break
                
                if length>9000:
                    length='OVER 9000!'
                else:
                    length=repr(length)
                
                raise ValueError(f'Dictionary update sequence element #{index} has length {length}; 2 is required.')
            return
        
        raise TypeError(f'{other.__class__.__name__!r} object is not iterable')
    
    def values(self):
        return _WeakKeyDictionaryValueIterator(self)

class _WeakMapCallback(object):
    __slots__ = ('_parent', )
    def __new__(cls, parent):
        parent = WeakReferer(parent)
        self = object.__new__(cls)
        self._parent = parent
        return self
    
    def __call__(self, reference):
        parent = self._parent()
        if parent is None:
            return
        
        if parent._iterating:
            parent._pending_removals.add(reference)
        else:
            try:
                dict.__delitem__(parent, reference)
            except KeyError:
                pass

class _WeakMapIterator(object):
    __slots__ = ('_parent', )
    def __init__(self, parent):
        self._parent=parent
    
    def __iter__(self):
        parent = self._parent
        parent._iterating +=1
        pending_removals = parent._pending_removals
        
        try:
            for reference in dict.__iter__(parent):
                key = reference()
                if (key is None):
                    pending_removals.add(reference)
                    continue
                
                yield key
                continue
        
        finally:
            parent._iterating -=1
            parent._commit_removals()
    
    def __contains__(self, key):
        return (key in self._parent)
    
    def __len__(self):
        return len(self._parent)

class WeakMap(dict):
    __slots__ = ('__weakref__', '_pending_removals', '_iterating', '_callback')
    
    MAX_RERP_ELEMENT_LIMIT = 50
    
    def _commit_removals(self):
        if self._iterating:
            return
        
        pending_removals = self._pending_removals
        while pending_removals:
            reference = pending_removals.pop()
            
            try:
                dict.__delitem__(self, reference)
            except KeyError:
                pass
    
    # __class__ -> same
    
    def __contains__(self, key):
        try:
            reference = WeakReferer(key)
        except TypeError:
            return False
        
        return dict.__contains__(self, reference)
    
    # __delattr__ -> same
    
    def __delitem__(self, key):
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
        try:
            reference = WeakReferer(key)
        except TypeError:
            raise KeyError(key) from None
        
        return dict.__getitem__(self, reference)
    
    # __gt__ -> same
    # __hash__ -> same
    
    def __init__(self,iterable=None):
        self._pending_removals=set()
        self._iterating=0
        self._callback=_WeakMapCallback(self)
        if (iterable is not None):
            self.update(iterable)
    
    # __init_subclass__ -> same
    
    def __iter__(self):
        return iter(_WeakMapIterator(self))
    
    # __le__ -> same
    
    def __len__(self):
        return dict.__len__(self) - len(self._pending_removals)
    
    # __lt__ -> same
    # __ne__ -> same
    # __new__ -> same
    # __reduce__ -> we do not care
    # __redue_ex__ -> we do not care
    
    def __repr__(self):
        result = [self.__class__.__name__, '({']
        if dict.__len__(self) - len(self._pending_removals):
            limit = self.MAX_RERP_ELEMENT_LIMIT
            collected = 0
            pending_removals = self._pending_removals
            for reference in dict.__iter__(self):
                key = reference()
                if (key is None):
                    pending_removals.add(reference)
                    continue
                
                result.append(repr(key))
                result.append(', ')
                
                collected +=1
                if collected != limit:
                    continue
                
                leftover = dict.__len__(self) - len(pending_removals) - collected
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
        dict.clear(self)
        self._pending_removals.clear()
    
    def copy(self):
        new = dict.__new__(type(self))
        new._iterating = False
        new._pending_removals = set()
        new._callback = callback = _WeakMapCallback(new)
        
        pending_removals = self._pending_removals
        
        for reference in dict.__iter__(self):
            key = reference()
            if (key is None):
                pending_removals.add(reference)
                continue
            
            reference = WeakReferer(key, callback)
            dict.__setitem__(new, reference, reference)
            continue
        
        self._commit_removals()
        
        return new
    
    def get(self, key, default=None):
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
            self._pending_removals.add(real_reference)
        else:
            dict.__delitem__(self, real_reference)
        
        return default
    
    items = RemovedDescriptor()
    keys = RemovedDescriptor()
    
    def pop(self, key, default=_spaceholder):
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
                    self._pending_removals.add(real_reference)
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
