__all__ = ()

import re

NAME_LENGTH_MIN = 2
NAME_LENGTH_MAX = 32

NAME_ALLOWED_CHARACTERS = re.compile('([0-9A-Za-z_]+)')

UNICODE_EMOJI_LIMIT = 1 << 21
