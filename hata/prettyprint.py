# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
try:
    from dateutil.relativedelta import relativedelta
except ImportError:
    relativedelta=None

from .dereaddons_local import multidict
from .others import cchunkify
if (relativedelta is not None):
    from .others import elapsed_time
from .permission import PERM_KEYS
from .user import ZEROUSER
from .message import MessageType

#testerfile for events
#later embeds will be added in plan

PRETTY_PRINTERS={}

class Pretty_empty(object):
    __slots__=()
    def __init__(self,text=None,back=None):
        pass
    def __str__(self):
        return ''
    def __repr__(self):
        return f'<{self.__class__.__name__} back=0 textlen=0>'
    def __len__(self):
        return None
    @property
    def textform(self):
        return ''

    def get_text(self):
        return ''
    def set_text(self,value):
        pass
    text=property(get_text,set_text)
    del get_text,set_text

    def get_back(self):
        return 0
    back=property(get_back,text.fset)
    del get_back
    
    def __call__(self,amount):
        return self
    
Pretty_empty=Pretty_empty()

class Pretty_line(object):
    __slots__=('back', 'text')
    def __init__(self,text,back=0):
        self.text=text
        self.back=back
    def __str__(self):
        return self.text
    def __repr__(self):
        return f'<{self.__class__.__name__} back=ignored textlen={len(self.text)}>'
    def __len__(self):
        return len(self.text)
    @property
    def textform(self):
        return f'{" "*(self.back<<2)}{self.text}'
    def __call__(self,amount):
        self.back+=amount
        return self


class Pretty_ignore_push(object):
    __slots__=('text',)
    def __init__(self,text,back=None):
        self.text=text
    def __str__(self):
        return self.text
    def __repr__(self):
        return f'<{self.__class__.__name__} back={self.back} textlen={len(self.text)}>'
    def __len__(self):
        return (self.back<<2)+len(self.text)
    @property
    def textform(self):
        return self.text
    def __call__(self,amount):
        pass
    back=type(Pretty_empty).back

        
    
class Pretty_block(object):
    __slots__=('container', 'back',)
    def __init__(self,back=0):
        self.container=[]
        self.back=back
    def append(self,content,back=0):
        if not content:
            value=Pretty_empty
        elif back<0:
            value=Pretty_ignore_push(content)
        elif type(content)==str:
            value=Pretty_line(content,self.back+back)
        else:
            value=content(self.back+back)
        self.container.append(value)
        
    def __repr__(self):
        return f'<{self.__class__.__name__} linelen={len(self.container)}>'
    def __call__(self,amount):
        self.back+=amount
        for value in self.container:
            value(amount)
        return self
    @property
    def textform(self):
        result=[]
        for line in self.container:
            content=line.textform
            if type(content) is list:
                result.extend(content)
            else:
                result.append(content)
        return result

def pretty_print(obj,**kwargs):
    return PRETTY_PRINTERS[obj.__class__.__name__](obj,**kwargs).textform
    
def pchunkify(obj,**kwargs):
    return cchunkify(pretty_print(obj,**kwargs))

def pconnect(obj,**kwargs):
    return '\n'.join(pretty_print(obj,**kwargs))
    
def str_message(message,index=None,**kwargs):
    result=Pretty_block()
    if index is None:
        start=''
    else:
        start=f'{index}.: '
    result.append(f'{start}Message {message.id}:')
    result.append(f'- length: {len(message)}')
    if message.author is not ZEROUSER:
        result.append(f'- author: {message.author:f}',1)
    if message.type is not MessageType.default:
        result.append(f'--------------------\n{message.clean_content}\n--------------------',-1)
    elif message.content:
        content=message.clean_content
        content_ln=len(content)
        result.append(f'- content: (len={content_ln})',1)
        if content_ln>500:
            content=content[:500].replace('`','\\`')
            result.append(f'--------------------\n{content}\n... +{content_ln-500} more\n--------------------',-1)
        else:
            content=content.replace('`','\\`')
            result.append(f'--------------------\n{content}\n--------------------',-1)
    channel=message.channel
    result.append(f'- channel {channel.id} ({channel.__class__.__name__}, {channel.type})',1)
    if channel.guild is not None:
        result.append(f'- guild {channel.guild.id}',1)
    result.append(f'- created at: {message:c}',1)
    if message.edited is not None:
        result.append(f'- edited at: {message.edited:%Y.%m.%d-%H:%M:%S}',1)
    
    if message.reactions is not None:
        result.append(str_reaction_mapping(message.reactions),1)
    if message.application is not None:
        result.append(str_message_application(message.application,1))
    
    activity=message.activity
    if (activity is not None):
        line=['- activity: ',activity.type.name]
        party_id=activity.party_id
        if party_id:
            line.append('(')
            line.append(party_id)
            line.append(')')
        
        result.append(''.join(line),1)

    if message.pinned:
        result.append('- pinned = True',1)
    if message.tts:
        result.append('- tts = True',1)
    result.append(f'- type : {message.type.name} ({message.type.value})',1)
    if message.nonce:
        result.append('- nonce = True',1)
        
    mention_count=len(message.mentions)
    if mention_count:
        result.append(f'Mentions: {mention_count}',1)
        if mention_count<9:
            index=1
            if message.everyone_mention:
                result.append(f'- {index}.: everyone',2)
                index+=1
            if message.user_mentions is not None:
                for user in message.user_mentions:
                    result.append(f'- {index}.: {user:f} ({user.id})',2)
                    index+=1
            if message.role_mentions is not None:
                for role in message.role_mentions:
                    result.append(f'- {index}.: {role.name} ({role.id})',2)
                    index+=1
            if message.channel_mentions is not None:
                for channel in message.channel_mentions:
                    result.append(f'- {index}.: {channel.name} ({channel.id})',2)
                    index+=1

        else:
            if message.everyone_mention:
                result.append('- everyone',2)
            if message.user_mentions is not None:
                result.append(f'- users ({len(message.user_mentions)})',2)
            if message.role_mentions is not None:
                result.append(f'- roles ({len(message.role_mentions)})',2)
            if message.channel_mentions is not None:
                result.append(f'- channels ({len(message.channel_mentions)})',2)
            if message.cross_mentions is not None:
                result.append(f'- cross channels ({len(message.cross_mentions)})',2)

    if message.call is not None:
        result.append(str_message_call(message.call),1)
    if message.attachments is not None:
        result.append(f'Attachments: ({len(message.attachments)})',1)
        for index,attachment in enumerate(message.attachments,1):
            result.append(str_attachment(attachment,index),1)
    if message.embeds:
        result.append(f'Embeds: ({len(message.embeds)})',1)
        for index,embed in enumerate(message.embeds,1):
            result.append(str_embed_core(embed,index),1)
    cross_reference=message.cross_reference
    if cross_reference is not None:
        result.append('Cross reference:',1)
        result.append(f'- message id : {cross_reference.message_id}',2)
        result.append(f'- channel id : {cross_reference.channel_id}',2)
        result.append(f'- guild id : {cross_reference.guild_id}',2)
    return result

