import vampytest

from ..fields import put_session_id_into


def test__put_session_id_into():
    """
    Tests whether ``put_session_id_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        ('a', False, {'session_id': 'a'}),
    ):
        data = put_session_id_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
