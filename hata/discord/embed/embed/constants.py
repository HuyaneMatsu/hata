__all__ = ('EXTRA_EMBED_TYPES',)

from .preinstanced import EmbedType


EMBED_TITLE_LENGTH_MAX = 256
EMBED_DESCRIPTION_LENGTH_MAX = 4096
EMBED_FIELDS_LENGTH_MAX = 25


EXTRA_EMBED_TYPES = frozenset((
    EmbedType.application_news,
    EmbedType.article,
    EmbedType.auto_moderation_message,
    EmbedType.gifv,
    EmbedType.image,
    EmbedType.link,
    EmbedType.tweet,
    EmbedType.video,
))
