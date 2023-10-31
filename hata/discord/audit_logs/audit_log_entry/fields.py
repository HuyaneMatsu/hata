__all__ = ()

from ....env import ALLOW_DEBUG_MESSAGES
from ....utils.debug import call_debug_logger

from ...field_parsers import entity_id_parser_factory, nullable_string_parser_factory, preinstanced_parser_factory
from ...field_putters import (
    entity_id_optional_putter_factory, entity_id_putter_factory, nullable_string_optional_putter_factory,
    preinstanced_putter_factory
)
from ...field_validators import (
    entity_id_validator_factory, nullable_entity_validator_factory, nullable_string_validator_factory,
    preinstanced_validator_factory
)
from ...guild import Guild
from ...user import ClientUserBase

from ..audit_log_change import AuditLogChange
from ..audit_log_change.flags import (
    FLAG_HAS_AFTER, FLAG_HAS_BEFORE, FLAG_IS_ADDITION, FLAG_IS_IGNORED, FLAG_IS_MODIFICATION, FLAG_IS_REMOVAL,
    get_flags_name
)

from .constants import REASON_LENGTH_MAX, REASON_LENGTH_MIN
from .preinstanced import AuditLogEntryType


# changes

def parse_changes(data, entry_type = AuditLogEntryType.none):
    """
    Parses the entry's changes.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    entry_type : `None`, ``AuditLogEntryType`` = `AuditLogEntryType.none`, Optional
        The event's type.
    
    Returns
    -------
    changes : `None | dict<str, AuditLogChange>` 
    """
    change_datas = data.get('changes', None)
    if (change_datas is None) or (not change_datas):
        return None
    
    changes = None
    
    change_conversions = entry_type.target_type.change_conversions
    if change_conversions is None:
        converters = None
    else:
        converters = change_conversions.get_converters
    
    for change_data in change_datas:
        key = change_data.get('key', None)
        if key is None:
            continue
        
        if converters is None:
            triplet = None
        else:
            triplet = converters.get(key, None)
        
        if triplet is None:
            if ALLOW_DEBUG_MESSAGES:
                call_debug_logger(
                    (
                        f'Unknown audit log entry change key: {key!r}\n'
                        f'- Change data: {change_data!r}\n'
                        f'- Event type: {entry_type!r}'
                    ),
                    True,
                )
            continue
        
        attribute_name, flags, get_converter = triplet
        
        if flags & FLAG_IS_MODIFICATION:
            try:
                before = change_data['old_value']
            except KeyError:
                before = None
            else:
                before = get_converter(before)
                flags |= FLAG_HAS_BEFORE
            
            try:
                after = change_data['new_value']
            except KeyError:
                after = None
            else:
                after = get_converter(after)
                flags |= FLAG_HAS_AFTER
        
        elif flags & FLAG_IS_REMOVAL:
            try:
                before = change_data['new_value']
            except KeyError:
                before = None
            else:
                before = get_converter(before)
                flags |= FLAG_HAS_BEFORE
            
            after = None
            
        elif flags & FLAG_IS_ADDITION:
            before = None
            
            try:
                after = change_data['new_value']
            except KeyError:
                after = None
            else:
                after = get_converter(after)
                flags |= FLAG_HAS_AFTER
        
        elif flags & FLAG_IS_IGNORED:
            continue
        
        else:
            # Should not happen
            before = None
            after = None
        
        change = AuditLogChange.from_fields(attribute_name, flags, before, after)
        
        if changes is None:
            changes = {}
        
        current_change = changes.setdefault(attribute_name, change)
        if (change is not current_change):
            merged_change = current_change + change
            changes[attribute_name] = merged_change

    return changes


