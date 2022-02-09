"""
Hata extensions come into this folder.

If a hata library extension is imported, it should register itself with the ``register_library_extension``, so if an
other library extension is imported, it can register a hook to run only if both are imported.

Hook registrations can be done with the ``add_library_extension_hook`` function.
"""
from scarletio.ext import (
    add_library_extension_hook, get_and_validate_setup_functions, register_library_extension, register_setup_function,
    run_setup_functions
)

__all__ = ()
