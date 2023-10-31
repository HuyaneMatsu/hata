import vampytest

from ....channel import (
    ChannelFlag, ChannelType, ForumLayout, ForumTag, PermissionOverwrite, PermissionOverwriteTargetType, SortOrder,
    VideoQualityMode, VoiceRegion
)
from ....channel.channel.fields import validate_type
from ....channel.channel_metadata.constants import (
    AUTO_ARCHIVE_DEFAULT, BITRATE_DEFAULT, SLOWMODE_DEFAULT, USER_LIMIT_DEFAULT
)
from ....channel.channel_metadata.fields import (
    validate_applied_tag_ids, validate_archived, validate_auto_archive_after, validate_available_tags, validate_bitrate,
    validate_default_forum_layout, validate_default_sort_order, validate_default_thread_auto_archive_after,
    validate_default_thread_reaction, validate_default_thread_slowmode, validate_flags, validate_invitable,
    validate_name, validate_nsfw, validate_open, validate_parent_id, validate_permission_overwrites, validate_position,
    validate_region, validate_slowmode, validate_topic, validate_user_limit, validate_video_quality_mode
)
from ....core import BUILTIN_EMOJIS
from ....emoji import create_partial_emoji_data

from ...conversion_helpers.converters import (
    get_converter_description, get_converter_id, get_converter_ids, get_converter_name, put_converter_description,
    put_converter_id, put_converter_ids, put_converter_name
)

from ..channel import (
    APPLIED_TAG_IDS_CONVERSION, ARCHIVED_CONVERSION, AUTO_ARCHIVE_AFTER_CONVERSION, AVAILABLE_TAGS_CONVERSION,
    BITRATE_CONVERSION, CHANNEL_CONVERSIONS, DEFAULT_FORUM_LAYOUT_CONVERSION, DEFAULT_SORT_ORDER_CONVERSION,
    DEFAULT_THREAD_AUTO_ARCHIVE_AFTER_CONVERSION, DEFAULT_THREAD_REACTION_CONVERSION,
    DEFAULT_THREAD_SLOWMODE_CONVERSION, FLAGS_CONVERSION, INVITABLE_CONVERSION, NAME_CONVERSION, NSFW_CONVERSION,
    OPEN_CONVERSION, PARENT_ID_CONVERSION, PERMISSION_OVERWRITES_CONVERSION, POSITION_CONVERSION, REGION_CONVERSION,
    SLOWMODE_CONVERSION, TOPIC_CONVERSION, TYPE_CONVERSION, USER_LIMIT_CONVERSION, VIDEO_QUALITY_MODE_CONVERSION
)


def test__CHANNEL_CONVERSIONS():
    """
    Tests whether `CHANNEL_CONVERSIONS` contains conversion for every expected key.
    """
    vampytest.assert_eq(
        {*CHANNEL_CONVERSIONS.get_converters.keys()},
        {
            'applied_tags', 'archived', 'auto_archive_duration', 'available_tags', 'bitrate',
            'default_auto_archive_duration', 'default_forum_layout', 'default_sort_order', 'default_reaction_emoji',
            'default_thread_rate_limit_per_user', 'flags', 'invitable', 'name', 'nsfw', 'locked', 'parent_id',
            'permission_overwrites', 'rate_limit_per_user', 'rtc_region', 'rate_limit_per_user', 'topic', 'type',
            'video_quality_mode', 'user_limit', 'position', 'icon_emoji', 'theme_color', 'template'
        },
    )

# ---- applied_tag_ids ----

def test__APPLIED_TAG_IDS_CONVERSION__generic():
    """
    Tests whether ``APPLIED_TAG_IDS_CONVERSION`` works as intended.
    """
    vampytest.assert_is(APPLIED_TAG_IDS_CONVERSION.get_converter, get_converter_ids)
    vampytest.assert_is(APPLIED_TAG_IDS_CONVERSION.put_converter, put_converter_ids)
    vampytest.assert_is(APPLIED_TAG_IDS_CONVERSION.validator, validate_applied_tag_ids)


# ---- archived ----

