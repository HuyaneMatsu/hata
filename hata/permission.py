# -*- coding: utf-8 -*-
__all__ = ('PERM_KEYS', 'Permission', )

PERM_KEYS = {
    'create_instant_invite' :  0,
    'kick_users'            :  1,
    'ban_users'             :  2,
    'administrator'         :  3,
    'manage_channel'        :  4,
    'manage_guild'          :  5,
    'add_reactions'         :  6,
    'view_audit_log'        :  7,
    'priority_speaker'      :  8,
    'stream'                :  9,
    'view_channel'          : 10,
    'send_messages'         : 11,
    'send_tts_messages'     : 12,
    'manage_messages'       : 13,
    'embed_links'           : 14,
    'attach_files'          : 15,
    'read_message_history'  : 16,
    'mention_everyone'      : 17,
    'use_external_emojis'   : 18,
    'view_guild_insights'   : 19,
    'connect'               : 20,
    'speak'                 : 21,
    'mute_users'            : 22,
    'deafen_users'          : 23,
    'move_users'            : 24,
    'use_voice_activation'  : 25,
    'change_nickname'       : 26,
    'manage_nicknames'      : 27,
    'manage_roles'          : 28,
    'manage_webhooks'       : 29,
    'manage_emojis'         : 30,
    #'unused'               : 31,
    #rest is unused
        }
    
