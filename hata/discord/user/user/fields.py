__all__ = ()

from ...activity import Activity
from ...color import Color
from ...field_parsers import (
    bool_parser_factory, entity_id_parser_factory, flag_parser_factory, nullable_entity_parser_factory,
    nullable_string_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, entity_id_putter_factory, flag_putter_factory, force_bool_putter_factory,
    force_string_putter_factory, nullable_entity_optional_putter_factory, preinstanced_putter_factory,
    url_optional_putter_factory
)
from ...field_validators import (
    bool_validator_factory, entity_id_validator_factory, flag_validator_factory, force_string_validator_factory,
    nullable_entity_validator_factory, nullable_string_validator_factory, preinstanced_validator_factory
)
from ...localization import Locale
from ...localization.utils import LOCALE_DEFAULT

from ..avatar_decoration import AvatarDecoration
from ..name_plate import NamePlate

from .constants import (
    DISCRIMINATOR_VALUE_MAX, DISCRIMINATOR_VALUE_MIN, DISPLAY_NAME_LENGTH_MAX, NAME_LENGTH_MAX, NAME_LENGTH_MIN,
    WEBHOOK_NAME_LENGTH_MAX, WEBHOOK_NAME_LENGTH_MIN
)
from .flags import UserFlag
from .preinstanced import PremiumType, Status


# activities

def parse_activities(data):
    """
    Parses the activities out from the given presence data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        User presence data.
    
    Returns
    -------
    activities : ``None | list<Activity>``
    """
    activity_datas = data.get('activities', None)
    if (activity_datas is None) or (not activity_datas):
        return None
    
    return [Activity.from_data(activity_data) for activity_data in activity_datas]


def put_activities(activities, data, defaults):
    """
    Puts the given activities into the given data.
    
    Parameters
    ----------
    activities : ``None | list<Activity>``
        Activities.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if activities is None:
        activity_datas = []
    else:
        activity_datas = [
            activity.to_data(defaults = defaults, include_internals = True, user = True)
            for activity in activities
        ]
    
    data['activities'] = activity_datas
    return data


def validate_activities(activities):
    """
    Validates the given activities.
    
    Parameters
    ----------
    activities : `None`, `iterable` of ``Activity``
        The activities to validate.
    
    Returns
    -------
    activities : ``None | list<Activity>``
    
    Raises
    ------
    TypeError
        - If `activities` type is incorrect.
    """
    if activities is None:
        return None
    
    if getattr(activities, '__iter__', None) is None:
        raise TypeError(
            f'`activities` can be `None`, `iterable` of `{Activity.__name__}`, got '
            f'{activities.__class__.__name__}; {activities!r}.'
        )
    
    activities_validated = None
    
    for entity in activities:
        if not isinstance(entity, Activity):
            raise TypeError(
                f'`activities` elements can be `{Activity.__name__}`, got '
                f'{entity.__class__.__name__}; {entity!r}; activities = {activities!r}'
            )
        
        if activities_validated is None:
            activities_validated = []
        
        activities_validated.append(entity)
    
    return activities_validated

# avatar_decoration

parse_avatar_decoration = nullable_entity_parser_factory('avatar_decoration_data', AvatarDecoration)
put_avatar_decoration = nullable_entity_optional_putter_factory('avatar_decoration_data', AvatarDecoration)
validate_avatar_decoration = nullable_entity_validator_factory('avatar_decoration', AvatarDecoration)

# banner_color

def parse_banner_color(data):
    """
    Gets banner color from the given user data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        User data.
    
    Returns
    -------
    banner_color : `None`, ``Color``
    """
    banner_color = data.get('accent_color', None)
    if (banner_color is not None):
        banner_color = Color(banner_color)
    
    return banner_color


def put_banner_color(banner_color, data, defaults):
    """
    Puts the given banner color into the given data.
    
    Parameters
    ----------
    banner_color : `None`, ``Color``
        Banner color.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (banner_color is not None):
        if (banner_color is not None):
            banner_color = int(banner_color)
        data['accent_color'] = banner_color
    
    return data


