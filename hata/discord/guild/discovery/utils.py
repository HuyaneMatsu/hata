__all__ = ()

from .fields import (
    put_emoji_discovery, put_keywords, put_primary_category, validate_emoji_discovery,
    validate_keywords, validate_primary_category
)


GUILD_DISCOVERY_FIELD_CONVERTERS = {
    'emoji_discovery': (validate_emoji_discovery, put_emoji_discovery),
    'keywords': (validate_keywords, put_keywords),
    'primary_category': (validate_primary_category, put_primary_category),
}
