__all__ = ('PlaceHolderFunctional',)

from scarletio import copy_docs

from .base import PlaceHolderBase


class PlaceHolderFunctional(PlaceHolderBase):
    __type_doc__ = (
    """
    Slot place holder returning a default value.
    
    Might be used to avoid `__getattr__` definitions.
    
    Attributes
    ----------
    attribute_name : `None | str`
        The name of the place held attribute.
    
    default_function : `callable`
        A function to create the default value.
       
    docs : `None | str`
        Documentation of the place held attribute.
    
    type_name : `None | str`
        The name of the type the we place held at.
    """)
    
    __slots__ = ('default_function',)
    
    
    def __new__(cls, default_function, docs = None):
        """
        Creates a new new slot place holder.
        
        Parameters
        ----------
        default_function : `callable`
            A function to create the default value.
        
        docs : `None`, `str` = `None`, Optional
            Documentation of the place held attribute.
        """
        self = PlaceHolderBase.__new__(cls, docs)
        self.default_function = default_function
        return self
    
    
    @copy_docs(PlaceHolderBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not PlaceHolderBase._is_equal_same_type(self, other):
            return False
        
        # default_function
        if self.default_function != other.default_function:
            return False
        
        return True
    
    
    @copy_docs(PlaceHolderBase._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts, field_added):
        # default_function
        if field_added:
            repr_parts.append(',')
        else:
            field_added = True
        
        repr_parts.append(' default_function = ')
        repr_parts.append(repr(self.default_function))
        
        return field_added
    
    
    @copy_docs(PlaceHolderBase.__hash__)
    def __hash__(self):
        hash_value = PlaceHolderBase.__hash__(self)
        
        # default_function
        default_function = self.default_function
        try:
            default_function_hash = hash(default_function)
        except TypeError:
            default_function_hash = object.__hash__(default_function)
        hash_value ^= default_function_hash
        
        return hash_value
    
    
    @copy_docs(PlaceHolderBase.__get__)
    def __get__(self, instance, type_):
        if instance is None:
            return self
        
        return self.default_function()
