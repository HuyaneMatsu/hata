__all__ = ()

import re, reprlib

from scarletio import export

from .builder_html import create_relative_link, description_serializer, graved_to_escaped, sub_section_serializer
from .graver import GravedAttributeDescription, GravedDescription
from .module_mapper import FunctionUnit, InstanceAttributeUnit, MAPPED_OBJECTS, ModuleUnit, PropertyUnit, TypeUnit
from .parser import ATTRIBUTE_NAME_RP, ATTRIBUTE_SECTION_NAME_RP

from html import escape as html_escape


class Structure:
    """
    Represents an extended docstring's html structure.
    
    Attributes
    ----------
    title : `str`
        The title of the represented unit or section.
    prefixed_title : `str`
        Can be used as local reference in the html file.
    children : `None` or (`list` of ``Structure``)
        The child units of sections. Set as `None` if would have non.
    """
    __slots__ = ( 'title', 'prefixed_title', 'children')
    
    def __init__(self, title, prefixed_title, children):
        """
        Creates a nw structure object with the given parameters.
        
        Parameters
        ----------
        title : `str`
            The title of the represented unit or section.
        prefixed_title : `str`
            Can be used as local reference in the html file.
        children : `None` or (`list` of ``Structure``)
            The child units of sections.
            
            Should be given as `None` if the structure has no child.
        """
        self.title = title
        self.prefixed_title = prefixed_title
        self.children = children


def create_relative_sectioned_link(source, target):
    """
    Creates relative link between two objects. Not like ``create_relative_link``, this function uses anchors as well.
    
    Parameters
    ----------
    source : ``QualPath``
        Source object's path.
    target : ``QualPath``
        Target object's path.
    
    Returns
    -------
    url : `str`
        Generated relative url.
    """
    while True:
        parent_maybe = source.parent
        unit = MAPPED_OBJECTS.get(parent_maybe, None)
        if unit is None:
            break
        
        if type(unit) is ModuleUnit:
            break
        
        source = parent_maybe
        continue
    
    target_backfetched = []
    
    while True:
        target_maybe = target.parent
        unit = MAPPED_OBJECTS.get(target_maybe, None)
        if unit is None:
            break
        
        if type(unit) is ModuleUnit:
            break
        
        target_backfetched.append(target.parts[-1])
        target = target_maybe
        continue
    
    url = create_relative_link(source, target)
    if target_backfetched:
        target_backfetched.reverse()
        target_backfetched = '-'.join(target_backfetched)
        target_backfetched = anchor_escape(target_backfetched)
        
        url = f'{url}#{target_backfetched}'
    
    return url

def anchor_escape(text):
    """
    Anchor escapes the given text.
    
    Parameters
    ----------
    text : `str`
        The text to escape.
    
    Returns
    -------
    escaped : `str`
    """
    return text.lower().replace(' ', '-')

ANCHOR_SVG = (
    '<svg viewBox="0 0 16 16">'
        '<path fill-rule="evenodd" d="M 7.775 3.275 a 0.75 0.75 0 0 0 1.06 1.06 l 1.25 -1.25 a 2 2 0 1 1 2.83 2.83 '
            'l -2.5 2.5 a 2 2 0 0 1 -2.83 0 a 0.75 0.75 0 0 0 -1.06 1.06 a 3.5 3.5 0 0 0 4.95 0 l 2.5 -2.5 '
            'a 3.5 3.5 0 0 0 -4.95 -4.95 l -1.25 1.25 Z m -4.69 9.64 a 2 2 0 0 1 0 -2.83 l 2.5 -2.5 a 2 2 0 0 1 2.83 0 '
            'a 0.75 0.75 0 0 0 1.06 -1.06 a 3.5 3.5 0 0 0 -4.95 0 l -2.5 2.5 a 3.5 3.5 0 0 0 4.95 4.95 l 1.25 -1.25 '
            'a 0.75 0.75 0 0 0 -1.06 -1.06 l -1.25 1.25 a 2 2 0 0 1 -2.83 0 Z"></path>'
    '</svg>'
)

YES_SVG = (
    '<svg '
        'width="1.2em" '
        'height="1.2em" '
        'preserveAspectRatio="xMidYMid meet" '
        'viewBox="0 0 24 24" '
        'aria-hidden="true"'
    '>'
        '<g fill="none">'
            '<path '
                'd="M5 13l4 4L19 7" '
                'stroke="currentColor" '
                'stroke-width="2" '
                'stroke-linecap="round" '
                'stroke-linejoin="round"'
            '>'
            '</path>'
        '</g>'
    '</svg>'
)

def anchor_for_serializer(section_name):
    """
    Returns the anchor for the given section name.
    
    This function is a generator.
    
    Parameters
    ----------
    section_name : `str`
        The section's name.
    
    Yields
    ------
    html : `str`
    """
    yield '<a name="'
    yield section_name
    yield '" class="anchor" aria-hidden="true" href="#'
    yield section_name
    yield '">'
    yield ANCHOR_SVG
    yield '</a>'

def section_title_serializer(title):
    """
    Serializes to html the given section name.
    
    This function is a generator.
    
    Parameters
    ----------
    title : `str`
        The respective section's name.
    
    Yields
    -------
    html : `str`
    """
    yield '<h2>'
    yield from anchor_for_serializer(title)
    yield html_escape(title)
    yield '<div class="underline"></div></h2>'

SECTION_TYPE_DEFAULT = 0

SECTION_TYPE_USAGES = 10

SECTION_TYPE_INSTANCE_ATTRIBUTES = 20
SECTION_TYPE_X_ATTRIBUTES = 21
SECTION_TYPE_CLASS_ATTRIBUTES = 22

SECTION_TYPE_PARAMETERS = 30
SECTION_TYPE_OTHER_PARAMETERS = 31

SECTION_TYPE_YIELDS = 40
SECTION_TYPE_RETURNS = 41
SECTION_TYPE_RAISES = 42

SECTION_TYPE_NOTES = 50
SECTION_TYPE_X = 51

