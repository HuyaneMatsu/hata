import vampytest

from ..fields_common import validate_required


def _iter_options__passing():
    yield None, False
    yield True, True
    yield False, False


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_required(input_value):
    output = validate_required(input_value)
    vampytest.assert_instance(output, bool)
    return output
