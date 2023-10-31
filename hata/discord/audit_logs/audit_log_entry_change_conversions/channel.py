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
    validate_default_thread_reaction, validate_default_thread_slowmode, validate_flags, validate_invitable,
    validate_name, validate_nsfw, validate_open, validate_parent_id, validate_permission_overwrites, validate_position,
    validate_region, validate_slowmode, validate_topic, validate_user_limit, validate_video_quality_mode
)
from ...emoji import create_emoji_from_exclusive_data, put_exclusive_emoji_data_into

from ..audit_log_change.flags import FLAG_IS_MODIFICATION
from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import (
    get_converter_description, get_converter_id, get_converter_ids, get_converter_name, put_converter_description,
    put_converter_id, put_converter_ids, put_converter_name
)


# ---- applied_tag_ids ----

APPLIED_TAG_IDS_CONVERSION = AuditLogEntryChangeConversion(
    'applied_tags',
    'applied_tag_ids',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_ids,
    put_converter = put_converter_ids,
    validator = validate_applied_tag_ids,
)


# ---- archived ----

ARCHIVED_CONVERSION = AuditLogEntryChangeConversion(
    'archived',
    'archived',
    FLAG_IS_MODIFICATION,
    validator = validate_archived,
)


@ARCHIVED_CONVERSION.set_get_converter
def archived_get_converter(value):
    if value is None:
        value = False

    return value


# ---- auto_archive_after ----

AUTO_ARCHIVE_AFTER_CONVERSION = AuditLogEntryChangeConversion(
    'auto_archive_duration',
    'auto_archive_after',
    FLAG_IS_MODIFICATION,
    validator = validate_auto_archive_after,
)


@AUTO_ARCHIVE_AFTER_CONVERSION.set_get_converter
def auto_archive_after_get_converter(value):
    if value is None:
        value = AUTO_ARCHIVE_DEFAULT
    else:
        value *= 60
    return value


@AUTO_ARCHIVE_AFTER_CONVERSION.set_put_converter
def auto_archive_after_put_converter(value):
    return value // 60


# --- available_tags ----

AVAILABLE_TAGS_CONVERSION = AuditLogEntryChangeConversion(
    'available_tags',
    'available_tags',
    FLAG_IS_MODIFICATION,
    validator = validate_available_tags,
)


@AVAILABLE_TAGS_CONVERSION.set_get_converter
def available_tags_get_converter(value):
    if value is None:
        pass
    elif (not value):
        value = None
    else:
        value = (*sorted(ForumTag.from_data(tag_data) for tag_data in value),)
    return value


@AVAILABLE_TAGS_CONVERSION.set_put_converter
def available_tags_put_converter(value):
    if value is None:
        value = []
    else:
        value = [forum_tag.to_data(defaults = True, include_internals = True) for forum_tag in value]
    return value


# ---- bitrate ----

BITRATE_CONVERSION = AuditLogEntryChangeConversion(
    'bitrate',
    'bitrate',
    FLAG_IS_MODIFICATION,
    validator = validate_bitrate,
)


@BITRATE_CONVERSION.set_get_converter
def bitrate_get_converter(value):
    if value is None:
        value = BITRATE_DEFAULT
    return value


# ---- default_thread_auto_archive_after ----

DEFAULT_THREAD_AUTO_ARCHIVE_AFTER_CONVERSION = AuditLogEntryChangeConversion(
    'default_auto_archive_duration',
    'default_thread_auto_archive_after',
    FLAG_IS_MODIFICATION,
    validator = validate_default_thread_auto_archive_after,
)


@DEFAULT_THREAD_AUTO_ARCHIVE_AFTER_CONVERSION.set_get_converter
def default_thread_auto_archive_after_get_converter(value):
    if value is None:
        value = AUTO_ARCHIVE_DEFAULT
    else:
        value *= 60
    return value


@DEFAULT_THREAD_AUTO_ARCHIVE_AFTER_CONVERSION.set_put_converter
def default_thread_auto_archive_after_put_converter(value):
    return value // 60


# ---- default_forum_layout ----

