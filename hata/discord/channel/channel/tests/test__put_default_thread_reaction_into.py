import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..fields import put_default_thread_reaction_into


def test__put_default_thread_reaction_into():
    """
    Tests whether ``put_default_thread_reaction_into`` is working as intended.
    """
    unicode_emoji = BUILTIN_EMOJIS['heart']
    custom_emoji = Emoji.precreate(202209110004)
    
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'default_reaction_emoji': None}),
        (unicode_emoji, False, {'default_reaction_emoji': {'emoji_name': unicode_emoji.unicode}}),
        (custom_emoji, False, {'default_reaction_emoji': {'emoji_id': str(custom_emoji.id)}}),
    ):
        data = put_default_thread_reaction_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
