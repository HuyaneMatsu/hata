import vampytest

from ..fields import put_target_id


def test__put_target_id():
    """
    Tests whether ``put_target_id`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'target_id': None}),
        (1, False, {'target_id': '1'}),
    ):
        data = put_target_id(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
