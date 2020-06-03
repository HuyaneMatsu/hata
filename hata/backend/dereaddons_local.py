# -*- coding: utf-8 -*-
__all__ = ('BaseMethodDescriptor', 'KeepType', 'KeyedReferer', 'RemoveMeta', 'WeakCallable', 'WeakMap', 'WeakReferer',
    'alchemy_incendiary', 'any_to_any', 'cached_property', 'isweakreferable', 'listdifference', 'methodize',
    'modulize', 'multidict', 'multidict_titled', 'titledstr', 'weakmethod', )

from types import \
    MethodType              as method, \
    FunctionType            as function, \
    MappingProxyType        as mappingproxy, \
    GetSetDescriptorType    as getset_descriptor, \
    ModuleType              as module

NoneType = type(None)

import sys, weakref

class RemoveMeta(type):
    def __new__(meta, name, bases, values, remove=None):
        if (remove is not None) and remove:
            for name_ in remove:
                values[name_]=Removed(name_)
        
        return type.__new__(meta, name, bases, values)

class Removed:
    __slots__=('name',)
    def __init__(self,name):
        self.name=name
    
    def __get__(self,obj,objtype=None):
        if obj is None:
            raise AttributeError(f"type object '{objtype.__name__}' has no attribute '{self.name}'")
        raise AttributeError(f"'{obj.__class__.__name__}' object has no attribute '{self.name}'")
    
    def __set__(self, obj, value):
        raise AttributeError(self.name)
    
    def __delete__(self,obj):
        raise AttributeError(self.name)

def any_to_any(v1,v2):
    for v in v1:
        if v in v2:
            return True
    return False

class autoposlist(list, metaclass=RemoveMeta, remove=['extend', '__add__', '__iadd__', '__radd__', '__mul__',
        '__imul__', '__rmul__', '__setitem__', 'insert', 'sort', 'reverse']):
    __slots__=()
    
    def __init__(self):
        list.__init__(self)
    
    def append(self,value):
        index=value.position
        ln=len(self)
        while True:
            if index==ln:
                break
            self[index].position+=1
            index+=1
        list.insert(self,value.position,value)

    def append_unchecked(self,value):
        list.insert(self,self.index(value),value)

    def append_halfchecked(self,value):
        index=self.index(value)
        list.insert(self,index,value)
        ln=len(self)
        last_position=value.position
        while True:
            index+=1
            if index>=ln:
                break
            value=self[index]
            position=value.position
            if position!=last_position:
                break
            last_position+=1
            value.position=last_position
            
    def index(self,value):
        bot=0
        top=len(self)
        if not top:
            return 0
        while True:
            if bot<top:
                half=(bot+top)>>1
                if self[half].position<value.position:
                    bot=half+1
                else:
                    top=half
                continue
            return bot

    def remove(self,value):
        index=self.index(value)
        if self[index]==value:
            del self[index]
        else:
            raise ValueError(f'Searched for {value}, but found {self[index]}')
    def __contains__(self,value):
        return self[self.index(value)]==value
    def change_on_switch(self,value,new_position,key=None):
        ln=len(self)
        if new_position>=ln:
            new_position=ln-1
        elif new_position<0:
            new_position=0
        old_position=value.position
        if self[old_position]!=value:
            raise ValueError('The object is not in the list')
        result=[]
        if new_position==old_position:
            return result
        if new_position<old_position:
            index=new_position
            limit=old_position
            change=+1
        else:
            index=old_position+1
            limit=new_position+1
            change=-1
        if key is None:
            while True:
                actual=self[index]
                result.append((actual,actual.position+change),)
                index+=1
                if index==limit:
                    break
            if change>0:
                result.insert(0,(value,new_position),)
            else:
                result.append((value,new_position),)
        else:
            while True:
                 actual=self[index]
                 result.append(key(actual,actual.position+change),)
                 index+=1
                 if index==limit:
                     break
            if change>0:
                result.insert(0,key(value,new_position),)
            else:
                result.append(key(value,new_position),)
        return result
    def __delitem__(self,index):
        list.__delitem__(self,index)
        ln=len(self)
        while True:
            if index==ln:
                break
            self[index].position-=1
            index+=1

    def switch(self,value,new_position):
        #discord dev safe
        value.position=new_position
        list.sort(self)
        
