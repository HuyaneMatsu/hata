import vampytest

from ..fields import put_type_into
from ..preinstanced import ChannelType


def test__put_type_into():
    """
    Tests whether ``put_type_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (ChannelType.guild_text, False, {'type': ChannelType.guild_text.value}),
    ):
        data = put_type_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
