import vampytest

from ..fields import validate_nsfw_level
from ..preinstanced import NsfwLevel


def test__validate_nsfw_level__0():
    """
    Tests whether `validate_nsfw_level` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (NsfwLevel.safe, NsfwLevel.safe),
        (NsfwLevel.safe.value, NsfwLevel.safe)
    ):
        output = validate_nsfw_level(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_nsfw_level__1():
    """
    Tests whether `validate_nsfw_level` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_nsfw_level(input_value)
