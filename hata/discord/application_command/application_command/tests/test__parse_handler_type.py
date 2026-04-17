import vampytest

from ..fields import parse_handler_type
from ..preinstanced import ApplicationCommandHandlerType


def _iter_options():
    yield (
        {},
        ApplicationCommandHandlerType.none,
    )
    
    yield (
        {'handler': None},
        ApplicationCommandHandlerType.none,
    )
    
    yield (
        {'handler': ApplicationCommandHandlerType.application.value},
        ApplicationCommandHandlerType.application,
    )
    
    yield (
        {'handler': ApplicationCommandHandlerType.discord_embedded_activity_launcher.value},
        ApplicationCommandHandlerType.discord_embedded_activity_launcher,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_handler_type(input_data):
    """
    Tests whether ``parse_handler_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``ApplicationCommandHandlerType``
    """
    output = parse_handler_type(input_data)
    vampytest.assert_instance(output, ApplicationCommandHandlerType)
    return output
