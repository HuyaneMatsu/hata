import vampytest

from ....integration import Integration

from ..fields import put_integrations_into


def _iter_options():
    integration_id_0 = 202406250008
    integration_id_1 = 202406250009
    
    integration_0 = Integration.precreate(integration_id_0)
    integration_1 = Integration.precreate(integration_id_1)
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'integrations': [],
        },
    )
    
    yield (
        {
            integration_id_0: integration_0,
            integration_id_1: integration_1,
        },
        False,
        {
            'integrations': [
                integration_0.to_data(defaults = False, include_internals = True),
                integration_1.to_data(defaults = False, include_internals = True),
            ],
        },
    )
    
    yield (
        {
            integration_id_0: integration_0,
            integration_id_1: integration_1,
        },
        True,
        {
            'integrations': [
                integration_0.to_data(defaults = True, include_internals = True),
                integration_1.to_data(defaults = True, include_internals = True),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_integrations_into(input_value, defaults):
    """
    Tests whether ``put_integrations_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | dict<int, Integration>`
        The value to serialise.
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_integrations_into(input_value, {}, defaults)
