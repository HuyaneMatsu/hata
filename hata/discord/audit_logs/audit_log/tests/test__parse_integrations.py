import vampytest

from ....integration import Integration

from ..fields import parse_integrations


def _iter_options():
    integration_id_0 = 202406240008
    integration_id_1 = 202406240009
    
    integration_0 = Integration.precreate(integration_id_0)
    integration_1 = Integration.precreate(integration_id_1)
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'integrations': [],
        },
        None,
    )
    
    yield (
        {
            'integrations': [
                integration_0.to_data(defaults = True, include_internals = True),
                integration_1.to_data(defaults = True, include_internals = True),
            ],
        },
        {
            integration_id_0: integration_0,
            integration_id_1: integration_1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_integrations(input_data):
    """
    Tests whether ``parse_integrations`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `dict<int, Integration>`
    """
    return parse_integrations(input_data)
