import vampytest

from ..fields import parse_role_ids


def test__parse_role_ids():
    """
    Tests whether ``parse_role_ids`` works as intended.
    """
    role_id_1 = 202210280000
    role_id_2 = 202210280001
    
    for input_data, expected_output in (
        ({}, None),
        ({'roles': None}, None),
        ({'roles': []}, None),
        ({'roles': [str(role_id_1), str(role_id_2)]}, (role_id_1, role_id_2)),
        ({'roles': [str(role_id_2), str(role_id_1)]}, (role_id_1, role_id_2)),
    ):
        output = parse_role_ids(input_data)
        vampytest.assert_eq(output, expected_output)
