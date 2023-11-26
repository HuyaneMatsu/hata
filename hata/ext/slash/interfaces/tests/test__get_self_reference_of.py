import vampytest
from scarletio import WeakReferer

from ..self_reference import SelfReferenceInterface, get_self_reference_of


class TestSelfReferenceInterface(SelfReferenceInterface):
    __slots__ = ('__weakref__',)


def _iter_options():
    yield None, None
    yield object(), None
    
    interface = SelfReferenceInterface()
    yield interface, None
    
    interface = TestSelfReferenceInterface()
    yield interface, WeakReferer(interface)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_self_reference_of(input_value):
    """
    Tests whether ``get_self_reference_of`` works as intended.
    
    Parameters
    ----------
    input_value : `None | object | SelfReferenceInterface`
        Value to try to get self reference of.
    
    Returns
    -------
    output : `None | WeakReferer`
    """
    output = get_self_reference_of(input_value)
    vampytest.assert_instance(output, WeakReferer, nullable = True)
    return output
