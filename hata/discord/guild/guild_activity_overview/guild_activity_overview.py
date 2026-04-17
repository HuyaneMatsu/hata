__all__ = ('GuildActivityOverview',)

from ...bases import DiscordEntity, IconSlot
from ...http.urls import (
    build_guild_badge_icon_url, build_guild_badge_icon_url_as, build_guild_discovery_splash_url,
    build_guild_discovery_splash_url_as, build_guild_icon_url, build_guild_icon_url_as
)
from ...precreate_helpers import process_precreate_parameters_and_raise_extra
from ...scheduled_event import PrivacyLevel

from ..guild_activity_overview_activity import GuildActivityOverviewActivity, GuildActivityOverviewActivityLevel

from .fields import (
    parse_activities, parse_activity_application_ids, parse_approximate_online_count, parse_approximate_user_count,
    parse_badge, parse_badge_color_primary, parse_badge_color_secondary, parse_badge_tag, parse_banner_color,
    parse_boost_count, parse_boost_level, parse_description, parse_features, parse_id, parse_name, parse_privacy_level,
    parse_tags, put_activities, put_activity_application_ids, put_approximate_online_count, put_approximate_user_count,
    put_badge, put_badge_color_primary, put_badge_color_secondary, put_badge_tag, put_banner_color, put_boost_count,
    put_boost_level, put_description, put_features, put_id, put_name, put_privacy_level, put_tags, validate_activities,
    validate_activity_application_ids, validate_approximate_online_count, validate_approximate_user_count,
    validate_badge, validate_badge_color_primary, validate_badge_color_secondary, validate_badge_tag,
    validate_banner_color, validate_boost_count, validate_boost_level, validate_description, validate_features,
    validate_id, validate_name, validate_privacy_level, validate_tags, 
)

GUILD_ACTIVITY_OVERVIEW_BADGE_ICON = IconSlot('badge_icon', 'badge_hash')
GUILD_ACTIVITY_OVERVIEW_DISCOVERY_SPLASH = IconSlot('discovery_splash', 'custom_banner_hash')
GUILD_ACTIVITY_OVERVIEW_ICON = IconSlot('icon', 'icon')


PRECREATE_FIELDS = {
    'activities' : ('activities', validate_activities),
    'activity_application_ids' : ('activity_application_ids', validate_activity_application_ids),
    'approximate_online_count' : ('approximate_online_count', validate_approximate_online_count),
    'approximate_user_count' : ('approximate_user_count', validate_approximate_user_count),
    'badge' : ('badge', validate_badge),
    'badge_color_primary' : ('badge_color_primary', validate_badge_color_primary),
    'badge_color_secondary' : ('badge_color_secondary', validate_badge_color_secondary),
    'badge_icon': ('badge_icon', GUILD_ACTIVITY_OVERVIEW_BADGE_ICON.validate_icon),
    'badge_tag' : ('badge_tag', validate_badge_tag),
    'banner_color': ('banner_color', validate_banner_color),
    'boost_count' : ('boost_count', validate_boost_count),
    'boost_level' : ('boost_level', validate_boost_level),
    'description' : ('description', validate_description),
    'discovery_splash': ('discovery_splash', GUILD_ACTIVITY_OVERVIEW_DISCOVERY_SPLASH.validate_icon),
    'features' : ('features', validate_features),
    'icon' : ('icon', GUILD_ACTIVITY_OVERVIEW_ICON.validate_icon),
    'name' : ('name', validate_name),
    'privacy_level': ('privacy_level', validate_privacy_level),
    'tags' : ('tags', validate_tags),
}



def _application_id_and_activity_sort_key_getter(item):
    """
    Sort key getter used when sorting ``GuildActivityOverviewActivity``-s in display order.
    
    Parameters
    ----------
    item : ``((int, int, int), (int, GuildActivityOverviewActivity))``
        Item to get key of.
    
    Returns
    -------
    key : `(int, int, int)`
    """
    return item[0]