def test__ARCHIVED_CONVERSION__generic():
    """
    Tests whether ``ARCHIVED_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(ARCHIVED_CONVERSION.get_converter, )
    # vampytest.assert_is(ARCHIVED_CONVERSION.put_converter, )
    vampytest.assert_is(ARCHIVED_CONVERSION.validator, validate_archived)


def _iter_options__archived__get_converter():
    yield True, True
    yield False, False
    yield None, False


@vampytest._(vampytest.call_from(_iter_options__archived__get_converter()).returning_last())
def test__ARCHIVED_CONVERSION__get_converter(input_value):
    """
    Tests whether `ARCHIVED_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return ARCHIVED_CONVERSION.get_converter(input_value)


def _iter_options__archived__put_converter():
    yield True, True
    yield False, False


@vampytest._(vampytest.call_from(_iter_options__archived__put_converter()).returning_last())
def test__ARCHIVED_CONVERSION__put_converter(input_value):
    """
    Tests whether `ARCHIVED_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Processed value.
    
    Returns
    -------
    output : `bool`
    """
    return ARCHIVED_CONVERSION.put_converter(input_value)


# ---- auto_archive_after ----

def test__AUTO_ARCHIVE_AFTER_CONVERSION__generic():
    """
    Tests whether ``AUTO_ARCHIVE_AFTER_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(AUTO_ARCHIVE_AFTER_CONVERSION.get_converter, )
    # vampytest.assert_is(AUTO_ARCHIVE_AFTER_CONVERSION.put_converter, )
    vampytest.assert_is(AUTO_ARCHIVE_AFTER_CONVERSION.validator, validate_auto_archive_after)


def _iter_options__auto_archive_after__get_converter():
    yield 1, 60
    yield 0, 0
    yield None, AUTO_ARCHIVE_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__auto_archive_after__get_converter()).returning_last())
def test__AUTO_ARCHIVE_AFTER_CONVERSION__get_converter(input_value):
    """
    Tests whether `AUTO_ARCHIVE_AFTER_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return AUTO_ARCHIVE_AFTER_CONVERSION.get_converter(input_value)


def _iter_options__auto_archive_after__put_converter():
    yield 60, 1
    yield 0, 0


@vampytest._(vampytest.call_from(_iter_options__auto_archive_after__put_converter()).returning_last())
def test__AUTO_ARCHIVE_AFTER_CONVERSION__put_converter(input_value):
    """
    Tests whether `AUTO_ARCHIVE_AFTER_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return AUTO_ARCHIVE_AFTER_CONVERSION.put_converter(input_value)


# --- available_tags ----

def test__AVAILABLE_TAGS_CONVERSION__generic():
    """
    Tests whether ``AVAILABLE_TAGS_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(AVAILABLE_TAGS_CONVERSION.get_converter, )
    # vampytest.assert_is(AVAILABLE_TAGS_CONVERSION.put_converter, )
    vampytest.assert_is(AVAILABLE_TAGS_CONVERSION.validator, validate_available_tags)
    

def _iter_options__available_tags__get_converter():
    tag_0 = ForumTag.precreate(202310260000, name = 'koishi')
    tag_1 = ForumTag.precreate(202310260001, name = 'satori')
    
    yield None, None
    yield [], None
    yield (
        [
            tag_0.to_data(defaults = True,include_internals = True),
            tag_1.to_data(defaults = True, include_internals = True),
        ],
        (tag_0, tag_1),
    )


@vampytest._(vampytest.call_from(_iter_options__available_tags__get_converter()).returning_last())
def test__AVAILABLE_TAGS_CONVERSION__get_converter(input_value):
    """
    Tests whether `AVAILABLE_TAGS_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `None | tuple<AutoModerationAction>`
    """
    return AVAILABLE_TAGS_CONVERSION.get_converter(input_value)


def _iter_options__available_tags__put_converter():
    tag_0 = ForumTag.precreate(202310260002, name = 'koishi')
    tag_1 = ForumTag.precreate(202310260003, name = 'satori')
    
    yield None, []
    yield (
        (tag_0, tag_1),
        [
            tag_0.to_data(defaults = True, include_internals = True),
            tag_1.to_data(defaults = True, include_internals = True),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__available_tags__put_converter()).returning_last())
def test__AVAILABLE_TAGS_CONVERSION__put_converter(input_value):
    """
    Tests whether `AVAILABLE_TAGS_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<AutoModerationAction>`
        Processed value.
    
    Returns
    -------
    output : `list<dict<str, object>>`
    """
    return AVAILABLE_TAGS_CONVERSION.put_converter(input_value)


# ---- bitrate ----

def test__BITRATE_CONVERSION__generic():
    """
    Tests whether ``BITRATE_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(BITRATE_CONVERSION.get_converter, )
    # vampytest.assert_is(BITRATE_CONVERSION.put_converter, )
    vampytest.assert_is(BITRATE_CONVERSION.validator, validate_bitrate)


