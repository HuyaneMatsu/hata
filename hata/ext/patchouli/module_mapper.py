# -*- coding: utf-8 -*-
__all__ = ('AttributeUnitBase', 'ClassAttributeUnit', 'FolderedUnit', 'FunctionUnit', 'InstanceAttributeUnit', \
    'MAPPED_OBJECTS', 'ModuleUnit', 'ObjectedUnitBase', 'PropertyUnit', 'TypeUnit', 'UnitBase', 'map_module', )

import sys, re
from types import FunctionType, BuiltinFunctionType, BuiltinMethodType, MethodType, GetSetDescriptorType, MemberDescriptorType

from ...backend.dereaddons_local import cached_property, MethodLike, module_property
from .qualpath import QualPath
from .parser import DocString
from .builder_text import serialize_docs_embed_sized, serialize_docs, serialize_docs_source_text

WrapperDescriptorType= object.__eq__.__class__
MethodDescriptorType = int.bit_length.__class__
SlotWrapperType = object.__lt__.__class__

METHOD_TYPES = {
    BuiltinMethodType,
    MethodType,
    WrapperDescriptorType,
    MethodDescriptorType,
    MethodLike,
        }

FUNCTION_TYPES = {
    *METHOD_TYPES,
    FunctionType,
    BuiltinFunctionType,
    BuiltinMethodType,
        }

IGNORED_TYPES = {
    type,
    object,
        }

IGNORED_CLASS_ATTRIBUTE_TYPES = {
    *METHOD_TYPES,
        }

if (SlotWrapperType is not FunctionType) and (SlotWrapperType is not MethodType):
    IGNORED_CLASS_ATTRIBUTE_TYPES.add(SlotWrapperType)

IGNORED_FUNCTIONS = set()

converted = None
for func in (
        object.__delattr__,
        object.__dir__,
        object.__eq__,
        object.__format__,
        object.__ge__,
        object.__getattribute__,
        object.__gt__,
        object.__hash__,
        object.__init__,
        object.__init_subclass__,
        object.__le__,
        object.__lt__,
        object.__ne__,
        object.__new__,
        object.__reduce__,
        object.__reduce_ex__,
        object.__repr__,
        object.__setattr__,
        getattr(object, '__sizeof__', None), # Not present in Pypy
        object.__str__,
        object.__subclasshook__,
        type.__call__,
        type.__delattr__,
        type.__dir__,
        type.__eq__,
        type.__format__,
        type.__ge__,
        type.__getattribute__,
        type.__gt__,
        type.__hash__,
        type.__init__,
        type.__init_subclass__,
        type.__instancecheck__,
        type.__le__,
        type.__lt__,
        type.__ne__,
        type.__new__,
        type.__prepare__,
        type.__reduce__,
        type.__reduce_ex__,
        type.__repr__,
        type.__setattr__,
        getattr(type, '__sizeof__', None), # Not present in Pypy
        type.__str__,
        type.__subclasscheck__,
        type.__subclasses__,
        type.__subclasshook__,
        type.mro,
            ):
    
    if func is None:
        continue
    
    if (func.__class__ in METHOD_TYPES):
        converted = getattr(func, '__func__', None)
        if (converted is not None):
            func = converted
    
    IGNORED_FUNCTIONS.add(func)

del func, converted

PROPERTY_TYPES = {
    property,
    cached_property,
    module_property,
        }

ATTRIBUTE_TYPES = {
    GetSetDescriptorType,
    MemberDescriptorType,
        }

