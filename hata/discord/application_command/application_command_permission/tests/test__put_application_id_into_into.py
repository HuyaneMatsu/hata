import vampytest

from ..fields import put_application_id_into


def test__put_application_id_into():
    """
    Tests whether ``put_application_id_into`` is working as intended.
    """
    application_id = 202302210025
    
    for input_value, defaults, expected_output in (
        (application_id, False, {'application_id': str(application_id)}),
    ):
        data = put_application_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
