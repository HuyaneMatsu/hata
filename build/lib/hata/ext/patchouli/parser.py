# -*- coding: utf-8 -*-
__all__ = ('DocString', )
import re, sys

from .graver import build_graves_on_subsection, GravedListing, GravedListingElement, GravedTable, GravedDescription, \
    GravedCodeBlock, DocWarning, GravedAttributeDescription, GravedBlockQuote

SECTION_NAME_RP = re.compile('(?:[A-Z][a-z]*)(?: [A-Z][a-z]*)*')
SECTION_UNDERLINE_RP = re.compile('[\-]+')
TABLE_BORDER_PATTERN = '\+(?:[\-=]+\+)+'
TABLE_TEXT_PATTERN = '\|(?:[^\|]+\|)+'
TABLE_BORDER_RP = re.compile(TABLE_BORDER_PATTERN)
TABLE_TEXT_RP = re.compile(TABLE_TEXT_PATTERN)
TABLE_ANY_RP = re.compile(f'{TABLE_BORDER_PATTERN}|{TABLE_TEXT_PATTERN}')
TABLE_TEXT_SPLITTER = re.compile('(?:\| )?(.*?) \|')
LISTING_HEAD_LINE_RP = re.compile('[\-]+[ \t]*(.*)')

ATTRIBUTE_SECTION_NAME_RP = re.compile('.*?attributes?', re.I)
ATTRIBUTE_NAME_RP = re.compile('([A-Za-z_][0-9A-Za-z_]*) *([\:\(]) *')

del TABLE_BORDER_PATTERN
del TABLE_TEXT_PATTERN

RIGHT_STRIP_IGNORE = '\\ \t\n'

def remove_indents(lines):
    """
    Removes tailing characters from the right, the base indention and the empty lines from the start and from the end.
    
    Parameters
    ----------
    lines : `list` of `str`
        Input lines.
    
    Returns
    -------
    lines : `None` or (`list` of `str`)
    """
    if not lines:
        return None
    
    # remove tailing characters from the right side
    for index in range(len(lines)):
        lines[index] = lines[index].rstrip(RIGHT_STRIP_IGNORE)
    
    # First line might not be indented, so check it meanwhile it is first.
    first_line = lines[0]
    if first_line and (first_line[0] not in (' ', '\t')):
        first_line_filled = True
    else:
        first_line_filled = False
    
    # Remove empty lines from the end
    while True:
        if not lines:
            return None
        
        if lines[-1]:
            break
        
        del lines[-1]
        continue
    
    # Remove empty lines from the start
    while True:
        if lines[0]:
            break
        
        del lines[0]
        continue
    
    # Collect line indexes, which have content
    content_line_indexes = []
    for index in range(len(lines)):
        line = lines[index]
        if line:
            content_line_indexes.append(index)
    
    # If first line has any content, ignore it when removing indents.
    if first_line_filled and content_line_indexes[0] == 0:
        del content_line_indexes[0]
    
    # Do not remove indents if there is non.
    if content_line_indexes:
        # Calculate indent size
        ignore_index = 0
        
        while True:
            next_char = lines[content_line_indexes[0]][ignore_index]
            if next_char not in ('\t', ' '):
                break
            
            for index in content_line_indexes[1:]:
                char = lines[index][ignore_index]
                if char != next_char:
                    break
                
                continue
            else:
                ignore_index +=1
                continue
            
            break
        
        # Remove indents
        if ignore_index:
            for index in range(first_line_filled, len(lines)):
                line = lines[index]
                
                lines[index] = line[ignore_index:]
                continue
    
    return lines
    
def parse_sections(lines):
    """
    Parses out sections from the given lines.
    
    Parameters
    ----------
    lines : `list` of `str`
        Unindented lines of a docstring.
    
    Returns
    -------
    sections : `list` of `tuple` (`str`, `str`)
    """
    sections = []
    
    section_name = None
    section_lines = []
    
    index = 0
    limit = len(lines)
    
    while True:
        line = lines[index]
        
        # If there are at least 2 lines and we can match:
        if (limit-index) > 2 and (SECTION_NAME_RP.fullmatch(line) is not None) and \
                (SECTION_UNDERLINE_RP.fullmatch(lines[index+1]) is not None):
            # Get the current line out.
            while section_lines:
                if section_lines[-1]:
                    sections.append((section_name, section_lines))
                    section_lines = []
                    break
                
                del section_lines[-1]
                continue
            
            section_name = line
            index += 1
        else:
            section_lines.append(line)
        
        index+=1
        
        if index >= limit:
            while section_lines:
                if section_lines[-1]:
                    sections.append((section_name, section_lines))
                    break
                
                del section_lines[-1]
                continue
            
            break
    
    return sections

