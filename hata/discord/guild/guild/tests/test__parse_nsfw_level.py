import vampytest

from ..fields import parse_nsfw_level
from ..preinstanced import NsfwLevel


def test__parse_nsfw_level():
    """
    Tests whether ``parse_nsfw_level`` works as intended.
    """
    for input_data, expected_output in (
        ({}, NsfwLevel.none),
        ({'nsfw_level': NsfwLevel.safe.value}, NsfwLevel.safe),
    ):
        output = parse_nsfw_level(input_data)
        vampytest.assert_eq(output, expected_output)
