import vampytest

from ..fields import put_role_id


def test__put_role_id():
    """
    Tests whether ``put_role_id`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'role_id': None}),
        (1, False, {'role_id': '1'}),
    ):
        data = put_role_id(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
