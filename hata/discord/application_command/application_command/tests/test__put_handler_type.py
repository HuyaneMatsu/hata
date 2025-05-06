import vampytest

from ..fields import put_handler_type
from ..preinstanced import ApplicationCommandHandlerType


def _iter_options():
    yield (
        ApplicationCommandHandlerType.none,
        False,
        {},
    )

    yield (
        ApplicationCommandHandlerType.none,
        True,
        {'handler': ApplicationCommandHandlerType.none.value},
    )
    
    yield (
        ApplicationCommandHandlerType.application,
        False,
        {'handler': ApplicationCommandHandlerType.application.value},
    )

    yield (
        ApplicationCommandHandlerType.application,
        True,
        {'handler': ApplicationCommandHandlerType.application.value},
    )
    
    yield (
        ApplicationCommandHandlerType.discord_embedded_activity_launcher,
        False,
        {'handler': ApplicationCommandHandlerType.discord_embedded_activity_launcher.value},
    )

    yield (
        ApplicationCommandHandlerType.discord_embedded_activity_launcher,
        True,
        {'handler': ApplicationCommandHandlerType.discord_embedded_activity_launcher.value},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_handler_type(input_value, defaults):
    """
    Tests whether ``put_handler_type`` works as intended.
    
    Parameters
    ----------
    input_value : ``ApplicationCommandHandlerType``
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_handler_type(input_value, {}, defaults)
