import vampytest

from ..fields import put_join_into


def test__put_join_into():
    """
    Tests whether ``put_join_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        ('a', False, {'join': 'a'}),
    ):
        data = put_join_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
