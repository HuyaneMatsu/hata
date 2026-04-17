import vampytest

from ....application_command import (
    ApplicationCommandPermissionOverwrite, ApplicationCommandPermissionOverwriteTargetType
)
from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ...audit_log_change import AuditLogChange
from ...audit_log_change.flags import FLAG_HAS_AFTER, FLAG_HAS_BEFORE

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion
from ..change_serializers import (
    change_serializer_addition_and_removal, change_serializer_application_command_permission_overwrite,
    change_serializer_flattened_emoji, change_serializer_modification
)


def _iter_options__change_serializer_modification():
    yield (
        AuditLogEntryChangeConversion(
            ('koishi',),
            '',
            change_serializer = change_serializer_modification,
        ),
        AuditLogChange.from_fields('koishi', 0, None, None),
        [{'key': 'koishi'}],
    )

    yield (
        AuditLogEntryChangeConversion(
            ('koishi',),
            '',
            change_serializer = change_serializer_modification,
        ),
        AuditLogChange.from_fields('koishi', FLAG_HAS_BEFORE, 12, None),
        [{'key': 'koishi', 'old_value': 12}],
    )

    yield (
        AuditLogEntryChangeConversion(
            ('koishi',),
            '',
            change_serializer = change_serializer_modification,
        ),
        AuditLogChange.from_fields('koishi', FLAG_HAS_AFTER, None, 14),
        [{'key': 'koishi', 'new_value': 14}],
    )

    yield (
        AuditLogEntryChangeConversion(
            None,
            'koishi',
            change_serializer = change_serializer_modification,
        ),
        AuditLogChange.from_fields('koishi', FLAG_HAS_BEFORE | FLAG_HAS_AFTER, 12, 14),
        [{'key': None, 'old_value': 12, 'new_value': 14}],
    )

    yield (
        AuditLogEntryChangeConversion(
            ('koishi',),
            '',
            change_serializer = change_serializer_modification,
            value_serializer = (lambda x: x + 5),
        ),
        AuditLogChange.from_fields('koishi', FLAG_HAS_BEFORE | FLAG_HAS_AFTER, 12, 14),
        [{'key': 'koishi', 'old_value': 17, 'new_value': 19}],
    )


@vampytest._(vampytest.call_from(_iter_options__change_serializer_modification()).returning_last())
def test_change_serializer_modification(conversion, change):
    """
    Tests whether ``change_serializer_modification`` works as intended.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        The conversion to pull its field of.
    change : ``AuditLogChange``
        Audit log change to deserialize.
    
    Yields
    ------
    output : `list<dict<str, object>>`
    """
    return [*conversion.change_serializer(conversion, change)]


def _iter_options__change_serializer_addition_and_removal():
    yield (
        AuditLogEntryChangeConversion(
            ('koishi', 'satori'),
            'koishi',
            change_serializer = change_serializer_addition_and_removal,
        ),
        AuditLogChange.from_fields('koishi', 0, None, None),
        [],
    )

    yield (
        AuditLogEntryChangeConversion(
            ('koishi', 'satori'),
            'koishi',
            change_serializer = change_serializer_addition_and_removal,
        ),
        AuditLogChange.from_fields('koishi', FLAG_HAS_BEFORE, 12, None),
        [{'key': 'koishi', 'new_value': 12}],
    )

    yield (
        AuditLogEntryChangeConversion(
            ('koishi', 'satori'),
            'koishi',
            change_serializer = change_serializer_addition_and_removal,
        ),
        AuditLogChange.from_fields('koishi', FLAG_HAS_AFTER, None, 14),
        [{'key': 'satori', 'new_value': 14}],
    )

    yield (
        AuditLogEntryChangeConversion(
            ('koishi', 'satori'),
            'koishi',
            change_serializer = change_serializer_addition_and_removal,
        ),
        AuditLogChange.from_fields('koishi', FLAG_HAS_BEFORE | FLAG_HAS_AFTER, 12, 14),
        [{'key': 'koishi', 'new_value': 12}, {'key': 'satori', 'new_value': 14}],
    )

    yield (
        AuditLogEntryChangeConversion(
            ('koishi', 'satori'),
            'koishi',
            change_serializer = change_serializer_addition_and_removal,
            value_serializer = (lambda x: x + 5),
        ),
        AuditLogChange.from_fields('koishi', FLAG_HAS_BEFORE | FLAG_HAS_AFTER, 12, 14),
        [{'key': 'koishi', 'new_value': 17}, {'key': 'satori', 'new_value': 19}],
    )


