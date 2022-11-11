import vampytest

from ...string_select_option import StringSelectOption
from ..fields import validate_options


def test__validate_options__0():
    """
    Tests whether ``validate_options`` works as intended.
    
    Case: passing.
    """
    option = StringSelectOption('hello')
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([option], (option, )),
    ):
        output = validate_options(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_options__1():
    """
    Tests whether ``validate_options`` works as intended.
    
    Case: `TypeError`.
    """
    option = StringSelectOption('hello')
    
    for input_value in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_options(input_value)