SECTION_TYPE_PROPERTIES = 60
SECTION_TYPE_METHODS = 61
SECTION_TYPE_FUNCTIONS = 62
SECTION_TYPE_CLASSES = 63
SECTION_TYPE_MODULES = 64

def get_attribute_section_mentioned_names(section_content):
    """
    Gets the attribute names mention by the respective section.
    
    Parameters
    ----------
    section_content : `list` of `Any`
    
    Returns
    -------
    names : `set` of `str`
        The parsed names from the respective section.
    """
    names = set()
    
    index = 0
    limit = len(section_content)
    while True:
        if index == limit:
            break
        
        part = section_content[index]
        if (type(part) is not GravedDescription):
            break
        
        starter = part.content[0]
        if (type(starter) is not str):
            break
        
        parsed = ATTRIBUTE_NAME_RP.match(starter)
        if parsed is None:
            break
        
        attr_name = parsed.group(1)
        
        index += 1
        if index != limit:
            part = section_content[index]
            if type(part) is list:
                index += 1
        
        names.add(attr_name)
        continue
    
    return names


def get_anchor_prefix_for(path):
    """
    Returns the given object's anchor prefix to remove overlapping anchor names.
    
    Parameters
    ----------
    path : ``QualPath``
        The respective unit.
    
    Returns
    -------
    prefix : `str`
    """
    prefix_parts = []
    while True:
        parent = path.parent
        unit = MAPPED_OBJECTS.get(parent, None)
        if unit is None:
            break
        
        if type(unit) is ModuleUnit:
            break
        
        prefix_parts.append(path.parts[-1])
        path = parent
        continue
    
    return anchor_escape('-'.join(prefix_parts))

def get_tier_for(path):
    """
    Returns the given object's tier level. Tier level should be used to decide header type.
    
    Parameters
    ----------
    path : ``QualPath``
        The respective unit's path.
    
    Returns
    -------
    tier : `int`
    """
    tier = 1
    while True:
        parent = path.parent
        unit = MAPPED_OBJECTS.get(parent, None)
        if unit is None:
            break
        
        if type(unit) is ModuleUnit:
            break
        
        tier += 2
        path = parent
        continue
    
    return tier

def get_parent_path_of(path):
    """
    Returns the given path 0 tier parent path.
    
    Parameters
    ----------
    path : ``QualPath``
        The respective unit's path
    
    Returns
    -------
    parent_path : ``QualPath``
    """
    while True:
        parent = path.parent
        unit = MAPPED_OBJECTS.get(parent, None)
        if unit is None:
            break
        
        if type(unit) is ModuleUnit:
            break
        
        path = parent
        continue
    
    return path

def name_sort_key(name):
    """
    Gets sort key for the given name, when sorting attribute, method, or such names.
    
    Parameters
    ----------
    name : `str`
            Name of an attribute, method or class.
    
    Returns
    -------
    key : `tuple` (`int`, `str`)
        The generated key.
    """
    if name.startswith('__'):
        if name == '__new__':
            prefix_count = 0
        elif name == '__init__':
             prefix_count = 1
        elif name == '__call__':
            prefix_count = 2
        else:
            prefix_count = 102
    elif name.startswith('_'):
        prefix_count = 101
    else:
        prefix_count = 100
    
    return prefix_count, name

def item_sort_key(item):
    """
    Gets sort key for the given item, when sorting name - docstring pairs
    
    Parameters
    ----------
    item : `tuple (`str`, ``DocString``)
        A `name` - ``Docstring`` relation.
    
    Returns
    -------
    key : `tuple` (`int`, `str`)
        The generated key.
    """
    return name_sort_key(item[0])


class SimpleSection:
    """
    Represents a simple section.
    
    Attributes
    ----------
    content : `list` of `Any`
        Contained section part.
    object : ``UnitBase``
        The owner unit.
    title : `None`, `str`
        The title of the section.
    path : ``QualPath``
        Path to use instead of the objects'.
    """
    __slots__ = ('content', 'object', 'title', 'path')
    
    def __init__(self, title, content, object_, path):
        """
        Creates a new attribute section with the given parameters.
        
        Parameters
        ----------
        title : `None`, `str`
            The title of the represented section.
        content : `list` of `Any`
            Contained section part.
        object_ : ``TypeUnit``
            The owner type-unit.
        path : `None`, ``QualPath``
            Path to use instead of the objects'.
        """
        self.title = title
        self.content = content
        self.object = object_
        if path is None:
            path = object_.path
        self.path = path
    
    def serialize(self):
        """
        Serializes the section to html string parts.
        
        This method is a generator.
        
        Yields
        ------
        html : `str`
        """
        object_ = self.object
        path = self.path
        title = self.title
        
        if (title is not None):
            prefix = get_anchor_prefix_for(path)
            if prefix:
                prefix = f'{prefix}-{anchor_escape(title)}'
            else:
                prefix = anchor_escape(title)
            
            tier = get_tier_for(path) + 1
            
            yield '<h'
            yield str(tier)
            yield '>'
            yield from anchor_for_serializer(prefix)
            yield html_escape(title)
            yield '<div class="underline"></div></h'
            yield str(tier)
            yield '>'
        
        
        yield from sub_section_serializer(self.content, object_, get_parent_path_of(path),
            create_relative_sectioned_link)
        
        return
    
    def structurize(self):
        """
        Returns the structure of the section.
        
        Returns
        -------
        structure : `None`, ``Structure``
            If the section is unnamed, returns `None`.
        """
        title = self.title
        if title is None:
            return None
        
        prefixed_title = get_anchor_prefix_for(self.path)
        if prefixed_title:
            prefixed_title = f'{prefixed_title}-{anchor_escape(title)}'
        else:
            prefixed_title = anchor_escape(title)
        
        return Structure(title, prefixed_title, None)


