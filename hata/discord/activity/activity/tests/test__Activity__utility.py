from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest

from ....color import Color
from ....utils import is_url

from ...activity_assets import ActivityAssets
from ...activity_timestamps import ActivityTimestamps

from ..activity import Activity
from ..preinstanced import ActivityType

from .test__Activity__constructor import _assert_fields_set


def test__Activity__color():
    """
    Tests whether ``Activity.color`` works as intended.
    """
    activity = Activity(activity_type = ActivityType.playing)
    vampytest.assert_instance(activity.color, Color)


def test__Activity__discord_side_id__no_id():
    """
    Tests whether ``Activity.discord_side_id`` works as intended.
    
    Case: no id.
    """
    activity = Activity(activity_type = ActivityType.playing)
    vampytest.assert_instance(activity.discord_side_id, str)


def test__Activity__discord_side_id__id_given():
    """
    Tests whether ``Activity.discord_side_id`` works as intended.
    
    Case: id given.
    """
    activity_id = 202209080000
    activity = Activity(activity_type = ActivityType.playing, activity_id = activity_id)
    vampytest.assert_instance(activity.discord_side_id, str)


def test__Activity__twitch_name():
    """
    Tests whether ``Activity.twitch_name`` works as intended.
    """
    name = 'senya'
    
    activity = Activity(activity_type = ActivityType.stream, assets = ActivityAssets(image_large = f'twitch:{name}'))
    
    vampytest.assert_eq(activity.twitch_name, name)


def test__Activity__twitch_preview_image_url():
    """
    Tests whether ``Activity.twitch_preview_image_url`` works as intended.
    """
    name = 'senya'
    
    activity = Activity(activity_type = ActivityType.stream, assets = ActivityAssets(image_large = f'twitch:{name}'))
    
    twitch_preview_image_url = activity.twitch_preview_image_url
    vampytest.assert_instance(twitch_preview_image_url, str)
    vampytest.assert_true(is_url(twitch_preview_image_url))
    vampytest.assert_in(name, twitch_preview_image_url)


def test__Activity__youtube_video_id():
    """
    Tests whether ``Activity.youtube_video_id`` works as intended.
    """
    name = 'senya'
    
    activity = Activity(activity_type = ActivityType.stream, assets = ActivityAssets(image_large = f'youtube:{name}'))
    
    vampytest.assert_eq(activity.youtube_video_id, name)


def test__Activity__youtube_preview_image_url():
    """
    Tests whether ``Activity.youtube_preview_image_url`` works as intended.
    """
    name = 'senya'
    
    activity = Activity(activity_type = ActivityType.stream, assets = ActivityAssets(image_large = f'youtube:{name}'))
    
    youtube_preview_image_url = activity.youtube_preview_image_url
    vampytest.assert_instance(youtube_preview_image_url, str)
    vampytest.assert_true(is_url(youtube_preview_image_url))
    vampytest.assert_in(name, youtube_preview_image_url)


def test__Activity__spotify_track_duration():
    """
    Tests whether ``Activity.spotify_track_duration`` works as intended.
    """
    duration = TimeDelta(seconds = 69)
    start = DateTime(2022, 6, 6, tzinfo = TimeZone.utc)
    end = start + duration
    
    activity = Activity(activity_type = ActivityType.spotify, timestamps = ActivityTimestamps(end = end, start = start))
    
    vampytest.assert_eq(activity.spotify_track_duration, duration)


def test__Activity__spotify_cover_id():
    """
    Tests whether ``Activity.spotify_cover_id`` works as intended.
    """
    name = 'senya'
    
    activity = Activity(activity_type = ActivityType.spotify, assets = ActivityAssets(image_large = f'spotify:{name}'))
    
    vampytest.assert_eq(activity.spotify_cover_id, name)


def test__Activity__spotify_album_cover_url():
    """
    Tests whether ``Activity.spotify_album_cover_url`` works as intended.
    """
    name = 'senya'
    
    activity = Activity(activity_type = ActivityType.spotify, assets = ActivityAssets(image_large = f'spotify:{name}'))
    
    spotify_album_cover_url = activity.spotify_album_cover_url
    vampytest.assert_instance(spotify_album_cover_url, str)
    vampytest.assert_true(is_url(spotify_album_cover_url))
    vampytest.assert_in(name, spotify_album_cover_url)


def test__Activity__spotify_track_id():
    """
    Tests whether ``Activity.spotify_track_id`` works as intended.
    """
    name = 'senya'
    
    activity = Activity(activity_type = ActivityType.spotify, sync_id = name)
    
    vampytest.assert_eq(activity.spotify_track_id, name)


def test__Activity__spotify_track_url():
    """
    Tests whether ``Activity.spotify_track_url`` works as intended.
    """
    name = 'senya'
    
    activity = Activity(activity_type = ActivityType.spotify, sync_id = name)
    
    spotify_track_url = activity.spotify_track_url
    vampytest.assert_instance(spotify_track_url, str)
    vampytest.assert_true(is_url(spotify_track_url))
    vampytest.assert_in(name, spotify_track_url)


