import vampytest

from ...bases import IconType

from ..urls import CDN_ENDPOINT, build_scheduled_event_image_url_as


def _iter_options():
    scheduled_event_id = 202504180013
    yield (
        scheduled_event_id,
        IconType.none,
        0,
        None,
        None,
        None,
    )
    
    scheduled_event_id = 202504180014
    yield (
        scheduled_event_id,
        IconType.static,
        2,
        None,
        1024,
        f'{CDN_ENDPOINT}/guild-events/{scheduled_event_id}/00000000000000000000000000000002.png?size=1024',
    )
    
    scheduled_event_id = 202504180015
    yield (
        scheduled_event_id,
        IconType.animated,
        3,
        None,
        None,
        f'{CDN_ENDPOINT}/guild-events/{scheduled_event_id}/a_00000000000000000000000000000003.gif',
    )
    
    scheduled_event_id = 202504180016
    yield (
        scheduled_event_id,
        IconType.animated,
        3,
        'png',
        None,
        f'{CDN_ENDPOINT}/guild-events/{scheduled_event_id}/a_00000000000000000000000000000003.png',
    )
    
    role_id = 202506210020
    yield (
        role_id,
        IconType.static,
        4,
        'webp',
        None,
        f'{CDN_ENDPOINT}/guild-events/{role_id}/00000000000000000000000000000004.webp',
    )
    
    role_id = 202506210021
    yield (
        role_id,
        IconType.animated,
        4,
        'webp',
        None,
        f'{CDN_ENDPOINT}/guild-events/{role_id}/a_00000000000000000000000000000004.webp?animated=true',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_scheduled_event_image_url_as(scheduled_event_id, icon_type, icon_hash, ext, size):
    """
    Tests whether ``build_scheduled_event_image_url_as`` works as intended.
    
    Parameters
    ----------
    scheduled_event_id : `int`
        ScheduledEvent identifier to create scheduled event for.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    ext : `None | str`
        The extension of the image's url.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_scheduled_event_image_url_as(scheduled_event_id, icon_type, icon_hash, ext, size)
    vampytest.assert_instance(output, str, nullable = True)
    return output
