import vampytest

from ..target_id import parse_target_id


def test__parse_target_id():
    """
    Tests whether ``parse_target_id`` works as intended.
    """
    target_id = 202210050006
    
    for input_value, expected_output in (
        ({'id': str(target_id)}, target_id),
    ):
        output = parse_target_id(input_value)
        vampytest.assert_eq(output, expected_output)
