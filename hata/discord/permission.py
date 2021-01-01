# -*- coding: utf-8 -*-
__all__ = ('Permission', )

from .bases import FlagBase

class Permission(FlagBase, access_keyword='can', enable_keyword='allow', disable_keyword='deny'):
    """
    Represents a Discord permission.
    
    The implemented permissions are the following:
    
    +-----------------------+-------------------+
    | Respective name       | Bitwise position  |
    +=======================+===================+
    | create_instant_invite |  0                |
    +-----------------------+-------------------+
    | kick_users            |  1                |
    +-----------------------+-------------------+
    | ban_users             |  2                |
    +-----------------------+-------------------+
    | administrator         |  3                |
    +-----------------------+-------------------+
    | manage_channel        |  4                |
    +-----------------------+-------------------+
    | manage_guild          |  5                |
    +-----------------------+-------------------+
    | add_reactions         |  6                |
    +-----------------------+-------------------+
    | view_audit_logs       |  7                |
    +-----------------------+-------------------+
    | priority_speaker      |  8                |
    +-----------------------+-------------------+
    | stream                |  9                |
    +-----------------------+-------------------+
    | view_channel          | 10                |
    +-----------------------+-------------------+
    | send_messages         | 11                |
    +-----------------------+-------------------+
    | send_tts_messages     | 12                |
    +-----------------------+-------------------+
    | manage_messages       | 13                |
    +-----------------------+-------------------+
    | embed_links           | 14                |
    +-----------------------+-------------------+
    | attach_files          | 15                |
    +-----------------------+-------------------+
    | read_message_history  | 16                |
    +-----------------------+-------------------+
    | mention_everyone      | 17                |
    +-----------------------+-------------------+
    | use_external_emojis   | 18                |
    +-----------------------+-------------------+
    | connect               | 20                |
    +-----------------------+-------------------+
    | speak                 | 21                |
    +-----------------------+-------------------+
    | mute_users            | 22                |
    +-----------------------+-------------------+
    | deafen_users          | 23                |
    +-----------------------+-------------------+
    | move_users            | 24                |
    +-----------------------+-------------------+
    | use_voice_activation  | 25                |
    +-----------------------+-------------------+
    | change_nickname       | 26                |
    +-----------------------+-------------------+
    | manage_nicknames      | 27                |
    +-----------------------+-------------------+
    | manage_roles          | 28                |
    +-----------------------+-------------------+
    | manage_webhooks       | 29                |
    +-----------------------+-------------------+
    | manage_emojis         | 30                |
    +-----------------------+-------------------+
    
    Each permission can be accessed as property with `can_` + it's respective name, meanwhile a new edited permission
    can be created with the `allow_...` and with the `deny_...` methods.
    
    There are some predefined permissions as well set as class attributes, mainly for internal usage:
    
    +---------------------------+-----------------------------------------------+
    | Name                      | Value                                         |
    +===========================+===============================================+
    | permission_all            | 0b01111111111111111111111111111111            |
    +---------------------------+-----------------------------------------------+
    | permission_none           | 0b00000000000000000000000000000000            |
    +---------------------------+-----------------------------------------------+
    | permission_private        | 0b00000000000001111100110001000000            |
    +---------------------------+-----------------------------------------------+
    | permission_private_bot    | 0b00000000000001101100110001000000            |
    +---------------------------+-----------------------------------------------+
    | permission_group          | 0b00000000000001111100010001000000            |
    +---------------------------+-----------------------------------------------+
    | permission_group_owner    | 0b00000000000001111100110001000010            |
    +---------------------------+-----------------------------------------------+
    | permission_deny_text      | 0b11111111111111011000011111111111            |
    +---------------------------+-----------------------------------------------+
    | permission_deny_voice     | 0b11111100000011111111110011111111            |
    +---------------------------+-----------------------------------------------+
    | permission_deny_voice_con | 0b11101100000011111111111011101111            |
    +---------------------------+-----------------------------------------------+
    | permission_deny_both      | permission_deny_text|permission_deny_voice    |
    +---------------------------+-----------------------------------------------+
    """
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

    def handle_overwrite(self, allow, deny):
        """
        Applies an allow and a deny operation on the permission.
        
        Parameters
        ----------
        allow : ``Permission``
            Permissions to allow.
        deny : ``Permission``
            Permissions to deny.
        
        Returns
        -------
        result : ``Permission``
        """
        # 1st denies permissions, then allows
        return type(self)((self&~deny)|allow)
    
    # guild specific permissions: manage_guild, kick_users, ban_users, administrator, change_nicknames, manage_nicknames
    
    permission_all            = NotImplemented
    permission_none           = NotImplemented
    permission_private        = NotImplemented
    permission_private_bot    = NotImplemented
    permission_group          = NotImplemented
    permission_group_owner    = NotImplemented
    permission_deny_text      = NotImplemented
    permission_deny_voice     = NotImplemented
    permission_deny_voice_con = NotImplemented
    permission_deny_both      = NotImplemented

Permission.permission_all            = Permission(0b01111111111111111111111111111111)
Permission.permission_none           = Permission(0b00000000000000000000000000000000)
Permission.permission_private        = Permission(0b00000000000001111100110001000000)
Permission.permission_private_bot    = Permission(0b00000000000001101100110001000000)
Permission.permission_group          = Permission(0b00000000000001111100010001000000)
Permission.permission_group_owner    = Permission(0b00000000000001111100110001000010)
Permission.permission_deny_text      = Permission(0b11111111111111011000011111111111)
Permission.permission_deny_voice     = Permission(0b11111100000011111111110011111111) #~voice
Permission.permission_deny_voice_con = Permission(0b11101100000011111111111011101111) #~voice - manage_roles - manage_channel
Permission.permission_deny_both      = Permission(Permission.permission_deny_text|Permission.permission_deny_voice)

del FlagBase
