import vampytest

from ..fields import put_excluded_role_ids


def test__put_excluded_role_ids():
    """
    Tests whether ``put_excluded_role_ids`` is working as intended.
    """
    role_id = 202211170037
    
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'exempt_roles': []}),
        ((role_id, ), False, {'exempt_roles': [str(role_id)]}),
    ):
        data = put_excluded_role_ids(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
