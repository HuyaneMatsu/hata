import vampytest

from ..fields import parse_details
from ..preinstanced import AuditLogEntryType


def _iter_options():
    yield {}, None
    yield {'options': None}, None
    yield {'options': {}}, None
    
    yield (
        {
            'options': {
                'delete_message_seconds': 60,
                'members_removed': 5
            }
        },
        {
            'delete_message_duration': 60,
            'users_removed': 5
        }
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test_parse_details(input_data):
    """
    Tests whether ``parse_details`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | dict<str, object>`
    """
    return parse_details(input_data, AuditLogEntryType.guild_update)
