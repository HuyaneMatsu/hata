import vampytest

from ...application import Application
from ...bases import Icon, IconType

from ..urls import CDN_ENDPOINT, application_icon_url


def _iter_options():
    application_id = 202504170080
    yield (
        application_id,
        None,
        None,
    )
    
    application_id = 202504170081
    yield (
        application_id,
        Icon(IconType.static, 2),
        f'{CDN_ENDPOINT}/app-icons/{application_id}/00000000000000000000000000000002.png',
    )
    
    application_id = 202504170082
    yield (
        application_id,
        Icon(IconType.animated, 3),
        f'{CDN_ENDPOINT}/app-icons/{application_id}/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__application_icon_url(application_id, icon):
    """
    Tests whether ``application_icon_url`` works as intended.
    
    Parameters
    ----------
    application_id : `int`
        Application identifier to create application for.
    
    icon : `None | Icon`
        Icon to create the application with.
    
    Returns
    -------
    output : `None | str`
    """
    application = Application.precreate(application_id, icon = icon)
    output = application_icon_url(application)
    vampytest.assert_instance(output, str, nullable = True)
    return output
