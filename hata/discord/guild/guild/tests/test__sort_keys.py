from datetime import datetime as DateTime

import vampytest

from ....emoji import Emoji
from ....soundboard import SoundboardSound
from ....sticker import Sticker
from ....user import User

from ..helpers import (
    _emoji_match_sort_key, _soundboard_sound_match_sort_key, _sticker_match_sort_key, _user_date_sort_key
)


def iter_user_options():
    user_0 = User.precreate(202306180000)
    user_1 = User.precreate(202306180001)
    user_2 = User.precreate(202306180002)
    
    date_time_0 = DateTime(2016, 5, 14)
    date_time_1 = DateTime(2017, 5, 14)
    date_time_2 = DateTime(2018, 5, 14)
    
    yield [], []
    yield [(user_0, date_time_0)], [(user_0, date_time_0)]
    yield (
        [(user_0, date_time_1), (user_1, date_time_0), (user_2, date_time_2)],
        [(user_1, date_time_0), (user_0, date_time_1), (user_2, date_time_2)],
    )


@vampytest._(vampytest.call_from(iter_user_options()).returning_last())
def test__user_date_sort_key(input_items):
    """
    Tests whether ``_user_date_sort_key`` works as intended.
    
    Parameters
    ----------
    input_items : `list` of `tuple` (``ClientUserBase``, `datetime`)
        Input items to sort.
    
    Returns
    -------
    sorted_items : `list` of `tuple` (``ClientUserBase``, `datetime`)
    """
    return sorted(input_items, key = _user_date_sort_key)


def iter_emoji_options():
    emoji_0 = Emoji.precreate(202306180003)
    emoji_1 = Emoji.precreate(202306180004)
    emoji_2 = Emoji.precreate(202306180005)
    
    match_rate_0 = (1, 3)
    match_rate_1 = (1, 4)
    match_rate_2 = (2, 3)
    
    yield [], []
    yield [(emoji_0, match_rate_0)], [(emoji_0, match_rate_0)]
    yield (
        [(emoji_0, match_rate_1), (emoji_1, match_rate_0), (emoji_2, match_rate_2)],
        [(emoji_1, match_rate_0), (emoji_0, match_rate_1), (emoji_2, match_rate_2)],
    )


@vampytest._(vampytest.call_from(iter_emoji_options()).returning_last())
def test__emoji_match_sort_key(input_items):
    """
    Tests whether ``_emoji_match_sort_key`` works as intended.
    
    Parameters
    ----------
    input_items : `list` of `tuple` (``Emoji``, `tuple` (`int`, `int`))
        Input items to sort.
    
    Returns
    -------
    sorted_items : `list` of `tuple` (``Emoji``, `tuple` (`int`, `int`))
    """
    return sorted(input_items, key = _emoji_match_sort_key)


def iter_soundboard_sound_options():
    soundboard_sound_0 = SoundboardSound.precreate(202306180006)
    soundboard_sound_1 = SoundboardSound.precreate(202306180007)
    soundboard_sound_2 = SoundboardSound.precreate(202306180008)
    
    match_rate_0 = (1, 3)
    match_rate_1 = (1, 4)
    match_rate_2 = (2, 3)
    
    yield [], []
    yield [(soundboard_sound_0, match_rate_0)], [(soundboard_sound_0, match_rate_0)]
    yield (
        [(soundboard_sound_0, match_rate_1), (soundboard_sound_1, match_rate_0), (soundboard_sound_2, match_rate_2)],
        [(soundboard_sound_1, match_rate_0), (soundboard_sound_0, match_rate_1), (soundboard_sound_2, match_rate_2)],
    )


@vampytest._(vampytest.call_from(iter_soundboard_sound_options()).returning_last())
def test__soundboard_sound_match_sort_key(input_items):
    """
    Tests whether ``_soundboard_sound_match_sort_key`` works as intended.
    
    Parameters
    ----------
    input_items : `list` of `tuple` (``SoundboardSound``, `tuple` (`int`, `int`))
        Input items to sort.
    
    Returns
    -------
    sorted_items : `list` of `tuple` (``SoundboardSound``, `tuple` (`int`, `int`))
    """
    return sorted(input_items, key = _soundboard_sound_match_sort_key)


@vampytest._(vampytest.call_from(iter_emoji_options()).returning_last())
def test__emoji_match_sort_key(input_items):
    """
    Tests whether ``_emoji_match_sort_key`` works as intended.
    
    Parameters
    ----------
    input_items : `list` of `tuple` (``Emoji``, `tuple` (`int`, `int`))
        Input items to sort.
    
    Returns
    -------
    sorted_items : `list` of `tuple` (``Emoji``, `tuple` (`int`, `int`))
    """
    return sorted(input_items, key = _emoji_match_sort_key)


def iter_sticker_options():
    sticker_0 = Sticker.precreate(202306180009)
    sticker_1 = Sticker.precreate(202306180010)
    sticker_2 = Sticker.precreate(202306180011)
    
    match_rate_0 = (False, 1, 3)
    match_rate_1 = (False, 2, 3)
    match_rate_2 = (True, 1, 4)
    
    yield [], []
    yield [(sticker_0, match_rate_0)], [(sticker_0, match_rate_0)]
    yield (
        [(sticker_0, match_rate_1), (sticker_1, match_rate_0), (sticker_2, match_rate_2)],
        [(sticker_1, match_rate_0), (sticker_0, match_rate_1), (sticker_2, match_rate_2)],
    )


@vampytest._(vampytest.call_from(iter_sticker_options()).returning_last())
def test__sticker_match_sort_key(input_items):
    """
    Tests whether ``_sticker_match_sort_key`` works as intended.
    
    Parameters
    ----------
    input_items : `list` of `tuple` (``Sticker``, `tuple` (`bool`, `int`, `int`))
        Input items to sort.
    
    Returns
    -------
    sorted_items : `list` of `tuple` (``Sticker``, `tuple` (`bool`, `int`, `int`))
    """
    return sorted(input_items, key = _sticker_match_sort_key)