def _iter_options__bitrate__get_converter():
    yield 60, 60
    yield 0, 0
    yield None, BITRATE_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__bitrate__get_converter()).returning_last())
def test__BITRATE_CONVERSION__get_converter(input_value):
    """
    Tests whether `BITRATE_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return BITRATE_CONVERSION.get_converter(input_value)


def _iter_options__bitrate__put_converter():
    yield 60, 60
    yield BITRATE_DEFAULT, BITRATE_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__bitrate__put_converter()).returning_last())
def test__BITRATE_CONVERSION__put_converter(input_value):
    """
    Tests whether `BITRATE_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return BITRATE_CONVERSION.put_converter(input_value)


# ---- default_thread_auto_archive_after ----

def test__DEFAULT_THREAD_AUTO_ARCHIVE_AFTER_CONVERSION__generic():
    """
    Tests whether ``DEFAULT_THREAD_AUTO_ARCHIVE_AFTER_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(DEFAULT_THREAD_AUTO_ARCHIVE_AFTER_CONVERSION.get_converter, )
    # vampytest.assert_is(DEFAULT_THREAD_AUTO_ARCHIVE_AFTER_CONVERSION.put_converter, )
    vampytest.assert_is(
        DEFAULT_THREAD_AUTO_ARCHIVE_AFTER_CONVERSION.validator, validate_default_thread_auto_archive_after
    )


def _iter_options__default_thread_auto_archive_after__get_converter():
    yield 1, 60
    yield 0, 0
    yield None, AUTO_ARCHIVE_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__default_thread_auto_archive_after__get_converter()).returning_last())
def test__DEFAULT_THREAD_AUTO_ARCHIVE_AFTER_CONVERSION__get_converter(input_value):
    """
    Tests whether `DEFAULT_THREAD_AUTO_ARCHIVE_AFTER_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return DEFAULT_THREAD_AUTO_ARCHIVE_AFTER_CONVERSION.get_converter(input_value)


def _iter_options__default_thread_auto_archive_after__put_converter():
    yield 60, 1
    yield 0, 0


@vampytest._(vampytest.call_from(_iter_options__default_thread_auto_archive_after__put_converter()).returning_last())
def test__DEFAULT_THREAD_AUTO_ARCHIVE_AFTER_CONVERSION__put_converter(input_value):
    """
    Tests whether `DEFAULT_THREAD_AUTO_ARCHIVE_AFTER_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return DEFAULT_THREAD_AUTO_ARCHIVE_AFTER_CONVERSION.put_converter(input_value)


# ---- default_forum_layout ----

def test__DEFAULT_FORUM_LAYOUT_CONVERSION__generic():
    """
    Tests whether ``DEFAULT_FORUM_LAYOUT_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(DEFAULT_FORUM_LAYOUT_CONVERSION.get_converter, )
    # vampytest.assert_is(DEFAULT_FORUM_LAYOUT_CONVERSION.put_converter, )
    vampytest.assert_is(DEFAULT_FORUM_LAYOUT_CONVERSION.validator, validate_default_forum_layout)


def _iter_options__default_forum_layout__get_converter():
    yield None, ForumLayout.none
    yield ForumLayout.list.value, ForumLayout.list


@vampytest._(vampytest.call_from(_iter_options__default_forum_layout__get_converter()).returning_last())
def test__DEFAULT_FORUM_LAYOUT_CONVERSION__get_converter(input_value):
    """
    Tests whether `DEFAULT_FORUM_LAYOUT_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``ForumLayout``
    """
    return DEFAULT_FORUM_LAYOUT_CONVERSION.get_converter(input_value)


