import vampytest

from ..fields import put_format
from ..preinstanced import StickerFormat


def test__put_format():
    """
    Tests whether ``put_format`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (StickerFormat.png, False, {'format_type': StickerFormat.png.value}),
    ):
        output = put_format(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
