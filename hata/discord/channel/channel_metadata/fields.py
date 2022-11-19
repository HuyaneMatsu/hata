__all__ = ()

from scarletio import include

from ...bases import maybe_snowflake
from ...emoji import Emoji, create_emoji_from_exclusive_data, put_exclusive_emoji_data_into
from ...field_parsers import (
    bool_parser_factory, entity_id_array_parser_factory, entity_id_parser_factory, flag_parser_factory,
    force_string_parser_factory, int_parser_factory, int_postprocess_parser_factory,
    nullable_entity_array_parser_factory, nullable_string_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, entity_id_array_optional_putter_factory, entity_id_optional_putter_factory,
    flag_optional_putter_factory, force_string_putter_factory, int_optional_postprocess_putter_factory,
    int_putter_factory, nullable_entity_array_optional_putter_factory, nullable_int_optional_putter_factory,
    nullable_string_putter_factory, preinstanced_optional_putter_factory
)
from ...field_validators import (
    bool_validator_factory, entity_id_array_validator_factory, entity_id_validator_factory, flag_validator_factory,
    force_string_validator_factory, int_conditional_validator_factory, int_options_validator_factory,
    nullable_date_time_validator_factory, nullable_entity_array_validator_factory, nullable_entity_validator_factory,
    nullable_string_validator_factory, preinstanced_validator_factory
)
from ...permission import PermissionOverwrite
from ...user import ClientUserBase, User, create_partial_user_from_id
from ...utils import datetime_to_timestamp, timestamp_to_datetime

from ..forum_tag import ForumTag

from .constants import (
    AUTO_ARCHIVE_DEFAULT, AUTO_ARCHIVE_OPTIONS, BITRATE_DEFAULT, BITRATE_MAX, BITRATE_MIN, NAME_LENGTH_MAX,
    NAME_LENGTH_MIN, SLOWMODE_DEFAULT, SLOWMODE_MAX, SLOWMODE_MIN, TOPIC_LENGTH_MAX, TOPIC_LENGTH_MIN,
    USER_LIMIT_DEFAULT, USER_LIMIT_MAX, USER_LIMIT_MIN
)
from .flags import ChannelFlag
from .preinstanced import SortOrder, VideoQualityMode, VoiceRegion


Channel = include('Channel')

# applied_tag_ids

parse_applied_tag_ids = entity_id_array_parser_factory('applied_tags')
put_applied_tag_ids_into = entity_id_array_optional_putter_factory('applied_tags')
validate_applied_tag_ids = entity_id_array_validator_factory('applied_tag_ids', ForumTag)

# archived

def parse_archived(data):
    """
    Parses out the `archived` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    archived : `bool`
    """
    try:
        sub_data = data['thread_metadata']
    except KeyError:
        archived = False
    else:
        archived = sub_data.get('archived', False)
    
    return archived


def put_archived_into(archived, data, defaults):
    """
    Puts the `archived`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    archived : `bool`
        Whether the channel is archived.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if archived or defaults:
        try:
            sub_data = data['thread_metadata']
        except KeyError:
            sub_data = {}
            data['thread_metadata'] = sub_data
        
        sub_data['archived'] = archived
    
    return data


validate_archived = bool_validator_factory('archived')

# archived_at

def parse_archived_at(data):
    """
    Parses out the `archived_at` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    archived_at : `int`
    """
    try:
        sub_data = data['thread_metadata']
    except KeyError:
        archived_at = None
    else:
        archived_at_timestamp = sub_data.get('archive_timestamp', None)
        if (archived_at_timestamp is None):
            archived_at = None
        else:
            archived_at = timestamp_to_datetime(archived_at_timestamp)
    
    return archived_at


def put_archived_at_into(archived_at, data, defaults):
    """
    Puts the `archived_at`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    archived_at : `None`, `datetime`
        When the channel was archived.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if defaults or (archived_at is not None):
        try:
            sub_data = data['thread_metadata']
        except KeyError:
            sub_data = {}
            data['thread_metadata'] = sub_data
        
        if archived_at is None:
            archived_at_timestamp = None
        else:
            archived_at_timestamp = datetime_to_timestamp(archived_at)
            
        sub_data['archive_timestamp'] = archived_at_timestamp
    
    return data


