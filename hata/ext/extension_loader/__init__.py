# -*- coding: utf-8 -*-
from .extension_loader import *

__all__ = extension_loader.__all__

from .. import register_library_extension
register_library_extension('HuyaneMatsu.extension_loader')
del register_library_extension
