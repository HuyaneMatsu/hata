from .embed import *
from .embed_author import *
from .embed_field import *
from .embed_field_base import *
from .embed_footer import *
from .embed_image import *
from .embed_provider import *
from .embed_thumbnail import *
from .embed_video import *


__all__ = (
    *embed.__all__,
    *embed_author.__all__,
    *embed_field.__all__,
    *embed_field_base.__all__,
    *embed_footer.__all__,
    *embed_image.__all__,
    *embed_provider.__all__,
    *embed_thumbnail.__all__,
    *embed_video.__all__,
)


# Deprecations

from ...utils.module_deprecation import deprecated_import

deprecated_import(Embed, 'EmbedBase')
deprecated_import(Embed, 'EmbedCore')

del deprecated_import
