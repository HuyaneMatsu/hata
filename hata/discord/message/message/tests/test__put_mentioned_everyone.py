import vampytest

from ..fields import put_mentioned_everyone


def test__put_mentioned_everyone():
    """
    Tests whether ``put_mentioned_everyone`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'mention_everyone': False}),
        (True, False, {'mention_everyone': True}),
    ):
        data = put_mentioned_everyone(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
