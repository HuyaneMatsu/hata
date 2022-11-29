import vampytest

from ...application_install_parameters import ApplicationInstallParameters

from ..fields import validate_install_parameters


def test__validate_install_parameters():
    """
    Tests whether ``validate_install_parameters`` works as intended.
    """
    install_parameters = ApplicationInstallParameters(permissions = 69)
    
    for input_value, expected_output in (
        (None, None),
        (install_parameters, install_parameters),
    ):
        output = validate_install_parameters(input_value)
        vampytest.assert_eq(output, expected_output)