def str_reaction_mapping(reactions,index=None,**kwargs): #ignore index, 1 message can have only 1
    result=Pretty_block()
    reaction_count=len(reactions)
    result.append(f'Reactions: ({reaction_count})')
    reaction_ordering=list((len(v),k) for k,v in reactions.items())
    reaction_ordering.sort(reverse=True,key=lambda x:x[0])
    for times,emoji in reaction_ordering:
        if emoji.is_unicode_emoji():
            anim=''  
        else:
            if emoji.animated:
                anim=' (animated)'
            else:
                anim=''
        result.append(f'- {emoji} ({emoji.id}){anim} : {times} times',1)
    #TODO: create a more accurate rendering for containers with small amount of emojis
    #    it will need to be able to handle unknown reactors too!
    return result

def str_reaction_mapping_line(users,**kwargs): #ignore index
    result=Pretty_block()
    user_count=len(users)
    unknown=users.unknown
    if unknown:
        result.append(f'Reacters: ({user_count}, unknown: {unknown})')
    else:
        result.append(f'Reacters: ({user_count})')
    
    for index, user in enumerate(users):
        result.append(f'{index}.: {user.full_name} ({user.id})')
    
    return result

def str_message_application(application,index=None,**kwargs): #ignore index, 1/message
    result=Pretty_block()
    result.append(f'message_application : ({application.id})')
    result.append(f'- name : {application.name}',1)
    result.append(f'- id : {application.id}',1)
    
    cover_url=application.cover_url
    if (cover_url is not None):
        result.append(f'- cover: {application.cover_url}',1)
    
    icon_url=application.icon_url
    if (icon_url is not None):
        result.append(f'- icon : {icon_url}',1)
    
    if len(application.description)>32:
        result.append(f'- descr.: {application.description[:26]}...(+{len(application.description)-26})',1)
    else:
        result.append(f'- descr.: {application.description}',1)
    return result
    
def str_attachment(attachment,index=None,**kwargs):
    result=Pretty_block()
    if index is None:
        start=''
    else:
        start=f'{index}.: '
    result.append(f'{start}Attachment: ({attachment.id}):')
    result.append(f'- name     : {attachment.name}',1)
    result.append(f'- url      : {attachment.url}',1)
    result.append(f'- proxy_url: {attachment.proxy_url}',1)
    result.append(f'- size     : {attachment.size}',1)
    if attachment.height:
        result.append(f'- height   : {attachment.height}',1)
    if attachment.width:
        result.append(f'- width    : {attachment.width}',1)
    return result

#TODO: def str_message_call(call,**kwargs):
    
