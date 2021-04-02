# -*- coding: utf-8 -*-
__all__ = ('Permission', )

from .bases import FlagBase

class Permission(FlagBase, access_keyword='can', enable_keyword='allow', disable_keyword='deny'):
    """
    Represents a Discord permission.
    
    The implemented permissions are the following:
    
    +---------------------------+-------------------+
    | Respective name           | Bitwise position  |
    +===========================+===================+
    | create_instant_invite     |  0                |
    +---------------------------+-------------------+
    | kick_users                |  1                |
    +---------------------------+-------------------+
    | ban_users                 |  2                |
    +---------------------------+-------------------+
    | administrator             |  3                |
    +---------------------------+-------------------+
    | manage_channel            |  4                |
    +---------------------------+-------------------+
    | manage_guild              |  5                |
    +---------------------------+-------------------+
    | add_reactions             |  6                |
    +---------------------------+-------------------+
    | view_audit_logs           |  7                |
    +---------------------------+-------------------+
    | priority_speaker          |  8                |
    +---------------------------+-------------------+
    | stream                    |  9                |
    +---------------------------+-------------------+
    | view_channel              | 10                |
    +---------------------------+-------------------+
    | send_messages             | 11                |
    +---------------------------+-------------------+
    | send_tts_messages         | 12                |
    +---------------------------+-------------------+
    | manage_messages           | 13                |
    +---------------------------+-------------------+
    | embed_links               | 14                |
    +---------------------------+-------------------+
    | attach_files              | 15                |
    +---------------------------+-------------------+
    | read_message_history      | 16                |
    +---------------------------+-------------------+
    | mention_everyone          | 17                |
    +---------------------------+-------------------+
    | use_external_emojis       | 18                |
    +---------------------------+-------------------+
    | connect                   | 20                |
    +---------------------------+-------------------+
    | speak                     | 21                |
    +---------------------------+-------------------+
    | mute_users                | 22                |
    +---------------------------+-------------------+
    | deafen_users              | 23                |
    +---------------------------+-------------------+
    | move_users                | 24                |
    +---------------------------+-------------------+
    | use_voice_activation      | 25                |
    +---------------------------+-------------------+
    | change_nickname           | 26                |
    +---------------------------+-------------------+
    | manage_nicknames          | 27                |
    +---------------------------+-------------------+
    | manage_roles              | 28                |
    +---------------------------+-------------------+
    | manage_webhooks           | 29                |
    +---------------------------+-------------------+
    | manage_emojis             | 30                |
    +---------------------------+-------------------+
    | use_application_commands  | 31                |
    +---------------------------+-------------------+
    | request_to_speak          | 32                |
    +---------------------------+-------------------+
    
    Each permission can be accessed as property with `can_` + it's respective name, meanwhile a new edited permission
    can be created with the `allow_...` and with the `deny_...` methods.
    """
    __keys__ = {
        'create_instant_invite'     :  0,
        'kick_users'                :  1,
        'ban_users'                 :  2,
        'administrator'             :  3,
        'manage_channel'            :  4,
        'manage_guild'              :  5,
        'add_reactions'             :  6,
        'view_audit_logs'           :  7,
        'priority_speaker'          :  8,
        'stream'                    :  9,
        'view_channel'              : 10,
        'send_messages'             : 11,
        'send_tts_messages'         : 12,
        'manage_messages'           : 13,
        'embed_links'               : 14,
        'attach_files'              : 15,
        'read_message_history'      : 16,
        'mention_everyone'          : 17,
        'use_external_emojis'       : 18,
        'view_guild_insights'       : 19,
        'connect'                   : 20,
        'speak'                     : 21,
        'mute_users'                : 22,
        'deafen_users'              : 23,
        'move_users'                : 24,
        'use_voice_activation'      : 25,
        'change_nickname'           : 26,
        'manage_nicknames'          : 27,
        'manage_roles'              : 28,
        'manage_webhooks'           : 29,
        'manage_emojis'             : 30,
        'use_application_commands'  : 31,
        'request_to_speak'          : 32,
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


PERMISSION_ALL = Permission().update_by_keys(
    create_instant_invite    = True,
    kick_users               = True,
    ban_users                = True,
    administrator            = True,
    manage_channel           = True,
    manage_guild             = True,
    add_reactions            = True,
    view_audit_logs          = True,
    priority_speaker         = True,
    stream                   = True,
    view_channel             = True,
    send_messages            = True,
    send_tts_messages        = True,
    manage_messages          = True,
    embed_links              = True,
    attach_files             = True,
    read_message_history     = True,
    mention_everyone         = True,
    use_external_emojis      = True,
    view_guild_insights      = True,
    connect                  = True,
    speak                    = True,
    mute_users               = True,
    deafen_users             = True,
    move_users               = True,
    use_voice_activation     = True,
    change_nickname          = True,
    manage_nicknames         = True,
    manage_roles             = True,
    manage_webhooks          = True,
    manage_emojis            = True,
    use_application_commands = True,
    request_to_speak         = True,
        )

PERMISSION_NONE = Permission()

PERMISSION_PRIVATE = Permission().update_by_keys(
    create_instant_invite    = False,
    kick_users               = False,
    ban_users                = False,
    administrator            = False,
    manage_channel           = False,
    manage_guild             = False,
    add_reactions            = True,
    view_audit_logs          = False,
    priority_speaker         = False,
    stream                   = False,
    view_channel             = True,
    send_messages            = True,
    send_tts_messages        = False,
    manage_messages          = False,
    embed_links              = True,
    attach_files             = True,
    read_message_history     = True,
    mention_everyone         = True,
    use_external_emojis      = True,
    view_guild_insights      = False,
    connect                  = False,
    speak                    = False,
    mute_users               = False,
    deafen_users             = False,
    move_users               = False,
    use_voice_activation     = True,
    change_nickname          = False,
    manage_nicknames         = False,
    manage_roles             = False,
    manage_webhooks          = False,
    manage_emojis            = False,
    use_application_commands = True,
    request_to_speak         = False,
        )

PERMISSION_PRIVATE_BOT = PERMISSION_PRIVATE.update_by_keys(
    read_message_history     = False,
        )

PERMISSION_GROUP = PERMISSION_PRIVATE.update_by_keys(
    create_instant_invite    = True,
        )

PERMISSION_GROUP_OWNER = PERMISSION_GROUP.update_by_keys(
    kick_users               = True,
        )

PERMISSION_TEXT_ALL = Permission().update_by_keys(
    create_instant_invite    = False,
    kick_users               = False,
    ban_users                = False,
    administrator            = False,
    manage_channel           = False,
    manage_guild             = False,
    add_reactions            = True,
    view_audit_logs          = False,
    priority_speaker         = False,
    stream                   = False,
    view_channel             = False,
    send_messages            = True,
    send_tts_messages        = True,
    manage_messages          = False,
    embed_links              = True,
    attach_files             = True,
    read_message_history     = False,
    mention_everyone         = True,
    use_external_emojis      = True,
    view_guild_insights      = False,
    connect                  = False,
    speak                    = False,
    mute_users               = False,
    deafen_users             = False,
    move_users               = False,
    use_voice_activation     = False,
    change_nickname          = False,
    manage_nicknames         = False,
    manage_roles             = False,
    manage_webhooks          = False,
    manage_emojis            = False,
    use_application_commands = True,
    request_to_speak         = False,
        )

PERMISSION_TEXT_DENY = Permission(~PERMISSION_TEXT_ALL)

PERMISSION_TEXT_AND_STAGE_DENY = PERMISSION_TEXT_DENY.update_by_keys(
    request_to_speak         = False,
        )

PERMISSION_VOICE_ALL = Permission().update_by_keys(
    create_instant_invite    = False,
    kick_users               = False,
    ban_users                = False,
    administrator            = False,
    manage_channel           = False,
    manage_guild             = False,
    add_reactions            = False,
    view_audit_logs          = False,
    priority_speaker         = True,
    stream                   = True,
    view_channel             = False,
    send_messages            = False,
    send_tts_messages        = False,
    manage_messages          = False,
    embed_links              = False,
    attach_files             = False,
    read_message_history     = False,
    mention_everyone         = False,
    use_external_emojis      = False,
    view_guild_insights      = False,
    connect                  = True,
    speak                    = True,
    mute_users               = True,
    deafen_users             = True,
    move_users               = True,
    use_voice_activation     = True,
    change_nickname          = False,
    manage_nicknames         = False,
    manage_roles             = False,
    manage_webhooks          = False,
    manage_emojis            = False,
    use_application_commands = False,
    request_to_speak         = True,
        )

PERMISSION_VOICE_DENY = Permission(~PERMISSION_VOICE_ALL)

PERMISSION_VOICE_DENY_CONNECTION = PERMISSION_VOICE_DENY.update_by_keys(
    manage_roles             = False,
    manage_channel           = False,
        )

PERMISSION_TEXT_AND_VOICE_DENY = Permission(PERMISSION_TEXT_DENY|PERMISSION_VOICE_DENY)

PERMISSION_STAGE_MODERATOR = Permission().update_by_keys(
    create_instant_invite    = False,
    kick_users               = False,
    ban_users                = False,
    administrator            = False,
    manage_channel           = False,
    manage_guild             = False,
    add_reactions            = False,
    view_audit_logs          = False,
    priority_speaker         = False,
    stream                   = False,
    view_channel             = False,
    send_messages            = False,
    send_tts_messages        = False,
    manage_messages          = False,
    embed_links              = False,
    attach_files             = False,
    read_message_history     = False,
    mention_everyone         = False,
    use_external_emojis      = False,
    view_guild_insights      = False,
    connect                  = False,
    speak                    = False,
    mute_users               = True,
    deafen_users             = False,
    move_users               = True,
    use_voice_activation     = False,
    change_nickname          = False,
    manage_nicknames         = False,
    manage_roles             = False,
    manage_webhooks          = False,
    manage_emojis            = False,
    use_application_commands = False,
    request_to_speak         = True,
        )
