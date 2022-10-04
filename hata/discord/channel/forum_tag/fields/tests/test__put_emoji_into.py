import vampytest

from .....core import BUILTIN_EMOJIS
from .....emoji import Emoji

from ..emoji import put_emoji_into


def test__put_emoji_into():
    """
    Tests whether ``put_emoji_into`` is working as intended.
    """
    unicode_emoji = BUILTIN_EMOJIS['heart']
    custom_emoji = Emoji.precreate(202210040001)
    
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'emoji_name': None}),
        (unicode_emoji, False, {'emoji_name': unicode_emoji.unicode}),
        (custom_emoji, False, {'emoji_id': str(custom_emoji.id)}),
    ):
        data = put_emoji_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
