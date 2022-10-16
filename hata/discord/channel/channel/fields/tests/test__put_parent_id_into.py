import vampytest

from ..parent_id import put_parent_id_into


def test__put_parent_id_into():
    """
    Tests whether ``put_parent_id_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'parent_id': None}),
        (1, False, {'parent_id': '1'}),
    ):
        data = put_parent_id_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