validate_archived_at = nullable_date_time_validator_factory('archived_at')

# auto_archive_after

def parse_auto_archive_after(data):
    """
    Parses out the `auto_archive_after` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    auto_archive_after : `int`
    """
    try:
        sub_data = data['thread_metadata']
    except KeyError:
        auto_archive_after = AUTO_ARCHIVE_DEFAULT
    else:
        auto_archive_after = sub_data.get('auto_archive_duration', None)
        if auto_archive_after is None:
            auto_archive_after = AUTO_ARCHIVE_DEFAULT
        else:
            auto_archive_after *= 60

    return auto_archive_after

def put_auto_archive_after_into(auto_archive_after, data, defaults, *, flatten_thread_metadata = False):
    """
    Puts the `auto_archive_after`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    auto_archive_after : `int`
        Duration in seconds to automatically archive the thread after recent activity.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    flatten_thread_metadata : `bool` = `False`, Optional (Keyword only)
        Whether the field should be flattened instead of nested.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if defaults or (auto_archive_after != AUTO_ARCHIVE_DEFAULT):
        if flatten_thread_metadata:
            data_to_use = data
        
        else:
            try:
                data_to_use = data['thread_metadata']
            except KeyError:
                data_to_use = {}
                data['thread_metadata'] = data_to_use
        
        data_to_use['auto_archive_duration'] = auto_archive_after // 60
    
    return data


validate_auto_archive_after = int_options_validator_factory('auto_archive_after', AUTO_ARCHIVE_OPTIONS)

# available_tags

parse_available_tags = nullable_entity_array_parser_factory('available_tags', ForumTag)
put_available_tags_into = nullable_entity_array_optional_putter_factory('available_tags')
validate_available_tags = nullable_entity_array_validator_factory('available_tags', ForumTag)

# bitrate

parse_bitrate = int_parser_factory('bitrate', BITRATE_DEFAULT)
put_bitrate_into = int_putter_factory('bitrate')
validate_bitrate = int_conditional_validator_factory(
    'bitrate',
    BITRATE_MIN,
    (lambda bitrate: bitrate >= BITRATE_MIN and bitrate <= BITRATE_MAX),
    f'>= {BITRATE_MIN} and <= {BITRATE_MAX},'
)

# created_at

def parse_created_at(data):
    """
    Parses out the `created_at` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    created_at : `int`
    """
    try:
        sub_data = data['thread_metadata']
    except KeyError:
        created_at = None
    else:
        created_at_timestamp = sub_data.get('create_timestamp', None)
        if (created_at_timestamp is None):
            created_at = None
        else:
            created_at = timestamp_to_datetime(created_at_timestamp)
    
    return created_at


def put_created_at_into(created_at, data, defaults):
    """
    Puts the `created_at`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    created_at : `None`, `datetime`
        When the channel was created.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if defaults or (created_at is not None):
        try:
            sub_data = data['thread_metadata']
        except KeyError:
            sub_data = {}
            data['thread_metadata'] = sub_data
        
        if created_at is None:
            created_at_timestamp = None
        else:
            created_at_timestamp = datetime_to_timestamp(created_at)
            
        sub_data['create_timestamp'] = created_at_timestamp
    
    return data


validate_created_at = nullable_date_time_validator_factory('created_at')

# default_sort_order

parse_default_sort_order = preinstanced_parser_factory('default_sort_order', SortOrder, SortOrder.latest_activity)
put_default_sort_order_into = preinstanced_optional_putter_factory('default_sort_order', SortOrder.latest_activity)
validate_default_sort_order = preinstanced_validator_factory('default_sort_order', SortOrder)


# default_thread_auto_archive_after

