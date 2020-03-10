# -*- coding: utf-8 -*-
from email._parseaddr import _parsedate_tz
from datetime import datetime,timedelta,timezone
from time import monotonic
from collections import deque

from .dereaddons_local import modulize
from .futures import Future, PENDING, Lock

from .client_core import GC_cycler, CLIENTS, KOKORO
from .py_hdrs import DATE
from .others import Discord_hdrs

RATELIMIT_RESET         = Discord_hdrs.RATELIMIT_RESET
RATELIMIT_RESET_AFTER   = Discord_hdrs.RATELIMIT_RESET_AFTER
RATELIMIT_LIMIT         = Discord_hdrs.RATELIMIT_LIMIT

del Discord_hdrs

def GC_handlers(cycler):
    collected=[]
    for client in CLIENTS:
        session=client.http
        
        handlers=session.handlers
        
        for handler in handlers:
            if handler:
                continue
            
            collected.append(handler)
        
        for handler in collected:
            del handlers[handler]
        
        collected.clear()

GC_cycler.append(GC_handlers)

del GC_cycler, GC_handlers

#parsing time
#email.utils.parsedate_to_datetime
def parsedate_to_datetime(data):
    *dtuple, tz = _parsedate_tz(data)
    if tz is None:
        return datetime(*dtuple[:6])
    return datetime(*dtuple[:6],tzinfo=timezone(timedelta(seconds=tz)))

class global_lock_canceller:
    __slots__=('session',)
    def __init__(self,session):
        self.session=session
    def __call__(self,future):
        self.session.global_lock=None
    
def ratelimit_global(session,retry_after):
    future=session.global_lock
    if future is not None:
        return future
    future=Future(session.loop)
    future.add_done_callback(global_lock_canceller(session))
    session.global_lock=future
    future._loop.call_later(retry_after,future.__class__.set_result_if_pending,future,None)
    return future

GLOBALLY_LIMITED = 0x4000000000000000
RATELIMIT_DROP_ROUND = 0.20

class RatelimitGroup(object):
    CHANNEL     = 'channel_id'
    GUILD       = 'guild_id'
    WEBHOOK     = 'webhook_id'
    GLOBAL      = 'global'
    UNLIMITED   = 'unlimited'
    
    __slots__ = ('group_id', 'limiter', 'size', )
    
    __auto_next_id = 105<<8
    __unlimited = None
    
    def __new__(cls, limiter = GLOBAL):
        self = object.__new__(cls)
        self.limiter = limiter
        self.size = 1
        group_id = cls.__auto_next_id
        cls.__auto_next_id = group_id + (7<<8)
        self.group_id = group_id
        return self
    
    @classmethod
    def unlimited(cls):
        self = cls.__unlimited
        if (self is not None):
            return self
        
        self = object.__new__(cls)
        self.size = 0
        self.group_id = 0
        self.limiter = cls.UNLIMITED
        
        cls.__unlimited = self
        return self
    
    def __hash__(self):
        return self.group_id
    
    def __repr__(self):
        result = [
            '<',
            self.__class__.__name__,
            ' size=',
            repr(self.size),
            ', ',
                ]
        
        limiter = self.limiter
        if limiter is self.GLOBAL:
            result.append('limited globally')
        elif limiter is self.UNLIMITED:
            result.append('unlimited')
        else:
            result.append('limited by ')
            result.append(limiter)
        
        result.append('>')
        
        return ''.join(result)

