import vampytest

from ..fields import put_pinned_into


def test__put_pinned_into():
    """
    Tests whether ``put_pinned_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'pinned': False}),
        (True, False, {'pinned': True}),
    ):
        data = put_pinned_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