parse_default_thread_auto_archive_after = int_postprocess_parser_factory(
    'default_auto_archive_duration',
    AUTO_ARCHIVE_DEFAULT,
    (lambda default_thread_auto_archive_after: default_thread_auto_archive_after * 60),
)
put_default_thread_auto_archive_after_into = int_optional_postprocess_putter_factory(
    'default_auto_archive_duration',
    AUTO_ARCHIVE_DEFAULT,
    (lambda default_thread_auto_archive_after: default_thread_auto_archive_after // 60),
)
validate_default_thread_auto_archive_after = int_options_validator_factory(
    'default_thread_auto_archive_after', AUTO_ARCHIVE_OPTIONS
)

# default_thread_reaction

def parse_default_thread_reaction(data):
    """
    Parses out the `default_thread_reaction` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    default_thread_reaction : `None`, ``Emoji``
    """
    default_thread_reaction_data = data.get('default_reaction_emoji', None)
    if (default_thread_reaction_data is None):
        default_thread_reaction = None
    else:
        default_thread_reaction = create_emoji_from_exclusive_data(default_thread_reaction_data)
    
    return default_thread_reaction


def put_default_thread_reaction_into(default_thread_reaction, data, defaults):
    """
    Puts the `default_thread_reaction`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    default_thread_reaction : `None`, ``Emoji``
        The emoji to show in the add reaction button on a thread of the forum channel.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if defaults or (default_thread_reaction is not None):
        if default_thread_reaction is None:
            emoji_data = None
        else:
            emoji_data = put_exclusive_emoji_data_into(default_thread_reaction, {})
        
        data['default_reaction_emoji'] = emoji_data
    
    return data


validate_default_thread_reaction = nullable_entity_validator_factory('default_thread_reaction', Emoji)

# default_thread_slowmode

parse_default_thread_slowmode = int_parser_factory('default_thread_rate_limit_per_user', SLOWMODE_DEFAULT)
put_default_thread_slowmode_into = nullable_int_optional_putter_factory(
    'default_thread_rate_limit_per_user',
    SLOWMODE_DEFAULT,
)
validate_default_thread_slowmode = int_conditional_validator_factory(
    'default_thread_slowmode',
    SLOWMODE_MIN,
    (
        lambda default_thread_slowmode:
        default_thread_slowmode >= SLOWMODE_MIN and default_thread_slowmode <= SLOWMODE_MAX
    ),
    f'>= {SLOWMODE_MIN} and <= {SLOWMODE_MAX},'
)

# flags

parse_flags = flag_parser_factory('flags', ChannelFlag)
put_flags_into = flag_optional_putter_factory('flags', ChannelFlag())
validate_flags = flag_validator_factory('flags', ChannelFlag)

# invitable

def parse_invitable(data):
    """
    Parses out the `invitable` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    invitable : `bool`
    """
    try:
        sub_data = data['thread_metadata']
    except KeyError:
        invitable = True
    else:
        invitable = sub_data.get('invitable', True)
    
    return invitable


def put_invitable_into(invitable, data, defaults, *, flatten_thread_metadata = False):
    """
    Puts the `invitable`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    invitable : `bool`
        Whether non-moderators can invite other non-moderators to the threads.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    flatten_thread_metadata : `bool` = `False`, Optional (Keyword only)
        Whether the field should be flattened instead of nested.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if (not invitable) or defaults:
        if flatten_thread_metadata:
            data_to_use = data
        
        else:
            try:
                data_to_use = data['thread_metadata']
            except KeyError:
                data_to_use = {}
                data['thread_metadata'] = data_to_use
        
        data_to_use['invitable'] = invitable
    
    return data


validate_invitable = bool_validator_factory('invitable')

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)

# nsfw

parse_nsfw = bool_parser_factory('nsfw', False)
put_nsfw_into = bool_optional_putter_factory('nsfw', False)
validate_nsfw = bool_validator_factory('nsfw')

# open

def parse_open(data):
    """
    Parses out the `open` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
         Channel data.
    
    Returns
    -------
    open_ : `bool`
    """
    try:
        sub_data = data['thread_metadata']
    except KeyError:
        open_ = True
    else:
        open_ = not sub_data.get('locked', False)
    
    return open_


