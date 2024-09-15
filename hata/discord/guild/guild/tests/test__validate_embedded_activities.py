import vampytest

from ....embedded_activity import EmbeddedActivity

from ..fields import validate_embedded_activities


def _iter_options__passing():
    embedded_activity_0 = EmbeddedActivity.precreate(202409030005)
    embedded_activity_1 = EmbeddedActivity.precreate(202409030006)
    
    yield None, None
    yield [], None
    yield [embedded_activity_0], {embedded_activity_0}
    yield [embedded_activity_0, embedded_activity_1], {embedded_activity_0, embedded_activity_1}


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_embedded_activities(input_value):
    """
    Tests whether ``validate_embedded_activities`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | set<EmbeddedActivity>`
    
    Raises
    ------
    TypeError
    """
    output = validate_embedded_activities(input_value)
    vampytest.assert_instance(output, set, nullable = True)
    return output