class FunctionOrPropertySerializer:
    """
    Serializer for a method or for a property.
    
    Attributes
    ----------
    content : `list` of `Any`
        Contained section part.
    object : ``PropertyUnit``, ``FunctionUnit``
        The owner type-unit.
    parameter_section : `None`, ``ParameterSection``
        The parameter section of the serializer.
    path : ``QualPath``
        Path to use instead of the object's.
    """
    __slots__ = ('content', 'object', 'parameter_section', 'path')
    
    def __init__(self, object_, path = None):
        """
        Creates a new method or property serializer.
        
        Parameters
        ----------
        object_ : ``PropertyUnit``, ``FunctionUnit``
            The object to serialize.
        path : `None`, ``QualPath`` = `None`, Optional
            Path to use instead of the object's.
        """
        self.object = object_
        if path is None:
            path = object_.path
        self.path = path
        
        docs = object_.docs
        if docs is None:
            self.content = None
            self.parameter_section = None
            return
        
        parameter_section = None
        
        section_parts = {}
        for section_name, section_content in docs.sections:
            if section_name is None:
                section_parts[SECTION_TYPE_DEFAULT] = SimpleSection(None, section_content, object_, path)
                continue
            
            try:
                section_type_value = SECTION_NAME_TYPE_DEFAULT_RELATIONS[section_name]
            except KeyError:
                pass
            else:
                section_parts[section_type_value] = SimpleSection(section_name, section_content, object_, path)
                continue
            
            if section_name in ('Parameters', 'Other Parameters'):
                if (parameter_section is None):
                    parameter_section = ParameterSection(section_content, object_, path)
                    section_parts[SECTION_TYPE_PARAMETERS] = parameter_section
                else:
                    parameter_section.extend(section_content)
                
                continue
            
            try:
                existing = section_parts[SECTION_TYPE_X]
            except KeyError:
                existing = section_parts[SECTION_TYPE_X] = []
            
            existing.append(SimpleSection(section_name, section_content, object_, path))
            continue
        
        self.parameter_section = parameter_section
        
        content = []
        for part in sorted(section_parts.items()):
            sub_section = part[1]
            if type(sub_section) is list:
                content.extend(sub_section)
            else:
                content.append(sub_section)
        
        self.content = content
    
    
    def serialize(self):
        """
        Serializes the represented method or property to html parts.
        
        This method is a generator.
        
        Yields
        ------
        html : `str`
        """
        path = self.path
        
        name = path.parts[-1]
        prefix = get_anchor_prefix_for(path)
        tier = get_tier_for(path)
        
        yield '<h'
        yield str(tier)
        yield '>'
        yield from anchor_for_serializer(anchor_escape(prefix))
        yield html_escape(name)
        
        is_function = isinstance(self.object, FunctionUnit)
        
        if is_function:
            yield '<span class="function_parameter">('
        
            parameter_section = self.parameter_section
            if (parameter_section is not None):
                parameter_added = False
                
                for parameter_sub_section in parameter_section.parameter_sub_sections:
                    if parameter_sub_section.optional:
                        if parameter_added:
                            yield ', '
                        
                        yield '...'
                        break
                        
                    if parameter_added:
                        yield ', '
                    else:
                        parameter_added = True
                    
                    yield html_escape(parameter_sub_section.name)
            
            yield ')</span>'
        
        
        yield '</h'
        yield str(tier)
        yield '>'
        
        yield '<div class="underline"></div>'
        
        content = self.content
        if content is None:
            return
        
        if tier > 1:
            yield '<div class="sub_unit">'
        
        for serializer in content:
            yield from serializer.serialize()
        
        if tier > 1:
            yield '</div>'
        
        return
    
    def structurize(self):
        """
        Creates a structure for the represented unit.
        
        Returns
        -------
        structure : ``Structure``
        """
        content = self.content
        if content is None:
            children = None
        else:
            children = []
            for serializer in self.content:
                child = serializer.structurize()
                if child is None:
                    continue
                
                children.append(child)
                continue
            
            if not children:
                children = None
        
        path = self.path
        title = path.parts[-1]
        prefixed_title = get_anchor_prefix_for(path)
        return Structure(title, prefixed_title, children)


class UnitSection:
    """
    Represents a section, which is filled with units.
    
    Attributes
    ----------
    title : `str`
        The section's title.
    object : ``TypeUnit``
        The represented parent object.
    units : `list` of `tuple` (`str`, ``UnitBase``)
        The contained units.
    path : ``QualPath``
        Path to use instead of the object's.
    """
    __slots__ = ('title', 'object', 'units', 'path')
    
    def __init__(self, title, object_, units, path):
        """
        Creates a new unit section.
        
        Parameters
        ----------
        title : `str`
            The section's title.
        object_ : ``TypeUnit``
            The represented parent object.
        units : `list` of ``UnitBase``
            The contained units.
        path : `None`, ``QualPath``
            Path to use instead of the object's.
        """
        self.title = title
        self.object = object_
        self.units = units
        if path is None:
            path = object_.path
        self.path = path
    
    def serialize(self):
        """
        Serializes the unit section to html parts.
        
        This method is a generator.
        
        Yields
        ------
        html : `str`
        """
        title = self.title
        path = self.path
        prefix = get_anchor_prefix_for(path)
        
        if prefix:
            prefix = f'{prefix}-{anchor_escape(title)}'
        else:
            prefix = anchor_escape(title)
        
        tier = get_tier_for(path) + 1
        
        yield '<h'
        yield str(tier)
        yield '>'
        yield from anchor_for_serializer(prefix)
        yield html_escape(title)
        yield '<div class="underline"></div></h'
        yield str(tier)
        yield '>'
        
        yield '<div class="unit_section">'
        for name, unit in self.units:
            serializer_type = UNIT_CONVERSION_TABLE[type(unit)]
            serializer = serializer_type(unit, path / name)
            yield from serializer.serialize()
        
        yield '</div>'
        
        return
    
    def structurize(self):
        """
        Returns the structure of the unit section.
        
        Returns
        -------
        structure : `None`, ``Structure``
            If the section is unnamed, returns `None`.
        """
        path = self.path
        children = []
        
        for name, unit in self.units:
            serializer_type = UNIT_CONVERSION_TABLE[type(unit)]
            serializer = serializer_type(unit, path / name)
            child = serializer.structurize()
            children.append(child)
        
        if not children:
            children = None
        
        title = self.title
        prefixed_title = get_anchor_prefix_for(path)
        
        if prefixed_title:
            prefixed_title = f'{prefixed_title}-{anchor_escape(title)}'
        else:
            prefixed_title = anchor_escape(title)
        
        return Structure(title, prefixed_title, children)


