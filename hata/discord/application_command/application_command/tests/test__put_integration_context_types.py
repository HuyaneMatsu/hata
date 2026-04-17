import vampytest

from ..fields import put_integration_context_types
from ..preinstanced import ApplicationCommandIntegrationContextType


def _iter_options():
    yield None, False, {'contexts': None}
    yield None, True, {'contexts': None}
    yield (
        (ApplicationCommandIntegrationContextType.bot_private_channel, ),
        False,
        {'contexts': [ApplicationCommandIntegrationContextType.bot_private_channel.value]},
    )
    yield (
        (ApplicationCommandIntegrationContextType.bot_private_channel, ),
        True,
        {'contexts': [ApplicationCommandIntegrationContextType.bot_private_channel.value]},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_integration_context_types(input_value, defaults):
    """
    Tests whether ``put_integration_context_types`` is working as intended.
    
    Parameters
    ----------
    input_value : `none | tuple<ApplicationCommandIntegrationContextType>`
        Value to serialize.
    defaults : `bool`
        Whether fields with their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_integration_context_types(input_value, {}, defaults)
