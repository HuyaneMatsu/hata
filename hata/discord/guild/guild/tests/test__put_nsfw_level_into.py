import vampytest

from ..fields import put_nsfw_level_into
from ..preinstanced import NsfwLevel


def test__put_nsfw_level_into():
    """
    Tests whether ``put_nsfw_level_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (NsfwLevel.safe, False, {'nsfw_level': NsfwLevel.safe.value}),
    ):
        data = put_nsfw_level_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
