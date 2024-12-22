import vampytest

from ..fields import validate_handler_type
from ..preinstanced import ApplicationCommandHandlerType


def _iter_options__passing():
    yield None, ApplicationCommandHandlerType.none
    yield ApplicationCommandHandlerType.none, ApplicationCommandHandlerType.none
    yield ApplicationCommandHandlerType.none.value, ApplicationCommandHandlerType.none
    yield ApplicationCommandHandlerType.application, ApplicationCommandHandlerType.application
    yield ApplicationCommandHandlerType.application.value, ApplicationCommandHandlerType.application
    yield ApplicationCommandHandlerType.discord_embedded_activity_launcher, ApplicationCommandHandlerType.discord_embedded_activity_launcher
    yield (
        ApplicationCommandHandlerType.discord_embedded_activity_launcher.value,
        ApplicationCommandHandlerType.discord_embedded_activity_launcher,
    )


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_handler_type(input_value):
    """
    Validates whether ``validate_handler_type`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``ApplicationCommandHandlerType``
    
    Raises
    ------
    TypeError
    """
    output = validate_handler_type(input_value)
    vampytest.assert_instance(output, ApplicationCommandHandlerType)
    return output
