import vampytest

from ..fields import parse_integration_context_types
from ..preinstanced import ApplicationCommandIntegrationContextType


def _iter_options():
    yield {}, None
    yield {'contexts': None}, None
    yield {'contexts': []}, None
    yield (
        {'contexts': [ApplicationCommandIntegrationContextType.bot_private_channel.value]},
        (ApplicationCommandIntegrationContextType.bot_private_channel,),
    )
    yield (
        {
            'contexts': [
                ApplicationCommandIntegrationContextType.bot_private_channel.value,
                ApplicationCommandIntegrationContextType.guild.value
            ],
        },
        (ApplicationCommandIntegrationContextType.guild, ApplicationCommandIntegrationContextType.bot_private_channel,),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_integration_context_types(input_data):
    """
    Tests whether ``parse_integration_context_types`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<ApplicationCommandIntegrationContextType>`
    """
    return parse_integration_context_types(input_data)