class GuildActivityOverview(DiscordEntity):
    """
    Represents a guild's activity's overview.
    
    Attributes
    ----------
    activities : `None | dict<int, GuildActivityOverviewActivity>`
        An application identifier to an activity overview relation.
        Its application identifiers are a subset of the ones mentioned in ``.activity_application_ids``.
    
    activity_application_ids : `None | tuple<int>`
        Application identifiers of activities to be shown.
    
    approximate_online_count : `int`
        Approximate amount of online users at the represented guild.
    
    approximate_user_count : `int`
        Approximate amount of users at the represented guild.
    
    badge : `int`
        Unknown type or flag field.
        
        `0` means no badge. Likely values: `0`, `2`, `6`, `7`.
    
    badge_color_primary : `None | Color`
        Auto generated primary banner color.
    
    badge_color_secondary : `None | Color`
        Auto generated secondary banner color.
    
    badge_icon_hash : `int`
        The guild's badge icon's hash in `uint128`.
    
    badge_icon_type : ``IconType``
        The guild's badge icon's type.
    
    badge_tag : `str`
        The guild's badge tag.
    
    banner_color : `None | Color`
        Banner color.
    
    boost_count : `int`
        The amount of boosts the represented guild has.
    
    boost_level : `int`
        The boost level of the represented guild.
    
    description : `None | str`
        Description of the represented guild.
    
    discovery_splash_hash : `int`
        The guild's discovery splash's hash in `uint128`.
    
    discovery_splash_type : ``IconType``
        The guild's discovery splash's type.
    
    features :  ``None | tuple<GuildFeature>``
        The represented guild's public features.
    
    icon_hash : `int`
        The guild's icon's hash in `uint128`.
    
    icon_type : ``IconType``
        The guild's icon's type.
    
    id : `int`
        The represented guild's identifier.
    
    name : `str`
        Name of the represented guild.
    
    privacy_level : ``PrivacyLevel``
        For who is the guild overview visible for and other related information.
    
    tags : ``None | tuple<GuildActivityOverviewTag>``
        Additional tags assigned to the guild.
    """
    __slots__ = (
        'activities', 'activity_application_ids', 'approximate_online_count', 'approximate_user_count',
        'badge', 'badge_color_primary', 'badge_color_secondary', 'badge_tag', 'banner_color', 'boost_count',
        'boost_level', 'description', 'features', 'name', 'privacy_level', 'tags'
    )
    
    discovery_splash = GUILD_ACTIVITY_OVERVIEW_DISCOVERY_SPLASH
    icon = GUILD_ACTIVITY_OVERVIEW_ICON
    badge_icon = GUILD_ACTIVITY_OVERVIEW_BADGE_ICON
    
    def __new__(
        cls,
        *,
        activity_application_ids = ...,
        banner_color = ...,
        description = ...,
        discovery_splash = ...,
        icon = ...,
        name = ...,
        privacy_level = ...,
        tags = ...,
    ):
        """
        Creates a new guild overview.
        
        Parameters
        ----------
        activity_application_ids : ``None | iterable<Application> | iterable<int>``, Optional (Keyword only)
            Application identifiers of activities to be shown.
        
        banner_color : `None | Color | int`, Optional (Keyword only)
            Banner color.
        
        description : `None | str`, Optional (Keyword only)
            Description of the represented guild.
        
        discovery_splash : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The represented guild's discovery splash.
        
        icon : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The represented guild's icon.
        
        name : `str`, Optional (Keyword only)
            Name of the represented guild.
        
        privacy_level : ``None | int | PrivacyLevel``, Optional (Keyword only)
            For who is the guild overview visible for and other related information.
        
        tags : ``None | iterable<GuildActivityOverviewTag>``, Optional (Keyword only)
            Additional tags assigned to the guild.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value in incorrect.
        """
        # activity_application_ids
        if activity_application_ids is ...:
            activity_application_ids = None
        else:
            activity_application_ids = validate_activity_application_ids(activity_application_ids)
        
        # banner_color
        if banner_color is ...:
            banner_color = None
        else:
            banner_color = validate_banner_color(banner_color)
        
        # description
        if description is ...:
            description = None
        else:
            description = validate_description(description)
        
        # discovery_splash
        if discovery_splash is ...:
            discovery_splash = None
        else:
            discovery_splash = cls.discovery_splash.validate_icon(discovery_splash, allow_data = True)
        
        # icon
        if icon is ...:
            icon = None
        else:
            icon = cls.icon.validate_icon(icon, allow_data = True)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # privacy_level
        if privacy_level is ...:
            privacy_level = PrivacyLevel.guild_only
        else:
            privacy_level = validate_privacy_level(privacy_level)
        
        # tags
        if tags is ...:
            tags = None
        else:
            tags = validate_tags(tags)
        
        # Construct
        self = object.__new__(cls)
        self.activities = None
        self.activity_application_ids = activity_application_ids
        self.approximate_online_count = 0
        self.approximate_user_count = 0
        self.badge = 0
        self.badge_color_primary = None
        self.badge_color_secondary = None
        self.badge_icon = None
        self.badge_tag = ''
        self.banner_color = banner_color
        self.boost_count = 0
        self.boost_level = 0
        self.description = description
        self.discovery_splash = discovery_splash
        self.features = None
        self.icon = icon
        self.id = 0
        self.name = name
        self.privacy_level = privacy_level
        self.tags = tags
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        field_added = False
        
        # activities
        activities = self.activities
        if (activities is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' activities = ')
            repr_parts.append(repr(self.activities))
        
        activity_application_ids = self.activity_application_ids
        if (activity_application_ids is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            # activity_application_ids
            repr_parts.append(' activity_application_ids = ')
            repr_parts.append(repr(self.activity_application_ids))
        
        # approximate_online_count & approximate_user_count
        approximate_online_count = self.approximate_online_count
        approximate_user_count = self.approximate_user_count
        if approximate_online_count or approximate_user_count:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            # approximate_online_count
            repr_parts.append(' approximate_online_count = ')
            repr_parts.append(repr(self.approximate_online_count))
            
            # approximate_user_count
            repr_parts.append(', approximate_user_count = ')
            repr_parts.append(repr(self.approximate_user_count))
        
        # badge
        badge = self.badge
        if badge:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            # badge
            repr_parts.append(' badge = ')
            repr_parts.append(repr(badge))
        
        # badge_color_primary
        badge_color_primary = self.badge_color_primary
        if (badge_color_primary is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            # badge_color_primary
            repr_parts.append(' badge_color_primary = ')
            repr_parts.append(repr(badge_color_primary))
        
        # badge_color_secondary
        badge_color_secondary = self.badge_color_secondary
        if (badge_color_secondary is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            # badge_color_secondary
            repr_parts.append(' badge_color_secondary = ')
            repr_parts.append(repr(badge_color_secondary))
        
        # badge_icon
        badge_icon = self.badge_icon
        if badge_icon:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' badge_icon = ')
            repr_parts.append(repr(badge_icon))
        
        # badge_tag
        badge_tag = self.badge_tag
        if badge_tag:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' badge_tag = ')
            repr_parts.append(repr(badge_tag))
        
        # banner_color
        banner_color = self.banner_color
        if (banner_color is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' banner_color = ')
            repr_parts.append(repr(banner_color))
        
        # boost_count
        boost_count = self.boost_count
        if boost_count:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' boost_count = ')
            repr_parts.append(repr(boost_count))
        
        # boost_level
        boost_level = self.boost_level
        if boost_level:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' boost_level = ')
            repr_parts.append(repr(boost_level))
        
        # description
        description = self.description
        if (description is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' description = ')
            repr_parts.append(repr(description))
        
        # discovery_splash
        discovery_splash = self.discovery_splash
        if discovery_splash:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' discovery_splash = ')
            repr_parts.append(repr(discovery_splash))
        
        # features
        features = self.features
        if (features is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' features = ')
            repr_parts.append(repr(features))
        
        # icon
        icon = self.icon
        if icon:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' icon = ')
            repr_parts.append(repr(icon))
        
        # id
        guild_id = self.id
        if guild_id:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' id = ')
            repr_parts.append(repr(guild_id))
        
        # name
        name = self.name
        if name:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' name = ')
            repr_parts.append(repr(name))
        
        # privacy_level
        privacy_level = self.privacy_level
        if privacy_level:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' privacy_level = ')
            repr_parts.append(privacy_level.name)
            repr_parts.append(' ~ ')
            repr_parts.append(repr(privacy_level.value))
        
        # tags
        tags = self.tags
        if tags:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' tags = ')
            repr_parts.append(repr(tags))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # activities
        activities = self.activities
        if (activities is not None):
            hash_value ^= len(activities) << 8
            for application_id, activity in activities.items():
                hash_value ^= application_id & hash(activity)
        
        # activity_application_ids
        activity_application_ids = self.activity_application_ids
        if (activity_application_ids is not None):
            hash_value ^= len(activity_application_ids) << 9
            for application_id in activity_application_ids:
                hash_value ^= application_id
        # approximate_online_count
        approximate_online_count = self.approximate_online_count
        if approximate_online_count:
            hash_value ^= 1 << 20
            hash_value ^= approximate_online_count
        
        # approximate_user_count
        approximate_user_count = self.approximate_user_count
        if approximate_user_count:
            hash_value ^= 1 << 21
            hash_value ^= approximate_user_count
        
        # badge
        badge = self.badge
        if badge:
            hash_value ^= 1 << 21
            hash_value ^= badge
        
        # badge_color_primary
        badge_color_primary = self.badge_color_primary
        if (badge_color_primary is not None):
            hash_value ^= 1 << 10
            hash_value ^= badge_color_primary
        
        # badge_color_secondary
        badge_color_secondary = self.badge_color_secondary
        if (badge_color_secondary is not None):
            hash_value ^= 1 << 23
            hash_value ^= badge_color_secondary
        
        # badge_icon
        badge_icon = self.badge_icon
        if badge_icon:
            hash_value ^= 1 << 18
            hash_value ^= hash(badge_icon)
        
        # badge_tag
        badge_tag = self.badge_tag
        if (badge_tag is not None):
            hash_value ^= 1 << 19
            hash_value ^= hash(badge_tag)
        
        # banner_color
        banner_color = self.banner_color
        if (banner_color is not None):
            hash_value ^= 1 << 24
            hash_value ^= banner_color
        
        # boost_count
        boost_count = self.boost_count
        if boost_count:
            hash_value ^= 1 << 11
            hash_value ^= boost_count
        
        # boost_level
        boost_level = self.boost_level
        if boost_level:
            hash_value ^= 1 << 12
            hash_value ^= boost_level
        
        # description
        description = self.description
        if (description is not None):
            hash_value ^= 1 << 13
            hash_value ^= hash(description)
        
        # discovery_splash
        discovery_splash = self.discovery_splash
        if discovery_splash:
            hash_value ^= 1 << 22
            hash_value ^= hash(discovery_splash)
        
        # features
        features = self.features
        if (features is not None):
            hash_value ^= len(features) << 14
            for feature in features:
                hash_value ^= hash(feature)
        
        # icon
        icon = self.icon
        if icon:
            hash_value ^= 1 << 15
            hash_value ^= hash(icon)
        
        # id -> skip
        
        # name
        name = self.name
        if name:
            hash_value ^= 1 << 16
            hash_value ^= hash(name)
        
        # privacy_level
        hash_value ^= hash(self.privacy_level)
        
        # tags
        tags = self.tags
        if (tags is not None):
            hash_value ^= len(tags) << 17
            for tag in tags:
                hash_value ^= hash(tag)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns self != other."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether self equals to other. Other must be the same type as wel.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance.
        
        Returns
        -------
        is_equal : `bool`
        """
        # id
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            if self_id != other_id:
                return False
            
            # activities
            if self.activities != other.activities:
                return False
            
            # approximate_online_count
            if self.approximate_online_count != other.approximate_online_count:
                return False
            
            # approximate_user_count
            if self.approximate_user_count != other.approximate_user_count:
                return False
            
            # badge
            if self.badge != other.badge:
                return False
            
            # badge_color_primary
            if self.badge_color_primary != other.badge_color_primary:
                return False
            
            # badge_color_secondary
            if self.badge_color_secondary != other.badge_color_secondary:
                return False
            
            # badge_icon
            if self.badge_icon != other.badge_icon:
                return False
            
            # badge_tag
            if self.badge_tag != other.badge_tag:
                return False
            
            # boost_count
            if self.boost_count != other.boost_count:
                return False
            
            # boost_level
            if self.boost_level != other.boost_level:
                return False
            
            # features
            if self.features != other.features:
                return False
        
        # activity_application_ids
        if self.activity_application_ids != other.activity_application_ids:
            return False
        
        # banner_color
        if self.banner_color != other.banner_color:
            return False
        
        # description
        if self.description != other.description:
            return False
        
        # discovery_splash
        if self.discovery_splash != other.discovery_splash:
            return False
        
        # icon
        if self.icon != other.icon:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # privacy_level
        if self.privacy_level is not other.privacy_level:
            return False
        
        # tags
        if self.tags != other.tags:
            return False
        
        return True
        
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new information.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Channel data receive from Discord.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.activities = parse_activities(data)
        self.activity_application_ids = parse_activity_application_ids(data)
        self.approximate_online_count = parse_approximate_online_count(data)
        self.approximate_user_count = parse_approximate_user_count(data)
        self.badge = parse_badge(data)
        self.badge_color_primary = parse_badge_color_primary(data)
        self.badge_color_secondary = parse_badge_color_secondary(data)
        self._set_badge_icon(data)
        self.badge_tag = parse_badge_tag(data)
        self.banner_color = parse_banner_color(data)
        self.boost_count = parse_boost_count(data)
        self.boost_level = parse_boost_level(data)
        self.description = parse_description(data)
        self._set_discovery_splash(data)
        self.features = parse_features(data)
        self._set_icon(data)
        self.id = parse_id(data)
        self.name = parse_name(data)
        self.privacy_level = parse_privacy_level(data)
        self.tags = parse_tags(data)
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Serializes the guild overview.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal field values should be included.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        
        put_activity_application_ids(self.activity_application_ids, data, defaults)
        put_banner_color(self.banner_color, data, defaults)
        put_description(self.description, data, defaults)
        type(self).discovery_splash.put_into(self.discovery_splash, data, defaults, as_data = not include_internals)
        type(self).icon.put_into(self.icon, data, defaults, as_data = not include_internals)
        put_name(self.name, data, defaults)
        put_privacy_level(self.privacy_level, data, defaults)
        put_tags(self.tags, data, defaults)
        
        if include_internals:
            put_activities(self.activities, data, defaults)
            put_approximate_online_count(self.approximate_online_count, data, defaults)
            put_approximate_user_count(self.approximate_user_count, data, defaults)
            put_badge(self.badge, data, defaults)
            put_badge_color_primary(self.badge_color_primary, data, defaults)
            put_badge_color_secondary(self.badge_color_secondary, data, defaults)
            type(self).badge_icon.put_into(self.badge_icon, data, defaults, as_data = not include_internals)
            put_badge_tag(self.badge_tag, data, defaults)
            put_boost_count(self.boost_count, data, defaults)
            put_boost_level(self.boost_level, data, defaults)
            put_features(self.features, data, defaults)
            put_id(self.id, data, defaults)
        
        return data
    
    
    @classmethod
    def _create_empty(cls, guild_id):
        """
        Creates an empty guild activity overview with the given fields.
        
        Parameters
        ----------
        guild_id : `int`
            Guild identifier to create the guild activity overview with.
        
        Returns
        -------
        self : `instance<cls>`
        """
        # Construct
        self = object.__new__(cls)
        self.activities = None
        self.activity_application_ids = None
        self.approximate_online_count = 0
        self.approximate_user_count = 0
        self.badge = 0
        self.badge_color_primary = None
        self.badge_color_secondary = None
        self.badge_icon = None
        self.badge_tag = ''
        self.banner_color = None
        self.boost_count = 0
        self.boost_level = 0
        self.description = None
        self.discovery_splash = None
        self.features = None
        self.icon = None
        self.id = guild_id
        self.name = ''
        self.privacy_level = PrivacyLevel.guild_only
        self.tags = None
        return self
    
    
    @classmethod
    def precreate(cls, guild_id, **keyword_parameters):
        """
        Creates a guild activity overview instance.
        Since these objects are not cached, the only advantage of using ``.precreate`` is that it allows setting
        ``.id`` and various other fields that cannot be used for templating.
        
        Parameters
        ----------
        guild_id : `int`
            The represented guild's identifier.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        activities : `None | dict<int, GuildActivityOverviewActivity>`, Optional (Keyword only)
            An application identifier to an activity overview relation.
        
        activity_application_ids : ``None | iterable<Application> | iterable<int>``, Optional (Keyword only)
            Application identifiers of activities to be shown.
        
        approximate_online_count : `None | int`, Optional (Keyword only)
            Approximate amount of online users at the represented guild.
        
        approximate_user_count : `None | int`, Optional (Keyword only)
            Approximate amount of users at the represented guild.
        
        badge : `None | int`, Optional (Keyword only)
            Unknown type or flag field.
        
        badge_color_primary : `None | int | Color`, Optional (Keyword only)
            Auto generated primary banner color.
        
        badge_color_secondary : `None | int | Color`, Optional (Keyword only)
            Auto generated secondary banner color.
        
        badge_icon : ``None | str | Icon``, Optional (Keyword only)
            The guild's badge icon.
        
        badge_tag : `None | str`, Optional (Keyword only)
            The guild's badge tag.
        
        banner_color : `None | int | Color`, Optional (Keyword only)
            Banner color.
        
        boost_count : `None | int`, Optional (Keyword only)
            The amount of boosts the represented guild has.
        
        boost_level : `None | int`, Optional (Keyword only)
            The boost level of the represented guild.
        
        description : `None | str`, Optional (Keyword only)
            Description of the represented guild.
        
        discovery_splash : ``None | str | Icon``, Optional (Keyword only)
            The represented guild's discovery splash.
        
        features : `None | iterable<GuildFeature> | iterable<str>``, Optional (Keyword only)
            The represented guild's features.
        
        icon : ``None | str | Icon``, Optional (Keyword only)
            The guild's icon.
        
        name : `str`, Optional (Keyword only)
            The represented guild's name.
        
        privacy_level : ``None | int | PrivacyLevel``, Optional (Keyword only)
            For who is the guild overview visible for and other related information.
        
        tags : ``None | iterable<GuildActivityOverviewTag>``, Optional (Keyword only)
            Additional tags assigned to the guild.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - if a parameter's value is incorrect.
        """
        guild_id = validate_id(guild_id)
        
        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        self = cls._create_empty(guild_id)
        
        if (processed is not None):
            for name, value in processed:
                setattr(self, name, value)
        
        return self
    
    
    def copy(self):
        """
        Copies the guild overview.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.activities = None
        
        activity_application_ids = self.activity_application_ids
        if (activity_application_ids is not None):
            activity_application_ids = (*activity_application_ids,)
        new.activity_application_ids = activity_application_ids
        
        new.approximate_online_count = 0
        new.approximate_user_count = 0
        new.badge = 0
        new.badge_color_primary = None
        new.badge_color_secondary = None
        new.badge_icon = None
        new.badge_tag = ''
        new.banner_color = self.banner_color
        new.boost_count = 0
        new.boost_level = 0
        new.description = self.description
        new.discovery_splash = self.discovery_splash
        new.features = None
        new.icon = self.icon
        new.id = 0
        new.name = self.name
        new.privacy_level = self.privacy_level
        
        tags = self.tags
        if (tags is not None):
            tags = (*(tag.copy() for tag in tags),)
        new.tags = tags
        
        return new
    
    
    def copy_with(
        self,
        *,
        activity_application_ids = ...,
        banner_color = ...,
        description = ...,
        discovery_splash = ...,
        icon = ...,
        name = ...,
        tags = ...,
        privacy_level = ...,
    ):
        """
        Copies the guild overview with the given fields.
        
        Parameters
        ----------
        activity_application_ids : ``None | iterable<Application> | iterable<int>``, Optional (Keyword only)
            Application identifiers of activities to be shown.
        
        banner_color : `None | Color | int`, Optional (Keyword only)
            Banner color.
        
        description : `None | str`, Optional (Keyword only)
            Description of the represented guild.
        
        discovery_splash : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The represented guild's discovery splash.
        
        icon : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The represented guild's icon.
        
        name : `str`, Optional (Keyword only)
            The name of the represented guild.
        
        tags : ``None | iterable<GuildActivityOverviewTag>``, Optional (Keyword only)
            Additional tags assigned to the guild.
        
        privacy_level : ``None | int | PrivacyLevel``, Optional (Keyword only)
            For who is the guild overview visible for and other related information.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value in incorrect.
        """
        # activity_application_ids
        if activity_application_ids is ...:
            activity_application_ids = self.activity_application_ids
            if (activity_application_ids is not None):
                activity_application_ids = (*activity_application_ids,)
        else:
            activity_application_ids = validate_activity_application_ids(activity_application_ids)
        
        # banner_color
        if banner_color is ...:
            banner_color = self.banner_color
        else:
            banner_color = validate_banner_color(banner_color)
        
        # description
        if description is ...:
            description = self.description
        else:
            description = validate_description(description)
        
        # discovery_splash
        if discovery_splash is ...:
            discovery_splash = self.discovery_splash
        else:
            discovery_splash = type(self).discovery_splash.validate_icon(discovery_splash, allow_data = True)
        
        # icon
        if icon is ...:
            icon = self.icon
        else:
            icon = type(self).icon.validate_icon(icon, allow_data = True)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # tags
        if tags is ...:
            tags = self.tags
            if (tags is not None):
                tags = (*(tag.copy() for tag in tags),)
        else:
            tags = validate_tags(tags)
        
        # privacy_level
        if privacy_level is ...:
            privacy_level = self.privacy_level
        else:
            privacy_level = validate_privacy_level(privacy_level)
        
        # Construct
        new = object.__new__(type(self))
        new.activities = None
        new.activity_application_ids = activity_application_ids
        new.approximate_online_count = 0
        new.approximate_user_count = 0
        new.badge = 0
        new.badge_color_primary = None
        new.badge_color_secondary = None
        new.badge_icon = None
        new.badge_tag = ''
        new.banner_color = banner_color
        new.boost_count = 0
        new.boost_level = 0
        new.description = description
        new.discovery_splash = discovery_splash
        new.features = None
        new.icon = icon
        new.id = 0
        new.name = name
        new.privacy_level = privacy_level
        new.tags = tags
        return new
    
    
    def iter_application_ids_and_activities_ordered(self):
        """
        Iterates over the represented application identifiers and the overview activities in display order.
        
        This method is an iterable generator.
        
        Yields
        ------
        application_id_and_activity : ``(int, GuildActivityOverviewActivity)``
        """
        activity_application_ids = self.activity_application_ids
        if activity_application_ids is None:
            return
        
        activities = self.activities
        if (activities is None):
            for application_id in activity_application_ids:
                yield application_id, GuildActivityOverviewActivity._create_empty()
            return
        
        sort_key_output_pairs = []
        
        for index, application_id in enumerate(activity_application_ids):
            try:
                activity = activities[application_id]
            except KeyError:
                activity = GuildActivityOverviewActivity._create_empty()
            
            activity_level = activity.level
            if activity_level is GuildActivityOverviewActivityLevel.recently_popular:
                priority = 0
            
            elif activity_level is GuildActivityOverviewActivityLevel.any_previous:
                priority = 1
            
            else:
                priority = 2
            
            sort_key_output_pairs.append(((priority, -activity.score, index), (application_id, activity)))
        
        sort_key_output_pairs.sort(key = _application_id_and_activity_sort_key_getter)
        for item in sort_key_output_pairs:
            yield item[1]
    
    
    def iter_activity_application_ids(self):
        """
        Iterates over the activity application identifiers.
        
        This method is an iterable generator.
        
        Yields
        ------
        activity_application_id : `int`
        """
        activity_application_ids = self.activity_application_ids
        if (activity_application_ids is not None):
            yield from activity_application_ids
    
    
    def iter_features(self):
        """
        Iterates over the represented guild's features.
        
        This method is an iterable generator.
        
        Yields
        ------
        feature : ``GuildFeature``
        """
        features = self.features
        if (features is not None):
            yield from features
    
    
    def iter_tags(self):
        """
        Iterates over the guild activity overview's tags.
        
        This method is an iterable generator.
        
        Yields
        ------
        tag : ``GuildActivityOverviewTag``
        """
        tags = self.tags
        if (tags is not None):
            yield from tags
    
    
    @property
    def badge_icon_url(self):
        """
        Returns the guild badge's icon's url. If the guild badge has no icon, then returns `None`.
        
        Returns
        -------
        url : `None | str`
        """
        return build_guild_badge_icon_url(self.id, self.badge_icon_type, self.badge_icon_hash)
    
    
    def badge_icon_url_as(self, ext = None, size = None):
        """
        Returns the guild badge's icon's url. If the guild badge has no icon, then returns `None`.
        
        Parameters
        ----------
        ext : `None | str` = `None`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
            If the guild has animated badge icon, it can be `'gif'` as well.
        
        size : `None | int` = `None`, Optional
            The preferred minimal size of the image's url.
        
        Returns
        -------
        url : `None | str`
        """
        return build_guild_badge_icon_url_as(self.id, self.badge_icon_type, self.badge_icon_hash, ext, size)
    
    
    @property
    def discovery_splash_url(self):
        """
        Returns the guild's discovery splash's url. If the guild has no discovery_splash, then returns `None`.
        
        Returns
        -------
        url : `None | str`
        """
        return build_guild_discovery_splash_url(self.id, self.discovery_splash_type, self.discovery_splash_hash)
    
    
    def discovery_splash_url_as(self, ext = None, size = None):
        """
        Returns the guild's discovery splash's url. If the guild has no discovery splash, then returns `None`.
        
        Parameters
        ----------
        ext : `None | str` = `None`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
            If the guild has animated discovery splash, it can be `'gif'` as well.
        
        size : `None | int` = `None`, Optional
            The preferred minimal size of the image's url.
        
        Returns
        -------
        url : `None | str`
        """
        return build_guild_discovery_splash_url_as(self.id, self.discovery_splash_type, self.discovery_splash_hash, ext, size)
    
    
    @property
    def icon_url(self):
        """
        Returns the guild's icon's url. If the guild has no icon, then returns `None`.
        
        Returns
        -------
        url : `None | str`
        """
        return build_guild_icon_url(self.id, self.icon_type, self.icon_hash)
    
    
    def icon_url_as(self, ext = None, size = None):
        """
        Returns the guild's icon's url. If the guild has no icon, then returns `None`.
        
        Parameters
        ----------
        ext : `None | str` = `None`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
            If the guild has animated icon, it can `'gif'` as well.
        
        size : `None | int` = `None`, Optional
            The preferred minimal size of the image's url.
        
        Returns
        -------
        url : `None | str`
        """
        return build_guild_icon_url_as(self.id, self.icon_type, self.icon_hash, ext, size)
