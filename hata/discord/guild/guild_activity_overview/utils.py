__all__ = ()

from functools import partial as partial_func

from .fields import (
    put_activity_application_ids, put_banner_color, put_description, put_name, put_privacy_level, put_tags,
    validate_activity_application_ids, validate_banner_color, validate_description, validate_name,
    validate_privacy_level, validate_tags
)
from .guild_activity_overview import GUILD_ACTIVITY_OVERVIEW_DISCOVERY_SPLASH, GUILD_ACTIVITY_OVERVIEW_ICON


GUILD_ACTIVITY_OVERVIEW_FIELD_CONVERTERS = {
    'activity_application_ids': (validate_activity_application_ids, put_activity_application_ids),
    'banner_color': (validate_banner_color, put_banner_color),
    'description': (validate_description, put_description),
    'discovery_splash': (
        partial_func(GUILD_ACTIVITY_OVERVIEW_DISCOVERY_SPLASH.validate_icon, allow_data = True),
        partial_func(GUILD_ACTIVITY_OVERVIEW_DISCOVERY_SPLASH.put_into, as_data = True),
    ),
    'icon': (
        partial_func(GUILD_ACTIVITY_OVERVIEW_ICON.validate_icon, allow_data = True),
        partial_func(GUILD_ACTIVITY_OVERVIEW_ICON.put_into, as_data = True),
    ),
    'name': (validate_name, put_name),
    'privacy_level': (validate_privacy_level, put_privacy_level),
    'tags': (validate_tags, put_tags),
}
