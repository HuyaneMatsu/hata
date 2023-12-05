__all__ = ()

from ...channel import (
    ChannelFlag, ChannelType, ForumLayout, ForumTag, PermissionOverwrite, SortOrder, VideoQualityMode, VoiceRegion
)
from ...channel.channel.fields import validate_type
from ...channel.channel_metadata.constants import (
    AUTO_ARCHIVE_DEFAULT, BITRATE_DEFAULT, SLOWMODE_DEFAULT, USER_LIMIT_DEFAULT
)
from ...channel.channel_metadata.fields import (
    validate_applied_tag_ids, validate_archived, validate_auto_archive_after, validate_available_tags, validate_bitrate,
    validate_default_forum_layout, validate_default_sort_order, validate_default_thread_auto_archive_after,
    validate_default_thread_reaction_emoji, validate_default_thread_slowmode, validate_flags, validate_invitable,
    validate_name, validate_nsfw, validate_open, validate_parent_id, validate_permission_overwrites, validate_position,
    validate_region, validate_slowmode, validate_topic, validate_user_limit, validate_video_quality_mode
)
from ...emoji import create_partial_emoji_data, create_partial_emoji_from_data

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..audit_log_entry_change_conversion.change_deserializers import change_deserializer_deprecation
from ..conversion_helpers.converters import (
    value_deserializer_description, value_deserializer_id, value_deserializer_ids, value_deserializer_name,
    value_serializer_description, value_serializer_id, value_serializer_ids, value_serializer_name
)


# ---- applied_tag_ids ----

APPLIED_TAG_IDS_CONVERSION = AuditLogEntryChangeConversion(
    ('applied_tags',),
    'applied_tag_ids',
    value_deserializer = value_deserializer_ids,
    value_serializer = value_serializer_ids,
    value_validator = validate_applied_tag_ids,
)


# ---- archived ----

ARCHIVED_CONVERSION = AuditLogEntryChangeConversion(
    ('archived',),
    'archived',
    value_validator = validate_archived,
)


@ARCHIVED_CONVERSION.set_value_deserializer
def archived_value_deserializer(value):
    if value is None:
        value = False

    return value


# ---- auto_archive_after ----

AUTO_ARCHIVE_AFTER_CONVERSION = AuditLogEntryChangeConversion(
    ('auto_archive_duration',),
    'auto_archive_after',
    value_validator = validate_auto_archive_after,
)


@AUTO_ARCHIVE_AFTER_CONVERSION.set_value_deserializer
def auto_archive_after_value_deserializer(value):
    if value is None:
        value = AUTO_ARCHIVE_DEFAULT
    else:
        value *= 60
    return value


@AUTO_ARCHIVE_AFTER_CONVERSION.set_value_serializer
def auto_archive_after_value_serializer(value):
    return value // 60


# --- available_tags ----

AVAILABLE_TAGS_CONVERSION = AuditLogEntryChangeConversion(
    ('available_tags',),
    'available_tags',
    value_validator = validate_available_tags,
)


@AVAILABLE_TAGS_CONVERSION.set_value_deserializer
def available_tags_value_deserializer(value):
    if value is None:
        pass
    elif (not value):
        value = None
    else:
        value = (*sorted(ForumTag.from_data(tag_data) for tag_data in value),)
    return value


@AVAILABLE_TAGS_CONVERSION.set_value_serializer
def available_tags_value_serializer(value):
    if value is None:
        value = []
    else:
        value = [forum_tag.to_data(defaults = True, include_internals = True) for forum_tag in value]
    return value


# ---- bitrate ----

BITRATE_CONVERSION = AuditLogEntryChangeConversion(
    ('bitrate',),
    'bitrate',
    value_validator = validate_bitrate,
)


@BITRATE_CONVERSION.set_value_deserializer
def bitrate_value_deserializer(value):
    if value is None:
        value = BITRATE_DEFAULT
    return value


# ---- default_thread_auto_archive_after ----

DEFAULT_THREAD_AUTO_ARCHIVE_AFTER_CONVERSION = AuditLogEntryChangeConversion(
    ('default_auto_archive_duration',),
    'default_thread_auto_archive_after',
    value_validator = validate_default_thread_auto_archive_after,
)


@DEFAULT_THREAD_AUTO_ARCHIVE_AFTER_CONVERSION.set_value_deserializer
def default_thread_auto_archive_after_value_deserializer(value):
    if value is None:
        value = AUTO_ARCHIVE_DEFAULT
    else:
        value *= 60
    return value


@DEFAULT_THREAD_AUTO_ARCHIVE_AFTER_CONVERSION.set_value_serializer
def default_thread_auto_archive_after_value_serializer(value):
    return value // 60


# ---- default_forum_layout ----

DEFAULT_FORUM_LAYOUT_CONVERSION = AuditLogEntryChangeConversion(
    ('default_forum_layout',),
    'default_forum_layout',
    value_validator = validate_default_forum_layout,
)


