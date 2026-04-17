__all__ = ('EXTRA_EMBED_TYPES',)

from .preinstanced import EmbedType


TITLE_LENGTH_MAX = 256
DESCRIPTION_LENGTH_MAX = 4096
FIELDS_LENGTH_MAX = 25
URL_LENGTH_MAX = 2048


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