##        ln=len(self)
##        old_position=value.position
##        if old_position<0 or old_position>=ln:
##            raise IndexError(old_position)
##        if new_position<0 or new_position>=ln:
##            raise IndexError(new_position)
##        if new_position==old_position:
##            return
##        if new_position<old_position:
##            index=new_position
##            limit=old_position
##            change=+1
##        else:
##            index=old_position+1
##            limit=new_position+1
##            change=-1
##        while True:
##            if index==limit:
##                break
##            self[index].position+=change
##            index+=1
##        list.pop(self,old_position)
##        value.position=new_position
##        list.insert(self,new_position,value)
    def pop(self,index=None):
        if index is None:
            return list.pop(self)
        value=list.pop(self,index)
        ln=len(self)
        while True:
            self[index].position-=1
            index+=1
            if index==ln:
                break
        return value
    def change_on_remove(self,value,key=None):
        index=self.index(value)
        if self[index]==value:
            return self._change_on_del(index,key)
        else:
            raise ValueError(f'Searched for {self[index]}, but found {value}')
    def change_on_del(self,index,key=None):
        if index<0 or index>=len(self):
            raise ValueError('List index out of range.')
        return self._change_on_del(index,key)
    def change_on_pop(self,index=None,key=None):
        if index is None:
            #index=len(self)-1
            return []
        if index<0 or index>=len(self):
            raise ValueError('List index out of range.')
        return self._change_on_del(index,key)
    def _change_on_del(self,index,key):
        result=[]
        index+=1
        ln=len(self)
        if key:
            while True:
                if index==ln:
                    break
                value=self[index]
                result.append(key(value,value.position-1))
                index+=1

        else:
            while True:
                if index==ln:
                    break
                value=self[index]
                result.append((value,value.position-1),)
                index+=1

        return result
    def change_on_append(self,value,key=None):
        position=value.position
        ln=len(self)
        result=[]
        if position>ln:
            position=ln
        if key is None:
            while True:
                result.append((value,position),)
                if position==ln:
                    break
                value=self[position]
                position+=1
        else:
            while True:
                result.append(key(value,position))
                if position==ln:
                    break
                value=self[position]
                position+=1
                
        return result
    
    def where(self,key):
        for value in self:
            if key(value):
                return value
        raise LookupError(key)

class weakposlist(list):
    __slots__   = autoposlist.__slots__
    __init__    = autoposlist.__init__
    def index(self,value):
        bot=0
        top=len(self)
        if not top:
            return 0
        while True:
            if bot<top:
                half=(bot+top)>>1
                if self[half]<value:
                    bot=half+1
                else:
                    top=half
                continue
            return bot
    append      = autoposlist.append_unchecked
    remove      = autoposlist.remove
    __contains__= autoposlist.__contains__
    where       = autoposlist.where

    #no append_unchecked(self,value)
        
    #list's __delitem__(self,index)
    #list's pop(self,index=None)
    
    def switch(self,value,new_position):
        value.position=new_position
        self.sort()

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
    __slots__=('parent',)
    def __init__(self,parent):
        self.parent=parent
    def __len__(self):
        return len(self.parent)
    def __iter__(self):
        for key, values in dict.items(self.parent):
            for value in values:
                yield key,value
    
    def __contains__(self,item):
        parent=self.parent
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
        for values in dict.values(self.parent):
            yield from values
    def __contains__(self,value):
        for values in dict.values(self.parent):
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

    @classmethod
    def bypass_titling(cls,value='',encoding=sys.getdefaultencoding(),errors='strict'):
        if type(value) is cls:
            return value
        if isinstance(value,(bytes, bytearray, memoryview)):
            value=str(value,encoding,errors)
        elif isinstance(value,str):
            pass
        else:
            value=str(value)
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
    __slots__=('func','__name__',)
    #Use as a class method decorator.  It operates almost exactly like
    #the Python `@property` decorator, but it puts the result of the
    #method it decorates into the instance dict after the first call,
    #effectively replacing the function it decorates with an instance
    #variable.
    def __init__(self, func):
        self.func = func
        self.__name__ = func.__name__
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        value = obj._cache.get(self.__name__,_spaceholder)
        if value is _spaceholder:
            value = self.func(obj)
            obj._cache[self.__name__] = value
        
        return value
    
    def __set__(self, obj, value):
        raise AttributeError('can\'t set attribute')

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
    __slots__=('__base__', '__func__', '__self__', )
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
        return self.func.__doc__

