__all__ = ()

from scarletio import include

from ...application import Application
from ...bases import id_sort_key
from ...component import Component
from ...embed import Embed
from ...emoji import ReactionMapping, merge_update_reaction_mapping
from ...field_parsers import (
    bool_parser_factory, entity_id_array_parser_factory, entity_id_parser_factory, flag_parser_factory,
    nullable_date_time_parser_factory, nullable_entity_array_parser_factory, nullable_entity_parser_factory,
    nullable_functional_array_parser_factory, nullable_object_array_parser_factory, nullable_string_parser_factory,
    preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, entity_id_optional_putter_factory, entity_id_putter_factory,
    flag_optional_putter_factory, nullable_date_time_optional_putter_factory,
    nullable_entity_array_optional_putter_factory, nullable_entity_optional_putter_factory,
    nullable_functional_array_optional_putter_factory, nullable_object_array_optional_putter_factory,
    nullable_string_optional_putter_factory, optional_entity_id_array_optional_putter_factory,
    preinstanced_putter_factory, url_optional_putter_factory
)
from ...field_validators import (
    bool_validator_factory, default_entity_validator_factory, entity_id_array_validator_factory,
    entity_id_validator_factory, flag_validator_factory, nullable_date_time_validator_factory,
    nullable_entity_array_validator_factory, nullable_entity_validator_factory, nullable_object_array_validator_factory,
    nullable_string_validator_factory, preinstanced_validator_factory
)
from ...poll import Poll
from ...role import Role
from ...sticker import Sticker, create_partial_sticker_data, create_partial_sticker_from_partial_data
from ...user import ClientUserBase, User, UserBase, ZEROUSER
from ...webhook import WebhookBase, WebhookRepr, WebhookType, create_partial_webhook_from_id

from ..attachment import Attachment
from ..message_activity import MessageActivity
from ..message_application import MessageApplication
from ..message_call import MessageCall
from ..message_interaction import MessageInteraction
from ..message_role_subscription import MessageRoleSubscription
from ..poll_change import PollChange
from ..poll_update import PollUpdate

from .constants import CONTENT_LENGTH_MAX, NONCE_LENGTH_MAX
from .flags import MessageFlag
from .preinstanced import MessageType


Channel = include('Channel')
Message = include('Message')
MessageSnapshot = include('MessageSnapshot')
Resolved = include('Resolved')


# activity

parse_activity = nullable_entity_parser_factory('activity', MessageActivity)
put_activity_into = nullable_entity_optional_putter_factory('activity', MessageActivity)
validate_activity = nullable_entity_validator_factory('activity', MessageActivity)

# application

parse_application = nullable_entity_parser_factory('application', MessageApplication)
put_application_into = nullable_entity_optional_putter_factory(
    'application', MessageApplication, force_include_internals = True
)
validate_application = nullable_entity_validator_factory('application', MessageApplication)

# application_id

parse_application_id = entity_id_parser_factory('application_id')


def put_application_id_into(application_id, data, defaults):
    """
    Puts the message's application's identifier into the given `data` json serializable object.
    
    Parameters
    ----------
    application_id : `int`
        Application identifier.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    if application_id:
        raw_application_id = str(application_id)
        data['application_id'] = raw_application_id
        
        if data.get('webhook_id', None) is None:
            data['webhook_id'] = raw_application_id
    
    elif defaults:
        data['application_id'] = None
    
    return data

validate_application_id = entity_id_validator_factory('application_id', Application)

# attachments

parse_attachments = nullable_entity_array_parser_factory('attachments', Attachment)
put_attachments_into = nullable_entity_array_optional_putter_factory('attachments', Attachment)
validate_attachments = nullable_entity_array_validator_factory('attachments', Attachment)

# author

def parse_author(data, guild_id = 0, channel_id = 0):
    """
    Parses the message's author from its data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Message data.
    guild_id : `int` = `0`, Optional
        The guild's id where the message was created at.
    channel_id : `int` = `0`, Optional
        The channel's id where the message was created at.
    
    Returns
    -------
    author : ``UserBase``
    """
    author_data = data.get('author', None)
    
    webhook_id = data.get('webhook_id', None)
    if (webhook_id is not None):
        application_id = data.get('application_id', None)
        if ((application_id is None) or (webhook_id != application_id)):
            if data.get('message_reference', None) is None:
                webhook_type = WebhookType.bot
            else:
                webhook_type = WebhookType.server
            
            webhook_id = int(webhook_id)
            if author_data is None:
                return create_partial_webhook_from_id(webhook_id, '', webhook_type = webhook_type)
            
            return WebhookRepr.from_data(author_data, webhook_id, webhook_type, channel_id)
    
    if author_data is None:
        return ZEROUSER
    
    return User.from_data(author_data, data.get('member', None), guild_id)


def put_author_into(author, data, defaults, *, guild_id = 0):
    """
    Puts the message author's data into the given `data` json serializable object.
    
    Parameters
    ----------
    author : ``UserBase``
        Message author.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    guild_id : `int` = `0`, Optional (Keyword only)
        The guild's id where the message was created at.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    data['author'] =  author.to_data(defaults = defaults, include_internals = True)
    
    if guild_id:
        try:
            guild_profile = author.guild_profiles[guild_id]
        except KeyError:
            pass
        else:
            data['member'] = guild_profile.to_data(defaults = defaults, include_internals = True)
    
    # If the message as created by a webhook, put its into the data too.
    if isinstance(author, WebhookBase):
        data['webhook_id'] = str(author.id)
    elif defaults:
        data['webhook_id'] = None
    
    return data


