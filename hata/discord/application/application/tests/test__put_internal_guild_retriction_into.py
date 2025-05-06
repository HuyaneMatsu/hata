import vampytest

from ..fields import put_internal_guild_restriction
from ..preinstanced import ApplicationInternalGuildRestriction


def _iter_options():
    yield (
        ApplicationInternalGuildRestriction.restricted,
        False,
        {'internal_guild_restriction': ApplicationInternalGuildRestriction.restricted.value},
    )
    yield (
        ApplicationInternalGuildRestriction.restricted,
        True,
        {'internal_guild_restriction': ApplicationInternalGuildRestriction.restricted.value},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_internal_guild_restriction(input_value, defaults):
    """
    Tests whether ``put_internal_guild_restriction`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ApplicationInternalGuildRestriction``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_internal_guild_restriction(input_value, {}, defaults)
