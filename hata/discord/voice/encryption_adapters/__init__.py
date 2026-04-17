from .aead_aes256_gcm_rtpsize import *
from .aead_xchacha20_poly1305_rtpsize import *
from .base import *
from .nacl import *
from .xsalsa20_poly1305 import *


__all__ = (
    *aead_aes256_gcm_rtpsize.__all__,
    *aead_xchacha20_poly1305_rtpsize.__all__,
    *base.__all__,
    *nacl.__all__,
    *xsalsa20_poly1305.__all__,
)

# Construct `AVAILABLE_ENCRYPTION_ADAPTERS`

from .aead_aes256_gcm_rtpsize import EncryptionAdapter__aead_aes256_gcm_rtpsize
from .aead_xchacha20_poly1305_rtpsize import EncryptionAdapter__aead_xchacha20_poly1305_rtpsize
from .xsalsa20_poly1305 import EncryptionAdapter__xsalsa20_poly1305


AVAILABLE_ENCRYPTION_ADAPTERS = (*sorted(
    (
        encryption_adapter for encryption_adapter in
        (
            EncryptionAdapter__aead_aes256_gcm_rtpsize, # -> not working actually, lmeow
            EncryptionAdapter__aead_xchacha20_poly1305_rtpsize, # -> not working actually, lmeow
            EncryptionAdapter__xsalsa20_poly1305,
        )
        if encryption_adapter.available
    ),
    key = (lambda encryption_adapter : encryption_adapter.priority),
    reverse = True,
),)


# Import `EncryptionAdapterBase` to shorten imports

from .base import EncryptionAdapterBase
