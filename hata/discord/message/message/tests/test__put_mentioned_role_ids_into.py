import vampytest

from ..fields import put_mentioned_role_ids_into


def test__put_mentioned_role_ids_into():
    """
    Tests whether ``put_mentioned_role_ids_into`` works as intended.
    """
    role_id = 202305010016
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'mention_roles': []}),
        ((role_id, ), False, {'mention_roles': [str(role_id)]}),
    ):
        data = put_mentioned_role_ids_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
