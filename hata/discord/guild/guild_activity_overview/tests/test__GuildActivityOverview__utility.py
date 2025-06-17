import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....core import BUILTIN_EMOJIS
from ....scheduled_event import PrivacyLevel

from ...guild import GuildFeature
from ...guild_activity_overview_activity import GuildActivityOverviewActivity, GuildActivityOverviewActivityLevel
from ...guild_activity_overview_tag import GuildActivityOverviewTag

from ..guild_activity_overview import GuildActivityOverview

from .test__GuildActivityOverview__construct import _assert_fields_set


def test__GuildActivityOverview__copy():
    """
    Tests whether ``GuildActivityOverview.copy`` works as intended.
    """
    activity_application_ids = [
        202504260070,
        202504260071,
    ]
    banner_color = Color.from_rgb(255, 12, 33)
    description = 'Rot in hell'
    discovery_splash = Icon(IconType.static, 3)
    icon = Icon(IconType.static, 2)
    name = '!!'
    privacy_level = PrivacyLevel.public
    tags = [
        GuildActivityOverviewTag(emoji = BUILTIN_EMOJIS['heart'], title = 'collecting'),
        GuildActivityOverviewTag(emoji = BUILTIN_EMOJIS['custard'], title = 'pudding'),
    ]
    
    guild_activity_overview = GuildActivityOverview(
        activity_application_ids = activity_application_ids,
        banner_color = banner_color,
        description = description,
        discovery_splash = discovery_splash,
        icon = icon,
        privacy_level = privacy_level,
        name = name,
        tags = tags,
    )
    
    copy = guild_activity_overview.copy()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, guild_activity_overview)
    vampytest.assert_eq(copy, guild_activity_overview)


def test__GuildActivityOverview__copy_with__no_fields():
    """
    Tests whether ``GuildActivityOverview.copy_with`` works as intended.
    
    Case: no fields given,
    """
    activity_application_ids = [
        202504260080,
        202504260081,
    ]
    banner_color = Color.from_rgb(255, 12, 33)
    description = 'Rot in hell'
    discovery_splash = Icon(IconType.static, 3)
    icon = Icon(IconType.static, 2)
    name = '!!'
    privacy_level = PrivacyLevel.public
    tags = [
        GuildActivityOverviewTag(emoji = BUILTIN_EMOJIS['heart'], title = 'collecting'),
        GuildActivityOverviewTag(emoji = BUILTIN_EMOJIS['custard'], title = 'pudding'),
    ]
    
    guild_activity_overview = GuildActivityOverview(
        activity_application_ids = activity_application_ids,
        banner_color = banner_color,
        description = description,
        discovery_splash = discovery_splash,
        icon = icon,
        privacy_level = privacy_level,
        name = name,
        tags = tags,
    )
    
    copy = guild_activity_overview.copy_with()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, guild_activity_overview)
    vampytest.assert_eq(copy, guild_activity_overview)


def test__GuildActivityOverview__copy_with__all_fields():
    """
    Tests whether ``GuildActivityOverview.copy_with`` works as intended.
    
    Case: no fields given,
    """
    old_activity_application_ids = [
        202504260090,
        202504260091,
    ]
    old_banner_color = Color.from_rgb(255, 12, 33)
    old_description = 'Rot in hell'
    old_discovery_splash = Icon(IconType.static, 3)
    old_icon = Icon(IconType.static, 2)
    old_name = '!!'
    old_privacy_level = PrivacyLevel.public
    old_tags = [
        GuildActivityOverviewTag(emoji = BUILTIN_EMOJIS['heart'], title = 'collecting'),
        GuildActivityOverviewTag(emoji = BUILTIN_EMOJIS['custard'], title = 'pudding'),
    ]
    
    new_activity_application_ids = [
        202504260100,
        202504260111,
    ]
    new_banner_color = Color.from_rgb(255, 12, 56)
    new_description = 'Gush'
    new_discovery_splash = Icon(IconType.animated, 3)
    new_icon = Icon(IconType.animated, 2)
    new_name = 'Hina'
    new_privacy_level = PrivacyLevel.guild_only
    new_tags = [
        GuildActivityOverviewTag(emoji = BUILTIN_EMOJIS['mushroom'], title = 'kirisame'),
        GuildActivityOverviewTag(emoji = BUILTIN_EMOJIS['brown_mushroom'], title = 'marisa'),
    ]
    
    guild_activity_overview = GuildActivityOverview(
        activity_application_ids = old_activity_application_ids,
        banner_color = old_banner_color,
        description = old_description,
        discovery_splash = old_discovery_splash,
        icon = old_icon,
        privacy_level = old_privacy_level,
        name = old_name,
        tags = old_tags,
    )
    
    copy = guild_activity_overview.copy_with(
        activity_application_ids = new_activity_application_ids,
        banner_color = new_banner_color,
        description = new_description,
        discovery_splash = new_discovery_splash,
        icon = new_icon,
        privacy_level = new_privacy_level,
        name = new_name,
        tags = new_tags,
        
    )
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, guild_activity_overview)
    vampytest.assert_ne(copy, guild_activity_overview)
    
    vampytest.assert_eq(copy.activity_application_ids, tuple(new_activity_application_ids))
    vampytest.assert_eq(copy.banner_color, new_banner_color)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.discovery_splash, new_discovery_splash)
    vampytest.assert_eq(copy.icon, new_icon)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.tags, tuple(new_tags))
    vampytest.assert_is(copy.privacy_level, new_privacy_level)


