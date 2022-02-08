import sys

import scarletio.ext.asyncio


sys.modules['hata.ext.asyncio'] = sys.modules['scarletio.ext.asyncio']