class BaseMethodDescriptor(object):
    __slots__=('func',)
    def __init__(self, func):
        self.func = func
    
    def __get__(self, obj, type_=None):
        if type_ is None:
            type_ = type(obj)
        
        return basemethod(self.func, type_, obj)
    
    def __set__(self, obj, value):
        raise AttributeError('can\'t set attribute')
    
    def __delete__(self, obj):
        raise AttributeError('can\'t delete attribute')

# This 2 type can be function
wrapper_descriptor=type(object.__ne__)
method_descriptor=type(object.__format__)

DO_NOT_MODULIZE_TYPES=[mappingproxy, getset_descriptor, ]

if wrapper_descriptor is not function:
    DO_NOT_MODULIZE_TYPES.append(wrapper_descriptor)

if method_descriptor is not function:
    DO_NOT_MODULIZE_TYPES.append(method_descriptor)

DO_NOT_MODULIZE_TYPES = tuple(DO_NOT_MODULIZE_TYPES)

del mappingproxy
del getset_descriptor
del wrapper_descriptor
del method_descriptor

def modulize(klass):
    if not isinstance(klass,type):
        raise TypeError('Only types can be modulized')
    result=module(klass.__name__)
    for name in type.__dir__(klass):
        if name.startswith('__') and name.endswith('__') and name!='__doc__':
            continue
        
        value=type.__getattribute__(klass,name)
        if type(value) in DO_NOT_MODULIZE_TYPES:
            continue
        
        module.__setattr__(result,name,value)
    return result
    
class methodize(object):
    __slots__=('klass',)
    def __init__(self,klass):
        self.klass=klass
    
    def __get__(self, obj, type_=None):
        if obj is None:
            return self.klass
        return method(self.klass, obj)
    
    def __set__(self,obj,value):
        raise AttributeError('can\'t set attribute')
    
    def __delete__(self,obj):
        raise AttributeError('can\'t delete attribute')

class sortedlist(list,metaclass=RemoveMeta, remove=['__setitem__', 'insert', 'sort', '__add__', '__radd__', '__iadd__',
        '__mul__', '__rmul__', '__imul__', 'append', ]):
    __slots__ = ('_reversed', )
    
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
class WeakReferer(weakref.ref):
    __slots__ = ()
    if NEEDS_DUMMY_INIT:
        def __init__(self, *args, **kwargs):
            pass
    else:
        __init__ = object.__init__

weakref.ref = WeakReferer

class KeyedReferer(WeakReferer):
    __slots__ = ('key', )
    def __new__(cls, obj, callback, key, ):
        self = WeakReferer.__new__(cls, obj, callback)
        self.key=key
        return self

weakref.KeyedRef = KeyedReferer

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

class _HybridValueDictionaryCallback(object):
    __slots__ = ('parent', )
    def __new__(cls, parent):
        self=object.__new__(cls)
        self.parent=WeakReferer(parent)
        return self
    
    def __call__(self, reference):
        parent = self.parent()
        if parent is None:
            return
        
        key=reference.key
        if parent._iterating:
            parent._pending_removals.add(key)
        else:
            dict.__delitem__(parent,key)

class _HybridValueDictionaryKeyIterator(object):
    __slots__ = ('parent',)
    def __init__(self,parent):
        self.parent = parent
    
    def __iter__(self):
        parent = self.parent
        parent._iterating +=1
        pending_removals = parent._pending_removals
        
        try:
            for key, value in dict.items(parent):
                if not value[0]:
                    yield key
                    continue
                
                if (value[1]() is not None):
                    yield key
                    continue
                
                pending_removals.add(key)
                continue
        
        finally:
            iterating = parent._iterating-1
            parent._iterating = iterating
            if iterating:
                return
            
            while pending_removals:
                key = pending_removals.pop()
                dict.__delitem__(self,key)
    
    def __contains__(self, key):
        return (key in self.parent)
    
    def __len__(self):
        return len(self.parent)