DEFAULT_FORUM_LAYOUT_CONVERSION = AuditLogEntryChangeConversion(
    'default_forum_layout',
    'default_forum_layout',
    FLAG_IS_MODIFICATION,
    validator = validate_default_forum_layout,
)


@DEFAULT_FORUM_LAYOUT_CONVERSION.set_get_converter
def default_forum_layout_get_converter(value):
    return ForumLayout.get(value)


@DEFAULT_FORUM_LAYOUT_CONVERSION.set_put_converter
def default_forum_layout_put_converter(value):
    return value.value


# ---- default_sort_order ----

DEFAULT_SORT_ORDER_CONVERSION = AuditLogEntryChangeConversion(
    'default_sort_order',
    'default_sort_order',
    FLAG_IS_MODIFICATION,
    validator = validate_default_sort_order,
)


@DEFAULT_SORT_ORDER_CONVERSION.set_get_converter
def default_sort_order_get_converter(value):
    return SortOrder.get(value)


@DEFAULT_SORT_ORDER_CONVERSION.set_put_converter
def default_sort_order_put_converter(value):
    return value.value


# ---- default_thread_reaction ----

DEFAULT_THREAD_REACTION_CONVERSION = AuditLogEntryChangeConversion(
    'default_reaction_emoji',
    'default_thread_reaction',
    FLAG_IS_MODIFICATION,
    validator = validate_default_thread_reaction,
)


@DEFAULT_THREAD_REACTION_CONVERSION.set_get_converter
def default_thread_reaction_get_converter(value):
    if (value is not None):
        value = create_emoji_from_exclusive_data(value)
    
    return value


@DEFAULT_THREAD_REACTION_CONVERSION.set_put_converter
def default_thread_reaction_put_converter(value):
    if value is not None:
        value = put_exclusive_emoji_data_into(value, {})
    
    return value


# ---- default_thread_slowmode ----

DEFAULT_THREAD_SLOWMODE_CONVERSION = AuditLogEntryChangeConversion(
    'default_thread_rate_limit_per_user',
    'default_thread_slowmode',
    FLAG_IS_MODIFICATION,
    validator = validate_default_thread_slowmode,
)

@DEFAULT_THREAD_SLOWMODE_CONVERSION.set_get_converter
def default_thread_slowmode_get_converter(value):
    if value is None:
        value = SLOWMODE_DEFAULT
    return value


# ---- flags ----

FLAGS_CONVERSION = AuditLogEntryChangeConversion(
    'flags',
    'flags',
    FLAG_IS_MODIFICATION,
    validator = validate_flags,
)


@FLAGS_CONVERSION.set_get_converter
def flags_get_converter(value):
    if value is None:
        value = ChannelFlag()
    else:
        value = ChannelFlag(value)
    
    return value


@FLAGS_CONVERSION.set_put_converter
def flags_put_converter(value):
    return int(value)


# ---- invitable ----

INVITABLE_CONVERSION = AuditLogEntryChangeConversion(
    'invitable',
    'invitable',
    FLAG_IS_MODIFICATION,
    validator = validate_invitable,
)


@INVITABLE_CONVERSION.set_get_converter
def invitable_get_converter(value):
    if value is None:
        value = True
    return value


# ---- name ----

NAME_CONVERSION = AuditLogEntryChangeConversion(
    'name',
    'name',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_name,
    put_converter = put_converter_name,
    validator = validate_name,
)


# ---- nsfw ----

NSFW_CONVERSION = AuditLogEntryChangeConversion(
    'nsfw',
    'nsfw',
    FLAG_IS_MODIFICATION,
    validator = validate_nsfw,
)


@NSFW_CONVERSION.set_get_converter
def nsfw_get_converter(value):
    if value is None:
        value = False
    return value


# ---- open ----

OPEN_CONVERSION = AuditLogEntryChangeConversion(
    'locked',
    'open',
    FLAG_IS_MODIFICATION,
    validator = validate_open,
)


@OPEN_CONVERSION.set_get_converter
def open_get_converter(value):
    if value is None:
        value = True
    else:
        value = not value
    return value


