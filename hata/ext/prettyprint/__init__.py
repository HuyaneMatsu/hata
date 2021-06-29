# -*- coding: utf-8 -*-
from .prettyprint import *

__all__ = prettyprint.__all__

from .. import register_library_extension
register_library_extension('HuyaneMatsu.prettyprint')
del register_library_extension