IGNORED_CLASS_ATTRIBUTE_NAMES = {
    '__ne__',
    '__module__',
    '__str__',
    '__format__',
    '__lt__',
    '__gt__',
    '__le__',
    '__ge__',
    '__eq__',
    '__reduce__',
    '__reduce_ex__',
    '__setattr__',
    '__getattr__',
    '__delattr__',
    '__slots__',
    '__getattribute__',
    '__repr__',
    '__doc__',
    '__dir__',
    '__sizeof__',
    '__dict__',
    '__new__',
    '__init__',
    '__hash__',
    '__reversed__',
    '__getitem__',
    '__setitem__',
    '__delitem__',
    '__init_subclass__',
    '__subclasshook__',
    '__call__',
    '__class__',
    '__setstate__',
    '__getstate__',
    '__floor__',
    '__mro__',
    '__dictoffset__',
    '__round__',
    '__trunc__',
    '__len__',
    '__bases__',
    '__basicsize__',
    '__name__',
    '__qualname__',
    '__subclasscheck__',
    '__text_signature__',
    '__Weakrefoffset__',
    '__ceil__',
    '__getnewargs__',
    '__contains__',
    '__enter__',
    '__exit__',
    '__slots__',
    '__abstractmethods__',
    '__aenter__',
    '__aexit__',
    '__weakrefoffset__',
    '__instancecheck__',
    '__itemsize__',
    '__subclasses__',
    '__iter__',
    '__weakref__',
        }

def map_types_and_functions(obj, references, path, from_type):
    """
    Maps types and functions of the given `obj` to it's `references`.
    
    Parameters
    ----------
    obj : `type` or `module`
        The object to map.
    references : `dict` of (`str`, ``UnitBase``) items
        References of `obj` to it's contained objects.
    path : ``QualPath``
        Tha path of `obj`.
    from_type : `bool`
        Whether `obj` is a `type` instance.
    """
    for attr_name in dir(obj):
        try:
            attr_value = getattr(obj, attr_name)
        except AttributeError:
            continue
        
        attr_value_type = attr_value.__class__
        
        # Porcess only hashables
        hashhable = (getattr(obj, '__hash__', None) is not None)
        if hashhable:
            try:
                hash(attr_value)
            except (TypeError, RuntimeError):
                hashhable = False
        
        if (not hashhable):
            if not from_type:
                continue
            
            if attr_value_type in IGNORED_CLASS_ATTRIBUTE_TYPES:
                continue
            
            if attr_name in IGNORED_CLASS_ATTRIBUTE_NAMES:
                continue
            
            references[attr_name] = ClassAttributeUnit(attr_name, QualPath(path, attr_name))
            continue
        
        # Translate methods
        if attr_value_type in METHOD_TYPES:
            attr_value_func = getattr(attr_value, '__func__', None)
            # Cpython, check. Let built in methods trough.
            if (attr_value_func is not None):
                attr_value = attr_value_func
                attr_value_type = attr_value.__class__
        
        # Check types.
        if issubclass(attr_value_type, type):
            if attr_value in IGNORED_TYPES:
                continue
            
            attr_value_path = QualPath(attr_value.__module__, attr_value.__qualname__)
            
            if attr_value_path.parent == path:
                attr_name = attr_value.__name__
                references[attr_name] = TypeUnit(attr_name, attr_value_path, attr_value)
            
            continue
        
        # Check functions.
        if attr_value_type in FUNCTION_TYPES:
            if attr_value in IGNORED_FUNCTIONS:
                continue
            
            try:
                if from_type:
                    name = attr_value.__qualname__
                else:
                    name = attr_value.__name__
            except AttributeError:
                name = attr_value_type.__name__
            
            if name == '<lambda>':
                name = attr_name
            
            attr_value_module = getattr(attr_value, '__module__', None)
            if attr_value_module is None:
                # Builtin stuff, skip
                continue
            
            attr_value_path = QualPath(attr_value_module, name)
            
            if from_type or attr_value_path.parent == path:
                if from_type:
                    alternative_path = QualPath(path, attr_name)
                else:
                    alternative_path = None
                
                references[attr_name] = FunctionUnit(name, attr_value_path, attr_value, alternative_path)
            
            continue
        
        if not from_type:
            continue
        
        if attr_value_type in PROPERTY_TYPES:
#            for name in ('fget', 'fset', 'fdel'):
#                func = getattr(attr_value,name, None)
#                if (func is not None):
#                    break
#            else:
#                continue
#
#            try:
#                name = func.__name__
#            except AttributeError:
#                name = func.__class__.__name__
#
#            if name == '<lambda>':
#                name = attr_name
            
            references[attr_name] = PropertyUnit(attr_name, QualPath(path, attr_name), attr_value)
            continue
        
        if attr_value_type in ATTRIBUTE_TYPES:
            name = attr_value.__name__
            references[attr_name] = InstanceAttributeUnit(name, QualPath(path, attr_name))
            continue
        
        if attr_value_type in IGNORED_CLASS_ATTRIBUTE_TYPES:
            continue
        
        if attr_name in IGNORED_CLASS_ATTRIBUTE_NAMES:
            continue
        
        references[attr_name] = ClassAttributeUnit(attr_name, QualPath(path, attr_name))
        continue

