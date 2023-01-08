import vampytest

from ..emoji import Emoji
from ..utils import create_partial_emoji_data


def test__create_partial_emoji_data():
    """
    Tests whether ``create_partial_emoji_data`` works as intended.
    """
    emoji_id = 202301010078
    name = 'darling'
    animated = True
    
    emoji = Emoji.precreate(
        emoji_id,
        name = name,
        animated = animated,
    )
    
    expected_output = {
        'id': str(emoji_id),
        'name': name,
        'animated': animated,
    }
    
    vampytest.assert_eq(
        create_partial_emoji_data(emoji),
        expected_output,
    )
