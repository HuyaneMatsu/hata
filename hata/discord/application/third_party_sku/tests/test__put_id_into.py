import vampytest

from ..fields import put_id_into


def test__put_id_into():
    """
    Tests whether ``put_id_into`` works as intended.
    """
    for input_, defaults, expected_output in (
        ('', False, {'id': ''}),
        ('a', False, {'id': 'a'}),
    ):
        data = put_id_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
