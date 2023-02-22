import vampytest

from ..fields import put_application_command_id_into


def test__put_application_command_id_into():
    """
    Tests whether ``put_application_command_id_into`` is working as intended.
    """
    application_command_id = 202302210022
    
    for input_value, defaults, expected_output in (
        (application_command_id, False, {'id': str(application_command_id)}),
    ):
        data = put_application_command_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
