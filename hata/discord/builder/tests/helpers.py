from ..constants import CONVERSION_KIND_NONE
from ..conversion import Conversion


def _create_default_conversion(extra = None):
    """
    Parameters
    ----------
    extra : `dict<str, object>`
        Extra parameters to use when creating the conversion.
    
    Returns
    -------
    conversion : ``Conversion``
    """
    items = {
        'name_aliases': None,
        'expected_types_messages': '',
        'set_identifier': None,
        'serializer_key': None,
        'kind': CONVERSION_KIND_NONE,
        'set_merger': None,
        'name': 'flags',
        'output_conversion': None,
        'serializer_optional': None,
        'serializer_required': None,
        'set_validator': None,
        'get_default': None,
        'get_processor': None,
        'sort_priority': 0,
        'set_type': None,
        'set_type_processor': None,
        'set_listing_identifier': None,
    }
    
    if (extra is not None):
        items.update(extra)
    
    return Conversion(items)


class TestType():
    __slots__ = ('fields',)
    
    def __new__(cls, fields):
        self = object.__new__(cls)
        self.fields = fields
        return self
    
    
    def __getattr__(self, name):
        try:
            return self.fields[name]
        except KeyError as exception:
            raise AttributeError from exception
