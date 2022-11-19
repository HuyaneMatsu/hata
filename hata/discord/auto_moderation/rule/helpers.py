__all__ = ()

from .preinstanced import AutoModerationRuleTriggerType


KEYWORD_TO_RULE_TRIGGER_TYPE = {
    'excluded_keywords': None, # This is applicable for 2 types, so we ignore it
    'keywords': AutoModerationRuleTriggerType.keyword,
    'regex_patterns': AutoModerationRuleTriggerType.keyword,
    'keyword_presets': AutoModerationRuleTriggerType.keyword_preset,
    'mention_limit': AutoModerationRuleTriggerType.mention_spam,
}


def guess_rule_trigger_type_from_keyword_parameters(rule_trigger_type, keyword_parameters):
    """
    Guesses the rule trigger's type from the given fields.
    
    Parameters
    ----------
    rule_trigger_type : ``AutoModerationRuleTriggerType``
        Already detected rule trigger type.
    
    keyword_parameters : `dict` of (`str`, `object`) items
        Keyword parameters passed.
    
    Returns
    -------
    rule_trigger_type : ``AutoModerationRuleTriggerType``
        The detected type.
    
    Raises
    ------
    TypeError
        - Extra keyword parameter.
        - Multiple trigger types received / detected.
    """
    for key in keyword_parameters.keys():
        try:
            key_rule_trigger_type = KEYWORD_TO_RULE_TRIGGER_TYPE[key]
        except KeyError:
            raise TypeError(
                f'Extra keyword parameter: {key} = {keyword_parameters[key]!r}.'
            )
        
        if key_rule_trigger_type is None:
            continue
        
        if rule_trigger_type is AutoModerationRuleTriggerType.none:
            rule_trigger_type = key_rule_trigger_type
            continue
        
        if rule_trigger_type is not key_rule_trigger_type:
            raise TypeError(
                f'Multiple rule trigger types received / detected: {rule_trigger_type!r}; {key_rule_trigger_type!r}; '
                f'keyword parameters = {keyword_parameters!r}.'
            )
    
    return rule_trigger_type