def str_embed_core(embed,index=None,**kwargs):
    result=Pretty_block()
    if index is None:
        start=''
    else:
        start=f'{index}.: '
    result.append(f'{start}Embed:')
    
    title=embed.title
    if title is not None:
        content=title
        content_ln=len(content)
        result.append(f'- title    : {content_ln}',1)
        content=content.replace('`','\\`')
        result.append(f'--------------------\n{content}\n--------------------',-1)
        
    type_=embed.type
    if type_ is not None:
        result.append(f'- type     : {type_}',1)
    
    description=embed.description
    if description:
        content=description
        content_ln=len(content)
        result.append(f'- descript.: (len={content_ln})',1)
        if content_ln>500:
            content=content[:500].replace('`','\\`')
            result.append(f'--------------------\n{content}\n... +{content_ln-500} more\n--------------------',-1)
        else:
            content=content.replace('`','\\`')
            result.append(f'--------------------\n{content}\n--------------------',-1)
    
    url=embed.url
    if url is not None:
        result.append(f'- url      : {url}',1)
    
    timestamp=embed.timestamp
    if timestamp is not None:
        result.append(f'- timestamp: {timestamp:%Y.%m.%d-%H:%M:%S}',1)
    
    color=embed.color
    if color is not None:
        result.append(f'- color    : {color.as_html}',1)
    
    footer=embed.footer
    if footer is not None:
        result.append(f'- footer    :',1)
        
        content=footer.text
        content_ln=len(content)
        result.append(f'- text : {content_ln}',2)
        if content_ln>500:
            content=content[:500].replace('`','\\`')
            result.append(f'--------------------\n{content}\n... +{content_ln-500} more\n--------------------',-1)
        else:
            content=content.replace('`','\\`')
            result.append(f'--------------------\n{content}\n--------------------',-1)
        
        icon_url=footer.icon_url
        if icon_url is not None:
            result.append(f'- icon_url : {icon_url}',2)
            
            proxy_icon_url=footer.proxy_icon_url
            if proxy_icon_url is not None:
                result.append(f'- proxy_icon_url : {proxy_icon_url}',2)
                
    image=embed.image
    if image is not None:
        result.append('- image    :',1)
        
        url=image.url
        if url is not None:
            result.append(f'- url : {url}',2)
            
            proxy_url=image.proxy_url
            if proxy_url is not None:
                result.append(f'- proxy_url : {proxy_url}',2)
        
        height=image.height
        if height:
            result.append(f'- height : {height}',2)
        
        width=image.width
        if width:
            result.append(f'- width : {width}',2)
    
    thumbnail=embed.thumbnail
    if thumbnail is not None:
        result.append('- thumbnail:',1)
        
        url=thumbnail.url
        if url is not None:
            result.append(f'- url : {url}',2)
            
            proxy_url=thumbnail.proxy_url
            if proxy_url is not None:
                result.append(f'- proxy_url : {proxy_url}',2)
        
        height=thumbnail.height
        if height:
            result.append(f'- height : {height}',2)
        
        width=thumbnail.width
        if width:
            result.append(f'- width : {width}',2)
    
    video=embed.video
    if video is not None:
        result.append('- video    :',1)
        
        url=video.url
        if url is not None:
            result.append(f'- url : {url}',2)
        
        height=video.height
        if height:
            result.append(f'- height : {height}',2)
        
        width=video.width
        if width:
            result.append(f'- width : {width}',2)
            
    provider=embed.provider
    if provider is not None:
        result.append('- provider :',1)
        
        url=provider.url
        if url is not None:
            result.append(f'- url : {url}',2)
        
        name=provider.name
        if name is not None:
            result.append(f'- name : {name}',2)
            
    author=embed.author
    if author is not None:
        result.append('- author   :',1)
        
        name=author.name
        if name is not None:
            result.append(f'- name : {name}',2)
        
        url=author.url
        if url is not None:
            result.append(f'- url : {url}',2)
        
        icon_url=author.icon_url
        if icon_url is not None:
            result.append(f'- icon_url : {icon_url}',2)
            
            proxy_icon_url=author.proxy_icon_url
            if proxy_icon_url is not None:
                result.append(f'- proxy_icon_url : {proxy_icon_url}',2)
    
    fields=embed.fields
    if fields is not None:
        for index,field in enumerate(fields,1):
            result.append(f'- field {index} :',1)

            content=field.name
            content_ln=len(content)
            result.append(f'- name : {content_ln}',2)
            content=content.replace('`','\\`')
            result.append(f'--------------------\n{content}\n--------------------',-1)


            content=field.value
            content_ln=len(content)
            result.append(f'- value : {content_ln}',2)
            if content_ln>500:
                content=content[:500].replace('`','\\`')
                result.append(f'--------------------\n{content}\n... +{content_ln-500} more\n--------------------',-1)
            else:
                content=content.replace('`','\\`')
                result.append(f'--------------------\n{content}\n--------------------',-1)

            if field.inline:
                result.append(f'- inline',2)
                
    return result


def str_role(role,index=None,write_parents=True,detailed=True,**kwargs):
    result=Pretty_block()
    if index is None:
        start=''
    else:
        start=f'{index}.: '
    result.append(f'{start}Role: ({role.id})')
    result.append(f'- name : {role.name}',1)
    guild=role.guild
    if not guild:
        result.append('- DELETED',1)
        return result

    if write_parents:
        result.append(f'- guild : {guild.name} ({guild.id})',1)
    result.append(f'- position : {role.position}',1)
    result.append(f'- color : {role.color.as_html}',1)
    result.append(f'- permissions : {role.permissions}',1)
    if role.separated:
        result.append('- separated',1)
    if role.mentionable:
        result.append('- mentionable',1)
    if role.managed:
        result.append('- managed',1)
    if detailed:
        result.append('Permissions:',1)
        for key,value in role.permissions.items():
            result.append(f'- {key: <22}: {bool(value)}',2)
    return result


def str_channel_text(channel,index=None,write_parents=True,overwrites=False,**kwargs):
    result=Pretty_block()
    if index is None:
        start=''
    else:
        start=f'{index}.: '
    result.append(f'{start}ChannelText ({"news" if channel.type else "text"} {channel.type}) : ({channel.id})')
    result.append(f'- name : {channel.name}',1)
    result.append(f'- created at : {channel:c}',1)
    if not channel.clients:
        result.append('- DELETED',1)
        return result
    
    result.append(f'- position : {channel.position}',1)
    if write_parents:
        result.append(f'- guild : {channel.guild.name} ({channel.guild.id})',1)
        if channel.category!=channel.guild:
            result.append(f'- category : {channel.category.name} ({channel.category.id})',1)
    if channel.topic:
        result.append(f'- topic : "{channel.topic}"',1)
    if channel.slowmode:
        result.append(f'- slowmode : {channel.slowmode}s',1)
    if channel.nsfw:
        result.append('- NSFW',1)
    if channel.overwrites:
        if overwrites:
            result.append(f'Permission overwrites: ({len(channel.overwrites)})',1)
            for index,overwrite in enumerate(channel.overwrites,1):
                result.append(str_PermOW(overwrite,index=index,**kwargs),2)
        else:
            result.append(f'- overwrites count: {len(channel.overwrites)}',1)
    
    return result


def str_channel_private(channel,**kwargs):
    result=Pretty_block()
    result.append(f'ChannelPrivate: ({channel.id})')
    result.append(f'- created at : {channel:c}',1)
    if not channel.clients:
        result.append('- DELETED',1)
        return result

    result.append(f'Users : ({len(channel.users)})',1)
    for index,user in enumerate(channel.users,1):
        if user.partial:
            result.append(f'{index}.: Partial user {user.id}',2)
        else:
            result.append(f'{index}.: {user:f} {user.id}',2)
            
    return result