class _HybridValueDictionaryValueIterator(object):
    __slots__ = ('parent',)
    def __init__(self,parent):
        self.parent = parent
    
    def __iter__(self):
        parent = self.parent
        parent._iterating +=1
        pending_removals = parent._pending_removals
        
        try:
            for key, (weakreferable, reference) in dict.items(parent):
                if not weakreferable:
                    yield reference
                    continue
                
                reference=reference()
                if (reference is not None):
                    yield reference
                    continue
                
                pending_removals.add(key)
                continue
        
        finally:
            iterating = parent._iterating-1
            parent._iterating = iterating
            if iterating:
                return
            
            while pending_removals:
                key = pending_removals.pop()
                dict.__delitem__(self,key)
    
    def __contains__(self, value):
        parent = self.parent
        pending_removals = parent._pending_removals
        for key, (weakreferable, reference) in dict.items(parent):
            if not weakreferable:
                if reference!=value:
                    continue
                
                result=True
                break
            
            reference=reference()
            if (reference is not None):
                if reference!=value:
                    continue
                
                result=True
                break
            
            pending_removals.add(key)
            continue
        else:
            result=False
        
        if parent._iterating:
            return result
        
        while pending_removals:
            key = pending_removals.pop()
            dict.__delitem__(self,key)
        
        return result
    
    def __len__(self):
        return len(self.parent)
    
class _HybridValueDictionaryItemIterator(object):
    __slots__ = ('parent',)
    def __init__(self,parent):
        self.parent = parent
    
    def __iter__(self):
        parent = self.parent
        parent._iterating +=1
        pending_removals = parent._pending_removals
        
        try:
            for key, (weakreferable, reference) in dict.items(parent):
                if not weakreferable:
                    yield key, reference
                    continue
                
                reference=reference()
                if (reference is not None):
                    yield key, reference
                    continue
                
                pending_removals.add(key)
                continue
        
        finally:
            iterating = parent._iterating-1
            parent._iterating = iterating
            if iterating:
                return
            
            while pending_removals:
                key = pending_removals.pop()
                dict.__delitem__(self,key)
    
    def __contains__(self, item):
        if not isinstance(item,tuple):
            return False
        
        if len(item)!=2:
            return False
        
        parent = self.parent
        pending_removals = parent._pending_removals
        item_key, item_value = item
        
        for key, (weakreferable, reference) in dict.items(parent):
            if key!=item_key:
                continue
            
            if not weakreferable:
                if reference!=item_value:
                    continue
                    
                result=True
                break
                
            reference=reference()
            if (reference is not None):
                if reference!=item_value:
                    continue
                
                result=True
                break
            
            pending_removals.add(key)
            continue
        else:
            result=False
        
        if parent._iterating:
            return result
        
        while pending_removals:
            key = pending_removals.pop()
            dict.__delitem__(self,key)
        
        return result
    
    def __len__(self):
        return len(self.parent)

