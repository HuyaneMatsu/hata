import vampytest

from ....core import BUILTIN_EMOJIS
from ....user import User

from ...reaction import Reaction, ReactionType
from ...reaction_mapping_line import ReactionMappingLine

from ..reaction_mapping import ReactionMapping

from .test__ReactionMapping__constructor import _assert_fields_set


def test__ReactionMapping__copy__empty():
    """
    Tests whether ``ReactionMapping.copy`` works as intended.
    
    Case : empty.
    """
    reaction_mapping = ReactionMapping()
    
    copy = reaction_mapping.copy()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(reaction_mapping, copy)
    vampytest.assert_eq(reaction_mapping, copy)
    vampytest.assert_is(copy.lines, None)


def test__ReactionMapping__copy__filled():
    """
    Tests whether ``ReactionMapping.copy`` works as intended.
    
    Case : filled.
    """
    user_0 = User.precreate(202405120005)
    user_1 = User.precreate(202405120006)
    
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['eye']
    
    reaction_mapping = ReactionMapping(
        lines = {
            Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 2, users = [user_0, user_1]),
            Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 2, users = [user_0]),
        },
    )
    
    copy = reaction_mapping.copy()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(reaction_mapping, copy)
    vampytest.assert_eq(reaction_mapping, copy)
    
    vampytest.assert_is_not(copy.lines, None)


def test__ReactionMapping__emoji_count():
    """
    Tests whether ``ReactionMapping.emoji_count`` works as intended.
    """
    reaction_mapping = ReactionMapping(
        lines = {
            Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.standard): ReactionMappingLine(count = 1),
            Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.burst): ReactionMappingLine(count = 1),
            Reaction.from_fields(BUILTIN_EMOJIS['eye'], ReactionType.standard): ReactionMappingLine(count = 1),
        },
    )
    
    vampytest.assert_eq(reaction_mapping.emoji_count, 2)


def test__ReactionMapping__reaction_count():
    """
    Tests whether ``ReactionMapping.reaction_count`` works as intended.
    """
    reaction_mapping = ReactionMapping(
        lines = {
            Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.standard): ReactionMappingLine(count = 2),
            Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.burst): ReactionMappingLine(count = 2),
            Reaction.from_fields(BUILTIN_EMOJIS['eye'], ReactionType.standard): ReactionMappingLine(count = 2),
        },
    )
    
    vampytest.assert_eq(reaction_mapping.reaction_count, 3)


def test__ReactionMapping__total_count():
    """
    Tests whether ``ReactionMapping.total_count`` works as intended.
    """
    reaction_mapping = ReactionMapping(
        lines = {
            Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.standard): ReactionMappingLine(count = 2),
            Reaction.from_fields(BUILTIN_EMOJIS['eye'], ReactionType.standard): ReactionMappingLine(count = 2),
        }
    )
    
    vampytest.assert_eq(reaction_mapping.total_count, 4)


def test__ReactionMapping__clear__empty():
    """
    Tests whether ``ReactionMapping.clear`` works as intended.
    
    Case: empty.
    """
    reaction_mapping = ReactionMapping()
    
    reaction_mapping.clear()
    
    vampytest.assert_eq(reaction_mapping, ReactionMapping())
    vampytest.assert_is(reaction_mapping.lines, None)


def test__ReactionMapping__clear__filled():
    """
    Tests whether ``ReactionMapping.clear`` works as intended.
    
    Case: filled.
    """
    user_0 = User.precreate(202210010039)
    user_1 = User.precreate(202405120002)
    
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['eye']
    
    reaction_mapping = ReactionMapping(
        lines = {
            Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 2, users = [user_0, user_1]),
            Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 2, users = [user_0]),
        },
    )
    
    reaction_mapping.clear()
    
    vampytest.assert_eq(reaction_mapping, ReactionMapping())
    vampytest.assert_is_not(reaction_mapping.lines, None)


