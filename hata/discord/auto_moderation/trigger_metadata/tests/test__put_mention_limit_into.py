import vampytest

from ..fields import put_mention_limit_into


def test__put_mention_limit_into():
    """
    Tests whether ``put_mention_limit_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (0, False, {'mention_total_limit': 0}),
        (1, False, {'mention_total_limit': 1}),
    ):
        data = put_mention_limit_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
