import vampytest

from ...bases import IconType

from ..urls import CDN_ENDPOINT, build_application_icon_url


def _iter_options():
    application_id = 202504170080
    yield (
        application_id,
        IconType.none,
        0,
        None,
    )
    
    application_id = 202504170081
    yield (
        application_id,
        IconType.static,
        2,
        f'{CDN_ENDPOINT}/app-icons/{application_id}/00000000000000000000000000000002.png',
    )
    
    application_id = 202504170082
    yield (
        application_id,
        IconType.animated,
        3,
        f'{CDN_ENDPOINT}/app-icons/{application_id}/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_application_icon_url(application_id, icon_type, icon_hash):
    """
    Tests whether ``build_application_icon_url`` works as intended.
    
    Parameters
    ----------
    application_id : `int`
        Application identifier to create application for.
    
    icon_type : ``IconType``
        Icon type to use.
    
    icon_hash : `int`
        Icon hash to use (uint128).
    
    Returns
    -------
    output : `None | str`
    """
    output = build_application_icon_url(application_id, icon_type, icon_hash)
    vampytest.assert_instance(output, str, nullable = True)
    return output