def _iter_options__add_reaction():
    user_0 = User.precreate(202210010040)
    user_1 = User.precreate(202210010041)
    emoji_0 = BUILTIN_EMOJIS['heart']
    
    yield (
        {},
        Reaction.from_fields(emoji_0, ReactionType.standard),
        user_0,
        (
            {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
            },
            True,
        ),
    )
    
    yield (
        {
            'lines': {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
            },
        },
        Reaction.from_fields(emoji_0, ReactionType.standard),
        user_1,
        (
            {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 2, users = [user_0, user_1]),
            },
            True,
        ),
    )
    
    yield (
        {
            'lines': {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 2, users = [user_0, user_1]),
            },
        },
        Reaction.from_fields(emoji_0, ReactionType.standard),
        user_0,
        (
            {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 2, users = [user_0, user_1]),
            },
            False,
        ),
    )
    
    yield (
        {
            'lines': {
                Reaction.from_fields(emoji_0, ReactionType.burst): ReactionMappingLine(count = 2, users = [user_0, user_1]),
            },
        },
        Reaction.from_fields(emoji_0, ReactionType.standard),
        user_0,
        (
            {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
                Reaction.from_fields(emoji_0, ReactionType.burst): ReactionMappingLine(count = 1, users = [user_0, user_1]),
            },
            True,
        )
    )


@vampytest._(vampytest.call_from(_iter_options__add_reaction()).returning_last())
def test__ReactionMapping__add(keyword_parameters, reaction, user):
    """
    Tests whether ``ReactionMapping._add_reaction`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the instance from.
    reaction : ``Reaction``
        Reaction to add.
    user : ``ClientUserBase``
        The user to add the reaction with.
    
    Returns
    -------
    output : `(None | dict<Reaction, ReactionMappingLine>, bool)`
    """
    reaction_mapping = ReactionMapping(**keyword_parameters).copy()
    output = reaction_mapping._add_reaction(reaction, user)
    vampytest.assert_instance(output, bool)
    return reaction_mapping.lines, output


def _iter_options__remove_reaction():
    user_0 = User.precreate(202210010042)
    user_1 = User.precreate(202210010043)
    emoji_0 = BUILTIN_EMOJIS['heart']
    
    yield (
        {
            'lines': {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 2, users = [user_0, user_1]),
            },
        },
        Reaction.from_fields(emoji_0, ReactionType.standard),
        user_1,
        (
            {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
            },
            True,
        ),
    )
    
    yield (
        {
            'lines': {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
            },
        },
        Reaction.from_fields(emoji_0, ReactionType.standard),
        user_1,
        (
            {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
            },
            False,
        ),
    )
    
    yield (
        {
            'lines': {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 2, users = [user_0]),
            },
        },
        Reaction.from_fields(emoji_0, ReactionType.standard),
        user_0,
        (
            {},
            True,
        ),
    )
    
    yield (
        {
            'lines': {
                Reaction.from_fields(emoji_0, ReactionType.burst): ReactionMappingLine(count = 1, users = [user_0]),
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
            },
        },
        Reaction.from_fields(emoji_0, ReactionType.standard),
        user_0,
        (
            {
                Reaction.from_fields(emoji_0, ReactionType.burst): ReactionMappingLine(count = 1, users = [user_0]),
            },
            True,
        ),
    )
    
    yield (
        {
            'lines': {
                Reaction.from_fields(emoji_0, ReactionType.burst): ReactionMappingLine(count = 1, users = [user_0]),
            },
        },
        Reaction.from_fields(emoji_0, ReactionType.standard),
        user_0,
        (
            {
                Reaction.from_fields(emoji_0, ReactionType.burst): ReactionMappingLine(count = 1, users = [user_0]),
            },
            False,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__remove_reaction()).returning_last())
def test__reactionMapping__remove(keyword_parameters, reaction, user):
    """
    Tests whether ``ReactionMapping.remove`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the instance from.
    reaction : ``Reaction``
        Reaction to remove.
    user : ``ClientUserBase``
        The user to remove the reaction with.
    
    Returns
    -------
    output : `(None | dict<Reaction, ReactionMappingLine>, bool)`
    """
    reaction_mapping = ReactionMapping(**keyword_parameters).copy()
    output = reaction_mapping._remove_reaction(reaction, user)
    vampytest.assert_instance(output, bool)
    return reaction_mapping.lines, output


