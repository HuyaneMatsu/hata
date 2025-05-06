import vampytest

from ..fields import put_target_id


def test__put_target_id():
    """
    Tests whether ``put_target_id`` works as intended.
    """
    target_id = 202302200001
    
    for input_value, defaults, expected_output in (
        (0, False, {'id': None}),
        (0, True, {'id': None}),
        (target_id, False, {'id': str(target_id)}),
    ):
        data = put_target_id(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
