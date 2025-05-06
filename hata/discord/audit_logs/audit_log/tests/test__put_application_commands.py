import vampytest

from ....application_command import ApplicationCommand

from ..fields import put_application_commands


def _iter_options():
    application_command_id_0 = 202406250000
    application_command_id_1 = 202406250001
    
    application_command_0 = ApplicationCommand.precreate(application_command_id_0)
    application_command_1 = ApplicationCommand.precreate(application_command_id_1)
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'application_commands': [],
        },
    )
    
    yield (
        {
            application_command_id_0: application_command_0,
            application_command_id_1: application_command_1,
        },
        False,
        {
            'application_commands': [
                application_command_0.to_data(defaults = False, include_internals = True),
                application_command_1.to_data(defaults = False, include_internals = True),
            ],
        },
    )
    
    yield (
        {
            application_command_id_0: application_command_0,
            application_command_id_1: application_command_1,
        },
        True,
        {
            'application_commands': [
                application_command_0.to_data(defaults = True, include_internals = True),
                application_command_1.to_data(defaults = True, include_internals = True),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_application_commands(input_value, defaults):
    """
    Tests whether ``put_application_commands`` works as intended.
    
    Parameters
    ----------
    input_value : `None | dict<int, ApplicationCommand>`
        The value to serialise.
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_application_commands(input_value, {}, defaults)
