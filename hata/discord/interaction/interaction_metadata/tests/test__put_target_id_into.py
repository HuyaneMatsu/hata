import vampytest

from ..fields import put_target_id_into


def test__put_target_id_into():
    """
    Tests whether ``put_target_id_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'target_id': None}),
        (1, False, {'target_id': '1'}),
    ):
        data = put_target_id_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