@DEFAULT_FORUM_LAYOUT_CONVERSION.set_value_deserializer
def default_forum_layout_value_deserializer(value):
    return ForumLayout.get(value)


@DEFAULT_FORUM_LAYOUT_CONVERSION.set_value_serializer
def default_forum_layout_value_serializer(value):
    return value.value


# ---- default_sort_order ----

DEFAULT_SORT_ORDER_CONVERSION = AuditLogEntryChangeConversion(
    ('default_sort_order',),
    'default_sort_order',
    value_validator = validate_default_sort_order,
)


@DEFAULT_SORT_ORDER_CONVERSION.set_value_deserializer
def default_sort_order_value_deserializer(value):
    return SortOrder.get(value)


@DEFAULT_SORT_ORDER_CONVERSION.set_value_serializer
def default_sort_order_value_serializer(value):
    return value.value


# ---- default_thread_reaction_emoji ----

DEFAULT_THREAD_REACTION_EMOJI_CONVERSION = AuditLogEntryChangeConversion(
    ('default_reaction_emoji',),
    'default_thread_reaction_emoji',
    value_validator = validate_default_thread_reaction_emoji,
)


@DEFAULT_THREAD_REACTION_EMOJI_CONVERSION.set_value_deserializer
def default_thread_reaction_emoji_value_deserializer(value):
    if (value is not None):
        value = create_partial_emoji_from_data(value)
    
    return value


@DEFAULT_THREAD_REACTION_EMOJI_CONVERSION.set_value_serializer
def default_thread_reaction_emoji_value_serializer(value):
    if value is not None:
        value = create_partial_emoji_data(value)
    
    return value


# ---- default_thread_slowmode ----

DEFAULT_THREAD_SLOWMODE_CONVERSION = AuditLogEntryChangeConversion(
    ('default_thread_rate_limit_per_user',),
    'default_thread_slowmode',
    value_validator = validate_default_thread_slowmode,
)

@DEFAULT_THREAD_SLOWMODE_CONVERSION.set_value_deserializer
def default_thread_slowmode_value_deserializer(value):
    if value is None:
        value = SLOWMODE_DEFAULT
    return value


# ---- flags ----

FLAGS_CONVERSION = AuditLogEntryChangeConversion(
    ('flags',),
    'flags',
    value_validator = validate_flags,
)


@FLAGS_CONVERSION.set_value_deserializer
def flags_value_deserializer(value):
    if value is None:
        value = ChannelFlag()
    else:
        value = ChannelFlag(value)
    
    return value


@FLAGS_CONVERSION.set_value_serializer
def flags_value_serializer(value):
    return int(value)


# ---- icon_emoji  ----

ICON_EMOJI_CONVERSION_IGNORED = AuditLogEntryChangeConversion(
    ('icon_emoji',),
    '',
    change_deserializer = change_deserializer_deprecation,
)


# ---- invitable ----

INVITABLE_CONVERSION = AuditLogEntryChangeConversion(
    ('invitable',),
    'invitable',
    value_validator = validate_invitable,
)


@INVITABLE_CONVERSION.set_value_deserializer
def invitable_value_deserializer(value):
    if value is None:
        value = True
    return value


# ---- name ----

NAME_CONVERSION = AuditLogEntryChangeConversion(
    ('name',),
    'name',
    value_deserializer = value_deserializer_name,
    value_serializer = value_serializer_name,
    value_validator = validate_name,
)


# ---- nsfw ----

NSFW_CONVERSION = AuditLogEntryChangeConversion(
    ('nsfw',),
    'nsfw',
    value_validator = validate_nsfw,
)


@NSFW_CONVERSION.set_value_deserializer
def nsfw_value_deserializer(value):
    if value is None:
        value = False
    return value


# ---- open ----

OPEN_CONVERSION = AuditLogEntryChangeConversion(
    ('locked',),
    'open',
    value_validator = validate_open,
)


@OPEN_CONVERSION.set_value_deserializer
def open_value_deserializer(value):
    if value is None:
        value = True
    else:
        value = not value
    return value


@OPEN_CONVERSION.set_value_serializer
def open_value_serializer(value):
    return not value


# ---- parent_id ----

PARENT_ID_CONVERSION = AuditLogEntryChangeConversion(
    ('parent_id',),
    'parent_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_parent_id,
)


# ---- permission_overwrites ----

PERMISSION_OVERWRITES_CONVERSION = AuditLogEntryChangeConversion(
    ('permission_overwrites',),
    'permission_overwrites',
    value_validator = validate_permission_overwrites,
)

@PERMISSION_OVERWRITES_CONVERSION.set_value_deserializer
def permission_overwrite_value_deserializer(value):
    if value is None:
        pass
    elif (not value):
        value = None
    else:
        value = {
            permission_overwrite.target_id: permission_overwrite for permission_overwrite in
            (PermissionOverwrite.from_data(overwrite_data) for overwrite_data in value)
        }
    
    return value


