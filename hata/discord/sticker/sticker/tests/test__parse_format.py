import vampytest

from ..fields import parse_format
from ..preinstanced import StickerFormat


def test__parse_format():
    """
    Tests whether ``parse_format`` works as intended.
    """
    for input_data, expected_output in (
        ({}, StickerFormat.none),
        ({'format_type': StickerFormat.png.value}, StickerFormat.png),
    ):
        output = parse_format(input_data)
        vampytest.assert_is(output, expected_output)