def _iter_options__default_forum_layout__put_converter():
    yield ForumLayout.none, ForumLayout.none.value
    yield ForumLayout.list, ForumLayout.list.value


@vampytest._(vampytest.call_from(_iter_options__default_forum_layout__put_converter()).returning_last())
def test__DEFAULT_FORUM_LAYOUT_CONVERSION__put_converter(input_value):
    """
    Tests whether `DEFAULT_FORUM_LAYOUT_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``ForumLayout``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return DEFAULT_FORUM_LAYOUT_CONVERSION.put_converter(input_value)


# ---- default_sort_order ----

def test__DEFAULT_SORT_ORDER_CONVERSION__generic():
    """
    Tests whether ``DEFAULT_SORT_ORDER_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(DEFAULT_SORT_ORDER_CONVERSION.get_converter, )
    # vampytest.assert_is(DEFAULT_SORT_ORDER_CONVERSION.put_converter, )
    vampytest.assert_is(DEFAULT_SORT_ORDER_CONVERSION.validator, validate_default_sort_order)


def _iter_options__default_sort_order__get_converter():
    yield None, SortOrder.latest_activity
    yield SortOrder.creation_date.value, SortOrder.creation_date


@vampytest._(vampytest.call_from(_iter_options__default_sort_order__get_converter()).returning_last())
def test__DEFAULT_SORT_ORDER_CONVERSION__get_converter(input_value):
    """
    Tests whether `DEFAULT_SORT_ORDER_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``SortOrder``
    """
    return DEFAULT_SORT_ORDER_CONVERSION.get_converter(input_value)


def _iter_options__default_sort_order__put_converter():
    yield SortOrder.latest_activity, SortOrder.latest_activity.value
    yield SortOrder.creation_date, SortOrder.creation_date.value


@vampytest._(vampytest.call_from(_iter_options__default_sort_order__put_converter()).returning_last())
def test__DEFAULT_SORT_ORDER_CONVERSION__put_converter(input_value):
    """
    Tests whether `DEFAULT_SORT_ORDER_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``SortOrder``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return DEFAULT_SORT_ORDER_CONVERSION.put_converter(input_value)


# ---- default_thread_reaction ----

def test__DEFAULT_THREAD_REACTION_CONVERSION__generic():
    """
    Tests whether ``DEFAULT_THREAD_REACTION_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(DEFAULT_THREAD_REACTION_CONVERSION.get_converter, )
    # vampytest.assert_is(DEFAULT_THREAD_REACTION_CONVERSION.put_converter, )
    vampytest.assert_is(DEFAULT_THREAD_REACTION_CONVERSION.validator, validate_default_thread_reaction)


def _iter_options__default_thread_reaction__get_converter():
    emoji = BUILTIN_EMOJIS['x']
    yield None, None
    yield create_partial_emoji_data(emoji), emoji


@vampytest._(vampytest.call_from(_iter_options__default_thread_reaction__get_converter()).returning_last())
def test__DEFAULT_THREAD_REACTION_CONVERSION__get_converter(input_value):
    """
    Tests whether `DEFAULT_THREAD_REACTION_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `None | Emoji`
    """
    return DEFAULT_THREAD_REACTION_CONVERSION.get_converter(input_value)


def _iter_options__default_thread_reaction__put_converter():
    emoji = BUILTIN_EMOJIS['x']
    yield None, None
    yield emoji, create_partial_emoji_data(emoji)


@vampytest._(vampytest.call_from(_iter_options__default_thread_reaction__put_converter()).returning_last())
def test__DEFAULT_THREAD_REACTION_CONVERSION__put_converter(input_value):
    """
    Tests whether `DEFAULT_THREAD_REACTION_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `None | Emoji`
        Processed value.
    
    Returns
    -------
    output : `None | dict<str, object>`
    """
    return DEFAULT_THREAD_REACTION_CONVERSION.put_converter(input_value)


# ---- default_thread_slowmode ----