def test__Activity__start():
    """
    Tests whether ``Activity.start`` works as intended.
    """
    start = DateTime(2022, 6, 6, tzinfo = TimeZone.utc)
    
    activity = Activity(activity_type = ActivityType.spotify, timestamps = ActivityTimestamps(start = start))
    
    vampytest.assert_eq(activity.start, start)


def test__Activity__end():
    """
    Tests whether ``Activity.end`` works as intended.
    """
    end = DateTime(2022, 6, 6, tzinfo = TimeZone.utc)
    
    activity = Activity(activity_type = ActivityType.spotify, timestamps = ActivityTimestamps(end = end))
    
    vampytest.assert_eq(activity.end, end)


def test__Activity__copy():
    """
    Tests whether ``Activity.copy`` works as intended.
    """
    name = 'Yuuka'
    
    activity = Activity(name)
    
    copy = activity.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(activity, copy)
    
    vampytest.assert_eq(activity, copy)


def test__Activity__copy_with__no_fields_given():
    """
    Tests whether ``Activity.copy_with`` works as intended.
    
    Case: No fields given.
    """
    name = 'Yuuka'
    
    activity = Activity(name)
    
    copy = activity.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(activity, copy)
    
    vampytest.assert_eq(activity, copy)


def test__Activity__copy_with__fields_given():
    """
    Tests whether ``Activity.copy_with`` works as intended.
    
    Case: Fields given.
    """
    old_activity_type = ActivityType.playing
    old_name = 'Yuuka'
    
    new_activity_type = ActivityType.competing
    new_name = 'koishi'
    
    activity = Activity(old_name, activity_type = old_activity_type)
    
    copy = activity.copy_with(
        activity_type = new_activity_type,
        name = new_name,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(activity, copy)
    
    vampytest.assert_is(copy.type, new_activity_type)
    vampytest.assert_eq(copy.name, new_name)


def _iter_options__image_large_url():
    application_id = 202209080001
    image_large = '202209080002'
    
    yield (
        0,
        None,
        False,
    )
    
    yield (
        application_id,
        image_large,
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__image_large_url()).returning_last())
def test__Activity__image_large_url(application_id, image_large):
    """
    Tests whether ``Activity.image_large_url`` works as intended.
    
    Parameters
    ----------
    application_id : `int`
        Application identifier to create activity with.
    
    image_large : `None | str`
        Asset large image value to create activity with.
    
    Returns
    -------
    has_image_large_url : `bool`
    """
    activity = Activity(application_id = application_id, assets = ActivityAssets(image_large = image_large))
    
    output = activity.image_large_url
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__image_large_url_as():
    application_id = 202209080003
    image_large = '202209080004'
    
    yield (
        0,
        None,
        {'ext': 'jpg', 'size': 128},
        False,
    )
    
    yield (
        application_id,
        image_large,
        {'ext': 'jpg', 'size': 128},
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__image_large_url_as()).returning_last())
def test__Activity__image_large_url_as(application_id, image_large, keyword_parameters):
    """
    Tests whether ``Activity.image_large_url_as`` works as intended.
    
    Parameters
    ----------
    application_id : `int`
        Application identifier to create activity with.
    
    image_large : `None | str`
        Asset large image value to create activity with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    has_image_large_url : `bool`
    """
    activity = Activity(application_id = application_id, assets = ActivityAssets(image_large = image_large))
    
    output = activity.image_large_url_as(**keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__image_small_url():
    application_id = 202209080005
    image_small = '202209080006'
    
    yield (
        0,
        None,
        False,
    )
    
    yield (
        application_id,
        image_small,
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__image_small_url()).returning_last())
def test__Activity__image_small_url(application_id, image_small):
    """
    Tests whether ``Activity.image_small_url`` works as intended.
    
    Parameters
    ----------
    application_id : `int`
        Application identifier to create activity with.
    
    image_small : `None | str`
        Asset small image value to create activity with.
    
    Returns
    -------
    has_image_small_url : `bool`
    """
    activity = Activity(application_id = application_id, assets = ActivityAssets(image_small = image_small))
    
    output = activity.image_small_url
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__image_small_url_as():
    application_id = 202209080007
    image_small = '202209080008'
    
    yield (
        0,
        None,
        {'ext': 'jpg', 'size': 128},
        False,
    )
    
    yield (
        application_id,
        image_small,
        {'ext': 'jpg', 'size': 128},
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__image_small_url_as()).returning_last())
def test__Activity__image_small_url_as(application_id, image_small, keyword_parameters):
    """
    Tests whether ``Activity.image_small_url_as`` works as intended.
    
    Parameters
    ----------
    application_id : `int`
        Application identifier to create activity with.
    
    image_small : `None | str`
        Asset small image value to create activity with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    has_image_small_url : `bool`
    """
    activity = Activity(application_id = application_id, assets = ActivityAssets(image_small = image_small))
    
    output = activity.image_small_url_as(**keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)
