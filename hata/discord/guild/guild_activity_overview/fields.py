__all__ = ()

from ...color import Color
from ...field_parsers import (
    entity_id_array_parser_factory, entity_id_parser_factory, force_string_parser_factory, int_parser_factory,
    nullable_string_parser_factory, preinstanced_array_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    entity_id_putter_factory, force_string_putter_factory, int_optional_putter_factory, int_putter_factory,
    nullable_string_putter_factory, optional_entity_id_array_optional_putter_factory, preinstanced_array_putter_factory,
    preinstanced_putter_factory
)
from ...field_validators import (
    entity_id_array_validator_factory, entity_id_validator_factory, force_string_validator_factory,
    int_conditional_validator_factory, int_options_validator_factory, nullable_object_array_validator_factory,
    nullable_string_validator_factory, preinstanced_array_validator_factory, preinstanced_validator_factory
)
from ...scheduled_event import PrivacyLevel

from ..guild import GuildFeature
from ..guild.guild_boost_perks import LEVELS
from ..guild_activity_overview_activity import GuildActivityOverviewActivity
from ..guild_activity_overview_tag import GuildActivityOverviewTag

from .constants import (
    BADGE_TAG_LENGTH_MAX, BADGE_TAG_LENGTH_MIN, DESCRIPTION_LENGTH_MAX, NAME_LENGTH_MAX, NAME_LENGTH_MIN
)


# activities

def parse_activities(data):
    """
    Parses the activities from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    activities : `None | dict<int, GuildActivityOverviewActivity>`
    """
    activities_datas = data.get('game_activity', None)
    if (activities_datas is not None) and activities_datas:
        return {
            int(application_id): GuildActivityOverviewActivity.from_data(activity_data)
            for application_id, activity_data in activities_datas.items()
        }


def put_activities(activities, data, defaults):
    """
    Puts activity into the given data.
    
    Parameters
    ----------
    activities : `None | dict<int, GuildActivityOverviewActivity>`
        Activities to serialize.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if activities is None:
        activities_data = {}
    else:
        activities_data = {
            str(application_id): guild_activity_overview_activity.to_data(defaults = defaults)
            for application_id, guild_activity_overview_activity in activities.items()
        }
    
    data['game_activity'] = activities_data
    return data


def validate_activities(activities):
    """
    Validates the given activities.
    
    Parameters
    ----------
    activities : `object`
        Activities to validate.
    
    Returns
    -------
    activities : `None | dict<int, GuildActivityOverviewActivity>`
    
    Raises
    ------
    TypeError
        - If `activities` type is incorrect.
    """
    if activities is None:
        return None
    
    if not isinstance(activities, dict):
        raise TypeError(
            f'`activities` can be `None` or `dict`, got {type(activities).__name__}; {activities!r}.'
        )
    
    validated_activities = None
    
    for application_id, guild_activity_overview_activity in activities.items():
        if validated_activities is None:
            validated_activities = {}
        
        if not isinstance(application_id, int):
            raise TypeError(
                f'`activities` keys can be `int`, got {type(application_id).__name__}; {application_id!r}.'
            )
        
        if not isinstance(guild_activity_overview_activity, GuildActivityOverviewActivity):
            raise TypeError(
                f'`activities` keys can be `{GuildActivityOverviewActivity.__name__}`, '
                f'got {type(guild_activity_overview_activity).__name__}; {guild_activity_overview_activity!r}.'
            )
        
        validated_activities[application_id] = guild_activity_overview_activity
        
    return validated_activities


# activity_application_ids

parse_activity_application_ids = entity_id_array_parser_factory('game_application_ids', ordered = False)
put_activity_application_ids = optional_entity_id_array_optional_putter_factory('game_application_ids')
validate_activity_application_ids = entity_id_array_validator_factory(
    'activity_application_ids', NotImplemented, include = 'Application', ordered = False
)


# approximate_online_count

parse_approximate_online_count = int_parser_factory('online_count', 0)
put_approximate_online_count = int_putter_factory('online_count')
validate_approximate_online_count = int_conditional_validator_factory(
    'approximate_online_count',
    0,
    lambda approximate_online_count : approximate_online_count >= 0,
    '>= 0',
)


# approximate_user_count

parse_approximate_user_count = int_parser_factory('member_count', 0)
put_approximate_user_count = int_putter_factory('member_count')
validate_approximate_user_count = int_conditional_validator_factory(
    'approximate_user_count',
    0,
    lambda approximate_user_count : approximate_user_count >= 0,
    '>= 0',
)


# badge

parse_badge = int_parser_factory('badge', 0)
put_badge = int_putter_factory('badge')
validate_badge = int_conditional_validator_factory(
    'badge',
    0,
    lambda badge : badge >= 0,
    '>= 0',
)


# badge_color_primary

def parse_badge_color_primary(data):
    """
    Parses banner color (custom) from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        User data.
    
    Returns
    -------
    badge_color_primary : `None | Color`
    """
    badge_color_primary = data.get('badge_color_primary', None)
    if (badge_color_primary is not None):
        badge_color_primary = Color.from_html(badge_color_primary)
    
    return badge_color_primary


def put_badge_color_primary(badge_color_primary, data, defaults):
    """
    Serializes the given color into the given data.
    
    Parameters
    ----------
    badge_color_primary : `None | Color`
        Banner color.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if (badge_color_primary is not None):
        badge_color_primary = badge_color_primary.as_html
    data['badge_color_primary'] = badge_color_primary
    
    return data


