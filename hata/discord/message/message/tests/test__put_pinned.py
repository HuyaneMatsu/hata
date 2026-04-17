import vampytest

from ..fields import put_pinned


def test__put_pinned():
    """
    Tests whether ``put_pinned`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'pinned': False}),
        (True, False, {'pinned': True}),
    ):
        data = put_pinned(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
