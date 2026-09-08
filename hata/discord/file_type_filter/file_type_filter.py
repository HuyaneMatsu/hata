__all__ = (
    'FileTypeFilter', 'file_type_filter_convert_to_data', 'file_type_filter_create',
    'file_type_filter_create_from_data'
)

from scarletio import RichAttributeErrorBaseType

from .fields import validate_groups, validate_individuals
from .preinstanced import FileTypeFilterGroup


class FileTypeFilter(RichAttributeErrorBaseType):
    """
    File type filter used in application command parameters and in components.
    
    Attributes
    ----------
    groups : ``None | tuple<FileTypeFilterGroup>``
        File type groups.
    
    individuals : `None | tuple<str>`
        File types individually by their extensions.
    """
    __slots__ = ('groups', 'individuals')
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # groups
        groups = self.groups
        if (groups is None):
            field_added = False
        
        else:
            field_added = True
            
            repr_parts.append(' groups = ')
            repr_parts.append(repr(groups))
        
        # individuals
        individuals = self.individuals
        if (individuals is not None):
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' individuals = ')
            repr_parts.append(repr(individuals))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # groups
        groups = self.groups
        if (groups is not None):
            hash_value ^= hash(groups)
        
        # individuals
        individuals = self.individuals
        if (individuals is not None):
            hash_value ^= hash(individuals)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # groups
        if self.groups != other.groups:
            return False
        
        # individuals
        if self.individuals != other.individuals:
            return False
        
        return True


def file_type_filter_create(*, groups = ..., individuals = ...):
    """
    Creates a file type filter.
    
    Parameters
    ----------
    groups : ``None | iterable<str> | iterable<FileTypeFilterGroup>``
        File type groups.
    
    individuals : `None | iterable<str>`
        File types individually by their extensions.
    
    Returns
    -------
    file_type_filter : ``FileTypeFilter``
    """
    # individuals
    if individuals is ...:
        individuals = None
    else:
        individuals = validate_individuals(individuals)
    
    # groups
    if groups is ...:
        groups = None
    else:
        groups = validate_groups(groups)
    
    file_type_filter = object.__new__(FileTypeFilter)
    file_type_filter.groups = groups
    file_type_filter.individuals = individuals
    return file_type_filter


def file_type_filter_create_from_data(data):
    """
    Creates file type filter from the given data.
    
    Parameters
    ----------
    data : `list<str>`
        Data to deserialise.
    
    Returns
    -------
    file_type_filter : ``FileTypeFilter``
    """
    individuals = None
    groups = None
    
    for element in data:
        if element.startswith('.'):
            element = element[1:]
            
            if individuals is None:
                individuals = []
            
            if (element not in individuals):
                individuals.append(element)
        
        else:
            if groups is None:
                groups = []
            
            group = FileTypeFilterGroup(element)
            if (group not in groups):
                groups.append(group)
    
    if (individuals is not None):
        individuals.sort()
        individuals = tuple(individuals)
    
    if (groups is not None):
        groups.sort()
        groups = tuple(groups)
    
    file_type_filter = object.__new__(FileTypeFilter)
    file_type_filter.individuals = individuals
    file_type_filter.groups = groups
    return file_type_filter


def file_type_filter_convert_to_data(file_type_filter):
    """
    Serialises the file type filter.
    
    Parameters
    ----------
    file_type : ``FileTypeFilter``
        File type filter to serialise.
    
    Returns
    -------
    data : `list<str>`
    """
    data = []
    
    individuals = file_type_filter.individuals
    if (individuals is not None):
        for individual in individuals:
            data.append('.' + individual)
    
    groups = file_type_filter.groups
    if (groups is not None):
        for group in groups:
            data.append(group.value)
    
    return data