validate_author = default_entity_validator_factory('author', UserBase, default = ZEROUSER)

# call

parse_call = nullable_entity_parser_factory('call', MessageCall)
put_call_into = nullable_entity_optional_putter_factory('call', MessageCall)
validate_call = nullable_entity_validator_factory('call', MessageCall)

# channel_id

parse_channel_id = entity_id_parser_factory('channel_id')
put_channel_id_into = entity_id_putter_factory('channel_id')
validate_channel_id = entity_id_validator_factory('channel_id', NotImplemented, include = 'Channel')

# components

parse_components = nullable_object_array_parser_factory('components', Component)
put_components_into = nullable_object_array_optional_putter_factory('components')


def validate_components(components):
    """
    Validates the given components.
    
    Parameters
    ----------
    components : `None | iterable<Component>`
        The components to validate.
    
    Returns
    -------
    components_processed : `None | tuple<Component>`
    
    Raises
    ------
    TypeError
        - If `components` is invalid type.
    ValueError
        - If `components` contains an invalid value.
    """
    if components is None:
        return None
    
    if (getattr(components, '__iter__', None) is None):
        raise TypeError(
            f'`components` can be `None`, `iterable` of `{Component.__name__}`, got '
            f'{type(components).__name__}; {components!r}.'
        )
        
    components_processed = None
    
    for component in components:
        if not isinstance(component, Component):
            raise TypeError(
                f'`components` can contain `{Component.__name__}` elements, got '
                f'{type(component).__name__}; {component!r}; components = {components!r}.'
            )
        
        if not component.type.layout_flags.top_level:
            raise ValueError(
                f'Cannot add top level component of type {component.type.name}, '
                f'got {component!r}; components = {components!r}.'
            )
        
        if (components_processed is None):
            components_processed = []
        
        components_processed.append(component)
    
    if (components_processed is not None):
        components_processed = tuple(components_processed)
    
    return components_processed


# content

parse_content = nullable_string_parser_factory('content')
put_content_into = nullable_string_optional_putter_factory('content')
validate_content = nullable_string_validator_factory('content', 0, CONTENT_LENGTH_MAX)

# embed

parse_embeds = nullable_object_array_parser_factory('embeds', Embed)
put_embeds_into = nullable_object_array_optional_putter_factory('embeds', Embed)
validate_embeds = nullable_object_array_validator_factory('embeds', Embed)

# edited_at

parse_edited_at = nullable_date_time_parser_factory('edited_timestamp')
put_edited_at_into = nullable_date_time_optional_putter_factory('edited_timestamp')
validate_edited_at = nullable_date_time_validator_factory('edited_at')

# flags

parse_flags = flag_parser_factory('flags', MessageFlag)
put_flags_into = flag_optional_putter_factory('flags', MessageFlag())
validate_flags = flag_validator_factory('flags', MessageFlag)

# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id_into = entity_id_optional_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', NotImplemented, include = 'Guild')

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('message_id')

# interaction

