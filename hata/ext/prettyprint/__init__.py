import warnings

warnings.warn(
    '`hata.ext.prettyprint` is discontinued and will be removed in 2022 Jun.',
    FutureWarning,
    stacklevel = 2,
)

from .prettyprint import *

__all__ = prettyprint.__all__

from .. import register_library_extension
register_library_extension('HuyaneMatsu.prettyprint')
del register_library_extension
