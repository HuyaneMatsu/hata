import vampytest

from ...application import Application
from ...bases import Icon, IconType

from ..urls import CDN_ENDPOINT, application_cover_url


def _iter_options():
    application_id = 202504170100
    yield (
        application_id,
        None,
        None,
    )
    
    application_id = 202504170101
    yield (
        application_id,
        Icon(IconType.static, 2),
        f'{CDN_ENDPOINT}/app-assets/{application_id}/store/00000000000000000000000000000002.png',
    )
    
    application_id = 202504170102
    yield (
        application_id,
        Icon(IconType.animated, 3),
        f'{CDN_ENDPOINT}/app-assets/{application_id}/store/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__application_cover_url(application_id, icon):
    """
    Tests whether ``application_cover_url`` works as intended.
    
    Parameters
    ----------
    application_id : `int`
        Application identifier to create application for.
    
    icon : `None | Icon`
        Icon to use as the application's cover.
    
    Returns
    -------
    output : `None | str`
    """
    application = Application.precreate(application_id, cover = icon)
    output = application_cover_url(application)
    vampytest.assert_instance(output, str, nullable = True)
    return output