def detect_table(lines, index, limit):
    """
    Detects the lines of a table.
    
    Parameters
    ----------
    lines : `list` of `str`
        The lines of the section.
    index : `int`
        The starting index of the table.
    limit : `int`
        The last element's index.
    
    Returns
    -------
    index : `int`
        The index where the table is over. If there was no table, returns the initial index.
    """
    line = lines[index]
    if index+2 <= limit:
        if (TABLE_ANY_RP.fullmatch(line) is not None):
            line2 = lines[index+1]
            if (TABLE_ANY_RP.fullmatch(line2) is not None):
                index += 2
                while True:
                    if index == limit:
                        break
                    
                    line = lines[index]
                    if (TABLE_ANY_RP.fullmatch(line) is not None):
                        index +=1
                        continue
                    
                    break
    
    return index

class TextTable:
    """
    Represents a table inside of a docstring.
    
    Attributes
    ----------
    _array : `list` of (`str`, `None`)
        The elements of the table.
    _size : `tuple` (`int`, `int`)
        The dimensions of the table.
    """
    __slots__ = ('_array', '_size', )
    def __new__(cls, lines, start, end):
        """
        Creates a new table from the given lines's start:end range.
        
        Parameters
        ----------
        lines : `list` of `str`
            Line to create the table from.
        start : `int`
            The first line's index, where the table starts.
        end : `int`
            The 1 after the last line's index of the table.
        
        Returns
        -------
        self : `None` or ``TextTable``
            Returns `None` if would create an empty table.
        """
        splitted_lines = []
        # Split the lines. If a line is a border line, then add `None` to it, else a list of parts.
        while True:
            if start == end:
                break
            
            line = lines[start]
            start +=1
            
            if (TABLE_BORDER_RP.fullmatch(line) is not None):
                splitted_lines.append(None)
                continue
            
            splitted_line = TABLE_TEXT_SPLITTER.findall(line)
            # GOTO
            while True:
                if not splitted_line:
                    # Leave immediately if empty
                    break
                
                if not splitted_line[-1]:
                    # Remove last element, if empty.
                    del splitted_line[-1]
                
                if not splitted_line:
                    break
                
                if not splitted_line[0]:
                    # Remove first element if empty
                    del splitted_line[0]
                    
                if not splitted_line:
                    break
                
                # Replace empty elements with None and also strip the lines down as well.
                for index in range(len(splitted_line)):
                    splitted_part = splitted_line[index]
                    splitted_part = splitted_part.lstrip().rstrip(RIGHT_STRIP_IGNORE)
                    if not splitted_part:
                        splitted_part = None
                    
                    splitted_line[index] = splitted_part
                
                break
            
            splitted_lines.append(splitted_line)
        
        # Lets calculate how long is the longest line.
        longest = 0
        for splitted_part in splitted_lines:
            if splitted_part is None:
                continue
            
            actual_length = len(splitted_part)
            if actual_length > longest:
                longest = actual_length
                continue
        
        # If the longest is 0, we can leave
        if (not longest):
            return None
        
        # Fill up every line what is shorter than the longest with None
        for splitted_line in splitted_lines:
            if splitted_line is None:
                continue
            
            for _ in range(len(splitted_line), longest):
                splitted_line.append(None)
        
        processed_lines = []
        
        index = 0
        limit = len(splitted_lines)
        
        processed_line = [None for _ in range(longest)]
        
        while True:
            if index == limit:
                only_none = True
                for part_index in range(longest):
                    processed_part = processed_line[part_index]
                    if processed_part is None:
                        continue
                    
                    only_none = False
                    if type(processed_part) is list:
                        processed_part = ' '.join(processed_part)
                    
                    processed_line[part_index] = processed_part
                
                if only_none:
                    break
                
                processed_lines.append(processed_line)
                break
            
            splitted_line = splitted_lines[index]
            index +=1
            
            if splitted_line is None:
                # If we are at a border line, join the continuous lines together.
                # If every continuous line is empty, do not add them.
                only_none = True
                for part_index in range(longest):
                    processed_part = processed_line[part_index]
                    if processed_part is None:
                        continue
                    
                    only_none = False
                    if type(processed_part) is list:
                        processed_part = ' '.join(processed_part)
                    
                    processed_line[part_index] = processed_part
                
                if only_none:
                    continue
                
                processed_lines.append(processed_line)
                processed_line = [None for _ in range(longest)]
                continue
            
            # Add the current line to the actual processed line.
            for part_index in range(longest):
                splitted_part = splitted_line[part_index]
                if splitted_part is None:
                    continue
                
                processed_part = processed_line[part_index]
                if processed_part is None:
                    processed_line[part_index] = splitted_part
                elif type(processed_part) is list:
                    processed_part.append(splitted_part)
                else:
                    processed_line[part_index] = [processed_part, splitted_part]
        
        # Remove empty lines
        for index in reversed(range(len(processed_lines))):
            processed_line = processed_lines[index]
            if processed_line is None:
                continue
            
            for part in processed_line:
                if part:
                    break
            else:
                del processed_lines[index]
        
        # Remove None-s from end
        while True:
            if not processed_lines:
                return None
            
            if processed_lines[-1] is None:
                del processed_lines[-1]
                continue
            
            break
        
        # Remove None-s from start
        while True:
            if not processed_lines:
                return None
            
            if processed_lines[0] is None:
                del processed_lines[0]
                continue
            
            break
        
        # Remove Dupe None-s
        last_is_none = True
        for index in reversed(range(len(processed_lines))):
            processed_line = processed_lines[index]
            if processed_line is None:
                if last_is_none:
                    del processed_lines[index]
                else:
                    last_is_none = True
            else:
                last_is_none = False
        
        # Create size
        size = (longest, len(processed_lines))
        # Create array
        array = []
        for processed_line in processed_lines:
            array.extend(processed_line)
        
        self = object.__new__(cls)
        self._array = array
        self._size = size
        
        return self
    
    @property
    def size(self):
        """
        Returns the size of the table.
        
        Returns
        -------
        size : `tuple` (`int`, `int`)
            The x - y size of the table.
        """
        return self._size
    
    def __iter__(self):
        """
        Iterates over the table's lines.
        
        This method is a generator.
        
        Yields
        ------
        line : `list` of (`str`, `None`)
        """
        x, y = self._size
        array = self._array
        index = 0
        for _ in range(y):
            line = []
            for _ in range(x):
                element = array[index]
                index += 1
                
                line.append(element)
            
            yield line
    
    def __repr__(self):
        """Returns the table's representation."""
        result = [
            '<',
            self.__class__.__name__,
            ', size=',
            repr(self._size),
            ', table=[',
                ]
        
        for line in self:
            result.append(repr(line))
            result.append(', ')
    
        del result[-1]
        
        result.append(']>')
        return ''.join(result)
    
    def graved(self, path):
        """
        Returns a graved version of the table.
        
        Parameters
        ----------
        path : ``QualPath``
            The path of the parent docstring.
        
        Returns
        -------
        graved : ``GravedTable``
        """
        return GravedTable(self, path)

