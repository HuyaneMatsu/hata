# -*- coding: utf-8 -*-

# Upgraded commands extension for hata.
# Work in progress.

from .category import *
from . import checks
from .command import *
from .command_helpers import *
from .command_processor import *
from .content_parser import *
from .context import *
from .exceptions import *
from .utils import *

__all__ = (
    *category.__all__,
    'checks'
    *command.__all__,
    *command_helpers.__all__,
    *command_processor.__all__,
    *content_parser.__all__,
    *context.__all__,
    *exceptions.__all__,
    *utils.__all__,
)


def snapshot_hook():
    from . import snapshot


from .. import register_library_extension, add_library_extension_hook
register_library_extension('HuyaneMatsu.commands_v2')
add_library_extension_hook(snapshot_hook, ['HuyaneMatsu.extension_loader'])
del register_library_extension, add_library_extension_hook, snapshot_hook
