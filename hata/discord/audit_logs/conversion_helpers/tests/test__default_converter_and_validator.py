import vampytest

from ..helpers import _default_converter_and_validator


def test__default_converter_and_validator():
    """
    Tests whether ``default_converter_and_validator`` works as intended.
    """
    input = object()
    output = _default_converter_and_validator(input)
    vampytest.assert_is(input, output)