def detect_description(lines, index, limit):
    """
    Detects a description section.
    
    Parameters
    ----------
    lines : `list` of `str`
        The lines of the section.
    index : `int`
        The starting index of the description.
    limit : `int`
        The last element's index.
    
    Returns
    -------
    index : `int`
        The index where the description is over. If there was no description, returns the initial index.
    """
    while True:
        if index == limit:
            return index
        
        line = lines[index]
        
        if not line:
            return index
        
        if line[0] in (' ', '\t', '-'):
            return index
        
        if (TABLE_ANY_RP.fullmatch(line) is not None):
            return index
        
        index +=1
        continue


class TextDescription:
    """
    Represents a text part of a docstring.
    
    Attributes
    ----------
    _content : `str`
        The content of the description.
    """
    __slots__ = ('_content', )
    def __new__(cls, lines, start, end):
        """
        Creates a new description from the given lines's start:end range.
        
        Parameters
        ----------
        lines : `list` of `str`
            Lines to create the description from.
        start : `int`
            The first line's index, where the description starts.
        end : `int`
            The 1 after the last line's index of the description.
        """
        content = ' '.join(lines[start:end])
        
        self = object.__new__(cls)
        self._content = content
        return self
    
    def __repr__(self):
        """Returns the description's representation."""
        return f'<{self.__class__.__name__} content={self._content!r}>'
    
    def graved(self, path):
        """
        Returns a graved version of the description.
        
        Parameters
        ----------
        path : ``QualPath``
            The path of the parent docstring.
        
        Returns
        -------
        graved : ``GravedDescription``
        """
        return GravedDescription(self, path)

