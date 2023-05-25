import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..fields import put_emoji_into


def test__put_emoji_into():
    """
    Tests whether ``put_emoji_into`` is working as intended.
    """
    unicode_emoji = BUILTIN_EMOJIS['heart']
    custom_emoji = Emoji.precreate(202305240007, name = 'Yukari')
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'emoji_name': None}),
        (unicode_emoji, False, {'emoji_name': unicode_emoji.unicode}),
        (custom_emoji, False, {'emoji_name': custom_emoji.name, 'emoji_id': str(custom_emoji.id)}),
    ):
        data = put_emoji_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
