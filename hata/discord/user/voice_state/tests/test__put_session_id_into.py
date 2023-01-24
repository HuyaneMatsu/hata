import vampytest

from ..fields import put_session_id_into


def test__put_session_id_into():
    """
    Tests whether ``put_session_id_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        ('', False, {'session_id': ''}),
        ('a', False, {'session_id': 'a'}),
    ):
        data = put_session_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
