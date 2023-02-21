import vampytest

from ..fields import put_target_id_into


def test__put_target_id_into():
    """
    Tests whether ``put_target_id_into`` works as intended.
    """
    target_id = 202302200001
    
    for input_value, defaults, expected_output in (
        (0, False, {'id': None}),
        (0, True, {'id': None}),
        (target_id, False, {'id': str(target_id)}),
    ):
        data = put_target_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
