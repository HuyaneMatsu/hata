import vampytest

from ...client import Client
from ...core import BUILTIN_EMOJIS
from ...user import User

from ..reaction_mapping import ReactionMapping
from ..reaction_mapping_line import ReactionMappingLine


def test__ReactionMapping__emoji_count():
    """
    Tests whether ``ReactionMapping.emoji_count`` works as intended.
    """
    reaction_mapping = ReactionMapping({
        BUILTIN_EMOJIS['heart']: [None, None],
        BUILTIN_EMOJIS['eye']: [None, None],
    })
    
    vampytest.assert_eq(reaction_mapping.emoji_count, 2)


def test__ReactionMapping__total_count():
    """
    Tests whether ``ReactionMapping.total_count`` works as intended.
    """
    reaction_mapping = ReactionMapping({
        BUILTIN_EMOJIS['heart']: [None, None],
        BUILTIN_EMOJIS['eye']: [None, None],
    })
    
    vampytest.assert_eq(reaction_mapping.total_count, 4)


def test__ReactionMapping__clear():
    """
    Tests whether ``ReactionMapping.clear`` works as intended.
    """
    client = Client('token_202210010001')
    
    try:
        user_1 = User.precreate(202210010039)
        emoji_1 = BUILTIN_EMOJIS['heart']
        emoji_2 = BUILTIN_EMOJIS['eye']
        
        users_1 = [user_1, client]
        users_2 = [user_1, None]
        
        reaction_mapping = ReactionMapping({
            emoji_1: users_1,
            emoji_2: users_2,
        })
        
        reaction_mapping.clear()
        vampytest.assert_eq(reaction_mapping.total_count, len(users_1) + len(users_2))
        vampytest.assert_eq(reaction_mapping.fully_loaded, False)
        
        vampytest.assert_eq(
            reaction_mapping,
            ReactionMapping({
                emoji_1: [None if isinstance(user, User) else user for user in users_1],
                emoji_2: [None if isinstance(user, User) else user for user in users_2],
            }),
        )
        
        
    finally:
        client._delete()
        client = None


def test__ReactionMapping__add():
    """
    Tests whether ``ReactionMapping.add`` works as intended.
    """
    user_1 = User.precreate(202210010040)
    user_2 = User.precreate(202210010041)
    emoji_1 = BUILTIN_EMOJIS['heart']
    
    for original_value, expected_post_value, emoji, user in (
        (ReactionMapping(), ReactionMapping({emoji_1: [user_1]}), emoji_1, user_1),
        (ReactionMapping({emoji_1: [user_1]}), ReactionMapping({emoji_1: [user_1, user_2]}), emoji_1, user_2),
        (ReactionMapping({emoji_1: [user_1, user_2]}), ReactionMapping({emoji_1: [user_1, user_2]}), emoji_1, user_1),
    ):
        original_value.add(emoji, user)
        vampytest.assert_eq(original_value, expected_post_value)


def test__reactionMapping__remove():
    """
    Tests whether ``ReactionMapping.remove`` works as intended.
    """
    user_1 = User.precreate(202210010042)
    user_2 = User.precreate(202210010043)
    emoji_1 = BUILTIN_EMOJIS['heart']
    
    for original_value, expected_post_value, expected_output, emoji, user in (
        (ReactionMapping({emoji_1: [user_1, user_2]}), ReactionMapping({emoji_1: [user_1]}), True, emoji_1, user_2),
        (ReactionMapping({emoji_1: [user_1]}), ReactionMapping({emoji_1: [user_1]}), False, emoji_1, user_2),
        (ReactionMapping({emoji_1: [user_1]}), ReactionMapping(), True, emoji_1, user_1),
    ):
        output = original_value.remove(emoji, user)
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)
        
        vampytest.assert_eq(original_value, expected_post_value)
        

def test__ReactionMapping__remove_emoji():
    """
    Tests whether ``ReactionMapping.remove_emoji`` works as intended.
    """
    user_1 = User.precreate(202210010044)
    emoji_1 = BUILTIN_EMOJIS['heart']
    emoji_2 = BUILTIN_EMOJIS['eye']
    
    for original_value, expected_post_value, expected_fully_loaded, emoji, expected_output in (
        (ReactionMapping({emoji_1: [user_1]}), ReactionMapping(), True, emoji_1, [user_1]),
        (ReactionMapping({emoji_1: [user_1]}), ReactionMapping({emoji_1: [user_1]}), True, emoji_2, None),
        (ReactionMapping({emoji_1: [user_1, None]}), ReactionMapping({emoji_1: [user_1, None]}), False, emoji_2, None),
        (
            ReactionMapping({emoji_1: [None], emoji_2: [user_1]}),
            ReactionMapping({emoji_1: [None]}),
            False,
            emoji_2,
            [user_1]
        ),
    ):
        output = original_value.remove_emoji(emoji)
        vampytest.assert_instance(output, ReactionMappingLine, nullable = True)
        vampytest.assert_eq(output, expected_output)
        vampytest.assert_eq(original_value.fully_loaded, expected_fully_loaded)
        vampytest.assert_eq(original_value, expected_post_value)


def test__ReactionMapping__update_some_users():
    """
    Tests whether ``ReactionMapping._update_some_users`` works as intended.
    """
    user_1 = User.precreate(202210020000)
    user_2 = User.precreate(202210020001)
    user_3 = User.precreate(202210020002)
    emoji_1 = BUILTIN_EMOJIS['heart']
    
    reaction_mapping = ReactionMapping({emoji_1: [user_1, user_2, None, None],})
    
    reaction_mapping._update_some_users(emoji_1, [user_2, user_3])
    
    vampytest.assert_eq(reaction_mapping.total_count, 4)
    
    line = reaction_mapping[emoji_1]
    vampytest.assert_in(user_1, line)
    vampytest.assert_in(user_2, line)
    vampytest.assert_in(user_3, line)


def test__ReactionMapping__update_all_users():
    """
    Tests whether ``ReactionMapping._update_all_users`` works as intended.
    """
    user_1 = User.precreate(202210020003)
    user_2 = User.precreate(202210020004)
    user_3 = User.precreate(202210020005)
    emoji_1 = BUILTIN_EMOJIS['heart']
    
    reaction_mapping = ReactionMapping({emoji_1: [user_1, user_2, None, None],})
    
    reaction_mapping._update_all_users(emoji_1, [user_2, user_3])
    
    vampytest.assert_eq(reaction_mapping.total_count, 2)
    
    line = reaction_mapping[emoji_1]
    vampytest.assert_in(user_2, line)
    vampytest.assert_in(user_3, line)
