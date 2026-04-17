__all__ = ()

try:
    import libnacl

except ImportError:
    # Not installed.
    import_success = False

except OSError as exception:
    # Libsodium not found.
    try:
        args = exception.args
        if len(args) != 1:
            raise
        
        error_message = args[0]
        if not isinstance(error_message, str):
            raise
        
        if not error_message.startswith('Could not locate nacl lib, searched for'):
            raise
    finally:
        args = None
        error_message = None
        
        del args
        del error_message
     
    import_success = False

else:
    del libnacl
    import_success = True


while True:
    if import_success:
        try:
            from libnacl import (
                crypto_secretbox, crypto_secretbox_KEYBYTES, crypto_secretbox_NONCEBYTES, crypto_secretbox_open
            )
        except ImportError:
            pass
        else:
            break
    
    crypto_secretbox_KEYBYTES = 0
    crypto_secretbox_NONCEBYTES = 0
    crypto_secretbox = lambda plain_data, nonce, key: b''
    crypto_secretbox_open = lambda cipher_data, nonce, key: b''
    break


while True:
    if import_success:
        try:
            from libnacl import (
                crypto_aead_aes256gcm_KEYBYTES, crypto_aead_aes256gcm_NPUBBYTES, crypto_aead_aes256gcm_decrypt,
                crypto_aead_aes256gcm_encrypt
            )
        except ImportError:
            pass
        else:
            break
        
    crypto_aead_aes256gcm_KEYBYTES = 0
    crypto_aead_aes256gcm_NPUBBYTES = 0
    crypto_aead_aes256gcm_encrypt = lambda cipher_data, additional_authentication_data, nonce, key: b''
    crypto_aead_aes256gcm_decrypt = lambda plain_data, additional_authentication_data, nonce, key: b''
    break


while True:
    if import_success:
        try:
            from libnacl import (
                crypto_aead_xchacha20poly1305_ietf_KEYBYTES, crypto_aead_xchacha20poly1305_ietf_NPUBBYTES,
                crypto_aead_xchacha20poly1305_ietf_decrypt, crypto_aead_xchacha20poly1305_ietf_encrypt
            )
        except ImportError:
            pass
        else:
            break
    
    crypto_aead_xchacha20poly1305_ietf_KEYBYTES = 0
    crypto_aead_xchacha20poly1305_ietf_NPUBBYTES = 0
    crypto_aead_xchacha20poly1305_ietf_encrypt = lambda cipher_data, additional_authentication_data, nonce, key: b''
    crypto_aead_xchacha20poly1305_ietf_decrypt = lambda plain_data, additional_authentication_data, nonce, key: b''
    break