def put_open_into(open_, data, defaults, *, flatten_thread_metadata = False):
    """
    Puts the `open`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    open_ : `bool`
        Whether the channel is open.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    flatten_thread_metadata : `bool` = `False`, Optional (Keyword only)
        Whether the field should be flattened instead of nested.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if (not open_) or defaults:
        if flatten_thread_metadata:
            data_to_use = data
        
        else:
            try:
                data_to_use = data['thread_metadata']
            except KeyError:
                data_to_use = {}
                data['thread_metadata'] = data_to_use
        
        data_to_use['locked'] = not open_
    
    return data


validate_open = bool_validator_factory('open')

# owner_id

parse_owner_id = entity_id_parser_factory('owner_id')
put_owner_id_into = entity_id_optional_putter_factory('owner_id')
validate_owner_id = entity_id_validator_factory('owner_id', ClientUserBase)

# parent_id

parse_parent_id = entity_id_parser_factory('parent_id')
put_parent_id_into = entity_id_optional_putter_factory('parent_id')


def validate_parent_id(parent_id):
    """
    Validates the given `parent_id` field.
    
    Parameters
    ----------
    parent_id : `None`, `str`, `int`, ``Channel``
        The channel's parent's identifier.
    
    Returns
    -------
    parent_id : `int`
    
    Raises
    ------
    TypeError
        - If `parent_id` is not `None`, `str`.
    ValueError
        - If `parent_id` is out of the expected range.
    """
    if parent_id is None:
        processed_parent_id = 0
    
    elif isinstance(parent_id, Channel):
        processed_parent_id = parent_id.id
    
    else:
        processed_parent_id = maybe_snowflake(parent_id)
        if processed_parent_id is None:
            raise TypeError(
                f'`parent_id` can be `int`, `{Channel.__name__}`, `int`, got '
                f'{parent_id.__class__.__name__}; {parent_id!r}.'
            )
    
    return processed_parent_id

# permission_overwrites

def parse_permission_overwrites(data):
    """
    Parses the permission overwrites from the given data and returns them.
    
    Parameters
    ----------
    data : `list` of (`dict` of (`str`, `Any`) items) elements
        A list of permission overwrites' data.
    
    Returns
    -------
    permission_overwrites : `dict` of (`int`, ``PermissionOverwrite``) items
    """
    permission_overwrites = {}
    
    permission_overwrites_datas = data.get('permission_overwrites', None)
    if (permission_overwrites_datas is not None) and permission_overwrites_datas:
        for permission_overwrite_data in permission_overwrites_datas:
            permission_overwrite = PermissionOverwrite.from_data(permission_overwrite_data)
            permission_overwrites[permission_overwrite.target_id] = permission_overwrite
    
    return permission_overwrites


def put_permission_overwrites_into(permission_overwrites, data, defaults):
    """
    Puts the `permission_overwrites`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    permission_overwrites :`dict` of (`int`, ``PermissionOverwrite``) items
        The channel's permission overwrites.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    data['permission_overwrites'] = [
        permission_overwrite.to_data(include_internals = True)
        for permission_overwrite in permission_overwrites.values()
    ]
    
    return data


def validate_permission_overwrites(permission_overwrites):
    """
    Validates the given `permission_overwrites` field.
    
    Parameters
    ----------
    permission_overwrites : `None`, `iterable` of ``PermissionOverwrite``
        The permission_overwrites to validate.
    
    Returns
    -------
    permission_overwrites : `dict` of (`int`, ``PermissionOverwrite``) items
    """
    if permission_overwrites is None:
        return {}
    
    if (getattr(permission_overwrites, '__iter__', None) is None):
        raise TypeError(
            f'`permission_overwrites` can be `None`, `iterable` of `{PermissionOverwrite.__name__}`, got '
            f'{permission_overwrites.__class__.__name__}; {permission_overwrites!r}.'
        )
    
    permission_overwrites_processed = {}
    
    for permission_overwrite in permission_overwrites:
        if not isinstance(permission_overwrite, PermissionOverwrite):
            raise TypeError(
                f'`permission_overwrites` can contain `{PermissionOverwrite.__name__}` elements, got '
                f'{permission_overwrite.__class__.__name__}; {permission_overwrite!r}; '
                f'permission_overwrites = {permission_overwrites!r}.'
            )
        
        permission_overwrites_processed[permission_overwrite.target_id] = permission_overwrite
    
    return permission_overwrites_processed

# position

parse_position = int_parser_factory('position', 0)
put_position_into = int_putter_factory('position')
validate_position = int_conditional_validator_factory(
    'position',
    0,
    lambda position : position >= 0,
    '>= 0',
)

# region