def _iter_options___remove_reaction_emoji():
    user_0 = User.precreate(202210010044)
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['eye']

    yield (
        {
            'lines': {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
            },
        },
        emoji_0,
        (
            {},
            {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
            },
        ),
    )
    
    yield (
        {
            'lines': {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
            },
        },
        emoji_1,
        (
            {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
            },
            None,
        )
    )
    
    yield (
        {
            'lines': {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 2, users = [user_0]),
            },
        },
        emoji_1,
        (
            {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 2, users = [user_0]),
            },
            None,
        )
    )
    
    yield (
        {
            Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1),
            Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
        },
        emoji_1,
        (
            {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1),
            },
            {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
            },
        )
    )
    
    yield (
        {
            'lines': {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1),
                Reaction.from_fields(emoji_0, ReactionType.burst): ReactionMappingLine(count = 1, users = [user_0]),
                Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
            },
        },
        emoji_0,
        (
            {
                Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_0]),
            },
            {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 1),
                Reaction.from_fields(emoji_0, ReactionType.burst): ReactionMappingLine(count = 1, users = [user_0]),
            },
        )
    )


@vampytest._(vampytest.call_from(_iter_options___remove_reaction_emoji()).returning_last())
def test__ReactionMapping__remove_reaction_emoji(keyword_parameters, emoji):
    """
    Tests whether ``ReactionMapping._remove_reaction_emoji`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the instance from.
    emoji : ``Emoji``
        The emoji to remove.
    
    Returns
    -------
    output : `(None | dict<Reaction, ReactionMappingLine>, None | dict<Reaction, ReactionMappingLine>)`
    """
    reaction_mapping = ReactionMapping(**keyword_parameters).copy()
    output = reaction_mapping._remove_reaction_emoji(emoji)
    return reaction_mapping.lines, output


def test__ReactionMapping__fill_some_reactions():
    """
    Tests whether ``ReactionMapping._fill_some_reactions`` works as intended.
    """
    user_0 = User.precreate(202210020000)
    user_1 = User.precreate(202210020001)
    user_2 = User.precreate(202210020002)
    reaction_0 = Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.standard)
    
    reaction_mapping = ReactionMapping(
        lines = {
            reaction_0: ReactionMappingLine(count = 4, users = [user_0, user_1]),
        }
    )
    
    reaction_mapping._fill_some_reactions(reaction_0, [user_1, user_2])
    
    vampytest.assert_eq(
        reaction_mapping.lines,
        {
            reaction_0: ReactionMappingLine(count = 4, users = [user_0, user_1, user_2]),
        },
    )


def test__ReactionMapping__fill_all_reactions():
    """
    Tests whether ``ReactionMapping._fill_all_reactions`` works as intended.
    """
    user_0 = User.precreate(202210020003)
    user_1 = User.precreate(202210020004)
    user_2 = User.precreate(202210020005)
    reaction_0 = Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.standard)
    
    reaction_mapping = ReactionMapping(
        lines = {
            reaction_0: ReactionMappingLine(count = 4, users = [user_0, user_1]),
        },
    )
    
    reaction_mapping._fill_all_reactions(reaction_0, [user_1, user_2])
    
    vampytest.assert_eq(reaction_mapping.total_count, 2)
    
    vampytest.assert_eq(
        reaction_mapping.lines,
        {
            reaction_0: ReactionMappingLine(count = 2, users = [user_1, user_2]),
        },
    )


def _iter_options__get_or_create_line():
    emoji_0 = BUILTIN_EMOJIS['heart']
    
    reaction_0 = Reaction.from_fields(emoji_0, ReactionType.standard)
    reaction_1 = Reaction.from_fields(emoji_0, ReactionType.burst)
    
    yield (
        {},
        reaction_0,
        (
            {
                reaction_0: ReactionMappingLine(),
            },
            ReactionMappingLine(),
        ),
    )
    
    yield (
        {
            'lines': {
                reaction_0: ReactionMappingLine(count = 3),
            },
        },
        reaction_0,
        (
            {
                reaction_0: ReactionMappingLine(count = 3),
            },
            ReactionMappingLine(count = 3),
        ),
    )
    
    yield (
        {
            'lines': {
                reaction_0: ReactionMappingLine(count = 3),
            },
        },
        reaction_1,
        (
            {
                reaction_0: ReactionMappingLine(count = 3),
                reaction_1: ReactionMappingLine(),
            },
            ReactionMappingLine(),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__get_or_create_line()).returning_last())
