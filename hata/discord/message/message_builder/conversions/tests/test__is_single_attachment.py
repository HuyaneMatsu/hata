import vampytest

from ....attachment import Attachment

from ..attachments import _is_single_attachment


class TestType():
    __slots__ = ('name')
    
    def __new__(cls, name):
        self = object.__new__(cls)
        self.name = name
        return self


def _iter_options():
    instance_0 = TestType('hey')
    
    yield (), []
    yield Attachment.precreate(202402250000), [(True, 202402250000)]
    yield ('mister', instance_0), [(False, ('mister', instance_0, None))]
    yield instance_0, [(False, ('hey', instance_0, None))]


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__is_single_attachment(input_value):
    """
    Tests whether ``_is_single_attachment`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test on.
    
    Returns
    -------
    output : `list<(bool<True>, int) | (bool<False>, (str, object, None | str))>`
    """
    output = [*_is_single_attachment(input_value)]

    for element in output:
        vampytest.assert_instance(element, tuple)
    
    return output
