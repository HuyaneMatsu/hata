import vampytest

from ....stage import Stage

from ..guild import Guild

from ..fields import parse_stages


def _iter_options():
    stage_id = 202306110008
    guild_id = 202306110009
    stage_topic = 'Koishi'
    
    
    stage = Stage.precreate(
        stage_id,
        guild_id = guild_id,
        topic = stage_topic,
    )
    
    yield {}, 202306110010, None
    yield {'stage_instances': []}, 202306110011, None
    yield (
        {'stage_instances': [stage.to_data(defaults = True, include_internals = True)]},
        guild_id,
        {stage_id: stage},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_stages(input_value, guild_id):
    """
    Tests whether ``parse_stages`` works as intended.
    
    Parameters
    ----------
    input_value : `dict<str, object>`
        Value to pass.
    guild_id : `int`
        The guild's identifier we are populating its scheduled events of.
    
    Returns
    -------
    output : `None | dict<int, Stage>`
    """
    guild = Guild.precreate(guild_id)
    
    return parse_stages(input_value, guild.stages)
