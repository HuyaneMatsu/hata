import vampytest

from ...application import Application
from ...bases import Icon, IconType

from ..urls import CDN_ENDPOINT, application_cover_url_as


def _iter_options():
    application_id = 202504170110
    yield (
        application_id,
        None,
        {},
        None,
    )
    
    application_id = 202504170111
    yield (
        application_id,
        Icon(IconType.static, 2),
        {'size': 1024},
        f'{CDN_ENDPOINT}/app-assets/{application_id}/store/00000000000000000000000000000002.png?size=1024',
    )
    
    application_id = 202504170112
    yield (
        application_id,
        Icon(IconType.animated, 3),
        {},
        f'{CDN_ENDPOINT}/app-assets/{application_id}/store/a_00000000000000000000000000000003.gif',
    )
    
    application_id = 202504170113
    yield (
        application_id,
        Icon(IconType.animated, 3),
        {'ext': 'png'},
        f'{CDN_ENDPOINT}/app-assets/{application_id}/store/a_00000000000000000000000000000003.png',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__application_cover_url_as(application_id, icon, keyword_parameters):
    """
    Tests whether ``application_cover_url_as`` works as intended.
    
    Parameters
    ----------
    application_id : `int`
        Application identifier to create application for.
    
    icon : `None | Icon`
        Icon to use as the application's cover.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    output : `None | str`
    """
    application = Application.precreate(application_id, cover = icon)
    output = application_cover_url_as(application, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return output