def test__DEFAULT_THREAD_SLOWMODE_CONVERSION__generic():
    """
    Tests whether ``DEFAULT_THREAD_SLOWMODE_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(DEFAULT_THREAD_SLOWMODE_CONVERSION.get_converter, )
    # vampytest.assert_is(DEFAULT_THREAD_SLOWMODE_CONVERSION.put_converter, )
    vampytest.assert_is(DEFAULT_THREAD_SLOWMODE_CONVERSION.validator, validate_default_thread_slowmode)


def _iter_options__default_thread_slowmode__get_converter():
    yield 60, 60
    yield 0, 0
    yield None, SLOWMODE_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__default_thread_slowmode__get_converter()).returning_last())
def test__DEFAULT_THREAD_SLOWMODE_CONVERSION__get_converter(input_value):
    """
    Tests whether `DEFAULT_THREAD_SLOWMODE_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return DEFAULT_THREAD_SLOWMODE_CONVERSION.get_converter(input_value)


def _iter_options__default_thread_slowmode__put_converter():
    yield 60, 60
    yield SLOWMODE_DEFAULT, SLOWMODE_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__default_thread_slowmode__put_converter()).returning_last())
def test__DEFAULT_THREAD_SLOWMODE_CONVERSION__put_converter(input_value):
    """
    Tests whether `DEFAULT_THREAD_SLOWMODE_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return DEFAULT_THREAD_SLOWMODE_CONVERSION.put_converter(input_value)


# ---- flags ----

def test__FLAGS_CONVERSION__generic():
    """
    Tests whether ``FLAGS_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(FLAGS_CONVERSION.get_converter, )
    # vampytest.assert_is(FLAGS_CONVERSION.put_converter, )
    vampytest.assert_is(FLAGS_CONVERSION.validator, validate_flags)


def _iter_options__flags__get_converter():
    yield 60, ChannelFlag(60)
    yield 0, ChannelFlag()
    yield None, ChannelFlag()


@vampytest._(vampytest.call_from(_iter_options__flags__get_converter()).returning_last())
def test__FLAGS_CONVERSION__get_converter(input_value):
    """
    Tests whether `FLAGS_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``ChannelFlag``
    """
    output = FLAGS_CONVERSION.get_converter(input_value)
    vampytest.assert_instance(output, ChannelFlag)
    return output


def _iter_options__flags__put_converter():
    yield ChannelFlag(60), 60
    yield ChannelFlag(), 0


@vampytest._(vampytest.call_from(_iter_options__flags__put_converter()).returning_last())
def test__FLAGS_CONVERSION__put_converter(input_value):
    """
    Tests whether `FLAGS_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``ChannelFlag``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    output = FLAGS_CONVERSION.put_converter(input_value)
    vampytest.assert_instance(output, int, accept_subtypes = False)
    return output


# ---- invitable ----

def test__INVITABLE_CONVERSION__generic():
    """
    Tests whether ``INVITABLE_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(INVITABLE_CONVERSION.get_converter, )
    # vampytest.assert_is(INVITABLE_CONVERSION.put_converter, )
    vampytest.assert_is(INVITABLE_CONVERSION.validator, validate_invitable)


def _iter_options__invitable__get_converter():
    yield True, True
    yield False, False
    yield None, True


@vampytest._(vampytest.call_from(_iter_options__invitable__get_converter()).returning_last())
def test__INVITABLE_CONVERSION__get_converter(input_value):
    """
    Tests whether `INVITABLE_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return INVITABLE_CONVERSION.get_converter(input_value)


def _iter_options__invitable__put_converter():
    yield True, True
    yield False, False


@vampytest._(vampytest.call_from(_iter_options__invitable__put_converter()).returning_last())
def test__INVITABLE_CONVERSION__put_converter(input_value):
    """
    Tests whether `INVITABLE_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Processed value.
    
    Returns
    -------
    output : `bool`
    """
    return INVITABLE_CONVERSION.put_converter(input_value)


# ---- name ----

def test__NAME_CONVERSION__generic():
    """
    Tests whether ``NAME_CONVERSION`` works as intended.
    """
    vampytest.assert_is(NAME_CONVERSION.get_converter, get_converter_name)
    vampytest.assert_is(NAME_CONVERSION.put_converter, put_converter_name)
    vampytest.assert_is(NAME_CONVERSION.validator, validate_name)


# ---- nsfw ----

def test__NSFW_CONVERSION__generic():
    """
    Tests whether ``NSFW_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(NSFW_CONVERSION.get_converter, )
    # vampytest.assert_is(NSFW_CONVERSION.put_converter, )
    vampytest.assert_is(NSFW_CONVERSION.validator, validate_nsfw)