def str_channel_voice(channel,index=None,write_parents=True,overwrites=False,**kwargs):
    result=Pretty_block()
    if index is None:
        start=''
    else:
        start=f'{index}.: '
    result.append(f'{start}ChannelVoice: ({channel.id})')
    result.append(f'- name : {channel.name}',1)
    result.append(f'- created at : {channel:c}',1)
    if not channel.clients:
        result.append('- DELETED',1)
        return result
    
    result.append(f'- position : {channel.position}',1)
    if write_parents:
        result.append(f'- guild : {channel.guild.name} ({channel.guild.id})',1)
        if channel.category!=channel.guild:
            result.append(f'- category : {channel.category.name} ({channel.category.id})',1)
    if channel.bitrate:
        result.append(f'- bitrate : {channel.bitrate}',1)
    if channel.user_limit:
        result.append(f'- user limit : {channel.user_limit}',1)
    if channel.overwrites:
        if overwrites:
            result.append(f'Permission overwrites: ({len(channel.overwrites)})',1)
            for index,overwrite in enumerate(channel.overwrites,1):
                result.append(str_PermOW(overwrite,index=index,**kwargs),2)
        else:
            result.append(f'- overwrites count: {len(channel.overwrites)}',1)

    return result

def str_channel_group(channel,**kwargs):
    result=Pretty_block()
    result.append(f'ChannelGroup: ({channel.id})')
    result.append(f'- name : {channel.name}',1)
    result.append(f'- created at : {channel:c}',1)
    if not channel.clients:
        result.append('- DELETED',1)
        return result

    if channel.owner.partial:
        result.append(f'- owner : Partial user {channel.owner.id}',1)
    else:
        result.append(f'- owner: {channel.owner:f} {channel.owner.id}',1)
            
    result.append(f'Users : ({len(channel.users)})',1)
    for index,user in enumerate(channel.users,1):
        if user.partial:
            result.append(f'{index}.: Partial user {user.id}',2)
        else:
            result.append(f'{index}.: {user:f} {user.id}',2)
    if channel.icon:
        result.append(f'- icon : ({channel.icon_url})',1)

    return result

def str_channel_category(channel,index=None,write_parents=True,overwrites=False,**kwargs):
    result=Pretty_block()
    if index is None:
        start=''
    else:
        start=f'{index}.: '
    result.append(f'{start}ChannelCategory: ({channel.id})')
    result.append(f'- name : {channel.name}',1)
    result.append(f'- created at : {channel:c}',1)
    if not channel.clients:
        result.append('- DELETED',1)
        return result
    
    result.append(f'- position : {channel.position}',1)
    if write_parents:
        result.append(f'- guild : {channel.guild.name} ({channel.guild.id})',1)
    if channel.channels:
        result.append(str_weakposlist(channel.channels,write_parents=write_parents),1)
    if channel.overwrites:
        if overwrites:
            result.append('Permission overwrites: ({len(channel.overwrites)})',1)
            for index,overwrite in enumerate(channel.overwrites,1):
                result.append(str_PermOW(overwrite,index=index,**kwargs),2)
        else:
            result.append(f'- overwrites count: {len(channel.overwrites)}',1)
    
    return result

def str_channel_store(channel,index=None,write_parents=True,overwrites=False,**kwargs):
    result=Pretty_block()
    if index is None:
        start=''
    else:
        start=f'{index}.: '
    result.append(f'{start}ChannelStore ({channel.type})')
    result.append(f'- name : {channel.name}',1)
    result.append(f'- created at : {channel:c}',1)
    if not channel.clients:
        result.append('- DELETED',1)
        return result
    
    result.append(f'- position : {channel.position}',1)

    if write_parents:
        result.append(f'- guild : {channel.guild.name} ({channel.guild.id})',1)
        if channel.category!=channel.guild:
            result.append(f'- category : {channel.category.name} ({channel.category.id})',1)
    if channel.nsfw:
        result.append('- NSFW',1)
    if channel.overwrites:
        if overwrites:
            result.append(f'Permission overwrites: ({len(channel.overwrites)})',1)
            for index,overwrite in enumerate(channel.overwrites,1):
                result.append(str_PermOW(overwrite,index=index,**kwargs),2)
        else:
            result.append(f'- overwrites count: {len(channel.overwrites)}',1)

    return result

def str_weakposlist(list_,**kwargs):
    result=Pretty_block()
    result.append(f'Channels : ({len(list_)})')
    for index,value in enumerate(list_,1):
        result.append(PRETTY_PRINTERS[value.__class__.__name__](value,index=index,**kwargs),1)
    return result

def str_autoposlist(list_,detailed=False,**kwargs):
    result=Pretty_block()
    result.append(f'Roles : ({len(list_)})')
    for index,value in enumerate(list_,1):
        result.append(PRETTY_PRINTERS[value.__class__.__name__](value,index=index,detailed=detailed,**kwargs),1)
    return result

