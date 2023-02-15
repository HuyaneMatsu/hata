__all__ = ('show_warnings',)

import re, sys
from ast import literal_eval


GRAVE_TYPE_BUILTIN = 0
GRAVE_TYPE_EXPRESSION = 1
GRAVE_TYPE_LOCAL_REFERENCE = 2
GRAVE_TYPE_GLOBAL_REFERENCE = 3
GRAVE_TYPE_QUOTE = 4
GRAVE_TYPE_LINK = 5

WARNINGS = []

GRAVE_URL_MATCHER = re.compile(f'(.*?):(https?://.*)')

class DocWarning:
    """
    Represents a documentation warning.
    
    Attributes
    ----------
    path : ``QualPath``
        The exact path of the warning.
    reason : `str`
        TextDescription of the error.
    """
    __slots__ = ('path', 'reason')
    
    def __new__(cls, path, reason):
        """
        Creates a new ``DocWarning`` with the given parameters.
        
        Parameters
        ----------
        path : ``QualPath``
            The exact path of the warning.
        reason : `str`
            TextDescription of the error.
        
        Returns
        -------
        self : ``DocWarning``
        """
        self = object.__new__(cls)
        self.path = path
        self.reason = reason
        
        WARNINGS.append(self)
        return self
    
    def __repr__(self):
        """Returns the representation of the doc-warning."""
        return f'{self.__class__.__name__}(path={self.path!r}, reason={self.reason!r})'
    
    @property
    def message(self):
        """
        A message representing the warning.
        
        Returns
        -------
        message : `str`
        """
        return f'{self.__class__.__name__} at {self.path!s}:\n>> {self.reason}\n'


def show_warnings(file = None):
    """
    Writes the warning messages to the given file exhausting them.
    
    Parameters
    ----------
    file : `None`, `file-like` = `None`, Optional
        File like to write the warnings to. Defaults to `sys.stderr`.
    """
    if file is None:
        file = sys.stderr
    
    while WARNINGS:
        warning = WARNINGS.pop()
        file.write(warning.message)


EXPECTED_BUILTIN_NAMES = {
    'int',
    'str',
    'bytes-like',
    'datetime',
    'float',
    'type',
    'bytes',
    'snowflake',
    'dict',
    'list',
    'set',
    'bytearray',
    'memoryview',
    'function',
    'async',
    'callable',
    'async-callable',
    'async-function',
    'method',
    'method-like',
    'function-like',
    'Any',
}

GRAMMAR_CHARS = {
    '.',
    ',',
    '-',
    '!',
    '?',
    ';',
    ':',
    '(',
    ')',
    ']',
    '[',
}

DO_NOT_ADD_SPACE_AFTER = {
    '(',
    '[',
}

