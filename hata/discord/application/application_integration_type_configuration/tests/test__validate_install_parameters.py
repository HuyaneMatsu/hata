import vampytest

from ...application_install_parameters import ApplicationInstallParameters

from ..fields import validate_install_parameters


def _iter_options__passing():
    install_parameters = ApplicationInstallParameters(permissions = 69)
    
    yield None, None
    yield install_parameters, install_parameters


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_install_parameters(input_value):
    """
    Tests whether ``validate_install_parameters`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | ApplicationInstallParameters`
    
    Raises
    ------
    TypeError
    """
    return validate_install_parameters(input_value)
