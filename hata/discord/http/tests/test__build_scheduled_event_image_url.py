import vampytest

from ...bases import IconType

from ..urls import CDN_ENDPOINT, build_scheduled_event_image_url


def _iter_options():
    scheduled_event_id = 202504180010
    yield (
        scheduled_event_id,
        IconType.none,
        0,
        None,
    )
    
    scheduled_event_id = 202504180011
    yield (
        scheduled_event_id,
        IconType.static,
        2,
        f'{CDN_ENDPOINT}/guild-events/{scheduled_event_id}/00000000000000000000000000000002.png',
    )
    
    scheduled_event_id = 202504180012
    yield (
        scheduled_event_id,
        IconType.animated,
        3,
        f'{CDN_ENDPOINT}/guild-events/{scheduled_event_id}/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_scheduled_event_image_url(scheduled_event_id, icon_type, icon_hash):
    """
    Tests whether ``build_scheduled_event_image_url`` works as intended.
    
    Parameters
    ----------
    scheduled_event_id : `int`
        ScheduledEvent identifier to create scheduled event for.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    Returns
    -------
    output : `None | str`
    """
    output = build_scheduled_event_image_url(scheduled_event_id, icon_type, icon_hash)
    vampytest.assert_instance(output, str, nullable = True)
    return output
