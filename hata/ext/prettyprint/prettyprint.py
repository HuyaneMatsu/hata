# -*- coding: utf-8 -*-
__all__ = ('pretty_print', 'pchunkify', 'pconnect', )

from datetime import datetime, timedelta
try:
    from dateutil.relativedelta import relativedelta
except ImportError:
    relativedelta=None

from ...backend.utils import multidict

from ...discord.utils import cchunkify, DISCORD_EPOCH_START, DATETIME_FORMAT_CODE
if (relativedelta is not None):
    from ...discord.utils import elapsed_time
from ...discord.permission import Permission
from ...discord.user import ZEROUSER
from ...discord.message import MessageType, Message
from ...discord.role import Role
from ...discord.integration import IntegrationAccount

#testerfile for events
#later embeds will be added in plan

PRETTY_PRINTERS = {}

class PrettyEmpty(object):
    __slots__ = ()
    def __init__(self, text=None, back=None):
        pass
    def __str__(self):
        return ''
    def __repr__(self):
        return f'<{self.__class__.__name__} back=0 text_length=0>'
    def __len__(self):
        return None
    @property
    def text_form(self):
        return ''

    def get_text(self):
        return ''
    def set_text(self, value):
        pass
    text = property(get_text, set_text)
    del get_text, set_text

    def get_back(self):
        return 0
    back = property(get_back, text.fset)
    del get_back
    
    def __call__(self, amount):
        return self
    
PrettyEmpty=PrettyEmpty()

class Pretty_line(object):
    __slots__ = ('back', 'text')
    def __init__(self,text, back=0):
        self.text = text
        self.back = back
    def __str__(self):
        return self.text
    def __repr__(self):
        return f'<{self.__class__.__name__} back=ignored text_length={len(self.text)}>'
    def __len__(self):
        return len(self.text)
    @property
    def text_form(self):
        return f'{" "*(self.back<<2)}{self.text}'
    def __call__(self, amount):
        self.back += amount
        return self


class PrettyIgnorePush(object):
    __slots__ = ('text',)
    def __init__(self, text, back=None):
        self.text = text
    def __str__(self):
        return self.text
    def __repr__(self):
        return f'<{self.__class__.__name__} back={self.back} text_length={len(self.text)}>'
    def __len__(self):
        return (self.back<<2)+len(self.text)
    @property
    def text_form(self):
        return self.text
    def __call__(self, amount):
        pass
    
    back = type(PrettyEmpty).back


class PrettyBlock(object):
    __slots__ = ('container', 'back',)
    def __init__(self, back=0):
        self.container = []
        self.back = back
    def append(self, content, back=0):
        if not content:
            value = PrettyEmpty
        elif back < 0:
            value = PrettyIgnorePush(content)
        elif type(content) == str:
            value = Pretty_line(content, self.back+back)
        else:
            value = content(self.back+back)
        self.container.append(value)
        
    def __repr__(self):
        return f'<{self.__class__.__name__} line_length={len(self.container)}>'
    def __call__(self, amount):
        self.back += amount
        for value in self.container:
            value(amount)
        return self
    @property
    def text_form(self):
        result = []
        for line in self.container:
            content = line.text_form
            if type(content) is list:
                result.extend(content)
            else:
                result.append(content)
        return result

def pretty_print(obj, **kwargs):
    return PRETTY_PRINTERS[obj.__class__.__name__](obj, **kwargs).text_form

def pchunkify(obj, **kwargs):
    return cchunkify(pretty_print(obj, **kwargs))

def pconnect(obj, **kwargs):
    return '\n'.join(pretty_print(obj, **kwargs))

