import vampytest

from ..fields import parse_internal_guild_restriction
from ..preinstanced import ApplicationInternalGuildRestriction


def _iter_options():
    yield {}, ApplicationInternalGuildRestriction.none
    yield (
        {'internal_guild_restriction': ApplicationInternalGuildRestriction.restricted.value},
        ApplicationInternalGuildRestriction.restricted,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_internal_guild_restriction(input_data):
    """
    Tests whether ``parse_internal_guild_restriction`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``ApplicationInternalGuildRestriction``
    """
    output = parse_internal_guild_restriction(input_data)
    vampytest.assert_instance(output, ApplicationInternalGuildRestriction)
    return output