@vampytest._(vampytest.call_from(_iter_options__change_serializer_addition_and_removal()).returning_last())
def test_change_serializer_addition_and_removal(conversion, change):
    """
    Tests whether ``change_serializer_addition_and_removal`` works as intended.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        The conversion to pull its field of.
    change : ``AuditLogChange``
        Audit log change to deserialize.
    
    Yields
    ------
    output : `list<dict<str, object>>`
    """
    return [*conversion.change_serializer(conversion, change)]


def _iter_options__change_serializer_flattened_emoji():
    emoji_0 = Emoji.precreate(202311160003)
    emoji_1 = BUILTIN_EMOJIS['x']
    
    yield (
        AuditLogEntryChangeConversion(
            ('emoji_name', 'emoji_id'),
            'emoji',
            change_serializer = change_serializer_flattened_emoji,
        ),
        AuditLogChange.from_fields('emoji', 0, None, None),
        [],
    )

    yield (
        AuditLogEntryChangeConversion(
            ('emoji_name', 'emoji_id'),
            'emoji',
            change_serializer = change_serializer_flattened_emoji,
        ),
        AuditLogChange.from_fields('emoji', FLAG_HAS_BEFORE, emoji_0, None),
        [{'key': 'emoji_id', 'old_value': str(emoji_0.id)}],
    )

    yield (
        AuditLogEntryChangeConversion(
            ('emoji_name', 'emoji_id'),
            'emoji',
            change_serializer = change_serializer_flattened_emoji,
        ),
        AuditLogChange.from_fields('emoji', FLAG_HAS_AFTER, None, emoji_0),
        [{'key': 'emoji_id', 'new_value': str(emoji_0.id)}],
    )

    yield (
        AuditLogEntryChangeConversion(
            ('emoji_name', 'emoji_id'),
            'emoji',
            change_serializer = change_serializer_flattened_emoji,
        ),
        AuditLogChange.from_fields('emoji', FLAG_HAS_BEFORE | FLAG_HAS_AFTER, emoji_0, emoji_0),
        [{'key': 'emoji_id', 'old_value': str(emoji_0.id), 'new_value': str(emoji_0.id)}],
    )

    yield (
        AuditLogEntryChangeConversion(
            ('emoji_name', 'emoji_id'),
            'emoji',
            change_serializer = change_serializer_flattened_emoji,
        ),
        AuditLogChange.from_fields('emoji', FLAG_HAS_BEFORE, emoji_1, None),
        [{'key': 'emoji_name', 'old_value': emoji_1.unicode}],
    )

    yield (
        AuditLogEntryChangeConversion(
            ('emoji_name', 'emoji_id'),
            'emoji',
            change_serializer = change_serializer_flattened_emoji,
        ),
        AuditLogChange.from_fields('emoji', FLAG_HAS_AFTER, None, emoji_1),
        [{'key': 'emoji_name', 'new_value': emoji_1.unicode}],
    )

    yield (
        AuditLogEntryChangeConversion(
            ('emoji_name', 'emoji_id'),
            'emoji',
            change_serializer = change_serializer_flattened_emoji,
        ),
        AuditLogChange.from_fields('emoji', FLAG_HAS_BEFORE | FLAG_HAS_AFTER, emoji_1, emoji_1),
        [{'key': 'emoji_name', 'old_value': emoji_1.unicode, 'new_value': emoji_1.unicode}],
    )

    yield (
        AuditLogEntryChangeConversion(
            ('emoji_name', 'emoji_id'),
            'emoji',
            change_serializer = change_serializer_flattened_emoji,
        ),
        AuditLogChange.from_fields('emoji', FLAG_HAS_BEFORE | FLAG_HAS_AFTER, emoji_0, emoji_1),
        [{'key': 'emoji_id', 'old_value': str(emoji_0.id)}, {'key': 'emoji_name', 'new_value': emoji_1.unicode}],
    )

    yield (
        AuditLogEntryChangeConversion(
            ('emoji_name', 'emoji_id'),
            'emoji',
            change_serializer = change_serializer_flattened_emoji,
        ),
        AuditLogChange.from_fields('emoji', FLAG_HAS_BEFORE | FLAG_HAS_AFTER, emoji_1, emoji_0),
        [{'key': 'emoji_name', 'old_value': emoji_1.unicode}, {'key': 'emoji_id', 'new_value': str(emoji_0.id)}],
    )


