import vampytest

from ..fields import put_sync_id_into


def test__put_sync_id_into():
    """
    Tests whether ``put_sync_id_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        ('a', False, {'sync_id': 'a'}),
    ):
        data = put_sync_id_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
