import vampytest

from ...message_application import MessageApplication

from ..fields import validate_application


def test__validate_application__0():
    """
    Tests whether `validate_application` works as intended.
    
    Case: passing.
    """
    application_id = 202304290005
    application = MessageApplication.precreate(application_id, name = 'Orin')
    
    for input_value, expected_output in (
        (None, None),
        (application, application),
    ):
        output = validate_application(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_application__1():
    """
    Tests whether `validate_application` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_application(input_value)
