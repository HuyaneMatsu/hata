__all__ = ()

from scarletio import copy_docs

from .builder_base import BuilderBase

from .conversions import CONVERSION_KEYWORD, CONVERSION_NONE, CONVERSION_POSITIONAL


class BuilderFielded(BuilderBase):
    """
    Builder using fields to store its values.
    
    Attributes
    ----------
    fields : `dict<Conversion, object>`
        Fields already added to the builder.
    """
    __conversions_default__ = [
        CONVERSION_NONE,
        CONVERSION_KEYWORD,
        CONVERSION_POSITIONAL,
    ]
    
    __slots__ = ('fields',)
    
    def __new__(cls):
        """
        Creates a new message builder.
        """
        self = object.__new__(cls)
        self.fields = {}
        return self
    
    
    @copy_docs(BuilderBase._store_field_value)
    def _store_field_value(self, conversion, value):
        self.fields[conversion] = value
    
    
    @copy_docs(BuilderBase._try_pull_field_value)
    def _try_pull_field_value(self, conversion):
        try:
            yield self.fields[conversion]
        except KeyError:
            pass
    
    
    @copy_docs(BuilderBase._with_positional_parameter_unknown)
    def _with_positional_parameter_unknown(self, value):
        raise TypeError(
            f'Could not recognise value as a field. Got {type(value).__name__}; {value!r}.'
        )
        return self._setter_field(CONVERSION_CONTENT, str(value))
    
    
    @copy_docs(BuilderBase._with_keyword_parameter_unknown)
    def _with_keyword_parameter_unknown(self, key, value):
        raise TypeError(
            f'{key!r} could not be recognised as a field. Got {type(value).__name__}; {value!r}.'
        )
    
    
    @copy_docs(BuilderBase._iter_conversions)
    def _iter_conversions(self):
        yield from self.fields.keys()
    
    
    @copy_docs(BuilderBase._iter_fields)
    def _iter_fields(self):
        yield from self.fields.items()
