import vampytest

from ..target_id import put_target_id_into


def test__put_target_id_into():
    """
    Tests whether ``put_target_id_into`` works as intended.
    """
    target_id = 202210050005
    
    for input_value, expected_output, include_internals in (
        (target_id, {}, False),
        (target_id, {'id': str(target_id)}, True),
    ):
        output_data = put_target_id_into(input_value, {}, True, include_internals = include_internals)
        vampytest.assert_eq(output_data, expected_output)
