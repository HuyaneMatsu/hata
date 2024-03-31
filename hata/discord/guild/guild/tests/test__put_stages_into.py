import vampytest

from ....stage import Stage

from ..fields import put_stages_into


def _iter_options():
    stage_id = 202306110007
    stage_topic = 'Koishi'
    
    stage = Stage.precreate(
        stage_id,
        topic = stage_topic,
    )
    
    yield None, False, {'stage_instances': []}
    yield None, True, {'stage_instances': []}
    yield (
        {stage_id: stage},
        True,
        {'stage_instances': [stage.to_data(defaults = True, include_internals = True)]},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_stages_into(input_value, defaults):
    """
    Tests whether ``put_stages_into`` works as intended.
    
    Parameters
    ----------
    input_value : `dict<int, Stage>`
        Input value to serialise.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_stages_into(input_value, {}, defaults)
