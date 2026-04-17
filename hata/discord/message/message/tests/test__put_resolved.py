import vampytest

from ....resolved import Resolved

from ...attachment import Attachment

from ..fields import put_resolved


def _iter_options():
    entity_id = 202310110002
    guild_id = 202310110003
    
    resolved = Resolved(attachments = [Attachment.precreate(entity_id)])
    
    yield (None, False, guild_id, {})
    yield (None, True, guild_id, {'resolved': {}})
    yield (resolved, False, guild_id, {'resolved': resolved.to_data(defaults = False, guild_id = guild_id)})
    yield (resolved, True, guild_id, {'resolved': resolved.to_data(defaults = True, guild_id = guild_id)})


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_resolved(input_value, defaults, guild_id):
    """
    Tests whether ``put_resolved`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | Resolved``
        The resolved to serialise.
    
    defaults : `bool`
        Whether default values should be included in the output as well.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_resolved(input_value, {}, defaults, guild_id = guild_id)
