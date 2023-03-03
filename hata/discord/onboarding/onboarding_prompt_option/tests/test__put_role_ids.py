import vampytest

from ..fields import put_role_ids_into


def test__put_role_ids_into():
    """
    Tests whether ``put_role_ids_into`` is working as intended.
    """
    role_id = 202303030007
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'role_ids': []}),
        ((role_id, ), False, {'role_ids': [str(role_id)]}),
    ):
        data = put_role_ids_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
