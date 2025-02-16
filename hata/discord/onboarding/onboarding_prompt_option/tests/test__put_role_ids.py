import vampytest

from ..fields import put_role_ids


def test__put_role_ids():
    """
    Tests whether ``put_role_ids`` is working as intended.
    """
    role_id = 202303030007
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'role_ids': []}),
        ((role_id, ), False, {'role_ids': [str(role_id)]}),
    ):
        data = put_role_ids(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
