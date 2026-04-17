import vampytest

from ..event import _validate_default_handler


async def func_0(a, b):
    pass


async def func_1(a):
    pass


async def func_2(a, b, c):
    pass


async def func_3(*a):
    pass


async def func_4(a, b, *c):
    pass


async def func_5(a, b, c, *d):
    pass


async def func_6(a = None):
    pass


async def func_7(a, b = None):
    pass


async def func_8(a, b, c = None):
    pass


async def func_9(a, b, c, d = None):
    pass


def func_10(a, b):
    pass


class type_0:
    async def __new__(cls, a, b):
        pass


class type_1:
    async def __call__(self, a, b):
        pass


def _iter_options__passing():
    yield None, 2, (None, False)
    yield func_0, 2, (func_0, False)
    yield func_3, 2, (func_3, False)
    yield func_4, 2, (func_4, False)
    yield func_7, 2, (func_7, False)
    yield func_8, 2, (func_8, False)
    yield type_0, 2, (type_0, False)
    yield type_1, 2, (type_1, True)


def _iter_options__type_error():
    yield object(), 2
    
    yield func_1, 2
    yield func_2, 2
    yield func_5, 2
    yield func_6, 2
    yield func_9, 2
    yield func_10, 2


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_default_handler(default_handler, parameter_count):
    """
    Tests whether ``_validate_default_handler`` works as intended.
    
    Parameters
    ----------
    default_handler : `object`
        Default handler to add by default.
    
    parameter_count : `int`
        How much parameters does the event handler should accept.
    
    Returns
    -------
    output : `(None | async-callable, bool)`
    
    Raises
    ------
    TypeError
    """
    output = _validate_default_handler(default_handler, parameter_count)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    return output
