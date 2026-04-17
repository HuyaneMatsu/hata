__all__ = ()

from vampytest import ScarletioCoroutineEnvironment, set_global_environment

from .discord import KOKORO


# We run every async test inside of hata on our event loop.
set_global_environment(ScarletioCoroutineEnvironment(event_loop = KOKORO))
