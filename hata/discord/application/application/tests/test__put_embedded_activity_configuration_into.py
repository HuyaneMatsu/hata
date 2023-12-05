import vampytest

from ...embedded_activity_configuration import EmbeddedActivityConfiguration

from ..fields import put_embedded_activity_configuration_into


def _iter_options():
    embedded_activity_configuration = EmbeddedActivityConfiguration(position = 69)
    
    yield None, False, {}
    yield None, True, {'embedded_activity_config': None}
    yield (
        embedded_activity_configuration,
        False,
        {'embedded_activity_config': embedded_activity_configuration.to_data(defaults = False)},
    )
    yield (
        embedded_activity_configuration,
        True,
        {'embedded_activity_config': embedded_activity_configuration.to_data(defaults = True)},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_embedded_activity_configuration_into(input_value, defaults):
    """
    Tests whether ``put_embedded_activity_configuration_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | EmbeddedActivityConfiguration`
        Value to serialize.
    defaults : `bool`
        Whether fields with their value should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_embedded_activity_configuration_into(input_value, {}, defaults)
