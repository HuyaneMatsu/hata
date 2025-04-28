import vampytest

from ....application import Application

from ..fields import validate_activity_application_ids


def _iter_options__passing():
    application_id_0 = 202504210009
    application_id_1 = 202504210010
    
    yield None, None
    yield [], None
    yield [application_id_0, application_id_1], (application_id_0, application_id_1)
    yield [application_id_1, application_id_0], (application_id_1, application_id_0)
    yield [Application.precreate(application_id_0), Application.precreate(application_id_1)], (application_id_0, application_id_1)


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_activity_application_ids(input_value):
    """
    Tests whether `validate_activity_application_ids` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<int>`
    
    Raises
    ------
    TypeError
    """
    output = validate_activity_application_ids(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
