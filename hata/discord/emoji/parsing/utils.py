__all__ = (
    'parse_all_emojis', 'parse_all_emojis_ordered', 'parse_custom_emojis', 'parse_custom_emojis_ordered', 'parse_emoji',
    'parse_reaction'
)

from ...core import BUILTIN_EMOJIS, UNICODE_TO_EMOJI
from ...utils import EMOJI_RP, REACTION_RP

from ..emoji import Emoji
from ..unicode.unicode_type import VARIATION_SELECTOR_16_POSTFIX

from .pattern import EMOJI_ALL_RP


VARIATION_SELECTOR_16_POSTFIX_WITH_COLON = VARIATION_SELECTOR_16_POSTFIX + ':'


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
            name, emoji_id = parsed.groups()
            emoji_id = int(emoji_id)
            emoji = Emoji._create_partial(emoji_id, name, False)
    
    return emoji