class RatelimitHandler(object):
    __slots__ = ('active', 'drops', 'limiter_id', 'parent', 'queue', 'wakeupper', )
    def __init__(self, parent, limiter_id):
        self.parent     = parent
        self.limiter_id = limiter_id
        self.drops      = []
        self.active     = 0
        self.queue      = deque()
        self.wakeupper  = None
    
    def __repr__(self):
        result = [
            '<',
            self.__class__.__name__,
                ]
        
        limiter = self.parent.limiter
        if limiter is RatelimitGroup.UNLIMITED:
            result.append(' unlimited')
        else:
            result.append(' size: ')
            result.append(repr(self.parent.size))
            result.append(', active: ')
            result.append(repr(self.active))
            result.append(', cooldown drops: ')
            result.append(repr(self.drops))
            result.append(', queue length: ')
            result.append(repr(len(self.queue)))
            
            if limiter is RatelimitGroup.GLOBAL:
                result.append(', limited globally')
            else:
                result.append(', limited by ')
                result.append(limiter)
                result.append(': ')
                result.append(repr(self.limiter_id))
            
            result.append(' group id: ')
            result.append(repr(self.parent.group_id))
            
        result.append('>')
        return ''.join(result)
    
    def __bool__(self):
        if self.active:
            return True
        
        if self.drops:
            return True
        
        if self.queue:
            return True
        
        return False
    
    def __eq__(self,other):
        if self.limiter_id!=other.limiter_id:
            return False
        
        if self.parent.group_id!=other.parent.group_id:
            return False
        
        return True
    
    def __ne__(self,other):
        if self.limiter_id!=other.limiter_id:
            return True
        
        if self.parent.group_id!=other.parent.group_id:
            return True
        
        return False
    
    def __hash__(self):
        return self.parent.group_id+self.limiter_id
    
    async def enter(self):
        size = self.parent.size
        if size == 0:
            return
        
        size = self.parent.size
        active = self.active
        left = size-active
        
        if left <= 0:
            future = Future(KOKORO)
            self.queue.append(future)
            await future
            
            self.active = self.active+1
            return
        
        drops = self.drops
        left = left-len(drops)
        if left > 0:
            self.active = active+1
            return
        
        future = Future(KOKORO)
        self.queue.append(future)
        await future
        
        self.active = self.active+1
    
    def exit(self, headers):
        current_size = self.parent.size
        if current_size==0:
            return
        
        self.active = self.active-1
        
        while True:
            if (headers is not None):
                size = headers.get(RATELIMIT_LIMIT,None)
                if (size is not None):
                    break
            
            wakeupper = self.wakeupper
            if (wakeupper is not None):
                wakeupper.cancel()
                self.wakeupper = None
            
            self.wakeup()
            return
        
        size = int(size)
        self.parent.size = size
        if size > current_size:
            can_free = size-current_size
            queue = self.queue
            queue_ln = len(queue)
            
            if can_free>queue_ln:
                can_free=queue_ln
            
            while can_free>0:
                future = queue.popleft()
                future.set_result(None)
                can_free-=1
                continue
        
        delay1 = (
            datetime.fromtimestamp(float(headers[RATELIMIT_RESET]),timezone.utc)-parsedate_to_datetime(headers[DATE])
                ).total_seconds()
        delay2 = float(headers[RATELIMIT_RESET_AFTER])
        
        if delay1 < delay2:
            delay = delay1
        else:
            delay = delay2
        
        drop = monotonic()+delay
        
        drops = self.drops
        drops.append(drop)
        drops.sort(reverse=True)
        
        wakeupper = self.wakeupper
        if wakeupper is None:
            wakeupper = KOKORO.call_at(drop,type(self).wakeup,self)
            self.wakeupper = wakeupper
            return
        
        if wakeupper.when<=drop:
            return
            
        wakeupper.cancel()
        wakeupper = KOKORO.call_at(drop,type(self).wakeup,self)
        self.wakeupper = wakeupper
    
    def wakeup(self):
        # add some delay, so we wont need to wakeup that much time
        now = monotonic()+RATELIMIT_DROP_ROUND
        
        drops = self.drops
        
        limit = len(drops)-1
        
        while limit>=0:
            drop = drops[limit]
            if drop > now:
                wakeupper = KOKORO.call_at(drop,type(self).wakeup,self)
                self.wakeupper = wakeupper
                break
            
            del drops[-1]
            limit = limit-1
            continue
        else:
            self.wakeupper = None
        
        queue = self.queue
        queue_ln = len(queue)
        if queue_ln == 0:
            return
        
        # if exception occures, nothing is added to self.drops, but active is descreased by one,
        # so lets check active count as well.
        # also the first requests might set self.parent.size as well, to higher than 1 >.>
        can_free = self.parent.size-self.active-len(drops)
        
        if can_free > queue_ln:
            can_free = queue_ln
        
        while can_free>0:
            future = queue.popleft()
            future.set_result(None)
            can_free-=1
            continue
    
    def ctx(self):
        return RatelimitHandlerCTX(self)

class RatelimitHandlerCTX(object):
    __slots__ = ('parent', 'exited', )
    def __init__(self,parent):
        self.parent = parent
        self.exited = False
    
    def exit(self, headers):
        self.exited = True
        self.parent.exit(headers)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.exited:
            return
        
        self.exited = True
        self.parent.exit(None)