class AttributeSection:
    """
    Represents an attribute section.
    
    Attributes
    ----------
    extra : `None`, `list` of `Any`
        Extra content after the attribute section.
    relations : `dict` of (`str`, `DocString`) items
        Attribute name, DocString relation.
    object : ``TypeUnit``
        The owner type-unit.
    title : `str`
        The title of the attribute section.
    path : ``QualPath``
        Path to use instead of the object's.
    """
    __slots__ = ('extra', 'relations', 'object', 'title', 'path')
    
    def __init__(self, title, mentioned_names, object_, path):
        """
        Creates a new attribute section with the given parameters.
        
        Parameters
        ----------
        title : `str`
            The title of the represented section.
        mentioned_names : `set` of `str`
            Mentioned attribute names at the attribute section.
        object_ : ``TypeUnit``
            The owner type-unit.
        path : `None`, ``QualPath``
            Path to use instead of the object's.
        """
        self.title = title
        docs = object_.docs
        if docs is None:
            relations = {mentioned_name:None for mentioned_name in mentioned_names}
            extra = None
        else:
            relations = {
                mentioned_name: docs.attribute_docstring_for(mentioned_name) for mentioned_name in mentioned_names
            }
            extra = docs.extra_attribute_docstring_for(title)
        self.relations = relations
        self.extra = extra
        self.object = object_
        if path is None:
            path = object_.path
        self.path = path
    
    def contains(self, name):
        """
        Returns whether the attribute section contains the given attribute name.
        """
        if name in self.relations:
            return True
        
        return False
    
    def add(self, name):
        """
        Adds the given attribute name to the attribute section.
        
        Parameters
        ----------
        name : `str`
        """
        self.relations.setdefault(name, None)
    
    def serialize(self):
        """
        Serializes the attribute section to html string parts.
        
        This method is a generator.
        
        Yields
        ------
        html : `str`
        """
        object_ = self.object
        title = self.title
        path = self.path
        prefix = get_anchor_prefix_for(path)
        
        tier = get_tier_for(path) + 1
        parent_path = get_parent_path_of(path)
        
        if prefix:
            prefixed_title = f'{prefix}-{anchor_escape(title)}'
        else:
            prefixed_title = anchor_escape(title)
        
        yield '<h'
        yield str(tier)
        yield '>'
        yield from anchor_for_serializer(prefixed_title)
        yield html_escape(title)
        yield '<div class="underline"></div></h'
        yield str(tier)
        yield '>'
        
        relations = self.relations
        attribute_names = sorted(relations, key = name_sort_key)
        
        for attribute_name in attribute_names:
            attribute_unit = relations[attribute_name]
            yield '<div class="with_anchor">'
            
            if prefix:
                prefixed_name = f'{prefix}-{anchor_escape(attribute_name)}'
            else:
                prefixed_name = anchor_escape(attribute_name)
            
            yield from anchor_for_serializer(prefixed_name)
            yield html_escape(attribute_name)
            
            if attribute_unit is None:
                yield '</div>'
                yield '<br>'
                continue
            
            attribute_content = attribute_unit.sections[0][1]
            maybe_head = attribute_content[0]
            if type(maybe_head) is GravedAttributeDescription:
                separator = maybe_head.separator
                if separator == '(':
                    yield_space = False
                else:
                    yield_space = True
                
                if yield_space:
                    yield ' '
                
                yield html_escape(separator)
                
                if yield_space:
                    yield ' '
                
                yield graved_to_escaped(maybe_head.content, object_, parent_path, create_relative_sectioned_link)
                yield '</div>'
                attribute_content = attribute_content[1:]
                if not attribute_content:
                    continue
            else:
                yield '</div>'
            
            yield '<div class="sub_section">'
            yield from sub_section_serializer(attribute_content, object_, parent_path, create_relative_sectioned_link)
            yield '</div>'
            continue
        
        extra = self.extra
        if extra is None:
            return
        
        extra_content = extra.sections[0][1]
        yield from sub_section_serializer(extra_content, object_, parent_path, create_relative_sectioned_link)
        return
    
    def structurize(self):
        """
        Creates a section structure for the represented attribute section.
        
        Returns
        -------
        structure : ``Structure``
        """
        path = self.path
        prefix = get_anchor_prefix_for(path)
        
        children = []
        
        for child_title in sorted(self.relations, key = name_sort_key):
            if prefix:
                child_prefixed_title = f'{prefix}-{anchor_escape(child_title)}'
            else:
                child_prefixed_title = anchor_escape(child_title)
            
            child = Structure(child_title, child_prefixed_title, None)
            children.append(child)
        
        if not children:
            children = None
        
        title = self.title
        if prefix:
            prefixed_title = f'{prefix}-{anchor_escape(title)}'
        else:
            prefixed_title = anchor_escape(title)
        
        return Structure(title, prefixed_title, children)

PARAMETER_NAME_RP = re.compile('(\*{0,2}[a-zA-Z_]+[a-zA-Z_0-9]*)(?: *\: *(.+)?)?')
PARAMETER_OPTIONALITY_RP = re.compile('(.*?)(?:,? *([Oo]ptional)(?:,? *\(?([Kk]eyword [Oo]nly)\)?)?)?')
PARAMETER_DEFAULT_START_RP = re.compile('(.*?) *= *(.*?)')

PARAMETER_SHIFT_NAME = 0
PARAMETER_SHIFT_DESCRIPTION = 1
PARAMETER_SHIFT_TYPE = 2
PARAMETER_SHIFT_OPTIONAL = 3
PARAMETER_SHIFT_KEYWORD_ONLY = 4
PARAMETER_SHIFT_DEFAULT = 5

