import vampytest

from ...action import AutoModerationAction

from ..fields import parse_actions


def _iter_options():
    action_0 = AutoModerationAction(duration = 69)
    action_1 = AutoModerationAction(channel_id = 202211170021)
    
    yield {}, None
    yield {'actions': None}, None
    yield {'actions': []}, None
    yield {'actions': [action_0.to_data(defaults = True), action_1.to_data(defaults = True)]}, (action_0, action_1)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_actions(input_data):
    """
    Tests whether ``parse_actions`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `Nome | tuple<AutoModerationAction>`
    """
    return parse_actions(input_data)
