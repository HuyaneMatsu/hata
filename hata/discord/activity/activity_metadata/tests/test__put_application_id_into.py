import vampytest

from ..fields import put_application_id_into


def test__put_application_id_into():
    """
    Tests whether ``put_application_id_into`` works as intended.
    """
    application_id = 202212290004
    
    for input_value, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'application_id': None}),
        (application_id, False, {'application_id': str(application_id)}),
    ):
        data = put_application_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
