import vampytest

from ..fields import validate_accepted


def _iter_options__passing():
    yield True, True
    yield False, False
    yield None, True


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_accepted(input_value):
    return validate_accepted(input_value)