def put_changes_into(changes, data, defaults, *, entry_type = AuditLogEntryType.none):
    """
    Serialises the given changes.
    
    Parameters
    ----------
    changes : `None | dict<str, AuditLogChange>` 
        Changes to serialize.
    data : `dict<str, object>`
        Data to extend.
    defaults : `bool`
        Whether fields with the default value should be ignored.
    entry_type : `None`, ``AuditLogEntryType`` = `AuditLogEntryType.none`, Optional (Keyword only)
        The event's type.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if changes is None:
        if defaults:
            data['changes'] = []
        return data
    
    change_datas = []
    
    change_conversions = entry_type.target_type.change_conversions
    if change_conversions is None:
        converters = None
    else:
        converters = change_conversions.put_converters
    
    for change in changes.values():
        attribute_name = change.attribute_name
        flags = change.flags
        
        if flags & FLAG_IS_MODIFICATION:
            if converters is None:
                duplet = None
            else:
                duplet = converters.get((attribute_name, FLAG_IS_MODIFICATION), None)
            if duplet is None:
                continue
            
            key, converter = duplet
            
            change_data = {'key': key}
            
            if flags & FLAG_HAS_BEFORE:
                change_data['old_value'] = converter(change.before)
            
            if flags & FLAG_HAS_AFTER:
                change_data['new_value'] = converter(change.after)
            change_datas.append(change_data)
        
        if flags & FLAG_IS_REMOVAL:
            if converters is None:
                duplet = None
            else:
                duplet = converters.get((attribute_name, FLAG_IS_REMOVAL), None)
            if duplet is None:
                continue
            
            key, converter = duplet
            
            change_data = {'key': key}
            
            if flags & FLAG_HAS_BEFORE:
                change_data['new_value'] = converter(change.before)
            
            change_datas.append(change_data)
        
        if flags & FLAG_IS_ADDITION:
            if converters is None:
                duplet = None
            else:
                duplet = converters.get((attribute_name, FLAG_IS_ADDITION), None)
            if duplet is None:
                continue
            
            key, converter = duplet
            
            change_data = {'key': key}
            
            if flags & FLAG_HAS_AFTER:
                change_data['new_value'] = converter(change.after)
            
            change_datas.append(change_data)
    
    
    data['changes'] = change_datas
    return data


def validate_changes(changes, *, entry_type = AuditLogEntryType.none):
    """
    Validates the given changes.
    
    Parameters
    ----------
    changes : `None | iterable<AuditLogChange>`
        Changes to validate
    entry_type : `None`, ``AuditLogEntryType`` = `AuditLogEntryType.none`, Optional (Keyword only)
        The event's type.
    
    Returns
    -------
    changes : `None | dict<str, AuditLogChange>`
    
    Raises
    ------
    TypeError
        . If `changes` type is incorrect.
    ValueError
        - If `changes` value is incorrect.
    """
    if changes is None:
        return None
    
    if (getattr(type(changes), '__iter__', None) is None):
        raise TypeError(
            f'`changes` can be `None`, `iterable` of `{AuditLogChange.__name__}`, '
            f'got {type(changes).__name__}; {AuditLogChange!r}.'
        )
    
    
    change_conversions = entry_type.target_type.change_conversions
    if change_conversions is None:
        validators = None
    else:
        validators = change_conversions.validators
    
    validated_changes = None
    
    for change in changes:
        if not isinstance(change, AuditLogChange):
            raise TypeError(
                f'`changes` can contain `{AuditLogChange.__name__}` elements, '
                f'got {type(change).__name__}; {change!r}; changes = {changes!r}.'
            )
        
        attribute_name = change.attribute_name
        flags = change.flags
        validated_change = AuditLogChange.create_clean(attribute_name)
        
        if flags & FLAG_IS_MODIFICATION:
            if change_conversions is None:
                validator = None
            else:
                validator = validators.get((attribute_name, FLAG_IS_MODIFICATION), None)
            
            if validator is None:
                raise ValueError(
                    f'No validator for `{attribute_name}` of `{get_flags_name(FLAG_IS_MODIFICATION)}` exists, '
                    f'got change = {change!r}; changes = {changes!r}.'
                )
            
            if flags & FLAG_HAS_BEFORE:
                validated_change.before = validator(change.before)
                validated_change.flags |= FLAG_HAS_BEFORE
            
            if flags & FLAG_HAS_AFTER:
                validated_change.after = validator(change.after)
                validated_change.flags |= FLAG_HAS_AFTER
            
            validated_change.flags |= FLAG_IS_MODIFICATION
        
        
        if flags & FLAG_IS_REMOVAL:
            if change_conversions is None:
                validator = None
            else:
                validator = validators.get((attribute_name, FLAG_IS_REMOVAL), None)
            
            if validator is None:
                raise ValueError(
                    f'No validator for `{attribute_name}` of `{get_flags_name(FLAG_IS_REMOVAL)}` exists, '
                    f'got change = {change!r}; changes = {changes!r}.'
                )
            
            if flags & FLAG_HAS_BEFORE:
                validated_change.before = validator(change.before)
                validated_change.flags |= FLAG_HAS_BEFORE
        
            validated_change.flags |= FLAG_IS_REMOVAL
        
        
        if flags & FLAG_IS_ADDITION:
            if change_conversions is None:
                validator = None
            else:
                validator = validators.get((attribute_name, FLAG_IS_ADDITION), None)
            
            if validator is None:
                raise ValueError(
                    f'No validator for `{attribute_name}` of `{get_flags_name(FLAG_IS_ADDITION)}` exists, '
                    f'got change = {change!r}; changes = {changes!r}.'
                )
            
            if flags & FLAG_HAS_AFTER:
                validated_change.after = validator(change.after)
                validated_change.flags |= FLAG_HAS_AFTER
        
            validated_change.flags |= FLAG_IS_ADDITION
        
        if validated_changes is None:
            validated_changes = {}
        validated_changes[attribute_name] = validated_change
    
    return validated_changes


# details

def parse_details(data, entry_type = AuditLogEntryType.none):
    """
    Parses the entry's details.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    entry_type : `None`, ``AuditLogEntryType`` = `AuditLogEntryType.none`, Optional
        The event's type.
    
    Returns
    -------
    changes : `None | dict<str, object>` 
    """
    details_raw = data.get('options', None)
    if (details_raw is None) or (not details_raw):
        return None
    
    details = None
    
    detail_conversions = entry_type.target_type.detail_conversions
    if detail_conversions is None:
        converters = None
    else:
        converters = detail_conversions.get_converters
    
    for key, value in details_raw.items():
        if converters is None:
            duplet = None
        else:
            duplet = converters.get(key, None)
        
        if duplet is None:
            if ALLOW_DEBUG_MESSAGES:
                call_debug_logger(
                    (
                        f'Unknown audit log entry detail key: {key!r}\n'
                        f'- Detail value: {value!r}\n'
                        f'- Event type: {entry_type!r}'
                    ),
                    True,
                )
            continue
        
        name, converter = duplet
        value = converter(value)
        
        if details is None:
            details = {}
        
        details[name] = value
    
    return details


def put_details_into(details, data, defaults, *, entry_type = AuditLogEntryType.none):
    """
    Serialises the given details.
    
    Parameters
    ----------
    details : `None | dict<str, object>` 
        Changes to serialize.
    data : `dict<str, object>`
        Data to extend.
    defaults : `bool`
        Whether fields with the default value should be ignored.
    entry_type : `None`, ``AuditLogEntryType`` = `AuditLogEntryType.none`, Optional (Keyword only)
        The event's type.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if details is None:
        if defaults:
            data['options'] = []
        return data
    
    detail_conversions = entry_type.target_type.detail_conversions
    if detail_conversions is None:
        converters = None
    else:
        converters = detail_conversions.put_converters
    
    details_raw = {}
    
    for name, value in details.items():
        if converters is None:
            duplet = None
        else:
            duplet = converters.get(name, None)
        if duplet is None:
            continue
        
        key, converter = duplet
        details_raw[key] = converter(value)
    
    data['options'] = details_raw
    return data


