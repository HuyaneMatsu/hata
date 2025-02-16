import vampytest

from ...action import AutoModerationAction

from ..fields import put_actions


def _iter_options():
    action_0 = AutoModerationAction(duration = 69)
    action_1 = AutoModerationAction(channel_id = 202211170022)
    
    yield None, False, {}
    yield None, True, {'actions': []}
    yield (
        (action_0, action_1),
        False,
        {'actions': [action_0.to_data(defaults = False), action_1.to_data(defaults = False)]},
    )
    yield (
        (action_0, action_1),
        True,
        {'actions': [action_0.to_data(defaults = True), action_1.to_data(defaults = True)]},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_actions(input_value, defaults):
    """
    Tests whether ``put_actions`` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<AutoModerationAction>`
        Input value to serialise.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_actions(input_value, {}, defaults)