@vampytest._(vampytest.call_from(_iter_options__change_serializer_flattened_emoji()).returning_last())
def test_change_serializer_flattened_emoji(conversion, change):
    """
    Tests whether ``change_serializer_flattened_emoji`` works as intended.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        The conversion to pull its field of.
    change : ``AuditLogChange``
        Audit log change to deserialize.
    
    Yields
    ------
    output : `list<dict<str, object>>`
    """
    return [*conversion.change_serializer(conversion, change)]




def _iter_options__change_serializer_application_command_permission_overwrite():
    permission_overwrite_0 = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202311160004), True
    )
    permission_overwrite_1 = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202311160004), False
    )
    permission_overwrite_2 = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202311160005), False
    )
    permission_overwrite_3 = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202311160006), True
    )
    
    
    yield (
        AuditLogEntryChangeConversion(
            '\\d+',
            'permission_overwrites',
            change_serializer = change_serializer_application_command_permission_overwrite,
        ),
        AuditLogChange.from_fields('koishi', 0, None, None),
        [],
    )

    yield (
        AuditLogEntryChangeConversion(
            '\\d+',
            'permission_overwrites',
            change_serializer = change_serializer_application_command_permission_overwrite,
        ),
        AuditLogChange.from_fields('permission_overwrites', FLAG_HAS_BEFORE, (permission_overwrite_0,), None),
        [{'key': str(permission_overwrite_0.target_id), 'old_value': permission_overwrite_0.to_data(defaults = True)}],
    )

    yield (
        AuditLogEntryChangeConversion(
            '\\d+',
            'permission_overwrites',
            change_serializer = change_serializer_application_command_permission_overwrite,
        ),
        AuditLogChange.from_fields('permission_overwrites', FLAG_HAS_AFTER, None, (permission_overwrite_1,)),
        [{'key': str(permission_overwrite_0.target_id), 'new_value': permission_overwrite_1.to_data(defaults = True)}],
    )

    yield (
        AuditLogEntryChangeConversion(
            '\\d+',
            'permission_overwrites',
            change_serializer = change_serializer_application_command_permission_overwrite,
        ),
        AuditLogChange.from_fields(
            'permission_overwrites',
            FLAG_HAS_BEFORE | FLAG_HAS_AFTER,
            (permission_overwrite_0,),
            (permission_overwrite_1,),
        ),
        [
            {
                'key': str(permission_overwrite_0.target_id),
                'old_value': permission_overwrite_0.to_data(defaults = True),
                'new_value': permission_overwrite_1.to_data(defaults = True),
            },
        ],
    )

    yield (
        AuditLogEntryChangeConversion(
            '\\d+',
            'permission_overwrites',
            change_serializer = change_serializer_application_command_permission_overwrite,
        ),
        AuditLogChange.from_fields(
            'permission_overwrites',
            FLAG_HAS_BEFORE | FLAG_HAS_AFTER,
            (permission_overwrite_0, permission_overwrite_2),
            (permission_overwrite_1, permission_overwrite_3),
        ),
        [
            {
                'key': str(permission_overwrite_0.target_id),
                'old_value': permission_overwrite_0.to_data(defaults = True),
                'new_value': permission_overwrite_1.to_data(defaults = True),
            },
            {
                'key': str(permission_overwrite_2.target_id),
                'old_value': permission_overwrite_2.to_data(defaults = True),
            },
            {
                'key': str(permission_overwrite_3.target_id),
                'new_value': permission_overwrite_3.to_data(defaults = True),
            },
        ],
    )


@vampytest._(
    vampytest.call_from(_iter_options__change_serializer_application_command_permission_overwrite()).returning_last()
)
def test_change_serializer_application_command_permission_overwrite(conversion, change):
    """
    Tests whether ``change_serializer_application_command_permission_overwrite`` works as intended.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        The conversion to pull its field of.
    change : ``AuditLogChange``
        Audit log change to deserialize.
    
    Yields
    ------
    output : `list<dict<str, object>>`
    """
    return [*conversion.change_serializer(conversion, change)]
