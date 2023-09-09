import vampytest

from ....client import Client
from ....core import BUILTIN_EMOJIS
from ....user import User

from ...reaction import Reaction, ReactionType

from ..reaction_mapping import ReactionMapping
from ..reaction_mapping_line import ReactionMappingLine


def test__ReactionMapping__emoji_count():
    """
    Tests whether ``ReactionMapping.emoji_count`` works as intended.
    """
    reaction_mapping = ReactionMapping({
        Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.standard): [None],
        Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.burst): [None],
        Reaction.from_fields(BUILTIN_EMOJIS['eye'], ReactionType.standard): [None],
    })
    
    vampytest.assert_eq(reaction_mapping.emoji_count, 2)


def test__ReactionMapping__reaction_count():
    """
    Tests whether ``ReactionMapping.reaction_count`` works as intended.
    """
    reaction_mapping = ReactionMapping({
        Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.standard): [None, None],
        Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.burst): [None, None],
        Reaction.from_fields(BUILTIN_EMOJIS['eye'], ReactionType.standard): [None, None],
    })
    
    vampytest.assert_eq(reaction_mapping.reaction_count, 3)


def test__ReactionMapping__total_count():
    """
    Tests whether ``ReactionMapping.total_count`` works as intended.
    """
    reaction_mapping = ReactionMapping({
        Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.standard): [None, None],
        Reaction.from_fields(BUILTIN_EMOJIS['eye'], ReactionType.standard): [None, None],
    })
    
    vampytest.assert_eq(reaction_mapping.total_count, 4)


def test__ReactionMapping__clear():
    """
    Tests whether ``ReactionMapping.clear`` works as intended.
    """
    client = Client('token_202210010001')
    
    try:
        user_0 = User.precreate(202210010039)
        emoji_0 = BUILTIN_EMOJIS['heart']
        emoji_1 = BUILTIN_EMOJIS['eye']
        
        users_1 = [user_0, client]
        users_2 = [user_0, None]
        
        reaction_mapping = ReactionMapping({
            Reaction.from_fields(emoji_0, ReactionType.standard): users_1,
            Reaction.from_fields(emoji_1, ReactionType.standard): users_2,
        })
        
        reaction_mapping.clear()
        vampytest.assert_eq(reaction_mapping.total_count, len(users_1) + len(users_2))
        vampytest.assert_eq(reaction_mapping.fully_loaded, False)
        
        vampytest.assert_eq(
            reaction_mapping,
            ReactionMapping({
                Reaction.from_fields(emoji_0, ReactionType.standard): [
                    None if isinstance(user, User) else user for user in users_1
                ],
                Reaction.from_fields(emoji_1, ReactionType.standard): [
                    None if isinstance(user, User) else user for user in users_2
                ],
            }),
        )
        
        
    finally:
        client._delete()
        client = None


def _iter_options__add():
    user_0 = User.precreate(202210010040)
    user_2 = User.precreate(202210010041)
    emoji_0 = BUILTIN_EMOJIS['heart']
    
    yield (
        ReactionMapping(),
        Reaction.from_fields(emoji_0, ReactionType.standard),
        user_0,
        ReactionMapping({
            Reaction.from_fields(emoji_0, ReactionType.standard): [user_0],
        }),
    )
    yield (
        ReactionMapping({
            Reaction.from_fields(emoji_0, ReactionType.standard): [user_0],
        }),
        Reaction.from_fields(emoji_0, ReactionType.standard),
        user_2,
        ReactionMapping({
            Reaction.from_fields(emoji_0, ReactionType.standard): [user_0, user_2],
        }),
    )
    yield (
        ReactionMapping({
            Reaction.from_fields(emoji_0, ReactionType.standard): [user_0, user_2],
        }),
        Reaction.from_fields(emoji_0, ReactionType.standard),
        user_0,
        ReactionMapping({
            Reaction.from_fields(emoji_0, ReactionType.standard): [user_0, user_2],
        }),
    )
    yield (
        ReactionMapping({
            Reaction.from_fields(emoji_0, ReactionType.burst): [user_0, user_2],
        }),
        Reaction.from_fields(emoji_0, ReactionType.standard),
        user_0,
        ReactionMapping({
            Reaction.from_fields(emoji_0, ReactionType.standard): [user_0],
            Reaction.from_fields(emoji_0, ReactionType.burst): [user_0, user_2],
        }),
    )