def str_guild(guild,index=None,**kwargs):
    result=Pretty_block()
    if index is None:
        start=''
    else:
        start=f'{index}.: '
    result.append(f'{start}Guild ({guild.id}):')
    
    result.append(f'- name : {guild.name}',1)
    if guild.icon:
        result.append(f'- icon : {guild.icon_url}',1)
    if guild.banner:
        result.append(f'banner : {guild.banner_url}',1)
    if guild.splash:
        result.append(f'- splash : {guild.splash_url}',1)
    if guild.discovery_splash:
        result.append(f'- discovery splash : {guild.discovery_splash_url}',1)
    if not guild.clients or not guild.available:
        result.append('- PARTIAL/UNAVAILABLE/DELETED',1)
        return result
    result.append(f'- verification level : {guild.verification_level.name}',1)
    result.append(f'- users : {guild.user_count}',1)
    result.append(f'- afk timeout : {guild.afk_timeout}s',1)
    result.append(f'- message notification : {guild.message_notification.name}',1)
    result.append(f'- mfa level : {guild.mfa.name}',1)
    result.append(f'- content filter : {guild.content_filter.name}',1)
    result.append(f'- available : {guild.available}',1)
    result.append(f'- max_users : {guild.max_users}',1)
    result.append(f'- max_presences : {guild.max_presences}',1)
    result.append(f'- preferred_locale : {guild.preferred_locale}',1)
    if guild.description:
        result.append(f'description : {guild.description}',1)
    if guild.vanity_code:
        result.append(f'vanity_code : {guild.vanity_code}',1)
    if guild.features:
        result.append(f'- features : {", ".join(feature.value for feature in guild.features)}',1)
    if guild.owner.partial:
            result.append(f'- owner : Partial user {guild.owner.id}',1)
    else:
        result.append(f'- owner : {guild.owner:f} {guild.owner.id}',1)
    
    system_channel=guild.system_channel
    if (system_channel is not None):
        result.append(f'- system channel: {system_channel.name} {system_channel.id}',1)
    
    afk_channel=guild.afk_channel
    if (afk_channel is not None):
        result.append(f'- afk channel: {afk_channel.name} {afk_channel.id}',1)
    
    widget_channel=guild.widget_channel
    if (widget_channel is not None):
        result.append(f'- widget channel: {widget_channel.name} {widget_channel.id}',1)
    
    embed_channel=guild.embed_channel
    if (embed_channel is not None):
        result.append(f'- embed channel : {embed_channel.name} {embed_channel.id}',1)
    
    rules_channel=guild.rules_channel
    if (rules_channel is not None):
        result.append(f'- rules channel : {rules_channel.name} {rules_channel.id}',1)
    
    public_updates_channel=guild.public_updates_channel
    if (public_updates_channel is not None):
        result.append(f'-public updates channel : {public_updates_channel.name} {public_updates_channel.id}',1)
    
    if guild.booster_count:
        result.append(f'- boosters : {guild.booster_count}',1)
        result.append(f'- premium tier : {guild.premium_tier}',1)
    result.append(str_weakposlist(guild.channels,write_parents=False),1)
    result.append(str_autoposlist(guild.roles,write_parents=False),1)
    if guild.voice_states:
        voice_states=multidict()
        for voice_state in guild.voice_states.values():
            voice_states[voice_state.channel]=voice_state.user
        result.append(f'Voice_states : {len(guild.voice_states)}',1)
        for channel,users in dict.items(voice_states):
            result.append(f'Channel {channel.name} {channel.id}',2)
            for index,user in enumerate(users,1):
                result.append(f'{index}.: {user:f} {user.id}',3)
    if guild.emojis:
        result.append(f'Emojis : {len(guild.emojis)}',1)
        for index,emoji in enumerate(guild.emojis.values(),1):
            if emoji.animated:
                animated=' (animated)'
            else:
                animated=''
            result.append(f'{index}.: {emoji.name} {emoji.id}{animated}',2)
    return result

def str_PermOW(overwrite,index=None,detailed=True,**kwargs):
    result=Pretty_block()
    if index is None:
        start=''
    else:
        start=f'{index}.: '
        
    result.append(f'{start}Permission overwrite:')
    target=overwrite.target
    if overwrite.type=='member':
        result.append(f'- target: user "{target:f}" ({target.id})',1)
    else:
        result.append(f'- target: role "{target.name}" ({target.id})',1)
    allow=overwrite.allow
    deny=overwrite.deny
    if detailed:
        result.append('Permission changes:',1)
        for name,push in PERM_KEYS.items():
            if (allow>>push)&1:
                v='allow'
            elif (deny>>push)&1:
                v='deny'
            else:
                continue
            result.append(f'- {name: <22}: {v}',2)
            
    else:
        result.append(f'- allow : {allow}',1)
        result.append(f'- deny  : {deny}',1)
        
    return result

def str_permission(permission,**kwargs):
    result=Pretty_block()
    result.append('Permission:')
    for name,value in permission.items():
        value=bool(value)
        result.append(f'- {name: <22}: {value}',1)
    return result

def str_invite(invite,index=None,write_parents=True,**kwargs):
    result=Pretty_block()
    if index is None:
        start=''
    else:
        start=f'{index}.: '
    result.append(f'{start}Invite:')
    result.append(f'- inviter : {invite.inviter:f}',1)
    result.append(f'- code : {invite.code}',1)
    
    channel=invite.channel
    if channel is not None:
        result.append(f'- channel : {channel.name} ({channel.id})',1)
    
    if write_parents:
        guild=invite.guild
        if guild is not None:
            result.append(f'- guild : {guild.name} ({guild.id})',1)
    
    uses=invite.uses
    if uses is not None:
        if invite.max_uses:
            max_uses=str(invite.max_uses)
        else:
            max_uses='unlimited'
        result.append(f'- uses : {uses}/{max_uses}',1)
    
    created_at=invite.created_at
    if (created_at is not None):
        result.append(f'- created at : {created_at:%Y.%m.%d-%H:%M:%S}',1)
        max_age=invite.max_age
        if (max_age is not None):
            if (relativedelta is None):
                result.append(f'- max_age : {max_age}')
            else:
                result.append(f'- time left : {elapsed_time(relativedelta(created_at+timedelta(0,max_age),datetime.utcnow()))}',1)
    
    target_user=invite.target_user
    if target_user is not ZEROUSER:
        result.append(f'- inviter : {target_user:f}',1)
    
    target_type=invite.target_type
    if target_type.value:
        result.append(f'- target_type : {target_type.name}',1)
    
    online_count=invite.online_count
    if online_count:
        result.append(f'- online count : {online_count}',1)
        
    total_count=invite.total_count
    if total_count:
        result.append(f'- total count : {total_count}',1)
    
    result.append(f'- {"temporary" if invite.temporary else "permament"}',1)

    return result

