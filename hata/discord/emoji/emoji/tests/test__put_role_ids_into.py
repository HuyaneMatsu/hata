import vampytest

from ..fields import put_role_ids_into


def test__put_role_ids_into():
    """
    Tests whether ``put_role_ids_into`` is working as intended.
    """
    role_id = 202212310007
    
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'roles': []}),
        ((role_id, ), False, {'roles': [str(role_id)]}),
    ):
        data = put_role_ids_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