parse_region = preinstanced_parser_factory('rtc_region', VoiceRegion, VoiceRegion.unknown)
put_region_into = preinstanced_optional_putter_factory('rtc_region', VoiceRegion.unknown)
validate_region = preinstanced_validator_factory('region', VoiceRegion)

# slowmode

parse_slowmode = int_parser_factory('rate_limit_per_user', SLOWMODE_DEFAULT)
put_slowmode_into = nullable_int_optional_putter_factory(
    'rate_limit_per_user',
    SLOWMODE_DEFAULT,
)
validate_slowmode = int_conditional_validator_factory(
    'slowmode',
    SLOWMODE_MIN,
    (
        lambda slowmode:
        slowmode >= SLOWMODE_MIN and slowmode <= SLOWMODE_MAX
    ),
    f'>= {SLOWMODE_MIN} and <= {SLOWMODE_MAX},'
)

# topic

parse_topic = nullable_string_parser_factory('topic')
put_topic_into = nullable_string_putter_factory('topic')
validate_topic = nullable_string_validator_factory('topic', TOPIC_LENGTH_MIN, TOPIC_LENGTH_MAX)

# user_limit

parse_user_limit = int_parser_factory('user_limit', USER_LIMIT_DEFAULT)
put_user_limit_into = int_putter_factory('user_limit')
validate_user_limit = int_conditional_validator_factory(
    'user_limit',
    USER_LIMIT_MIN,
    (lambda user_limit: user_limit >= USER_LIMIT_MIN and user_limit <= USER_LIMIT_MAX),
    f'>= {USER_LIMIT_MIN} and <= {USER_LIMIT_MAX},'
)

# users

def parse_users(data):
    """
    Parses out the `users` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    users : `list` of ``ClientUserBase``
    """
    users = []
    
    try:
        user_datas = data['recipients']
    except KeyError:
        pass
    else:
        for user_data in user_datas:
            user = User.from_data(user_data)
            users.append(user)
        
        users.sort()
    
    return users


def put_users_into(users, data, defaults):
    """
    Puts the `users`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    users : `list` of ``ClientUserBase``
        The users in the channel.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    data['recipients'] = [user.to_data() for user in users]
    
    return data


def validate_users(users):
    """
    Validates the given `users` field.
    
    Parameters
    ----------
    users : `iterable` of (``ClientUserBase``, `int`)
        The users in the channel.
    
    Returns
    -------
    users : `list` of ``ClientUserBase``
    
    Raises
    ------
    TypeError
        - If `users` is not `list` of (``ClientUserBase``, `int`).
    """
    if (getattr(users, '__iter__', None) is None):
        raise TypeError(
            f'`users` can be `None`, `iterable` of (`int`, `{ClientUserBase.__name__}`), '
            f'got {users.__class__.__name__}; {users!r}.'
        )
    
    users_processed = set()
    
    for user in users:
        if not isinstance(user, ClientUserBase):
            user_id = maybe_snowflake(user)
            if user_id is None:
                raise TypeError(
                    f'`users` can contain `int`, `{ClientUserBase.__name__}` elements, got '
                    f'{user.__class__.__name__}; {user!r}; users={users!r}.'
                )
            
            user = create_partial_user_from_id(user_id)
        
        users_processed.add(user)
    
    return sorted(users_processed)

# video_quality_mode


VIDEO_QUALITY_MODE_NONE = VideoQualityMode.none
VIDEO_QUALITY_MODE_AUTO = VideoQualityMode.auto

parse_video_quality_mode = preinstanced_parser_factory('video_quality_mode', VideoQualityMode, VideoQualityMode.auto)


def put_video_quality_mode_into(video_quality_mode, data, defaults):
    """
    Puts the `video_quality_mode`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    video_quality_mode : ``VideoQualityMode``
        The video quality of the voice channel.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if defaults or (
        (video_quality_mode is not VIDEO_QUALITY_MODE_NONE) and
        (video_quality_mode is not VIDEO_QUALITY_MODE_AUTO)
    ):
        if video_quality_mode is VIDEO_QUALITY_MODE_NONE:
            video_quality_mode = VIDEO_QUALITY_MODE_AUTO
        
        data['video_quality_mode'] = video_quality_mode.value
    
    return data


validate_video_quality_mode = preinstanced_validator_factory('video_quality_mode', VideoQualityMode)
