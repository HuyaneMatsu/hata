import vampytest

from ..fields import put_state_into


def test__put_state_into():
    """
    Tests whether ``put_state_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        ('a', False, {'state': 'a'}),
    ):
        data = put_state_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