def _iter_options__iter_application_ids_and_activities_ordered():
    application_id_0 = 202504260150
    application_id_1 = 202504260151
    
    # Nothing
    yield (
        202504260200,
        None,
        None,
        [],
    )
    
    # only application ids
    yield (
        202504260201,
        [
            application_id_0,
            application_id_1,
        ],
        None,
        [
            (
                application_id_0,
                GuildActivityOverviewActivity._create_empty(),
            ),
            (
                application_id_1,
                GuildActivityOverviewActivity._create_empty(),
            ),
        ],
    )
    
    # we have 1 overview activity -> the defined one is always first
    yield (
        202504260202,
        [application_id_0, application_id_1],
        {
            application_id_1 : GuildActivityOverviewActivity(
                level = GuildActivityOverviewActivityLevel.any_previous,
                score = 12,
            ),
        },
        [
            (
                application_id_1,
                GuildActivityOverviewActivity(
                    level = GuildActivityOverviewActivityLevel.any_previous,
                    score = 12,
                ),
            ),
            (
                application_id_0,
                GuildActivityOverviewActivity._create_empty(),
            ),
        ],
    )
    
    # we have 2 overview activity -> higher level first
    yield (
        202504260203,
        [application_id_0, application_id_1],
        {
            application_id_0 : GuildActivityOverviewActivity(
                level = GuildActivityOverviewActivityLevel.any_previous,
                score = 12,
            ),
            application_id_1 : GuildActivityOverviewActivity(
                level = GuildActivityOverviewActivityLevel.recently_popular,
                score = 10,
            ),
        },
        [
            (
                application_id_1,GuildActivityOverviewActivity(
                    level = GuildActivityOverviewActivityLevel.recently_popular,
                    score = 10,
                ),
            ),
            (
                application_id_0,GuildActivityOverviewActivity(
                    level = GuildActivityOverviewActivityLevel.any_previous,
                    score = 12,
                ),
            ),
        ],
    )
    
    # we have 2 overview activity -> higher score first
    yield (
        202504260204,
        [application_id_0, application_id_1],
        {
            application_id_0 : GuildActivityOverviewActivity(
                level = GuildActivityOverviewActivityLevel.recently_popular,
                score = 12,
            ),
            application_id_1 : GuildActivityOverviewActivity(
                level = GuildActivityOverviewActivityLevel.recently_popular,
                score = 14,
            ),
        },
        [
            (
                application_id_1,GuildActivityOverviewActivity(
                    level = GuildActivityOverviewActivityLevel.recently_popular,
                    score = 14,
                ),
            ),
            (
                application_id_0,GuildActivityOverviewActivity(
                    level = GuildActivityOverviewActivityLevel.recently_popular,
                    score = 12,
                ),
            ),
        ],
    )
    
    # we have 2 overview activity -> both same, but first in order should be first in output
    yield (
        202504260205,
        [application_id_0, application_id_1],
        {
            application_id_0 : GuildActivityOverviewActivity(
                level = GuildActivityOverviewActivityLevel.recently_popular,
                score = 12,
            ),
            application_id_1 : GuildActivityOverviewActivity(
                level = GuildActivityOverviewActivityLevel.recently_popular,
                score = 12,
            ),
        },
        [
            (
                application_id_0,GuildActivityOverviewActivity(
                    level = GuildActivityOverviewActivityLevel.recently_popular,
                    score = 12,
                ),
            ),
            (
                application_id_1,GuildActivityOverviewActivity(
                    level = GuildActivityOverviewActivityLevel.recently_popular,
                    score = 12,
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_application_ids_and_activities_ordered()).returning_last())
def test__GuildActivityOverview__iter_application_ids_and_activities_ordered(
    guild_id, activity_application_ids, activities
):
    """
    Tests whether ``GuildActivityOverview.iter_application_ids_and_activities_ordered`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to create instance with.
    
    activity_application_ids : `None | list<int>`
        Application identifiers of activities to be shown.
    
    activities : ``None | dict<int, GuildActivityOverviewActivity>``
        An application identifier to an activity overview relation.
    
    Returns
    --------
    output : ``list<(int, GuildActivityOverviewActivity)>``
    """
    guild_activity_overview = GuildActivityOverview.precreate(
        guild_id,
        activities = activities,
        activity_application_ids = activity_application_ids,
    )
    
    output = [*guild_activity_overview.iter_application_ids_and_activities_ordered()]
    
    for element in output:
        vampytest.assert_instance(element, tuple)
        vampytest.assert_eq(len(element), 2)
        vampytest.assert_instance(element[0], int)
        vampytest.assert_instance(element[1], GuildActivityOverviewActivity)
    
    return output


def _iter_options__iter_activity_application_ids():
    application_id_0 = 202504260160
    application_id_1 = 202504260161
    
    yield (
        202504260210,
        None,
        [],
    )
    
    yield (
        202504260211,
        [application_id_0, application_id_1],
        [application_id_0, application_id_1],
    )
    
    # Keep order since we use it at sorting activities.
    yield (
        202504260212,
        [application_id_1, application_id_0],
        [application_id_1, application_id_0],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_activity_application_ids()).returning_last())
def test__GuildActivityOverview__iter_activity_application_ids(guild_id, activity_application_ids):
    """
    Tests whether ``GuildActivityOverview.iter_activity_application_ids`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to create instance with.
    
    activity_application_ids : `None | list<int>`
        Application identifiers of activities to be shown.
    
    Returns
    --------
    output : `list<int>`
    """
    guild_activity_overview = GuildActivityOverview.precreate(
        guild_id,
        activity_application_ids = activity_application_ids,
    )
    
    output = [*guild_activity_overview.iter_activity_application_ids()]
    
    for element in output:
        vampytest.assert_instance(element, int)
    
    return output


def _iter_options__iter_features():
    guild_feature_0 = GuildFeature.banner
    guild_feature_1 = GuildFeature.commerce
    
    yield (
        202504260220,
        None,
        set(),
    )
    
    yield (
        202504260221,
        [guild_feature_0, guild_feature_1],
        {guild_feature_0, guild_feature_1},
    )


@vampytest._(vampytest.call_from(_iter_options__iter_features()).returning_last())
def test__GuildActivityOverview__iter_features(guild_id, features):
    """
    Tests whether ``GuildActivityOverview.iter_features`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to create instance with.
    
    features : `None | list<int>`
        Application identifiers of activities to be shown.
    
    Returns
    --------
    output : ``set<GuildFeature>``
    """
    guild_activity_overview = GuildActivityOverview.precreate(
        guild_id,
        features = features,
    )
    
    output = {*guild_activity_overview.iter_features()}
    
    for element in output:
        vampytest.assert_instance(element, GuildFeature)
    
    return output


def _iter_options__iter_tags():
    guild_tag_0 = GuildActivityOverviewTag(emoji = BUILTIN_EMOJIS['heart'], title = 'collecting')
    guild_tag_1 = GuildActivityOverviewTag(emoji = BUILTIN_EMOJIS['custard'], title = 'pudding')
    
    yield (
        2025042602230,
        None,
        [],
    )
    
    yield (
        202504260231,
        [guild_tag_0, guild_tag_1],
        [guild_tag_0, guild_tag_1],
    )
    
    # tags should keep their order.
    yield (
        202504260232,
        [guild_tag_1, guild_tag_0],
        [guild_tag_1, guild_tag_0],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_tags()).returning_last())
