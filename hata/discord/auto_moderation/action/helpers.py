__all__ = ()

from .preinstanced import AutoModerationActionType


KEYWORD_TO_ACTION_TYPE = {
    'channel_id': AutoModerationActionType.send_alert_message,
    'duration': AutoModerationActionType.timeout,
    'custom_message': AutoModerationActionType.block_message,
}


def guess_action_type_from_keyword_parameters(action_type, keyword_parameters):
    """
    Guesses the action's type from the given fields.
    
    Parameters
    ----------
    action_type : ``AutoModerationActionType``
        Already detected action type.
    
    keyword_parameters : `dict` of (`str`, `object`) items
        Keyword parameters passed.
    
    Returns
    -------
    action_type : ``AutoModerationActionType``
        The detected type.
    
    Raises
    ------
    TypeError
        - Extra keyword parameter.
        - Multiple actions received / detected.
    """
    for key in keyword_parameters.keys():
        try:
            key_action_type = KEYWORD_TO_ACTION_TYPE[key]
        except KeyError:
            raise TypeError(
                f'Extra keyword parameter: {key} = {keyword_parameters[key]!r}.'
            )
        
        if action_type is AutoModerationActionType.none:
            action_type = key_action_type
            continue
        
        if action_type is not key_action_type:
            raise TypeError(
                f'Multiple action types received / detected: {action_type!r}; {key_action_type!r}; '
                f'keyword parameters = {keyword_parameters!r}.'
            )
    
    return action_type