def validate_details(details, *, entry_type = AuditLogEntryType.none):
    """
    Validates the given details.
    
    Parameters
    ----------
    details : `None | dict<str, object>`
        Changes to validate
    entry_type : `None`, ``AuditLogEntryType`` = `AuditLogEntryType.none`, Optional (Keyword only)
        The event's type.
    
    Returns
    -------
    details : `None | dict<str, object>`
    
    Raises
    ------
    TypeError
        . If `details` type is incorrect.
    ValueError
        - If `details` value is incorrect.
    """
    if details is None:
        return None
    
    if not isinstance(details, dict):
        raise TypeError(
            f'`details` can be `None`, dict`, got {type(details).__name__}; {details!r}.'
        )
    
    detail_conversions = entry_type.target_type.detail_conversions
    if detail_conversions is None:
        validators = None
    else:
        validators = detail_conversions.validators
    
    validated_details = None
    
    for name, value in details.items():
        if not isinstance(name, str):
            raise TypeError(
                f'`details` keys can be `str`, got {type(name).__name__}; {name!r}; details = {details!r}.'
            )
        
        if validators is None:
            validator = None
        else:
            validator = validators.get(name, None)
        if validator is None:
            raise ValueError(
                f'No validator for `{name}` of exists, got value = {value!r}; details = {details!r}.'
            )
        
        value = validator(value)
        
        if validated_details is None:
            validated_details = {}
        validated_details[name] = value
    
    return validated_details


# guild_id

def parse_guild_id(data, parent = None):
    """
    Parses out the entry's guild's identifier.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    parent : `None`, ``AuditLog`` = `None`, Optional
        The parent of the entry.
    
    Returns
    -------
    guild_id : `int`
    """
    if parent is None:
        guild_id = data.get('guild_id', None)
        if guild_id is None:
            guild_id = 0
        else:
            guild_id = int(guild_id)
    else:
        guild_id = parent.guild_id
    
    return guild_id


put_guild_id_into = entity_id_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', Guild)

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('entry_id')

# parent

validate_parent = nullable_entity_validator_factory('parent', NotImplemented, include = 'AuditLog')

# reason

parse_reason = nullable_string_parser_factory('reason')
put_reason_into = nullable_string_optional_putter_factory('reason')
validate_reason = nullable_string_validator_factory('reason', REASON_LENGTH_MIN, REASON_LENGTH_MAX)

# target_id

parse_target_id = entity_id_parser_factory('target_id')
put_target_id_into = entity_id_optional_putter_factory('target_id')
validate_target_id = entity_id_validator_factory('target_id')

# type

parse_type = preinstanced_parser_factory('action_type', AuditLogEntryType, AuditLogEntryType.none)
put_type_into = preinstanced_putter_factory('action_type')
validate_type = preinstanced_validator_factory('entry_type', AuditLogEntryType)

# user_id

parse_user_id = entity_id_parser_factory('user_id')
put_user_id_into = entity_id_optional_putter_factory('user_id')
validate_user_id = entity_id_validator_factory('user_id', ClientUserBase)
