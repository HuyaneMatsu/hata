import vampytest

from ..fields import put_nsfw_into


def test__put_nsfw_into():
    """
    Tests whether ``put_nsfw_into`` works as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'nsfw': False}),
        (True, False, {'nsfw': True}),
    ):
        data = put_nsfw_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
