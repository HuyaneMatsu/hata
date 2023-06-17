__all__ = ()

from ...utils import seconds_to_id_difference

from ..interaction_metadata import InteractionMetadataBase


INTERACTION_EVENT_EXPIRE_AFTER = 900 # 15 min
INTERACTION_EVENT_EXPIRE_AFTER_ID_DIFFERENCE = seconds_to_id_difference(INTERACTION_EVENT_EXPIRE_AFTER)

DEFAULT_INTERACTION_METADATA = InteractionMetadataBase()


USER_GUILD_CACHE = {}
"""
USER_GUILD_CACHE : `dict` of (`tuple` (``ClientUserBase``, ``Guild``), `int`)
    A cache which stores `user-guild` pairs as keys and their reference count as values to remember
    ``InteractionEvent``'s ``.user``-s' guild profiles of the respective ``.guild`` even if the ``Guild`` is
    uncached.

    Note, that private channel interaction, neither interactions of cached guilds are not added, what means if
    all the clients are kicked from a guild the guild profile can be lost in unexpected time.
"""
