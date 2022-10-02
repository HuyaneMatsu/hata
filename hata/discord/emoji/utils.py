__all__ = (
    'create_partial_emoji_data', 'create_partial_emoji_from_data', 'create_partial_emoji_from_id',
    'create_emoji_from_exclusive_data', 'create_unicode_emoji', 'parse_all_emojis', 'parse_all_emojis_ordered',
    'parse_custom_emojis', 'parse_custom_emojis_ordered', 'parse_emoji', 'parse_reaction',
    'put_exclusive_emoji_data_into', 'put_partial_emoji_data_into', 'merge_update_reaction_mapping'
)

import warnings

from scarletio import export

from ..core import BUILTIN_EMOJIS, EMOJIS, UNICODE_TO_EMOJI
from ..utils import EMOJI_RP, REACTION_RP

from .emoji import Emoji
from .emoji_all_pattern import EMOJI_ALL_RP
from .unicode_type import Unicode, VARIATION_SELECTOR_16_POSTFIX


VARIATION_SELECTOR_16_POSTFIX_WITH_COLON = VARIATION_SELECTOR_16_POSTFIX + ':'


def _create_new_unicode(unicode_string):
    """
    Creates a new emoji from the given `unicode_string`.
    
    Parameters
    ----------
    unicode_string : `str`
        Unicode string to create emoji from.
    
    Returns
    -------
    emoji : ``Emoji``
    """
    unicode_bytes = unicode_string.encode()
    
    warnings.warn(
        f'\nUndefined emoji : {unicode_bytes!r}\nPlease open an issue with this message.',
        RuntimeWarning,
    )
    
    return Emoji._create_unicode(Unicode('', unicode_bytes, False, None, None), False)


@export
def create_partial_emoji_from_data(data):
    """
    Creates an emoji from partial emoji data sent by Discord.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Partial emoji data.
    
    Returns
    -------
    emoji : `None`, ``Emoji``
    """
    try:
        emoji_name = data['emoji_name']
    except KeyError:
        emoji_name = data['name']
        emoji_id = data.get('id', None)
        emoji_animated = data.get('animated', False)
    else:
        emoji_id = data.get('emoji_id', None)
        emoji_animated = data.get('emoji_animated', False)
    
    if emoji_name is None:
        return None
    
    if emoji_id is None:
        try:
            emoji = UNICODE_TO_EMOJI[emoji_name]
        except KeyError:
            emoji = _create_new_unicode(emoji_name)
    
    else:
        # name can change
        if emoji_name is None:
            emoji_name = ''
            
        emoji = Emoji._create_partial(int(emoji_id), emoji_name, emoji_animated)
    
    return emoji


def create_partial_emoji_from_id(emoji_id):
    """
    Creates a partial emoji from the given id.
    
    Parameters
    ----------
    emoji_id : `int`
        The emoji's identifier.
    
    Returns
    -------
    emoji : ``Emoji``
    """
    try:
        emoji = EMOJIS[emoji_id]
    except KeyError:
        emoji = Emoji._create_empty(emoji_id)
        EMOJIS[emoji_id] = emoji
    
    return emoji


@export
def create_partial_emoji_data(emoji):
    """
    Creates partial emoji data form the given emoji.
    
    Parameters
    ----------
    emoji : ``Emoji``
        The emoji to serialize.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
        The serialized emoji data.
    """
    emoji_data = {}
    unicode = emoji.unicode
    if unicode is None:
        emoji_data['id'] = str(emoji.id)
        emoji_data['name'] = emoji.name
        
        if emoji.animated:
            emoji_data['animated'] = True
    else:
        emoji_data['name'] = unicode
    
    return emoji_data


