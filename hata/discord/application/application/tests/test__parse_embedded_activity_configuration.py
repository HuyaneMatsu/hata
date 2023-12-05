import vampytest

from ...embedded_activity_configuration import EmbeddedActivityConfiguration

from ..fields import parse_embedded_activity_configuration


def _iter_options():
    embedded_activity_configuration = EmbeddedActivityConfiguration(position = 69)
    
    yield {}, None
    yield {'embedded_activity_config': None}, None
    yield (
        {'embedded_activity_config': embedded_activity_configuration.to_data(defaults = True)},
        embedded_activity_configuration,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_embedded_activity_configuration(input_data):
    """
    Tests whether ``parse_embedded_activity_configuration`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | EmbeddedActivityConfiguration`
    """
    return parse_embedded_activity_configuration(input_data)
