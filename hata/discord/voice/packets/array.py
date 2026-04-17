__all__ = ()

from scarletio import RichAttributeErrorBaseType


class ArrayUInt32BE(RichAttributeErrorBaseType):
    """
    Implements an uint32 array casted on bytes.
    Using `big endian` byte order.
    
    Attributes
    ----------
    _data : `bytes`
        The source `bytes` object.
    
    _start : `int`
        The first byte what is inside of the array.
    
    _end : `int`
        The first byte, what is not inside of the array after `._start`.
    """
    __slots__ = ('_data', '_end', '_start')
    
    def __new__(cls, data, start, end):
        """
        Creates a new uint32 array from the given parameters.
        
        Parameters
        ----------
        data : `bytes`
            The source `bytes` object.
        start : `int`
            The first byte what is inside of the array.
        end : `int`
            The first byte, what is not inside of the array after `._start`.
        """
        self = object.__new__(cls)
        self._data = data
        self._end = end
        self._start = start
        return self
    
    
    def __len__(self):
        """Returns the array's length"""
        return (self._end - self._start) >> 2
    
    
    def __getitem__(self, index):
        """Returns the element of the array at the given index."""
        location = self._start + (index << 2)
        return int.from_bytes(self._data[location : location + 4], 'big')
    
    
    def __repr__(self):
        """Returns the array's representation."""
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append(' length = ')
        repr_parts.append(repr(len(self)))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two arrays are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return memoryview(self._data)[self._start : self._end] == memoryview(other._data)[other._start : other._end]
    
    
    def __iter__(self):
        """Iterated over the array's elements."""
        data = self._data
        location = self._start
        end = self._end
        
        while True:
            if location >= end:
                break
            
            value = int.from_bytes(data[location : location + 4], 'big')
            yield value
            
            location += 4
            continue
