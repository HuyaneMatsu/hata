import vampytest

from ...bases import Icon, IconType
from ...scheduled_event import ScheduledEvent

from ..urls import CDN_ENDPOINT, scheduled_event_image_url


def _iter_options():
    scheduled_event_id = 202504180010
    yield (
        scheduled_event_id,
        None,
        None,
    )
    
    scheduled_event_id = 202504180011
    yield (
        scheduled_event_id,
        Icon(IconType.static, 2),
        f'{CDN_ENDPOINT}/guild-events/{scheduled_event_id}/00000000000000000000000000000002.png',
    )
    
    scheduled_event_id = 202504180012
    yield (
        scheduled_event_id,
        Icon(IconType.animated, 3),
        f'{CDN_ENDPOINT}/guild-events/{scheduled_event_id}/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__scheduled_event_image_url(scheduled_event_id, icon):
    """
    Tests whether ``scheduled_event_image_url`` works as intended.
    
    Parameters
    ----------
    scheduled_event_id : `int`
        ScheduledEvent identifier to create scheduled event for.
    
    icon : `None | Icon`
        Icon to use as the scheduled event's image.
    
    Returns
    -------
    output : `None | str`
    """
    scheduled_event = ScheduledEvent.precreate(scheduled_event_id, image = icon)
    output = scheduled_event_image_url(scheduled_event)
    vampytest.assert_instance(output, str, nullable = True)
    return output
