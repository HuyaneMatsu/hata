# -*- coding: utf-8 -*-
from html import escape as html_escape
from .graver import GRAMMAR_CHARS, GRAVE_TYPE_GLOBAL_REFERENCE, GravedListing, GravedDescription, GravedTable, \
    GravedCodeBlock
from ...backend.quote import quote

def create_relative_link(source, target):
    """
    Creates relative link from 1 object to the other one.
    
    Parameters
    ----------
    source : ``UnitBase`` instance
        Source object.
    target : ``UnitBase`` instance
        Target object.
    
    Returns
    -------
    url : `str`
        Gneerated relative url.
    """
    source_parts = source.path.parts.copy()
    target_parts = target.path.parts.copy()
    
    last_removed = None
    while source_parts and target_parts and source_parts[0] == target_parts[0]:
        del source_parts[0]
        last_removed = target_parts.pop(0)
    
    if len(source_parts) == 0:
        if len(target_parts) == 0:
            if last_removed is None:
                url = '/'
            else:
                url = last_removed
        elif len(target_parts) == 1:
            if last_removed is None:
                url = '/'+target_parts[0]
            else:
                url = '/'.join([last_removed, target_parts[0]])
        else:
            if last_removed is None:
                url = '/'.join(['', *target_parts])
            else:
                url = '/'.join([last_removed, *target_parts])
    elif len(source_parts) == 1:
        if len(target_parts) == 0:
            url = './'
        elif len(target_parts) == 1:
            url = target_parts[0]
        else:
            url = '/'.join(target_parts)
    else:
        if len(target_parts) == 0:
            url = '../'*(len(source_parts)-1)
        elif len(target_parts) == 1:
            url = '../'*(len(source_parts)-1) + target_parts[0]
        else:
            url = '../'*(len(source_parts)-1) + '/'.join(target_parts[0])
    
    return quote(url, safe=':@', protected='/')


def graved_link(reference, object_):
    """
    Converts the given graved link to it's html text form.
    
    Parameters
    ----------
    reference : `str`
        A reference, what's link should be clickable.
    object_ : ``UnitBase`` instance
        The respective object.
    
    Returns
    -------
    html : `str`
    """
    reference_escaped = html_escape(reference)
    
    referred_object = object_.lookup_reference(reference)
    if referred_object is None:
        return (
            '<code>'
                '<span>'
                    f'{reference_escaped}'
                '</span>'
            '</code>'
                )
    
    url = create_relative_link(object_, referred_object)
    
    return (
        f'<a href="{url}" title="{reference_escaped}">'
            '<code>'
                '<span>'
                    f'{reference_escaped}'
                '</span>'
            '</code>'
        '</a>'
            )

def graved_text(text):
    """
    Converts the given graved text to it's html text form.
    
    Parameters
    ----------
    text : `str`
        Graved content.
    
    Returns
    -------
    html : `str`
    """
    text = html_escape(text)
    return (
        '<code>'
            f'{text}'
        '</code>'
            )

def graved_to_escaped(graved, object_):
    """
    Translates the given graved content to html escaped words.
    
    Parameters
    ----------
    graved : `None` or `list` of (`str`, ``Grave``) elements
        Graved content.
    object_ : ``UnitBase``
        The respective unit.
    
    Returns
    -------
    escaped : `None` or `str`
    """
    if graved is None:
        return None
    
    words = []
    for element in graved:
        if type(element) is str:
            if words:
                last = words[-1]
                starter = last[0]
                if element[0] in GRAMMAR_CHARS:
                    add_space_before = False
                elif starter == '`':
                    add_space_before = True
                else:
                    add_space_before = True
            else:
                add_space_before = False
            
            element = html_escape(element)
            local_words = element.split(' ')
            if (not add_space_before) and words:
                words[-1] = words[-1]+local_words.pop(0)
            
            words.extend(local_words)
        
        else:
            content = element.content
            
            if element.type == GRAVE_TYPE_GLOBAL_REFERENCE:
                local_word = graved_link(content, object_)
            else:
                local_word = graved_text(content)
            
            words.append(local_word)
    
    return ' '.join(words)


def description_serializer(description, object_):
    """
    Serializes the given description.
    
    Parameters
    ----------
    description : ``GravedDescription``
        The table to serialize
    object_ : ``UnitBase``
        The respective unit.
    
    Yields
    ------
    html_part : `str`
    """
    yield '<p>'
    content = graved_to_escaped(description.content, object_)
    yield content
    yield '</p>'


