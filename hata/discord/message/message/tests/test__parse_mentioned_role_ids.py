import vampytest

from ..fields import parse_mentioned_role_ids


def test__parse_mentioned_role_ids():
    """
    Tests whether ``parse_mentioned_role_ids`` works as intended.
    """
    role_id_1 = 202305010014
    role_id_2 = 202305010015
    
    for input_data, expected_output in (
        ({}, None),
        ({'mention_roles': None}, None),
        ({'mention_roles': []}, None),
        ({'mention_roles': [str(role_id_1), str(role_id_2)]}, (role_id_1, role_id_2)),
        ({'mention_roles': [str(role_id_2), str(role_id_1)]}, (role_id_1, role_id_2)),
    ):
        output = parse_mentioned_role_ids(input_data)
        vampytest.assert_eq(output, expected_output)
