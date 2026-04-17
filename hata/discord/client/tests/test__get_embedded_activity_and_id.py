import vampytest

from ...embedded_activity import EmbeddedActivity

from ..request_helpers import get_embedded_activity_and_id


def _iter_options__passing():
    embedded_activity_id = 202409040050
    
    yield (
        embedded_activity_id,
        [],
        (None, embedded_activity_id),
    )
    
    
    embedded_activity_id = 202409040051
    
    yield (
        str(embedded_activity_id),
        [],
        (None, embedded_activity_id),
    )
    
    
    embedded_activity_id = 202409040052
    embedded_activity = EmbeddedActivity.precreate(embedded_activity_id) 
    
    yield (
        embedded_activity,
        [embedded_activity],
        (embedded_activity, embedded_activity_id),
    )
    
    
    embedded_activity_id = 202409040053
    embedded_activity = EmbeddedActivity.precreate(embedded_activity_id) 
    
    yield (
        embedded_activity_id,
        [embedded_activity],
        (embedded_activity, embedded_activity_id),
    )


def _iter_options__type_error():
    yield None, []
    yield 12.6, []


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__get_embedded_activity_and_id(input_value, extra):
    """
    Tests whether ``get_embedded_activity_and_id`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to test with.
    extra : `list<object>`
        Extra objects to keep in cache.
    
    Returns
    -------
    output : `(None | EmbeddedActivity, int)`
    
    Raises
    ------
    TypeError
    """
    return get_embedded_activity_and_id(input_value)
