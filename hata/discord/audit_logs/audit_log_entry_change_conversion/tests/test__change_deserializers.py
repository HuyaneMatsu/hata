import vampytest

from ....application_command import (
    ApplicationCommandPermissionOverwrite, ApplicationCommandPermissionOverwriteTargetType
)
from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ...audit_log_change import AuditLogChange
from ...audit_log_change.flags import FLAG_HAS_AFTER, FLAG_HAS_BEFORE

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion
from ..change_deserializers import (
    change_deserializer_addition_and_removal, change_deserializer_application_command_permission_overwrite,
    change_deserializer_deprecation, change_deserializer_flattened_emoji, change_deserializer_modification
)


def _iter_options__change_deserializer_modification():
    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_modification,
        ),
        {},
        [],
    )

    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_modification,
        ),
        {'old_value': 56},
        [AuditLogChange.from_fields('koishi', FLAG_HAS_BEFORE, 56, None)],
    )

    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_modification,
        ),
        {'new_value': 56},
        [AuditLogChange.from_fields('koishi', FLAG_HAS_AFTER, None, 56)],
    )

    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_modification,
        ),
        {'old_value': 12, 'new_value': 56},
        [AuditLogChange.from_fields('koishi', FLAG_HAS_BEFORE | FLAG_HAS_AFTER, 12, 56)],
    )

    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_modification,
            value_deserializer = (lambda x: x + 5),
        ),
        {'old_value': 12, 'new_value': 56},
        [AuditLogChange.from_fields('koishi', FLAG_HAS_BEFORE | FLAG_HAS_AFTER, 17, 61)],
    )


@vampytest._(vampytest.call_from(_iter_options__change_deserializer_modification()).returning_last())
def test__change_deserializer_modification(conversion, change_data):
    """
    Tests whether ``change_deserializer_modification`` works as intended.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        Conversion to use.
    change_data : `dict<str, object>`
        Change data to process.
    
    Returns
    -------
    output : `list<AuditLogChange>`
    """
    return [*conversion.change_deserializer(conversion, change_data)]


def _iter_options__change_deserializer_addition_and_removal():
    yield (
        AuditLogEntryChangeConversion(
            ('hey', 'mister'),
            'koishi',
            change_deserializer = change_deserializer_addition_and_removal,
        ),
        {'key': 'hey'},
        [],
    )
    
    yield (
        AuditLogEntryChangeConversion(
            ('hey', 'mister'),
            'koishi',
            change_deserializer = change_deserializer_addition_and_removal,
        ),
        {'key': 'hey', 'new_value': 12},
        [AuditLogChange.from_fields('koishi', FLAG_HAS_BEFORE, 12, None)],
    )
    
    yield (
        AuditLogEntryChangeConversion(
            ('hey', 'mister'),
            'koishi',
            change_deserializer = change_deserializer_addition_and_removal,
        ),
        {'key': 'mister', 'new_value': 14},
        [AuditLogChange.from_fields('koishi', FLAG_HAS_AFTER, None, 14)],
    )
    
    yield (
        AuditLogEntryChangeConversion(
            ('hey', 'mister'),
            'koishi',
            change_deserializer = change_deserializer_addition_and_removal,
            value_deserializer = (lambda x: x + 5),
        ),
        {'key': 'hey', 'new_value': 12},
        [AuditLogChange.from_fields('koishi', FLAG_HAS_BEFORE, 17, None)],
    )
    
    yield (
        AuditLogEntryChangeConversion(
            ('hey', 'mister'),
            'koishi',
            change_deserializer = change_deserializer_addition_and_removal,
            value_deserializer = (lambda x: x + 5),
        ),
        {'key': 'mister', 'new_value': 14},
        [AuditLogChange.from_fields('koishi', FLAG_HAS_AFTER, None, 19)],
    )


@vampytest._(vampytest.call_from(_iter_options__change_deserializer_addition_and_removal()).returning_last())
def test__change_deserializer_addition_and_removal(conversion, change_data):
    """
    Tests whether ``change_deserializer_addition_and_removal`` works as intended.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        Conversion to use.
    change_data : `dict<str, object>`
        Change data to process.
    
    Returns
    -------
    output : `list<AuditLogChange>`
    """
    return [*conversion.change_deserializer(conversion, change_data)]


def _iter_options__change_deserializer_deprecation():
    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_deprecation,
        ),
        {},
        [],
    )

    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_deprecation,
        ),
        {'old_value': 56, 'new_value': 56},
        [],
    )


@vampytest._(vampytest.call_from(_iter_options__change_deserializer_deprecation()).returning_last())
def test__change_deserializer_deprecation(conversion, change_data):
    """
    Tests whether ``change_deserializer_deprecation`` works as intended.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        Conversion to use.
    change_data : `dict<str, object>`
        Change data to process.
    
    Returns
    -------
    output : `list<AuditLogChange>`
    """
    return [*conversion.change_deserializer(conversion, change_data)]