class HybridValueDictionary(dict):
    __slots__ = ('__weakref__', '_pending_removals', '_iterating', '_callback')
    # __class__ -> same
    
    def __contains__(self, key):
        value = dict.get(self,key,None)
        if value is None:
            return False
        
        if not value[0]:
            return True
        
        reference = value[1]()
        if (reference is not None):
            return True
        
        if self._iterating:
            self._pending_removals.add(key)
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
        weakreferable, reference = dict.__getitem__(self,key)
        if not weakreferable:
            return reference
        
        reference = reference()
        if (reference is not None):
            return reference
        
        if self._iterating:
            self._pending_removals.add(key)
        else:
            dict.__delitem__(self, key)
        
        raise KeyError(key)
    
    # __gt__ -> same
    # __hash__ -> same
    
    def __init__(self,iterable=None):
        self._pending_removals=set()
        self._iterating=0
        self._callback=_HybridValueDictionaryCallback(self)
        if iterable is None:
            return
        
        self.update(iterable)
        return
    
    # __init_subclass__ -> same
    
    def __iter__(self):
        return iter(_HybridValueDictionaryKeyIterator(self))
    
    # __le__ -> same
    
    def __len__(self):
        return dict.__len__(self)-len(self._pending_removals)
    
    # __lt__ -> same
    # __ne__ -> same
    # __new__ -> same
    # __reduce__ -> we do not care
    # __redue_ex__ -> we do not care
    
    def __repr__(self):
        result = [self.__class__.__name__,'({']
        if self:
            pending_removals=self._pending_removals
            for key, (weakreferable, reference) in dict.items(self):
                if weakreferable:
                    reference = reference()
                    if reference is None:
                        pending_removals.add(key)
                        continue
                
                result.append(repr(key))
                result.append(': ')
                result.append(repr(reference))
                result.append(', ')
            
            if len(result)>2:
                result[-1]='})'
            else:
                result.append('})')
            
            if not self._iterating:
                while pending_removals:
                    key = pending_removals.pop()
                    dict.__delitem__(self, key)
        else:
            result.append('})')
        
        return ''.join(result)
    
    #__setattr__ -> same
    
    def __setitem__(self, key, value):
        if isweakreferable(value):
            weakreferable = True
            reference = KeyedReferer(value,self._callback,key)
        else:
            weakreferable = False
            reference = value
        
        dict.__setitem__(self, key, (weakreferable, reference), )
    
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
        callback = _HybridValueDictionaryCallback(new)
        new._callback = callback
        
        pending_removals = self._pending_removals
        
        for key, value in dict.items(self):
            if value[0]:
                value = value[1]()
                
                if (value is None):
                    pending_removals.add(key)
                    continue
                
                value = (True, KeyedReferer(value, callback, key), )
            
            dict.__setitem__(new, key, value)
            continue
        
        if not self._iterating:
            while pending_removals:
                key = pending_removals.pop()
                dict.__delitem__(self, key)
        
        return new
    
    def get(self, key, default=None):
        value = dict.get(self,default,None)
        if value is None:
            return default
        
        if not value[0]:
            return value[1]
        
        reference = value[1]()
        if (reference is not None):
            return reference
        
        if self._iterating:
            self._pending_removals.add(key)
        else:
            dict.__delitem__(self, key)
        
        return default

    def items(self):
        return _HybridValueDictionaryItemIterator(self)
    
    def keys(self):
        return _HybridValueDictionaryKeyIterator(self)
    
    def pop(self, key, default=_spaceholder):
        value = dict.pop(self, key, _spaceholder)
        if (value is not _spaceholder):
            if not value[0]:
                return value[1]
            
            reference = value[1]()
            if (reference is not None):
                return reference
            
            if self._iterating:
                self._pending_removals.add(key)
            else:
                dict.__delitem__(self, key)
        
        if default is _spaceholder:
            raise KeyError(key)
        return default
    
    def popitem(self):
        while dict.__len__(self):
            key, value = dict.popitem(self)
            if not value[0]:
                return key, value[1]
            
            value = value[1]()
            if (value is not None):
                return key, value
            
            if self._iterating:
                self._pending_removals.add(key)
            else:
                dict.__delitem__(self, key)
            
            continue
        
        raise KeyError('popitem(): dictionary is empty.')
    
    def setdefault(self, key, default=None):
        value = dict.get(self, key, None)
        if (value is not None):
            if not value[0]:
                return value[1]
            
            reference = value[1]()
            if (reference is not None):
                return reference
        
        self[key]=default
        return default
    
    def update(self, other):
        if hasattr(type(other),'items'):
            for key, value in other.items():
                self[key]=value
            return
        
        if hasattr(type(other),'keys') and hasattr(type(other),'__getitem__'):
            for key in other.keys():
                value = other[key]
                self[key]=value
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