# Old messages use `interaction` instead of `interaction_metadata`.
def parse_interaction(data):
    """
    Parses message interaction from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    interaction : `None | MessageInteraction`
    """
    try:
        interaction_data = data['interaction_metadata']
    except KeyError:
        interaction_data = data.get('interaction', None)
    
    if (interaction_data is not None):
        return MessageInteraction.from_data(interaction_data)


put_interaction_into = nullable_entity_optional_putter_factory(
    'interaction_metadata', MessageInteraction, force_include_internals = True
)
validate_interaction = nullable_entity_validator_factory('interaction', MessageInteraction)

# mentioned_channels_cross_guild

parse_mentioned_channels_cross_guild = nullable_functional_array_parser_factory(
    'mention_channels',
    NotImplemented,
    include = 'create_partial_channel_from_data',
    sort_key = id_sort_key,
)
put_mentioned_channels_cross_guild_into = nullable_functional_array_optional_putter_factory(
    'mention_channels',
    NotImplemented,
    include = 'create_partial_channel_data',
)
validate_mentioned_channels_cross_guild = nullable_entity_array_validator_factory(
    'mentioned_channels_cross_guild', NotImplemented, include = 'Channel', sort_key = id_sort_key,
)

# mentioned_everyone

parse_mentioned_everyone = bool_parser_factory('mention_everyone', False)
put_mentioned_everyone_into = bool_optional_putter_factory('mention_everyone', False)
validate_mentioned_everyone = bool_validator_factory('mention_everyone', False)

# mentioned_role_ids

parse_mentioned_role_ids = entity_id_array_parser_factory('mention_roles')
put_mentioned_role_ids_into = optional_entity_id_array_optional_putter_factory('mention_roles')
validate_mentioned_role_ids = entity_id_array_validator_factory('mentioned_role_ids', Role)

# mentioned_users

def parse_mentioned_users(data, guild_id = 0):
    """
    Parses out the mentioned users from the given message data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Message data.
    guild_id : `int` = `0`, Optional
        The guild's id where the message was created at.
    
    Returns
    -------
    mentioned_users : `None`, `tuple` of ``ClientUserBase``
    """
    user_mention_datas = data.get('mentions', None)
    if (user_mention_datas is None) or (not user_mention_datas):
        return
    
    return tuple(sorted(
        (
            User.from_data(user_mention_data, user_mention_data.get('member', None), guild_id)
            for user_mention_data in user_mention_datas
        ),
        key = id_sort_key,
    ))


