import vampytest

from ..fields import put_id_into


def test__put_id_into():
    """
    Tests whether ``put_id_into`` works as intended.
    """
    application_command_id = 202302260007
    
    for input_value, defaults, expected_output in (
        (0, False, {'id': None}),
        (0, True, {'id': None}),
        (application_command_id, False, {'id': str(application_command_id)}),
    ):
        data = put_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