def str_list(list_,mixed=False,name=None,**kwargs):
    result=Pretty_block()
    if not list_:
        if name is not None:
            result.append(f'{name}s: (0)')
        else:
            result.append('Empty list')
        return result
    type_name=list_[0].__class__.__name__
    if name is None:
        name=type_name
    result.append(f'{name}s: ({len(list_)})')
    if mixed:
        func=PRETTY_PRINTERS[type_name]
        for index,value in enumerate(list_,1):
            result.append(PRETTY_PRINTERS[value.__class__.__name__](value,index=index,**kwargs),1)
    else:
        func=PRETTY_PRINTERS[type_name]
        for index,value in enumerate(list_,1):
            result.append(func(value,index=index,**kwargs),1)

    return result

def str_dict(dict_,mixed=False,name=None,**kwargs):
    result=Pretty_block()
    if not dict_:
        result.append('Empty')
        return result
    type_name=dict_.values().__iter__().__next__().__class__.__name__
    if name is None:
        name=type_name
    result.append(f'{name}s: ({len(dict_)})')
    if mixed:
        func=PRETTY_PRINTERS[type_name]
        for index,value in enumerate(dict_.values(),1):
            result.append(PRETTY_PRINTERS[value.__class__.__name__](value,index=index,**kwargs),1)
    else:
        func=PRETTY_PRINTERS[type_name]
        for index,value in enumerate(dict_.values(),1):
            result.append(func(value,index=index,**kwargs),1)

    return result

def str_webhook(webhook,index=None,write_parents=True,**kwargs):
    result=Pretty_block()
    
    if index is None:
        start=''
    else:
        start=f'{index}.: '
    
    result.append(f'{start}Webhook:')
    
    name=webhook.name
    if name:
        result.append(f'- name: {name}',1)
    else:
        result.append('- unnamed')
        
    user=webhook.user
    if user is not ZEROUSER:
        result.append(f'- user: {user.full_name}',1)
    
    if webhook.avatar:
        result.append(f'- avatar: {webhook.avatar_url}',1)
    
    result.append(f'- type: {webhook.type.name}',1)
    
    channel=webhook.channel
    result.append(f'- channel : {channel.name} ({channel.id})',1)
    if write_parents:
        guild=channel.guild
        if guild is not None:
            result.append(f'- guild : {guild.name} ({guild.id})',1)
            
    return result

def str_AuditLog(AuditLog,**kwargs):
    result=Pretty_block()
    
    result.append('AuditLog:')
    result.append(f'- guild: {AuditLog.guild.name} ({AuditLog.guild.id})',1)
    result.append(f'- included users: {len(AuditLog.users)}',1)
    result.append(f'- included webhooks: {len(AuditLog.webhooks)}',1)
    result.append(f'Entries: {len(AuditLog.logs)}',1)
    for index,entry in enumerate(AuditLog.logs,1):
        result.append(str_AuditLogEntry(entry,index,**kwargs))

    return result

def str_AuditLogEntry(entry,index=None,**kwargs):
    result=Pretty_block()
    
    if index is None:
        start=''
    else:
        start=f'{index}.: '
    
    result.append(f'{start}AuditLogEntry:')
    result.append(f'- created: {entry.created_at:%Y.%m.%d-%H:%M:%S}',1)
    result.append(f'- type: {entry.type.name} ({entry.type.value})',1)
    user=entry.user
    if user is not None:
        result.append(f'- user: {user:f} ({user.id})',1)
    target=entry.target
    if target is not None:
        result.append(f'- target: {target.name} {target.id} ({target.__class__.__name__})',1)
    reason=entry.reason
    if reason is not None:
        result.append(f'- reason: {reason}',1)
    details=entry.details
    if details is not None:
        result.append(f'- details:',1)
        for key,value in details.items():
            result.append(f'{key} : {value}',2)
    changes=entry.changes
    if changes is not None:
        result.append(f'- changes: ({len(changes)})',1)
        for change in changes:
            attr=change.attr
            texts=[]
            for value in (change.before,change.after):
                if value is None:
                    text='None'
                elif type(value) is list:
                    if attr=='role':
                        text=', '.join(f'{element.name} {element.id}' for element in value)
                    elif attr=='overwrites':
                        text=', '.join(f'PermOW of {element.target.name} ({element.target.id})' for element in value)
                    else:
                        raise ValueError(attr,value)
                elif type(value) is str:
                    text=value
                elif type(value) is tuple:
                    text=f'animated {value[0]} value {value[1]}'
                elif isinstance(value,int):
                    text=str(value)
                elif hasattr(value,'id'):
                    text=f'{value.name} {value.id}'
                else:
                    text=f'{value.name} {value.value}'

                texts.append(text)
            
            result.append(f'- {attr}: {texts[0]} -> {texts[1]}',2)

    return result

def str_connection(connection,index=None,**kwargs):
    result=Pretty_block()
    
    if index is None:
        start=''
    else:
        start=f'{index}.: '
    
    result.append(f'{start}Connection:')
    
    result.append(f'- name : {connection.name}',1)
    result.append(f'- type : {connection.type}',1)
    result.append(f'- id : {connection.id}',1)
    result.append(f'- revoked : {connection.revoked}',1)
    result.append(f'- verified : {connection.verified}',1)
    result.append(f'- show_activity : {connection.show_activity}',1)
    result.append(f'- friend_sync : {connection.friend_sync}',1)
    result.append(f'- visibility : {connection.visibility}',1)
    integrations=connection.integrations
    if integrations is not None:
        result.append(f'- integrations : ({len(integrations)})',1)
        for index,integration in enumerate(integrations,1):
            result.append(str_integration(integration,index=index,**kwargs),2)
    else:
        result.append(f'- integrations : None',1)
    return result