class Permission(int):

    def __repr__(self):
        return f'{self.__class__.__name__}({self!s})'
        
    def __getitem__(self,key):
        return (self>>PERM_KEYS[key])&1

    def keys(self):
        for key,position in PERM_KEYS.items():
            if (self>>position)&1:
                yield key

    __iter__=keys

    def values(self):
        for position in PERM_KEYS.values():
            if (self>>position)&1:
                yield position

    def items(self):
        for key,index in PERM_KEYS.items():
            yield key,(self>>index)&1

    def __contains__(self,key):
        try:
            position=PERM_KEYS[key]
        except KeyError:
            return 0
        return (self>>position)&1
    
    #Returns True if self has the same or fewer permissions than other.
    def is_subset(self,other):
       return (self&other)==self

    #Returns True if self has the same or more permissions than other.
    def is_superset(self,other):
        return (self|other)==self

    #Returns True if the permissions on other are a strict subset of those on self.
    def is_strict_subset(self,other):
        return self!=other and (self&other)==self

    #Returns True if the permissions on other are a strict superset of those on self.
    def is_strict_superset(self,other):
        return self!=other and (self|other)==self

    __ge__ = is_superset
    __gt__ = is_strict_superset
    __lt__ = is_strict_subset
    __le__ = is_subset

    # Allows you to update more with 1 call
    def update_by_keys(self,**kwargs):
        new=self
        for key,value in kwargs.items():
            try:
                position=PERM_KEYS[key]
            except KeyError as err:
                err.args=(f'Invalid key:\'{key}\'',)
                raise

            if value:
                new=new|(1<<position)
            else:
                new=new&(0b11111111111111111111111111111111^(1<<position))

        return type(self)(new)

    def handle_overwrite(self,allow,deny):
        #1st denies permissions, then allows
        return type(self)((self&~deny)|allow)

    #0
    @property
    def can_create_instant_invite(self):
        return self&1
    def allow_create_instant_invite(self):
        return type(self)(self|0b00000000000000000000000000000001)
    def deny_create_instant_invite(self):
        return type(self)(self&0b11111111111111111111111111111110)
   
    #1
    @property
    def can_kick_users(self):
        return (self>>1)&1
    def allow_kick_users(self):
        return type(self)(self|0b00000000000000000000000000000010)
    def deny_kick_users(self):
        return type(self)(self&0b11111111111111111111111111111101)

    #2
    @property
    def can_ban_users(self):
        return (self>>2)&1
    def allow_ban_users(self):
        return type(self)(self|0b00000000000000000000000000000100)
    def deny_ban_users(self):
        return type(self)(self&0b11111111111111111111111111111011)

    #3
    @property
    def can_administrator(self):
        return (self>>3)&1
    def allow_administrator(self):
        return type(self)(self|0b00000000000000000000000000001000)
    def deny_administrator(self):
        return type(self)(self&0b11111111111111111111111111110111)

    #4
    @property
    def can_manage_channel(self):
        return (self>>4)&1
    def allow_manage_channel(self):
        return type(self)(self|0b00000000000000000000000000010000)
    def deny_manage_channel(self):
        return type(self)(self&0b11111111111111111111111111101111)

    #5
    @property
    def can_manage_guild(self):
        return (self>>5)&1
    def allow_manage_guild(self):
        return type(self)(self|0b00000000000000000000000000100000)
    def deny_manage_guild(self):
        return type(self)(self&0b11111111111111111111111111011111)

    #6
    @property
    def can_add_reactions(self):
        return (self>>6)&1
    def allow_add_reactions(self):
        return type(self)(self|0b00000000000000000000000001000000)
    def deny_add_reactions(self):
        return type(self)(self&0b11111111111111111111111110111111)

    #7
    @property
    def can_view_audit_log(self):
        return (self>>7)&1
    def allow_view_audit_log(self):
        return type(self)(self|0b00000000000000000000000010000000)
    def deny_view_audit_log(self):
        return type(self)(self&0b11111111111111111111111101111111)
    
    #8
    @property
    def can_priority_speaker(self):
        return (self>>8)&1
    def allow_priority_speaker(self):
        return type(self)(self|0b00000000000000000000000100000000)
    def deny_priority_speaker(self):
        return type(self)(self&0b11111111111111111111111011111111)

    #9
    @property
    def can_stream(self):
        return (self>>9)&1
    def allow_stream(self):
        return type(self)(self|0b00000000000000000000001000000000)
    def deny_stream(self):
        return type(self)(self&0b11111111111111111111110111111111)

    #10
    @property
    def can_view_channel(self):
        return (self>>10)&1
    def allow_view_channel(self):
        return type(self)(self|0b00000000000000000000010000000000)
    def deny_view_channel(self):
        return type(self)(self&0b11111111111111111111101111111111)
    
    #11
    @property
    def can_send_messages(self):
        return (self>>11)&1
    def allow_send_messages(self):
        return type(self)(self|0b00000000000000000000100000000000)
    def deny_send_messages(self):
        return type(self)(self&0b11111111111111111111011111111111)
    
    #12
    @property
    def can_send_tts_messages(self):
        return (self>>12)&1
    def allow_send_tts_messages(self):
        return type(self)(self|0b00000000000000000001000000000000)
    def deny_send_tts_messages(self):
        return type(self)(self&0b11111111111111111110111111111111)
    
    #13
    @property
    def can_manage_messages(self):
        return (self>>13)&1
    def allow_manage_messages(self):
        return type(self)(self|0b00000000000000000010000000000000)
    def deny_manage_messages(self):
        return type(self)(self&0b11111111111111111101111111111111)

    #14
    @property
    def can_embed_links(self):
        return (self>>14)&1
    def allow_embed_links(self):
        return type(self)(self|0b00000000000000000100000000000000)
    def deny_embed_links(self):
        return type(self)(self&0b1111111111111111101111111111111)

    #15
    @property
    def can_attach_files(self):
        return (self>>15)&1
    def allow_attach_files(self):
        return type(self)(self|0b00000000000000000100000000000000)
    def deny_attach_files(self):
        return type(self)(self&0b11111111111111111011111111111111)

    #16
    @property
    def can_read_message_history(self):
        return (self>>16)&1
    def allow_read_message_history(self):
        return type(self)(self|0b00000000000000010000000000000000)
    def deny_read_message_history(self):
        return type(self)(self&0b11111111111111101111111111111111)
    
    #17
    @property
    def can_mention_everyone(self):
        return (self>>17)&1
    def allow_mention_everyone(self):
        return type(self)(self|0b00000000000000100000000000000000)
    def deny_mention_everyone(self):
        return type(self)(self&0b11111111111111011111111111111111)

    #18
    @property
    def can_use_external_emojis(self):
        return (self>>18)&1
    def allow_use_external_emojis(self):
        return type(self)(self|0b00000000000001000000000000000000)
    def deny_use_external_emojis(self):
        return type(self)(self&0b11111111111110111111111111111111)

    #19
    @property
    def can_view_guild_insights(self):
        return (self>>19)&1
    def allow_view_guild_insights(self):
        return type(self)(self|0b00000000000010000000000000000000)
    def deny_view_guild_insights(self):
        return type(self)(self&0b11111111111101111111111111111111)

    #20
    @property
    def can_connect(self):
        return (self>>20)&1
    def allow_connect(self):
        return type(self)(self|0b00000000000100000000000000000000)
    def deny_connect(self):
        return type(self)(self&0b11111111111011111111111111111111)
    
    #21
    @property
    def can_speak(self):
        return (self>>21)&1
    def allow_speak(self):
        return type(self)(self|0b00000000001000000000000000000000)
    def deny_speak(self):
        return type(self)(self&0b11111111110111111111111111111111)

    #22
    @property
    def can_mute_users(self):
        return (self>>22)&1
    def allow_mute_users(self):
        return type(self)(self|0b00000000010000000000000000000000)
    def deny_mute_users(self):
        return type(self)(self&0b11111111101111111111111111111111)
    
    #23
    @property
    def can_deafen_users(self):
        return (self>>23)&1
    def allow_deafen_users(self):
        return type(self)(self|0b00000000100000000000000000000000)
    def deny_deafen_users(self):
        return type(self)(self&0b11111111011111111111111111111111)

    #24
    @property
    def can_move_users(self):
        return (self>>24)&1
    def allow_move_users(self):
        return type(self)(self|0b00000001000000000000000000000000)
    def deny_move_users(self):
        return type(self)(self&0b11111110111111111111111111111111)

    #25
    @property
    def can_use_voice_activation(self):
        return (self>>25)&1
    def allow_use_voice_activation(self):
        return type(self)(self|0b00000010000000000000000000000000)
    def deny_use_voice_activation(self):
        return type(self)(self&0b11111110111111111111111111111111)

    #26
    @property
    def can_change_nickname(self):
        return (self>>26)&1
    def allow_change_nickname(self):
        return type(self)(self|0b00000100000000000000000000000000)
    def deny_change_nickname(self):
        return type(self)(self&0b11111011111111111111111111111111)

    #27
    @property
    def can_manage_nicknames(self):
        return (self>>27)&1
    def allow_manage_nicknames(self):
        return type(self)(self|0b00001000000000000000000000000000)
    def deny_manage_nicknames(self):
        return type(self)(self&0b11110111111111111111111111111111)

    #28
    @property
    def can_manage_roles(self):
        return (self>>28)&1
    def allow_manage_roles(self):
        return type(self)(self|0b00010000000000000000000000000000)
    def deny_manage_roles(self):
        return type(self)(self&0b11101111111111111111111111111111)

    #29
    @property
    def can_manage_webhooks(self):
        return (self>>29)&1
    def allow_manage_webhooks(self):
        return type(self)(self|0b00100000000000000000000000000000)
    def deny_manage_webhooks(self):
        return type(self)(self&0b11011111111111111111111111111111)

    #30
    @property
    def can_manage_emojis(self):
        return (self>>30)&1
    def allow_manage_emojis(self):
        return type(self)(self|0b01000000000000000000000000000000)
    def deny_manage_emojis(self):
        return type(self)(self&0b10111111111111111111111111111111)

    #31 unused