def code_block_serializer(code_block, object_):
    """
    Serializes the given description.
    
    Parameters
    ----------
    code_block : ``GravedCodeBlock``
        The table to serialize
    object_ : ``UnitBase``
        The respective unit.
    
    Yields
    ------
    html_part : `str`
    """
    yield '<div class="code_block"><pre>'
    lines = code_block.lines
    index = 0
    limit = len(lines)
    while True:
        line = lines[index]
        yield html_escape(line)
        index += 1
        if index == limit:
            break
        yield '<br>'
    yield '</pre></div>'


def table_serializer(table, object_):
    """
    Serializes the given table.
    
    Parameters
    ----------
    table : ``GravedTable``
        The table to serialize
    object_ : ``UnitBase``
        The respective unit.
    
    Yields
    ------
    html_part : `str`
    """
    head_line, *content_lines = table
    yield '<table><thead><tr>'
    for element in head_line:
        yield '<th>'
        
        content = graved_to_escaped(element, object_)
        if (content is not None):
            yield content
        
        yield '</th>'
    
    yield '</tr></thead>'
    if content_lines:
        yield '<tbody>'
        
        for line in content_lines:
            yield '<tr>'
            for element in line:
                yield '<td>'
                
                content = graved_to_escaped(element, object_)
                if (content is not None):
                    yield content
                
                yield '</td>'
            
            yield '</tr>'
        
        yield '</tbody>'
    
    yield '</table>'


def listing_element_serializer(listing_element, object_):
    """
    Serializes the given listing element.
    
    Parameters
    ----------
    listing_element : ``GravedListingElement``
        The listing element to seralize.
    object_ : ``UnitBase``
        The respective unit.
    
    Yields
    ------
    html_part : `str`
    """
    yield '<li>'
    head = listing_element.head
    if (head is not None):
        head = graved_to_escaped(head, object_)
        yield head
    
    content = listing_element.content
    if (content is not None):
        yield from sub_section_serializer(content, object_)
    
    yield '</li>'


def listing_serializer(listing, object_):
    """
    Serializes the given listing.
    
    Parameters
    ----------
    listing : ``GravedListing``
        The listing element to seralize.
    object_ : ``UnitBase``
        The respective unit.
    
    Yields
    ------
    html_part : `str`
    """
    yield '<ul>'
    
    for listing_element in listing.elements:
        yield from listing_element_serializer(listing_element, object_)
    
    yield '</ul>'


def section_title_serializer(title):
    """
    Serializes the given section title.
    
    Parameters
    ----------
    title : `str`
        The title to serialize
    
    Yields
    ------
    html_part : `str`
    """
    if title is None:
        return
    
    yield '<h2>'
    yield html_escape(title)
    yield '</h2>'


def section_serializer(section, object_):
    """
    Serializes the given section.
    
    Parameters
    ----------
    section : `tuple` ((`str` or `None`), `list` of `Any`)
        The title to serialize.
    object_ : ``UnitBase``
        The respective unit.
    
    Yields
    ------
    html_part : `str`
    """
    section_name, section_parts = section
    yield from section_title_serializer(section_name)
    yield from sub_section_serializer(section_parts, object_)


def sub_section_serializer(sub_section, object_):
    """
    Deserializes the given sub-section to converters.
    
    Parameters
    ----------
    sub_section : `list` of `Any`
        The source sub-section..
    object_ : ``UnitBase``
        The respective unit.
    
    Yields
    -----------
    html_part : `str`
    """
    for element in sub_section:
        # If the converter is a sub section converter, indent it
        converter = CONVERTER_TABLE[type(element)]
        if converter is sub_section_serializer:
            yield '<div class="sub_section">'
            yield from converter(element, object_)
            yield '</div>'
        else:
            yield from converter(element, object_)


CONVERTER_TABLE = {
    list : sub_section_serializer,
    GravedListing : listing_serializer,
    GravedDescription : description_serializer,
    GravedTable : table_serializer,
    GravedCodeBlock : code_block_serializer,
        }


def html_serialize_docs(docs, object_):
    """
    Serializes the given docs to one big string.
    
    Parameters
    ----------
    docs : ``DocString``
        The docstring to serialize.
    object_ : ``UnitBase``
        The respective unit.
    
    Returns
    -------
    result : `str`
    """
    result = []
    
    for section in docs.sections:
        result.extend(section_serializer(section, object_))
    
    return ''.join(result)