MAPPED_OBJECTS = {}

class UnitBase(object):
    """
    Base class for represnetative units.
    
    Attributes
    ----------
    _cache : `dict`
        Cache used by cached properties.
    _docs : `None` or ``DocString``
        The processed dcostring of the represented unit.
    _docs_parsed : `bool`
        Whether the represneted unit's docstring was already processed.
    name : `str`
        The name of the unit.
    path : ``QualPath``
        The path to the unit.
    """
    __slots__ = ('_cache', '_docs', '_docs_parsed', 'name', 'path',)
    
    def __repr__(self):
        """Returns the unit's represnetation."""
        return f'<{self.__class__.__name__} name={self.name}, path={self.path!s}>'
    
    def _get_raw_docstring(self):
        """
        Returns the raw docstring of the represented object.
        
        Returns
        -------
        docstring : `None` or ``DocString``
        """
        return None
    
    @property
    def docs(self):
        """
        Returns the docs of the represneted object.
        
        Returns
        -------
        docstring : `None` or ``DocString``
        """
        docs_parsed = self._docs_parsed
        if docs_parsed:
            docstring = self._docs
        else:
            self._docs = docstring = self._get_raw_docstring()
            self._docs_parsed = True
        
        return docstring
    
    @cached_property
    def text(self):
        """
        Renders the docstring of the respective object to one big chunk of string.
        
        Returns
        -------
        docs : `None` or `str`
        """
        docs = self.docs
        if docs is None:
            return None
        
        return serialize_docs(docs)
    
    @cached_property
    def source_text(self):
        """
        Renders the docstring of the respective object to source-like format.
        
        Returns
        -------
        docs : `None` or `str`
        """
        docs = self.docs
        if docs is None:
            return None
        
        return serialize_docs_source_text(docs)
    
    @cached_property
    def embed_sized(self):
        """
        Renders the docstring of the respective object to chunks of string with max size of embed description.
        
        Returns
        -------
        docs : `None` or `list` of `str`
        """
        docs = self.docs
        if docs is None:
            return None
        
        return serialize_docs_embed_sized(docs)


class AttributeUnitBase(UnitBase):
    """
    Base unit class for attributes.
    
    Attributes
    ----------
    _cache : `dict`
        Cache used by cached properties.
    _docs : `None` or ``DocString``
        The processed dcostring of the represented unit.
    _docs_parsed : `bool`
        Whether the represneted unit's docstring was already processed.
    name : `str`
        The name of the unit.
    path : ``QualPath``
        The path to the unit.
    """
    __slots__ = ()
    
    def _get_raw_docstring(self):
        """
        Returns the raw docstring of the represented object.
        
        Returns
        -------
        docstring : `None` or ``DocString``
        """
        parent = MAPPED_OBJECTS.get(self.path.parent)
        if parent is None:
            return None
        
        docstring = parent.docs
        if docstring is None:
            return None
        
        return docstring.attribute_docstring_for(self.name)


class InstanceAttributeUnit(AttributeUnitBase):
    """
    Represents an instance attribute.
    
    Attributes
    ----------
    _cache : `dict`
        Cache used by cached properties.
    _docs : `None` or ``DocString``
        The processed dcostring of the represented unit.
    _docs_parsed : `bool`
        Whether the represneted unit's docstring was already processed.
    name : `str`
        The name of the attribute.
    path : ``QualPath``
        The path to the attribute.
    """
    __slots__ = ()
    def __new__(cls, name, path):
        """
        Creates a new instance attribute unit from the given parameters.
        
        Parameters
        ----------
        name : `str`
            The name of the attribute
        path : ``QualPath``
            The path to the attribute.
        """
        self = object.__new__(cls)
        self.name = name
        self.path = path
        self._cache = {}
        self._docs = None
        self._docs_parsed = False
        MAPPED_OBJECTS[path] = self
        
        return self


