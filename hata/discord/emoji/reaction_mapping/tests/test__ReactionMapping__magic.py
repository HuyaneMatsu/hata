import vampytest

from ....core import BUILTIN_EMOJIS
from ....user import User

from ...reaction import Reaction, ReactionType
from ...reaction_mapping_line import ReactionMappingLine

from ..reaction_mapping import ReactionMapping


def _iter_options__bool():
    yield (
        {},
        False,
    )
    
    yield (
        {
            'lines': {
                Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.standard): ReactionMappingLine(count = 1),
            }
        },
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__ReactionMapping__bool(keyword_parameters):
    """
    Tests whether ``ReactionMapping.__bool__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    reaction_mapping = ReactionMapping(**keyword_parameters)
    output = bool(reaction_mapping)
    vampytest.assert_instance(output, bool)
    return output


def test__ReactionMapping__repr():
    """
    tests whether ``ReactionMapping.__repr__`` works as intended.
    """
    reaction_mapping = ReactionMapping(
        lines = {
            Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.standard): ReactionMappingLine(count = 1),
        }
    )
    vampytest.assert_instance(repr(reaction_mapping), str)


def _iter_options__len():
    yield (
        {},
        0,
    )
    
    yield (
        {
            'lines': {
                Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.standard): ReactionMappingLine(count = 3),
            },
        },
        1,
    )
    
    yield (
        {
            'lines': {
                Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.standard): ReactionMappingLine(count = 3),
                Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.burst): ReactionMappingLine(count = 1),
            },
        },
        2,
    )
    
    yield (
        {
            'lines': {
                Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.standard): ReactionMappingLine(count = 3),
                Reaction.from_fields(BUILTIN_EMOJIS['x'], ReactionType.standard): ReactionMappingLine(count = 1),
            },
        },
        2,
    )


@vampytest._(vampytest.call_from(_iter_options__len()).returning_last())
def test__ReactionMapping__len(keyword_parameters):
    """
    Tests whether ``ReactionMapping.__len__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `int`
    """
    reaction_mapping = ReactionMapping(**keyword_parameters)
    output = len(reaction_mapping)
    vampytest.assert_instance(output, int)
    return output


def _iter_options__eq__same_type():
    emoji_0 = BUILTIN_EMOJIS['x']
    emoji_1 = BUILTIN_EMOJIS['heart']
    user_0 = User.precreate(202210010037)
    
    yield (
        {},
        {},
        True,
    )
    
    yield (
        {
            'lines': {
                Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 1),
            },
        },
        {
            'lines': {
                Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 1),
            },
        },
        True,
    )
    
    yield (
        {
            'lines': {
                Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 1),
            },
        },
        {
            'lines': {
                Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 2),
            },
        },
        False,
    )
    
    yield (
        {},
        {
            'lines': {
                Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 1),
            },
        },
        False,
    )

    yield (
        {
            'lines': {
                Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
            },
        },
        {
            'lines': {
                Reaction.from_fields(emoji_1, ReactionType.burst): ReactionMappingLine(count = 1, users = [user_0]),
            },
        },
        False,
    )
    
    yield (
        {
            'lines': {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
            },
        },
        {
            'lines': {
                Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
            }
        },
        False,
    )
    
    yield (
        {
            'lines': {
                Reaction.from_fields(emoji_0, ReactionType.burst): ReactionMappingLine(count = 1, users = [user_0]),
            },
        },
        {
            'lines': {
                Reaction.from_fields(emoji_1, ReactionType.burst): ReactionMappingLine(count = 1, users = [user_0]),
            },
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__ReactionMapping__eq__same_type(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ReactionMapping.__eq__`` works as intended.
    
    Case: Same type.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    reaction_mapping_0 = ReactionMapping(**keyword_parameters_0)
    reaction_mapping_1 = ReactionMapping(**keyword_parameters_1)
    
    output = reaction_mapping_0 == reaction_mapping_1
    vampytest.assert_instance(output, bool)
    return output


def test__ReactionMapping__eq__different_type():
    """
    Tests whether ``ReactionMapping.__eq__`` works as intended.
    
    Case: Different type.
    """
    reaction_mapping = ReactionMapping()
    
    output = reaction_mapping == object()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__ReactionMapping__eq__cleared():
    """
    Tests whether ``ReactionMapping.__eq__`` works as intended.
    
    Case: Cleared
    """
    reaction_mapping = ReactionMapping(
        lines = {
            Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.burst): ReactionMappingLine(count = 1),
        },
    )
    reaction_mapping.clear()
    
    output = reaction_mapping == ReactionMapping()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__ReactionMapping__hash():
    """
    Tests whether ``ReactionMapping.__hash__`` works as intended.
    """
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['x']
    
    user_0 = User.precreate(202305040096)
    user_1 = User.precreate(202305040097)
    
    mapping = ReactionMapping(
        lines = {
            Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 3, users = [user_0]),
            Reaction.from_fields(emoji_0, ReactionType.burst): ReactionMappingLine(count = 3, users = [user_0]),
            Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_1]),
        },
    )
    
    vampytest.assert_instance(hash(mapping), int)


def _iter_options__contains():
    emoji_0 = BUILTIN_EMOJIS['heart']
    
    reaction_0 = Reaction.from_fields(emoji_0, ReactionType.standard)
    reaction_1 = Reaction.from_fields(emoji_0, ReactionType.burst)
    
    yield (
        {},
        reaction_0,
        False,
    )
    
    yield (
        {
            'lines': {
                reaction_0: ReactionMappingLine(count = 3),
            },
        },
        reaction_0,
        True,
    )
    
    yield (
        {
            'lines': {
                reaction_0: ReactionMappingLine(count = 3),
            },
        },
        reaction_1,
        False,
    )
    
    yield (
        {
            'lines': {
                reaction_0: ReactionMappingLine(count = 3),
            },
        },
        emoji_0,
        True,
    )
    
    yield (
        {
            'lines': {
                reaction_1: ReactionMappingLine(count = 3),
            },
        },
        emoji_0,
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__contains()).returning_last())
def test__ReactionMapping__contains(keyword_parameters, reaction):
    """
    Tests whether ``ReactionMapping.__contains__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    reaction : ``Emoji``, ``Reaction``
        Reaction or compatible to check.
    
    Returns
    -------
    output : `bool`
    """
    reaction_mapping = ReactionMapping(**keyword_parameters)
    output = reaction in reaction_mapping
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__getitem():
    emoji_0 = BUILTIN_EMOJIS['heart']
    
    reaction_0 = Reaction.from_fields(emoji_0, ReactionType.standard)
    reaction_1 = Reaction.from_fields(emoji_0, ReactionType.burst)
    
    yield (
        {},
        reaction_0,
        None,
    )
    
    yield (
        {
            'lines': {
                reaction_0: ReactionMappingLine(count = 3),
            },
        },
        reaction_0,
        ReactionMappingLine(count = 3),
    )
    
    yield (
        {
            'lines': {
                reaction_0: ReactionMappingLine(count = 3),
            },
        },
        reaction_1,
        None,
    )
    
    yield (
        {
            'lines': {
                reaction_0: ReactionMappingLine(count = 3),
            },
        },
        emoji_0,
        ReactionMappingLine(count = 3),
    )
    
    yield (
        {
            'lines': {
                reaction_1: ReactionMappingLine(count = 3),
            },
        },
        emoji_0,
        None,
    )


@vampytest._(vampytest.call_from(_iter_options__getitem()).returning_last())
def test__ReactionMapping__getitem(keyword_parameters, reaction):
    """
    Tests whether ``ReactionMapping.__getitem__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    reaction : ``Emoji``, ``Reaction``
        Reaction or compatible to check.
    
    Returns
    -------
    output : `None | ReactionMappingLine`
    """
    reaction_mapping = ReactionMapping(**keyword_parameters)
    output = reaction_mapping[reaction]
    vampytest.assert_instance(output, ReactionMappingLine, nullable = True)
    return output
