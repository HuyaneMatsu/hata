import vampytest

from ..helpers import (
    convert_string_to_boolean, convert_string_to_integer, serialise_boolean_to_string, serialise_integer_to_string
)

def _iter_options__convert_string_to_integer():
    yield None, 0
    yield 5, 5
    yield '5', 5
    yield 'a', 0
    yield 12.6, 0

@vampytest._(vampytest.call_from(_iter_options__convert_string_to_integer()).returning_last())
def test__convert_string_to_integer(value):
    output = convert_string_to_integer(value)
    vampytest.assert_instance(output, int)
    return output


def _iter_options__convert_string_to_boolean():
    yield None, 0
    yield True, True
    yield False, False
    yield '1', True
    yield '0', False
    yield 'a', False
    yield 12.6, False

@vampytest._(vampytest.call_from(_iter_options__convert_string_to_boolean()).returning_last())
def test__convert_string_to_boolean(value):
    output = convert_string_to_boolean(value)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__serialise_boolean_to_string():
    yield False, '0'
    yield True, '1'

@vampytest._(vampytest.call_from(_iter_options__serialise_boolean_to_string()).returning_last())
def test__serialise_boolean_to_string(value):
    output = serialise_boolean_to_string(value)
    vampytest.assert_instance(output, str)
    return output


def _iter_options__serialise_integer_to_string():
    yield 5, '5'

@vampytest._(vampytest.call_from(_iter_options__serialise_integer_to_string()).returning_last())
def test__serialise_integer_to_string(value):
    output = serialise_integer_to_string(value)
    vampytest.assert_instance(output, str)
    return output
