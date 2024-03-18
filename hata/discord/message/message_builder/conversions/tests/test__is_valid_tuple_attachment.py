import vampytest

from ..attachments import _is_valid_tuple_attachment


class TestType():
    __slots__ = ('name')
    
    def __new__(cls, name):
        self = object.__new__(cls)
        self.name = name
        return self


def _iter_options():
    instance_0 = TestType('mister')
    
    yield (instance_0,), [(False, ('mister', instance_0, None))]
    yield (None, instance_0,), [(False, ('mister', instance_0, None))]
    yield ('hey', instance_0,), [(False, ('hey', instance_0, None))]
    yield (None, instance_0, 'satori'), [(False, ('mister', instance_0, 'satori'))]
    yield ('hey', instance_0, 'satori'), [(False, ('hey', instance_0, 'satori'))]
    
    yield (), []
    yield (None, instance_0, None, None), []


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__is_valid_tuple_attachment(input_value):
    """
    Tests whether ``_is_valid_tuple_attachment`` works as intended.
    
    Parameters
    ----------
    input_value : `tuple`
        Value to test on.
    
    Returns
    -------
    output : list<(str, object, None | str)>
    """
    output = [*_is_valid_tuple_attachment(input_value)]
    
    for element in output:
        vampytest.assert_instance(element, tuple)
    
    return output