def put_mentioned_users_into(mentioned_users, data, defaults, *, guild_id = 0):
    """
    Puts the message's mentioned users' data into the given `data` json serializable object.
    
    Parameters
    ----------
    mentioned_users : `None`, `tuple` of ``ClientUserBase``
        The mentioned users.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    guild_id : `int` = `0`, Optional (Keyword only)
        The guild's id where the message was created at.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    if defaults or (mentioned_users is not None):
        user_mention_datas = []
        
        if (mentioned_users is not None):
            for user in mentioned_users:
                user_data = user.to_data(defaults = defaults, include_internals = True)
                
                if guild_id:
                    try:
                        guild_profile = user.guild_profiles[guild_id]
                    except KeyError:
                        pass
                    else:
                        user_data['member'] = guild_profile.to_data(defaults = defaults, include_internals = True)
                
                user_mention_datas.append(user_data)
            
        data['mentions'] = user_mention_datas
    
    return data


validate_mentioned_users = nullable_entity_array_validator_factory(
    'mentioned_users', ClientUserBase, sort_key = id_sort_key,
)

# message_id

def parse_message_id(data):
    """
    Parses out a message id from the given data. Not like `parse_id` it first checks for `message_id`
    and then for `id` keys.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Message data.
    
    Returns
    -------
    message_id : `int`
    """
    try:
        message_id = data['message_id']
    except KeyError:
        pass
    else:
        if message_id is None:
            return 0
        
        return int(message_id)
    
    try:
        message_id = data['id']
    except KeyError:
        pass
    else:
        if message_id is None:
            return 0
        
        return int(message_id)
    
    return 0

put_message_id_into = entity_id_putter_factory('message_id')

# nonce

parse_nonce = nullable_string_parser_factory('nonce')
put_nonce_into = url_optional_putter_factory('nonce')
validate_nonce = nullable_string_validator_factory('nonce', 0, NONCE_LENGTH_MAX)

# pinned

parse_pinned = bool_parser_factory('pinned', False)
put_pinned_into = bool_optional_putter_factory('pinned', False)
validate_pinned = bool_validator_factory('pinned', False)


# poll

def parse_poll(data, old_poll = None):
    """
    Parses the message's polls.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    old_poll : `None | Poll` = `None`, Optional
        The old poll of the message.
    
    Returns
    -------
    poll : `Non | Poll`
    """
    poll_data = data.get('poll', None)
    if poll_data is None:
        poll = None
    else:
        if old_poll is None:
            poll = Poll.from_data(poll_data)
        else:
            poll = old_poll
            old_poll._update_attributes(poll_data)
            
    return poll


def parse_poll_and_change(data, old_poll):
    """
    Parses the poll and returns the difference.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    old_poll : `None | Poll` = `None`, Optional
        The old poll of the message.
    
    Returns
    -------
    poll : `Non | Poll`
    change : `None | PollChange`
    """
    poll_data = data.get('poll', None)
    if poll_data is None:
        if old_poll is None:
            poll = None
            change = None
        else:
            poll = None
            change = PollChange.from_fields(None, None, old_poll)
    else:
        if old_poll is None:
            poll = Poll.from_data(poll_data)
            change = PollChange.from_fields(poll, None, None)
        
        else:
            poll = old_poll
            old_attributes = poll._difference_update_attributes(poll_data)
            if old_attributes:
                change = PollChange.from_fields(None, PollUpdate.from_fields(poll, old_attributes), None)
            else:
                change = None
    
    return poll, change


put_poll_into = nullable_entity_optional_putter_factory('poll', Poll)
validate_poll = nullable_entity_validator_factory('poll', Poll)

# reactions

def parse_reactions(data, old_reactions = None):
    """
    Parses the message's reactions.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Message data.
    old_reactions : `None`, ``ReactionMapping`` = `None`, Optional
        The old reactions on the message.
    
    Returns
    -------
    reactions : `None`, ``ReactionMapping``
    """
    reactions_data = data.get('reactions', None)
    if (reactions_data is None) or (not reactions_data):
        new_reactions = None
    else:
        new_reactions = ReactionMapping.from_data(reactions_data)
    
    return merge_update_reaction_mapping(new_reactions, old_reactions)


def put_reactions_into(reactions, data, defaults):
    """
    Puts the message's reactions' data into the given `data` json serializable object.
    
    Parameters
    ----------
    reactions : `None`, ``ReactionMapping``
        The message's reactions.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    if (reactions is not None):
        data['reactions'] = reactions.to_data()
    elif defaults:
        data['reactions'] = []
    
    return data


def validate_reactions(reactions):
    """
    Validates message's reactions.
    
    Parameters
    ----------
    reactions : `None`, ``ReactionMapping`` (or compatible)
        Reactions value to validate.
    
    Returns
    -------
    reactions : `None`, ``ReactionMapping``
    
    Raises
    ------
    TypeError
        - `reactions` of invalid type given.
    """
    if reactions is None:
        return None
    
    if isinstance(reactions, ReactionMapping):
        return reactions
    
    return ReactionMapping(lines = reactions)

# referenced_message

def parse_referenced_message(data):
    """
    Parses out the referenced message from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Message data.
    
    Returns
    -------
    referenced_message : `None`, ``Message``
    """
    referenced_message_data = data.get('referenced_message', None)
    if (referenced_message_data is not None):
        return Message.from_data(referenced_message_data)
    
    referenced_message_data = data.get('message_reference', None)
    if (referenced_message_data is not None):
        return Message._create_from_partial_data(referenced_message_data)


