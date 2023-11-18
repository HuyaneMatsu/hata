__all__ = ()

from ...application_command import ApplicationCommandPermissionOverwrite
from ...emoji import create_partial_emoji_from_id, create_unicode_emoji

from ..audit_log_change import AuditLogChange
from ..audit_log_change.flags import FLAG_HAS_AFTER, FLAG_HAS_BEFORE


def change_deserializer_modification(conversion, change_data):
    """
    Default deserializer used for regular modification entries.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        The conversion to pull its field of.
    change_data : `dict<str, object>`
        Audit log change to serialize.
    
    Yields
    ------
    change : ``AuditLogChange``
    """
    value_deserializer = conversion.value_deserializer
    flags = 0
    
    try:
        value = change_data['old_value']
    except KeyError:
        before = None
    else:
        if value_deserializer is None:
            before = value
        else:
            before = value_deserializer(value)
        
        flags |= FLAG_HAS_BEFORE
    
    try:
        value = change_data['new_value']
    except KeyError:
        after = None
    else:
        if value_deserializer is None:
            after = value
        else:
            after = value_deserializer(value)
        
        flags |= FLAG_HAS_AFTER
    
    if not flags:
        return
    
    yield AuditLogChange.from_fields(conversion.field_name, flags, before, after)


def change_deserializer_addition_and_removal(conversion, change_data):
    """
    Serializer for additions and removals.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        The conversion to pull its field of.
    change_data : `dict<str, object>`
        Audit log change to serialize.
    
    Yields
    ------
    change : ``AuditLogChange``
    """
    value_deserializer = conversion.value_deserializer
    flags = 0
    
    key = change_data.get('key', None)
    
    if key == conversion.get_field_key(0):
        try:
            value = change_data['new_value']
        except KeyError:
            before = None
        else:
            if value_deserializer is None:
                before = value
            else:
                before = value_deserializer(value)
            
            flags |= FLAG_HAS_BEFORE
        
        after = None
    
    else:
        before = None
        
        try:
            value = change_data['new_value']
        except KeyError:
            after = None
        else:
            if value_deserializer is None:
                after = value
            else:
                after = value_deserializer(value)
            
            flags |= FLAG_HAS_AFTER
    
    
    if not flags:
        return
    
    yield AuditLogChange.from_fields(conversion.field_name, flags, before, after)


def change_deserializer_deprecation(conversion, change_data):
    """
    Serializer for deprecated fields. Does nothing.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        The conversion to pull its field of.
    change_data : `dict<str, object>`
        Audit log change to serialize.
    
    Yields
    ------
    change : ``AuditLogChange``
    """
    return
    yield


def _value_deserializer_emoji_custom(value):
    """
    Default get converter returned for custom emojis.
    
    Parameters
    ----------
    value : `None | str`
        Emoji identifier string.
    
    Returns
    -------
    emoji : `None | Emoji`
    """
    if value is None:
        emoji = None
    else:
        emoji = create_partial_emoji_from_id(int(value))
    
    return emoji


def _value_deserializer_emoji_unicode(value):
    """
    Default get converter returned for unicode emojis.
    
    Parameters
    ----------
    value : `None | str`
        Emoji unicode string.
    
    Returns
    -------
    emoji : `None | Emoji`
    """
    if value is None:
        emoji = None
    else:
        emoji = create_unicode_emoji(value)
    
    return emoji


def change_deserializer_flattened_emoji(conversion, change_data):
    """
    Serializer for additions and removals.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        The conversion to pull its field of.
    change_data : `dict<str, object>`
        Audit log change to serialize.
    
    Yields
    ------
    change : ``AuditLogChange``
    """
    key = change_data.get('key', None)
    value_deserializer = _value_deserializer_emoji_custom if key == 'emoji_id' else _value_deserializer_emoji_unicode
    
    flags = 0
    
    try:
        value = change_data['old_value']
    except KeyError:
        before = None
    else:
        before = value_deserializer(value)
        flags |= FLAG_HAS_BEFORE
    
    try:
        value = change_data['new_value']
    except KeyError:
        after = None
    else:
        after = value_deserializer(value)
        flags |= FLAG_HAS_AFTER
    
    if not flags:
        return
    
    yield AuditLogChange.from_fields(conversion.field_name, flags, before, after)


def change_deserializer_application_command_permission_overwrite(conversion, change_data):
    """
    Serializer an application command permission overwrite.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        The conversion to pull its field of.
    change_data : `dict<str, object>`
        Audit log change to serialize.
    
    Yields
    ------
    change : ``AuditLogChange``
    """
    flags = 0
    
    try:
        value = change_data['old_value']
    except KeyError:
        before = None
    else:
        if value is None:
            before = None
        else:
            before = (ApplicationCommandPermissionOverwrite.from_data(value),)
        
        flags |= FLAG_HAS_BEFORE
    
    try:
        value = change_data['new_value']
    except KeyError:
        after = None
    else:
        if value is None:
            after = None
        else:
            after = (ApplicationCommandPermissionOverwrite.from_data(value),)
        flags |= FLAG_HAS_AFTER
    
    if not flags:
        return
    
    yield AuditLogChange.from_fields(conversion.field_name, flags, before, after)
