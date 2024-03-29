__all__ = ('EMBED_UPDATE_EMBED_ADD', 'EMBED_UPDATE_EMBED_REMOVE', 'EMBED_UPDATE_NONE', 'EMBED_UPDATE_SIZE_UPDATE',)

CONTENT_LENGTH_MAX = 4000
NONCE_LENGTH_MAX = 25


EMBED_UPDATE_NONE = 0
EMBED_UPDATE_SIZE_UPDATE = 1
EMBED_UPDATE_EMBED_ADD = 2
EMBED_UPDATE_EMBED_REMOVE = 3


MESSAGE_STATE_MASK_TEMPLATE = 1 << 0
MESSAGE_STATE_MASK_SHOULD_UPDATE = 1 << 1
MESSAGE_STATE_MASK_DELETED = 1 << 2

MESSAGE_STATE_MASK_CACHE_MENTIONED_CHANNELS = 1 << 3

MESSAGE_STATE_MASK_PARTIAL_ALL = (
    MESSAGE_STATE_MASK_TEMPLATE | MESSAGE_STATE_MASK_SHOULD_UPDATE | MESSAGE_STATE_MASK_DELETED
)

MESSAGE_STATE_MASK_CACHE_ALL = MESSAGE_STATE_MASK_CACHE_MENTIONED_CHANNELS