def validate_banner_color(banner_color):
    """
    Validates the given `banner_color` value.
    
    Parameters
    ----------
    banner_color : `None`, ``Color``, `int`
        The banner color to validate.
    
    Returns
    -------
    banner_color : `None`, ``Color``
    
    Raises
    ------
    TypeError
        - If `banner_color` is not `None`, `Color`, `int`.
    ValueError
        - If `banner_color`'s value is out of the expected range.
    """
    if (banner_color is None):
        return None
    
    if isinstance(banner_color, Color):
        return banner_color
    
    if isinstance(banner_color, int):
        if banner_color < 0 or banner_color > 0xffffff:
            raise ValueError(
                f'`banner_color` can be between 0 and 0xffffff, got {banner_color!r}.'
            )
        
        return Color(banner_color)
    
    raise TypeError(
        f'`banner_color` can be `None`, `{Color.__name__}`, `int`, '
        f'got {type(banner_color).__name__}; {banner_color!r}.'
    )

# bot

parse_bot = bool_parser_factory('bot', False)
put_bot = force_bool_putter_factory('bot')
validate_bot = bool_validator_factory('bot', False)


# primary_guild_badge

parse_primary_guild_badge = nullable_entity_parser_factory(
    'primary_guild', NotImplemented, include = 'GuildBadge'
)
put_primary_guild_badge = nullable_entity_optional_putter_factory(
    'primary_guild', NotImplemented, include = 'GuildBadge'
)
validate_primary_guild_badge = nullable_entity_validator_factory(
    'primary_guild_badge', NotImplemented, include = 'GuildBadge'
)


# discriminator

parse_discriminator = flag_parser_factory('discriminator', int)

def put_discriminator(discriminator, data, defaults):
    """
    Puts the given discriminator value into the given data.
    
    Parameters
    ----------
    discriminator : `int`
        Discriminator value.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    data['discriminator'] = str(discriminator).rjust(4, '0')
    return data


def validate_discriminator(discriminator):
    """
    validates the given discriminator.
    
    Parameters
    ----------
    discriminator : `str`, `int`
        The discriminator of an user to convert.
    
    Returns
    -------
    discriminator : `int`
    
    Raises
    ------
    TypeError
        - If `discriminator` was not passed neither as `int`, `str`.
    ValueError
        - If `discriminator` was passed as `str` and it is not numerical or it's length is over `4`.
        - If the `discriminator`'s value is less than `0` or is over than `9999`.
    """
    if (type(discriminator) is int):
        pass
    
    elif isinstance(discriminator, int):
        discriminator = int(discriminator)
    
    elif isinstance(discriminator, str):
        if not discriminator.isdigit():
            raise ValueError(
                f'`discriminator` can contain only numerical characters (0 - 9), got {discriminator!r}.'
            )
        discriminator = int(discriminator)
    
    else:
        raise TypeError(
            f'`discriminator` can be `int`, `str`, got '
            f'{type(discriminator).__name__}; {discriminator!r}.'
        )
    
    if (discriminator < DISCRIMINATOR_VALUE_MIN) or (discriminator > DISCRIMINATOR_VALUE_MAX):
        raise ValueError(
            f'`discriminator` must be >= {DISCRIMINATOR_VALUE_MIN!r} and <= {DISCRIMINATOR_VALUE_MAX!r}, '
            f'got {discriminator!r}.'
        )
    
    return discriminator


# display_name

parse_display_name = nullable_string_parser_factory('global_name')
put_display_name = url_optional_putter_factory('global_name')
validate_display_name = nullable_string_validator_factory('global_name', 0, DISPLAY_NAME_LENGTH_MAX)

# email

parse_email = nullable_string_parser_factory('email')
put_email = url_optional_putter_factory('email')
validate_email = nullable_string_validator_factory('email', 0, 1024)

# email_verified

parse_email_verified = bool_parser_factory('verified', False)
put_email_verified = bool_optional_putter_factory('verified', False)
validate_email_verified = bool_validator_factory('email_verified', False)

# flags

def parse_flags(data):
    """
    Parses the user's flags out from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        User data.
    
    Returns
    -------
    flags : ``UserFlag``
    """
    try:
        flags = data['flags']
    except KeyError:
        flags = data.get('public_flags', 0)
    
    return UserFlag(flags)

put_flags = flag_putter_factory('public_flags')
validate_flags = flag_validator_factory('public_flags', UserFlag)

# flags | oauth2_flags

put_oauth2_flags_into = flag_putter_factory('flags')

# id

parse_id = entity_id_parser_factory('id')
put_id = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('user_id')

# locale

parse_locale = preinstanced_parser_factory('locale', Locale, LOCALE_DEFAULT)
put_locale = preinstanced_putter_factory('locale')
validate_locale = preinstanced_validator_factory('locale', Locale)

# mfa_enabled

parse_mfa_enabled = bool_parser_factory('mfa_enabled', False)
put_mfa_enabled = bool_optional_putter_factory('mfa_enabled', False)
validate_mfa_enabled = bool_validator_factory('mfa_enabled', False)


# name

def parse_name(data):
    """
    Parses out the given user's name from the data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        User data.
    
    Returns
    -------
    name : `str`
    """
    try:
        name = data['username']
    except KeyError:
        # Webhook?
        name = data.get('name', None)
    
    if (name is None):
        name = ''
        
    return name


put_name = force_string_putter_factory('username')
validate_name = force_string_validator_factory('name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)


# name | webhook_name

put_webhook_name = force_string_putter_factory('name')
validate_webhook_name = force_string_validator_factory('name', WEBHOOK_NAME_LENGTH_MIN, WEBHOOK_NAME_LENGTH_MAX)


# name_plate

def parse_name_plate(data):
    """
    Parses out a name plate from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    name_plate : ``None | NamePlate``
    """
    nested_data = data.get('collectibles', None)
    if nested_data is None:
        return
    
    name_plate_data = nested_data.get('nameplate', None)
    if name_plate_data is None:
        return
    
    return NamePlate.from_data(name_plate_data)


def put_name_plate(name_plate, data, defaults):
    """
    Serializes the name plate value into the given data.
    
    Parameters
    ----------
    name_plate : ``None | NamePlate``
        Name plate to serialize.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if (name_plate is not None) or defaults:
        try:
            nested_data = data['collectibles']
        except KeyError:
            nested_data = {}
            data['collectibles'] = nested_data
        
        if name_plate is None:
            name_plate_data = None
        else:
            name_plate_data = name_plate.to_data(defaults = defaults)
        
        nested_data['nameplate'] = name_plate_data
    
    return data


