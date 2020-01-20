# -*- coding: utf-8 -*-
from email._parseaddr import _parsedate_tz
from datetime import datetime,timedelta,timezone
from time import monotonic

from .futures import Future,PENDING

from .client_core import GC_cycler,CLIENTS
from .py_hdrs import DATE
from .others import Discord_hdrs

RATELIMIT_RESET=Discord_hdrs.RATELIMIT_RESET
RATELIMIT_RESET_AFTER=Discord_hdrs.RATELIMIT_RESET_AFTER
del Discord_hdrs

def GC_handlers(cycler):
    now=monotonic()
    for client in CLIENTS:
        session=client.http
        if session is None:
            continue
        
        handlers=session.locks
        
        collected=[]
        for handler in handlers:
            if handler.future._state is PENDING:
                continue
            if handler.drops_at>now:
                continue
            collected.append(handler)
        
        for handler in collected:
            del handlers[handler]

GC_cycler.append(GC_handlers)

del GC_cycler,GC_handlers
        
#parsing time
#email.utils.parsedate_to_datetime
def parsedate_to_datetime(data):
    *dtuple, tz = _parsedate_tz(data)
    if tz is None:
        return datetime(*dtuple[:6])
    return datetime(*dtuple[:6],tzinfo=timezone(timedelta(seconds=tz)))
        
class ratelimit_handler(object):
    __slots__=('drops_at', 'future', 'group_id', 'limiter_id',)

    def __init__(self,loop,limiter_id,group_id):
        self.future     = Future(loop)
        self.limiter_id = limiter_id
        self.group_id   = group_id
        self.drops_at   = 0.

    @classmethod
    def unlimited(cls,loop):
        self=object.__new__(cls)
        self.future     = Future(loop)
        self.limiter_id = 0
        self.group_id   = 0
        self.drops_at   = 0.
        return self
    
    def __iter__(self):
        future=self.future
        yield from future
        drops_at=self.drops_at
        if drops_at>monotonic():
            future.clear()
            future._loop.call_at(drops_at,future.__class__.set_result_if_pending,future,None)
            yield from future
    
    __await__=__iter__

    def __eq__(self,other):
        return self.limiter_id==other.limiter_id and self.group_id==other.group_id

    def __ne__(self,other):
        return self.limiter_id!=other.limiter_id or self.group_id!=other.group_id

    def __hash__(self):
        return self.group_id+self.limiter_id
        
    def __enter__(self):
        return self

    def __exit__(self,exc_type,exc_val,exc_tb):
        self.future.set_result(None)
        return False

    def set_delay(self,headers):
        delay1=( \
            datetime.fromtimestamp(float(headers[RATELIMIT_RESET]),timezone.utc)
            -parsedate_to_datetime(headers[DATE]) 
                ).total_seconds()
        delay2=float(headers[RATELIMIT_RESET_AFTER])
        self.drops_at=monotonic()+(delay1 if delay1<delay2 else delay2)

    def is_active(self):
        return self.future._state is PENDING or (self.drops_at<=monotonic())

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

GLOBALLY_LIMITED=0x4000000000000000

##INFO : some endpoints might be off 1s
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
##used at : METH_GET guild.embed_url
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
##used at : METH_GET guild.widget_url
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
##used at : relationsip_delete
##limits  : UNTESTED
##
##endpoint: /users/@me/relationships/{user_id}
##method  : PUT
##auth    : user
##used at : relationsip_create
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
##used at : user_get_profile
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
##used at : user_profle
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