PARAMETER_MASK_NAME = 1 << PARAMETER_SHIFT_NAME
PARAMETER_MASK_DESCRIPTION = 1 << PARAMETER_SHIFT_DESCRIPTION
PARAMETER_MASK_TYPE = 1 << PARAMETER_SHIFT_TYPE
PARAMETER_MASK_OPTIONAL = 1 << PARAMETER_SHIFT_OPTIONAL
PARAMETER_MASK_KEYWORD_ONLY = 1 << PARAMETER_SHIFT_KEYWORD_ONLY
PARAMETER_MASK_DEFAULT = 1 << PARAMETER_SHIFT_DEFAULT


class ParameterSubSection:
    """
    A ``ParameterSection``'s parameter row.
    
    Parameters
    ----------
    default : `None`, ``GravedDescription``
        The default value of the parameter.
    description : `None`, `list` of ``GravedDescription``
        Description of the parameter.
    keyword_only : `bool`
        Whether the parameter is keyword only.
    name : `str`
        The parameter's name.
    optional : `bool`
        Whether the parameter is optional.
    type : `None`, ``GravedDescription``
        The parameter's type.
    """
    __slots__ = ('default', 'description', 'keyword_only', 'name', 'optional', 'type')
    
    def __init__(self, header, description):
        self.description = description
        header = header.copy()
        header_contents = header.content
        
        parameter_name_part = header_contents[0]
        if isinstance(parameter_name_part, str):
            match = PARAMETER_NAME_RP.fullmatch(parameter_name_part)
            if match is None:
                name = ''
            else:
                name, after_part = match.groups()
                if after_part is None:
                    del header_contents[0]
                else:
                    header_contents[0] = after_part
        else:
            # should not happen
            name = ''
            
        self.name = name
        
        if header_contents:
            parameter_optionality_part = header_contents[-1]
            if isinstance(parameter_optionality_part, str):
                match = PARAMETER_OPTIONALITY_RP.fullmatch(parameter_optionality_part)
                if match is None:
                    optional = False
                    keyword_only = False
                else:
                    before_part, optional_part, keyword_only_part = match.groups()
                    
                    if (before_part is not None) and before_part:
                        header_contents[-1] = before_part
                    else:
                        del header_contents[-1]
                    
                    if (optional_part is None):
                        optional = False
                    else:
                        optional = True
                    
                    if (keyword_only_part is None):
                        keyword_only = False
                    else:
                        keyword_only = True
            else:
                optional = False
                keyword_only = False
        else:
            optional = False
            keyword_only = False
        
        if name.startswith('**'):
            optional = True
            keyword_only = True
        
        elif name.startswith('*'):
            optional = True
            keyword_only = False
        
        self.optional = optional
        self.keyword_only = keyword_only
        
        if header_contents:
            type_ = header
            default = header.split_at(PARAMETER_DEFAULT_START_RP)
        else:
            type_ = None
            default = None
        
        self.type = type_
        self.default = default
    
    
    def get_mask(self):
        """
        Gets the mask of the used features by the parameter sub part.
        
        Returns
        -------
        mask : `int`
        """
        # We add name every time
        mask = PARAMETER_MASK_NAME
        
        if (self.description is not None):
            mask |= PARAMETER_MASK_DESCRIPTION
        
        if self.keyword_only:
            mask |= PARAMETER_MASK_KEYWORD_ONLY
        
        if self.optional:
            mask |= PARAMETER_MASK_OPTIONAL
        
        if (self.type is not None):
            mask |= PARAMETER_MASK_TYPE
        
        if (self.default is not None):
            mask |= PARAMETER_MASK_DEFAULT
        
        return mask
    
    
    def serialize(self, parent, mask):
        """
        Serializes the parameter sub section to html string parts.
        
        This method is a generator.
        
        Parameters
        ----------
        parent : ``ParameterSerializer``
            The parent parameter serializer.
        mask : `int`
            Mask to serialize the mask based of.
        
        Yields
        ------
        html : `str`
        """
        yield '<tr>'
        
        if mask & PARAMETER_MASK_NAME:
            yield '<td class="parameter_table_name">'
            
            name = self.name
            if name:
                yield html_escape(name)
            
            yield '</td>'
        
        if mask & PARAMETER_MASK_TYPE:
            yield '<td class="parameter_table_type">'
            
            type_ = self.type
            if (type_ is not None):
                yield from description_serializer(type_, parent.object, parent.path, create_relative_sectioned_link)
            
            yield '</td>'
        
        if mask & PARAMETER_MASK_OPTIONAL:
            yield '<td class="parameter_table_optional">'
            
            if self.optional:
                yield YES_SVG
            
            yield '</td>'
        
        if mask & PARAMETER_MASK_KEYWORD_ONLY:
            yield '<td class="parameter_table_keyword_only">'
            
            if self.keyword_only:
                yield YES_SVG
            
            yield '</td>'
        
        if mask & PARAMETER_MASK_DEFAULT:
            yield '<td class="parameter_table_default">'
            
            default = self.default
            if (default is not None):
                yield from description_serializer(default, parent.object, parent.path, create_relative_sectioned_link)
            
            yield '</td>'
        
        if mask & PARAMETER_MASK_DESCRIPTION:
            yield '<td class="parameter_table_description">'
            
            description = self.description
            if (description is not None):
                yield from sub_section_serializer(description, parent.object, get_parent_path_of(parent.path),
                    create_relative_sectioned_link)
            
            yield '</td>'
        
        yield '</tr>'
    
    
    def __repr__(self):
        """Returns the parameter sub section's representation."""
        repr_parts = ['<', self.__class__.__name__, ' name = ', repr(self.name)]
        
        type_ = self.type
        if (type_ is not None):
            repr_parts.append(', type = ')
            repr_parts.append(reprlib.repr(type_))
        
        description = self.description
        if (description is not None):
            repr_parts.append(', description = ')
            repr_parts.append(reprlib.repr(description))
        
        if self.optional:
            repr_parts.append(', optional = True')
        
        if self.keyword_only:
            repr_parts.append(', keyword only = True')
        
        repr_parts.append('>')
        return ''.join(repr_parts)


