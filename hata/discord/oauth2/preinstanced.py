__all__ = ('Oauth2Scope',)

from ..bases import Preinstance as P, PreinstancedBase


class Oauth2Scope(PreinstancedBase):
    """
    Represents an oauth2 scope.
    
    Attributes
    ----------
    name : `str`
        The name of the oauth2 scope
    value : `str`
        The identifier value the oauth2 scope.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``Oauth2Scope``) items
        Stores the predefined ``Oauth2Scope``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `str`
        The connection types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the connection types.
    
    Every predefined oauth2 scope can be accessed as class attribute as well:
    
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | Class attribute name                      | name                  | value                                     |
    +===========================================+=======================+===========================================+
    | activities_read                           | activities read       | activities.read                           |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | activities_write                          | activities write      | activities.write                          |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | applications_builds_read                  | applications builds   | applications.builds.read                  |
    |                                           | read                  |                                           |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | applications_builds_upload                | applications builds   | applications.builds.upload                |
    |                                           | upload                |                                           |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | applications_commands                     | applications commands | applications.commands                     |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | applications_commands_update              | applications commands | applications.commands.update              |
    |                                           | update                |                                           |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | applications_commands_permissions_update  | applications commands | applications.commands.permissions.update  |
    |                                           | permissions update    |                                           |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | applications_entitlements                 | applications          | applications.entitlements                 |
    |                                           | entitlements          |                                           |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | applications_store_update                 | applications store    | applications.store.update                 |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | bot                                       | bot                   | bot                                       |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | channels_private_group_join               | channels private      | gdm.join                                  |
    |                                           | group join            |                                           |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | channels_private_read                     | channels private read | dm_channels.read                          |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | connections                               | connections           | connections                               |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | email                                     | email                 | email                                     |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | guilds                                    | guilds                | guilds                                    |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | guilds_join                               | guilds join           | guilds.join                               |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | guilds_users_read                         | guilds users read     | guilds.members.read                       |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | identify                                  | identify              | identify                                  |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | messages_read                             | messages read         | messages.read                             |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | relationships_read                        | relationships read    | relationships.read                        |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | role_connections_write                    | role connections      | role_connections.write                    |
    |                                           | write                 |                                           |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | rpc                                       | rpc                   | rpc                                       |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | rpc_activities_write                      | rpc activities write  | rpc.activities.write                      |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | rpc_notifications_read                    | rpc notifications     | rpc.notifications.read                    |
    |                                           | read                  |                                           |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | rpc_voice_read                            | rpc voice read        | rpc.voice.read                            |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | rpc_voice_write                           | rpc voice write       | rpc.voice.write                           |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | voice                                     | voice                 | voice                                     |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    | webhook_incoming                          | webhook incoming      | webhook.incoming                          |
    +-------------------------------------------+-----------------------+-------------------------------------------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    DEFAULT_NAME = 'UNDEFINED'
    
    activities_read = P('activities.read', 'activities read')
    activities_write = P('activities.write', 'activities write')
    applications_builds_read = P('applications.builds.read', 'applications builds read')
    applications_builds_upload = P('applications.builds.upload', 'applications builds upload')
    applications_commands = P('applications.commands', 'applications commands')
    applications_commands_update = P('applications.commands.update', 'applications commands update')
    applications_commands_permissions_update = P(
        'applications.commands.permissions.update', 'applications commands permissions update'
    )
    applications_entitlements = P('applications.entitlements', 'applications entitlements')
    applications_store_update = P('applications.store.update', 'applications store update')
    bot = P('bot', 'bot')
    channels_private_group_join = P('gdm.join', 'channels private group join')
    channels_private_read = P('dm_channels.read', 'channels private read')
    connections = P('connections', 'connections')
    email = P('email', 'email')
    guilds = P('guilds', 'guilds')
    guilds_join = P('guilds.join', 'guilds join')
    guilds_users_read = P('guilds.members.read', 'guilds users read')
    identify = P('identify', 'identify')
    messages_read = P('messages.read', 'messages read')
    relationships_read = P('relationships.read', 'relationships read')
    role_connections_write = P('role_connections.write', 'role connections write')
    rpc = P('rpc', 'rpc')
    rpc_activities_write = P('rpc.activities.write', 'rpc activities write')
    rpc_notifications_read = P('rpc.notifications.read', 'rpc notifications read')
    rpc_voice_read = P('rpc.voice.read', 'rpc voice read')
    rpc_voice_write = P('rpc.voice.write', 'rpc voice write')
    voice = P('voice', 'voice')
    webhook_incoming = P('webhook.incoming', 'webhook incoming')