def put_partial_emoji_data_into(emoji, data):
    """
    Familiar to ``create_partial_emoji_data``, but instead of creating a standalone emoji data, uses the `emoji_`
    prefix field form to add it to an already defined dictionary.
    
    Parameters
    ----------
    emoji : `None`, ``Emoji``
        The emoji to serialize.
    data : `dict` of (`str`, `Any`) items
        The data to put the emoji fields into.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if (emoji is None):
        # Require at least the `emoji_name` field.
        data['emoji_name'] = None
    
    else:
        unicode = emoji.unicode
        if unicode is None:
            data['emoji_id'] = str(emoji.id)
            data['emoji_name'] = emoji.name
            
            if emoji.animated:
                data['emoji_animated'] = True
        else:
            data['emoji_name'] = unicode
        
    return data


def create_emoji_from_exclusive_data(data):
    """
    Creates partial emoji from the given exclusive emoji data.
    
    Exclusive means, that we expect exactly `1` emoji field to be set.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Partial emoji data.
    
    Returns
    -------
    emoji : `None`, ``Emoji``
    """
    emoji_name = data.get('emoji_name', None)
    emoji_id = data.get('emoji_id', None)
    
    if (emoji_name is not None):
        try:
            emoji = UNICODE_TO_EMOJI[emoji_name]
        except KeyError:
            emoji = _create_new_unicode(emoji_name)
    
    elif (emoji_id is not None):
        emoji = create_partial_emoji_from_id(int(emoji_id))
    
    else:
        emoji = None
    
    return emoji


def put_exclusive_emoji_data_into(emoji, data):
    """
    The reversed function of ``create_emoji_from_exclusive_data``.
    
    Parameters
    ----------
    emoji : `None`, ``Emoji``
        The emoji to serialize.
    data : `dict` of (`str`, `Any`) items
        The data to put the emoji fields into.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if (emoji is None):
        # Require at least the `emoji_name` field.
        data['emoji_name'] = None
    
    else:
        unicode = emoji.unicode
        if unicode is None:
            data['emoji_id'] = str(emoji.id)
        
        else:
            data['emoji_name'] = unicode
    
    return data


def parse_emoji(text):
    """
    Tries to parse out an ``Emoji`` from the inputted text. This emoji can be custom and unicode emoji as well.
    
    If the parsing fails the function returns `None`.
    
    Parameters
    ----------
    text : `str`
        The text to parse emojis from.
    
    Returns
    -------
    emoji : `None`, ``Emoji``
    """
    parsed = EMOJI_RP.fullmatch(text)
    if (parsed is not None):
        animated, name, emoji_id = parsed.groups()
        animated = (animated is not None)
        emoji_id = int(emoji_id)
        return Emoji._create_partial(emoji_id, name, animated)
        
    try:
        return UNICODE_TO_EMOJI[text]
    except KeyError:
        pass
    
    if text.startswith(':') and text.endswith(':') and not text.endswith(VARIATION_SELECTOR_16_POSTFIX_WITH_COLON):
        try:
            return BUILTIN_EMOJIS[text[1:-1]]
        except KeyError:
            pass
    
    return None


def _iter_parse_custom_emojis(text):
    """
    Iterates over all the custom emojis in the text as they appear.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    text : `str`
        The text to parse.
    
    Yields
    ------
    emoji : ``Emoji``
    """
    for groups in EMOJI_RP.findall(text):
        
        animated, name, emoji_id = groups
        animated = (True if animated else False)
        emoji_id = int(emoji_id)
        
        yield Emoji._create_partial(emoji_id, name, animated)


def _iter_parse_all_emojis(text):
    """
    Iterates over all emojis in the text as they appear.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    text : `str`
        The text to parse.
    
    Yields
    ------
    emoji : ``Emoji``
    """
    for groups in EMOJI_ALL_RP.findall(text):
        
        unicode_value, unicode_name, custom_animated, custom_name, custom_emoji_id = groups
        if unicode_value:
            yield UNICODE_TO_EMOJI[unicode_value]
            continue
        
        if unicode_name:
            yield BUILTIN_EMOJIS[unicode_name]
            continue
        
        yield Emoji._create_partial(
            int(custom_emoji_id),
            custom_name,
            (True if custom_animated else False),
        )
        continue


def parse_custom_emojis(text):
    """
    Parses out every custom emoji from the given text.
    
    Parameters
    ----------
    text : `str`
        The text to parse.
    
    Returns
    -------
    emojis : `set` of ``Emoji``
    """
    if text is None:
        return set()
    
    return {*_iter_parse_custom_emojis(text)}


