from datetime import datetime as DateTime

import vampytest

from ....channel import Channel
from ....emoji import Emoji
from ....role import Role
from ....soundboard import SoundboardSound
from ....sticker import Sticker
from ....user import User

from ..helpers import (
    _channel_match_sort_key, _emoji_match_sort_key, _role_match_sort_key, _soundboard_sound_match_sort_key,
    _sticker_match_sort_key, _user_date_sort_key, _user_match_sort_key
)


def _iter_options__users():
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


@vampytest._(vampytest.call_from(_iter_options__users()).returning_last())
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


def _iter_options__emojis():
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


@vampytest._(vampytest.call_from(_iter_options__emojis()).returning_last())
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


def _iter_options__soundboard_sounds():
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


@vampytest._(vampytest.call_from(_iter_options__soundboard_sounds()).returning_last())
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


@vampytest._(vampytest.call_from(_iter_options__emojis()).returning_last())
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


def _iter_options__sticker():
    sticker_0 = Sticker.precreate(202306180009)
    sticker_1 = Sticker.precreate(202306180010)
    sticker_2 = Sticker.precreate(202306180011)
    
    match_rate_0 = (1, 1, 3)
    match_rate_1 = (1, 2, 3)
    match_rate_2 = (2, 1, 4)
    
    yield [], []
    yield [(sticker_0, match_rate_0)], [(sticker_0, match_rate_0)]
    yield (
        [(sticker_0, match_rate_1), (sticker_1, match_rate_0), (sticker_2, match_rate_2)],
        [(sticker_1, match_rate_0), (sticker_0, match_rate_1), (sticker_2, match_rate_2)],
    )


@vampytest._(vampytest.call_from(_iter_options__sticker()).returning_last())
def test__sticker_match_sort_key(input_items):
    """
    Tests whether ``_sticker_match_sort_key`` works as intended.
    
    Parameters
    ----------
    input_items : `list` of `tuple` (``Sticker``, `tuple` (`int`, `int`, `int`))
        Input items to sort.
    
    Returns
    -------
    sorted_items : `list` of `tuple` (``Sticker``, `tuple` (`int`, `int`, `int`))
    """
    return sorted(input_items, key = _sticker_match_sort_key)


def _iter_options__role():
    role_0 = Role.precreate(202306240081)
    role_1 = Role.precreate(202306240082)
    role_2 = Role.precreate(202306240083)
    
    match_rate_0 = (1, 3)
    match_rate_1 = (2, 3)
    match_rate_2 = (1, 4)
    
    yield [], []
    yield [(role_0, match_rate_0)], [(role_0, match_rate_0)]
    yield (
        [(role_1, match_rate_1), (role_0, match_rate_0), (role_2, match_rate_2)],
        [(role_0, match_rate_0), (role_2, match_rate_2), (role_1, match_rate_1)],
    )


@vampytest._(vampytest.call_from(_iter_options__role()).returning_last())
def test__role_match_sort_key(input_items):
    """
    Tests whether ``_role_match_sort_key`` works as intended.
    
    Parameters
    ----------
    input_items : `list` of `tuple` (``Role``, `tuple` (`int`, `int`))
        Input items to sort.
    
    Returns
    -------
    sorted_items : `list` of `tuple` (``Role``, `tuple` (`int`, `int`))
    """
    return sorted(input_items, key = _role_match_sort_key)


def _iter_options__channels():
    channel_0 = Channel.precreate(202306250000)
    channel_1 = Channel.precreate(202306250001)
    channel_2 = Channel.precreate(202306250002)
    
    match_rate_0 = (1, 3)
    match_rate_1 = (1, 4)
    match_rate_2 = (2, 3)
    
    yield [], []
    yield [(channel_0, match_rate_0)], [(channel_0, match_rate_0)]
    yield (
        [(channel_0, match_rate_1), (channel_1, match_rate_0), (channel_2, match_rate_2)],
        [(channel_1, match_rate_0), (channel_0, match_rate_1), (channel_2, match_rate_2)],
    )


@vampytest._(vampytest.call_from(_iter_options__channels()).returning_last())
def test__channel_match_sort_key(input_items):
    """
    Tests whether ``_channel_match_sort_key`` works as intended.
    
    Parameters
    ----------
    input_items : `list` of `tuple` (``Channel``, `tuple` (`int`, `int`))
        Input items to sort.
    
    Returns
    -------
    sorted_items : `list` of `tuple` (``Channel``, `tuple` (`int`, `int`))
    """
    return sorted(input_items, key = _channel_match_sort_key)


def _iter_options__user():
    user_0 = User.precreate(202306250043)
    user_1 = User.precreate(202306250044)
    user_2 = User.precreate(202306250045)
    
    match_rate_0 = (1, 1, 3)
    match_rate_1 = (1, 2, 3)
    match_rate_2 = (2, 1, 4)
    
    yield [], []
    yield [(user_0, match_rate_0)], [(user_0, match_rate_0)]
    yield (
        [(user_0, match_rate_1), (user_1, match_rate_0), (user_2, match_rate_2)],
        [(user_1, match_rate_0), (user_0, match_rate_1), (user_2, match_rate_2)],
    )


@vampytest._(vampytest.call_from(_iter_options__user()).returning_last())
def test__user_match_sort_key(input_items):
    """
    Tests whether ``_user_match_sort_key`` works as intended.
    
    Parameters
    ----------
    input_items : `list` of `tuple` (``ClientUserBase``, `tuple` (`int`, `int`, `int`))
        Input items to sort.
    
    Returns
    -------
    sorted_items : `list` of `tuple` (``ClientUserBase``, `tuple` (`int`, `int`, `int`))
    """
    return sorted(input_items, key = _user_match_sort_key)
