import vampytest

from ....resolved import Resolved

from ...attachment import Attachment

from ..fields import parse_resolved


def _iter_options():
    entity_id = 202310110000
    guild_id = 202310110001
    resolved = Resolved(attachments = [Attachment.precreate(entity_id)])
    
    yield (
        {},
        guild_id,
        None,
    )
    
    yield (
        {
            'resolved': None,
        },
        guild_id,
        None,
    )
    
    yield (
        {
            'resolved': {}
        },
        guild_id,
        None,
    )
    
    yield (
        {
            'resolved': resolved.to_data(defaults = True, guild_id = guild_id),
        },
        guild_id,
        resolved,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_resolved(input_data, guild_id):
    """
    Tests whether ``parse_resolved`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : `None | Resolved`
    """
    return parse_resolved(input_data, guild_id)
