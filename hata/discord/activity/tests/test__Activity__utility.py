from datetime import datetime as DateTime, timedelta as TimeDelta

import vampytest

from ...color import Color
from ...utils import is_url

from ..activity import Activity
from ..fields import ActivityAssets, ActivityTimestamps
from ..preinstanced import ActivityType


def test__Activity__color():
    """
    Tests whether ``Activity.color`` works as intended.
    """
    activity = Activity('', activity_type = ActivityType.game)
    vampytest.assert_instance(activity.color, Color)


def test__Activity__discord_side_id__0():
    """
    Tests whether ``Activity.discord_side_id`` works as intended.
    
    Case: no id.
    """
    activity = Activity('', activity_type = ActivityType.game)
    vampytest.assert_instance(activity.discord_side_id, str)


def test__Activity__discord_side_id__1():
    """
    Tests whether ``Activity.discord_side_id`` works as intended.
    
    Case: id given.
    """
    activity_id = 202209080000
    activity = Activity('', activity_type = ActivityType.game, activity_id = activity_id)
    vampytest.assert_instance(activity.discord_side_id, str)


def test__Activity__twitch_name():
    """
    Tests whether ``Activity.twitch_name`` works as intended.
    """
    name = 'senya'
    
    activity = Activity(
        '', activity_type = ActivityType.stream, assets = ActivityAssets(image_large = f'twitch:{name}')
    )
    
    vampytest.assert_eq(activity.twitch_name, name)


def test__Activity__twitch_preview_image_url():
    """
    Tests whether ``Activity.twitch_preview_image_url`` works as intended.
    """
    name = 'senya'
    
    activity = Activity(
        '', activity_type = ActivityType.stream, assets = ActivityAssets(image_large = f'twitch:{name}')
    )
    
    twitch_preview_image_url = activity.twitch_preview_image_url
    vampytest.assert_instance(twitch_preview_image_url, str)
    vampytest.assert_true(is_url(twitch_preview_image_url))
    vampytest.assert_in(name, twitch_preview_image_url)


def test__Activity__youtube_video_id():
    """
    Tests whether ``Activity.youtube_video_id`` works as intended.
    """
    name = 'senya'
    
    activity = Activity(
        '', activity_type = ActivityType.stream, assets = ActivityAssets(image_large = f'youtube:{name}')
    )
    
    vampytest.assert_eq(activity.youtube_video_id, name)


def test__Activity__youtube_preview_image_url():
    """
    Tests whether ``Activity.youtube_preview_image_url`` works as intended.
    """
    name = 'senya'
    
    activity = Activity(
        '', activity_type = ActivityType.stream, assets = ActivityAssets(image_large = f'youtube:{name}')
    )
    
    youtube_preview_image_url = activity.youtube_preview_image_url
    vampytest.assert_instance(youtube_preview_image_url, str)
    vampytest.assert_true(is_url(youtube_preview_image_url))
    vampytest.assert_in(name, youtube_preview_image_url)


def test__Activity__spotify_track_duration():
    """
    Tests whether ``Activity.spotify_track_duration`` works as intended.
    """
    duration = TimeDelta(seconds = 69)
    start = DateTime(2022, 6, 6)
    end = start + duration
    
    activity = Activity(
        '', activity_type = ActivityType.spotify, timestamps = ActivityTimestamps(end = end, start = start)
    )
    
    vampytest.assert_eq(activity.spotify_track_duration, duration)


def test__Activity__spotify_cover_id():
    """
    Tests whether ``Activity.spotify_cover_id`` works as intended.
    """
    name = 'senya'
    
    activity = Activity(
        '', activity_type = ActivityType.spotify, assets = ActivityAssets(image_large = f'spotify:{name}')
    )
    
    vampytest.assert_eq(activity.spotify_cover_id, name)


