import vampytest

from ....application_command import ApplicationCommand

from ..fields import validate_application_commands


def _iter_options__passing():
    application_command_id_0 = 202406270004
    application_command_id_1 = 202406270005
    
    application_command_0 = ApplicationCommand.precreate(application_command_id_0)
    application_command_1 = ApplicationCommand.precreate(application_command_id_1)

    yield None, None
    yield [], None
    yield [application_command_0], {application_command_id_0: application_command_0}
    yield (
        [application_command_0, application_command_0],
        {application_command_id_0: application_command_0},
    )
    yield (
        [application_command_1, application_command_0],
        {application_command_id_0: application_command_0, application_command_id_1: application_command_1},
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_application_commands(input_value):
    """
    Validates whether ``validate_application_commands`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | dict<int, ApplicationCommand>`
    
    Raises
    ------
    TypeError
    """
    output = validate_application_commands(input_value)
    vampytest.assert_instance(output, dict, nullable = True)
    return output