@vampytest._(vampytest.call_from(_iter_options__add()).returning_last())
def test__ReactionMapping__add(input_value, reaction, user):
    """
    Tests whether ``ReactionMapping.add`` works as intended.
    
    Parameters
    ----------
    input_value : ``ReactionMapping``
        Reaction mapping to operate on.
    reaction : ``Reaction``
        Reaction to add.
    user : ``ClientUserBase``
        The user to add the reaction with.
    
    Returns
    -------
    output : `(bool, ReactionMapping)`
    """
    value = input_value.copy()
    value.add(reaction, user)
    return value


def _iter_options__remove():
    user_0 = User.precreate(202210010042)
    user_2 = User.precreate(202210010043)
    emoji_0 = BUILTIN_EMOJIS['heart']
    
    yield (
        ReactionMapping({
            Reaction.from_fields(emoji_0, ReactionType.standard): [user_0, user_2],
        }),
        Reaction.from_fields(emoji_0, ReactionType.standard),
        user_2,
        (
            True,
            ReactionMapping({
                Reaction.from_fields(emoji_0, ReactionType.standard): [user_0],
            }),
        ),
    )
    yield (
        ReactionMapping({
            Reaction.from_fields(emoji_0, ReactionType.standard): [user_0],
        }),
        Reaction.from_fields(emoji_0, ReactionType.standard),
        user_2,
        (
            False,
            ReactionMapping({
                Reaction.from_fields(emoji_0, ReactionType.standard): [user_0],
            }),
        ),
    )
    yield (
        ReactionMapping({
            Reaction.from_fields(emoji_0, ReactionType.standard): [user_0],
        }),
        Reaction.from_fields(emoji_0, ReactionType.standard),
        user_0,
        (
            True,
            ReactionMapping(),
        ),
    )
    yield (
        ReactionMapping({
            Reaction.from_fields(emoji_0, ReactionType.burst): [user_0],
            Reaction.from_fields(emoji_0, ReactionType.standard): [user_0],
        }),
        Reaction.from_fields(emoji_0, ReactionType.standard),
        user_0,
        (
            True,
            ReactionMapping({
                Reaction.from_fields(emoji_0, ReactionType.burst): [user_0],
            }),
        ),
    )
    yield (
        ReactionMapping({
            Reaction.from_fields(emoji_0, ReactionType.burst): [user_0],
        }),
        Reaction.from_fields(emoji_0, ReactionType.standard),
        user_0,
        (
            False,
            ReactionMapping({
                Reaction.from_fields(emoji_0, ReactionType.burst): [user_0],
            }),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__remove()).returning_last())
def test__reactionMapping__remove(input_value, reaction, user):
    """
    Tests whether ``ReactionMapping.remove`` works as intended.
    
    Parameters
    ----------
    input_value : ``ReactionMapping``
        Reaction mapping to operate on.
    reaction : ``Reaction``
        Reaction to remove.
    user : ``ClientUserBase``
        The user to remove the reaction with.
    
    Returns
    -------
    output : `(bool, ReactionMapping)`
    """
    value = input_value.copy()
    output = value.remove(reaction, user)
    vampytest.assert_instance(output, bool)
    return output, value
        