class ParameterSection:
    """
    Represents a parameter's section.
    
    Attributes
    ----------
    parameter_sub_sections : `list` of `ParameterSubSection`
        The stored parameters.
    object : ``UnitBase``
        The owner unit.
    path : ``QualPath``
        Path to use instead of the objects'.
    """
    __slots__ = ('parameter_sub_sections', 'object', 'path')
    
    def __init__(self, section_content, object_, path):
        """
        Creates a new parameter section instance with the given initial content.
        
        Parameters
        ----------
        section_content : `list` of `Any`
            Contained section parts.
        object_ : ``TypeUnit``
            The owner type-unit.
        path : `None`, ``QualPath``
            Path to use instead of the objects'.
        """
        self.parameter_sub_sections = []
        self.object = object_
        if path is None:
            path = object_.path
        self.path = path
        self.extend(section_content)
    
    
    def extend(self, section_content):
        """
        Extends the parameter section with the given content.
        
        Parameters
        ----------
        section_content : `list` of `Any`
            Contained section parts.
        """
        header = None
        for section_content in section_content:
            # section content can be either ``GraveDescription``, `list` of it.
            
            if isinstance(section_content, GravedDescription):
                if header is None:
                    header = section_content
                else:
                    # Unlucky. Parameter definition without description
                    self.parameter_sub_sections.append(ParameterSubSection(header, None))
                    header = section_content
            
            else:
                if header is None:
                    # nani desuka?
                    pass
                else:
                    self.parameter_sub_sections.append(ParameterSubSection(header, section_content))
                    header = None
        
        if (header is not None):
            self.parameter_sub_sections.append(ParameterSubSection(header, None))
    
    
    def serialize(self):
        """
        Serializes the section to html string parts.
        
        This method is a generator.
        
        Yields
        ------
        html : `str`
        """
        mask = 0
        for parameter_sub_section in self.parameter_sub_sections:
            mask |= parameter_sub_section.get_mask()
        
        yield '<table class="parameter_table"><thead><tr>'
        
        if mask & PARAMETER_MASK_NAME:
            yield '<th class="parameter_table_name">Parameter</th>'
        
        if mask & PARAMETER_MASK_TYPE:
            yield '<th class="parameter_table_type">Type</th>'
        
        if mask & PARAMETER_MASK_OPTIONAL:
            yield '<th class="parameter_table_optional">Optional</th>'
        
        if mask & PARAMETER_MASK_KEYWORD_ONLY:
            yield '<th class="parameter_table_keyword_only">Keyword only</th>'
        
        if mask & PARAMETER_MASK_DEFAULT:
            yield '<th class="parameter_table_default">Default</th>'
        
        if mask & PARAMETER_MASK_DESCRIPTION:
            yield '<th class="parameter_table_description">Description</th>'
        
        yield '</tr></thead><tbody>'
        
        for parameter_sub_section in self.parameter_sub_sections:
            yield from parameter_sub_section.serialize(self, mask)
        
        yield '</tbody></table>'
    
    
    def structurize(self):
        """
        Returns the structure of the section.
        
        Returns
        -------
        structure : `None`, ``Structure``
            If the section is unnamed, returns `None`.
        """
        # Since we are building a big table this time, we have nothing to do with this.
        return None


SECTION_NAME_TYPE_DEFAULT_RELATIONS = {
    'Usage': SECTION_TYPE_USAGES,
    'Usages': SECTION_TYPE_USAGES,
    'Yields': SECTION_TYPE_YIELDS,
    'Returns': SECTION_TYPE_RETURNS,
    'Raises': SECTION_TYPE_RAISES,
    'Notes': SECTION_TYPE_NOTES,
}


