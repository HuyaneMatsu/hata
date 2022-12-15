__all__ = ()

from .fields import (
    put_emoji_discovery_into, put_keywords_into, put_primary_category_into, put_sub_categories_into,
    validate_emoji_discovery, validate_keywords, validate_primary_category, validate_sub_categories
)


GUILD_DISCOVERY_FIELD_CONVERTERS = {
    'emoji_discovery': (validate_emoji_discovery, put_emoji_discovery_into),
    'keywords': (validate_keywords, put_keywords_into),
    'primary_category': (validate_primary_category, put_primary_category_into),
}
