__all__ = ()
from scarletio import to_json

from ...discord.utils import datetime_to_timestamp

from .constants import (
    JSON_KEY_BOT_INFO_AVATAR_BASE64, JSON_KEY_BOT_INFO_BANNER_URL, JSON_KEY_BOT_INFO_CERTIFIED_AT,
    JSON_KEY_BOT_INFO_DISCRIMINATOR_STRING, JSON_KEY_BOT_INFO_DONATE_BOT_GUILD_ID,
    JSON_KEY_BOT_INFO_FEATURED_GUILD_ID_ARRAY, JSON_KEY_BOT_INFO_GITHUB_URL, JSON_KEY_BOT_INFO_ID,
    JSON_KEY_BOT_INFO_INVITE_URL, JSON_KEY_BOT_INFO_IS_CERTIFIED, JSON_KEY_BOT_INFO_LONG_DESCRIPTION,
    JSON_KEY_BOT_INFO_NAME, JSON_KEY_BOT_INFO_OWNER_ID_ARRAY, JSON_KEY_BOT_INFO_PREFIX,
    JSON_KEY_BOT_INFO_SHORT_DESCRIPTION, JSON_KEY_BOT_INFO_SUPPORT_SERVER_INVITE_URL, JSON_KEY_BOT_INFO_TAG_ARRAY,
    JSON_KEY_BOT_INFO_UPVOTES, JSON_KEY_BOT_INFO_UPVOTES_MONTHLY, JSON_KEY_BOT_INFO_VANITY_URL,
    JSON_KEY_BOT_INFO_WEBSITE_URL
)


def snowflake_to_string(snowflake):
    """
    Converts snowflake value to string.
    
    Parameters
    ----------
    snowflake : `int`
        Snowflake to convert.
    
    Returns
    -------
    snowflake : `int`
    """
    return int(snowflake)


def discriminator_to_string(discriminator):
    """
    Converts a discriminator back to string.
    
    Parameters
    ----------
    discriminator : `int`
        The discriminator to convert.
    
    Returns
    -------
    discriminator : `str`
    """
    return str(discriminator)


def avatar_to_base16(avatar):
    """
    Converts a avatar to base16.
    
    Parameters
    ----------
    avatar : ``Icon``
        The icon to convert.
    
    Returns
    -------
    avatar : `str`
    """
    return avatar.as_base_16_hash


def nullable_string_tuple_to_string_array(nullable_string_tuple):
    """
    Converts a nullable string tuple to an array representing it.
    
    Parameters
    ----------
    nullable_string_tuple : `None`, `tuple` of `str`
        The value to convert.
    
    Returns
    -------
    array : `list` of `str`
    """
    if nullable_string_tuple is None:
        array = []
    else:
        array = list(nullable_string_tuple)
    
    return array


def nullable_snowflake_tuple_to_string_array(nullable_snowflake_tuple):
    """
    Converts a nullable snowflake tuple to an array representing it.
    
    Parameters
    ----------
    nullable_snowflake_tuple : `None`, `tuple` of `int`
        The value to convert.
    
    Returns
    -------
    array : `list` of `str`
    """
    if nullable_snowflake_tuple is None:
        array = []
    else:
        array = [str(snowflake) for snowflake in nullable_snowflake_tuple]
    
    return array


def owner_id_to_string_array(owner_id):
    """
    Converts a snowflake owner id to an array of strings.
    
    Parameters
    ----------
    owner_id : `int`
        Snowflake value.
    
    Returns
    -------
    owner_id_array : `list` of `str`
    """
    return [str(owner_id)]


def owner_ids_to_string_array(owner_ids):
    """
    Converts a snowflake owner id to an array of strings.
    
    Parameters
    ----------
    owner_ids : `iterable` of `int`
        Snowflakes.
    
    Returns
    -------
    owner_id_array : `list` of `str`
    """
    return [str(owner_id) for owner_id in owner_ids]


def nullable_datetime_to_timestamp(date_time):
    """
    Converts a nullable datetime to timestamp.
    
    Parameters
    ----------
    date_time : `None`, `datetime`
        The date time to convert.
    
    Returns
    -------
    timestamp : `None`, `str`
    """
    if date_time is None:
        timestamp = None
    else:
        timestamp = datetime_to_timestamp(date_time)
    
    return timestamp