def detect_indent(lines, index, limit):
    """
    Detects an indented part.
    
    Parameters
    ----------
    lines : `list` of `str`
        The lines of the section.
    index : `int`
        The starting index of the indent.
    limit : `int`
        The last element's index.
    
    Returns
    -------
    index : `int`
        The index where the indent is over. If there was no indent, returns the initial index.
    """
    source_index = index
    found_indented = False
    while True:
        if index == limit:
            break
        
        line = lines[index]
        if not line:
            index +=1
            continue
        
        if line[0] in (' ', '\t'):
            found_indented = True
            index +=1
            continue
        
        break
    
    if found_indented:
        return index
    
    return source_index


def build_indent(lines, start, end):
    """
    Builds a section out from an indented part.
    
    Parameters
    ----------
    lines : `list` of `str`
        Lines to create the section from.
    start : `int`
        The first line's index, where the section starts.
    end : `int`
        The 1 after the last line's index of the section.
    
    Returns
    -------
    section : `None` or `list` of `Any`
        Instead of returning an empty section, returns `None`.
    """
    lines = lines[start:end]
    lines = remove_indents(lines)
    if lines is None:
        return None
    
    return parse_section(lines)


def detect_code_block(lines, index, limit):
    """
    Detects a code block and returns it's last line +1's index, or the source index if not found.
    
    Parameters
    ----------
    lines : `list` of `str`
        The lines of the section.
    index : `int`
        The starting index of the code block.
    limit : `int`
        The last element's index.
    
    Returns
    -------
    index : `int`
        The index where the code block is over. If there was no code block, returns the initial index.
    """
    source_index = index
    found_starter = False
    while True:
        if index == limit:
            if found_starter:
                return index
            else:
                return source_index
        
        line = lines[index]
        if not line:
            index += 1
            continue
        
        if line.endswith('```') if found_starter else line.startswith('```'):
            index += 1
            
            if found_starter:
                return index
            
            found_starter = True
            continue
        
        if found_starter:
            index += 1
            continue
        
        return source_index

class TextCodeBlock:
    """
    Represents a code-block part in a docstring.
    
    Attributes
    ----------
    _language : `None` or `str`
        The code block's language's name if any. Always lower case.
    _lines : `list` of `str`
        The internal lines of the code block.
    """
    __slots__ = ('_language', '_lines',)
    def __new__(cls, lines, start, end):
        """
        Creates a new code block from the given lines's start:end range.
        
        Parameters
        ----------
        lines : `list` of `str`
            Lines to create the code block from.
        start : `int`
            The first line's index, where the code block starts.
        end : `int`
            The 1 after the last line's index of the code block.

        
        Returns
        -------
        self : `None` or ``TextCodeBlock``
            Returns `None` if would create an empty code block.
        """
        line = lines[start]
        if len(line) == 3:
            language = None
            first_line = None
        else:
            first_line = line[3:]
            break_index = first_line.find(' ')
            if break_index == -1:
                language = first_line
                first_line = None
            else:
                language = first_line[:break_index]
                if language:
                    language = language.lower()
                else:
                    language = None
                
                first_line = first_line[break_index:].lstrip()
                if not first_line:
                    first_line = None
        
        if first_line is None:
            start += 1
        
        line = lines[end-1]
        if len(line) == 3:
            last_line = None
        else:
            last_line = line[:-3]
            last_line = last_line.rstrip(RIGHT_STRIP_IGNORE)
            if not last_line:
                last_line = None
        
        if last_line is None:
            end -= 1
        
        if start >= end:
            return None
        
        lines = lines[start:end]
        if (first_line is not None):
            lines[0] = first_line
        
        if (last_line is not None):
            lines[-1] = last_line
        
        # Remove empty lines from the end
        while True:
            if not lines:
                return None
            
            if lines[-1]:
                break
            
            del lines[-1]
            continue
        
        # Remove empty lines from the start.
        while True:
            if not lines:
                return None
            
            if lines[0]:
                break
            
            del lines[0]
            continue
        
        self = object.__new__(cls)
        self._lines = lines
        self._language = language
        return self
    
    def __repr__(self):
        """Returns the code blocks's representation."""
        result = ['<', self.__class__.__name__]
        
        language = self._language
        if language is None:
            result.append(' language=')
            result.append(repr(language))
            
            add_comma = True
        else:
            add_comma = False
        
        if add_comma:
            result.append(', ')
        
        result.append(' lines=')
        result.append(repr(self._lines))
        
        result.append('>')
        
        return ''.join(result)
    
    def graved(self, path):
        """
        Returns a graved version of the code block.
        
        Parameters
        ----------
        path : ``QualPath``
            The path of the parent docstring.
        
        Returns
        -------
        graved : ``GravedCodeBlock``
        """
        return GravedCodeBlock(self, path)