def _iter_options__change_deserializer_flattened_emoji():
    emoji_0 = Emoji.precreate(202311160001)
    emoji_1 = BUILTIN_EMOJIS['x']
    
    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_flattened_emoji,
        ),
        {},
        [],
    )

    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_flattened_emoji,
        ),
        {'key': 'emoji_name', 'old_value': None},
        [AuditLogChange.from_fields('koishi', FLAG_HAS_BEFORE, None, None)],
    )

    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_flattened_emoji,
        ),
        {'key': 'emoji_name', 'old_value': emoji_1.unicode},
        [AuditLogChange.from_fields('koishi', FLAG_HAS_BEFORE, emoji_1, None)],
    )

    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_flattened_emoji,
        ),
        {'key': 'emoji_name', 'new_value': None},
        [AuditLogChange.from_fields('koishi', FLAG_HAS_AFTER, None, None)],
    )

    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_flattened_emoji,
        ),
        {'key': 'emoji_name', 'new_value': emoji_1.unicode},
        [AuditLogChange.from_fields('koishi', FLAG_HAS_AFTER, None, emoji_1)],
    )

    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_flattened_emoji,
        ),
        {'key': 'emoji_name', 'old_value': None, 'new_value': None},
        [AuditLogChange.from_fields('koishi', FLAG_HAS_BEFORE | FLAG_HAS_AFTER, None, None)],
    )

    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_flattened_emoji,
        ),
        {'key': 'emoji_name', 'old_value': emoji_1.unicode, 'new_value': emoji_1.unicode},
        [AuditLogChange.from_fields('koishi', FLAG_HAS_BEFORE | FLAG_HAS_AFTER, emoji_1, emoji_1)],
    )

    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_flattened_emoji,
        ),
        {'key': 'emoji_id', 'old_value': None},
        [AuditLogChange.from_fields('koishi', FLAG_HAS_BEFORE, None, None)],
    )

    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_flattened_emoji,
        ),
        {'key': 'emoji_id', 'old_value': str(emoji_0.id)},
        [AuditLogChange.from_fields('koishi', FLAG_HAS_BEFORE, emoji_0, None)],
    )

    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_flattened_emoji,
        ),
        {'key': 'emoji_id', 'new_value': None},
        [AuditLogChange.from_fields('koishi', FLAG_HAS_AFTER, None, None)],
    )

    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_flattened_emoji,
        ),
        {'key': 'emoji_id', 'new_value': str(emoji_0.id)},
        [AuditLogChange.from_fields('koishi', FLAG_HAS_AFTER, None, emoji_0)],
    )

    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_flattened_emoji,
        ),
        {'key': 'emoji_id', 'old_value': None, 'new_value': None},
        [AuditLogChange.from_fields('koishi', FLAG_HAS_BEFORE | FLAG_HAS_AFTER, None, None)],
    )

    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_flattened_emoji,
        ),
        {'key': 'emoji_id', 'old_value': str(emoji_0.id), 'new_value': str(emoji_0.id)},
        [AuditLogChange.from_fields('koishi', FLAG_HAS_BEFORE | FLAG_HAS_AFTER, emoji_0, emoji_0)],
    )


@vampytest._(vampytest.call_from(_iter_options__change_deserializer_flattened_emoji()).returning_last())
def test__change_deserializer_flattened_emoji(conversion, change_data):
    """
    Tests whether ``change_deserializer_flattened_emoji`` works as intended.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        Conversion to use.
    change_data : `dict<str, object>`
        Change data to process.
    
    Returns
    -------
    output : `list<AuditLogChange>`
    """
    return [*conversion.change_deserializer(conversion, change_data)]


def _iter_options__change_deserializer_application_command_permission_overwrite():
    permission_overwrite_0 = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202311160002), True
    )
    permission_overwrite_1 = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202311160002), False
    )
    
    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_application_command_permission_overwrite,
        ),
        {},
        [],
    )
    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_application_command_permission_overwrite,
        ),
        {'key': str(permission_overwrite_0.target_id), 'old_value': permission_overwrite_0.to_data()},
        [AuditLogChange.from_fields('koishi', FLAG_HAS_BEFORE, (permission_overwrite_0,), None)],
    )

    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_application_command_permission_overwrite,
        ),
        {'key': str(permission_overwrite_0.target_id), 'new_value': permission_overwrite_0.to_data()},
        [AuditLogChange.from_fields('koishi', FLAG_HAS_AFTER, None, (permission_overwrite_0,))],
    )

    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_deserializer = change_deserializer_application_command_permission_overwrite,
        ),
        {
            'key': str(permission_overwrite_0.target_id),
            'old_value': permission_overwrite_0.to_data(),
            'new_value': permission_overwrite_1.to_data(),
        },
        [
            AuditLogChange.from_fields(
                'koishi', 
                FLAG_HAS_BEFORE | FLAG_HAS_AFTER,
                (permission_overwrite_0,),
                (permission_overwrite_1,),
            ),
        ],
    )


@vampytest._(
    vampytest.call_from(_iter_options__change_deserializer_application_command_permission_overwrite()).returning_last()
)
def test__change_deserializer_application_command_permission_overwrite(conversion, change_data):
    """
    Tests whether ``change_deserializer_application_command_permission_overwrite`` works as intended.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        Conversion to use.
    change_data : `dict<str, object>`
        Change data to process.
    
    Returns
    -------
    output : `list<AuditLogChange>`
    """
    return [*conversion.change_deserializer(conversion, change_data)]

