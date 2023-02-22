import vampytest

from ..fields import put_id_into


def test__put_id_into():
    """
    Tests whether ``put_id_into`` works as intended.
    """
    application_entity_id = 202211240042
    
    for input_value, defaults, expected_output in (
        (application_entity_id, False, {'id': str(application_entity_id)}),
    ):
        data = put_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
