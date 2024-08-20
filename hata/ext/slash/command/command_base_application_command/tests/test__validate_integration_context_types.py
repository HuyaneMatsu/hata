import vampytest

from ......discord import ApplicationCommandIntegrationContextType, INTEGRATION_CONTEXT_TYPES_ALL

from ..helpers import _validate_integration_context_types


def _iter_options__passing():
    yield None, None
    yield [], None
    yield (
        [ApplicationCommandIntegrationContextType.bot_private_channel],
        (ApplicationCommandIntegrationContextType.bot_private_channel, ),
    )
    yield (
        [ApplicationCommandIntegrationContextType.bot_private_channel.value],
        (ApplicationCommandIntegrationContextType.bot_private_channel, )
    )
    yield (
        ['bot_private_channel'],
        (ApplicationCommandIntegrationContextType.bot_private_channel, )
    )
    yield (
        [
            ApplicationCommandIntegrationContextType.bot_private_channel,
            ApplicationCommandIntegrationContextType.guild,
        ],
        (
            ApplicationCommandIntegrationContextType.guild,
            ApplicationCommandIntegrationContextType.bot_private_channel,
        ),
    )
    yield (
        [
            ApplicationCommandIntegrationContextType.bot_private_channel,
            ApplicationCommandIntegrationContextType.any_private_channel,
            ApplicationCommandIntegrationContextType.guild,
        ],
        INTEGRATION_CONTEXT_TYPES_ALL,
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_integration_context_types(input_value):
    """
    Tests whether `_validate_integration_context_types` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<ApplicationCommandIntegrationContextType>`
    
    Raises
    ------
    TypeError
    """
    return _validate_integration_context_types(input_value)
