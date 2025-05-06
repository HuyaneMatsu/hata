import vampytest

from ..fields import put_parent_id


def test__put_parent_id():
    """
    Tests whether ``put_parent_id`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'parent_id': None}),
        (1, False, {'parent_id': '1'}),
    ):
        data = put_parent_id(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