def detect_void(lines, index, limit):
    """
    Detects empty lines.
    
    Parameters
    ----------
    lines : `list` of `str`
        The lines of the section.
    index : `int`
        The starting index of the void..
    limit : `int`
        The last element's index.
    
    Returns
    -------
    index : `int`
        The index where the void is over. If there was no void, returns the initial index.
    """
    while True:
        if index == limit:
            return index
        
        line = lines[index]
        if line:
            return index
        
        index +=1
        continue


def build_void(lines, start, end):
    """
    Builds a void from the given parameters.
    
    Parameters
    ----------
    lines : `list` of `str`
        The lines of the section.
    start : `int`
        The starting index of the void.
    end : `int`
        The void's last line's index +1.
    
    Returns
    -------
    void : `None`
    """
    return None


def parse_section(lines):
    """
    Parses the given section and returns the built objects.
    
    Parameters
    ----------
    lines : `list` of `str`
        Lines to build the section from.
    
    Returns
    -------
    built : `None` or `list` of `Any`
        The built up elements of the sections. If would return an empty list, returns `None` instead.
    """
    index = 0
    limit = len(lines)
    
    builts = []
    
    while True:
        if index == limit:
            break
        
        for detector, builder in (
                (detect_void, build_void),
                (detect_indent, build_indent),
                (detect_table, TextTable),
                (detect_listing, TextListing),
                (detect_code_block, TextCodeBlock),
                (detect_block_quote, TextBlockQuote),
                (detect_description, TextDescription),
                    ):
            
            detected_end = detector(lines, index, limit)
            if detected_end == index:
                continue
            
            built = builder(lines, index, detected_end)
            index = detected_end
            if built is None:
                break
            
            builts.append(built)
            break
        else:
            sys.stderr.write(f'Could not detect anything, skipping. Line :{lines[index]}\n')
            index += 1
            continue
    
    if (not builts):
        return None
    
    # If a description is indented alone by 2 behind an other one, connect them.
    index = 0
    limit = len(builts)-1
    while True:
        if index >= limit:
            break
        
        built = builts[index]
        index +=1
        
        if type(built) is not TextDescription:
            continue
        
        next_built = builts[index]
        if type(next_built) is not list:
            continue
        
        next_built_internal = next_built[0]
        if type(next_built_internal) is not list:
            continue
        
        if len(next_built_internal) != 1:
            continue
        
        maybe_description = next_built_internal[0]
        if type(maybe_description) is not TextDescription:
            continue
        
        built._content = f'{built._content} {maybe_description._content}'
        del next_built[0]
        index +=1
        limit -=1
        continue
    
    return builts


def detect_listing(lines, index, limit):
    """
    Detects the lines of a listing.
    
    Parameters
    ----------
    lines : `list` of `str`
        The lines of the section.
    index : `int`
        The starting index of the listing.
    limit : `int`
        The last element's index.
    
    Returns
    -------
    index : `int`
        The index where the listing is over. If there was no listing, returns the initial index.
    """
    get_back_index = index
    dash_count = 0
    while True:
        if index == limit:
            return index
        
        line = lines[index]
        
        if line.startswith('-'):
            dash_count += 1
            index += 1
            continue
        
        if dash_count == 0:
            # No dash is detected
            return get_back_index
        
        if not line:
            index += 1
            continue
        
        if line[0] in (' ', '\t'):
            index += 1
            continue
        
        if dash_count == 1:
            return get_back_index
        
        break
    
    return index