def validate_badge_color_primary(badge_color_primary):
    """
    Validates the given `badge_color_primary` value.
    
    Parameters
    ----------
    badge_color_primary : `None | Color | value`
        The banner color to validate.
    
    Returns
    -------
    badge_color_primary : `None | Color`
    
    Raises
    ------
    TypeError
        - If `badge_color_primary` is not `None`, `Color`, `int`.
    ValueError
        - If `badge_color_primary`'s value is out of the expected range.
    """
    if (badge_color_primary is None):
        return None
    
    if isinstance(badge_color_primary, Color):
        return badge_color_primary
    
    if isinstance(badge_color_primary, int):
        if badge_color_primary < 0 or badge_color_primary > 0xffffff:
            raise ValueError(
                f'`badge_color_primary` can be between 0 and 0xffffff, got {badge_color_primary!r}.'
            )
        
        return Color(badge_color_primary)
    
    raise TypeError(
        f'`badge_color_primary` can be `None`, `{Color.__name__}`, `int`, '
        f'got {type(badge_color_primary).__name__}; {badge_color_primary!r}.'
    )


# badge_color_secondary

def parse_badge_color_secondary(data):
    """
    Parses banner color (custom) from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        User data.
    
    Returns
    -------
    badge_color_secondary : `None | Color`
    """
    badge_color_secondary = data.get('badge_color_secondary', None)
    if (badge_color_secondary is not None):
        badge_color_secondary = Color.from_html(badge_color_secondary)
    
    return badge_color_secondary


def put_badge_color_secondary(badge_color_secondary, data, defaults):
    """
    Serializes the given color into the given data.
    
    Parameters
    ----------
    badge_color_secondary : `None | Color`
        Banner color.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if (badge_color_secondary is not None):
        badge_color_secondary = badge_color_secondary.as_html
    data['badge_color_secondary'] = badge_color_secondary
    
    return data


def validate_badge_color_secondary(badge_color_secondary):
    """
    Validates the given `badge_color_secondary` value.
    
    Parameters
    ----------
    badge_color_secondary : `None | Color | value`
        The banner color to validate.
    
    Returns
    -------
    badge_color_secondary : `None | Color`
    
    Raises
    ------
    TypeError
        - If `badge_color_secondary` is not `None`, `Color`, `int`.
    ValueError
        - If `badge_color_secondary`'s value is out of the expected range.
    """
    if (badge_color_secondary is None):
        return None
    
    if isinstance(badge_color_secondary, Color):
        return badge_color_secondary
    
    if isinstance(badge_color_secondary, int):
        if badge_color_secondary < 0 or badge_color_secondary > 0xffffff:
            raise ValueError(
                f'`badge_color_secondary` can be between 0 and 0xffffff, got {badge_color_secondary!r}.'
            )
        
        return Color(badge_color_secondary)
    
    raise TypeError(
        f'`badge_color_secondary` can be `None`, `{Color.__name__}`, `int`, '
        f'got {type(badge_color_secondary).__name__}; {badge_color_secondary!r}.'
    )


# badge_tag

parse_badge_tag = force_string_parser_factory('tag')
put_badge_tag = force_string_putter_factory('tag')
validate_badge_tag = force_string_validator_factory('badge_tag', BADGE_TAG_LENGTH_MIN, BADGE_TAG_LENGTH_MAX)


# banner_color

def parse_banner_color(data):
    """
    Parses banner color from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        User data.
    
    Returns
    -------
    banner_color : `None | Color`
    """
    banner_color = data.get('brand_color_primary', None)
    if (banner_color is not None):
        banner_color = Color.from_html(banner_color)
    
    return banner_color


def put_banner_color(banner_color, data, defaults):
    """
    Serializes the given color into the given data.
    
    Parameters
    ----------
    banner_color : `None | Color`
        Banner color.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (banner_color is not None):
        if (banner_color is not None):
            banner_color = banner_color.as_html
        data['brand_color_primary'] = banner_color
    
    return data