##    @property
##    def can_(self):
##        return (self>>31)&1
##    def allow_(self):
##        return type(self)(self|0b10000000000000000000000000000000)
##    def deny_(self):
##        return type(self)(self&0b01111111111111111111111111111111)

    
    #20 more unused
    
    #guild specific permissions: manage_guild,kick_users,ban_users,administrator,change_nicknames,manage_nicknames

    voice         = 0b00000011111100000000001100000000
    none          = 0b00000000000000000000000000000000
    all           = 0b01111111111111111111111111111111
    all_channel   = 0b00110011111101111111111001010001 #no guild permissions
    text          = 0b00000000000001111111110001000000
    general       = 0b01111100000000000000000010111111
    
    deny_text     = 0b11111111111111011000011111111111
    deny_voice    = 0b11111100000011111111111011111111 #~voice
    deny_voice_con= 0b11111100000011111111111011111111 #~voice - manage_roles - manage_channel
    deny_both     = deny_text&deny_voice

    permission_all              = NotImplemented
    permission_none             = NotImplemented
    permission_private          = NotImplemented
    permission_private_bot      = NotImplemented
    permission_group            = NotImplemented
    permission_group_owner      = NotImplemented
    permission_all_deny_text    = NotImplemented
    permission_all_deny_voice   = NotImplemented
    permission_all_deny_both    = NotImplemented

Permission.permission_all           = Permission(Permission.all)
Permission.permission_none          = Permission(Permission.none)
Permission.permission_private       = Permission(0b00000000000001111100110001000000)
Permission.permission_private_bot   = Permission(0b00000000000001101100110001000000)
Permission.permission_group         = Permission(0b00000000000001111100010001000000)
Permission.permission_group_owner   = Permission(0b00000000000001111100110001000010)
Permission.permission_all_deny_text = Permission(Permission.deny_text)
Permission.permission_all_deny_voice= Permission(Permission.deny_voice)
Permission.permission_all_deny_both = Permission(Permission.deny_both)

