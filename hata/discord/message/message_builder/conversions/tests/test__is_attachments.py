from collections import OrderedDict

import vampytest

from ....attachment import Attachment

from ..attachments import _is_attachments


class TestType():
    __slots__ = ('name')
    
    def __new__(cls, name):
        self = object.__new__(cls)
        self.name = name
        return self


def _iter_options():
    instance_0 = TestType('hey')
    instance_1 = TestType('there')
    
    # None
    yield None, [None]
    
    # tuple
    yield (), []
    yield ('mister', instance_0), [[(False, ('mister', instance_0, None))]]
    
    # Attachment
    yield Attachment.precreate(202402250001), [[(True, 202402250001)]]
    
    # list | Deque
    yield [], [None]
    yield (
        [
            instance_0,
            ('satori', instance_1),
            Attachment.precreate(202402250002),
        ],
        [[
            (False, ('hey', instance_0, None)),
            (False, ('satori', instance_1, None)),
            (True, 202402250002)
        ]]
    )
    
    # dict-like
    yield (
        OrderedDict([('hey', instance_0), ('mister', instance_1)]),
        [[
            (False, ('hey', instance_0, None)),
            (False, ('mister', instance_1, None)),
        ]]
    )
    
    # rest
    yield instance_0, [[(False, ('hey', instance_0, None))]]


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__is_attachments(input_value):
    """
    Tests whether ``_is_attachments`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test on.
    
    Returns
    -------
    output : `list<None | list<(bool<True>, int) | (bool<False>, (str, object, None | str))>>`
    """
    output = [*_is_attachments(input_value)]
    return output
