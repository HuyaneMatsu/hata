import vampytest

from ...integration_application import IntegrationApplication

from ..fields import put_application_into


def _iter_options():
    integration_application_id = 202210140019
    application = IntegrationApplication.precreate(integration_application_id, name = 'hell')
    
    yield (
        None,
        False,
        {
            'application': None,
        },
    )
    
    yield (
        None,
        True,
        {
            'application': None,
        },
    )
    
    yield (
        application,
        False,
        {
            'application': application.to_data(defaults = False),
        },
    )
    
    yield (
        application,
        True,
        {
            'application': application.to_data(defaults = True),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_application_into(application, defaults):
    """
    Tests whether ``put_application_into`` works as intended.
    
    Parameters
    ----------
    application : `None | IntegrationApplication`
        The application to serialize.
    
    defaults : `bool`
        Whether default fields should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_application_into(application, {}, defaults)