def _iter_options__nsfw__get_converter():
    yield True, True
    yield False, False
    yield None, False


@vampytest._(vampytest.call_from(_iter_options__nsfw__get_converter()).returning_last())
def test__NSFW_CONVERSION__get_converter(input_value):
    """
    Tests whether `NSFW_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return NSFW_CONVERSION.get_converter(input_value)


def _iter_options__nsfw__put_converter():
    yield True, True
    yield False, False


@vampytest._(vampytest.call_from(_iter_options__nsfw__put_converter()).returning_last())
def test__NSFW_CONVERSION__put_converter(input_value):
    """
    Tests whether `NSFW_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Processed value.
    
    Returns
    -------
    output : `bool`
    """
    return NSFW_CONVERSION.put_converter(input_value)


# ---- open ----

def test__OPEN_CONVERSION__generic():
    """
    Tests whether ``OPEN_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(OPEN_CONVERSION.get_converter, )
    # vampytest.assert_is(OPEN_CONVERSION.put_converter, )
    vampytest.assert_is(OPEN_CONVERSION.validator, validate_open)


def _iter_options__open__get_converter():
    yield True, False
    yield False, True
    yield None, True


@vampytest._(vampytest.call_from(_iter_options__open__get_converter()).returning_last())
def test__OPEN_CONVERSION__get_converter(input_value):
    """
    Tests whether `OPEN_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return OPEN_CONVERSION.get_converter(input_value)


def _iter_options__open__put_converter():
    yield True, False
    yield False, True


@vampytest._(vampytest.call_from(_iter_options__open__put_converter()).returning_last())
def test__OPEN_CONVERSION__put_converter(input_value):
    """
    Tests whether `OPEN_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Processed value.
    
    Returns
    -------
    output : `bool`
    """
    return OPEN_CONVERSION.put_converter(input_value)


# ---- parent_id ----

