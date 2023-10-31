import vampytest

from ..fields import put_details_into
from ..preinstanced import AuditLogEntryType


def _iter_options():
    yield None, False, {}
    yield None, True, {'options': []}
    
    data = {
        'options': {
            'delete_member_days': 60,
            'members_removed': 5
        }
    }
    
    details = {
        'days': 60,
        'users_removed': 5
    }
    
    yield details, False, data
    yield details, True, data


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test_put_details_into(input_value, defaults):
    """
    Tests whether ``put_details_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_details_into(input_value, {}, defaults, entry_type = AuditLogEntryType.guild_update)