class TextListingElement:
    """
    Represents an element of a listing.
    
    Attributes
    ----------
    _content : `None`, `list` of `Any`
        The content stored inside of a listing element. If would be set as empty `list`, is set as `None` instead.
    _head : `None` or `str`
        The head content of the listing. If would be set as empty string, is set as `None` instead.
    """
    __slots__ = ('_content', '_head')
    def __new__(cls, lines):
        """
        Creates a new listing element from the given lines.
        
        Parameters
        ----------
        lines : `list` of `str`
            The lines to create the element from.
        
        Returns
        -------
        self : `None` or ``TextListingElement``
            Instead of returning an empty listing element, returns `None` instead.
        """
        head_line = lines.pop(0)
        
        parsed = LISTING_HEAD_LINE_RP.fullmatch(head_line)
        if parsed is None:
            head = None
        else:
            head = parsed.group(1)
            if not head:
                head = None
        
        # GOTO
        content = None
        while True:
            if not lines:
                break
            
            continue_head = bool(lines[0])
            
            lines = remove_indents(lines)
            if lines is None:
                break
            
            section = parse_section(lines)
            if section is None:
                continue
            
            if not continue_head:
                content = section
                break
            
            maybe_description = section[0]
            if type(maybe_description) is not TextDescription:
                content = section
                break
            
            del section[0]
            
            extra_head_content = maybe_description._content
            if head is None:
                head = extra_head_content
            else:
                head = f'{head} {extra_head_content}'
            
            if not section:
                break
            
            content = section
            break
        
        if None is head is content:
            self = None
        else:
            self = object.__new__(cls)
            self._head = head
            self._content = content
        
        return self
    
    def __repr__(self):
        """Returns the listing element's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__
        ]
        
        head = self._head
        if head is None:
            add_comma = False
        else:
            repr_parts.append(' head=')
            repr_parts.append(repr(head))
            add_comma = True
        
        content = self._content
        if (content is not None):
            if add_comma:
                repr_parts.append(',')
            
            repr_parts.append(' content=')
            repr_parts.append(repr(content))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    def graved(self, path):
        """
        Returns a graved version of the listing element.
        
        Parameters
        ----------
        path : ``QualPath``
            The path of the parent docstring.
        
        Returns
        -------
        graved : ``GravedListingElement``
        """
        return GravedListingElement(self, path)


class TextListing:
    """
    Represents a listing inside of a docstring.
    
    Attributes
    ----------
    _elements : `list` of ``TextListingElement``
        The elements of the listing.
    """
    __slots__ = ('_elements')
    def __new__(cls, lines, start, end):
        """
        Creates a new listing instance.
        
        Parameters
        ----------
        lines : `list` of `str`
            Lines to build the listing from.
        start : `int`
            The first lines index of the listing.
        end : `int`
            The last lines +1 index.
        
        Returns
        -------
        self : `None` or ``TextListing``
            If would create an empty listing, returns `None` instead.
        """
        sections = []
        
        # Separate each part
        section_parts = []
        while True:
            if start == end:
                if section_parts:
                    sections.append(section_parts)
                break
            
            line = lines[start]
            start += 1
            
            if line.startswith('-'):
                # If the line starts with `-`, then save the currently created part if any.
                if section_parts:
                    sections.append(section_parts)
                    section_parts = []
            
            section_parts.append(line)
            continue
        
        # Remove empty lines from the end and remove empty sections if any.
        index = len(sections)
        
        while True:
            if index == 0:
                break
            
            index -= 1
            section_parts = sections[index]
            
            while True:
                if not section_parts:
                    del sections[index]
                    break
                
                if not section_parts[-1]:
                    del section_parts[-1]
                    continue
                
                break
        
        # Nice, now lets make the elements.
        elements = []
        for section_parts in sections:
            element = TextListingElement(section_parts)
            if element is None:
                continue
            
            elements.append(element)
            continue
        
        if not elements:
            return None
        
        self = object.__new__(cls)
        self._elements = elements
        return self
    
    def __repr__(self):
        """Returns the listing's representation."""
        return f'<{self.__class__.__name__} elements={self._elements!r}>'
    
    def graved(self, path):
        """
        Returns a graved version of the listing.
        
        Parameters
        ----------
        path : ``QualPath``
            The path of the parent docstring.
        
        Returns
        -------
        graved : ``GravedListing``
        """
        return GravedListing(self, path)


def detect_block_quote(lines, index, limit):
    """
    Detects the lines of a block quote.
    
    Parameters
    ----------
    lines : `list` of `str`
        The lines of the section.
    index : `int`
        The starting index of the block quote.
    limit : `int`
        The last element's index.
    
    Returns
    -------
    index : `int`
        The index where the block quote is over. If there was no block quote, returns the initial index.
    """
    while True:
        if index == limit:
            return index
        
        line = lines[index]
        if not line:
            return index
        
        if line[0] not in '>':
            return index
        
        index += 1
        continue