def str_message(message, index=None, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    result.append(f'{start}Message {message.id}:')
    result.append(f'- length: {len(message)}')
    
    author = message.author
    if (author is not ZEROUSER):
        result.append(f'- author: {author:f}', 1)
    
    if message.type is not MessageType.default:
        result.append(f'--------------------\n{message.clean_content}\n--------------------', -1)
    elif message.content:
        content = message.clean_content
        content_ln = len(content)
        result.append(f'- content: (len={content_ln})', 1)
        if content_ln > 500:
            content = content[:500].replace('`', '\\`')
            result.append(f'--------------------\n{content}\n... +{content_ln-500} more\n--------------------', -1)
        else:
            content = content.replace('`', '\\`')
            result.append(f'--------------------\n{content}\n--------------------', -1)
    
    channel = message.channel
    result.append(f'- channel {channel.id} ({channel.__class__.__name__}, {channel.type})', 1)
    
    guild = channel.guild
    if (guild is not None):
        result.append(f'- guild {guild.id}', 1)
    
    result.append(f'- created at: {message:c}', 1)
    
    edited = message.edited
    if (edited is not None):
        result.append(f'- edited at: {edited:{DATETIME_FORMAT_CODE}}', 1)
    
    reactions = message.reactions
    if reactions:
        result.append(str_reaction_mapping(reactions), 1)
    
    application = message.application
    if (application is not None):
        result.append(str_message_application(application, 1))
    
    activity = message.activity
    if (activity is not None):
        line = ['- activity: ', activity.type.name]
        party_id=activity.party_id
        if party_id:
            line.append('(')
            line.append(party_id)
            line.append(')')
        
        result.append(''.join(line), 1)
    
    if message.pinned:
        result.append('- pinned', 1)
    if message.tts:
        result.append('- tts', 1)
    
    result.append(f'- type : {message.type.name} ({message.type.value})', 1)
    
    nonce = message.nonce
    if (nonce is not None):
        result.append(f'- nonce : {nonce!r}', 1)
        
    mention_count = len(message.mentions)
    if mention_count:
        result.append(f'Mentions: {mention_count}', 1)
        if mention_count < 9:
            index = 1
            if message.everyone_mention:
                result.append(f'- {index}.: everyone', 2)
                index += 1
            
            user_mentions = message.user_mentions
            if (user_mentions is not None):
                for user in user_mentions:
                    result.append(f'- {index}.: {user:f} ({user.id})', 2)
                    index += 1
            
            role_mentions = message.role_mentions
            if (role_mentions is not None):
                for role in role_mentions:
                    result.append(f'- {index}.: {role.name} ({role.id})', 2)
                    index += 1
            
            channel_mentions = message.channel_mentions
            if (channel_mentions is not None):
                for channel in channel_mentions:
                    result.append(f'- {index}.: {channel.name} ({channel.id})', 2)
                    index += 1
        
        else:
            if message.everyone_mention:
                result.append('- everyone', 2)
            
            user_mentions = message.user_mentions
            if (user_mentions is not None):
                result.append(f'- users ({len(user_mentions)})', 2)
            
            role_mentions = message.role_mentions
            if (role_mentions is not None):
                result.append(f'- roles ({len(role_mentions)})', 2)
            
            channel_mentions = message.channel_mentions
            if channel_mentions is not None:
                result.append(f'- channels ({len(channel_mentions)})', 2)
            
            cross_mentions = message.cross_mentions
            if (cross_mentions is not None):
                result.append(f'- cross channels ({len(cross_mentions)})', 2)
    
    attachments = message.attachments
    if (attachments is not None):
        result.append(f'Attachments: ({len(attachments)})', 1)
        for index, attachment in enumerate(attachments, 1):
            result.append(str_attachment(attachment, index), 1)
    
    embeds = message.embeds
    if (embeds is not None):
        result.append(f'Embeds: ({len(embeds)})', 1)
        for index, embed in enumerate(embeds, 1):
            result.append(str_embed_core(embed, index), 1)
    
    referenced_message = message.referenced_message
    if (referenced_message is not None):
        if isinstance(referenced_message, Message):
            referenced_message_message_id = referenced_message.id
            referenced_message_channel = referenced_message.channel
            referenced_message_channel_id = referenced_message_channel.id
            referenced_message_guild = referenced_message_channel.guild
            if referenced_message_guild is None:
                referenced_message_guild_id = 0
            else:
                referenced_message_guild_id = referenced_message_guild.id
        else:
            referenced_message_message_id = referenced_message.message_id
            referenced_message_channel_id = referenced_message.channel_id
            referenced_message_guild_id = referenced_message.guild_id
        
        result.append('Referenced message:', 1)
        result.append(f'- message id : {referenced_message_message_id}', 2)
        result.append(f'- channel id : {referenced_message_channel_id}', 2)
        if referenced_message_guild_id:
            result.append(f'- guild id : {referenced_message_guild_id}', 2)
    
    stickers = message.stickers
    if (stickers is not None):
        result.append(f'Stickers: ({len(stickers)})', 1)
        for index, sticker in enumerate(stickers, 1):
            result.append(str_sticker(sticker, index), 1)
    
    return result

def str_reaction_mapping(reactions, index=None, **kwargs): #ignore index, 1 message can have only 1
    result = PrettyBlock()
    reaction_count = len(reactions)
    result.append(f'Reactions: ({reaction_count})')
    reaction_ordering = list((len(v),k) for k, v in reactions.items())
    reaction_ordering.sort(reverse=True,key=lambda x:x[0])
    for times, emoji in reaction_ordering:
        if emoji.is_unicode_emoji():
            animated = ''
        else:
            if emoji.animated:
                animated = ' (animated)'
            else:
                animated = ''
        result.append(f'- {emoji} ({emoji.id}){animated} : {times} times', 1)
    #TODO: create a more accurate rendering for containers with small amount of emojis
    #    it will need to be able to handle unknown reactors too!
    return result

def str_reaction_mapping_line(users, **kwargs): #ignore index
    result = PrettyBlock()
    user_count = len(users)
    unknown = users.unknown
    if unknown:
        result.append(f'Reactors: ({user_count}, unknown: {unknown})')
    else:
        result.append(f'Reactors: ({user_count})')
    
    for index, user in enumerate(users):
        result.append(f'{index}.: {user.full_name} ({user.id})')
    
    return result

def str_message_application(application, index=None, **kwargs): #ignore index, 1/message
    result = PrettyBlock()
    result.append(f'message_application : ({application.id})')
    result.append(f'- name : {application.name}', 1)
    result.append(f'- id : {application.id}', 1)
    
    cover_url = application.cover_url
    if (cover_url is not None):
        result.append(f'- cover: {cover_url}', 1)
    
    icon_url = application.icon_url
    if (icon_url is not None):
        result.append(f'- icon : {icon_url}', 1)
    
    description = application.description
    if len(description)>32:
        result.append(f'- description: {description[:26]}...(+{len(description)-26})', 1)
    else:
        result.append(f'- description: {description}', 1)
    
    return result
    
def str_attachment(attachment, index=None, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    result.append(f'{start}Attachment:')
    result.append(f'- id : {attachment.id}', 1)
    result.append(f'- name : {attachment.name}', 1)
    result.append(f'- url : {attachment.url}', 1)
    result.append(f'- proxy_url : {attachment.proxy_url}', 1)
    result.append(f'- size : {attachment.size}', 1)
    if attachment.height:
        result.append(f'- height : {attachment.height}', 1)
    if attachment.width:
        result.append(f'- width : {attachment.width}', 1)
    return result

def str_sticker(sticker, index=None, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    result.append(f'{start}Sticker:')
    result.append(f'- id : {sticker.id}', 1)
    type_ = sticker.type
    result.append(f'- type: {type_.name} ({type_.value})')
    result.append(f'- name : {sticker.name}', 1)
    result.append(f'- pack_id : {sticker.pack_id}', 1)
    result.append(f'- description : {sticker.description!r}', 1)
    
    tags = sticker.tags
    if tags is not None:
        result.append(f'- tags: ({len(tags)})', 1)
        for index, tag in enumerate(tags):
            result.append(f'{index}.: {tag}', 2)
    
    asset = sticker.asset
    if asset:
        result.append(f'- asset : {asset.as_base16_hash}', 1)
    
    preview_asset = sticker.preview_asset
    if preview_asset:
        result.append(f'- preview_asset : {preview_asset.as_base16_hash}', 1)
    
    return result

def str_embed_core(embed, index=None, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    result.append(f'{start}Embed:')
    
    title = embed.title
    if title is not None:
        content = title
        content_ln = len(content)
        result.append(f'- title    : {content_ln}', 1)
        content = content.replace('`', '\\`')
        result.append(f'--------------------\n{content}\n--------------------', -1)
        
    type_ = embed.type
    if type_ is not None:
        result.append(f'- type     : {type_}', 1)
    
    description = embed.description
    if description:
        content = description
        content_ln = len(content)
        result.append(f'- description: (len={content_ln})', 1)
        if content_ln > 500:
            content = content[:500].replace('`', '\\`')
            result.append(f'--------------------\n{content}\n... +{content_ln-500} more\n--------------------', -1)
        else:
            content = content.replace('`', '\\`')
            result.append(f'--------------------\n{content}\n--------------------', -1)
    
    url = embed.url
    if url is not None:
        result.append(f'- url      : {url}', 1)
    
    timestamp = embed.timestamp
    if timestamp is not None:
        result.append(f'- timestamp: {timestamp:{DATETIME_FORMAT_CODE}}', 1)
    
    color = embed.color
    if color is not None:
        result.append(f'- color    : {color.as_html}', 1)
    
    footer = embed.footer
    if footer is not None:
        result.append(f'- footer    :', 1)
        
        content = footer.text
        content_ln = len(content)
        result.append(f'- text : {content_ln}', 2)
        if content_ln > 500:
            content=content[:500].replace('`', '\\`')
            result.append(f'--------------------\n{content}\n... +{content_ln-500} more\n--------------------', -1)
        else:
            content=content.replace('`', '\\`')
            result.append(f'--------------------\n{content}\n--------------------', -1)
        
        icon_url=footer.icon_url
        if icon_url is not None:
            result.append(f'- icon_url : {icon_url}', 2)
            
            proxy_icon_url=footer.proxy_icon_url
            if proxy_icon_url is not None:
                result.append(f'- proxy_icon_url : {proxy_icon_url}', 2)
                
    image = embed.image
    if image is not None:
        result.append('- image    :', 1)
        
        url = image.url
        if url is not None:
            result.append(f'- url : {url}', 2)
            
            proxy_url = image.proxy_url
            if proxy_url is not None:
                result.append(f'- proxy_url : {proxy_url}', 2)
        
        height = image.height
        if height:
            result.append(f'- height : {height}', 2)
        
        width = image.width
        if width:
            result.append(f'- width : {width}', 2)
    
    thumbnail = embed.thumbnail
    if thumbnail is not None:
        result.append('- thumbnail:', 1)
        
        url = thumbnail.url
        if url is not None:
            result.append(f'- url : {url}', 2)
            
            proxy_url = thumbnail.proxy_url
            if proxy_url is not None:
                result.append(f'- proxy_url : {proxy_url}', 2)
        
        height = thumbnail.height
        if height:
            result.append(f'- height : {height}', 2)
        
        width = thumbnail.width
        if width:
            result.append(f'- width : {width}', 2)
    
    video = embed.video
    if video is not None:
        result.append('- video    :', 1)
        
        url = video.url
        if url is not None:
            result.append(f'- url : {url}', 2)
        
        height = video.height
        if height:
            result.append(f'- height : {height}', 2)
        
        width = video.width
        if width:
            result.append(f'- width : {width}', 2)
            
    provider = embed.provider
    if provider is not None:
        result.append('- provider :', 1)
        
        url = provider.url
        if url is not None:
            result.append(f'- url : {url}', 2)
        
        name = provider.name
        if name is not None:
            result.append(f'- name : {name}', 2)
            
    author = embed.author
    if author is not None:
        result.append('- author   :', 1)
        
        name = author.name
        if name is not None:
            result.append(f'- name : {name}', 2)
        
        url = author.url
        if url is not None:
            result.append(f'- url : {url}', 2)
        
        icon_url = author.icon_url
        if icon_url is not None:
            result.append(f'- icon_url : {icon_url}', 2)
            
            proxy_icon_url = author.proxy_icon_url
            if proxy_icon_url is not None:
                result.append(f'- proxy_icon_url : {proxy_icon_url}', 2)
    
    fields = embed.fields
    if fields is not None:
        for index, field in enumerate(fields, 1):
            result.append(f'- field {index} :', 1)

            content = field.name
            content_ln = len(content)
            result.append(f'- name : {content_ln}', 2)
            content = content.replace('`', '\\`')
            result.append(f'--------------------\n{content}\n--------------------', -1)


            content = field.value
            content_ln = len(content)
            result.append(f'- value : {content_ln}', 2)
            if content_ln > 500:
                content = content[:500].replace('`', '\\`')
                result.append(f'--------------------\n{content}\n... +{content_ln-500} more\n--------------------', -1)
            else:
                content = content.replace('`', '\\`')
                result.append(f'--------------------\n{content}\n--------------------', -1)

            if field.inline:
                result.append(f'- inline', 2)
                
    return result


def str_role(role, index=None, write_parents=True, detailed=True, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    result.append(f'{start}Role: ({role.id})')
    result.append(f'- name : {role.name}', 1)
    
    guild = role.guild
    if (guild is None):
        result.append('- DELETED', 1)
        return result

    if write_parents:
        result.append(f'- guild : {guild.name} ({guild.id})', 1)
    
    result.append(f'- position : {role.position}', 1)
    result.append(f'- color : {role.color.as_html}', 1)
    result.append(f'- permissions : {role.permissions}', 1)
    
    if role.separated:
        result.append('- separated', 1)
    if role.mentionable:
        result.append('- mentionable', 1)
    
    if role.managed:
        result.append('- managed:', 1)
        result.append(f'- manager type: {role.manager_type}', 2)
        manager_id = role.manager_id
        if manager_id:
            result.append(f'- manager id: {manager_id}', 2)
    
    if detailed:
        result.append('Permissions:', 1)
        for key, value in role.permissions.items():
            result.append(f'- {key: <22}: {bool(value)}', 2)
    return result


def write_guild_channel_extras(channel, result, write_parents, write_overwrites, kwargs):
    guild = channel.guild
    if write_parents:
        result.append(f'- guild : {guild.name!r} ({guild.id})', 1)
    
    result.append(f'- position : {channel.position}', 1)
    
    category = channel.category
    if category is not guild:
        result.append(f'- category : {category.name!r} ({category.id})', 1)
    
    overwrites = channel.overwrites
    if overwrites:
        if write_overwrites:
            result.append(f'Permission overwrites: ({len(overwrites)})', 1)
            for index,overwrite in enumerate(overwrites, 1):
                result.append(str_PermissionOverwrite(overwrite, index=index, **kwargs), 2)
        else:
            result.append(f'- overwrites count: {len(overwrites)}', 1)

def str_channel_text(channel, index=None, write_parents=True, overwrites=False, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    result.append(f'{start}ChannelText ({"news" if channel.type else "text"} {channel.type}) : ({channel.id})')
    result.append(f'- name : {channel.name!r}', 1)
    result.append(f'- created at : {channel:c}', 1)
    if not channel.clients:
        result.append('- DELETED', 1)
        return result
    
    topic = channel.topic
    if (topic is not None):
        result.append(f'- topic : {topic!r}', 1)
    slowmode = channel.slowmode
    if slowmode:
        result.append(f'- slowmode : {slowmode}s', 1)
    if channel.nsfw:
        result.append('- NSFW', 1)

    write_guild_channel_extras(channel, result, write_parents, overwrites, kwargs)
    
    return result


def str_channel_private(channel, **kwargs):
    result = PrettyBlock()
    result.append(f'ChannelPrivate: ({channel.id})')
    result.append(f'- created at : {channel:c}', 1)
    if not channel.clients:
        result.append('- DELETED', 1)
        return result

    result.append(f'Users : ({len(channel.users)})', 1)
    for index, user in enumerate(channel.users, 1):
        if user.partial:
            result.append(f'{index}.: Partial user {user.id}', 2)
        else:
            result.append(f'{index}.: {user:f} {user.id}', 2)
            
    return result

def str_channel_voice(channel, index=None, write_parents=True, overwrites=False, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    result.append(f'{start}ChannelVoice: ({channel.id})')
    result.append(f'- name : {channel.name!r}', 1)
    result.append(f'- created at : {channel:c}', 1)
    if not channel.clients:
        result.append('- DELETED', 1)
        return result
    
    if channel.bitrate:
        result.append(f'- bitrate : {channel.bitrate}', 1)
    if channel.user_limit:
        result.append(f'- user limit : {channel.user_limit}', 1)
    
    write_guild_channel_extras(channel, result, write_parents, overwrites, kwargs)
    
    return result

def str_channel_group(channel, **kwargs):
    result = PrettyBlock()
    result.append(f'ChannelGroup: ({channel.id})')
    result.append(f'- name : {channel.name!r}', 1)
    result.append(f'- created at : {channel:c}', 1)
    if not channel.clients:
        result.append('- DELETED', 1)
        return result
    
    owner = channel.owner
    if channel.owner.partial:
        result.append(f'- owner : Partial user {owner.id}', 1)
    else:
        result.append(f'- owner: {owner.full_name} {owner.id}', 1)
    
    users = channel.users
    result.append(f'Users : ({len(users)})', 1)
    for index, user in enumerate(users, 1):
        if user.partial:
            result.append(f'{index}.: Partial user {user.id}', 2)
        else:
            result.append(f'{index}.: {user.full_name} {user.id}', 2)
    
    icon_url = channel.icon_url
    if (icon_url is not None):
        result.append(f'- icon : ({icon_url})', 1)
    
    return result

def str_channel_category(channel, index=None, write_parents=True, overwrites=False, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    
    result.append(f'{start}ChannelCategory: ({channel.id})')
    result.append(f'- name : {channel.name!r}', 1)
    result.append(f'- created at : {channel:c}', 1)
    if not channel.clients:
        result.append('- DELETED', 1)
        return result
    
    channels = channel.channel_list
    if channels:
        result.append(str_list(channels, write_parents=write_parents, overwrites=overwrites, **kwargs), 1)
    
    write_guild_channel_extras(channel, result, write_parents, overwrites, kwargs)
    
    return result

def str_channel_store(channel, index=None, write_parents=True, overwrites=False, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    result.append(f'{start}ChannelStore ({channel.type})')
    result.append(f'- name : {channel.name!r}', 1)
    result.append(f'- created at : {channel:c}', 1)
    if not channel.clients:
        result.append('- DELETED', 1)
        return result
    
    if channel.nsfw:
        result.append('- NSFW', 1)
    
    write_guild_channel_extras(channel, result, write_parents, overwrites, kwargs)
    
    return result

def str_channel_thread(channel, index=None, write_parents=True, overwrites=False, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    
    result.append(f'{start}ChannelStore ({channel.type})')
    result.append(f'- name : {channel.name!r}', 1)
    result.append(f'- created at : {channel:c}', 1)
    if not channel.clients:
        result.append('- DELETED', 1)
        return result
    
    result.append(f'- position : {channel.position}', 1)
    
    write_guild_channel_extras(channel, result, write_parents, overwrites, kwargs)
    
    return result

def str_channel_guild_undefined(channel, index=None, write_parents=True, overwrites=False, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    
    result.append(f'{start}ChannelStore ({channel.type})')
    result.append(f'- name : {channel.name!r}', 1)
    result.append(f'- created at : {channel:c}', 1)
    if not channel.clients:
        result.append('- DELETED', 1)
        return result
    
    result.append(f'- position : {channel.position}', 1)
    for key, value in channel.__dict__:
        result.append(f'{key} : {value!r}', 1)
    
    write_guild_channel_extras(channel, result, write_parents, overwrites, kwargs)
    
    return result

def str_guild(guild, index=None, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    result.append(f'{start}Guild ({guild.id}):')
    
    result.append(f'- name : {guild.name}', 1)
    if guild.icon:
        result.append(f'- icon : {guild.icon_url}', 1)
    if guild.banner:
        result.append(f'banner : {guild.banner_url}', 1)
    if guild.invite_splash:
        result.append(f'- invite_splash : {guild.invite_splash_url}', 1)
    if guild.discovery_splash:
        result.append(f'- discovery splash : {guild.discovery_splash_url}', 1)
    if not guild.clients or not guild.available:
        result.append('- PARTIAL/UNAVAILABLE/DELETED', 1)
        return result
    result.append(f'- verification level : {guild.verification_level.name}', 1)
    result.append(f'- user count: {guild.user_count}', 1)
    result.append(f'- afk timeout : {guild.afk_timeout}s', 1)
    result.append(f'- message notification : {guild.message_notification.name}', 1)
    result.append(f'- mfa level : {guild.mfa.name}', 1)
    result.append(f'- content filter : {guild.content_filter.name}', 1)
    result.append(f'- available : {guild.available}', 1)
    result.append(f'- max users : {guild.max_users}', 1)
    result.append(f'- max presences : {guild.max_presences}', 1)
    result.append(f'- max video channel users : {guild.max_video_channel_users}', 1)
    result.append(f'- preferred locale : {guild.preferred_locale}', 1)
    
    description = guild.description
    if (description is not None):
        result.append(f'description : {description}', 1)
    
    vanity_code = guild.vanity_code
    if (vanity_code is not None):
        result.append(f'vanity_code : {vanity_code}', 1)
    
    features = guild.features
    if features:
        result.append(f'- features : {", ".join(feature.value for feature in features)}', 1)
    
    owner = guild.owner
    if owner.partial:
        result.append(f'- owner : Partial user {owner.id}', 1)
    else:
        result.append(f'- owner : {owner.full_name} {owner.id}', 1)
    
    system_channel = guild.system_channel
    if (system_channel is not None):
        result.append(f'- system channel: {system_channel.name} {system_channel.id}', 1)
    
    afk_channel = guild.afk_channel
    if (afk_channel is not None):
        result.append(f'- afk channel: {afk_channel.name} {afk_channel.id}', 1)
    
    widget_channel = guild.widget_channel
    if (widget_channel is not None):
        result.append(f'- widget channel: {widget_channel.name} {widget_channel.id}', 1)
    
    rules_channel = guild.rules_channel
    if (rules_channel is not None):
        result.append(f'- rules channel : {rules_channel.name} {rules_channel.id}', 1)
    
    public_updates_channel = guild.public_updates_channel
    if (public_updates_channel is not None):
        result.append(f'-public updates channel : {public_updates_channel.name} {public_updates_channel.id}', 1)
    
    if guild.booster_count:
        result.append(f'- boosters : {guild.booster_count}', 1)
        result.append(f'- premium tier : {guild.premium_tier}', 1)
    result.append(str_list(guild.channel_list, write_parents=False), 1)
    result.append(str_list(guild.role_list, write_parents=False), 1)
    if guild.voice_states:
        voice_states = multidict()
        for voice_state in guild.voice_states.values():
            voice_states[voice_state.channel]=voice_state.user
        result.append(f'Voice_states : {len(guild.voice_states)}', 1)
        for channel, users in dict.items(voice_states):
            result.append(f'Channel {channel.name} {channel.id}', 2)
            for index, user in enumerate(users, 1):
                result.append(f'{index}.: {user:f} {user.id}', 3)
    emojis = guild.emojis
    if emojis:
        result.append(f'Emojis : {len(emojis)}', 1)
        for index, emoji in enumerate(emojis.values(), 1):
            if emoji.animated:
                animated = ' (animated)'
            else:
                animated = ''
            result.append(f'{index}.: {emoji.name} {emoji.id}{animated}', 2)
    return result

def str_PermissionOverwrite(overwrite, index=None, detailed=True, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
        
    result.append(f'{start}Permission overwrite:')
    target = overwrite.target
    if type(target) is Role:
        entity_type_name = 'role'
        entity_name = target.name
    else:
        entity_type_name = 'user'
        entity_name = target.full_name
    
    result.append(f'- target: {entity_type_name} {entity_name!r} ({target.id})', 1)
    
    allow = overwrite.allow
    deny = overwrite.deny
    if detailed:
        result.append('Permission changes:', 1)
        for name, push in Permission.__keys__.items():
            if (allow>>push)&1:
                v='allow'
            elif (deny>>push)&1:
                v='deny'
            else:
                continue
            result.append(f'- {name: <22}: {v}', 2)
            
    else:
        result.append(f'- allow : {allow}', 1)
        result.append(f'- deny  : {deny}', 1)
        
    return result

def str_permission(permission, **kwargs):
    result = PrettyBlock()
    result.append('Permission:')
    for name, value in permission.items():
        value = bool(value)
        result.append(f'- {name: <22}: {value}', 1)
    return result

def str_invite(invite, index=None,write_parents=True, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    result.append(f'{start}Invite:')
    result.append(f'- inviter : {invite.inviter:f}', 1)
    result.append(f'- code : {invite.code}', 1)
    
    channel = invite.channel
    if channel is not None:
        result.append(f'- channel : {channel.name} ({channel.id})', 1)
    
    if write_parents:
        guild=invite.guild
        if guild is not None:
            result.append(f'- guild : {guild.name} ({guild.id})', 1)
    
    uses = invite.uses
    if uses is not None:
        if invite.max_uses:
            max_uses=str(invite.max_uses)
        else:
            max_uses='unlimited'
        result.append(f'- uses : {uses}/{max_uses}', 1)
    
    created_at = invite.created_at
    if (created_at > DISCORD_EPOCH_START):
        result.append(f'- created at : {created_at:{DATETIME_FORMAT_CODE}}', 1)
        max_age = invite.max_age
        if (max_age is not None):
            if (relativedelta is None):
                result.append(f'- max_age : {max_age}')
            else:
                result.append('- time left : '
                  f'{elapsed_time(relativedelta(created_at+timedelta(0, max_age), datetime.utcnow()))}', 1)
    
    target_user = invite.target_user
    if target_user is not ZEROUSER:
        result.append(f'- inviter : {target_user:f}', 1)
    
    target_type = invite.target_type
    if target_type.value:
        result.append(f'- target_type : {target_type.name}', 1)
    
    online_count = invite.online_count
    if online_count:
        result.append(f'- online count : {online_count}', 1)
        
    user_count = invite.user_count
    if user_count:
        result.append(f'- user count : {user_count}', 1)
    
    result.append(f'- {"temporary" if invite.temporary else "permanent"}', 1)

    return result

def str_list(list_, index=None, mixed=True, name=None, **kwargs):
    result = PrettyBlock()
    
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    
    if not list_:
        if name is not None:
            result.append(f'{start}{name}s: (0)')
        else:
            result.append(f'{start}Empty {list_.__class__}')
        return result
    type_name = list_[0].__class__.__name__
    if name is None:
        name = type_name
    result.append(f'{start}{name}s: ({len(list_)})')
    if mixed:
        for index, value in enumerate(list_, 0):
            result.append(PRETTY_PRINTERS[value.__class__.__name__](value, index=index, **kwargs), 0)
    else:
        func = PRETTY_PRINTERS[type_name]
        for index, value in enumerate(list_, 0):
            result.append(func(value, index=index, **kwargs), 0)
    
    return result

def str_dict(dict_, mixed=False, name=None, **kwargs):
    result = PrettyBlock()
    if not dict_:
        result.append('Empty')
        return result
    type_name = dict_.values().__iter__().__next__().__class__.__name__
    if name is None:
        name = type_name
    result.append(f'{name}s: ({len(dict_)})')
    if mixed:
        func = PRETTY_PRINTERS[type_name]
        for index, value in enumerate(dict_.values(), 1):
            result.append(PRETTY_PRINTERS[value.__class__.__name__](value, index=index, **kwargs), 1)
    else:
        func = PRETTY_PRINTERS[type_name]
        for index, value in enumerate(dict_.values(), 1):
            result.append(func(value, index=index, **kwargs), 1)

    return result

def str_webhook(webhook, index=None,write_parents=True, **kwargs):
    result = PrettyBlock()
    
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    
    result.append(f'{start}Webhook:')
    
    name = webhook.name
    if name:
        result.append(f'- name: {name}', 1)
    else:
        result.append('- unnamed')
        
    user = webhook.user
    if user is not ZEROUSER:
        result.append(f'- user: {user.full_name}', 1)
    
    if webhook.avatar:
        result.append(f'- avatar: {webhook.avatar_url}', 1)
    
    result.append(f'- type: {webhook.type.name}', 1)
    
    channel = webhook.channel
    result.append(f'- channel : {channel.name} ({channel.id})', 1)
    if write_parents:
        guild = channel.guild
        if guild is not None:
            result.append(f'- guild : {guild.name} ({guild.id})', 1)
    
    application_id = webhook.application_id
    if application_id:
        result.append(f'- application id : {application_id}', 1)
    
    return result

def str_AuditLog(audit_log, **kwargs):
    result = PrettyBlock()
    
    result.append('AuditLog:')
    result.append(f'- guild: {audit_log.guild.name} ({audit_log.guild.id})', 1)
    result.append(f'- included users: {len(audit_log.users)}', 1)
    result.append(f'- included webhooks: {len(audit_log.webhooks)}', 1)
    result.append(f'- included integrations: {len(audit_log.integrations)}', 1)
    result.append(f'Entries: {len(audit_log.entries)}', 1)
    for index, entry in enumerate(audit_log.entries, 1):
        result.append(str_AuditLogEntry(entry, index, **kwargs))

    return result

def str_AuditLogEntry(entry, index=None, **kwargs):
    result = PrettyBlock()
    
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    
    result.append(f'{start}AuditLogEntry:')
    result.append(f'- created: {entry.created_at:{DATETIME_FORMAT_CODE}}', 1)
    result.append(f'- type: {entry.type.name} ({entry.type.value})', 1)
    user = entry.user
    if user is not None:
        result.append(f'- user: {user:f} ({user.id})', 1)
    target = entry.target
    if target is not None:
        result.append(f'- target: {target.name} {target.id} ({target.__class__.__name__})', 1)
    reason = entry.reason
    if reason is not None:
        result.append(f'- reason: {reason}', 1)
    details = entry.details
    if details is not None:
        result.append(f'- details:', 1)
        for key, value in details.items():
            result.append(f'{key} : {value}', 2)
    changes = entry.changes
    if changes is not None:
        result.append(f'- changes: ({len(changes)})', 1)
        for change in changes:
            attr = change.attr
            texts = []
            for value in (change.before, change.after):
                if value is None:
                    text='None'
                elif type(value) is list:
                    if attr == 'role':
                        text=', '.join(f'{element.name} {element.id}' for element in value)
                    elif attr == 'overwrites':
                        text = ', '.join(f'PermissionOverwrite of {element.target.name} ({element.target.id})' for element in value)
                    else:
                        raise ValueError(attr, value)
                
                elif type(value) is str:
                    text = value
                elif type(value) is tuple:
                    text = f'animated {value[0]} value {value[1]}'
                elif isinstance(value, int):
                    text = str(value)
                elif hasattr(value, 'id'):
                    text = f'{value.name} {value.id}'
                else:
                    text = repr(value)
                
                texts.append(text)
            
            result.append(f'- {attr}: {texts[0]} -> {texts[1]}', 2)
    
    return result

def str_connection(connection, index=None, **kwargs):
    result = PrettyBlock()
    
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    
    result.append(f'{start}Connection:')
    
    result.append(f'- name : {connection.name}', 1)
    result.append(f'- type : {connection.type}', 1)
    result.append(f'- id : {connection.id}', 1)
    result.append(f'- revoked : {connection.revoked}', 1)
    result.append(f'- verified : {connection.verified}', 1)
    result.append(f'- show_activity : {connection.show_activity}', 1)
    result.append(f'- friend_sync : {connection.friend_sync}', 1)
    result.append(f'- visibility : {connection.visibility}', 1)
    integrations=connection.integrations
    if integrations is not None:
        result.append(f'- integrations : ({len(integrations)})', 1)
        for index, integration in enumerate(integrations, 1):
            result.append(str_integration(integration, index=index, **kwargs), 2)
    else:
        result.append(f'- integrations : None', 1)
    return result

def str_integration(integration, index=None, **kwargs):
    result = PrettyBlock()
    
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    
    result.append(f'{start}Integration:')
    result.append(f'- name: {integration.name!r}', 1)
    result.append(f'- type: {integration.type}', 1)
    result.append(f'- {"enabled" if integration.enabled else "disabled"}', 1)
    
    result.append(f'Account:', 1)
    result.append(str_integration_account(integration.account, head_line=False, **kwargs), 1)
    
    application = integration.application
    if (application is not None):
        result.append('Application:', 1)
        result.append(str_integration_application(application, head_line=False, **kwargs), 1)
    
    detail = integration.detail
    if (detail is not None):
        result.append('Detail:', 1)
        result.append(str_integration_detail(detail, head_line=False, **kwargs), 1)
    
    return result

def str_integration_detail(detail, index=None, head_line=True, **kwargs):
    result = PrettyBlock()
    
    if head_line:
        if index is None:
            start = ''
        else:
            start = f'{index}.:'
        
        result.append(f'{start}Integration Detail:')
    
    if detail.syncing:
        result.append(f'- syncing', 1)
    
    role = detail.role
    if (role is not None):
        result.append(f'- role : {role.name!r} ({role.id})', 1)
        guild = role.guild
        if guild is None:
            result.append('- role already deleted', 1)
        else:
            result.append(f'- guild : {guild.name} ({guild.id})', 1)
    
    expire_behavior = detail.expire_behavior
    if expire_behavior != -1:
        result.append(f'- expire behavior : {expire_behavior}', 1)
    
    expire_grace_period = detail.expire_grace_period
    if expire_grace_period != -1:
        result.append(f'- expire grace period : {expire_grace_period}', 1)
    
    user = detail.user
    if (user is not ZEROUSER):
        result.append(f'- user : {user.full_name!r} ({user.id})', 1)
    
    synced_at = detail.synced_at
    if synced_at != DISCORD_EPOCH_START:
        result.append(f'- synced at : {synced_at:{DATETIME_FORMAT_CODE}}', 1)
    
    subscriber_count = detail.subscriber_count
    if subscriber_count:
        result.append(f'- subscriber count: {subscriber_count}', 1)
    
    return result

def str_integration_account(account, index=None, head_line=True, **kwargs):
    if type(account) is not IntegrationAccount:
        return str_user(account, index=index, head_line=head_line, **kwargs)
    
    result = PrettyBlock()
    
    if head_line:
        if index is None:
            start = ''
        else:
            start = f'{index}.:'
        
        result.append(f'{start}Integration Account:')
    
    result.append(f'name : {account.name!r}', 1)
    result.append(f'id : {account.id!r}', 1)
    return result

def str_integration_application(application, index=None, head_line=True, **kwargs):
    result = PrettyBlock()
    
    if head_line:
        if index is None:
            start = ''
        else:
            start = f'{index}.:'
        
        result.append(f'{start}Integration Application:')
    
    result.append(f'- id : {application.id}', 1)
    result.append(f'- name : {application.name!r}', 1)
    icon_url = application.icon_url
    if (icon_url is not None):
        result.append(f'- icon : {icon_url}', 1)
    
    description = application.description
    if len(description) > 32:
        result.append(f'- description: {description[:26]}...(+{len(description)-26})', 1)
    else:
        result.append(f'- description : {description}', 1)
    
    summary = application.summary
    if len(description) > 32:
        result.append(f'- summary: {summary[:26]}...(+{len(summary)-26})', 1)
    else:
        result.append(f'- summary : {summary}', 1)
    
    bot = application.bot
    if (bot is not ZEROUSER):
        result.append('Bot:', 1)
        result.append(str_user(bot, head_line=False, **kwargs), 1)
    
    return result

def str_activity(activity, **kwargs):
    result = PrettyBlock()
    result.append('Activity:')
    for key, value in activity.full_dict().items():
        if type(value) is dict:
            result.append(f'- {key} :', 1)
            for key, value in value.items():
                result.append(f'- {key} : {value!r}', 2)
        else:
            result.append(f'- {key} : {value!r}', 1)

    return result

def str_voice_state(state, index=None, **kwargs):
    result = PrettyBlock()
    
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    
    result.append(f'{start}Voice state:')
    user = state.user
    if user.partial:
        result.append(f'- user : Partial user {user.id}', 1)
    else:
        result.append(f'- user : {user:f} ({user.id})', 1)
    channel = state.channel
    result.append(f'- channel : {channel.name} ({channel.id})', 1)
    guild = channel.guild
    if guild is not None:
        result.append(f'- guild : {guild.name} ({guild.id})', 1)
    result.append(f'- session_id : {state.session_id!r}', 1)
    result.append(f'- mute : {state.mute}', 1)
    result.append(f'- deaf : {state.deaf}', 1)
    result.append(f'- self_mute : {state.self_mute}', 1)
    result.append(f'- self_deaf : {state.self_deaf}', 1)
    result.append(f'- self_video : {state.self_video}', 1)

    return result

def str_user_oa2(user, index=None, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    result.append(f'{start}Completed user:')
    result.append(f'- name : {user:f}', 1)
    result.append(f'- id : {user.id}', 1)
    result.append(f'- created at : {user:c}', 1)
    result.append(f'- avatar: {user.avatar_url}', 1)
    result.append(f'- mfa: {user.mfa}', 1)
    result.append(f'- verified: {user.verified}', 1)
    email = user.email
    if (email is not None):
        result.append(f'- email : {email}', 1)
    flags = user.flags
    if flags:
        result.append(f'- flags :', 1)
        for index, flag in enumerate(flags, 1):
            result.append(f'{index}.: {flag}', 2)
    else:
        result.append(f'- flags : None', 1)
    result.append(f'- premium type : {user.premium_type!s}', 1)
    result.append(f'- locale : {user.locale}', 1)

    return result

def str_GuildEmbed(guild_embed, **kwargs):
    result = PrettyBlock()
    
    result.append(f'Guild embed:')
    guild = guild_embed.guild
    result.append(f'- guild : {guild.name} ({guild.id})', 1)
    channel = guild_embed.channel
    if channel is None:
        result.append(f'- channel : None', 1)
    else:
        result.append(f'- channel : {channel.name} ({channel.id})', 1)
    result.append(f'- enabled : {guild_embed.enabled!r}', 1)
    
    return result

def str_user(user, index=None, head_line=True, **kwargs):
    result = PrettyBlock()
    
    if head_line:
        if index is None:
            start = ''
        else:
            start = f'{index}.: '
        result.append(f'{start}User:')
    
    if user.partial:
        result.append('- PARTIAL')
        result.append(f'- id : {user.id}', 1)
    else:
        result.append(f'- name : {user:f}', 1)
        result.append(f'- id : {user.id}', 1)
        if user.is_bot:
            result.append(f'- BOT', 1)
        result.append(f'- avatar: {user.avatar_url}', 1)
        flags = user.flags
        if flags:
            result.append(f'- flags :', 1)
            for index, flag in enumerate(flags, 1):
                result.append(f'{index}.: {flag}', 2)
        
        result.append(f'- known guilds: {len(user.guild_profiles)}', 1)
    result.append(f'- created at : {user:c}', 1)
    activities = user.activities
    if activities:
        result.append(f'- activities : ({len(activities)})', 1)
        for activity in activities:
            result.append(str_activity(activity, **kwargs), 2)
    
    result.append(f'- status : {user.status!s}', 1)
    if user.statuses:
        result.append(f'- statuses : ', 1)
        for platform, status in user.statuses.items():
            result.append(f'- {platform} : {status!s}', 2)
    
    return result

def str_GuildWidget(widget, **kwargs):
    result = PrettyBlock()
    result.append(f'Guild widget:')
    result.append(f'- guild : {widget.guild.name} ({widget.guild.id})', 1)
    invite_url = widget.invite_url
    if (invite_url is None):
        invite_url = '*Not included*'
    result.append(f'- invite_url : {invite_url}', 1)
    result.append(f'- online_count : {widget.online_count}', 1)
    
    result.append(str_list(widget.users, name='user', **kwargs), 1)
    result.append(str_list(widget.channels, name='channels', **kwargs), 1)
    
    return result

def str_GuildWidgetUser(GWU, index=None, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    result.append(f'{start}Guild widget user:')

    result.append(f'- name : {GWU.name}', 1)
    result.append(f'- id : {GWU.id}', 1)
    result.append(f'- avatar: {GWU.avatar_url}', 1)
    result.append(f'- status : {GWU.status!s}', 1)
    activity_name = GWU.activity_name
    if activity_name is not None:
        result.append(f'- activity : {activity_name}', 1)
        
    return result

def str_GuildWidgetChannel(GWC, index=None, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    result.append(f'{start}Guild widget channel:')

    result.append(f'- name : {GWC.name}', 1)
    result.append(f'- id : {GWC.id}', 1)
    result.append(f'- position {GWC.position}', 1)

    return result

def str_achievement(achievement, index=None, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    result.append(f'{start}Achievement:')
    result.append(f'- application_id : {achievement.application_id}', 1)
    result.append(f'- id : {achievement.id}', 1)
    result.append(f'- name : {achievement.name}', 1)
    result.append(f'- description : {achievement.description}', 1)
    result.append(f'- secret : {achievement.secret}', 1)
    result.append(f'- secure : {achievement.secure}', 1)
    result.append(f'- icon: {achievement.icon_url_as(size=4096)}', 1)
    
    return result

def str_emoji(emoji, index=None, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    result.append(f'{start}Emoji:')
    
    result.append(f'- id : {emoji.id}', 1)
    result.append(f'- name : {emoji.name}', 1)
    
    unicode = emoji.unicode
    if (unicode is not None):
        result.append(f'- unicode : {unicode.encode("utf8")}')
        return result
    
    guild = emoji.guild
    if guild is None:
        result.append('- guild : *none*', 1)
    else:
        result.append(f'- guild : {guild.name} ({guild.id})', 1)
    
    roles = emoji.roles
    if (roles is not None):
        line = ['- roles :']
        roles = sorted(roles)
        it_index = 0
        it_length = len(roles)
        
        while True:
            role = roles[it_index]
            line.append(role.mention)
            it_index +=1
            if it_index == it_length:
                break
            
            line.append(', ')
            continue
            
        result.append(''.join(line), 1)
    
    user = emoji.user
    if (user is not ZEROUSER):
        result.append(f'- user : {user.name} ({user.id})', 1)
    
    if emoji.animated:
        result.append('- animated', 1)
    
    if emoji.managed:
        result.append('- managed', 1)
    
    if not emoji.require_colons:
        result.append('- no colons required', 1)
    
    return result

def str_guild_preview(guild_preview, index=None, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    result.append(f'{start}Guild ({guild_preview.id}):')
    
    result.append(f'- name : {guild_preview.name}', 1)
    if guild_preview.icon:
        result.append(f'- icon : {guild_preview.icon_url}', 1)
    if guild_preview.splash:
        result.append(f'- splash : {guild_preview.splash_url}', 1)
    if guild_preview.discovery_splash:
        result.append(f'- discovery splash : {guild_preview.discovery_splash_url}', 1)
    result.append(f'- user count : {guild_preview.user_count}', 1)
    result.append(f'- online count : {guild_preview.online_count}', 1)
    
    description = guild_preview.description
    if (description is not None):
        result.append(f'description : {description}', 1)
    
    features = guild_preview.features
    if features:
        result.append(f'- features : {", ".join(feature.value for feature in features)}', 1)
    
    emojis = guild_preview.emojis
    if emojis:
        result.append(f'Emojis : {len(emojis)}', 1)
        for index, emoji in enumerate(emojis.values(), 1):
            if emoji.animated:
                animated = ' (animated)'
            else:
                animated = ''
            result.append(f'{index}.: {emoji.name!r} {emoji.id}{animated}', 2)
    
    return result

def str_application(application, index=None, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    
    result.append(f'{start}Application:')
    if application.partial:
        result.append('- PARTIAL', 1)
        return result
    
    result.append(f'- id : {application.id}', 1)
    result.append(f'- name : {application.name!r}', 1)
    if application.bot_public:
        result.append(f'- bot_public', 1)
    if application.bot_require_code_grant:
        result.append(f'- bot require code grant', 1)
    cover_url = application.cover_url
    if (cover_url is not None):
        result.append(f'- cover: {cover_url}', 1)
    description = application.description
    if description:
        result.append(f'- description : {description!r}', 1)
    guild_id = application.guild_id
    if guild_id:
        result.append(f'- guild id : {guild_id}', 1)
    icon_url = application.icon_url
    if (icon_url is not None):
        result.append(f'- icon : {icon_url}', 1)
    
    owner = application.owner
    if (owner is not ZEROUSER):
        result.append(PRETTY_PRINTERS[owner.__class__.__name__](owner, **kwargs), 1)
    
    primary_sku_id = application.primary_sku_id
    if primary_sku_id:
        result.append(f'- primary sku id : {primary_sku_id}', 1)
    rpc_origins = application.rpc_origins
    if (rpc_origins is not None):
        result.append(f'- rpc origins : {rpc_origins!r}', 1)
    slug = application.slug
    if (slug is not None):
        result.append(f'- slug: {slug!r}', 1)
    summary = application.summary
    if summary:
        result.append(f'- summary : {summary!r}', 1)
    verify_key = application.verify_key
    if verify_key:
        result.append(f'- verify key : {verify_key!r}', 1)
    developers = application.developers
    if (developers is not None):
        result.append(f'- developers: ({len(developers)})', 1)
        for index, developer in enumerate(developers, 1):
            result.append(f'{index}.: name={developer.name!r}, id={developer.id}', 2)
    if application.hook:
        result.append('- hook', 1)
    publishers = application.publishers
    if (publishers is not None):
        result.append(f'- publishers: ({len(publishers)})', 1)
        for index, publisher in enumerate(publishers, 1):
            result.append(f'{index}.: name={publisher.name!r}, id={publisher.id}', 2)
    executables = application.executables
    if (executables is not None):
        result.append(f'- executables: ({len(executables)})', 1)
        for index, executable in enumerate(executables, 1):
            arguments = executable.arguments
            if arguments is None:
                arguments_r = ''
            else:
                arguments_r = f', arguments={arguments!r}'
            
            if executable.is_launcher:
                is_launcher_r = f', is_launcher=True'
            else:
                is_launcher_r = ''
            
            result.append(f'{index}.: name={executable.name!r}, os={executable.os!r}{arguments_r}{is_launcher_r}', 2)
    
    third_party_skus = application.third_party_skus
    if (third_party_skus is not None):
        result.append(f' third party skus: ({len(third_party_skus)})', 1)
        for index, sku in enumerate(third_party_skus, 1):
            result.append(f'{index}.: distributor={sku.distributor!r}, id={sku.id!r} sku={sku.sku!r}' , 2)
    splash = application.splash
    if splash:
        result.append(f'- splash : {splash.as_base16_hash!r}', 1)
    if application.overlay:
        result.append('- overlay', 1)
    if application.overlay_compatibility_hook:
        result.append('- overlay compatibility hook', 1)
    aliases = application.aliases
    if (aliases is not None):
        result.append(f'- aliases : {aliases!r}', 1)
    eula_id = application.eula_id
    if eula_id:
        result.append(f'- eula id : {eula_id}', 1)
    
    return result

def str_team(team, index=None, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    
    result.append(f'{start}Team:')
    
    result.append(f'- name : {team.name}', 1)
    
    icon_url = team.icon_url
    if (icon_url is not None):
        result.append(f'- icon : {icon_url}', 1)
    
    owner = team.owner
    if (owner is not ZEROUSER):
        result.append('- owner:', 1)
        result.append(str_user(owner, head_line=False), 1)
    
    members = team.members
    if members:
        result.append(f'- members: ({len(members)})', 1)
        for index, member in enumerate(members, 1):
            result.append(f'{index}.: state={member.state.name}, permissions={member.permissions!r}', 2)
            result.append(str_user(member.user), 3)
    
    return result

def str_message_repr(message, index=None, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    
    result.append(f'{start}MessageRepr {message.id}:')
    channel = message.channel
    result.append(f'- channel {channel.id} ({channel.__class__.__name__}, {channel.type})', 1)
    
    guild = channel.guild
    if (guild is not None):
        result.append(f'- guild {guild.id}', 1)
    
    return result

def str_user_guild_permission(user_guild_permission, index=None, **kwargs):
    result = PrettyBlock()
    if index is None:
        start = ''
    else:
        start = f'{index}.: '
    
    result.append(f'{start}UserGuildPermission:')
    result.append(f'- owner: {user_guild_permission.owner}', 1)
    result.append(f'- permission: {int.__repr__(user_guild_permission.permission)}', 1)
    
    return result

PRETTY_PRINTERS['Message'] = str_message
PRETTY_PRINTERS['reaction_mapping'] = str_reaction_mapping
PRETTY_PRINTERS['reaction_mapping_line'] = str_reaction_mapping_line
PRETTY_PRINTERS['MessageApplication'] = str_message_application
PRETTY_PRINTERS['Attachment'] = str_attachment
PRETTY_PRINTERS['EmbedCore'] = str_embed_core
PRETTY_PRINTERS['Role'] = str_role
PRETTY_PRINTERS['ChannelText'] = str_channel_text
PRETTY_PRINTERS['ChannelPrivate'] = str_channel_private
PRETTY_PRINTERS['ChannelVoice'] = str_channel_voice
PRETTY_PRINTERS['ChannelGroup'] = str_channel_group
PRETTY_PRINTERS['ChannelCategory'] = str_channel_category
PRETTY_PRINTERS['ChannelStore'] = str_channel_store
PRETTY_PRINTERS['ChannelThread'] = str_channel_thread
PRETTY_PRINTERS['ChannelGuildUndefined'] = str_channel_guild_undefined
PRETTY_PRINTERS['Guild'] = str_guild
PRETTY_PRINTERS['PermissionOverwrite'] = str_PermissionOverwrite
PRETTY_PRINTERS['Permission'] = str_permission
PRETTY_PRINTERS['Invite'] = str_invite
PRETTY_PRINTERS['list'] = str_list
PRETTY_PRINTERS['dict'] = str_dict
PRETTY_PRINTERS['Webhook'] = str_webhook
PRETTY_PRINTERS['AuditLog'] = str_AuditLog
PRETTY_PRINTERS['AuditLogEntry'] = str_AuditLogEntry
PRETTY_PRINTERS['Connection'] = str_connection
PRETTY_PRINTERS['Integration'] = str_integration
PRETTY_PRINTERS['ActivityRich'] = str_activity
PRETTY_PRINTERS['ActivityUnknown'] = str_activity
PRETTY_PRINTERS['ActivityCustom'] = str_activity
PRETTY_PRINTERS['VoiceState'] = str_voice_state
PRETTY_PRINTERS['UserOA2'] = str_user_oa2
PRETTY_PRINTERS['GuildEmbed'] = str_GuildEmbed
PRETTY_PRINTERS['User'] = str_user
PRETTY_PRINTERS['Client'] = str_user
PRETTY_PRINTERS['GuildWidget'] = str_GuildWidget
PRETTY_PRINTERS['GuildWidgetUser'] = str_GuildWidgetUser
PRETTY_PRINTERS['GuildWidgetChannel'] = str_GuildWidgetChannel
PRETTY_PRINTERS['Achievement'] = str_achievement
PRETTY_PRINTERS['Emoji'] = str_emoji
PRETTY_PRINTERS['GuildPreview'] = str_guild_preview
PRETTY_PRINTERS['IntegrationApplication'] = str_integration_application
PRETTY_PRINTERS['IntegrationAccount'] = str_integration_account
PRETTY_PRINTERS['Application'] = str_application
PRETTY_PRINTERS['Team'] = str_team
PRETTY_PRINTERS['MessageRepr'] = str_message_repr
PRETTY_PRINTERS['IntegrationDetail'] = str_integration_detail
PRETTY_PRINTERS['tuple'] = str_list
PRETTY_PRINTERS['UserGuildPermission'] = str_user_guild_permission