class ClassAttributeUnit(AttributeUnitBase):
    """
    Represents a class attribute
    
    Attributes
    ----------
    name : `str`
        The name of the attribute.
    path : ``QualPath``
        The path to the attribute.
    """
    __slots__ = ()
    def __new__(cls, name, path):
        """
        Creates a new class attribute unit from the given parameters.
        
        Parameters
        ----------
        name : `str`
            The name of the attribute
        path : ``QualPath``
            The path to the attribute.
        """
        self = object.__new__(cls)
        self.name = name
        self.path = path
        self._cache = {}
        self._docs = None
        self._docs_parsed = False
        
        MAPPED_OBJECTS[path] = self
        
        return self


class ObjectedUnitBase(UnitBase):
    """
    Base class for dicstrings, which store their represneted object.

    Attributes
    ----------
    _cache : `dict`
        Cache used by cached properties.
    _docs : `None` or ``DocString``
        The processed dcostring of the represented unit.
    _docs_parsed : `bool`
        Whether the represneted unit's docstring was already processed.
    name : `str`
        The name of the unit.
    path : ``QualPath``
        The path to the unit.
    object : `property-like`
        The represented property.
    """
    __slots__ = ('object', )
    
    def _get_raw_docstring(self):
        """
        Returns the raw docstring of the represented object.
        
        Returns
        -------
        docstring : `None` or ``DocString``
        """
        docstring = getattr(self.object, '__doc__', 'None')
        if docstring is None:
            return None
        
        if type(docstring) is not str:
            return None
        
        return DocString(docstring, self.path)


class PropertyUnit(ObjectedUnitBase):
    """
    Represents a property.
    
    Attributes
    ----------
    _cache : `dict`
        Cache used by cached properties.
    _docs : `None` or ``DocString``
        The processed dcostring of the represented unit.
    _docs_parsed : `bool`
        Whether the represneted unit's docstring was already processed.
    name : `str`
        The name of the unit.
    path : ``QualPath``
        The path to the unit.
    object : `property-like`
        The represented property.
    """
    __slots__ = ()
    def __new__(cls, name, path, obj):
        """
        Creates a new property unit from the given parameters.
        
        Parameters
        ----------
        name : `str`
            The name of the property.
        path : ``QualPath``
            The path to the property.
        obj : `property-like`
            The represented property.
        """
        self = object.__new__(cls)
        self.name = name
        self.path = path
        self.object = obj
        self._cache = {}
        self._docs = None
        self._docs_parsed = False
        
        MAPPED_OBJECTS[path] = self
        
        return self


class FunctionUnit(ObjectedUnitBase):
    """
    Reprents a function or method.
    
    Attributes
    ----------
    _cache : `dict`
        Cache used by cached properties.
    _docs : `None` or ``DocString``
        The processed dcostring of the represented unit.
    _docs_parsed : `bool`
        Whether the represneted unit's docstring was already processed.
    name : `str`
        The name of the function.
    path : ``QualPath``
        The path to the function.
    object : `function-like`
        The represented function.
    """
    __slots__= ()
    def __new__(cls, name, path, obj, alternative_path):
        """
        Creates a new property unit from the given parameters.
        
        Parameters
        ----------
        name : `str`
            The name of the function.
        path : ``QualPath``
            The path to the function.
        obj : `property-like`
            The represented function.
        alternative_path : `None` or ``QualPath``
            Alternatvie path to the function.
            
            Methods might show up at multyple places, so more access path can be added to them.
        """
        try:
            self = MAPPED_OBJECTS[path]
        except KeyError:
            self = object.__new__(cls)
            self.name = name
            self.path = path
            self.object = obj
            self._cache = {}
            self._docs = None
            self._docs_parsed = False
            
            MAPPED_OBJECTS[path] = self
        
        if (alternative_path is not None) and (alternative_path != path):
            MAPPED_OBJECTS[alternative_path] = self
        
        return self