@modulize
class RATELIMIT_GROUPS:
    GROUP_REACTION_MODIFY       = RatelimitGroup(RatelimitGroup.CHANNEL)
    GROUP_PIN_MODIFY            = RatelimitGroup(RatelimitGroup.CHANNEL)
    GROUP_USER_MODIFY           = RatelimitGroup(RatelimitGroup.GUILD) # both has the same endpoint
    GROUP_USER_ROLE_MODIFY      = RatelimitGroup(RatelimitGroup.GUILD)
    
    oauth2_token                = RatelimitGroup.unlimited()
    application_get             = RatelimitGroup() # untested
    achievement_get_all         = RatelimitGroup()
    achievement_create          = RatelimitGroup()
    achievement_delete          = RatelimitGroup()
    achievement_get             = RatelimitGroup()
    achievement_edit            = RatelimitGroup()
    client_logout               = RatelimitGroup() # untested
    channel_delete              = RatelimitGroup.unlimited()
    channel_group_leave         = RatelimitGroup() # untested; same as channel_delete?
    channel_edit                = RatelimitGroup.unlimited()
    channel_group_edit          = RatelimitGroup() # untested; same as channel_edit?
    channel_follow              = RatelimitGroup.unlimited()
    invite_get_channel          = RatelimitGroup.unlimited()
    invite_create               = RatelimitGroup()
    message_logs                = RatelimitGroup.unlimited()
    message_create              = RatelimitGroup(RatelimitGroup.CHANNEL)
    message_delete_multiple     = RatelimitGroup(RatelimitGroup.CHANNEL)
    message_delete              = RatelimitGroup(RatelimitGroup.CHANNEL)
    message_delete_b2wo         = RatelimitGroup(RatelimitGroup.CHANNEL)
    message_get                 = RatelimitGroup.unlimited()
    message_edit                = RatelimitGroup(RatelimitGroup.CHANNEL)
    message_mar                 = RatelimitGroup() # untested
    reaction_clear              = GROUP_REACTION_MODIFY
    reaction_delete_emoji       = GROUP_REACTION_MODIFY
    reaction_users              = RatelimitGroup.unlimited()
    reaction_delete_own         = GROUP_REACTION_MODIFY
    reaction_add                = GROUP_REACTION_MODIFY
    reaction_delete             = GROUP_REACTION_MODIFY
    message_suppress_embeds     = RatelimitGroup()
    permission_ow_delete        = RatelimitGroup.unlimited()
    permission_ow_create        = RatelimitGroup.unlimited()
    channel_pins                = RatelimitGroup()
    message_unpin               = GROUP_PIN_MODIFY
    message_pin                 = GROUP_PIN_MODIFY
    channel_group_user_delete   = RatelimitGroup() # untested
    channel_group_user_add      = RatelimitGroup() # untested
    typing                      = RatelimitGroup(RatelimitGroup.CHANNEL)
    webhook_get_channel         = RatelimitGroup.unlimited()
    webhook_create              = RatelimitGroup.unlimited()
    client_gateway_hooman       = RatelimitGroup() # untested
    client_gateway_bot          = RatelimitGroup()
    guild_create                = RatelimitGroup.unlimited()
    guild_delete                = RatelimitGroup.unlimited()
    guild_get                   = RatelimitGroup.unlimited()
    guild_edit                  = RatelimitGroup.unlimited()
    guild_mar                   = RatelimitGroup() # untested
    audit_logs                  = RatelimitGroup.unlimited()
    guild_bans                  = RatelimitGroup.unlimited()
    guild_ban_delete            = RatelimitGroup.unlimited()
    guild_ban_get               = RatelimitGroup.unlimited()
    guild_ban_add               = RatelimitGroup.unlimited()
    guild_channels              = RatelimitGroup.unlimited()
    channel_move                = RatelimitGroup.unlimited()
    channel_create              = RatelimitGroup.unlimited()
    guild_embed_get             = RatelimitGroup.unlimited()
    guild_embed_edit            = RatelimitGroup.unlimited()
    guild_emojis                = RatelimitGroup.unlimited()
    emoji_create                = RatelimitGroup(RatelimitGroup.GUILD)
    emoji_delete                = RatelimitGroup(RatelimitGroup.GUILD)
    emoji_get                   = RatelimitGroup.unlimited()
    emoji_edit                  = RatelimitGroup()
    integration_get_all         = RatelimitGroup() # untested
    integration_create          = RatelimitGroup() # untested
    integration_delete          = RatelimitGroup() # untested
    integration_edit            = RatelimitGroup() # untested
    integration_sync            = RatelimitGroup() # untested
    invite_get_guild            = RatelimitGroup.unlimited()
    guild_users                 = RatelimitGroup(RatelimitGroup.GUILD)
    client_edit_nick            = RatelimitGroup()
    guild_user_delete           = RatelimitGroup(RatelimitGroup.GUILD)
    guild_user_get              = RatelimitGroup()
    user_edit                   = GROUP_USER_MODIFY
    user_move                   = GROUP_USER_MODIFY
    guild_user_add              = RatelimitGroup(RatelimitGroup.GUILD)
    user_role_delete            = GROUP_USER_ROLE_MODIFY
    user_role_add               = GROUP_USER_ROLE_MODIFY
    guild_preview               = RatelimitGroup()
    guild_prune_estimate        = RatelimitGroup.unlimited()
    guild_prune                 = RatelimitGroup.unlimited()
    guild_regions               = RatelimitGroup.unlimited()
    guild_roles                 = RatelimitGroup.unlimited()
    role_move                   = RatelimitGroup.unlimited()
    role_create                 = RatelimitGroup.unlimited()
    role_delete                 = RatelimitGroup.unlimited()
    role_edit                   = RatelimitGroup.unlimited()
    vanity_get                  = RatelimitGroup.unlimited()
    vanity_edit                 = RatelimitGroup.unlimited() # untested
    webhook_get_guild           = RatelimitGroup.unlimited()
    guild_widget_get            = RatelimitGroup.unlimited()
    hypesquad_house_leave       = RatelimitGroup() # untested
    hypesquad_house_change      = RatelimitGroup() # untested
    invite_delete               = RatelimitGroup.unlimited()
    invite_get                  = RatelimitGroup()
    client_application_info     = RatelimitGroup.unlimited()
    user_info                   = RatelimitGroup.unlimited()
    client_user                 = RatelimitGroup.unlimited()
    client_edit                 = RatelimitGroup()
    user_achievements           = RatelimitGroup() # untested; has expected global ratelimit
    user_achievement_update     = RatelimitGroup()
    channel_private_get_all     = RatelimitGroup.unlimited()
    channel_private_create      = RatelimitGroup.unlimited()
    client_connections          = RatelimitGroup.unlimited()
    user_connections            = RatelimitGroup.unlimited()
    guild_get_all               = RatelimitGroup()
    user_guilds                 = RatelimitGroup()
    guild_leave                 = RatelimitGroup.unlimited()
    relationship_friend_request = RatelimitGroup() # untested
    relationship_delete         = RatelimitGroup() # untested
    relationship_create         = RatelimitGroup() # untested
    client_get_settings         = RatelimitGroup() # untested
    client_edit_settings        = RatelimitGroup() # untested
    user_get                    = RatelimitGroup() # untested
    channel_group_create        = RatelimitGroup() # untested
    user_get_profile            = RatelimitGroup() # untested
    webhook_delete              = RatelimitGroup.unlimited()
    webhook_get                 = RatelimitGroup.unlimited()
    webhook_edit                = RatelimitGroup.unlimited()
    webhook_delete_token        = RatelimitGroup.unlimited()
    webhook_get_token           = RatelimitGroup.unlimited()
    webhook_edit_token          = RatelimitGroup.unlimited()
    webhook_send                = RatelimitGroup(RatelimitGroup.WEBHOOK)