def test__ReactionMapping__get_or_create_line(keyword_parameters, reaction):
    """
    Tests whether ``ReactionMapping._get_or_create_line`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    reaction : ``Reaction``
        Reaction or compatible to check.
    
    Returns
    -------
    output : `(None | dict<Reaction, ReactionMappingLine>, ReactionMappingLine)`
    """
    reaction_mapping = ReactionMapping(**keyword_parameters).copy()
    output = reaction_mapping._get_or_create_line(reaction)
    vampytest.assert_instance(output, ReactionMappingLine)
    return reaction_mapping.lines, output


def _iter_options__iter_reactions():
    emoji_0 = BUILTIN_EMOJIS['heart']
    
    reaction_0 = Reaction.from_fields(emoji_0, ReactionType.standard)
    reaction_1 = Reaction.from_fields(emoji_0, ReactionType.burst)
    
    yield (
        {},
        set()
    )
    
    yield (
        {
            'lines': {
                reaction_0: ReactionMappingLine(count = 3),
            },
        },
        {reaction_0}
    )
    
    yield (
        {
            'lines': {
                reaction_0: ReactionMappingLine(count = 3),
                reaction_1: ReactionMappingLine(count = 1),
            },
        },
        {reaction_0, reaction_1},
    )


@vampytest._(vampytest.call_from(_iter_options__iter_reactions()).returning_last())
def test__ReactionMapping__iter_reactions(keyword_parameters):
    """
    Tests whether ``ReactionMapping.iter_reactions`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `set<Reaction>`
    """
    reaction_mapping = ReactionMapping(**keyword_parameters)
    return {*reaction_mapping.iter_reactions()}


def _iter_options__iter_lines():
    emoji_0 = BUILTIN_EMOJIS['heart']
    
    reaction_0 = Reaction.from_fields(emoji_0, ReactionType.standard)
    reaction_1 = Reaction.from_fields(emoji_0, ReactionType.burst)
    
    yield (
        {},
        set()
    )
    
    yield (
        {
            'lines': {
                reaction_0: ReactionMappingLine(count = 3),
            },
        },
        {ReactionMappingLine(count = 3)}
    )
    
    yield (
        {
            'lines': {
                reaction_0: ReactionMappingLine(count = 3),
                reaction_1: ReactionMappingLine(count = 1),
            },
        },
        {ReactionMappingLine(count = 3), ReactionMappingLine(count = 1)},
    )


@vampytest._(vampytest.call_from(_iter_options__iter_lines()).returning_last())
def test__ReactionMapping__iter_lines(keyword_parameters):
    """
    Tests whether ``ReactionMapping.iter_lines`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `set<ReactionMappingLine>`
    """
    reaction_mapping = ReactionMapping(**keyword_parameters)
    return {*reaction_mapping.iter_lines()}


def _iter_options__iter_items():
    emoji_0 = BUILTIN_EMOJIS['heart']
    
    reaction_0 = Reaction.from_fields(emoji_0, ReactionType.standard)
    reaction_1 = Reaction.from_fields(emoji_0, ReactionType.burst)
    
    yield (
        {},
        set()
    )
    
    yield (
        {
            'items': {
                reaction_0: ReactionMappingLine(count = 3),
            },
        },
        {(reaction_0, ReactionMappingLine(count = 3))}
    )
    
    yield (
        {
            'items': {
                reaction_0: ReactionMappingLine(count = 3),
                reaction_1: ReactionMappingLine(count = 1),
            },
        },
        {(reaction_0, ReactionMappingLine(count = 3)), (reaction_1, ReactionMappingLine(count = 1))},
    )


@vampytest._(vampytest.call_from(_iter_options__iter_items()).returning_last())
def test__ReactionMapping__iter_items(keyword_parameters):
    """
    Tests whether ``ReactionMapping.iter_items`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `set<(Reaction, ReactionMappingLine)>`
    """
    reaction_mapping = ReactionMapping(**keyword_parameters)
    return {*reaction_mapping.iter_items()}
