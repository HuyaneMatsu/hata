import vampytest

from ..fields import put_application_command_id


def test__put_application_command_id():
    """
    Tests whether ``put_application_command_id`` is working as intended.
    """
    application_command_id = 202302210022
    
    for input_value, defaults, expected_output in (
        (application_command_id, False, {'id': str(application_command_id)}),
    ):
        data = put_application_command_id(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
