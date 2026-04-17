import vampytest
from scarletio import WeakReferer

from ..self_reference import SelfReferenceInterface


class TestSelfReferenceInterface(SelfReferenceInterface):
    __slots__ = ('__weakref__', '_self_reference')
    
    def __new__(cls):
        self = object.__new__(cls)
        self._self_reference = None
        return self


def test__SelfReferenceInterface__get_self_reference():
    """
    Tests whether ``SelfReferenceInterface.get_self_reference`` works as intended.
    """
    interface = TestSelfReferenceInterface()
    
    output = interface.get_self_reference()
    vampytest.assert_instance(output, WeakReferer)
    vampytest.assert_is(output(), interface)
    vampytest.assert_is(output, interface._self_reference)
    
    test_output = interface.get_self_reference()
    vampytest.assert_is(test_output, output)
