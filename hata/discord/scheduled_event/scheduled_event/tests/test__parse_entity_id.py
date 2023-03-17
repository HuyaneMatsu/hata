import vampytest

from ..fields import parse_entity_id


def test__parse_entity_id():
    """
    Tests whether ``parse_entity_id`` works as intended.
    """
    entity_id = 202303140006
    
    for input_data, expected_output in (
        ({}, 0),
        ({'entity_id': None}, 0),
        ({'entity_id': str(entity_id)}, entity_id),
    ):
        output = parse_entity_id(input_data)
        vampytest.assert_eq(output, expected_output)
