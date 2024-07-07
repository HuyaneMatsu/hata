import vampytest

from ....integration import Integration

from ..fields import validate_integrations


def _iter_options__passing():
    integration_id_0 = 202406270008
    integration_id_1 = 202406270009
    
    integration_0 = Integration.precreate(integration_id_0)
    integration_1 = Integration.precreate(integration_id_1)

    yield None, None
    yield [], None
    yield [integration_0], {integration_id_0: integration_0}
    yield (
        [integration_0, integration_0],
        {integration_id_0: integration_0},
    )
    yield (
        [integration_1, integration_0],
        {integration_id_0: integration_0, integration_id_1: integration_1},
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_integrations(input_value):
    """
    Validates whether ``validate_integrations`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | dict<int, Integration>`
    
    Raises
    ------
    TypeError
    """
    output = validate_integrations(input_value)
    vampytest.assert_instance(output, dict, nullable = True)
    return output