def test__PARENT_ID_CONVERSION__generic():
    """
    Tests whether ``PARENT_ID_CONVERSION`` works as intended.
    """
    vampytest.assert_is(PARENT_ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(PARENT_ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(PARENT_ID_CONVERSION.validator, validate_parent_id)


# ---- permission_overwrites ----

def test__PERMISSION_OVERWRITES_CONVERSION__generic():
    """
    Tests whether ``PERMISSION_OVERWRITES_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(PERMISSION_OVERWRITES_CONVERSION.get_converter, )
    # vampytest.assert_is(PERMISSION_OVERWRITES_CONVERSION.put_converter, )
    vampytest.assert_is(PERMISSION_OVERWRITES_CONVERSION.validator, validate_permission_overwrites)
    

def _iter_options__permission_overwrites__get_converter():
    permission_overwrite_0 = PermissionOverwrite(202310260006, target_type = PermissionOverwriteTargetType.role)
    permission_overwrite_1 = PermissionOverwrite(202310260007, target_type = PermissionOverwriteTargetType.role)
    
    yield None, None
    yield [], None
    yield (
        [
            permission_overwrite_0.to_data(defaults = True,include_internals = True),
            permission_overwrite_1.to_data(defaults = True, include_internals = True),
        ],
        {
            permission_overwrite_0.target_id: permission_overwrite_0,
            permission_overwrite_1.target_id: permission_overwrite_1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options__permission_overwrites__get_converter()).returning_last())
def test__PERMISSION_OVERWRITES_CONVERSION__get_converter(input_value):
    """
    Tests whether `PERMISSION_OVERWRITES_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `None | tuple<AutoModerationAction>`
    """
    return PERMISSION_OVERWRITES_CONVERSION.get_converter(input_value)


def _iter_options__permission_overwrites__put_converter():
    permission_overwrite_0 = PermissionOverwrite(202310260008, target_type = PermissionOverwriteTargetType.role)
    permission_overwrite_1 = PermissionOverwrite(202310260009, target_type = PermissionOverwriteTargetType.role)
    
    yield None, []
    yield (
        {
            permission_overwrite_0.target_id: permission_overwrite_0,
            permission_overwrite_1.target_id: permission_overwrite_1,
        },
        [
            permission_overwrite_0.to_data(defaults = True, include_internals = True),
            permission_overwrite_1.to_data(defaults = True, include_internals = True),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__permission_overwrites__put_converter()).returning_last())
def test__PERMISSION_OVERWRITES_CONVERSION__put_converter(input_value):
    """
    Tests whether `PERMISSION_OVERWRITES_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<AutoModerationAction>`
        Processed value.
    
    Returns
    -------
    output : `list<dict<str, object>>`
    """
    return PERMISSION_OVERWRITES_CONVERSION.put_converter(input_value)


# ---- position ----

def test__POSITION_CONVERSION__generic():
    """
    Tests whether ``POSITION_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(POSITION_CONVERSION.get_converter, )
    # vampytest.assert_is(POSITION_CONVERSION.put_converter, )
    vampytest.assert_is(POSITION_CONVERSION.validator, validate_position)


def _iter_options__position__get_converter():
    yield 60, 60
    yield 0, 0
    yield None, 0


@vampytest._(vampytest.call_from(_iter_options__position__get_converter()).returning_last())
def test__POSITION_CONVERSION__get_converter(input_value):
    """
    Tests whether `POSITION_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return POSITION_CONVERSION.get_converter(input_value)


def _iter_options__position__put_converter():
    yield 60, 60
    yield 0, 0


@vampytest._(vampytest.call_from(_iter_options__position__put_converter()).returning_last())
def test__POSITION_CONVERSION__put_converter(input_value):
    """
    Tests whether `POSITION_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return POSITION_CONVERSION.put_converter(input_value)


# ---- region ----

def test__REGION_CONVERSION__generic():
    """
    Tests whether ``REGION_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(REGION_CONVERSION.get_converter, )
    # vampytest.assert_is(REGION_CONVERSION.put_converter, )
    vampytest.assert_is(REGION_CONVERSION.validator, validate_region)


def _iter_options__region__get_converter():
    yield None, VoiceRegion.unknown
    yield VoiceRegion.brazil.value, VoiceRegion.brazil


@vampytest._(vampytest.call_from(_iter_options__region__get_converter()).returning_last())
def test__REGION_CONVERSION__get_converter(input_value):
    """
    Tests whether `REGION_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``VoiceRegion``
    """
    return REGION_CONVERSION.get_converter(input_value)


def _iter_options__region__put_converter():
    yield VoiceRegion.unknown, VoiceRegion.unknown.value
    yield VoiceRegion.brazil, VoiceRegion.brazil.value


@vampytest._(vampytest.call_from(_iter_options__region__put_converter()).returning_last())
def test__REGION_CONVERSION__put_converter(input_value):
    """
    Tests whether `REGION_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``VoiceRegion``
        Processed value.
    
    Returns
    -------
    output : `str`
    """
    return REGION_CONVERSION.put_converter(input_value)


# ---- slowmode ----

def test__SLOWMODE_CONVERSION__generic():
    """
    Tests whether ``SLOWMODE_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(SLOWMODE_CONVERSION.get_converter, )
    # vampytest.assert_is(SLOWMODE_CONVERSION.put_converter, )
    vampytest.assert_is(SLOWMODE_CONVERSION.validator, validate_slowmode)


def _iter_options__slowmode__get_converter():
    yield 60, 60
    yield 0, 0
    yield None, SLOWMODE_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__slowmode__get_converter()).returning_last())
def test__SLOWMODE_CONVERSION__get_converter(input_value):
    """
    Tests whether `SLOWMODE_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return SLOWMODE_CONVERSION.get_converter(input_value)


def _iter_options__slowmode__put_converter():
    yield 60, 60
    yield SLOWMODE_DEFAULT, SLOWMODE_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__slowmode__put_converter()).returning_last())
def test__SLOWMODE_CONVERSION__put_converter(input_value):
    """
    Tests whether `SLOWMODE_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return SLOWMODE_CONVERSION.put_converter(input_value)


# ---- topic ----

def test__TOPIC_CONVERSION__generic():
    """
    Tests whether ``TOPIC_CONVERSION`` works as intended.
    """
    vampytest.assert_is(TOPIC_CONVERSION.get_converter, get_converter_description)
    vampytest.assert_is(TOPIC_CONVERSION.put_converter, put_converter_description)
    vampytest.assert_is(TOPIC_CONVERSION.validator, validate_topic)


# ---- type ----

def test__TYPE_CONVERSION__generic():
    """
    Tests whether ``TYPE_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(TYPE_CONVERSION.get_converter, )
    # vampytest.assert_is(TYPE_CONVERSION.put_converter, )
    vampytest.assert_is(TYPE_CONVERSION.validator, validate_type)


def _iter_options__type__get_converter():
    yield None, ChannelType.guild_text
    yield ChannelType.guild_voice.value, ChannelType.guild_voice


@vampytest._(vampytest.call_from(_iter_options__type__get_converter()).returning_last())
def test__TYPE_CONVERSION__get_converter(input_value):
    """
    Tests whether `TYPE_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``ChannelType``
    """
    return TYPE_CONVERSION.get_converter(input_value)


def _iter_options__type__put_converter():
    yield ChannelType.guild_text, ChannelType.guild_text.value
    yield ChannelType.guild_voice, ChannelType.guild_voice.value


@vampytest._(vampytest.call_from(_iter_options__type__put_converter()).returning_last())
def test__TYPE_CONVERSION__put_converter(input_value):
    """
    Tests whether `TYPE_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``ChannelType``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return TYPE_CONVERSION.put_converter(input_value)


# ---- video_quality_mode ----

def test__VIDEO_QUALITY_MODE_CONVERSION__generic():
    """
    Tests whether ``VIDEO_QUALITY_MODE_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(VIDEO_QUALITY_MODE_CONVERSION.get_converter, )
    # vampytest.assert_is(VIDEO_QUALITY_MODE_CONVERSION.put_converter, )
    vampytest.assert_is(VIDEO_QUALITY_MODE_CONVERSION.validator, validate_video_quality_mode)


def _iter_options__video_quality_mode__get_converter():
    yield None, VideoQualityMode.none
    yield VideoQualityMode.full.value, VideoQualityMode.full


@vampytest._(vampytest.call_from(_iter_options__video_quality_mode__get_converter()).returning_last())
def test__VIDEO_QUALITY_MODE_CONVERSION__get_converter(input_value):
    """
    Tests whether `VIDEO_QUALITY_MODE_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``VideoQualityMode``
    """
    return VIDEO_QUALITY_MODE_CONVERSION.get_converter(input_value)


def _iter_options__video_quality_mode__put_converter():
    yield VideoQualityMode.none, VideoQualityMode.none.value
    yield VideoQualityMode.full, VideoQualityMode.full.value


@vampytest._(vampytest.call_from(_iter_options__video_quality_mode__put_converter()).returning_last())
def test__VIDEO_QUALITY_MODE_CONVERSION__put_converter(input_value):
    """
    Tests whether `VIDEO_QUALITY_MODE_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``VideoQualityMode``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return VIDEO_QUALITY_MODE_CONVERSION.put_converter(input_value)


# ---- user_limit ----

def test__USER_LIMIT_CONVERSION__generic():
    """
    Tests whether ``USER_LIMIT_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(USER_LIMIT_CONVERSION.get_converter, )
    # vampytest.assert_is(USER_LIMIT_CONVERSION.put_converter, )
    vampytest.assert_is(USER_LIMIT_CONVERSION.validator, validate_user_limit)


def _iter_options__user_limit__get_converter():
    yield 60, 60
    yield 0, 0
    yield None, USER_LIMIT_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__user_limit__get_converter()).returning_last())
def test__USER_LIMIT_CONVERSION__get_converter(input_value):
    """
    Tests whether `USER_LIMIT_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return USER_LIMIT_CONVERSION.get_converter(input_value)


def _iter_options__user_limit__put_converter():
    yield 60, 60
    yield USER_LIMIT_DEFAULT, USER_LIMIT_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__user_limit__put_converter()).returning_last())
def test__USER_LIMIT_CONVERSION__put_converter(input_value):
    """
    Tests whether `USER_LIMIT_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return USER_LIMIT_CONVERSION.put_converter(input_value)