def put_referenced_message_into(
    referenced_message, data, defaults, *, recursive = True, message_type = MessageType.default
):
    """
    Puts the referenced message's data into the  given `data` json serializable object.
    
    Parameters
    ----------
    referenced_message : `None`, ``Message``
        The referenced message.
    
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    recursive : `bool` = `True`, Optional (Keyword only)
        Whether the referenced message's data should be included as well.
    
    message_type : ``MessageType` = `MessageType.default`, Optional (Keyword only)
        The message's type. Used to check whether the referenced message should be recursively included.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    if (referenced_message is not None):
        data['message_reference'] = referenced_message.to_message_reference_data()
        
        if recursive and message_type in (MessageType.inline_reply, MessageType.thread_started):
            data['referenced_message'] = referenced_message.to_data(
                defaults = defaults, include_internals = True, recursive = False
            )
    
    return data


validate_referenced_message = nullable_entity_validator_factory(
    'referenced_message', NotImplemented, include = 'Message'
)

# resolved

def parse_resolved(data, guild_id = 0):
    """
    Parsers out a resolved value from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    guild_id : `int` = `0`, Optional
        The respective guild's identifier.
    
    Returns
    -------
    resolved : `None`, ``Resolved``
    """
    resolved_data = data.get('resolved', None)
    if (resolved_data is not None) and resolved_data:
        return Resolved.from_data(resolved_data, guild_id)


def put_resolved_into(resolved, data, defaults, *, guild_id = 0):
    """
    Serialises the given resolved value.
    
    Parameters
    ----------
    resolved  : `None`, ``Resolved``
        The instance to serialise.
        
    data : `dict<str, object>`
        Data to parse from.
    
    defaults : `bool`
        Whether default field values should be included as well.
    
    guild_id : `int` = `None`, Optional (Keyword only)
        The respective guild's identifier to use for handing user guild profiles.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    while True:
        if (resolved is None):
            if not defaults:
                break
            
            resolved_data = {}
        
        else:
            resolved_data = resolved.to_data(defaults = defaults, guild_id = guild_id)
        
        data['resolved'] = resolved_data
        break
    
    return data


validate_resolved = nullable_entity_validator_factory('resolved', NotImplemented, include = 'Resolved')


# role_subscription

parse_role_subscription = nullable_entity_parser_factory('role_subscription_data', MessageRoleSubscription)
put_role_subscription_into = nullable_entity_optional_putter_factory(
    'role_subscription_data', MessageRoleSubscription
)
validate_role_subscription = nullable_entity_validator_factory('role_subscription', MessageRoleSubscription)

# snapshots


def parse_snapshots(data, guild_id = 0):
    """
    Parsers out the snapshots from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    guild_id : `int` = `0`, Optional
        The respective guild's identifier.
    
    Returns
    -------
    snapshots : `None | tuple<MessageSnapshot>`
    """
    snapshot_datas = data.get('message_snapshots', None)
    if (snapshot_datas is not None) and snapshot_datas:
        return (*(MessageSnapshot.from_data(snapshot_data, guild_id) for snapshot_data in snapshot_datas),)


def put_snapshots_into(snapshots, data, defaults, *, guild_id = 0):
    """
    Serailises the given snapshots,
    
    Parameters
    ----------
    snapshots : `None | tuple<MessageSnapshot>`
        The instances to serialise.
        
    data : `dict<str, object>`
        Interaction metadata data.
    
    defaults : `bool`
        Whether default field values should be included as well.
    
    guild_id : `int` = `None`, Optional (Keyword only)
        The respective guild's identifier to use for handing user guild profiles.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (snapshots is not None):
        if snapshots is None:
            snapshot_datas = []
        else:
            snapshot_datas = [snapshot.to_data(defaults = defaults, guild_id = guild_id) for snapshot in snapshots]
        
        data['message_snapshots'] = snapshot_datas
    
    return data


validate_snapshots = nullable_object_array_validator_factory('snapshots', NotImplemented, include = 'MessageSnapshot')

# stickers

parse_stickers = nullable_functional_array_parser_factory(
    'sticker_items', create_partial_sticker_from_partial_data, do_sort = False
)
put_stickers_into = nullable_functional_array_optional_putter_factory('sticker_items', create_partial_sticker_data)
validate_stickers = nullable_entity_array_validator_factory(
    'stickers', Sticker, sort_key = id_sort_key,
)

# thread

def parse_thread(data, guild_id = 0):
    """
    Parses out the thread started by the message from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Message data.
    guild_id : `int` = `0`, Optional
        The guild's identifier where the message was sent to.
    """
    thread_data = data.get('thread', None)
    if (thread_data is not None):
        return Channel.from_data(thread_data, guild_id = guild_id)


put_thread_into = nullable_entity_optional_putter_factory(
    'thread', NotImplemented, force_include_internals = True
)
validate_thread = nullable_entity_validator_factory('thread', NotImplemented, include = 'Channel')

# tts

parse_tts = bool_parser_factory('tts', False)
put_tts_into = bool_optional_putter_factory('tts', False)
validate_tts = bool_validator_factory('tts', False)

# type

parse_type = preinstanced_parser_factory('type', MessageType, MessageType.default)
put_type_into = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('type', MessageType)
