import vampytest

from ...integration_application import IntegrationApplication

from ..fields import parse_application


def _iter_options():
    integration_application_id = 202210140018
    application = IntegrationApplication.precreate(integration_application_id, name = 'hell')
    
    yield {}, None
    yield {'application': None}, None
    yield {'application': application.to_data(defaults = True, include_internals = True)}, application


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_application(input_data):
    """
    Tests whether ``parse_application`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | Application`
    """
    output = parse_application(input_data)
    vampytest.assert_instance(output, IntegrationApplication, nullable = True)
    return output