class FolderedUnit(ObjectedUnitBase):
    """
    Represents a foldered unit.
    
    Attributes
    ----------
    _cache : `dict`
        Cache used by cached properties.
    _docs : `None` or ``DocString``
        The processed dcostring of the represented unit.
    _docs_parsed : `bool`
        Whether the represneted unit's docstring was already processed.
    name : `str`
        The name of the unit.
    path : ``QualPath``
        The path to the unit.
    references : `dict` of (`str`, `UnitBase`) items
        The references of the object to the objects contained by itself. AKA it's folder.
    object : `property-like`
        The represented unit.
    """
    __slots__ = ('references',)
    
    def __repr__(self):
        """Returns the foldered unit's represnetation."""
        return f'<{self.__class__.__name__} name={self.name!r}, path={self.path!s}, references={self.references!r}>'


class TypeUnit(FolderedUnit):
    """
    Represents a type.
    
    Attributes
    ----------
    _cache : `dict`
        Cache used by cached properties.
    _docs : `None` or ``DocString``
        The processed dcostring of the represented unit.
    _docs_parsed : `bool`
        Whether the represneted unit's docstring was already processed.
    name : `str`
        The name of the type.
    path : ``QualPath``
        The path to the type.
    references : `dict` of (`str`, `UnitBase`) items
        The references of the type to the objects contained by itself. AKA it's folder.
    object : `type`
        The represented type.
    """
    __slots__ = ()
    def __new__(cls, name, path, obj):
        """
        Creates a new type unit from the given `obj`.
        
        Parameters
        ----------
        name : `str`
            The name of the type.
        path : ``QualPath``
            The path to the type.
        obj : `type`
            The represented type.
        """
        references = {}
        map_types_and_functions(obj, references, path, True)
        
        self = object.__new__(cls)
        self.name = name
        self.path = path
        self.references = references
        self.object = obj
        self._cache = {}
        self._docs = None
        self._docs_parsed = False
        
        MAPPED_OBJECTS[path] = self
        
        return self


class ModuleUnit(FolderedUnit):
    """
    Represents a module.
    
    Attributes
    ----------
    _cache : `dict`
        Cache used by cached properties.
    _docs : `None` or ``DocString``
        The processed dcostring of the represented unit.
    _docs_parsed : `bool`
        Whether the represneted unit's docstring was already processed.
    name : `str`
        The name of the module.
    path : ``QualPath``
        The path to the module.
    references : `dict` of (`str`, `UnitBase`) items
        The references of the module to the objects contained by itself. AKA it's folder.
    object : `module`
        The represented module.
    """
    __slots__= ()
    def __new__(cls, name, path, obj, modules):
        """
        Creates a new module unit from the given `obj`.
        
        Parameters
        ----------
        name : `str`
            The name of the module.
        path : ``QualPath``
            The path to the module.
        obj : `module`
            The represented module.
        """
        references = {}
        
        base_path_pattern = re.compile(f'{re.escape(str(path))}\.([^\.]+)')
        for module_object in modules:
            parsed = base_path_pattern.fullmatch(module_object.__name__)
            if parsed is None:
                continue
            
            sub_module_name = parsed.group(1)
            references[sub_module_name] = \
                ModuleUnit(sub_module_name, path / sub_module_name, module_object, modules)
        
        map_types_and_functions(obj, references, path, False)
        
        self = object.__new__(cls)
        self.name = name
        self.path = path
        self.references = references
        self.object = obj
        self._cache = {}
        self._docs = None
        self._docs_parsed = False
        
        MAPPED_OBJECTS[path] = self
        
        return self

def map_module(module_name):
    """
    Maps the given module by it's name and reutnrs the root.
    
    Attributes
    ----------
    module_name : `str`
        The module's name.
    
    Returns
    -------
    root : ``ModulePath``
    """
    try:
        return MAPPED_OBJECTS[module_name]
    except KeyError:
        pass
    
    main_module_object = sys.modules[module_name]
    
    module_name_pattern = re.compile(f'{re.escape(module_name)}(?:\..*)?')
    modules = []
    
    for name, module_object in sys.modules.items():
        if (module_name_pattern.fullmatch(name) is not None):
            modules.append(module_object)
    
    root = ModuleUnit(module_name, QualPath(module_name), main_module_object, modules)
    return root

