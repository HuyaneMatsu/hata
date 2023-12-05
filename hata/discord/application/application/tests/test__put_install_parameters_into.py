import vampytest

from ...application_install_parameters import ApplicationInstallParameters

from ..fields import put_install_parameters_into


def _iter_options():
    install_parameters = ApplicationInstallParameters(permissions = 69)
    
    yield None, False, {}
    yield None, True, {'install_params': None}
    yield install_parameters, False, {'install_params': install_parameters.to_data(defaults = False)}
    yield install_parameters, True, {'install_params': install_parameters.to_data(defaults = True)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_install_parameters_into(input_value, defaults):
    """
    Tests whether ``put_install_parameters_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | EmbeddedActivityConfiguration`
        Value to serialize.
    defaults : `bool`
        Whether fields with their value should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_install_parameters_into(input_value, {}, defaults)