##INFO :
##    some endpoints might be off 1s
##    groups are not accurate now, because we use autogroups
##    last group id: 89600
##
##endpoint: https://cdn.discordapp.com/
##method  : GET
##auth    : none
##used at :
##limits  : unlimited
##
##endpoint: oauth2/token
##method  : POST
##auth    : application
##used at : oauth2_token
##limits  : unlimited
##
##endpoint: /applications/{application_id}
##method  : GET
##auth    : user
##used at : application_get
##limits  : UNTESTED
##
##endpoint: /applications/{application_id}/achievements
##method  : GET
##auth    : bot
##used at : achievement_get_all
##limits  :
##    group   : 75264
##    limit   : 5
##    reset   : 5
##    limiter : GLOBAL
##
##endpoint: /applications/{application_id}/achievements
##method  : POST
##auth    : bot
##used at : achievement_create
##limits  :
##    group   : 78848
##    limit   : 5
##    reset   : 5
##    limiter : GLOBAL
##
##endpoint: /applications/{application_id}/achievements/{achievement_id}
##method  : DELETE
##auth    : bot
##used at : achievement_delete
##limits  :
##    group   : 82432
##    limit   : 5
##    reset   : 5
##    limiter : GLOBAL
##
##endpoint: /applications/{application_id}/achievements/{achievement_id}
##method  : GET
##auth    : bot
##used at : achievement_get
##limits  :
##    group   : 77056
##    limit   : 5
##    reset   : 5
##    limiter : GLOBAL
##
##endpoint: /applications/{application_id}/achievements/{achievement_id}
##method  : PATCH
##auth    : bot
##used at : achievement_edit
##limits  :
##    group   : 80640
##    limit   : 5
##    reset   : 5
##    limiter : GLOBAL
##
##endpoint: /auth/logout
##method  : POST
##auth    : user
##used at : client_logout
##limits  : UNTESTED
##
##endpoint: /channels/{channel_id}
##method  : DELETE
##auth    : bot
##used at : channel_delete
##limits  : unlimited
##
##endpoint: /channels/{channel_id}
##method  : DELETE
##auth    : user
##used at : channel_group_leave
##limits  : UNTESTED
##
##endpoint: /channels/{channel_id}
##method  : PATCH
##auth    : bot
##used at : channel_edit
##limits  : unlimited
##
##endpoint: /channels/{channel_id}
##method  : PATCH
##auth    : user
##used at : channel_group_edit
##limits  : UNTESTED
##
##endpoint: /channels/{channel_id}/followers
##method  : POT
##auth    : bot
##used at : channel_follow
##limits  : unlimited
##
##endpoint: /channels/{channel_id}/invites
##method  : GET
##auth    : bot
##used at : invite_get_channel
##limits  : unlimited
##
##endpoint: /channels/{channel_id}/invites
##method  : POST
##auth    : bot
##used at : invite_create
##limits  :
##    group   : 39424
##    limit   : 5
##    reset   : 15
##    limiter : GLOBAL
##
##endpoint: /channels/{channel_id}/messages
##method  : GET
##auth    : bot
##used at : message_logs
##limits  : unlimited
##
##endpoint: /channels/{channel_id}/messages
##method  : POST
##auth    : bot
##used at : message_create
##limits  :
##    group   : 28672
##    limit   : 5
##    reset   : 4
##    limiter : channel_id
##
##endpoint: /channels/{channel_id}/messages/bulk_delete
##method  : POST
##auth    : bot
##used at : message_delete_multiple
##limits  :
##    group   : 30464
##    limit   : 1
##    reset   : 3
##    limiter : channel_id
##
##endpoint: /channels/{channel_id}/messages/{message_id}
##method  : DELETE
##auth    : bot
##used at : message_delete / message_delete_b2wo
##limits  : `newer than 14 days` or `own` / `else`
##    group   : 71680 / 87808
##    limit   : 3 / 30
##    reset   : 1 / 120
##    limiter : channel_id
##comment :
##    For newer messages ratelimit is not every time included, but we ll ignore
##    those, because we cannot detect, at which cases ar those applied.
##
##endpoint: /channels/{channel_id}/messages/{message_id}
##method  : GET
##auth    : bot
##used at : message_get
##limits  : unlimited
##
##endpoint: /channels/{channel_id}/messages/{message_id}
##method  : PATCH
##auth    : bot
##used at : message_edit
##limits  :
##    group   : 32256
##    limit   : 5
##    reset   : 4
##    limiter : channel_id
##
##endpoint: /channels/{channel_id}/messages/{message_id}/ack
##method  : POST
##auth    : user
##used at : message_mar
##limits  : UNTESTED
##
##endpoint: /channels/{channel_id}/messages/{message_id}/reactions
##method  : DELETE
##auth    : bot
##used at : reaction_clear
##limits  :
##    group   : 26880
##    limit   : 1
##    reset   : 0.25
##    limiter : channel_id
##
##endpoint: /channels/{channel_id}/messages/{message_id}/reactions/{reaction}
##method  : DELETE
##auth    : bot
##used at : reaction_delete_emoji
##limits  :
##    group   : 26880
##    limit   : 1
##    reset   : 0.25
##    limiter : channel_id
##
##endpoint: /channels/{channel_id}/messages/{message_id}/reactions/{reaction}
##method  : GET
##auth    : bot
##used at : reaction_users
##limits  : unlimited
##
##endpoint: /channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me
##method  : DELETE
##auth    : bot
##used at : reaction_delete_own
##limits  :
##    group   : 26880
##    limit   : 1
##    reset   : 0.25
##    limiter : channel_id
##
##endpoint: /channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me
##method  : PUT
##auth    : bot
##used at : reaction_add
##limits  :
##    group   : 26880
##    limit   : 1
##    reset   : 0.25
##    limiter : channel_id
##
##endpoint: /channels/{channel_id}/messages/{message_id}/reactions/{reaction}/{user_id}
##method  : DELETE
##auth    : bot
##used at : reaction_delete
##limits  :
##    group   : 26880
##    limit   : 1
##    reset   : 0.25
##    limiter : channel_id
##
##endpoint: /channels/{channel_id}/messages/{message_id}/suppress-embeds
##method  : POST
##auth    : bot
##used at : message_suppress_embeds
##limits  :
##    group   : 73472
##    limit   : 3
##    reset   : 1
##    limiter : GLOBAL
##
##endpoint: /channels/{channel_id}/permissions/{overwrite_id}
##method  : DELETE
##auth    : bot
##used at : permission_ow_delete
##limits  : unlimited
##
##endpoint: /channels/{channel_id}/permissions/{overwrite_id}
##method  : PUT
##auth    : bot
##used at : permission_ow_create
##limits  : unlimited
##
##endpoint: /channels/{channel_id}/pins
##method  : PUT
##auth    : bot
##used at : channel_pins
##limits  :
##    group   : 35840
##    limit   : 1
##    reset   : 5
##    limiter : GLOBAL
##
##endpoint: /channels/{channel_id}/pins/{message_id}
##method  : DELETE
##auth    : bot
##used at : message_unpin
##limits  :
##    group   : 34048
##    limit   : 5
##    reset   : 4
##    limiter : channel_id
##
##endpoint: /channels/{channel_id}/pins/{message_id}
##method  : PUT
##auth    : bot
##used at : message_pin
##limits  :
##    group   : 34048
##    limit   : 5
##    reset   : 4
##    limiter : channel_id
##
##endpoint: /channels/{channel_id}/recipients/{user_id}
##method  : DELETE
##auth    : user
##used at : channel_group_user_delete
##limits  : UNTESTED
##
##endpoint: /channels/{channel_id}/recipients/{user_id}
##method  : PUT
##auth    : user
##used at : channel_group_user_add
##limits  : UNTESTED
##
##endpoint: /channels/{channel_id}/typing
##method  : POST
##auth    : bot
##used at : typing
##limits  :
##    group   : 37632
##    limit   : 5
##    reset   : 5
##    limiter : channel_id
##
##endpoint: /channels/{channel_id}/webhooks
##method  : GET
##auth    : bot
##used at : webhook_get_channel
##limits  : unlimited
##
##endpoint: /channels/{channel_id}/webhooks
##method  : POST
##auth    : bot
##used at : webhook_create
##limits  : unlimited
##
##endpoint: /gateway
##method  : GET
##auth    : user
##used at : client_gateway_hooman
##limits  : UNTESTED
##
##endpoint: /gateway/bot
##method  : GET
##auth    : bot
##used at : client_gateway_bot
##limits  :
##    group   : 41216
##    limit   : 2
##    reset   : 5
##    limiter : GLOBAL
##
##endpoint: /guilds
##method  : POST
##auth    : bot
##used at : guild_create
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}
##method  : DELETE
##auth    : bot
##used at : guild_delete
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}
##method  : GET
##auth    : bot
##used at : guild_get
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}
##method  : PATCH
##auth    : bot
##used at : guild_edit
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/ack
##method  : POST
##auth    : user
##used at : guild_mar
##limits  : UNTESTED
##
##endpoint: /guilds/{guild_id}/audit-logs
##method  : GET
##auth    : bot
##used at : audit_logs
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/bans
##method  : GET
##auth    : bot
##used at : guild_bans
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/bans/{user_id}
##method  : DELETE
##auth    : bot
##used at : guild_ban_delete
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/bans/{user_id}
##method  : GET
##auth    : bot
##used at : guild_ban_get
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/bans/{user_id}
##method  : PUT
##auth    : bot
##used at : guild_ban_add
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/channels
##method  : GET
##auth    : bot
##used at : guild_channels
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/channels
##method  : PATCH
##auth    : bot
##used at : channel_move
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/channels
##method  : POST
##auth    : bot
##used at : channel_create
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/embed
##method  : GET
##auth    : bot
##used at : guild_embed_get
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/embed
##method  : PATCH
##auth    : bot
##used at : guild_embed_edit
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/embed.png
##method  : GET
##auth    : none
##used at : guild.embed_url
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/emojis
##method  : GET
##auth    : bot
##used at : guild_emojis
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/emojis
##method  : POST
##auth    : bot
##used at : emoji_create
##limits  :
##    group   : 43008
##    limit   : 50
##    reset   : 3600
##    limiter : guild_id
##
##endpoint: /guilds/{guild_id}/emojis/{emoji_id}
##method  : DELETE
##auth    : bot
##used at : emoji_delete
##limits  :
##    group   : 44800
##    limit   : 1
##    reset   : 3
##    limiter : GLOBAL
##
##endpoint: /guilds/{guild_id}/emojis/{emoji_id}
##method  : GET
##auth    : bot
##used at : emoji_get
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/emojis/{emoji_id}
##method  : PATCH
##auth    : bot
##used at : emoji_edit
##limits  :
##    group   : 46592
##    limit   : 1
##    reset   : 3
##    limiter : GLOBAL
##
##endpoint: /guilds/{guild_id}/integrations
##method  : GET
##auth    : bot
##used at : integration_get_all
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/integrations
##method  : POST
##auth    : bot
##used at : integration_create
##limits  : UNTESTED
##
##endpoint: /guilds/{guild_id}/integrations/{integration_id}
##method  : DELETE
##auth    : bot
##used at : integration_delete
##limits  : UNTESTED
##
##endpoint: /guilds/{guild_id}/integrations/{integration_id}
##method  : PATCH
##auth    : bot
##used at : integration_edit
##limits  : UNTESTED
##
##endpoint: /guilds/{guild_id}/integrations/{integration_id}/sync
##method  : POST
##auth    : bot
##used at : integration_sync
##limits  : UNTESTED
##
##endpoint: /guilds/{guild_id}/invites
##method  : GET
##auth    : bot
##used at : invite_get_guild
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/members
##method  : GET
##auth    : bot
##used at : guild_users
##limits  :
##    group   : 68096
##    limit   : 10
##    reset   : 10
##    limiter : guild_id
##
##endpoint: /guilds/{guild_id}/members/@me/nick
##method  : PATCH
##auth    : bot
##used at : client_edit_nick
##limits  :
##    group   : 48384
##    limit   : 1
##    reset   : 2
##    limiter : GLOBAL
##
##endpoint: /guilds/{guild_id}/members/{user_id}
##method  : DELETE
##auth    : bot
##used at : guild_user_delete
##limits  :
##    group   : 50176
##    limit   : 5
##    reset   : 2
##    limiter : guild_id
##
##endpoint: /guilds/{guild_id}/members/{user_id}
##method  : GET
##auth    : bot
##used at : guild_user_get
##limits  :
##    group   : 69888
##    limit   : 5
##    reset   : 2
##    limiter : GLOBAL
##
##endpoint: /guilds/{guild_id}/members/{user_id}
##method  : PATCH
##auth    : bot
##used at : user_edit, user_move
##limits  :
##    group   : 51968
##    limit   : 10
##    reset   : 10
##    limiter : guild_id
##
##endpoint: /guilds/{guild_id}/members/{user_id}
##method  : PUT
##auth    : bot
##used at : guild_user_add
##limits  :
##    group   : 53760
##    limit   : 10
##    reset   : 10
##    limiter : guild_id
##
##endpoint: /guilds/{guild_id}/members/{user_id}/roles/{role_id}
##method  : DELETE
##auth    : bot
##used at : user_role_delete
##limits  :
##    group   : 55552
##    limit   : 10
##    reset   : 10
##    limiter : guild_id
##
##endpoint: /guilds/{guild_id}/members/{user_id}/roles/{role_id}
##method  : PUT
##auth    : bot
##used at : user_role_add
##limits  :
##    group   : 55552
##    limit   : 10
##    reset   : 10
##    limiter : guild_id
##
##endpoint: /guilds/{guild_id}/preview
##method  : GET
##auth    : bot
##used at : guild_preview
##limits   :
##    group   : 89600
##    limit   : 5
##    reset   : 5
##    limiter : GLOBAL
##
##endpoint: /guilds/{guild_id}/prune
##method  : GET
##auth    : bot
##used at : guild_prune_estimate
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/prune
##method  : POST
##auth    : bot
##used at : guild_prune
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/regions
##method  : GET
##auth    : bot
##used at : guild_regions
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/roles
##method  : GET
##auth    : bot
##used at : guild_roles
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/roles
##method  : PATCH
##auth    : bot
##used at : role_move
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/roles
##method  : POST
##auth    : bot
##used at : role_create
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/roles/{role_id}
##method  : DELETE
##auth    : bot
##used at : role_delete
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/roles/{role_id}
##method  : PATCH
##auth    : bot
##used at : role_edit
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/vanity-url
##method  : GET
##auth    : bot
##used at : vanity_get
##limits  : UNTESTED
##
##endpoint: /guilds/{guild_id}/vanity-url
##method  : PATCH
##auth    : bot
##used at : vanity_edit
##limits  : UNTESTED
##
##endpoint: /guilds/{guild_id}/webhooks
##method  : GET
##auth    : bot
##used at : webhook_get_guild
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/widget.json
##method  : GET
##auth    : none
##used at : guild_widget_get
##limits  : unlimited
##
##endpoint: /guilds/{guild_id}/widget.png
##method  : GET
##auth    : none
##used at : guild.widget_url
##limits  : unlimited
##
##endpoint: /hypesquad/online
##method  : DELETE
##auth    : user
##used at : hypesquad_house_leave
##limits  : UNTESTED
##
##endpoint: /hypesquad/online
##method  : POST
##auth    : user
##used at : hypesquad_house_change
##limits  : UNTESTED
##
##endpoint: /invites/{invite_code}
##method  : DELETE
##auth    : bot
##used at : invite_delete
##limits  : unlimited
##
##endpoint: /invites/{invite_code}
##method  : GET
##auth    : bot
##used at : invite_get
##limits  :
##    group   : 57344
##    limit   : 250
##    reset   : 6
##    limiter : GLOBAL
##
##endpoint: /oauth2/applications/@me
##method  : GET
##auth    : bot
##used at : client_application_info
##limits  : unlimited
##
##endpoint: /users/@me
##method  : GET
##auth    : bearer
##used at : user_info
##limits  : unlimited
##
##endpoint: /users/@me
##method  : GET
##auth    : bot
##used at : client_user
##limits  : unlimited
##
##endpoint: /users/@me
##method  : PATCH
##auth    : bot
##used at : client_edit
##limits  :
##    group   : 59136
##    limit   : 2
##    reset   : 3600
##    limiter : GLOBAL
##
##endpoint: /users/@me/applications/{application_id}/achievements
##method  : GET
##auth    : bearer
##used at : user_achievements
##limits  : UNTESTED
##    group   : 84224
##    limit   : 2
##    reset   : 5
##    limiter : GLOBAL
##
##endpoint: /users/{user_id}/applications/{application_id}/achievements/{achievement_id}
##method  : PUT
##auth    : bot
##used at : user_achievement_update
##limits  :
##    group   : 86016
##    limit   : 5
##    reset   : 5
##    limiter : GLOBAL
##
##endpoint: /users/@me/channels
##method  : GET
##auth    : bot
##used at : channel_private_get_all
##limits  : unlimited
##
##endpoint: /users/@me/channels
##method  : POST
##auth    : bot
##used at : channel_private_create
##limits  : unlimited
##
##endpoint: /users/@me/connections
##method  : GET
##auth    : bot
##used at : client_connections
##limits  : unlimited
##
##endpoint: /users/@me/connections
##method  : GET
##auth    : bearer
##used at : user_connections
##limits  : unlimited
##
##endpoint: /users/@me/guilds
##method  : GET
##auth    : bot
##used at : guild_get_all
##limits  :
##    group   : 62720
##    limit   : 1
##    reset   : 1
##    limiter : GLOBAL
##
##endpoint: /users/@me/guilds
##method  : GET
##auth    : bearer
##used at : user_guilds
##limits  :
##    group   : 60928
##    limit   : 1
##    reset   : 1
##    limiter : GLOBAL
##
##endpoint: /users/@me/guilds/{guild_id}
##method  : DELETE
##auth    : bot
##used at : guild_leave
##limits  : unlimited
##
##endpoint: /users/@me/relationships
##method  : POST
##auth    : user
##used at : relationship_friend_request
##limits  : UNTESTED
##
##endpoint: /users/@me/relationships/{user_id}
##method  : DELETE
##auth    : user
##used at : relationship_delete
##limits  : UNTESTED
##
##endpoint: /users/@me/relationships/{user_id}
##method  : PUT
##auth    : user
##used at : relationship_create
##limits  : UNTESTED
##
##endpoint: /users/@me/settings
##method  : GET
##auth    : user
##used at : client_get_settings
##limits  : UNTESTED
##
##endpoint: /users/@me/settings
##method  : PATCH
##auth    : user
##used at : client_edit_settings
##limits  : UNTESTED
##
##endpoint: /users/{user_id}
##method  : GET
##auth    : bot
##used at : user_get
##limits  :
##    group   : 64512
##    limit   : 30
##    reset   : 30
##    limiter : GLOBAL
##
##endpoint: /users/{user_id}/channels
##method  : POST
##auth    : user
##used at : channel_group_create
##limits  : UNTESTED
##
##endpoint: /users/{user_id}/profile
##method  : GET
##auth    : user
##used at : user_get_profle
##limits  : UNTESTED
##
##endpoint: /webhooks/{webhook_id}
##method  : DELETE
##auth    : bot
##used at : webhook_delete
##limits  : unlimited
##
##endpoint: /webhooks/{webhook_id}
##method  : GET
##auth    : bot
##used at : webhook_get
##limits  : unlimited
##
##endpoint: /webhooks/{webhook_id}
##method  : PATCH
##auth    : bot
##used at : webhook_edit
##limits  : unlimited
##
##endpoint: webhooks/{webhook_id}/{webhook_token}
##method  : DELETE
##auth    : none
##used at : webhook_delete_token
##limits  : unlimited
##
##endpoint: webhooks/{webhook_id}/{webhook_token}
##method  : GET
##auth    : none
##used at : webhook_get_token
##limits  : unlimited
##
##endpoint: webhooks/{webhook_id}/{webhook_token}
##method  : PATCH
##auth    : none
##used at : webhook_edit_token
##limits  : unlimited
##
##endpoint: webhooks/{webhook_id}/{webhook_token}
##method  : POST
##auth    : none
##used at : webhook_send
##limits  :
##    group   : 66304
##    limit   : 5
##    reset   : 2
##    limiter : webhook_id
