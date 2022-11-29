import vampytest

from ...application_install_parameters import ApplicationInstallParameters

from ..fields import parse_install_parameters


def test__parse_install_parameters():
    """
    Tests whether ``parse_install_parameters`` works as intended.
    """
    install_parameters = ApplicationInstallParameters(permissions = 69)
    
    for input_value, expected_output in (
        ({}, None),
        ({'install_params': None}, None),
        ({'install_params': install_parameters.to_data(defaults = True)}, install_parameters),
    ):
        output = parse_install_parameters(input_value)
        vampytest.assert_eq(output, expected_output)
