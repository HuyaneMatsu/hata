import vampytest

from ..fields import parse_excluded_role_ids


def test__parse_excluded_role_ids():
    """
    Tests whether ``parse_excluded_role_ids`` works as intended.
    """
    role_id_1 = 202211170034
    role_id_2 = 202211170035
    
    for input_data, expected_output in (
        ({}, None),
        ({'exempt_roles': None}, None),
        ({'exempt_roles': []}, None),
        ({'exempt_roles': [str(role_id_1), str(role_id_2)]}, (role_id_1, role_id_2)),
        ({'exempt_roles': [str(role_id_2), str(role_id_1)]}, (role_id_1, role_id_2)),
    ):
        output = parse_excluded_role_ids(input_data)
        vampytest.assert_eq(output, expected_output)