class TypeSerializer:
    """
    Converts the given type docs to topically broken down parts.
    
    Attributes
    ----------
    object : ``TypeUnit``
        The represented type unit.
    sections : `list` of (``SimpleSection``, ``AttributeSection``, ``UnitSection``, ``ParameterSection``)
        The type's sections.
    path : ``QualPath``
        Path to use instead of the object's.
    """
    __slots__ = ('object', 'sections', 'path')
    
    def __init__(self, object_, path=None):
        """
        Parameters
        ----------
        object_ : ``UnitBase``
            The respective unit.
        path : `None`, ``QualPath`` = `None`, Optional
            Path to use instead of the object's.
        """
        self.object = object_
        if path is None:
            path = object_.path
        self.path = path
        
        section_parts = {}
        
        docs = object_.docs
        if docs is not None:
            for section_name, section_content in docs.sections:
                if section_name is None:
                    section_parts[SECTION_TYPE_DEFAULT] = SimpleSection(None, section_content, object_, path)
                    continue
                
                try:
                    section_type_value = SECTION_NAME_TYPE_DEFAULT_RELATIONS[section_name]
                except KeyError:
                    pass
                else:
                    section_parts[section_type_value] = SimpleSection(section_name, section_content, object_, path)
                    continue
                
                
                if section_name in ('Attributes', 'Instance Attributes'):
                    mentioned_names = get_attribute_section_mentioned_names(section_content)
                    section_parts[SECTION_TYPE_INSTANCE_ATTRIBUTES] = \
                        AttributeSection(section_name, mentioned_names, object_, None)
                    continue
                
                if section_name in ('Class Attributes', 'Type Attributes'):
                    mentioned_names = get_attribute_section_mentioned_names(section_content)
                    section_parts[SECTION_TYPE_OTHER_PARAMETERS] = \
                        AttributeSection(section_name, mentioned_names, object_, None)
                    continue
                
                if ATTRIBUTE_SECTION_NAME_RP.fullmatch(section_name) is not None:
                    try:
                        existing = section_parts[SECTION_TYPE_X_ATTRIBUTES]
                    except KeyError:
                        existing = section_parts[SECTION_TYPE_X_ATTRIBUTES] = []
                    
                    mentioned_names = get_attribute_section_mentioned_names(section_content)
                    existing.append(AttributeSection(section_name, mentioned_names, object_, path))
                    continue
                
                try:
                    existing = section_parts[SECTION_TYPE_X]
                except KeyError:
                    existing = section_parts[SECTION_TYPE_X] = []
                
                existing.append(SimpleSection(section_name, section_content, object_, path))
                continue
        
        collected_instance_attributes = []
        collected_properties = []
        collected_methods = []
        collected_classes = []
        
        # Do not mention `ClassAttributeUnit`. There might be a mention, why there are not mentioned. For example at the
        # case of precreation they are probably mentioned inside of a table.
        
        for item in object_.references.items():
            unit_type = type(item[1])
            if unit_type is PropertyUnit:
                container = collected_properties
            elif unit_type is InstanceAttributeUnit:
                container = collected_instance_attributes
            elif unit_type is FunctionUnit:
                container = collected_methods
            elif unit_type is TypeUnit:
                container = collected_classes
            else:
                # We do not care.
                continue
            
            container.append(item)
            continue
        
        for instance_attribute_name, _ in collected_instance_attributes:
            try:
                section_attributes_i = section_parts[SECTION_TYPE_INSTANCE_ATTRIBUTES]
            except KeyError:
                section_attributes_i = None
            else:
                if section_attributes_i.contains(instance_attribute_name):
                    continue
            
            # Extra?
            try:
                section_attributes_x = section_parts[SECTION_TYPE_X_ATTRIBUTES]
            except KeyError:
                pass
            else:
                for section_attribute_x in section_attributes_x:
                    if section_attribute_x.contains(instance_attribute_name):
                        found = True
                        break
                else:
                    found = False
                
                if found:
                    continue
            
            # Maybe misplaced?
            try:
                section_attributes_c = section_parts[SECTION_TYPE_CLASS_ATTRIBUTES]
            except:
                pass
            else:
                if section_attributes_c.contains(instance_attribute_name):
                    continue
            
            
            if section_attributes_i is None:
                section_parts[SECTION_TYPE_INSTANCE_ATTRIBUTES] = \
                    AttributeSection('Attributes', {instance_attribute_name}, object_, path)
            else:
                section_attributes_i.add(instance_attribute_name)
            continue
        
        if collected_properties:
            collected_properties = [item for item in sorted(collected_properties, key = item_sort_key)]
            section_parts[SECTION_TYPE_PROPERTIES] = UnitSection('Properties', object_, collected_properties, path)
        
        if collected_methods:
            collected_methods = [item for item in sorted(collected_methods, key = item_sort_key)]
            section_parts[SECTION_TYPE_METHODS] = UnitSection('Methods', object_, collected_methods, path)
        
        if collected_classes:
            collected_classes = [item for item in sorted(collected_classes, key = item_sort_key)]
            section_parts[SECTION_TYPE_CLASSES] = UnitSection('Classes', object_, collected_classes, path)
        
        sections = []
        
        for item in sorted(section_parts.items()):
            section = item[1]
            if type(section) is list:
                sections.extend(section)
            else:
                sections.append(section)
        
        self.sections = sections
        
    def serialize(self):
        """
        Serializes the attribute section to html string parts.
        
        This method is a generator.
        
        Yields
        ------
        html : `str`
        """
        path = self.path
        
        name = path.parts[-1]
        prefix = get_anchor_prefix_for(path)
        tier = get_tier_for(path)
        
        yield '<h'
        yield str(tier)
        yield '>'
        yield from anchor_for_serializer(anchor_escape(prefix))
        yield html_escape(name)
        yield '<div class="underline"></div></h'
        yield str(tier)
        yield '>'
        
        if tier > 1:
            yield '<div class="sub_unit">'
        
        for section in self.sections:
            yield from section.serialize()
        
        if tier > 1:
            yield '</div>'
        
        return

    def structurize(self):
        """
        Creates a section structure for the represented unit.
        
        Returns
        -------
        structure : ``Structure``
        """
        children = []
        for section in self.sections:
            child = section.structurize()
            if child is None:
                continue
            
            children.append(child)
        
        if not children:
            children = None
        
        path = self.path
        title = path.parts[-1]
        prefixed_title = get_anchor_prefix_for(path)
        
        return Structure(title, prefixed_title, children)

class UnitListerSection:
    """
    Serializer to list units inside of a module section.
    
    Attributes
    ----------
    title : `str`
        The section's title.
    object : ``TypeUnit``
        The represented parent object.
    units : `list` of ``UnitBase``
        The contained units.
    path : ``QualPath``
        Path to use instead of the object's.
    """
    __slots__ = ('title', 'object', 'units', 'path',)
    
    def __init__(self, title, object_, units, path):
        """
        Creates a new unit lister section.
        
        Parameters
        ----------
        title : `str`
            The section's title.
        object_ : ``TypeUnit``
            The represented parent object.
        units : `list` of ``UnitBase``
            The contained units.
        path : ``QualPath``
            Path to use instead of the object's.
        """
        self.title = title
        self.object = object_
        self.units = units
        if path is None:
            path = object_.path
        self.path = path
    
    def serialize(self):
        """
        Serializes the unit listing.
        
        This method is a generator.
        
        Yields
        ------
        html : `str`
        """
        title = self.title
        path = self.path
        prefix = get_anchor_prefix_for(path)
        if prefix:
            prefix = f'{prefix}-{anchor_escape(title)}'
        else:
            prefix = anchor_escape(title)
        
        tier = get_tier_for(path) + 1
        
        yield '<h'
        yield str(tier)
        yield '>'
        yield from anchor_for_serializer(prefix)
        yield html_escape(title)
        yield '<div class="underline"></div></h'
        yield str(tier)
        yield '><ul class="unit_listing">'
        
        for unit in self.units:
            url = create_relative_link(path, unit.path)
            
            name = html_escape(unit.name)
            yield '<li><a href="'
            yield url
            yield '" title="'
            yield name
            yield '">'
            yield name
            yield '</a></li>'
        
        yield '</ul>'
    
    def structurize(self):
        """
        Creates a section structure for the represented unit listing.
        
        Returns
        -------
        structure : ``Structure``
        """
        title = self.title
        child_prefixed_title = anchor_escape(title)
        return Structure(title, child_prefixed_title, None)


