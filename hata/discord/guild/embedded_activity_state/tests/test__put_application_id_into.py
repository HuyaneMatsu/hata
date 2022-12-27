import vampytest

from ..fields import put_application_id_into


def test__put_application_id_into():
    """
    Tests whether ``put_application_id_into`` is working as intended.
    """
    application_id = 202212260001
    
    for input_value, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'embedded_activity': {'application_id': None}}),
        (application_id, False, {'embedded_activity': {'application_id': str(application_id)}}),
    ):
        data = put_application_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
