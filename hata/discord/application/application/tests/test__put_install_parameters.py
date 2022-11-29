import vampytest

from ...application_install_parameters import ApplicationInstallParameters

from ..fields import put_install_parameters_into


def test__put_install_parameters_into():
    """
    Tests whether ``put_install_parameters_into`` works as intended.
    """
    install_parameters = ApplicationInstallParameters(permissions = 69)
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'install_params': None}),
        (install_parameters, True, {'install_params': install_parameters.to_data(defaults = True)}),
    ):
        output = put_install_parameters_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
