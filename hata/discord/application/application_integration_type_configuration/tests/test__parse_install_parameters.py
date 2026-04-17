import vampytest

from ...application_install_parameters import ApplicationInstallParameters

from ..fields import parse_install_parameters


def _iter_options():
    install_parameters = ApplicationInstallParameters(permissions = 69)
    
    yield {}, None
    yield {'oauth2_install_params': None}, None
    yield {'oauth2_install_params': install_parameters.to_data(defaults = True)}, install_parameters
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_install_parameters(input_data):
    """
    Tests whether ``parse_install_parameters`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | ApplicationInstallParameters`
    """
    return parse_install_parameters(input_data)