def test__GuildActivityOverview__iter_tags(guild_id, tags):
    """
    Tests whether ``GuildActivityOverview.iter_tags`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to create instance with.
    
    tags : `None | list<int>`
        Application identifiers of activities to be shown.
    
    Returns
    --------
    output : ``list<GuildActivityOverviewTag>``
    """
    guild_activity_overview = GuildActivityOverview.precreate(
        guild_id,
        tags = tags,
    )
    
    output = [*guild_activity_overview.iter_tags()]
    
    for element in output:
        vampytest.assert_instance(element, GuildActivityOverviewTag)
    
    return output


def _iter_options__icon_url():
    yield 202505280030, None, False
    yield 202505280031, Icon(IconType.animated, 5), True


@vampytest._(vampytest.call_from(_iter_options__icon_url()).returning_last())
def test__GuildActivityOverview__icon_url(guild_id, icon):
    """
    Tests whether ``GuildActivityOverview.icon_url`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Identifier to create guild with.
    
    icon : ``None | Icon``
        Icon to create the guild with.
    
    Returns
    -------
    has_icon_url : `bool`
    """
    guild = GuildActivityOverview.precreate(
        guild_id,
        icon = icon,
    )
    
    output = guild.icon_url
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__icon_url_as():
    yield 202505280040, None, {'ext': 'webp', 'size': 128}, False
    yield 202505280041, Icon(IconType.animated, 5), {'ext': 'webp', 'size': 128}, True


