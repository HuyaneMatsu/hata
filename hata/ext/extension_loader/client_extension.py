__all__ = ()

from ...backend.utils import KeepType
from ...discord.client import Client

from .extension import EXTENSIONS, EXTENSION_STATE_LOADED

@KeepType(Client)
class Client:

    @property
    def extensions(self):
        """
        Returns a list of extensions added to the client. Added by the `extension_loader` extension.
        
        Returns
        -------
        extensions : `list` of ``Extension``
        """
        extensions = []
        for extension in EXTENSIONS.values():
            if extension._state == EXTENSION_STATE_LOADED:
                snapshot_difference = extension._snapshot_difference
                if (snapshot_difference is not None):
                    for client, client_snapshot_difference in snapshot_difference:
                        if (self is client) and client_snapshot_difference:
                            extensions.append(extension)
                            break
        
        return extensions
