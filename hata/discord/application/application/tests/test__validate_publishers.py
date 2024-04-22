import vampytest

from ...application_entity import ApplicationEntity

from ..fields import validate_publishers


def _iter_options__passing():
    application_entity_0 = ApplicationEntity.precreate(202404140008)
    application_entity_1 = ApplicationEntity.precreate(202404140009)
    
    yield None, None
    yield [], None
    yield [application_entity_0], (application_entity_0,)
    yield [application_entity_0, application_entity_0], (application_entity_0, )
    yield [application_entity_0, application_entity_1], (application_entity_0, application_entity_1)
    yield [application_entity_1, application_entity_0], (application_entity_0, application_entity_1)


def _iter_options__type_error():
    yield 2.3
    yield [2.3]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_publishers(input_value):
    """
    Tests whether ``validate_publishers`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<ApplicationEntity>`
    """
    return validate_publishers(input_value)
