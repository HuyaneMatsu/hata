__all__ = (
    'create_emoji_from_exclusive_data', 'create_partial_emoji_data', 'create_partial_emoji_from_data',
    'create_partial_emoji_from_id', 'create_partial_emoji_from_inline_data', 'create_unicode_emoji',
    'put_exclusive_emoji_data_into', 'put_partial_emoji_inline_data_into'
)

import warnings

from scarletio import export, include

from ...core import EMOJIS, UNICODE_TO_EMOJI

from .emoji import Emoji


Unicode = include('Unicode')


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
    data : `dict` of (`str`, `object`) items
        Partial emoji data.
    
    Returns
    -------
    emoji : `None`, ``Emoji``
    """
    return _create_partial_emoji_from_fields(
        data.get('name', None), data.get('id', None), data.get('animated', False),
    )


@export
def create_partial_emoji_from_inline_data(data):
    """
    Creates an emoji from inline partial emoji data sent by Discord.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Partial emoji data.
    
    Returns
    -------
    emoji : `None`, ``Emoji``
    """
    return _create_partial_emoji_from_fields(
        data.get('emoji_name', None), data.get('emoji_id', None), data.get('emoji_animated', False)
    )


def _create_partial_emoji_from_fields(emoji_name, emoji_id, emoji_animated):
    """
    Creates a partial emoji from the given fields.
    
    Parameters
    ----------
    emoji_name : `None`, `str`
        The emoji's name.
    emoji_id : `None`, `str`
        The emoji's identifier.
    emoji_animated : `bool`
        Whether the emoji is animated.
    
    Returns
    -------
    emoji : `None`, ``Emoji``
    """
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
    data : `dict` of (`str`, `object`) items
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


def put_partial_emoji_inline_data_into(emoji, data):
    """
    Familiar to ``create_partial_emoji_data``, but instead of creating a standalone emoji data, uses the `emoji_`
    prefix field form to add it to an already defined dictionary.
    
    Parameters
    ----------
    emoji : `None`, ``Emoji``
        The emoji to serialize.
    data : `dict` of (`str`, `object`) items
        The data to put the emoji fields into.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
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
    data : `dict` of (`str`, `object`) items
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
    data : `dict` of (`str`, `object`) items
        The data to put the emoji fields into.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
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
        raw_value = unicode.encode()
        warnings.warn(
            f'Undefined emoji : {raw_value!r}\nPlease open an issue with this message.',
            RuntimeWarning,
        )
        unicode_emoji = Emoji._create_unicode(Unicode('', raw_value, False, None, None), False)
    
    return unicode_emoji
