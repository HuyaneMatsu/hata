import vampytest

from ..fields import put_entity_id_into


def test__put_entity_id_into():
    """
    Tests whether ``put_entity_id_into`` works as intended.
    """
    entity_id = 202303140007
    
    for input_value, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'entity_id': None}),
        (entity_id, False, {'entity_id': str(entity_id)}),
    ):
        data = put_entity_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