def _iter_options__remove_emoji():
    user_0 = User.precreate(202210010044)
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['eye']

    yield (
        ReactionMapping({
            Reaction.from_fields(emoji_0, ReactionType.standard): [user_0],
        }),
        emoji_0,
        (
            {
                Reaction.from_fields(emoji_0, ReactionType.standard): [user_0],
            },
            ReactionMapping(),
            True,
        ),
    )
    yield (
        ReactionMapping({
            Reaction.from_fields(emoji_0, ReactionType.standard): [user_0],
        }),
        emoji_1,
        (
            None,
            ReactionMapping({
                Reaction.from_fields(emoji_0, ReactionType.standard): [user_0],
            }),
            True,
        )
    )
    yield (
        ReactionMapping({
            Reaction.from_fields(emoji_0, ReactionType.standard): [user_0, None],
        }),
        emoji_1,
        (
            None,
            ReactionMapping({
                Reaction.from_fields(emoji_0, ReactionType.standard): [user_0, None],
            }),
            False,
        )
    )
    yield (
        ReactionMapping({
            Reaction.from_fields(emoji_0, ReactionType.standard): [None],
            Reaction.from_fields(emoji_1, ReactionType.standard): [user_0],
        }),
        emoji_1,
        (
            {
                Reaction.from_fields(emoji_0, ReactionType.standard): [user_0],
            },
            ReactionMapping({
                Reaction.from_fields(emoji_0, ReactionType.standard): [None],
            }),
            False,
        )
    )
    yield (
        ReactionMapping({
            Reaction.from_fields(emoji_0, ReactionType.standard): [None],
            Reaction.from_fields(emoji_0, ReactionType.burst): [user_0],
            Reaction.from_fields(emoji_1, ReactionType.standard): [user_0],
        }),
        emoji_0,
        (
            {
                Reaction.from_fields(emoji_0, ReactionType.standard): [None],
                Reaction.from_fields(emoji_0, ReactionType.burst): [user_0],
            },
            ReactionMapping({
                Reaction.from_fields(emoji_1, ReactionType.standard): [user_0],
            }),
            True,
        )
    )


def test__ReactionMapping__remove_emoji(input_value, emoji):
    """
    Tests whether ``ReactionMapping.remove_emoji`` works as intended.
    
    Parameters
    ----------
    input_value : ``ReactionMapping``
        Reaction mapping to operate on.
    emoji : ``Emoji``
        The emoji to remove.
    
    Returns
    -------
    output : `(None | dict<Reaction, ReactionMappingLine>, ReactionMapping, bool)`
    """
    value = input_value.copy()
    output = value.remove_emoji(emoji)
    return output, value, value.fully_loaded


def test__ReactionMapping__update_some_users():
    """
    Tests whether ``ReactionMapping._update_some_users`` works as intended.
    """
    user_0 = User.precreate(202210020000)
    user_2 = User.precreate(202210020001)
    user_3 = User.precreate(202210020002)
    emoji_0 = BUILTIN_EMOJIS['heart']
    
    reaction_mapping = ReactionMapping({emoji_0: [user_0, user_2, None, None],})
    
    reaction_mapping._update_some_users(emoji_0, [user_2, user_3])
    
    vampytest.assert_eq(reaction_mapping.total_count, 4)
    
    line = reaction_mapping[emoji_0]
    vampytest.assert_in(user_0, line)
    vampytest.assert_in(user_2, line)
    vampytest.assert_in(user_3, line)


def test__ReactionMapping__update_all_users():
    """
    Tests whether ``ReactionMapping._update_all_users`` works as intended.
    """
    user_0 = User.precreate(202210020003)
    user_2 = User.precreate(202210020004)
    user_3 = User.precreate(202210020005)
    emoji_0 = BUILTIN_EMOJIS['heart']
    
    reaction_mapping = ReactionMapping({emoji_0: [user_0, user_2, None, None],})
    
    reaction_mapping._update_all_users(emoji_0, [user_2, user_3])
    
    vampytest.assert_eq(reaction_mapping.total_count, 2)
    
    line = reaction_mapping[emoji_0]
    vampytest.assert_in(user_2, line)
    vampytest.assert_in(user_3, line)