@vampytest._(vampytest.call_from(_iter_options__icon_url_as()).returning_last())
def test__GuildActivityOverview__icon_url_as(guild_id, icon, keyword_parameters):
    """
    Tests whether ``GuildActivityOverview.icon_url_as`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Identifier to create guild with.
    
    icon : ``None | Icon``
        Icon to create the guild with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    has_icon_url : `bool`
    """
    guild = GuildActivityOverview.precreate(
        guild_id,
        icon = icon,
    )
    
    output = guild.icon_url_as(**keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__discovery_splash_url():
    yield 202505290012, None, False
    yield 202505290013, Icon(IconType.animated, 5), True


@vampytest._(vampytest.call_from(_iter_options__discovery_splash_url()).returning_last())
def test__GuildActivityOverview__discovery_splash_url(guild_id, icon):
    """
    Tests whether ``GuildActivityOverview.discovery_splash_url`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Identifier to create guild with.
    
    icon : ``None | Icon``
        Icon to create the guild with.
    
    Returns
    -------
    has_discovery_splash_url : `bool`
    """
    guild = GuildActivityOverview.precreate(
        guild_id,
        discovery_splash = icon,
    )
    
    output = guild.discovery_splash_url
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__discovery_splash_url_as():
    yield 202505290014, None, {'ext': 'webp', 'size': 128}, False
    yield 202505290015, Icon(IconType.animated, 5), {'ext': 'webp', 'size': 128}, True


@vampytest._(vampytest.call_from(_iter_options__discovery_splash_url_as()).returning_last())
def test__GuildActivityOverview__discovery_splash_url_as(guild_id, icon, keyword_parameters):
    """
    Tests whether ``GuildActivityOverview.discovery_splash_url_as`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Identifier to create guild with.
    
    icon : ``None | Icon``
        Icon to create the guild with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    has_discovery_splash_url : `bool`
    """
    guild = GuildActivityOverview.precreate(
        guild_id,
        discovery_splash = icon,
    )
    
    output = guild.discovery_splash_url_as(**keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__badge_icon_url():
    yield 202505310030, None, False
    yield 202505310031, Icon(IconType.animated, 5), True


@vampytest._(vampytest.call_from(_iter_options__badge_icon_url()).returning_last())
def test__GuildActivityOverview__badge_icon_url(guild_id, icon):
    """
    Tests whether ``GuildActivityOverview.badge_icon_url`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Identifier to create guild with.
    
    icon : ``None | Icon``
        Icon to create the guild with.
    
    Returns
    -------
    has_badge_icon_url : `bool`
    """
    guild = GuildActivityOverview.precreate(
        guild_id,
        badge_icon = icon,
    )
    
    output = guild.badge_icon_url
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__badge_icon_url_as():
    yield 202505310032, None, {'ext': 'webp', 'size': 128}, False
    yield 202505310033, Icon(IconType.animated, 5), {'ext': 'webp', 'size': 128}, True


@vampytest._(vampytest.call_from(_iter_options__badge_icon_url_as()).returning_last())
def test__GuildActivityOverview__badge_icon_url_as(guild_id, icon, keyword_parameters):
    """
    Tests whether ``GuildActivityOverview.badge_icon_url_as`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Identifier to create guild with.
    
    icon : ``None | Icon``
        Icon to create the guild with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    has_badge_icon_url : `bool`
    """
    guild = GuildActivityOverview.precreate(
        guild_id,
        badge_icon = icon,
    )
    
    output = guild.badge_icon_url_as(**keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)
