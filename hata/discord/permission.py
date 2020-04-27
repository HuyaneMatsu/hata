# -*- coding: utf-8 -*-
__all__ = ('Permission', )

from .bases import FlagBase

class Permission(FlagBase, access_keyword='can', enable_keyword='allow', disable_keyword='deny'):
    __keys__ = {
        'create_instant_invite' :  0,
        'kick_users'            :  1,
        'ban_users'             :  2,
        'administrator'         :  3,
        'manage_channel'        :  4,
        'manage_guild'          :  5,
        'add_reactions'         :  6,
        'view_audit_logs'       :  7,
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

    def handle_overwrite(self,allow,deny):
        #1st denies permissions, then allows
        return type(self)((self&~deny)|allow)
    
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

del FlagBase