validate_name_plate = nullable_entity_validator_factory('name_plate', NamePlate)

# premium_type

parse_premium_type = preinstanced_parser_factory('premium_type', PremiumType, PremiumType.none)
put_premium_type = preinstanced_putter_factory('premium_type')
validate_premium_type = preinstanced_validator_factory('premium_type', PremiumType)

# status

parse_status = preinstanced_parser_factory('status', Status, Status.offline)
put_status = preinstanced_putter_factory('status')
validate_status = preinstanced_validator_factory('status', Status)

# statuses

def parse_statuses(data):
    """
    Parses out a user statuses from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        User presence data.
    
    Returns
    -------
    statuses : `None | dict<str, str>`
    """
    statuses = data.get('client_status', None)
    if (statuses is not None) and (not statuses):
        statuses = None
    
    return statuses


def put_statuses(statuses, data, defaults):
    """
    Puts the given statuses value into the given data.
    
    Parameters
    ----------
    statuses : `None | dict<str, str>`
        user statuses by platform.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if (statuses is None):
        statuses = {}
    
    data['client_status'] = statuses
    return data


def validate_statuses(statuses):
    """
    validates the given `statuses` value.
    
    Parameters
    ----------
    statuses : `None | dict<str, str>`
        Statuses to validate.
    
    Returns
    -------
    statuses : `None | dict<str, str>`
    
    Raises
    ------
    TypeError
        - If `statuses`'s type is incorrect.
    """
    if statuses is None:
        return None
    
    if not isinstance(statuses, dict):
        raise TypeError(
            f'`statuses` can be `None | dict<str, str>`, '
            f'got {type(statuses).__name__}; {statuses!r}.'
        )
    
    statuses_validated = None
    
    for key, value in statuses.items():
        if not isinstance(key, str):
            raise TypeError(
                f'`statuses` keys can be `str`, got {key.__class__.__name__}; {key!r}; statuses = {statuses!r}.'
            )
        if not isinstance(value, str):
            raise TypeError(
                f'`statuses` values can be `str`, got {value.__class__.__name__}; {value!r}; statuses = {statuses!r}.'
            )
        
        if statuses_validated is None:
            statuses_validated = {}
            
        statuses_validated[key] = value
    
    return statuses_validated
