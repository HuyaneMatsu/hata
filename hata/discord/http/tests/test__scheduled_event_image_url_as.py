import vampytest

from ...bases import Icon, IconType
from ...scheduled_event import ScheduledEvent

from ..urls import CDN_ENDPOINT, scheduled_event_image_url_as


def _iter_options():
    scheduled_event_id = 202504180013
    yield (
        scheduled_event_id,
        None,
        {},
        None,
    )
    
    scheduled_event_id = 202504180014
    yield (
        scheduled_event_id,
        Icon(IconType.static, 2),
        {'size': 1024},
        f'{CDN_ENDPOINT}/guild-events/{scheduled_event_id}/00000000000000000000000000000002.png?size=1024',
    )
    
    scheduled_event_id = 202504180015
    yield (
        scheduled_event_id,
        Icon(IconType.animated, 3),
        {},
        f'{CDN_ENDPOINT}/guild-events/{scheduled_event_id}/a_00000000000000000000000000000003.gif',
    )
    
    scheduled_event_id = 202504180016
    yield (
        scheduled_event_id,
        Icon(IconType.animated, 3),
        {'ext': 'png'},
        f'{CDN_ENDPOINT}/guild-events/{scheduled_event_id}/a_00000000000000000000000000000003.png',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__scheduled_event_image_url_as(scheduled_event_id, icon, keyword_parameters):
    """
    Tests whether ``scheduled_event_image_url_as`` works as intended.
    
    Parameters
    ----------
    scheduled_event_id : `int`
        Scheduled event identifier to create scheduled event for.
    
    icon : `None | Icon`
        Icon to use as the scheduled event's image.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    output : `None | str`
    """
    scheduled_event = ScheduledEvent.precreate(scheduled_event_id, image = icon)
    output = scheduled_event_image_url_as(scheduled_event, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return output