class Grave:
    """
    Represents a string inside of '`' characters.
    
    Attributes
    ----------
    content : `str`
        The string inside of the '`' characters.
    type : `int`
        Type identifier for the grave. Possible values:
        
        +-------------------------------+-------+
        | Respective name               | Value |
        +===============================+=======+
        | GRAVE_TYPE_BUILTIN            | 0     |
        +-------------------------------+-------+
        | GRAVE_TYPE_EXPRESSION         | 1     |
        +-------------------------------+-------+
        | GRAVE_TYPE_LOCAL_REFERENCE    | 2     |
        +-------------------------------+-------+
        | GRAVE_TYPE_GLOBAL_REFERENCE   | 3     |
        +-------------------------------+-------+
        | GRAVE_TYPE_QUOTE              | 4     |
        +-------------------------------+-------+
    """
    __slots__ = ('content', 'type', )
    
    def __init__(self, content, type_):
        """
        Creates a new ``Grave`` from the given parameters.
        
        Parameters
        ----------
        content : `str`
            The string inside of the '`' characters.
        type_ : `int`
            Type identifier for the grave.
        """
        self.content = content
        self.type = type_
    
    def __repr__(self):
        """Returns the grave's representation."""
        return f'{self.__class__.__name__}(content={self.content!r}, type={self.type})'
    
    def __eq__(self, other):
        """Returns whether the two graves are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.type!= other.type:
            return False
        
        if self.content != other.content:
            return False
        
        return True


def get_part_around(content, index):
    """
    Gets the part of the given `content` around the given `index`.
    
    Parameters
    ----------
    content : `str`
        The content, around what the part will be cut out.
    index : `str`
        The index of around where the part will be cut out.
    """
    result = []
    
    low_limit = index - 25
    if low_limit < 0:
        low_limit = 0
    elif low_limit > 0:
        result.append('... ')
    
    high_limit = index + 25
    if high_limit > len(content):
        high_limit = len(content)
    
    result.append(content[low_limit:high_limit])
    
    if high_limit < len(content):
        result.append(' ...')
    
    return ''.join(result)


def build_graves(text):
    """
    Builds graves from the given text.
    
    Parameters
    ----------
    text : `str`
    
    Returns
    -------
    content : `list` of `str`, ``Grave``
        Broke down content.
    warnings : `list` of `str`
        Detected graving mistakes inside of the given text.
    """
    content = []
    warnings = []
    
    grave_end = 0
    while True:
        grave_start = text.find('`', grave_end)
        if grave_start == -1:
            if grave_end != len(text):
                section = text[grave_end:]
                if content:
                    last = content[-1]
                    if type(last) is str:
                        del content[-1]
                        section = last + section
                
                content.append(section)
            break
        
        if grave_start == len(text):
            warnings.append(f'Not ended grave character: {get_part_around(text, grave_start)!r}')
            break
        
        if grave_start == grave_end:
            if grave_end != 0:
                warnings.append(f'Empty ungraved section: {get_part_around(text, grave_end)!r}')
        else:
            section = text[grave_end:grave_start]
            if content:
                last = content[-1]
                if type(last) is str:
                    del content[-1]
                    section = last + section
            content.append(section)
        
        grave_start += 1
        if grave_start < len(text) and text[grave_start] == '`':
            double_grave = True
            grave_start += 1
        else:
            double_grave = False
        
        grave_end = text.find('`', grave_start)
        if grave_end == -1:
            section = text[grave_start:]
            if content:
                last = content[-1]
                if type(last) is str:
                    del content[-1]
                    section = last + section
                    
            content.append(section)
            warnings.append(f'Not ended grave section: {get_part_around(text, len(section))!r}')
            break
        
        if double_grave:
            if grave_end > len(text) - 2 or text[grave_end + 1] != '`':
                section = text[grave_start:grave_end]
                if content:
                    last = content[-1]
                    if type(last) is str:
                        del content[-1]
                        section = last + section
                
                content.append(section)
                warnings.append(f'Not ended double grave section: {get_part_around(text, len(section))!r}')
            else:
                if grave_start == grave_end:
                    warnings.append(f'Empty double grave: {get_part_around(text, grave_end)!r}')
                else:
                    reference = text[grave_start:grave_end]
                    content.append(Grave(reference, GRAVE_TYPE_GLOBAL_REFERENCE))
                
                grave_end += 1
        
        else:
            # single graves cannot be empty
            reference = text[grave_start:grave_end]
            if reference in EXPECTED_BUILTIN_NAMES:
                grave_type = GRAVE_TYPE_BUILTIN
            elif GRAVE_URL_MATCHER.fullmatch(reference) is not None:
                grave_type = GRAVE_TYPE_LINK
            else:
                try:
                    literal_eval(reference)
                except SyntaxError as err:
                    # warnings.append(f'{err.__class__.__name__}({err}) at a single grave: {reference!r}')
                    grave_type = GRAVE_TYPE_QUOTE
                except ValueError:
                    grave_type = GRAVE_TYPE_LOCAL_REFERENCE
                else:
                    grave_type = GRAVE_TYPE_EXPRESSION
            content.append(Grave(reference, grave_type))
        
        grave_end += 1
    
    for index in reversed(range(len(content))):
        part = content[index]
        if type(part) is not str:
            continue
        
        part = part.strip()
        if not part:
            del content[index]
            continue
        
        content[index] = part
    
    return content, warnings


def build_graves_on_subsection(sub_section, path):
    """
    Graves the given sub section.
    
    Parameters
    ----------
    sub_section : `list` of `Any`
        The subsection to grave.
    path : ``QualPath``
        The path of the respective docstring.
    
    Returns
    -------
    result : `None`, `list` of `Any`
        If would have return an empty list, returns `None` instead.
    """
    result = []
    for element in sub_section:
        if type(element) is list:
            element = build_graves_on_subsection(element, path)
        else:
            element = element.graved(path)
        
        if element is None:
            continue
        
        result.append(element)
    
    if (not result):
        result = None
    
    return result

def graved_to_source_text(graved):
    """
    Builds a graved content back to it's source like form.
    
    Parameters
    ----------
    graved : `None`, `list` of (`str`, ``Grave``) elements
    
    Returns
    -------
    text : `None`, `str`
    """
    if graved is None:
        return None
    
    result = []
    
    for element in graved:
        if type(element) is str:
            if result:
                last = result[-1]
                starter = last[0]
                if element[0] in GRAMMAR_CHARS:
                    add_space_before = False
                elif starter == '`':
                    add_space_before = True
                else:
                    add_space_before = True
            else:
                add_space_before = False
            
            if add_space_before:
                result.append(' ')
            
            result.append(element)
        
        else:
            if element.type == GRAVE_TYPE_GLOBAL_REFERENCE:
                graver = '``'
            else:
                graver = '`'
            
            if result:
                add_space_before = True
            else:
                add_space_before = False
            
            if add_space_before:
                result.append(' ')
            
            result.append(graver)
            result.append(element.content)
            result.append(graver)
    
    return ''.join(result)


class GravedDescription:
    """
    Represents a graved description part of a docstring.
    
    Attributes
    ----------
    content : `list` of (`str`, ``Grave``)
        The graved content of the description.
    """
    __slots__ = ('content', )
    
    def __new__(cls, parent, path):
        """
        Creates a new graved description.
        
        Parameters
        ----------
        parent : ``TextDescription``
            The source description.
        path : ``QualPath``
            The path of the respective docstring.
        
        Returns
        -------
        self : `None`, ``GravedDescription``
            Returns `None`, if would have been creating an empty description.
        """
        content, warnings = build_graves(parent._content)
        apply_warnings_to_path(warnings, path)
        if not content:
            DocWarning(path, 'Empty description would have been created.')
            return None
        
        self = object.__new__(cls)
        self.content = content
        return self
    
    
    def __repr__(self):
        """Returns the graved description's representation."""
        return f'<{self.__class__.__name__} content={graved_to_source_text(self.content)!r}>'
    
    
    def copy(self):
        """
        Copies the graved description.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.content = self.content.copy()
        return new
    
    
    def split_at(self, pattern):
        """
        Splits the description when the pattern matches.
        
        Parameters
        ----------
        pattern : `_sre.SRE_Pattern`
            The pattern to split based on.
            
            The pattern should split with 2 groups on success.
        
        Returns
        -------
        other : `None`, ``GravedDescription``
            The other split down value on success.
        """
        content = self.content
        
        for index in range(0, len(content)):
            part = content[index]
            if isinstance(part, str):
                match = pattern.fullmatch(part)
                if (match is not None):
                    break
        else:
            return
        
        pre_part, post_part = match.groups()
        
        new_parts = []
        if post_part:
            new_parts.append(post_part)
        
        new_parts.extend(content[index+1:])
        
        if pre_part:
            content[index] = pre_part
            del content[index+1:]
        else:
            del content[index:]
        
        other = object.__new__(type(self))
        other.content = new_parts
        return other


class GravedAttributeDescription:
    """
    Represents an attribute's graved header part.
    
    Attributes
    ----------
    name : `str`
        The respective attribute's name.
    separator : `str`
        Separator used between the attribute's name and it's type description.
    content : `str`
        The type description of the attribute.
    """
    __slots__ = ('name', 'separator', 'content')
    
    def __new__(cls, name, separator, content):
        """
        Creates a ``GravedAttributeDescription`` with the given parameters.
        
        Attributes
        ----------
        name : `str`
            The respective attribute's name.
        separator : `str`
            Separator used between the attribute's name and it's type description.
        content : `str`
            The type description of the attribute.
        
        Returns
        -------
        self : ``GravedAttributeDescription``
        """
        self = object.__new__(cls)
        self.name = name
        self.separator = separator
        self.content = content
        return self
    
    def __repr__(self):
        """Returns the graved description's representation."""
        return (
            f'<{self.__class__.__name__} name = {self.name!r}, separator = {self.separator!r}, content = '
            f'{graved_to_source_text(self.content)!r}>'
        )