def test__Activity__spotify_album_cover_url():
    """
    Tests whether ``Activity.spotify_album_cover_url`` works as intended.
    """
    name = 'senya'
    
    activity = Activity(
        '', activity_type = ActivityType.spotify, assets = ActivityAssets(image_large = f'spotify:{name}')
    )
    
    spotify_album_cover_url = activity.spotify_album_cover_url
    vampytest.assert_instance(spotify_album_cover_url, str)
    vampytest.assert_true(is_url(spotify_album_cover_url))
    vampytest.assert_in(name, spotify_album_cover_url)


def test__Activity__spotify_track_id():
    """
    Tests whether ``Activity.spotify_track_id`` works as intended.
    """
    name = 'senya'
    
    activity = Activity(
        '', activity_type = ActivityType.spotify, sync_id = name
    )
    
    vampytest.assert_eq(activity.spotify_track_id, name)


def test__Activity__spotify_track_url():
    """
    Tests whether ``Activity.spotify_track_url`` works as intended.
    """
    name = 'senya'
    
    activity = Activity(
        '', activity_type = ActivityType.spotify, sync_id = name
    )
    
    spotify_track_url = activity.spotify_track_url
    vampytest.assert_instance(spotify_track_url, str)
    vampytest.assert_true(is_url(spotify_track_url))
    vampytest.assert_in(name, spotify_track_url)


def test__Activity__image_large_url():
    """
    Tests whether ``Activity.image_large_url`` works as intended.
    """
    application_id = 202209080001
    image_id = '202209080002'
    
    activity = Activity('', application_id = application_id, assets = ActivityAssets(image_large = image_id))
    
    image_large_url = activity.image_large_url
    vampytest.assert_instance(image_large_url, str)
    vampytest.assert_true(is_url(image_large_url))
    vampytest.assert_in(image_id, image_large_url)


def test__Activity__image_large_url_as():
    """
    Tests whether ``Activity.image_large_url_as`` works as intended.
    """
    application_id = 202209080003
    image_id = '202209080004'
    
    activity = Activity('', application_id = application_id, assets = ActivityAssets(image_large = image_id))
    
    image_large_url = activity.image_large_url_as()
    vampytest.assert_instance(image_large_url, str)
    vampytest.assert_true(is_url(image_large_url))
    vampytest.assert_in(image_id, image_large_url)


def test__Activity__image_small_url():
    """
    Tests whether ``Activity.image_small_url`` works as intended.
    """
    application_id = 202209080005
    image_id = '202209080006'
    
    activity = Activity('', application_id = application_id, assets = ActivityAssets(image_small = image_id))
    
    image_small_url = activity.image_small_url
    vampytest.assert_instance(image_small_url, str)
    vampytest.assert_true(is_url(image_small_url))
    vampytest.assert_in(image_id, image_small_url)


def test__Activity__image_small_url_as():
    """
    Tests whether ``Activity.image_small_url_as`` works as intended.
    """
    application_id = 202209080007
    image_id = '202209080008'
    
    activity = Activity('', application_id = application_id, assets = ActivityAssets(image_small = image_id))
    
    image_small_url = activity.image_small_url_as()
    vampytest.assert_instance(image_small_url, str)
    vampytest.assert_true(is_url(image_small_url))
    vampytest.assert_in(image_id, image_small_url)


def test__Activity__start():
    """
    Tests whether ``Activity.start`` works as intended.
    """
    start = DateTime(2022, 6, 6)
    
    activity = Activity(
        '', activity_type = ActivityType.spotify, timestamps = ActivityTimestamps(start = start)
    )
    
    vampytest.assert_eq(activity.start, start)


def test__Activity__end():
    """
    Tests whether ``Activity.end`` works as intended.
    """
    end = DateTime(2022, 6, 6)
    
    activity = Activity(
        '', activity_type = ActivityType.spotify, timestamps = ActivityTimestamps(end = end)
    )
    
    vampytest.assert_eq(activity.end, end)
