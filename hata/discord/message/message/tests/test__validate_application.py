import vampytest

from ...message_application import MessageApplication

from ..fields import validate_application


def _iter_options__passing():
    application_id = 202304290005
    application = MessageApplication.precreate(application_id, name = 'Orin')
    
    yield None, None
    yield application, application


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_application(input_value):
    """
    Tests whether ``validate_application`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | MessageApplication`
    
    Raises
    ------
    TypeError
    """
    output = validate_application(input_value)
    vampytest.assert_instance(output, MessageApplication, nullable = True)
    return output