def remove_block_quote_indents(lines):
    """
    Removes the dedent from the given lines returning a new list with the lines without them.
    
    Parameters
    ----------
    lines : `list` of `str`
        Input lines.
    
    Returns
    -------
    lines : `None` or (`list` of `str`)
    """
    if not lines:
        return None
    
    for index in range(len(lines)):
        lines[index] = lines[index][1:].lstrip()
    
    while True:
        if lines[-1]:
            break
        
        del lines[-1]
        if not lines:
            return None
    
    while True:
        if lines[0]:
            break
        
        del lines[0]
        continue
    
    return lines


class TextBlockQuote:
    """
    Represents a block quote of a docstring.
    
    Attributes
    ----------
    _descriptions : `list` of  ``TextDescription``
        The description parts inside of the block quote.
    """
    __slots__ = ('_descriptions', )
    def __new__(cls, lines, start, end):
        """
        Creates a new block quote from the given lines's start:end range.
        
        Parameters
        ----------
        lines : `list` of `str`
            Lines to create the block quote from.
        start : `int`
            The first line's index, where the block quote starts.
        end : `int`
            The 1 after the last line's index of the block quote..
        """
        lines = lines[start:end]
        lines = remove_block_quote_indents(lines)
        if lines is None:
            return None
        
        index = 0
        limit = len(lines)
        
        builts = []
        
        while True:
            if index == limit:
                break
        
        
            for detector, builder in (
                    (detect_void, build_void),
                    (detect_description, TextDescription),
                        ):
                
                detected_end = detector(lines, index, limit)
                if detected_end == index:
                    continue
                
                built = builder(lines, index, detected_end)
                index = detected_end
                if built is None:
                    break
                
                builts.append(built)
                break
            else:
                sys.stderr.write(f'Could not detect anything, skipping. Line :{lines[index]}\n')
                index += 1
                continue
        
        if not builts:
            return None
        
        self = object.__new__(cls)
        self._descriptions = builts
        return self
    
    def __repr__(self):
        """Returns the description's representation."""
        return f'<{self.__class__.__name__} descriptions={self._descriptions!r}>'
    
    def graved(self, path):
        """
        Returns a graved version of the block quote.
        
        Parameters
        ----------
        path : ``QualPath``
            The path of the parent docstring.
        
        Returns
        -------
        graved : ``GravedBlockQuote``
        """
        return GravedBlockQuote(self, path)


def parse_docstring(text, path):
    """
    Parses the given docstring.
    
    Parameters
    ---------
    text : `None` or `str`
        The docstring itself.
    path : ``QUalPath``
        The path of the docstring's object.
    
    Returns
    -------
    built_sections : `None` or `list` of (`tuple` ((`None` or `str`), `Any`))
    """
    if text is None:
        return None
    
    lines = text.splitlines()
    
    remove_indents(lines)
    if lines is None:
        DocWarning(path, 'Empty docstring not defined as `None`.')
        return None
    
    if lines[0][0] in (' ', '\t'):
        DocWarning(path, 'Docstring starts with space or tab character. Might contain `\\n` or mixed indents.')
        return None
    
    sections = parse_sections(lines)
    if (sections[0][0] is not None):
        DocWarning(path, 'No general description provided.')
    
    built_sections = []
    
    for section_name, section_lines in sections:
        built = parse_section(section_lines)
        if built is None:
            DocWarning(path, f'Empty subsection part: {section_name}')
            continue
        
        built_sections.append((section_name, built))
    
    if (not built_sections):
        return None
    
    result = []
    
    for section_name, sub_section in built_sections:
        sub_section = build_graves_on_subsection(sub_section, path)
        if sub_section is None:
            DocWarning(path, f'Empty subsection part: {section_name}')
            continue
        
        result.append((section_name, sub_section))
    
    if not result:
        return None
    
    return result


def convert_extra_attribute_section_name(name):
    return '___'+name.lower().replace(' ', '_')