def validate_banner_color(banner_color):
    """
    Validates the given `banner_color` value.
    
    Parameters
    ----------
    banner_color : `None | Color | value`
        The banner color to validate.
    
    Returns
    -------
    banner_color : `None | Color`
    
    Raises
    ------
    TypeError
        - If `banner_color` is not `None`, `Color`, `int`.
    ValueError
        - If `banner_color`'s value is out of the expected range.
    """
    if (banner_color is None):
        return None
    
    if isinstance(banner_color, Color):
        return banner_color
    
    if isinstance(banner_color, int):
        if banner_color < 0 or banner_color > 0xffffff:
            raise ValueError(
                f'`banner_color` can be between 0 and 0xffffff, got {banner_color!r}.'
            )
        
        return Color(banner_color)
    
    raise TypeError(
        f'`banner_color` can be `None`, `{Color.__name__}`, `int`, '
        f'got {type(banner_color).__name__}; {banner_color!r}.'
    )


# boost_count

parse_boost_count = int_parser_factory('premium_subscription_count', 0)
put_boost_count = int_optional_putter_factory('premium_subscription_count', 0)
validate_boost_count = int_conditional_validator_factory(
    'boost_count',
    0,
    lambda boost_count : boost_count >= 0,
    '>= 0',
)


# boost_level

parse_boost_level = int_parser_factory('premium_tier', 0)
put_boost_level = int_putter_factory('premium_tier')
validate_boost_level = int_options_validator_factory('boost_level', frozenset(LEVELS.keys()), 0)


# description

parse_description = nullable_string_parser_factory('description')
put_description = nullable_string_putter_factory('description')
validate_description = nullable_string_validator_factory('description', 0, DESCRIPTION_LENGTH_MAX)


# features

parse_features = preinstanced_array_parser_factory('features', GuildFeature)
put_features = preinstanced_array_putter_factory('features')
validate_features = preinstanced_array_validator_factory('features', GuildFeature)


# id

parse_id = entity_id_parser_factory('id')
put_id = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('guild_id')


# name

parse_name = force_string_parser_factory('name')
put_name = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)


# privacy_level

parse_privacy_level = preinstanced_parser_factory('visibility', PrivacyLevel, PrivacyLevel.guild_only)
put_privacy_level = preinstanced_putter_factory('visibility')
validate_privacy_level = preinstanced_validator_factory('privacy_level', PrivacyLevel)


# tags

def _tag_data_sort_key_getter(tag_data):
    """
    Sort key getter used to sort tag datas based on their position.
    
    Parameters
    ----------
    tag_data : `dict<str, object>`
        Tag data.
    
    Returns
    -------
    key : `int`
    """
    return tag_data['position']


def parse_tags(data):
    """
    Parses the tags from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    tags : `None | tuple<GuildActivityOverviewTag>`
    """
    tag_datas = data.get('traits', None)
    if (tag_datas is not None) and tag_datas:
        return (*(
            GuildActivityOverviewTag.from_data(tag_data)
            for tag_data in sorted(tag_datas, key = _tag_data_sort_key_getter)
        ),)


def put_tags(tags, data, defaults):
    """
    Puts tag into the given data.
    
    Parameters
    ----------
    tags : `None | tuple<GuildActivityOverviewTag>`
        Activities to serialize.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    tag_datas = []
    
    if (tags is not None):
        for index, guild_tag_overview_tag in enumerate(tags):
            tag_data = guild_tag_overview_tag.to_data(defaults = defaults)
            tag_data['position'] = index
            tag_datas.append(tag_data)
    
    data['traits'] = tag_datas
    return data


validate_tags = nullable_object_array_validator_factory('tags', GuildActivityOverviewTag)
