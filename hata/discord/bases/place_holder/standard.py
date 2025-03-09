__all__ = ('PlaceHolder',)

from scarletio import copy_docs

from .base import PlaceHolderBase


class PlaceHolder(PlaceHolderBase):
    __type_doc__ = (
    """
    Slot place holder returning a default value.
    
    Might be used to avoid `__getattr__` definitions.
    
    Attributes
    ----------
    attribute_name : `None | str`
        The name of the place held attribute.
    
    default_value : `object`
        The object to return from getter.
    
    docs : `None | str`
        Documentation of the place held attribute.
    
    type_name : `None | str`
        The name of the type the we place held at.
    """)
    
    __slots__ = ('default_value',)
    
    
    def __new__(cls, default_value, docs = None):
        """
        Creates a new new slot place holder.
        
        Parameters
        ----------
        default_value : `object`
            The object to return from getter.
        
        docs : `None`, `str` = `None`, Optional
            Documentation of the place held attribute.
        """
        self = PlaceHolderBase.__new__(cls, docs)
        self.default_value = default_value
        return self
    
    
    @copy_docs(PlaceHolderBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not PlaceHolderBase._is_equal_same_type(self, other):
            return False
        
        # default
        if self.default_value != other.default_value:
            return False
        
        return True
    
    
    @copy_docs(PlaceHolderBase._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts, field_added):
        # default_value
        
        if field_added:
            repr_parts.append(',')
        else:
            field_added = True
        
        repr_parts.append(' default_value = ')
        repr_parts.append(repr(self.default_value))
        
        return field_added
    
    
    @copy_docs(PlaceHolderBase.__hash__)
    def __hash__(self):
        hash_value = PlaceHolderBase.__hash__(self)
        
        # default_value
        default_value = self.default_value
        try:
            default_value_hash = hash(default_value)
        except TypeError:
            default_value_hash = object.__hash__(default_value)
        hash_value ^= default_value_hash
        
        return hash_value
    
    
    @copy_docs(PlaceHolderBase.__get__)
    def __get__(self, instance, type_):
        if instance is None:
            return self
        
        return self.default_value