def get_attribute_docs_from(sections):
    """
    Gets the attribute doc parts from the given sections.
    
    Parameters
    ----------
    sections : `list` of `tuple` ((`None` or `str`), (`list` of `Any`))
        The sections of the docstring.
    
    Returns
    -------
    result : `dict` of (`str`, ``DocString``) items
    """
    result = {}
    
    for name, section in sections:
        if name is None:
            continue
        
        if ATTRIBUTE_SECTION_NAME_RP.fullmatch(name) is None:
            continue
        
        index = 0
        limit = len(section)
        while True:
            if index == limit:
                break
            
            part = section[index]
            if (type(part) is not GravedDescription):
                break
            
            starter = part.content[0]
            if (type(starter) is not str):
                break
            
            parsed = ATTRIBUTE_NAME_RP.match(starter)
            if parsed is None:
                break
            
            attr_name, attr_separator = parsed.groups()
            attr_head = part.content.copy()
            starter_continuous = starter[parsed.end():]
            if starter_continuous:
                attr_head[0] = starter_continuous
            else:
                if len(attr_head) == 1:
                    attr_head = []
                else:
                    del attr_head[0]
            
            index += 1
            if index == limit:
                attr_body = None
            else:
                part = section[index]
                if type(part) is list:
                    attr_body = part
                    index += 1
                else:
                    attr_body = None
            
            result[attr_name] = DocString._create_attribute_docstring_part(attr_name, attr_separator, attr_head, attr_body)
            continue
        
        extra = []
        while True:
            if index == limit:
                break
            
            part = section[index]
            index += 1
            extra.append(part)
            continue
        
        if extra:
            name = convert_extra_attribute_section_name(name)
            result[name] = DocString._create_attribute_docstring_extra(extra)
    
    return result

class DocString:
    """
    Represents a docstring.
    
    Attributes
    ----------
    _attribute_sections : `None` or `dict` of (`str`, ``DocString``) items
        A dict containing the attribute sections of the docstring. Set only when an attribute's docstring is requested.
    sections : `list` of `tuple` ((`None` or `str`), (`list` of `Any`))
        The sections of the docstring.
    """
    __slots__ = ('_attribute_sections', 'sections')
    def __new__(cls, docstring, path):
        """
        Creates a new docstring.
        
        docstring : `None` or ``Docstring``
        """
        if docstring is None:
            return None
        
        sections = parse_docstring(docstring, path)
        if sections is None:
            return None
        
        self = object.__new__(cls)
        self._attribute_sections = None
        self.sections = sections
        return self
    
    def __repr__(self):
        """Returns the docstring's representation."""
        return f'<{self.__class__.__name__} sections={self.sections!r}>'
    
    @classmethod
    def _create_attribute_docstring_part(cls, attr_name, attr_separator, attr_head, attr_body):
        """
        Creates an attribute docstring.
        
        Parameters
        ----------
        attr_name : `str`
            The name of the respective attribute.
        attr_separator : `str`
            Separator used between the attribute's name and it's type description.
        attr_head : `None` or `str`
            The attribute description following the attribute's name.
        attr_body : `None` or `list` of `Any`
            Extra content after the attribute's head.
        
        Returns
        -------
        self : ``DocString``
        """
        head = GravedAttributeDescription(attr_name, attr_separator, attr_head)
        
        section = [head]
        
        if (attr_body is not None):
            section.extend(attr_body)
        
        self = object.__new__(cls)
        self._attribute_sections = None
        self.sections = [(None, section)]
        return self
    
    @classmethod
    def _create_attribute_docstring_extra(cls, attr_body):
        """
        Creates an attribute docstring.
        
        Parameters
        ----------
        attr_body : `None` or `list` of `Any`
            The extra content.
        
        Returns
        -------
        self : ``DocString``
        """
        self = object.__new__(cls)
        self._attribute_sections = None
        self.sections = [(None, attr_body)]
        return self
    
    def attribute_docstring_for(self, name):
        """
        Gets the docstring for the given attribute.
        
        Parameters
        ----------
        name : `str`
            The name of the attribute.
        
        Returns
        -------
        docstring : `None` or ``Docstring``
        """
        attribute_sections = self._attribute_sections
        if attribute_sections is None:
            self._attribute_sections = attribute_sections = get_attribute_docs_from(self.sections)
        
        return attribute_sections.get(name, None)
    
    def extra_attribute_docstring_for(self, name):
        """
        Gets the extra docstring for the given attribute section name.
        
        Parameters
        ----------
        name : `str`
            The name of the attribute section.
        
        Returns
        -------
        docstring : `None` or ``Docstring``
        """
        attribute_sections = self._attribute_sections
        if attribute_sections is None:
            self._attribute_sections = attribute_sections = get_attribute_docs_from(self.sections)
        
        name = convert_extra_attribute_section_name(name)
        return attribute_sections.get(name, None)
