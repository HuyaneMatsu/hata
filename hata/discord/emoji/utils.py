__all__ = ('create_partial_emoji_from_data', 'create_partial_emoji_data', 'parse_emoji', 'parse_custom_emojis',
    'parse_reaction',)

from ...backend.export import export

from ..core import EMOJIS
from ..utils import EMOJI_RP, REACTION_RP

from .emoji import UNICODE_TO_EMOJI, Emoji


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
    emoji : ``Emoji``
    """
    try:
        name = data['name']
    except KeyError:
        name = data['emoji_name']
        emoji_id = data.get('emoji_id', None)
        emoji_animated = data.get('emoji_animated', False)
    else:
        emoji_id = data.get('id', None)
        emoji_animated = data.get('animated', False)
    
    if emoji_id is None:
        try:
            return UNICODE_TO_EMOJI[name]
        except KeyError:
            raise RuntimeError(f'Undefined emoji : {name.encode()!r}\nPlease open an issue with this message.') \
                from None
    
    emoji_id = int(emoji_id)
    
    try:
        emoji = EMOJIS[emoji_id]
    except KeyError:
        emoji = object.__new__(Emoji)
        emoji.id = emoji_id
        emoji.animated = emoji_animated
        EMOJIS[emoji_id] = emoji
        emoji.unicode = None
        emoji.guild = None
    
    # name can change
    if name is None:
        name = ''
    
    emoji.name = name
    
    return emoji


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
        emoji_data['id'] = emoji.id
        emoji_data['name'] = emoji.name
        
        if emoji.animated:
            emoji_data['animated'] = True
    else:
        emoji_data['name'] = unicode
    
    return emoji_data


def parse_emoji(text):
    """
    Tries to parse out an ``Emoji`` from the inputted text. This emoji can be custom and unicode emoji as well.
    
    If the parsing yields a custom emoji what is not loaded, the function will return an `untrusted` partial emoji,
    what means it wont be stored at `EMOJIS`. If the parsing fails the function returns `None`.
    
    Returns
    -------
    emoji : `None` or ``Emoji``
    """
    parsed = EMOJI_RP.fullmatch(text)
    if parsed is None:
        emoji = UNICODE_TO_EMOJI.get(text, None)
    else:
        animated, name, emoji_id = parsed.groups()
        animated = (animated is not None)
        emoji_id = int(emoji_id)
        emoji = Emoji._create_partial(emoji_id, name, animated)
    
    return emoji


def parse_custom_emojis(text):
    """
    Parses out every custom emoji from the given text.
    
    Parameters
    ----------
    text : `str`
        Text, what might contain custom emojis.
    
    Returns
    -------
    emojis : `set` of ``Emoji``
    """
    emojis = set()
    for groups in EMOJI_RP.findall(text):
        animated, name, emoji_id = groups
        animated = (animated is not None)
        emoji_id = int(emoji_id)
        emoji = Emoji._create_partial(emoji_id, name, animated)
        emojis.add(emoji)
    
    return emojis


def parse_reaction(text):
    """
    Parses out an emoji from the given reaction string.
    
    Parameters
    ----------
    text : `str`
        Reaction string.
    
    Returns
    -------
    emoji : `None` or ``Emoji``
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