class GravedCodeBlock:
    """
    Represents a graved code block part of a docstring.
    
    Attributes
    ----------
    language : `None`, `str`
        The language of the code if applicable.
    lines : `list` of `str`
        The lines of the code-block
    """
    __slots__ = ('language', 'lines', )
    
    def __new__(cls, parent, path):
        """
        Creates a new graved code block..
        
        Parameters
        ----------
        parent : ``TextCodeBlock``
            The source code block.
        path : ``QualPath``
            The path of the respective docstring.
        
        Returns
        -------
        self : ``GravedCodeBlock``
        """
        lines = []
        for line in parent._lines:
            if len(line) > 120:
                DocWarning(path, f'Code line length over 120 chars: {line!r}')
                line = line[:120]
            lines.append(line)
        
        self = object.__new__(cls)
        self.language = parent._language
        self.lines = lines
        return self
    
    def __repr__(self):
        """Returns the graved code block's representation."""
        result = ['<', self.__class__.__name__]
        
        language = self.language
        if language is None:
            result.append(' language=')
            result.append(repr(language))
            
            add_comma = True
        else:
            add_comma = False
        
        if add_comma:
            result.append(', ')
        
        result.append(' lines=')
        result.append(repr(self.lines))
        
        result.append('>')
        
        return ''.join(result)