def parse_all_emojis(text):
    """
    Parses out every emoji from the given text.
    
    Parameters
    ----------
    text : `str`
        The text to parse.
    
    Returns
    -------
    emojis : `set` of ``Emoji``
    """
    if text is None:
        return set()
    return {*_iter_parse_all_emojis(text)}
    


def _parse_emojis_ordered(text, parser):
    """
    Parses emojis of the given `text` with the given `parser`.
    Returns them ordered based on their appearance in the text.
    
    
    Parameters
    ----------
    text : `None`, `str`
        The text to parse.
    parser : `GeneratorFunction`
        The parser to use.
    
    Returns
    -------
    emojis_ordered : `list` of ``Emoji``
        Excludes duplicates.
    """
    emojis_ordered = []
    if (text is not None):
        emojis_unique = set()
        
        for emoji in parser(text):
            if emoji not in emojis_unique:
                emojis_ordered.append(emoji)
                emojis_unique.add(emoji)
    
    return emojis_ordered


def parse_custom_emojis_ordered(text):
    """
    Parses out every custom emoji from the given text. Returns them ordered based on their appearance in the text.
    
    Parameters
    ----------
    text : `None`, `str`
        The text to parse.
    
    Returns
    -------
    emojis_ordered : `list` of ``Emoji``
        Excludes duplicates.
    """
    return _parse_emojis_ordered(text, _iter_parse_custom_emojis)


def parse_all_emojis_ordered(text):
    """
    Parses out every emoji from the given text. Returns them ordered based on their appearance in the text.
    
    Parameters
    ----------
    text : `None`, `str`
        The text to parse.
    
    Returns
    -------
    emojis_ordered : `list` of ``Emoji``
        Excludes duplicates.
    """
    return _parse_emojis_ordered(text, _iter_parse_all_emojis)


def parse_reaction(text):
    """
    Parses out an emoji from the given reaction string.
    
    Parameters
    ----------
    text : `str`
        Reaction string.
    
    Returns
    -------
    emoji : `None`, ``Emoji``
    """
    try:
        emoji = UNICODE_TO_EMOJI[text]
    except KeyError:
        parsed = REACTION_RP.fullmatch(text)
        if parsed is None:
            emoji = None
        else:
            name, emoji_id = parsed.parsed()
            emoji_id = int(emoji_id)
            emoji = Emoji._create_partial(emoji_id, name, False)
    
    return emoji


@export
def create_unicode_emoji(unicode):
    """
    Creates an emoji from the given unicode value.
    
    Parameters
    ----------
    unicode : `str`
        Unicode value.
    
    Returns
    -------
    emoji : ``Emoji``
    """
    try:
        unicode_emoji = UNICODE_TO_EMOJI[unicode]
    except KeyError:
        warnings.warn(
            f'Undefined emoji : {unicode.encode()!r}\nPlease open an issue with this message.',
            RuntimeWarning,
        )
        unicode_emoji = Emoji._create_unicode(Unicode('', unicode, False, None, None), False)
    
    return unicode_emoji


def merge_update_reaction_mapping(old_reactions, new_reactions):
    """
    Merges the two reaction mapping, so values wont be overwritten if not required.
    
    Parameters
    ----------
    old_reactions : `None`, ``ReactionMapping``
        The old reactions on a message.
    new_reactions : `None`, ``ReactionMapping``
        The new reactions on a message.
    
    Returns
    -------
    real_reactions : `None`, ``ReactionMapping``
        The real merged reactions on a message.
    """
    if (old_reactions is None):
        return new_reactions
    
    elif (new_reactions is None):
        old_reactions.clear()
        return old_reactions
    
    old_emojis = {*old_reactions.keys()}
    new_emojis = {*new_reactions.keys()}
    
    for emoji in old_emojis - new_emojis:
        del old_reactions[emoji]
    
    for emoji in new_emojis - old_emojis:
        old_reactions[emoji] = new_reactions[emoji].copy()
    
    for emoji in new_emojis & old_emojis:
        old_users = old_reactions[emoji]
        new_users = new_reactions[emoji]
        
        if (len(old_users) != len(new_users)) or (not (old_users >= new_users)):
            old_reactions[emoji] = new_reactions[emoji].copy()
    
    old_reactions._full_check()
    
    return old_reactions
