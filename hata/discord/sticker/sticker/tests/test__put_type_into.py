import vampytest

from ..fields import put_type_into
from ..preinstanced import StickerType


def test__put_type_into():
    """
    Tests whether ``put_type_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (StickerType.guild, False, {'type': StickerType.guild.value}),
    ):
        output = put_type_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
