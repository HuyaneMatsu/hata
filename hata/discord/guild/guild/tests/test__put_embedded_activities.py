import vampytest

from ....embedded_activity import EmbeddedActivity

from ..fields import put_embedded_activities


def _iter_options():
    embedded_activity = EmbeddedActivity.precreate(202409030004)
    
    yield None, False, {'activity_instances': []}
    yield None, True, {'activity_instances': []}
    
    yield (
        {embedded_activity},
        False,
        {'activity_instances': [embedded_activity.to_data(defaults = False, include_internals = True)]},
    )
    
    yield (
        {embedded_activity},
        True,
        {'activity_instances': [embedded_activity.to_data(defaults = True, include_internals = True)]},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_embedded_activities(input_value, defaults):
    """
    Tests whether ``put_embedded_activities`` works as intended.
    
    Parameters
    ----------
    input_value : `set<EmbeddedActivity>`
        Input value to serialise.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_embedded_activities(input_value, {}, defaults)
