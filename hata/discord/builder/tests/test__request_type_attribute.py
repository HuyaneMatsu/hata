import vampytest

from ..builder_base import _request_type_attribute


class TestType():
    __slots__ = ('fields',)
    
    def __new__(cls, fields):
        self = object.__new__(cls)
        self.fields = fields
        return self
    
    
    def __getattr__(self, value):
        try:
            return self.fields[value]
        except KeyError as exception:
            raise AttributeError from exception


def _iter_options__passing():
    yield (), {'hey': 'mister'}, 'hey', 'mister'
    yield (TestType({'hey': 'mister'}),), {}, 'hey', 'mister'
    yield (object, TestType({'hey': 'mister'}), object,), {}, 'hey', 'mister'
    

def _iter_options__runtime_error():
    yield (), {}, 'hey'
    yield (object,), {}, 'hey'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__runtime_error()).raising(RuntimeError))
def test__request_type_attribute(base_types, type_attributes, attribute_name):
    """
    Tests whether ``_request_type_attribute`` works as intended.
    
    Parameters
    ----------
    base_types : `set<type>`
        Types to inherit from.
    type_attributes : `dict<str, object>`
            The type attributes of the type to be created.
    attribute_name : `str`
        The attribute's name.
    
    Returns
    -------
    output : `object`
    
    Raises
    ------
    RuntimeError
    """
    return _request_type_attribute('koishi', base_types, type_attributes, attribute_name)