class GravedTable:
    """
    Represents a graved table.
    
    Parameters
    ----------
    array : `list` of (`None`, (`list` of (`str`, ``Grave``) elements)) elements
        The elements of the table
    size : `tuple`  (`int`, `int`)
        The size of the table.
    """
    __slots__ = ('array', 'size', )
    
    def __new__(cls, parent, path):
        """
        Creates a new graved table instance.
        
        Parameters
        ----------
        parent : ``TextTable``
            The source table.
        path : ``QualPath``
            The path of the respective docstring.
        
        Returns
        -------
        self : `None`, ``GravedTable``
            Returns `None` if would return an empty table.
        """
        array = []
        x, y = parent._size
        for line in parent:
            new_line = []
            
            check_for_only_nones = False
            for element in line:
                if (element is None):
                    DocWarning(path, 'Empty table element.')
                else:
                    element, warnings = build_graves(element)
                    apply_warnings_to_path(warnings, path)
                    if not element:
                        DocWarning(path, 'Empty table element.')
                        element = None
                        check_for_only_nones = True
                
                new_line.append(element)
            
            if check_for_only_nones:
                for element in new_line:
                    if element is None:
                        continue
                    
                    break
                else:
                    y -= 1
                    continue
        
            array.extend(new_line)
        
        if not array:
            return None
        
        self = object.__new__(cls)
        self.array = array
        self.size = (x, y)
        return self
    
    def __iter__(self):
        """
        Iterates over the table's lines.
        
        This method is a generator.
        
        Yields
        ------
        line : `list` of (`None`, (`list` of (`str`, ``Grave``) elements)
        """
        x, y = self.size
        array = self.array
        index = 0
        for _ in range(y):
            line = []
            for _ in range(x):
                element = array[index]
                index +=1
                
                line.append(element)
            
            yield line
    
    def __repr__(self):
        """Returns the graved table's representation."""
        result = [
            '<',
            self.__class__.__name__,
            ', size=',
            repr(self.size),
            ', table=[',
        ]
        
        for line in self:
            line = [graved_to_source_text(element) for element in line]
            
            result.append(repr(line))
            result.append(', ')
        
        del result[-1]
        
        result.append(']>')
        return ''.join(result)

