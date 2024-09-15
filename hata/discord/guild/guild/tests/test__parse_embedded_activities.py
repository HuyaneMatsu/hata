import vampytest

from ....embedded_activity import EmbeddedActivity

from ..fields import parse_embedded_activities
from ..guild import Guild


def _iter_options():
    yield {}, 202409030001, None
    yield {'activity_instances': []}, 202409030002, None
    
    embedded_activity = EmbeddedActivity.precreate(202409030000)
    
    yield (
        {'activity_instances': [embedded_activity.to_data(include_internals = True)]},
        202409030003,
        {embedded_activity},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_embedded_activities(input_value, guild_id):
    """
    Tests whether ``parse_embedded_activities`` works as intended.
    
    Parameters
    ----------
    input_value : `dict<str, object>`
        Value to pass.
    
    guild_id : `int`
        The guild's identifier we are populating its scheduled events of.
    
    Returns
    -------
    output : `None | set<EmbeddedActivity>`
    """
    guild = Guild.precreate(guild_id)
    
    output = parse_embedded_activities(input_value, guild.embedded_activities)
    vampytest.assert_instance(output, set, nullable = True)
    return output