def str_integration(integration,index=None,**kwargs):
    result=Pretty_block()

    if index is None:
        start=''
    else:
        start=f'{index}.: '

    result.append(f'{start}Integration:')
    result.append(f'- name: {integration.name}',1)
    result.append(f'- type: {integration.type}',1)
    result.append(f'- {"enabled" if integration.enabled else "disabled"}',1)
    result.append(f'- {"syncing" if integration.syncing else "not syncing"}',1)
    role=integration.role
    if role is None:
        result.append('- role: None',1)
    else:
        result.append(f'- role : {role.name} ({role.id})',1)
        guild=role.guild
        if guild is None:
            result.append('- role already deleted',1)
        else:
            result.append(f'- guild : {guild.name} ({guild.id})',1)
    result.append(f'- expire behavior : {integration.expire_behavior}',1)
    result.append(f'- expire grace period : {integration.expire_grace_period}',1)
    result.append(f'- user : {integration.user:f} ({integration.user.id}',1)
    result.append(f'- account id : {integration.account_id}',1)
    result.append(f'- account name : {integration.account_name}',1)
    result.append(f'- synced at : {integration.synced_at:%Y.%m.%d-%H:%M:%S}',1)

    return result
            
def str_activity(activity,**kwargs):
    result=Pretty_block()
    result.append('Activity:')
    for key,value in activity.fulldict().items():
        if type(value) is dict:
            result.append(f'- {key} :',1)
            for key,value in value.items():
                result.append(f'- {key} : {value!r}',2)
        else:
            result.append(f'- {key} : {value!r}',1)

    return result

def str_voice_state(state,index=None,**kwargs):
    result=Pretty_block()
    
    if index is None:
        start=''
    else:
        start=f'{index}.: '
    
    result.append(f'{start}Voice state:')
    user=state.user
    if user.partial:
        result.append(f'- user : Parital user {user.id}',1)
    else:
        result.append(f'- user : {user:f} ({user.id})',1)
    channel=state.channel
    result.append(f'- channel : {channel.name} ({channel.id})',1)
    guild=channel.guild
    if guild is not None:
        result.append(f'- guild : {guild.name} ({guild.id})',1)
    result.append(f'- session_id : {state.session_id!r}',1)
    result.append(f'- mute : {state.mute}',1)
    result.append(f'- deaf : {state.deaf}',1)
    result.append(f'- self_mute : {state.self_mute}',1)
    result.append(f'- self_deaf : {state.self_deaf}',1)
    result.append(f'- self_video : {state.self_video}',1)

    return result

def str_useroa2(user,index=None,**kwargs):
    result=Pretty_block()
    if index is None:
        start=''
    else:
        start=f'{index}.: '
    result.append(f'{start}Completed user:')
    result.append(f'- name : {user:f}',1)
    result.append(f'- id : {user.id}',1)
    result.append(f'- created at : {user:c}',1)
    result.append(f'- avatar: {user.avatar_url}',1)
    result.append(f'- mfa: {user.mfa}',1)
    result.append(f'- verified: {user.verified}',1)
    if user.email:
        result.append(f'- email : {user.email}',1)
    flags=user.flags
    if flags:
        result.append(f'- flags :',1)
        for index,flag in enumerate(flags,1):
            result.append(f'{index}.: {flag}',2)
    else:
        result.append(f'- flags : None',1)
    result.append(f'- premium type : {user.premium_type!s}',1)
    result.append(f'- locale : {user.locale}',1)

    return result

def str_GuildEmbed(guild_embed,**kwargs):
    result=Pretty_block()
    
    result.append(f'Guild embed:')
    guild=guild_embed.guild
    result.append(f'- guild : {guild.name} ({guild.id})',1)
    channel=guild_embed.channel
    if channel is None:
        result.append(f'- channel : None',1)
    else:
        result.append(f'- channel : {channel.name} ({channel.id})',1)
    result.append(f'- enabled : {guild_embed.enabled!r}',1)
    
    return result

def str_user(user,index=None,**kwargs):
    result=Pretty_block()
    if index is None:
        start=''
    else:
        start=f'{index}.: '
    result.append(f'{start}User:')
    if user.partial:
        result.append('- PARTIAL')
        result.append(f'- id : {user.id}',1)
    else:
        result.append(f'- name : {user:f}',1)
        result.append(f'- id : {user.id}',1)
        if user.is_bot:
            result.append(f'- BOT',1)
        result.append(f'- avatar: {user.avatar_url}',1)
        result.append(f'- known guilds: {len(user.guild_profiles)}',1)
    result.append(f'- created at : {user:c}',1)
    if user.activities:
        result.append(f'- activities : ({len(user.activities)})')
        for activity in user.activities:
            result.append(str_activity(activity,**kwargs),2)
    else:
        result.append(str_activity(user.activity,**kwargs),1)
    result.append(f'- status : {user.status!s}',1)
    if user.statuses:
        result.append(f'- stauses : ',1)
        for platform,status in user.statuses.items():
            result.append(f'- {platform} : {status!s}',2)
    
    return result

def str_GuildWidget(widget,**kwargs):
    result=Pretty_block()
    result.append(f'Guild widget:')
    result.append(f'- guild : {widget.guild.name} ({widget.guild.id})',1)
    invite_url=widget.invite_url
    if invite_url:
        result.append(f'- invite_url : {invite_url}',1)
    else:
        result.append(f'- invite_url : *Not included*',1)
    result.append(f'- presence_count : {widget.presence_count}',1)
    
    result.append(str_list(widget.users,name='user',**kwargs),1)
    result.append(str_list(widget.channels,name='channels',**kwargs),1)
    
    return result

def str_GWUserReflection(GWU,index=None,**kwargs):
    result=Pretty_block()
    if index is None:
        start=''
    else:
        start=f'{index}.: '
    result.append(f'{start}Guild widget user:')

    result.append(f'- name : {GWU.name}',1)
    result.append(f'- id : {GWU.id}',1)
    result.append(f'- avatar: {GWU.avatar_url}',1)
    result.append(f'- status : {GWU.status!s}',1)
    activity_name=GWU.activity_name
    if activity_name is not None:
        result.append(f'- activity : {activity_name}',1)
        
    return result

