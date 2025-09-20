import vampytest

from ....message import Attachment
from ....resolved import Resolved

from ..fields import parse_resolved


def _iter_options():
    entity_id = 202211050039
    guild_id = 202211050040
    resolved = Resolved(attachments = [Attachment.precreate(entity_id)])
    
    yield (
        {},
        guild_id,
        None,
    )
    
    yield (
        {
            'data': None,
        },
        guild_id,
        None,
    )
    
    yield (
        {
            'data': {},
        },
        guild_id,
        None,
    )
    
    yield (
        {
            'data': {
                'resolved': None,
            },
        },
        guild_id,
        None,
    )
    
    yield (
        {
            'data': {
                'resolved': {},
            },
        },
        guild_id,
        None,
    )
    
    yield (
        {
            'data': {
                'resolved': resolved.to_data(defaults = True, guild_id = guild_id),
            },
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
    output = parse_resolved(input_data, guild_id)
    vampytest.assert_instance(output, Resolved, nullable = True)
    return output
