import vampytest

from ....application_command import ApplicationCommand

from ..fields import parse_application_commands


def _iter_options():
    application_command_id_0 = 202406240002
    application_command_id_1 = 202406240003
    
    application_command_0 = ApplicationCommand.precreate(application_command_id_0)
    application_command_1 = ApplicationCommand.precreate(application_command_id_1)
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'application_commands': [],
        },
        None,
    )
    
    yield (
        {
            'application_commands': [
                application_command_0.to_data(defaults = True, include_internals = True),
                application_command_1.to_data(defaults = True, include_internals = True),
            ],
        },
        {
            application_command_id_0: application_command_0,
            application_command_id_1: application_command_1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_application_commands(input_data):
    """
    Tests whether ``parse_application_commands`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `dict<int, ApplicationCommand>`
    """
    return parse_application_commands(input_data)
