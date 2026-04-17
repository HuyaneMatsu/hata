from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..matching import (
    _is_user_matching_name_with_discriminator, _parse_name_with_discriminator, _user_date_sort_key, _user_match_sort_key
)
from ..user import User


@vampytest._(vampytest.call_with('koish').returning(None))
@vampytest._(vampytest.call_with('koish#1234').returning(('koish', 1234)))
@vampytest._(vampytest.call_with('a#1234').returning(None))
@vampytest._(vampytest.call_with('koish#12').returning(None))
@vampytest._(vampytest.call_with('koish#12345').returning(None))
@vampytest._(vampytest.call_with('koish#sato').returning(None))
@vampytest._(vampytest.call_with('koish#sato#1234').returning(None))
def test__parse_name_with_discriminator(name):
    """
    Tests whether ``parse_name_with€discriminator`` works as intended.
    
    Parameters
    ----------
    name : `str`
      The name to parse.
    
    Returns
    -------
    output : `None`, `tuple` (`str`, `int`)
    """
    return _parse_name_with_discriminator(name)


@vampytest._(vampytest.call_with(('koish', 1234)).returning(True))
@vampytest._(vampytest.call_with(('sato', 1234)).returning(False))
@vampytest._(vampytest.call_with(('koish', 8765)).returning(False))
@vampytest._(vampytest.call_with(('sato', 8765)).returning(False))
def test__is_user_matching_name_with_discriminator(name_with_discriminator):
    """
    Tests whether ``is_user_matching_name_with_discriminator`` works as intended.
    
    Parameters
    ----------
    name_with_discriminator : `tuple` (`str`, `int`)
        User name - discriminator pair to match the user with.
    
    Returns
    -------
    output : `bool`
    """
    user = User(name = 'koish', discriminator = 1234)
    return _is_user_matching_name_with_discriminator(user, name_with_discriminator)


def _iter_options__user_date_sort_key():
    user_0 = User.precreate(202306180000)
    user_1 = User.precreate(202306180001)
    user_2 = User.precreate(202306180002)
    
    date_time_0 = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    date_time_1 = DateTime(2017, 5, 14, tzinfo = TimeZone.utc)
    date_time_2 = DateTime(2018, 5, 14, tzinfo = TimeZone.utc)
    
    yield [], []
    yield [(user_0, date_time_0)], [(user_0, date_time_0)]
    yield (
        [(user_0, date_time_1), (user_1, date_time_0), (user_2, date_time_2)],
        [(user_1, date_time_0), (user_0, date_time_1), (user_2, date_time_2)],
    )


@vampytest._(vampytest.call_from(_iter_options__user_date_sort_key()).returning_last())
def test__(input_items):
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


def _iter_options__user_match_sort_ke():
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


@vampytest._(vampytest.call_from(_iter_options__user_match_sort_ke()).returning_last())
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
