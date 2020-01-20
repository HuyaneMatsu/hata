# -*- coding: utf-8 -*-
__all__ = ('AuditLog', 'AuditLogEntry', 'AuditLogEvent',
    'AuditLogIterator', 'AuditLogChange', )

from .others import VerificationLevel, ContentFilterLevel, Unknown,         \
    now_as_id, id_to_time, VoiceRegion, MessageNotificationLevel, MFA
from .client_core import INTEGRATIONS, CHANNELS, USERS, ROLES, EMOJIS
from .permission import Permission
from .color import Color
from .user import User
from .webhook import Webhook
from .role import PermOW

class AuditLogEvent(object):
    # class related
    INSTANCES = {}
    
    # object related
    __slots__=('name', 'value', )
    
    def __init__(self,value,name):
        self.value=value
        self.name=name

        self.INSTANCES[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'
    
    # predefined
    GUILD_UPDATE            = NotImplemented
    
    CHANNEL_CREATE          = NotImplemented
    CHANNEL_UPDATE          = NotImplemented
    CHANNEL_DELETE          = NotImplemented
    CHANNEL_OVERWRITE_CREATE= NotImplemented
    CHANNEL_OVERWRITE_UPDATE= NotImplemented
    CHANNEL_OVERWRITE_DELETE= NotImplemented
    
    MEMBER_KICK             = NotImplemented
    MEMBER_PRUNE            = NotImplemented
    MEMBER_BAN_ADD          = NotImplemented
    MEMBER_BAN_REMOVE       = NotImplemented
    MEMBER_UPDATE           = NotImplemented
    MEMBER_ROLE_UPDATE      = NotImplemented
    MEMBER_MOVE             = NotImplemented
    MEMBER_DISCONNECT       = NotImplemented
    BOT_ADD                 = NotImplemented
    
    ROLE_CREATE             = NotImplemented
    ROLE_UPDATE             = NotImplemented
    ROLE_DELETE             = NotImplemented
    
    INVITE_CREATE           = NotImplemented
    INVITE_UPDATE           = NotImplemented
    INVITE_DELETE           = NotImplemented
    
    WEBHOOK_CREATE          = NotImplemented
    WEBHOOK_UPDATE          = NotImplemented
    WEBHOOK_DELETE          = NotImplemented
    
    EMOJI_CREATE            = NotImplemented
    EMOJI_UPDATE            = NotImplemented
    EMOJI_DELETE            = NotImplemented
    
    MESSAGE_DELETE          = NotImplemented
    MESSAGE_BULK_DELETE     = NotImplemented
    MESSAGE_PIN             = NotImplemented
    MESSAGE_UNPIN           = NotImplemented
    
    INTEGRATION_CREATE      = NotImplemented
    INTEGRATION_UPDATE      = NotImplemented
    INTEGRATION_DELETE      = NotImplemented

AuditLogEvent.GUILD_UPDATE              = AuditLogEvent( 1,'GUILD_UPDATE')

AuditLogEvent.CHANNEL_CREATE            = AuditLogEvent(10,'CHANNEL_CREATE')
AuditLogEvent.CHANNEL_UPDATE            = AuditLogEvent(11,'CHANNEL_UPDATE')
AuditLogEvent.CHANNEL_DELETE            = AuditLogEvent(12,'CHANNEL_DELETE')
AuditLogEvent.CHANNEL_OVERWRITE_CREATE  = AuditLogEvent(13,'CHANNEL_OVERWRITE_CREATE')
AuditLogEvent.CHANNEL_OVERWRITE_UPDATE  = AuditLogEvent(14,'CHANNEL_OVERWRITE_UPDATE')
AuditLogEvent.CHANNEL_OVERWRITE_DELETE  = AuditLogEvent(15,'CHANNEL_OVERWRITE_DELETE')

AuditLogEvent.MEMBER_KICK               = AuditLogEvent(20,'MEMBER_KICK')
AuditLogEvent.MEMBER_PRUNE              = AuditLogEvent(21,'MEMBER_PRUNE')
AuditLogEvent.MEMBER_BAN_ADD            = AuditLogEvent(22,'MEMBER_BAN_ADD')
AuditLogEvent.MEMBER_BAN_REMOVE         = AuditLogEvent(23,'MEMBER_BAN_REMOVE')
AuditLogEvent.MEMBER_UPDATE             = AuditLogEvent(24,'MEMBER_UPDATE')
AuditLogEvent.MEMBER_ROLE_UPDATE        = AuditLogEvent(25,'MEMBER_ROLE_UPDATE')
AuditLogEvent.MEMBER_MOVE               = AuditLogEvent(26,'MEMBER_MOVE')
AuditLogEvent.MEMBER_DISCONNECT         = AuditLogEvent(27,'MEMBER_DISCONNECT')
AuditLogEvent.BOT_ADD                   = AuditLogEvent(28,'MEMBER_ROLE_UPDATE')

AuditLogEvent.ROLE_CREATE               = AuditLogEvent(30,'ROLE_CREATE')
AuditLogEvent.ROLE_UPDATE               = AuditLogEvent(31,'ROLE_UPDATE')
AuditLogEvent.ROLE_DELETE               = AuditLogEvent(32,'ROLE_DELETE')

AuditLogEvent.INVITE_CREATE             = AuditLogEvent(40,'INVITE_CREATE')
AuditLogEvent.INVITE_UPDATE             = AuditLogEvent(41,'INVITE_UPDATE')
AuditLogEvent.INVITE_DELETE             = AuditLogEvent(42,'INVITE_DELETE')

AuditLogEvent.WEBHOOK_CREATE            = AuditLogEvent(50,'WEBHOOK_CREATE')
AuditLogEvent.WEBHOOK_UPDATE            = AuditLogEvent(51,'WEBHOOK_UPDATE')
AuditLogEvent.WEBHOOK_DELETE            = AuditLogEvent(52,'WEBHOOK_DELETE')

AuditLogEvent.EMOJI_CREATE              = AuditLogEvent(60,'EMOJI_CREATE')
AuditLogEvent.EMOJI_UPDATE              = AuditLogEvent(61,'EMOJI_UPDATE')
AuditLogEvent.EMOJI_DELETE              = AuditLogEvent(62,'EMOJI_DELETE')

AuditLogEvent.MESSAGE_DELETE            = AuditLogEvent(72,'MESSAGE_DELETE')
AuditLogEvent.MESSAGE_BULK_DELETE       = AuditLogEvent(73,'MESSAGE_BULK_DELETE')
AuditLogEvent.MESSAGE_PIN               = AuditLogEvent(74,'MESSAGE_PIN')
AuditLogEvent.MESSAGE_UNPIN             = AuditLogEvent(75,'MESSAGE_UNPIN')

AuditLogEvent.INTEGRATION_CREATE        = AuditLogEvent(80,'INTEGRATION_CREATE')
AuditLogEvent.INTEGRATION_UPDATE        = AuditLogEvent(81,'INTEGRATION_UPDATE')
AuditLogEvent.INTEGRATION_DELETE        = AuditLogEvent(82,'INTEGRATION_DELETE')

class AuditLog(object):
    __slots__=('guild', 'logs', 'users', 'webhooks',)
    def __init__(self,data,guild):
        self.guild=guild
        
        self.webhooks=webhooks={}
        try:
            webhook_datas=data['webhook']
        except KeyError:
            pass
        else:
            for webhook_data in webhook_datas:
                webhook=Webhook(webhook_data)
                webhooks[webhook.id]=webhook
        
        self.users=users={}
        try:
            user_datas=data['users']
        except KeyError:
            pass
        else:
            for user_data in user_datas:
                user=User(user_data)
                users[user.id]=user
        
        try:
            log_datas=data['audit_log_entries']
        except KeyError:
            self.logs=[]
        else:
            self.logs=[AuditLogEntry(log_data,guild,webhooks,users) for log_data in log_datas]
    
    def __iter__(self):
        return self.logs.__iter__()
    
    def __reversed__(self):
        return self.logs.__reversed__()
    
    def __len__(self):
        return len(self.logs)
    
    def __getitem__(self,index):
        return self.logs.__getitem__(index)
    
    def __repr__(self):
        return f'<{self.__class__.__name__} of {self.guild.name}, length={len(self.logs)}>'
    
class AuditLogIterator(object):
    __slots__=('_data', '_index', 'client', 'guild', 'logs', 'users',
        'webhooks',)
    
    def __init__(self,client,guild,user=None,event=None):
        self.guild=guild
        self._index=0
        
        data = {
            'limit' : 100,
            'before': now_as_id(),
                }
        
        if (user is not None):
            data['user_id']=user.id
        
        if (event is not None):
            data['action_type']=event.value
        
        self._data  = data
        self.client = client
        self.webhooks={}
        self.users  = {}
        self.logs   = []

    async def load_all(self):
        logs    = self.logs
        client  = self.client
        http    = client.http
        data    = self._data
        
        while True:
            if logs:
                data['before']=logs[-1].id
            
            log_data = await http.audit_logs(self.guild.id,data)
            
            try:
                self._process_data(log_data)
            except StopAsyncIteration:
                return
            
            if len(logs)%100:
                return
            
    def transform(self):
        result=object.__new__(AuditLog)
        result.guild=self.guild
        result.webhooks=self.webhooks
        result.users=self.users
        result.logs=self.logs
        return result
    
    def __aiter__(self):
        self._index=0
        return self

    async def __anext__(self):
        ln=len(self.logs)
        index=self._index
        
        if index<ln:
            self._index+=1
            return self.logs[index]
        
        if index%100:
            raise StopAsyncIteration
        
        data=self._data
        if ln:
            data['before']=self.logs[ln-1].id
        
        log_data = await self.client.http.audit_logs(self.guild.id,data)
        self._process_data(log_data)
        self._index+=1
        return self.logs[index]

    def __repr__(self):
        return f'<{self.__class__.__name__} of {self.client.full_name} at {self.guild.name}>'
    
    def _process_data(self,data):
        try:
            log_datas=data['audit_log_entries']
            if not log_datas:
                raise StopAsyncIteration
        except KeyError:
            raise StopAsyncIteration from None

        webhooks=self.webhooks
        try:
            webhooks_data=data['webhook']
        except KeyError:
            pass
        else:
            for webhook_data in webhooks_data:
                webhook=Webhook(webhook_data)
                webhooks[webhook.id]=webhook

        users=self.users
        try:
            users_data=data['users']
        except KeyError:
            pass
        else:
            for user_data in users_data:
                user=User(user_data)
                self.users[user.id]=user

        logs=self.logs
        guild=self.guild
        for log_data in log_datas:
            logs.append(AuditLogEntry(log_data,guild,webhooks,users))

def convert_guild(self,guild,webhooks,users,target_id):
    return guild

def convert_channel(self,guild,webhooks,users,target_id):
    id_=int(target_id)
    try:
        return guild.all_channel[id_]
    except KeyError:
        #what can we do?
        return Unknown('Channel',id_)

def convert_user(self,guild,webhooks,users,target_id):
    # target_id can be Nonefor any reason
    if target_id is None:
        return None
    
    id_=int(target_id)
    try:
        return USERS[id_]
    except KeyError:
        return Unknown('User',id_)

def convert_role(self,guild,webhooks,users,target_id):
    id_=int(target_id)
    try:
        return guild.all_role[id_]
    except KeyError:
        return Unknown('Role',id_)

def convert_invite(self,guild,webhooks,users,target_id):
    #every other data is at #change
    for change in self.changes:
        if change.attr!='code':
            continue
        
        if self.type is AuditLogEvent.INVITE_DELETE:
            code=change.before
        else:
            code=change.after
        break
    
    else:
        code='' #malformed ?
    
    return Unknown('Invite',code)

def convert_webhook(self,guild,webhooks,users,target_id):
    id_=int(target_id)
    try:
        return webhooks[id_]
    except KeyError:
        return Unknown('Webhook',id_)

def convert_emoji(self,guild,webhooks,users,target_id):
    id_=int(target_id)
    try:
        return guild.emojis[id_]
    except KeyError:
        try:
            return EMOJIS[id_]
        except KeyError:
            return Unknown('Emoji',id_)

def convert_message(self,guild,webhooks,users,target_id):
    # TODO: test for bulk, is target_id a list?
    # we wont waste time on message search
    return Unknown('Message',int(target_id))

def convert_integration(self,guild,webhooks,users,target_id):
    # TODO: test, I have no integration to test this endpoint
    id_=int(target_id)
    try:
        return INTEGRATIONS[id_]
    except KeyError:
        return Unknown('Integration',id_)

CONVERSIONS = (
    convert_guild,
    convert_channel,
    convert_user,
    convert_role,
    convert_invite,
    convert_webhook,
    convert_emoji,
    convert_message,
    convert_integration,
        )

del convert_guild
del convert_channel
del convert_user
del convert_role
del convert_invite
del convert_webhook
del convert_emoji
del convert_message
del convert_integration


DETAIL_CONVERSIONS={}

def convert_detail_days(key,value,all_):
    return 'days',int(value)

DETAIL_CONVERSIONS['delete_member_days']=convert_detail_days
del convert_detail_days

def convert_detail_users_removed(key,value,all_):
    return 'users_removed',int(value)
    
DETAIL_CONVERSIONS['members_removed']=convert_detail_users_removed
del convert_detail_users_removed

def convert_detail_channel(key,value,all_):
    channel_id=int(value)
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        channel=Unknown('Channel',channel_id)
    return 'channel',channel
    
DETAIL_CONVERSIONS['channel_id']=convert_detail_channel
del convert_detail_channel

def convert_detail_message(key,value,all_):
    message_id=int(value)
    return 'message',Unknown('Message',message_id)
    
DETAIL_CONVERSIONS['message_id']=convert_detail_message
del convert_detail_message

def convert_detail_amount(key,value,all_):
    return 'amount',int(value)

DETAIL_CONVERSIONS['count']=convert_detail_amount
del convert_detail_amount

def convert_detail_permow_target(key,value,all_):
    id_=int(value)
    try:
        type_name=all_['type']
    except KeyError:
        # broken data
        return None
    
    if type_name=='member':
        try:
            user=USERS[id_]
        except KeyError:
            user=Unknown('User',id_)
        return 'target',user
    
    if type_name=='role':
        try:
            role=ROLES[id_]
        except KeyError:
            name=all_.get('name','')
            role=Unknown('Role',id_,name)
        return 'target',role
    
    # permow type can be only member and role, so if it is else,
    # the data is broken again
    return None

DETAIL_CONVERSIONS['id']=convert_detail_permow_target
del convert_detail_permow_target

def convert_detail_permow_processed(key,value,all_):
    return None

DETAIL_CONVERSIONS['type']=convert_detail_permow_processed
DETAIL_CONVERSIONS['role_name']=convert_detail_permow_processed
del convert_detail_permow_processed

def DETAIL_CONVERTER_DEFAULT(key,value,all_):
    return key,value

class AuditLogEntry(object):
    __slots__=('changes', 'details', 'id', 'reason', 'target', 'type', 'user',)
    def __init__(self,data,guild,webhooks,users):
        self.id=int(data['id'])
        self.type=AuditLogEvent.INSTANCES[int(data['action_type'])]
        try:
            options=data['options']
        except KeyError:
            self.details=None
        else:
            details={}
            self.details=details
            for key,value in options.items():
                result=DETAIL_CONVERSIONS.get(key,DETAIL_CONVERTER_DEFAULT)(key,value,options)
                if result is None:
                    continue
                key,value=result
                details[key]=value
                
        user_id=data.get('user_id',None)
        if user_id is None:
            self.user=None
        else:
            user_id=int(user_id)
            self.user=users[user_id]

        self.reason=data.get('reason',None)
        changes=data.get('changes',None)
        if changes is None:
            self.changes=None
        else:
            transformed_changes=[]
            self.changes=transformed_changes
            for element in changes:
                try:
                    key=element['key']
                except KeyError: #malformed?
                    continue
                try:
                    transformer=TRANSFORMERS[key]
                except KeyError:
                    transformer=transform_nothing
                
                change=transformer(key,element)
                if change is not None:
                    transformed_changes.append(change)
        
        try:
            target_id=data['target_id']
        except KeyError:
            self.target=None
        else:
            self.target=CONVERSIONS[self.type.value//10](self,guild,webhooks,users,target_id)

    @property
    def created_at(self):
        return id_to_time(self.id)
    
    def __repr__(self):
        result = [
            '<',self.__class__.__name__,
            ' id=',repr(self.id),
            ', type=',self.type.name,
                ]
        
        result.append(', user=')
        user=self.user
        if user is None:
            user_repr='None'
        else:
            user_repr=user.full_name
        result.append(user_repr)
        
        result.append(', target=')
        result.append(repr(self.target))
        
        result.append(', change count=')
        changes=self.changes
        if changes is None:
            change_amount_repr='0'
        else:
            change_amount_repr=repr(len(self.changes))
        result.append(change_amount_repr)
        
        reason=self.reason
        if reason is not None:
            result.append(', reason=')
            # use repr to escape special inserted characters
            result.append(repr(reason))
        
        details=self.details
        if details is not None:
            result.append(', details=')
            result.append(repr(details))
        
        result.append('>')
        
        return ''.join(result)
    
def PermOW_from_logs(data):
    self=object.__new__(PermOW)
    id_=int(data['id'])
    if data['type']=='role':
        try:
            self.target=ROLES[id_]
        except KeyError:
            self.target=Unknown('Role',id_)
    else:
        try:
            self.target=USERS[id_]
        except KeyError:
            self.target=Unknown('User',id_)
    
    self.allow=data['allow']
    self.deny=data['deny']

    return self

def transform_nothing(name,data):
    change=AuditLogChange()
    change.attr=name
    change.before=data.get('old_value',None)
    change.after=data.get('new_value',None)
    return change

def transform_avatar(name,data):
    change=AuditLogChange()
    change.attr=name[:-5]

    avatar=data.get('old_value',None)
    if avatar is None:
        avatar=0
        has_animated_avatar=False
    elif avatar.startswith('a_'):
        avatar=int(avatar[2:],16)
        has_animated_avatar=True
    else:
        avatar=int(avatar,16)
        has_animated_avatar=False
    
    change.before=(has_animated_avatar,avatar)
    
    avatar=data.get('new_value',None)
    if avatar is None:
        avatar=0
        has_animated_avatar=False
    elif avatar.startswith('a_'):
        avatar=int(avatar[2:],16)
        has_animated_avatar=True
    else:
        avatar=int(avatar,16)
        has_animated_avatar=False
    
    change.after=(has_animated_avatar,avatar)
    
    return change

def transform_bool__separated(name,data):
    change=AuditLogChange()
    change.attr='separated'
    change.before=data.get('old_value',None)
    change.after=data.get('new_value',None)
    return change

def transform_channel(name,data):
    change=AuditLogChange()
    change.attr=name[:-3]
    value=data.get('old_value',None)
    if value is None:
        change.before=None
    else:
        value=int(value)
        try:
            change.before=CHANNELS[value]
        except KeyError:
            change.before=Unknown('Channel',value)
    value=data.get('new_value',None)
    if value is None:
        change.after=None
    else:
        value=int(value)
        try:
            change.after=CHANNELS[value]
        except KeyError:
            change.after=Unknown('Channel',value)
    return change

def transform_color(name,data):
    change=AuditLogChange()
    change.attr='color'
    value=data.get('old_value',None)
    change.before=None if value is None else Color(value)
    value=data.get('new_value',None)
    change.after=None if value is None else Color(value)
    return change

def transform_content_filter(name,data):
    change=AuditLogChange()
    change.attr='content_filter'
    value=data.get('old_value',None)
    change.before=None if value is None else ContentFilterLevel.INSTANCES[value]
    value=data.get('new_value',None)
    change.after=None if value is None else ContentFilterLevel.INSTANCES[value]
    return change

def transform_int__days(name,data):
    change=AuditLogChange()
    change.attr='days'
    change.before=data.get('old_value',None)
    change.after=data.get('new_value',None)
    return change

def transform_int__slowmode(name,data):
    change=AuditLogChange()
    change.attr='slowmode'
    change.before=data.get('old_value',None)
    change.after=data.get('new_value',None)
    return change

def transform_message_notification(name,data):
    change=AuditLogChange()
    change.attr='message_notification'
    before=data.get('old_value',None)
    change.before=None if before is None else MessageNotificationLevel.INSTANCES[before]
    after=data.get('new_value',None)
    change.after=None if before is None else MessageNotificationLevel.INSTANCES[after]
    return change

def transform_mfa(name,data):
    change=AuditLogChange()
    change.attr='mfa'
    before=data.get('old_value',None)
    change.before=None if before is None else MFA.INSTANCES[before]
    after=data.get('new_value',None)
    change.after=None if before is None else MFA.INSTANCES[after]
    return change

def transform_overwrites(name,data):
    change=AuditLogChange()
    change.attr='overwrites'
    value=data.get('old_value',None)
    change.before=None if value is None else [PermOW_from_logs(ow_data) for ow_data in value]
    value=data.get('new_value',None)
    change.after=None if value is None else [PermOW_from_logs(ow_data) for ow_data in value]
    return change

def transform_permission(name,data):
    change=AuditLogChange()
    change.attr=name
    value=data.get('old_value',None)
    change.before=None if value is None else Permission(value)
    value=data.get('new_value',None)
    change.after=None if value is None else Permission(value)
    return change

def transform_region(name,data):
    change=AuditLogChange()
    change.attr='region'
    before=data.get('old_value',None)
    change.before=None if before is None else VoiceRegion.get(before)
    after=data.get('new_value',None)
    change.after=None if before is None else VoiceRegion.get(after)
    return change

def transform_role(name,data):
    change=AuditLogChange()
    change.attr='role'
    if name=='$add':
        change.before=None
        change.after=roles=[]
    else:
        change.before=roles=[]
        change.after=None

    for element in data['new_value']:
        role_id=int(element['id'])
        try:
            role=ROLES[role_id]
        except KeyError:
            role=Unknown('Role',role_id,element['name'])
        roles.append(role)

    return change

def transform_snowfalke(name,data):
    change=AuditLogChange()
    change.attr=name
    value=data.get('old_value',None)
    change.before=None if value is None else int(value)
    value=data.get('new_value',None)
    change.after=None if value is None else int(value)
    return change

def transform_str__vanity_code(name,data):
    change=AuditLogChange()
    change.attr='vanity_code'
    change.before=data.get('old_value',None)
    change.after=data.get('new_value',None)
    return change

def transform_type(name,data):
    # if we talk about permission overwrite, type can be `str` too,
    # what we ignore
    before=data.get('old_value',None)
    if type(before) is str:
        return
    
    after=data.get('new_value',None)
    if type(after) is str:
        return
    
    change=AuditLogChange()
    change.attr='type'
    change.before=before
    change.after=after
    return change

def transform_user(name,data):
    change=AuditLogChange()
    change.attr=name[:-3]
    value=data.get('old_value',None)
    if value is None:
        change.before=None
    else:
        value=int(value)
        try:
            change.before=USERS[value]
        except KeyError:
            change.before=Unknown('User',value)
    value=data.get('new_value',None)
    if value is None:
        change.after=None
    else:
        value=int(value)
        try:
            change.after=USERS[value]
        except KeyError:
            change.after=Unknown('User',value)
    return change

def transform_verification_level(name,data):
    change=AuditLogChange()
    change.attr='verification_level'
    value=data.get('old_value',None)
    change.before=None if value is None else VerificationLevel.value[value]
    value=data.get('new_value',None)
    change.after=None if value is None else VerificationLevel.value[value]
    return change

TRANSFORMERS = {
    '$add'                  : transform_role,
    '$remove'               : transform_role,
    'account_id'            : transform_snowfalke,
    'afk_channel_id'        : transform_channel,
    'allow'                 : transform_permission,
    'application_id'        : transform_snowfalke,
    'avatar_hash'           : transform_avatar,
    # bitrate (int)
    'channel_id'            : transform_channel,
    # code (str)
    'color'                 : transform_color,
    # deaf (bool)
    'default_message_notifications':transform_message_notification,
    'deny'                  : transform_permission,
    # enable_emoticons (bool)
    # expire_behavior (int)
    # expire_grace_period (int)
    'explicit_content_filter':transform_content_filter,
    'hoist'                 : transform_bool__separated,
    'icon_hash'             : transform_avatar,
    'id'                    : transform_snowfalke,
    'inviter_id'            : transform_user,
    # mentionable (bool)
    # max_age (int)
    # max_uses (int)
    'mfa_level'             : transform_mfa,
    # mute (mute)
    # name (str)
    # nick (str)
    # nsfw (bool)
    'owner_id'              : transform_user,
    # position (int)
    'prune_delete_days'     : transform_int__days,
    'permission_overwrites' : transform_overwrites,
    'permissions'           : transform_permission,
    'rate_limit_per_user'   : transform_int__slowmode,
    'region'                : transform_region,
    'splash_hash'           : transform_avatar,
    'system_channel_id'     : transform_channel,
    # temporary (bool)
    # topic (str)
    'type'                  : transform_type,
    # uses (int)
    'vanity_url_code'       : transform_str__vanity_code,
    'verification_level'    : transform_verification_level,
    'widget_channel_id'     : transform_channel,
    # widget_enabled (bool)
        }

del transform_avatar
del transform_bool__separated
del transform_channel
del transform_color
del transform_content_filter
del transform_int__days
del transform_int__slowmode
del transform_message_notification
del transform_mfa
del transform_overwrites
del transform_permission
del transform_region
del transform_role
del transform_snowfalke
del transform_str__vanity_code
del transform_type
del transform_user
del transform_verification_level


class AuditLogChange(object):
    __slots__=('before', 'after', 'attr',)
    
    def __repr__(self):
        return f'{self.__class__.__name__}(attr=`{self.attr}`, before=`{self.before}`, after=`{self.after}`)'
