__all__ = (
    'AttributeUnitBase', 'ClassAttributeUnit', 'DirectoryUnit', 'FunctionUnit', 'InstanceAttributeUnit',
    'MAPPED_OBJECTS', 'ModuleUnit', 'ObjectedUnitBase', 'PropertyUnit', 'TypeUnit', 'UnitBase', 'map_module',
    'search_paths'
)

import re, sys, warnings
from difflib import get_close_matches
from types import (
    BuiltinFunctionType, BuiltinMethodType, FunctionType, GetSetDescriptorType, MemberDescriptorType, MethodType
)

from scarletio import BaseMethodType, MethodLike, cached_property, include, module_property, weak_method

from ...discord.bases import IconSlot

from .builder_html import html_serialize_docs
from .builder_text import generate_preview_for, serialize_docs, serialize_docs_embed_sized, serialize_docs_source_text
from .parser import DocString
from .qualpath import QualPath


html_serialize_docs_extended = include('html_serialize_docs_extended')

WrapperDescriptorType = object.__eq__.__class__
MethodDescriptorType = int.bit_length.__class__
SlotWrapperType = object.__lt__.__class__

METHOD_TYPES = {
    GetSetDescriptorType,
    BuiltinMethodType,
    MethodType,
    WrapperDescriptorType,
    MethodDescriptorType,
    MethodLike,
    BaseMethodType,
    weak_method,
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
    IconSlot,
}