BOT_INFO_ATTRIBUTE_TO_FIELD_NAME = {
    'id': JSON_KEY_BOT_INFO_ID,
    'name': JSON_KEY_BOT_INFO_NAME,
    'discriminator': JSON_KEY_BOT_INFO_DISCRIMINATOR_STRING,
    'avatar': JSON_KEY_BOT_INFO_AVATAR_BASE64,
    'banner_url': JSON_KEY_BOT_INFO_BANNER_URL,
    'prefix': JSON_KEY_BOT_INFO_PREFIX,
    'short_description': JSON_KEY_BOT_INFO_SHORT_DESCRIPTION,
    'long_description': JSON_KEY_BOT_INFO_LONG_DESCRIPTION,
    'tags': JSON_KEY_BOT_INFO_TAG_ARRAY,
    'website_url': JSON_KEY_BOT_INFO_WEBSITE_URL,
    'support_server_invite_url': JSON_KEY_BOT_INFO_SUPPORT_SERVER_INVITE_URL,
    'github_url': JSON_KEY_BOT_INFO_GITHUB_URL,
    'owner_id': JSON_KEY_BOT_INFO_OWNER_ID_ARRAY,
    'owner_ids': JSON_KEY_BOT_INFO_OWNER_ID_ARRAY,
    'featured_guild_ids': JSON_KEY_BOT_INFO_FEATURED_GUILD_ID_ARRAY,
    'invite_url': JSON_KEY_BOT_INFO_INVITE_URL,
    'certified_at': JSON_KEY_BOT_INFO_CERTIFIED_AT,
    'is_certified': JSON_KEY_BOT_INFO_IS_CERTIFIED,
    'vanity_url': JSON_KEY_BOT_INFO_VANITY_URL,
    'upvotes': JSON_KEY_BOT_INFO_UPVOTES,
    'upvotes_monthly': JSON_KEY_BOT_INFO_UPVOTES_MONTHLY,
    'donate_bot_guild_id': JSON_KEY_BOT_INFO_DONATE_BOT_GUILD_ID,
}

BOT_INFO_ATTRIBUTE_TO_FIELD_NAME_AND_CONVERTER = {
    'id': (JSON_KEY_BOT_INFO_ID, snowflake_to_string),
    'name': (JSON_KEY_BOT_INFO_NAME, None),
    'discriminator': (JSON_KEY_BOT_INFO_DISCRIMINATOR_STRING, discriminator_to_string),
    'avatar': (JSON_KEY_BOT_INFO_AVATAR_BASE64, avatar_to_base16),
    'banner_url': (JSON_KEY_BOT_INFO_BANNER_URL, None),
    'prefix': (JSON_KEY_BOT_INFO_PREFIX, None),
    'short_description': (JSON_KEY_BOT_INFO_SHORT_DESCRIPTION, None),
    'long_description': (JSON_KEY_BOT_INFO_LONG_DESCRIPTION, None),
    'tags': (JSON_KEY_BOT_INFO_TAG_ARRAY, None),
    'website_url': (JSON_KEY_BOT_INFO_WEBSITE_URL, None),
    'support_server_invite_url': (JSON_KEY_BOT_INFO_SUPPORT_SERVER_INVITE_URL, None),
    'github_url': (JSON_KEY_BOT_INFO_GITHUB_URL, None),
    'owner_id': (JSON_KEY_BOT_INFO_OWNER_ID_ARRAY, owner_id_to_string_array),
    'owner_ids': (JSON_KEY_BOT_INFO_OWNER_ID_ARRAY, owner_ids_to_string_array),
    'featured_guild_ids': (JSON_KEY_BOT_INFO_FEATURED_GUILD_ID_ARRAY, nullable_snowflake_tuple_to_string_array),
    'invite_url': (JSON_KEY_BOT_INFO_INVITE_URL, None),
    'certified_at': (JSON_KEY_BOT_INFO_CERTIFIED_AT, nullable_datetime_to_timestamp),
    'is_certified': (JSON_KEY_BOT_INFO_IS_CERTIFIED, None),
    'vanity_url': (JSON_KEY_BOT_INFO_VANITY_URL, None),
    'upvotes': (JSON_KEY_BOT_INFO_UPVOTES, None),
    'upvotes_monthly': (JSON_KEY_BOT_INFO_UPVOTES_MONTHLY, None),
    'donate_bot_guild_id': (JSON_KEY_BOT_INFO_DONATE_BOT_GUILD_ID, snowflake_to_string),
}


