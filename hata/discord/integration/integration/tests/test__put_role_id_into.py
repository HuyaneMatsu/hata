import vampytest

from ..fields import put_role_id_into


def test__put_role_id_into():
    """
    Tests whether ``put_role_id_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'role_id': None}),
        (1, False, {'role_id': '1'}),
    ):
        data = put_role_id_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