ATTRIBUTE_TYPES = {
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
    obj : `type`, `module`
        The object to map.
    references : `dict` of (`str`, ``UnitBase``) items
        References of `obj` to it's contained objects.
    path : ``QualPath``
        Tha path of `obj`.
    from_type : `bool`
        Whether `obj` is a `type`.
    """
    for attr_name in dir(obj):
        try:
            attr_value = getattr(obj, attr_name)
        except AttributeError:
            continue
        
        attr_value_type = attr_value.__class__
        
        # Process only hashables
        try:
            hash(attr_value)
        except (TypeError, RuntimeError):
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

class UnitBase:
    """
    Base class for representative units.
    
    Attributes
    ----------
    _cache : `dict`
        Cache used by cached properties.
    _docs : `None`, ``DocString``
        The processed docstring of the represented unit.
    _docs_parsed : `bool`
        Whether the represented unit's docstring was already processed.
    name : `str`
        The name of the unit.
    path : ``QualPath``
        The path to the unit.
    """
    __slots__ = ('_cache', '_docs', '_docs_parsed', 'name', 'path',)
    
    def __repr__(self):
        """Returns the unit's representation."""
        return f'<{self.__class__.__name__} name={self.name}, path={self.path!s}>'
    
    @property
    def parent(self):
        """
        Returns the parent object of the unit if applicable.
        
        Returns
        -------
        parent : `None`, ``UnitBase``
        """
        parent_path = self.path.parent
        if parent_path:
            parent = MAPPED_OBJECTS.get(parent_path, None)
        else:
            parent = None
        
        return parent
    
    def _get_raw_docstring(self):
        """
        Returns the raw docstring of the represented object.
        
        Returns
        -------
        docstring : `None`, ``DocString``
        """
        return None
    
    @property
    def docs(self):
        """
        Returns the docs of the represented object.
        
        Returns
        -------
        docstring : `None`, ``DocString``
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
        docs : `None`, `str`
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
        docs : `None`, `str`
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
        docs : `None`, `list` of `str`
        """
        docs = self.docs
        if docs is None:
            return None
        
        return serialize_docs_embed_sized(docs)
    
    @cached_property
    def html(self):
        """
        Renders the docstring to html.
        
        Returns
        -------
        docs : `None`, `str`
        """
        docs = self.docs
        if docs is None:
            return None
        
        return html_serialize_docs(docs, self)
    
    @cached_property
    def html_extended(self):
        """
        Renders the extended docstring to html.
        
        This html renderer will not only render the given docstring, but render it with the other related
        docstrings.
        
        Returns
        -------
        html_extended : `None`, `str`
        """
        html_extended, _ = html_serialize_docs_extended(self, True, False)
        return html_extended
    
    @cached_property
    def html_extended_structure(self):
        """
        Creates the extended docstring's html structure.
        
        Returns
        -------
        html_extended_structure : `None`, ``Structure``
        """
        _, html_extended_structure = html_serialize_docs_extended(self, False, True)
        return html_extended_structure
    
    @cached_property
    def html_extended_with_structure(self):
        """
        Renders the extended docstring to html and returns it's structure as well.
        
        Returns
        -------
        html_extended : `None`, `str`
        html_extended_structure : `None`, ``Structure``
        """
        html_extended, html_extended_structure = html_serialize_docs_extended(self, True, True)
        cache = self._cache
        cache['html_extended'] = html_extended
        cache['html_extended_structure'] = html_extended_structure
        return html_extended, html_extended_structure
        
    @cached_property
    def preview(self):
        """
        Generates preview for the docstring.
        
        Returns
        -------
        preview : `None`, `str`
        """
        docs = self.docs
        if docs is None:
            return None
        
        return generate_preview_for(docs)
    
    def lookup_reference(self, reference):
        """
        Returns the closest unit to the given unit.
        
        Returns
        -------
        referred : `None`, ``UnitBase``.
            The referenced unit.
        """
        # Is local reference?
        reference_parts = reference.split('.')
        if not reference_parts:
            return None
        
        reference_parts.reverse()
        
        if not reference_parts[-1]:
            del reference_parts[-1]
            if isinstance(self, DirectoryUnit):
                if not reference_parts:
                    return self
                
                object_ = direct_lookup_in(self, reference_parts)
                if (object_ is not None):
                    return object_
            
            parent = MAPPED_OBJECTS.get(self.path.parent, None)
            if parent is None:
                return self
            else:
                return direct_lookup_in(parent, reference_parts)
        
        if isinstance(self, DirectoryUnit):
            object_ = lookup_from(self, reference_parts)
            if (object_ is not None):
                return object_
        
        path = self.path.parent
        while path:
            parent = MAPPED_OBJECTS.get(path, None)
            if parent is None:
                break
            
            object_ = lookup_from(parent, reference_parts)
            if (object_ is not None):
                return object_
            
            path = path.parent


def direct_lookup_in(object_, reference_parts):
    """
    Looks up the given reference in a deep unit directly.
    
    Parameters
    ----------
    object_ : ``UnitBase``
        The directory to lookup up from.
    reference_parts : `list` of `str`
        Reference parts to lookup.
        
        The given `reference_parts` should be reversed from their original state.
    
    Returns
    -------
    object_ : `None`, ``UnitBase``
        The found object if applicable.
    """
    reference_parts = reference_parts.copy()
    
    while reference_parts:
        if not isinstance(object_, DirectoryUnit):
            # Cannot move further deep, the reference will not be found, leave.
            object_ = None
            break
        
        reference_part = reference_parts.pop()
        try:
            object_ = object_.references.get(reference_part, None)
        except KeyError:
            # Reference not be found, leave.
            object_ = None
            break
    
    # No more reference part to lookup, return object.
    return object_


def lookup_from(directory, reference_parts):
    """
    Looks up the given reference in the directory and in all of it's sub-directories.
    
    Parameters
    ----------
    directory : ``UnitBase``
        The directory to look up from.
    reference_parts : `list` of `str`
        Reference parts to lookup.
        
        The given `reference_parts` should be reversed from their original state.
    
    Returns
    -------
    object_ : ``UnitBase``
        The unit-base if anything found matching the references.
    """
    if not isinstance(directory, DirectoryUnit):
        return None
    
    search_for = reference_parts[-1]
    
    for sub_name, sub_object in directory.references.items():
        if sub_name == search_for:
            if len(reference_parts)  == 1:
                return sub_object
            else:
                object_ = lookup_from(sub_object, reference_parts[:-1])
        else:
            object_ = lookup_from(sub_object, reference_parts)
        
        if object_ is not None:
            return object_
    
    return None

class AttributeUnitBase(UnitBase):
    """
    Base unit class for attributes.
    
    Attributes
    ----------
    _cache : `dict`
        Cache used by cached properties.
    _docs : `None`, ``DocString``
        The processed docstring of the represented unit.
    _docs_parsed : `bool`
        Whether the represented unit's docstring was already processed.
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
        docstring : `None`, ``DocString``
        """
        parent = MAPPED_OBJECTS.get(self.path.parent, None)
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
    _docs : `None`, ``DocString``
        The processed docstring of the represented unit.
    _docs_parsed : `bool`
        Whether the represented unit's docstring was already processed.
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
    Base class for docstrings, which store their represented object.

    Attributes
    ----------
    _cache : `dict`
        Cache used by cached properties.
    _docs : `None`, ``DocString``
        The processed docstring of the represented unit.
    _docs_parsed : `bool`
        Whether the represented unit's docstring was already processed.
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
        docstring : `None`, ``DocString``
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
    _docs : `None`, ``DocString``
        The processed docstring of the represented unit.
    _docs_parsed : `bool`
        Whether the represented unit's docstring was already processed.
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
    Represents a function or method.
    
    Attributes
    ----------
    _cache : `dict`
        Cache used by cached properties.
    _docs : `None`, ``DocString``
        The processed docstring of the represented unit.
    _docs_parsed : `bool`
        Whether the represented unit's docstring was already processed.
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
        alternative_path : `None`, ``QualPath``
            Alternative path to the function.
            
            Methods might show up at multiple places, so more access path can be added to them.
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


class DirectoryUnit(ObjectedUnitBase):
    """
    Represents a directory like unit.
    
    Attributes
    ----------
    _cache : `dict`
        Cache used by cached properties.
    _docs : `None`, ``DocString``
        The processed docstring of the represented unit.
    _docs_parsed : `bool`
        Whether the represented unit's docstring was already processed.
    name : `str`
        The name of the unit.
    path : ``QualPath``
        The path to the unit.
    references : `dict` of (`str`, `UnitBase`) items
        The references of the object to the objects contained by itself. AKA it's directory.
    object : `property-like`
        The represented unit.
    """
    __slots__ = ('references',)
    
    def __repr__(self):
        """Returns the directory like unit's representation."""
        return (
            f'<{self.__class__.__name__} name={self.name!r}, path={self.path!s}, reference count='
            f'{len(self.references)!r}>'
        )


class TypeUnit(DirectoryUnit):
    """
    Represents a type.
    
    Attributes
    ----------
    _cache : `dict`
        Cache used by cached properties.
    _docs : `None`, ``DocString``
        The processed docstring of the represented unit.
    _docs_parsed : `bool`
        Whether the represented unit's docstring was already processed.
    name : `str`
        The name of the type.
    path : ``QualPath``
        The path to the type.
    references : `dict` of (`str`, `UnitBase`) items
        The references of the type to the objects contained by itself. AKA it's directory.
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


class ModuleUnit(DirectoryUnit):
    """
    Represents a module.
    
    Attributes
    ----------
    _cache : `dict`
        Cache used by cached properties.
    _docs : `None`, ``DocString``
        The processed docstring of the represented unit.
    _docs_parsed : `bool`
        Whether the represented unit's docstring was already processed.
    name : `str`
        The name of the module.
    path : ``QualPath``
        The path to the module.
    references : `dict` of (`str`, `UnitBase`) items
        The references of the module to the objects contained by itself. AKA it's directory.
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
    Maps the given module by it's name and returns the root.
    
    Attributes
    ----------
    module_name : `str`
        The module's name.
    
    Returns
    -------
    root : ``ModulePath``
    
    Raises
    ------
    LookupError
        No loaded module is named as `module_name`.
    """
    try:
        return MAPPED_OBJECTS[module_name]
    except KeyError:
        pass
    
    try:
        main_module_object = sys.modules[module_name]
    except KeyError:
        raise LookupError(
            f'No loaded module is named as {module_name!r}'
        ) from None
    
    # Invalidate search cache
    CachedSearcher._cache_valid = False
    
    module_name_pattern = re.compile(f'{re.escape(module_name)}(?:\..*)?')
    modules = []
    
    for name, module_object in sys.modules.items():
        if (module_name_pattern.fullmatch(name) is not None):
            modules.append(module_object)
    
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        root = ModuleUnit(module_name, QualPath(module_name), main_module_object, modules)
    
    return root


def qual_path_sort_key(qual_path):
    """
    Sort key to sort ``QualPath``-s.
    
    Parameters
    ----------
    qual_path : ``QualPath``
        The respective path.
    
    Returns
    -------
    sort_key : `str`
    """
    return str(qual_path)


class CachedSearcher:
    """
    Cached unit path searcher.
    
    Class Attributes
    ----------------
    _cached_relations : `dict` of (``QualPath``, (``QualPath``, `list` of ``QualPath``)) items
        Path shortening, path relations used when translating found patches back.
    _cached_possibilities : `list` of `str`
        The cached possibilities.
    _cache_valid : `bool`
        Whether the searcher cache is valid.
    """
    _cache_valid = True
    _cached_relations = {}
    _cached_possibilities = []
    
    @classmethod
    def _prepare(cls):
        """
        Prepares the cache of the searcher.
        
        Returns
        -------
        possibilities : `list` of `str`
            The cached possibilities.
        relations : `dict` of (``QualPath``, (``QualPath``, `list` of ``QualPath``)) items
            Path shortening, path relations used when translating found patches back.
        """
        cached_relations = cls._cached_relations
        cached_possibilities = cls._cached_possibilities
        if not cls._cache_valid:
            cached_relations.clear()
            cached_possibilities.clear()
            for path in MAPPED_OBJECTS:
                path_parts = path.parts
                for starter in range(len(path_parts)):
                    local_path = '.'.join(path_parts[starter:])
                    
                    try:
                        collected_paths = cached_relations[local_path]
                    except KeyError:
                        cached_relations[local_path] = path
                        cached_possibilities.append(local_path)
                    else:
                        if isinstance(collected_paths, QualPath):
                            cached_relations[local_path] = [collected_paths, path]
                        else:
                            collected_paths.append(path)
            
            for value in cached_relations.values():
                if isinstance(value, QualPath):
                    continue
                
                value.sort(key = qual_path_sort_key)
        
        return cached_possibilities, cached_relations
    
    def __call__(self, value, limit=100):
        """
        Returns all the found units with the given value in their path. Case insensitive.
        
        Parameters
        ----------
        value : `str`
            The query string.
        
        Returns
        -------
        paths : `list` of ``QualPath``
        """
        possibilities, relations = self._prepare()
        
        matcheds = get_close_matches(value, possibilities, n=limit, cutoff=0.60)
        
        paths = []
        collected = set()
        
        for matched in matcheds:
            path = relations[matched]
            if isinstance(path, QualPath):
                if path in collected:
                    continue
                
                collected.add(path)
                paths.append(path)
            else:
                for path in path:
                    if path in collected:
                        continue
                    
                    collected.add(path)
                    paths.append(path)
        
        del paths[limit:]
        
        return paths


search_paths = CachedSearcher()
