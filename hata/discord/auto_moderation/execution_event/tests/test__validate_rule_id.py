import vampytest

from ...rule import AutoModerationRule

from ..fields import validate_rule_id


def test__validate_rule_id__0():
    """
    Tests whether `validate_rule_id` works as intended.
    
    Case: passing.
    """
    rule_id = 202211160013
    
    for input_value, expected_output in (
        (None, 0),
        (rule_id, rule_id),
        (AutoModerationRule.precreate(rule_id), rule_id),
        (str(rule_id), rule_id)
    ):
        output = validate_rule_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_rule_id__1():
    """
    Tests whether `validate_rule_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_rule_id(input_value)


def test__validate_rule_id__2():
    """
    Tests whether `validate_rule_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_rule_id(input_value)