# used when generating exception messages.
FIELD_NAMES_STRING = ', '.join(
    repr(field_name) for field_name in BOT_INFO_ATTRIBUTE_TO_FIELD_NAME_AND_CONVERTER.keys()
)

def get_bots_query_sort_by_value(sort_by):
    """
    Gets bot query sort by field.
    
    Parameters
    ----------
    sort_by : `None`, `str`
        Sort by parameter.
    
    Returns
    -------
    query_sort_by_value : `str`
        The built query value.
    
    Raises
    ------
    LookupError
        Unknown field name given.
    """
    if (sort_by is None) or (not sort_by):
        query_sort_by_value = ''
    else:
        try:
            query_sort_by_value = BOT_INFO_ATTRIBUTE_TO_FIELD_NAME[sort_by]
        except KeyError:
            raise LookupError(
                f'There is no query field named: {sort_by!r}. The accepted fields are the '
                f'following: {FIELD_NAMES_STRING}.'
            ) from None
    
    return query_sort_by_value


def create_bots_query_search_value(query):
    """
    Creates a bots query search value.
    
    Parameters
    ----------
    query : `None`, `dict` of (`str`, `Any`)
        Search parameters.
    
    Returns
    -------
    query_search_value : `str`
        The built query value.
    
    Raises
    ------
    LookupError
        Unknown field name given.
    """
    if (query is None) or (not query):
        query_search_value = ''
    else:
        query_parts = []
        
        for field_name, field_value in query.items():
            try:
                top_gg_name, converter = BOT_INFO_ATTRIBUTE_TO_FIELD_NAME[field_name]
            except KeyError:
                raise LookupError(
                    f'There is no query field named: {field_name!r}. The accepted fields are the '
                    f'following: {FIELD_NAMES_STRING}.'
                ) from None
            
            if converter is None:
                top_gg_value = field_value
            else:
                top_gg_value = converter(field_value)
            
            top_gg_value = to_json(top_gg_value)
            query_parts.append((top_gg_name, top_gg_value))
        
        limit = len(query_parts)
        if limit:
            string_parts = []
            
            index = 0
            
            while True:
                top_gg_name, top_gg_value = query_parts[index]
                string_parts.append(top_gg_name)
                string_parts.append(': ')
                string_parts.append(top_gg_value)
                
                if index == limit:
                    break
                
                string_parts.append(' ')
                continue
            
            query_search_value = ''.join(string_parts)
            
        else:
            query_search_value = ''
    
    return query_search_value


BOTS_QUERY_FIELDS_VALUE = ', '.join((
    JSON_KEY_BOT_INFO_ID,
    JSON_KEY_BOT_INFO_NAME,
    JSON_KEY_BOT_INFO_DISCRIMINATOR_STRING,
    JSON_KEY_BOT_INFO_AVATAR_BASE64,
    JSON_KEY_BOT_INFO_BANNER_URL,
    JSON_KEY_BOT_INFO_PREFIX,
    JSON_KEY_BOT_INFO_SHORT_DESCRIPTION,
    JSON_KEY_BOT_INFO_LONG_DESCRIPTION,
    JSON_KEY_BOT_INFO_TAG_ARRAY,
    JSON_KEY_BOT_INFO_WEBSITE_URL,
    JSON_KEY_BOT_INFO_SUPPORT_SERVER_INVITE_URL,
    JSON_KEY_BOT_INFO_GITHUB_URL,
    JSON_KEY_BOT_INFO_OWNER_ID_ARRAY,
    JSON_KEY_BOT_INFO_FEATURED_GUILD_ID_ARRAY,
    JSON_KEY_BOT_INFO_INVITE_URL,
    JSON_KEY_BOT_INFO_CERTIFIED_AT,
    JSON_KEY_BOT_INFO_IS_CERTIFIED,
    JSON_KEY_BOT_INFO_VANITY_URL,
    JSON_KEY_BOT_INFO_UPVOTES,
    JSON_KEY_BOT_INFO_UPVOTES_MONTHLY,
    JSON_KEY_BOT_INFO_DONATE_BOT_GUILD_ID,
))