@PERMISSION_OVERWRITES_CONVERSION.set_value_serializer
def permission_overwrite_value_serializer(value):
    if value is None:
        value = []
    else:
        value = [
            permission_overwrite.to_data(defaults = True, include_internals = True)
            for permission_overwrite in sorted(value.values())
        ]
    
    return value


# ---- position ----

POSITION_CONVERSION = AuditLogEntryChangeConversion(
    ('position',),
    'position',
    value_validator = validate_position,
)

@POSITION_CONVERSION.set_value_deserializer
def position_value_deserializer(value):
    if value is None:
        value = 0
    return value


# ---- region ----

REGION_CONVERSION = AuditLogEntryChangeConversion(
    ('rtc_region',),
    'region',
    value_validator = validate_region,
)


@REGION_CONVERSION.set_value_deserializer
def region_value_deserializer(value):
    return VoiceRegion.get(value)


@REGION_CONVERSION.set_value_serializer
def region_value_serializer(value):
    return value.value


# ---- slowmode ----

SLOWMODE_CONVERSION = AuditLogEntryChangeConversion(
    ('rate_limit_per_user',),
    'slowmode',
    value_validator = validate_slowmode,
)

@SLOWMODE_CONVERSION.set_value_deserializer
def slowmode_value_deserializer(value):
    if value is None:
        value = SLOWMODE_DEFAULT
    return value


# ---- template  ----

TEMPLATE_CONVERSION_IGNORED = AuditLogEntryChangeConversion(
    ('template',),
    '',
    change_deserializer = change_deserializer_deprecation,
)


# ---- theme_color  ----

THEME_COLOR_CONVERSION_IGNORED = AuditLogEntryChangeConversion(
    ('theme_color',),
    '',
    change_deserializer = change_deserializer_deprecation,
)


# ---- topic ----

TOPIC_CONVERSION = AuditLogEntryChangeConversion(
    ('topic',),
    'topic',
    value_deserializer = value_deserializer_description,
    value_serializer = value_serializer_description,
    value_validator = validate_topic,
)


# ---- type ----

TYPE_CONVERSION = AuditLogEntryChangeConversion(
    ('type',),
    'type',
    value_validator = validate_type,
)


@TYPE_CONVERSION.set_value_deserializer
def type_value_deserializer(value):
    return ChannelType.get(value)


@TYPE_CONVERSION.set_value_serializer
def type_value_serializer(value):
    return value.value


# ---- video_quality_mode ----

VIDEO_QUALITY_MODE_CONVERSION = AuditLogEntryChangeConversion(
    ('video_quality_mode',),
    'video_quality_mode',
    value_validator = validate_video_quality_mode,
)


@VIDEO_QUALITY_MODE_CONVERSION.set_value_deserializer
def video_quality_mode_value_deserializer(value):
    return VideoQualityMode.get(value)


@VIDEO_QUALITY_MODE_CONVERSION.set_value_serializer
def video_quality_mode_value_serializer(value):
    return value.value


# ---- user_limit ----

USER_LIMIT_CONVERSION = AuditLogEntryChangeConversion(
    ('user_limit',),
    'user_limit',
    value_validator = validate_user_limit,
)

@USER_LIMIT_CONVERSION.set_value_deserializer
def user_limit_value_deserializer(value):
    if value is None:
        value = USER_LIMIT_DEFAULT
    return value


# ---- Construct ----

CHANNEL_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    APPLIED_TAG_IDS_CONVERSION,
    ARCHIVED_CONVERSION,
    AUTO_ARCHIVE_AFTER_CONVERSION,
    AVAILABLE_TAGS_CONVERSION,
    BITRATE_CONVERSION,
    DEFAULT_THREAD_AUTO_ARCHIVE_AFTER_CONVERSION,
    DEFAULT_FORUM_LAYOUT_CONVERSION,
    DEFAULT_SORT_ORDER_CONVERSION,
    DEFAULT_THREAD_REACTION_EMOJI_CONVERSION,
    DEFAULT_THREAD_SLOWMODE_CONVERSION,
    FLAGS_CONVERSION,
    ICON_EMOJI_CONVERSION_IGNORED,
    INVITABLE_CONVERSION,
    NAME_CONVERSION,
    NSFW_CONVERSION,
    OPEN_CONVERSION,
    PARENT_ID_CONVERSION,
    PERMISSION_OVERWRITES_CONVERSION,
    POSITION_CONVERSION,
    REGION_CONVERSION,
    SLOWMODE_CONVERSION,
    TEMPLATE_CONVERSION_IGNORED,
    THEME_COLOR_CONVERSION_IGNORED,
    TOPIC_CONVERSION,
    TYPE_CONVERSION,
    VIDEO_QUALITY_MODE_CONVERSION,
    USER_LIMIT_CONVERSION,
)
