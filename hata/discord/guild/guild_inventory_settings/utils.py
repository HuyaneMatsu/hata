__all__ = ()

from .fields import put_emoji_pack_collectible, validate_emoji_pack_collectible


GUILD_INVENTORY_SETTINGS_FIELD_CONVERTERS = {
    'emoji_pack_collectible': (validate_emoji_pack_collectible, put_emoji_pack_collectible),
}
