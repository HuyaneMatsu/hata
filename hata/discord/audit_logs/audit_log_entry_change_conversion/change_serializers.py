__all__ = ()

from ..audit_log_change.flags import FLAG_HAS_AFTER, FLAG_HAS_BEFORE


def change_serializer_modification(conversion, change):
    """
    Default serializer used for regular modification entries.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        The conversion to pull its field of.
    change : ``AuditLogChange``
        Audit log change to deserialize.
    
    Yields
    ------
    change_data : `dict<str, object>`
    """
    value_serializer = conversion.value_serializer
    flags = change.flags
    
    change_data = {
        'key': conversion.get_field_key(0),
    }
    
    if flags & FLAG_HAS_BEFORE:
        before = change.before
        if (value_serializer is None):
            value = before
        else:
            value = value_serializer(before)
        
        change_data['old_value'] = value
    
    if flags & FLAG_HAS_AFTER:
        after = change.after
        if (value_serializer is None):
            value = after
        else:
            value = value_serializer(after)
        
        change_data['new_value'] = value
    
    yield change_data


def change_serializer_addition_and_removal(conversion, change):
    """
    Serializer for additions and removals.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        The conversion to pull its field of.
    change : ``AuditLogChange``
        Audit log change to serialise.
    
    Yields
    ------
    change_data : `dict<str, object>`
    """
    value_serializer = conversion.value_serializer
    flags = change.flags
    
    if flags & FLAG_HAS_BEFORE:
        before = change.before
        if (value_serializer is None):
            value = before
        else:
            value = value_serializer(before)
        
        yield {
            'key': conversion.get_field_key(0),
            'new_value': value,
        }
    
    if flags & FLAG_HAS_AFTER:
        after = change.after
        if (value_serializer is None):
            value = after
        else:
            value = value_serializer(after)
        
        yield {
            'key': conversion.get_field_key(1),
            'new_value': value,
        }


def change_serializer_flattened_emoji(conversion, change):
    """
    Serializer for flattened emojis.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        The conversion to pull its field of.
    change : ``AuditLogChange``
        Audit log change to serialise.
    
    Yields
    ------
    change_data : `dict<str, object>`
    """
    flags = change.flags
    
    # Should not happen
    if not (flags & (FLAG_HAS_BEFORE | FLAG_HAS_AFTER)):
        return
    
    # Only before
    if flags & (FLAG_HAS_BEFORE | FLAG_HAS_AFTER) == FLAG_HAS_BEFORE:
        before = change.before
        if before is None:
            key = 'emoji_name'
            value = None
        elif before.is_unicode_emoji():
            key = 'emoji_name'
            value = before.unicode
        else:
            key = 'emoji_id'
            value = str(before.id)
        
        yield {
            'key': key,
            'old_value': value,
        }
        return
    
    # Only after
    if flags & (FLAG_HAS_BEFORE | FLAG_HAS_AFTER) == FLAG_HAS_AFTER:
        after = change.after
        if after is None:
            key = 'emoji_name'
            value = None
        elif after.is_unicode_emoji():
            key = 'emoji_name'
            value = after.unicode
        else:
            key = 'emoji_id'
            value = str(after.id)
        
        yield {
            'key': key,
            'new_value': value,
        }
        return
    
    
    after = change.after
    before = change.before
    
    # both before and after None
    if (before is None) and (after is None):
        # ????
        return
    
    # after not None
    if (before is None) and (after is not None):
        if after.is_unicode_emoji():
            key = 'emoji_name'
            value = None
        else:
            key = 'emoji_id'
            value = str(after.id)

        yield {
            'key': key,
            'old_value': None,
            'new_value': value,
        }
        return
    
    # before not None
    if (before is not None) and (after is None):
        if before.is_unicode_emoji():
            key = 'emoji_name'
            value = None
        else:
            key = 'emoji_id'
            value = str(before.id)

        yield {
            'key': key,
            'old_value': value,
            'new_value': None,
        }
        return
    
    # all not None
    # both unicode
    if before.is_unicode_emoji() and after.is_unicode_emoji():
        yield {
            'key': 'emoji_name',
            'old_value': before.unicode,
            'new_value': after.unicode,
        }
        return
    
    # both custom
    if before.is_custom_emoji() and after.is_custom_emoji():
        yield {
            'key': 'emoji_id',
            'old_value': str(before.id),
            'new_value': str(after.id),
        }
        return
    
    # mixed
    if before.is_unicode_emoji():
        key = 'emoji_name'
        value = before.unicode
    else:
        key = 'emoji_id'
        value = str(before.id)
    
    yield {
        'key': key,
        'old_value': value,
    }


    if after.is_unicode_emoji():
        key = 'emoji_name'
        value = after.unicode
    else:
        key = 'emoji_id'
        value = str(after.id)
    
    yield {
        'key': key,
        'new_value': value,
    }


def change_serializer_application_command_permission_overwrite(conversion, change):
    """
    Serializer for application command permission overwrites.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        The conversion to pull its field of.
    change : ``AuditLogChange``
        Audit log change to serialise.
    
    Yields
    ------
    change_data : `dict<str, object>`
    """
    before = change.before
    after = change.after
    
    
    merged = {}
    
    if (before is not None):
        for before_entry in before:
            target_id = before_entry.target_id
            merged[target_id] = (before_entry, None)
    
    
    if (after is not None):
        for after_entry in after:
            target_id = after_entry.target_id
            
            entry = merged.get(target_id, None)
            if entry is None:
                before_entry = None
            else:
                before_entry = entry[0]
            
            merged[target_id] = (before_entry, after_entry)
    
    # Sort the items, so we can predetermine the order
    for target_id, (before_entry, after_entry) in sorted(merged.items()):
        change_data = {'key': str(target_id)}
        
        if (before_entry is not None):
            change_data['old_value'] = before_entry.to_data(defaults = True)
        
        if (after_entry is not None):
            change_data['new_value'] = after_entry.to_data(defaults = True)
        
        yield change_data
