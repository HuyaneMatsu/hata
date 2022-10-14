import vampytest

from ....integration import Integration

from ..fields import validate_integrations


def test__validate_integrations__0():
    """
    Tests whether ``validate_integrations`` works as intended.
    
    Case: passing.
    """
    integration = Integration(name = 'ExistRuth')
    
    for input_parameter, expected_output in (
        (None, None),
        ([], None),
        ([integration], (integration, ))
    ):
        output = validate_integrations(input_parameter)
        vampytest.assert_eq(output, expected_output)


def test__validate_integrations__1():
    """
    Tests whether ``validate_integrations`` works as intended.
    
    Case: `TypeError`.
    """
    for input_parameter in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_integrations(input_parameter)