def str_GWChannelReflection(GWC,index=None,**kwargs):
    result=Pretty_block()
    if index is None:
        start=''
    else:
        start=f'{index}.: '
    result.append(f'{start}Guild widget channel:')

    result.append(f'- name : {GWC.name}',1)
    result.append(f'- id : {GWC.id}',1)
    result.append(f'- position {GWC.position}',1)

    return result

def str_message_call(call,**kwargs):
    result=Pretty_block()

    result.append(f'Message call:')

    if call.ended_timestamp is None:
        result.append('- ended : not yet',1)
    else:
        result.append(f'- ended : {call.ended_timestamp:%Y.%m.%d-%H:%M:%S}',1)
    result.append(f'- message : {call.message.id}',1)
    result.append(f'Users: {len(call.users)}',1)
    for index,user in enumerate(call.users,1):
        result.append(f'{index}.: {user:f}',2)

    return result

def str_achievement(achievement,index=None,**kwargs):
    result=Pretty_block()
    if index is None:
        start=''
    else:
        start=f'{index}.: '
    result.append(f'{start}Achievement:')
    result.append(f'- application_id : {achievement.application_id}',1)
    result.append(f'- id : {achievement.id}',1)
    result.append(f'- name : {achievement.name}',1)
    result.append(f'- description : {achievement.description}',1)
    result.append(f'- secret : {achievement.secret}',1)
    result.append(f'- secure : {achievement.secure}',1)
    result.append(f'- icon: {achievement.icon_url_as(size=4096)}',1)
    
    return result

def str_emoji(emoji,index=None,**kwargs):
    result=Pretty_block()
    if index is None:
        start=''
    else:
        start=f'{index}.: '
    result.append(f'{start}Emoji:')
    
    result.append(f'- id : {emoji.id}',1)
    result.append(f'- name : {emoji.name}',1)
    
    unicode = emoji.unicode
    if (unicode is not None):
        result.append(f'- unicode : {unicode.encode("utf8")}')
        return result
    
    guild=emoji.guild
    if guild is None:
        result.append('- guild : *none*',1)
    else:
        result.append(f'- guild : {guild.name} ({guild.id})',1)
    
    roles=emoji.roles
    if (roles is not None) and roles:
        line=['- roles :']
        roles=sorted(roles)
        it_index=0
        it_length=len(roles)
        
        while True:
            role=roles[it_index]
            line.append(role.mention)
            it_index+=1
            if it_index==it_length:
                break
            
            line.append(', ')
            continue
            
        result.append(''.join(line),1)
    
    user=emoji.user
    if (user is not ZEROUSER):
        result.append(f'- user : {user.name} ({user.id})',1)
        
    if emoji.animated:
        result.append('- animated',1)
    
    if emoji.managed:
        result.append('- managed',1)
    
    if not emoji.require_colons:
        result.append('- no colons required',1)
    
    return result
    
PRETTY_PRINTERS['Message']=str_message
PRETTY_PRINTERS['reaction_mapping']=str_reaction_mapping
PRETTY_PRINTERS['reaction_mapping_line']=str_reaction_mapping_line
PRETTY_PRINTERS['MessageApplication']=str_message_application
PRETTY_PRINTERS['Attachment']=str_attachment
PRETTY_PRINTERS['EmbedCore']=str_embed_core
PRETTY_PRINTERS['Role']=str_role
PRETTY_PRINTERS['ChannelText']=str_channel_text
PRETTY_PRINTERS['ChannelPrivate']=str_channel_private
PRETTY_PRINTERS['ChannelVoice']=str_channel_voice
PRETTY_PRINTERS['ChannelGroup']=str_channel_group
PRETTY_PRINTERS['ChannelCategory']=str_channel_category
PRETTY_PRINTERS['ChannelStore']=str_channel_store
PRETTY_PRINTERS['autoposlist']=str_autoposlist
PRETTY_PRINTERS['weakposlist']=str_weakposlist
PRETTY_PRINTERS['Guild']=str_guild
PRETTY_PRINTERS['PermOW']=str_PermOW
PRETTY_PRINTERS['Permission']=str_permission
PRETTY_PRINTERS['Invite']=str_invite
PRETTY_PRINTERS['list']=str_list
PRETTY_PRINTERS['dict']=str_dict
PRETTY_PRINTERS['Webhook']=str_webhook
PRETTY_PRINTERS['AuditLog']=str_AuditLog
PRETTY_PRINTERS['AuditLogEntry']=str_AuditLogEntry
PRETTY_PRINTERS['Connection']=str_connection
PRETTY_PRINTERS['Integration']=str_integration
PRETTY_PRINTERS['ActivityRich']=str_activity
PRETTY_PRINTERS['ActivityUnknown']=str_activity
PRETTY_PRINTERS['ActivityGame']=str_activity
PRETTY_PRINTERS['ActivityStream']=str_activity
PRETTY_PRINTERS['ActivitySpotify']=str_activity
PRETTY_PRINTERS['ActivityWatching']=str_activity
PRETTY_PRINTERS['ActivityCustom']=str_activity
PRETTY_PRINTERS['Voice_state']=str_voice_state
PRETTY_PRINTERS['UserOA2']=str_useroa2
PRETTY_PRINTERS['GuildEmbed']=str_GuildEmbed
PRETTY_PRINTERS['User']=str_user
PRETTY_PRINTERS['Client']=str_user
PRETTY_PRINTERS['GuildWidget']=str_GuildWidget
PRETTY_PRINTERS['GWUserReflection']=str_GWUserReflection
PRETTY_PRINTERS['GWChannelReflection']=str_GWChannelReflection
PRETTY_PRINTERS['Achievement']=str_achievement
PRETTY_PRINTERS['Emoji']=str_emoji