def apply_warnings_to_path(warnings, path):
    """
    Applies warning to the given path.
    
    Parameters
    ----------
    warnings : `list` of `str`
        The warning to apply.
    path : ``QualPath``
        The path of the respective docstring.
    """
    for warning in warnings:
        DocWarning(path, warning)


class GravedListingElement:
    """
    Represents a graved listing element.
    
    Attributes
    ----------
    content : `None`, `list` of (`str`, ``Grave``)
        The graved content of the listing element.
    head : `None`, `list` of (`str`, ``Grave``)
        The graved head of the element.
    """
    __slots__ = ('content', 'head',)
    def __new__(cls, parent, path):
        """
        Creates a new graved listing element.
        
        Parameters
        ----------
        parent : ``TextListingElement``
            The source listing element.
        path : ``QualPath``
            The path of the respective docstring.
        
        Returns
        -------
        self : `None`, ``GravedListingElement``
            Returns `None`, if would have been creating an empty listing element.
        """
        content = parent._content
        if (content is not None):
            content = build_graves_on_subsection(content, path)
            if content is None:
                DocWarning(path, 'Listing element with empty content.')
        
        head = parent._head
        if head is None:
            DocWarning(path, 'Listing element without empty head.')
        else:
            head, warnings = build_graves(head)
            apply_warnings_to_path(warnings, path)
            if not head:
                DocWarning(path, 'Listing element with empty head.')
                head = None
        
        if None is head is content:
            DocWarning(path, 'Empty listing element would have be created.')
            return None
        
        self = object.__new__(cls)
        self.content = content
        self.head = head
        return self
    
    def __repr__(self):
        """Returns the graved listing element's representation."""
        result = [
            '<',
            self.__class__.__name__,
            ' head=',
            repr(graved_to_source_text(self.head)),
        ]
        
        content = self.content
        if content is not None:
            content = repr(graved_to_source_text(content))
            result.append(', content=')
            result.append(content)
        
        result.append('>')
        
        return ''.join(result)

class GravedListing:
    """
    Represents a graved listing.
    
    Attributes
    ----------
    elements : `list` of ``GravedListingElement``
        The elements of the listing.
    """
    __slots__ = ('elements', )
    def __new__(cls, parent, path):
        """
        Creates a new graved listing instance.
        
        Parameters
        ----------
        parent : ``TextListing``
            The source listing.
        path : ``QualPath``
            The path of the respective docstring.
        
        Returns
        -------
        self : `None`, ``GravedListing``
            Returns `None`, if would have been creating an empty listing.
        """
        elements = []
        for element in parent._elements:
            element = element.graved(path)
            if element is None:
                continue
            
            elements.append(element)
        
        if not elements:
            DocWarning('Empty listing would have be created.')
            return None
        
        self = object.__new__(cls)
        self.elements = elements
        return self
    
    def __repr__(self):
        """Returns the graved listing's representation."""
        return f'<{self.__class__.__name__} elements={self.elements!r}>'


class GravedBlockQuote:
    """
    Represents a graved block quote part of a docstring.
    
    Attributes
    ----------
    descriptions : `list` of `list` of (`str`, ``Grave``)
        Graved description parts of the block quote.
    """
    __slots__ = ('descriptions', )
    def __new__(cls, parent, path):
        """
        Creates a new graved block quote.
        
        Parameters
        ----------
        parent : ``TextBlockQuote``
            The source block quote.
        path : ``QualPath``
            The path of the respective docstring.
        
        Returns
        -------
        self : `None`, ``GravedBlockQuote``
            Returns `None`, if would have been creating an empty graved block quote,
        """
        graved_descriptions = []
        for description in parent._descriptions:
            graved_description = description.graved(path)
            if graved_description is None:
                continue
            
            graved_descriptions.append(graved_description)
        
        if not graved_descriptions:
            DocWarning(path, 'Empty description would have been created.')
            return None
        
        self = object.__new__(cls)
        self.descriptions = graved_descriptions
        return self
    
    def __repr__(self):
        """Returns the graved block quote's representation."""
        return f'<{self.__class__.__name__} descriptions={self.descriptions!r}>'
