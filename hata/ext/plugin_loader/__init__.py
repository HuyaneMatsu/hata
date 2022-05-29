from .import_overwrite import *
from .snapshot import *
from .utils import *

from .client_extension import *
from .constants import *
from .exceptions import *
from .plugin import *
from .plugin_loader import *
from .plugin_root import *
from .helpers import *

__all__ = (
    *import_overwrite.__all__,
    *snapshot.__all__,
    *utils.__all__,
    
    *client_extension.__all__,
    *constants.__all__,
    *exceptions.__all__,
    *plugin.__all__,
    *plugin_loader.__all__,
    *plugin_root.__all__,
    *helpers.__all__,
)

from .. import register_library_extension
register_library_extension('HuyaneMatsu.plugin_loader')
del register_library_extension

import warnings


def __getattr__(attribute_name):
    new_attribute_name = attribute_name.replace(
        'extension', 'plugin'
    ).replace(
        'EXTENSION', 'PLUGIN'
    ).replace(
        'Extension', 'Plugin'
    )
    
    warnings.warn(
        (
            f'`plugin_loader.{attribute_name}` is deprecated and will be removed in 2022 December, '
            f'please use `.{new_attribute_name}` instead.'
        ),
        FutureWarning,
        stacklevel = 2,
    )
    
    # this import is fine, don not worry.
    from .. import plugin_loader
    return getattr(plugin_loader, new_attribute_name)
