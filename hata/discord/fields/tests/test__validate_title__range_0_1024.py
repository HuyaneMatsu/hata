import vampytest

from ..fields_common import validate_title__range_0_1024


def _iter_options__passing():
    yield None, None
    yield '', None
    yield 'a', 'a'
    yield 'aa', 'aa'


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_title__range_0_1024(input_value):
    output = validate_title__range_0_1024(input_value)
    vampytest.assert_instance(output, str, nullable = True)
    return output