@OPEN_CONVERSION.set_put_converter
def open_put_converter(value):
    return not value


# ---- parent_id ----

PARENT_ID_CONVERSION = AuditLogEntryChangeConversion(
    'parent_id',
    'parent_id',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_id,
    put_converter = put_converter_id,
    validator = validate_parent_id,
)


# ---- permission_overwrites ----

PERMISSION_OVERWRITES_CONVERSION = AuditLogEntryChangeConversion(
    'permission_overwrites',
    'permission_overwrites',
    FLAG_IS_MODIFICATION,
    validator = validate_permission_overwrites,
)

@PERMISSION_OVERWRITES_CONVERSION.set_get_converter
def permission_overwrite_get_converter(value):
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


@PERMISSION_OVERWRITES_CONVERSION.set_put_converter
def permission_overwrite_put_converter(value):
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
    'position',
    'position',
    FLAG_IS_MODIFICATION,
    validator = validate_position,
)

@POSITION_CONVERSION.set_get_converter
def position_get_converter(value):
    if value is None:
        value = 0
    return value


# ---- region ----

REGION_CONVERSION = AuditLogEntryChangeConversion(
    'rtc_region',
    'region',
    FLAG_IS_MODIFICATION,
    validator = validate_region,
)


@REGION_CONVERSION.set_get_converter
def region_get_converter(value):
    return VoiceRegion.get(value)


@REGION_CONVERSION.set_put_converter
def region_put_converter(value):
    return value.value


# ---- slowmode ----

SLOWMODE_CONVERSION = AuditLogEntryChangeConversion(
    'rate_limit_per_user',
    'slowmode',
    FLAG_IS_MODIFICATION,
    validator = validate_slowmode,
)

@SLOWMODE_CONVERSION.set_get_converter
def slowmode_get_converter(value):
    if value is None:
        value = SLOWMODE_DEFAULT
    return value


# ---- topic ----

TOPIC_CONVERSION = AuditLogEntryChangeConversion(
    'topic',
    'topic',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_description,
    put_converter = put_converter_description,
    validator = validate_topic,
)


# ---- type ----

TYPE_CONVERSION = AuditLogEntryChangeConversion(
    'type',
    'type',
    FLAG_IS_MODIFICATION,
    validator = validate_type,
)


@TYPE_CONVERSION.set_get_converter
def type_get_converter(value):
    return ChannelType.get(value)


@TYPE_CONVERSION.set_put_converter
def type_put_converter(value):
    return value.value


# ---- video_quality_mode ----

VIDEO_QUALITY_MODE_CONVERSION = AuditLogEntryChangeConversion(
    'video_quality_mode',
    'video_quality_mode',
    FLAG_IS_MODIFICATION,
    validator = validate_video_quality_mode,
)


@VIDEO_QUALITY_MODE_CONVERSION.set_get_converter
def video_quality_mode_get_converter(value):
    return VideoQualityMode.get(value)


@VIDEO_QUALITY_MODE_CONVERSION.set_put_converter
def video_quality_mode_put_converter(value):
    return value.value


# ---- user_limit ----

USER_LIMIT_CONVERSION = AuditLogEntryChangeConversion(
    'user_limit',
    'user_limit',
    FLAG_IS_MODIFICATION,
    validator = validate_user_limit,
)

@USER_LIMIT_CONVERSION.set_get_converter
def user_limit_get_converter(value):
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
    DEFAULT_THREAD_REACTION_CONVERSION,
    DEFAULT_THREAD_SLOWMODE_CONVERSION,
    FLAGS_CONVERSION,
    INVITABLE_CONVERSION,
    NAME_CONVERSION,
    NSFW_CONVERSION,
    OPEN_CONVERSION,
    PARENT_ID_CONVERSION,
    PERMISSION_OVERWRITES_CONVERSION,
    POSITION_CONVERSION,
    REGION_CONVERSION,
    SLOWMODE_CONVERSION,
    TOPIC_CONVERSION,
    TYPE_CONVERSION,
    VIDEO_QUALITY_MODE_CONVERSION,
    USER_LIMIT_CONVERSION,
)