class _WeakMapCallback(object):
    __slots__ = ('parent', )
    def __new__(cls, parent):
        self = object.__new__(cls)
        self.parent = WeakReferer(parent)
        return self
    
    def __call__(self, reference):
        parent = self.parent()
        if parent is None:
            return
        
        if parent._iterating:
            parent._pending_removals.add(reference)
        else:
            dict.__delitem__(parent,reference)

class _WeakMapIterator(object):
    __slots__ = ('parent', )
    def __init__(self, parent):
        self.parent=parent
    
    def __iter__(self):
        parent = self.parent
        parent._iterating +=1
        pending_removals = parent._pending_removals
        
        try:
            for reference in dict.__iter__(parent):
                key = reference()
                if (key is not None):
                    yield key
                    continue
                
                pending_removals.add(reference)
                continue
        
        finally:
            iterating = parent._iterating-1
            parent._iterating = iterating
            if iterating:
                return
            
            while pending_removals:
                reference = pending_removals.pop()
                dict.__delitem__(self, reference)
    
    def __contains__(self, key):
        return (key in self.parent)
    
    def __len__(self):
        return len(self.parent)

class WeakMap(dict, metaclass=RemoveMeta, remove=['__setitem__', 'items', 'keys', 'popitem', 'setdefault', 'update',
        'values', ]):
    __slots__ = ('__weakref__', '_pending_removals', '_iterating', '_callback')
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
    # __eq__ -> same
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
        if iterable is None:
            return
        
        self.update(iterable)
        return
    
    # __init_subclass__ -> same
    
    def __iter__(self):
        return iter(_WeakMapIterator(self))
    
    # __le__ -> same
    
    def __len__(self):
        return dict.__len__(self)-len(self._pending_removals)
    
    # __lt__ -> same
    # __ne__ -> same
    # __new__ -> same
    # __reduce__ -> we do not care
    # __redue_ex__ -> we do not care
    
    def __repr__(self):
        result = [self.__class__.__name__,'({']
        if self:
            pending_removals=self._pending_removals
            for reference in dict.__iter__(self):
                key = reference()
                if (key is None):
                    pending_removals.add(reference)
                    continue
                
                result.append(repr(key))
                result.append(', ')
                continue
            
            if len(result)>2:
                result[-1]='})'
            else:
                result.append('})')
            
            if not self._iterating:
                while pending_removals:
                    reference = pending_removals.pop()
                    dict.__delitem__(self, reference)
        else:
            result.append('})')
        
        return ''.join(result)
    
    # __setattr__ -> same
    # __setitem__ -> removed
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
        
        if not self._iterating:
            while pending_removals:
                reference = pending_removals.pop()
                dict.__delitem__(self, reference)
        
        return new
    
    def get(self, key, default=None):
        try:
            reference = WeakReferer(key)
        except TypeError:
            return default
        
        real_reference = dict.get(self, reference, None)
        if real_reference is None:
            return default
        
        real_key = real_reference()
        if (real_key is not None):
            return real_key
        
        if self._iterating:
            self._pending_removals.add(real_reference)
        else:
            dict.__delitem__(self, real_reference)
        
        return default
    
    # items -> removed
    # keys -> removed
    
    def pop(self, key, default=_spaceholder):
        try:
            reference = WeakReferer(key)
        except TypeError:
            pass
        else:
            real_reference = dict.pop(self, reference, _spaceholder)
            if (real_reference is not default):
                real_key = real_reference()
                if (real_key is None):
                    if self._iterating:
                        self._pending_removals.add(real_reference)
                    else:
                        dict.__delitem__(self, real_reference)
                else:
                    return real_key
        
        if default is _spaceholder:
            raise KeyError(key)
        else:
            return default
    
    # popitem -> removed
    # setdefault -> removed
    # update -> removed
    # values -> removed
    
    def set(self, key):
        reference = WeakReferer(key, self._callback)
        real_reference = dict.get(self, reference, None)
        if (real_reference is not None):
            real_key = real_reference()
            if real_key is None:
                if self._iterating:
                    self._pending_removals.add(real_reference)
                else:
                    dict.__delitem__(self, real_reference)
            else:
                return real_key
        
        dict.__setitem__(self, reference, reference)
        return key

del weakref
del dummy_init_tester
