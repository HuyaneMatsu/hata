__all__ = ('validate_application_target_type', )

from ....discord.application_command import ApplicationCommandTargetType


DEFAULT_APPLICATION_COMMAND_TARGET_TYPE = ApplicationCommandTargetType.chat

APPLICATION_COMMAND_TARGET_TYPES_BY_NAME = {
    application_command_target_type.name: application_command_target_type for
    application_command_target_type in ApplicationCommandTargetType.INSTANCES.values()
}

APPLICATION_COMMAND_TARGET_TYPES_BY_VALUE = {
    application_command_target_type.value: application_command_target_type for
    application_command_target_type in ApplicationCommandTargetType.INSTANCES.values()
}


def validate_application_target_type(target):
    """
    Validates the given ``ApplicationCommandTargetType`` value.
    
    Parameters
    ----------
    target : `None`, `int`, `str`, ``ApplicationCommandTargetType``
        The `target` to validate.
    
    Returns
    -------
    target : ``ApplicationCommandTargetType``
        The validated `target`.
    
    Raises
    ------
    ValueError
        - If `target` could not be matched by any expected target type name or value.
    TypeError
        - If `target` is neither `None`, `int`, `str`, nor ``ApplicationCommandTargetType``.
    """
    if target is None:
        target = ApplicationCommandTargetType.none
    
    elif isinstance(target, ApplicationCommandTargetType):
        pass
    
    elif isinstance(target, str):
        if type(target) is not str:
            target = str(target)
        
        target = target.lower()
        
        try:
            target = APPLICATION_COMMAND_TARGET_TYPES_BY_NAME[target]
        except KeyError:
            raise ValueError(
                f'Unknown `target` name: {target!r}.'
            ) from None
    
    elif isinstance(target, int):
        if type(target) is not int:
            target = int(target)
        
        try:
            target = APPLICATION_COMMAND_TARGET_TYPES_BY_NAME[target]
        except KeyError:
            raise ValueError(
                f'Unknown `target` value: {target!r}.'
            ) from None
    
    else:
        raise TypeError(
            f'`target` can be `None`, `{ApplicationCommandTargetType.__name__}`, `str`,  `int`, got '
            f'{target.__class__.__name__}; {target!r}.'
        )
    
    if target is ApplicationCommandTargetType.none:
        target = DEFAULT_APPLICATION_COMMAND_TARGET_TYPE
    
    return target