class ModuleSerializer:
    """
    Collects the given module to topically broken down parts.
    
    Attributes
    ----------
    object : ``ModuleUnit``
        The represented type unit.
    sections : `list` of (``SimpleSection``, ``AttributeSection``, ``UnitSection``)
        The type's sections.
    path : `None`, ``QualPath``
        Path to use instead of the object's.
    """
    __slots__ = ('object', 'sections', 'path')
    
    def __init__(self, object_, path=None):
        """
        Creates a module serializer to html serialize a module.
        
        Parameters
        ----------
        object_ : ``ModuleUnit``
            The module to serialize.
        path : `None`, ``QualPath``
            Path to use instead of the object's.
        """
        self.object = object_
        if path is None:
            path = object_.path
        self.path = path
        section_parts = {}
        
        docs = object_.docs
        if (docs is not None):
            for section_name, section_content in docs.sections:
                if section_name is None:
                    section_parts[SECTION_TYPE_DEFAULT] = SimpleSection(None, section_content, object_, path)
                    continue
                
                try:
                    section_type_value = SECTION_NAME_TYPE_DEFAULT_RELATIONS[section_name]
                except KeyError:
                    pass
                else:
                    section_parts[section_type_value] = SimpleSection(section_name, section_content, object_, path)
                    continue
                
                if section_name in ('Attributes', 'Instance Attributes'):
                    mentioned_names = get_attribute_section_mentioned_names(section_content)
                    section_parts[SECTION_TYPE_INSTANCE_ATTRIBUTES] = \
                        AttributeSection(section_name, mentioned_names, object_, None)
                    continue
                
                if section_name in ('Class Attributes', 'Type Attributes'):
                    mentioned_names = get_attribute_section_mentioned_names(section_content)
                    section_parts[SECTION_TYPE_OTHER_PARAMETERS] = \
                        AttributeSection(section_name, mentioned_names, object_, None)
                    continue
                
                if ATTRIBUTE_SECTION_NAME_RP.fullmatch(section_name) is not None:
                    try:
                        existing = section_parts[SECTION_TYPE_X_ATTRIBUTES]
                    except KeyError:
                        existing = section_parts[SECTION_TYPE_X_ATTRIBUTES] = []
                    
                    mentioned_names = get_attribute_section_mentioned_names(section_content)
                    existing.append(AttributeSection(section_name, mentioned_names, object_, None))
                    continue
                
                try:
                    existing = section_parts[SECTION_TYPE_X]
                except KeyError:
                    existing = section_parts[SECTION_TYPE_X] = []
                
                existing.append(SimpleSection(section_name, section_content, object_, path))
                continue
        
        collected_functions = []
        collected_classes = []
        collected_modules = []
        for item in object_.references.items():
            unit_type = type(item[1])
            if unit_type is FunctionUnit:
                container = collected_functions
            elif unit_type is TypeUnit:
                container = collected_classes
            elif unit_type is ModuleUnit:
                container = collected_modules
            else:
                continue
            
            container.append(item)
            continue
        
        if collected_functions:
            collected_functions = [item[1] for item in sorted(collected_functions, key = item_sort_key)]
            section_parts[SECTION_TYPE_FUNCTIONS] = UnitListerSection('Functions', object_, collected_functions, path)
        
        if collected_classes:
            collected_classes = [item[1] for item in sorted(collected_classes, key = item_sort_key)]
            section_parts[SECTION_TYPE_CLASSES] = UnitListerSection('Classes', object_, collected_classes, path)
        
        if collected_modules:
            collected_modules = [item[1] for item in sorted(collected_modules, key = item_sort_key)]
            section_parts[SECTION_TYPE_MODULES] = UnitListerSection('Modules', object_, collected_modules, path)
        
        sections = []
        
        for item in sorted(section_parts.items()):
            section = item[1]
            if type(section) is list:
                sections.extend(section)
            else:
                sections.append(section)
        
        self.sections = sections
    
    def serialize(self):
        """
        Serializes the attribute section to html string parts.
        
        This method is a generator.
        
        Yields
        ------
        html : `str`
        """
        path = self.path
        name = path.parts[-1]
        
        yield '<h1>'
        yield from anchor_for_serializer(anchor_escape(name))
        yield html_escape(name)
        yield '<div class="underline"></div></h1>'
        
        for section in self.sections:
            yield from section.serialize()
        
        return
    
    def structurize(self):
        """
        Creates a section structure for the represented unit.
        
        Returns
        -------
        structure : ``Structure``
        """
        children = []
        for section in self.sections:
            child = section.structurize()
            if child is None:
                continue
            
            children.append(child)
        
        if not children:
            children = None
        
        title = self.path.parts[-1]
        prefixed_title = anchor_escape(title)
        
        return Structure(title, prefixed_title, children)

UNIT_CONVERSION_TABLE = {
    PropertyUnit: FunctionOrPropertySerializer,
    FunctionUnit: FunctionOrPropertySerializer,
    TypeUnit: TypeSerializer,
    ModuleUnit: ModuleSerializer,
}

@export
def html_serialize_docs_extended(object_, get_html, get_structure):
    """
    Serializes the given docs to one big html code.
    
    Not like ``html_serialize_docs`` this serialization serializes all the methods and properties of the object as well.
    
    Parameters
    ----------
    object_ : ``UnitBase``
        The respective unit.
    get_html : `bool`
        Whether html code string should be created and returned.
    get_structure : `bool`
        Whether structure of the created html code string should be created.
    
    Returns
    -------
    html : `None`  or `str`
        The created html code if possible to create or applicable.
    structure : `None`, ``Structure``
        The structure of the html code if possible to create or applicable.
    """
    try:
        serializer_type = UNIT_CONVERSION_TABLE[type(object_)]
    except KeyError:
        html = None
        structure = None
    else:
        serializer = serializer_type(object_)
        if get_html:
            html = ''.join(serializer.serialize())
        else:
            html = None
        
        if get_structure:
            structure = serializer.structurize()
        else:
            structure = None
    
    return html, structure
