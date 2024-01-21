__all__ = ()


# heart beat
HEARTBEAT_TIMEOUT = 20.0
INTERVAL_DEFAULT = 40.0
LATENCY_DEFAULT = 9999.0

# gateway
GATEWAY_CONNECT_TIMEOUT = 30.0
POLL_TIMEOUT = 60.0

# rate limit
GATEWAY_RATE_LIMIT_LIMIT = 120
GATEWAY_RATE_LIMIT_RESET = 60.0

# gateway control
GATEWAY_ACTION_KEEP_GOING = 0
GATEWAY_ACTION_CONNECT = 1
GATEWAY_ACTION_RESUME = 2


# operations / client

GATEWAY_OPERATION_CLIENT_DISPATCH = 0
GATEWAY_OPERATION_CLIENT_HEARTBEAT = 1
GATEWAY_OPERATION_CLIENT_IDENTIFY = 2
GATEWAY_OPERATION_CLIENT_PRESENCE = 3
GATEWAY_OPERATION_CLIENT_VOICE_STATE = 4
GATEWAY_OPERATION_CLIENT_VOICE_PING = 5
GATEWAY_OPERATION_CLIENT_RESUME = 6
GATEWAY_OPERATION_CLIENT_RECONNECT = 7
GATEWAY_OPERATION_CLIENT_REQUEST_GUILD_USERS = 8
GATEWAY_OPERATION_CLIENT_INVALIDATE_SESSION = 9
GATEWAY_OPERATION_CLIENT_HELLO = 10
GATEWAY_OPERATION_CLIENT_HEARTBEAT_ACKNOWLEDGE = 11
GATEWAY_OPERATION_CLIENT_GUILD_SYNC = 12
GATEWAY_OPERATION_CLIENT_REQUEST_SOUNDBOARD_SOUNDS = 31

"""
GATEWAY_OPERATION_CLIENT_DISPATCH : `int` = `0`
    Receive only, used at `._handle_received_message`.
GATEWAY_OPERATION_CLIENT_HEARTBEAT : `int` = `1`
    Send and receive, used at `._beat` and at `._handle_special_operation`.
GATEWAY_OPERATION_CLIENT_IDENTIFY : `int` = `2`
    Send only, used `._identify`.
GATEWAY_OPERATION_CLIENT_PRESENCE : `int` = `3`
    Send only, used at ``Client.edit_presence``.
GATEWAY_OPERATION_CLIENT_VOICE_STATE : `int` = `4`
    Send only, used at `.change_voice_state`.
GATEWAY_OPERATION_CLIENT_VOICE_PING : `int` = `5`
    Removed.
GATEWAY_OPERATION_CLIENT_RESUME : `int` = `6`
    Send only, used at `._resume`.
GATEWAY_OPERATION_CLIENT_RECONNECT : `int` = `7`
    Receive only, used at `._special_operation`.
GATEWAY_OPERATION_CLIENT_REQUEST_GUILD_USERS : `int` = `8`
    Send only, used at ``Client._request_users_loop``, ``Client._request_users`` and at ``Client.request_member``.
GATEWAY_OPERATION_CLIENT_INVALIDATE_SESSION : `int` = `9`
    Receive only, used at `._handle_special_operation`.
GATEWAY_OPERATION_CLIENT_HELLO : `int` = `10`
    Receive only, used at `._handle_special_operation`.
GATEWAY_OPERATION_CLIENT_HEARTBEAT_ACKNOWLEDGE : `int` = `11`
    Receive only, used at `._handle_special_operation`.
GATEWAY_OPERATION_CLIENT_GUILD_SYNC : `int` = `12`
    Send only, not used.
GATEWAY_OPERATION_CLIENT_REQUEST_SOUNDBOARD_SOUNDS : `int` = `13`
    Send only, used to request the guilds' soundboard sounds.
"""

# operations / voice

GATEWAY_OPERATION_VOICE_IDENTIFY = 0
GATEWAY_OPERATION_VOICE_SELECT_PROTOCOL = 1
GATEWAY_OPERATION_VOICE_READY = 2
GATEWAY_OPERATION_VOICE_HEARTBEAT = 3
GATEWAY_OPERATION_VOICE_SESSION_DESCRIPTION = 4
GATEWAY_OPERATION_VOICE_SPEAKING = 5
GATEWAY_OPERATION_VOICE_HEARTBEAT_ACKNOWLEDGE = 6
GATEWAY_OPERATION_VOICE_RESUME = 7
GATEWAY_OPERATION_VOICE_HELLO = 8
GATEWAY_OPERATION_VOICE_RESUMED = 9
GATEWAY_OPERATION_VOICE_CLIENT_CONNECT = 12
GATEWAY_OPERATION_VOICE_CLIENT_DISCONNECT = 13
GATEWAY_OPERATION_VOICE_VIDEO_SESSION_DESCRIPTION = 14
GATEWAY_OPERATION_VOICE_VIDEO_SINK = 15
GATEWAY_OPERATION_VOICE_FLAGS = 18
GATEWAY_OPERATION_VOICE_PLATFORM = 20


"""
GATEWAY_OPERATION_VOICE_IDENTIFY : `int` = `0`
    Send only, used at `._identify`.
GATEWAY_OPERATION_VOICE_SELECT_PROTOCOL : `int` = `1`
    Send only, used at `._select_protocol`.
GATEWAY_OPERATION_VOICE_READY : `int` = `2`
    Receive only, used at `._initial_connection`.
GATEWAY_OPERATION_VOICE_HEARTBEAT : `int` = `3`
    Send only, used at `._beat`.
GATEWAY_OPERATION_VOICE_SESSION_DESCRIPTION : `int` = `4`
    Receive only, used at `._received_message`.
GATEWAY_OPERATION_VOICE_SPEAKING : `int` = `5`
    Send and receive, used at `.set_speaking` and at `._handle_operation_speaking`.
GATEWAY_OPERATION_VOICE_HEARTBEAT_ACKNOWLEDGE : `int` = `6`
    Receive only, used at `._handle_operation_heartbeat_acknowledge`.
GATEWAY_OPERATION_VOICE_RESUME : `int` = `7`
    Send only, used at `._resume`.
GATEWAY_OPERATION_VOICE_HELLO : `int` = `8`
    Receive only, used at `._handle_operation_hello`.
GATEWAY_OPERATION_VOICE_RESUMED : `int` = `9`
    Receive only, used at `._handle_operation_resumed`.
GATEWAY_OPERATION_VOICE_CLIENT_CONNECT : `int` = `12`
    Receive only, used at `._handle_operation_client_connect`.
GATEWAY_OPERATION_VOICE_CLIENT_DISCONNECT : `int` = `13`
    Receive only, used at `._handle_operation_client_disconnect`.
GATEWAY_OPERATION_VOICE_VIDEO_SESSION_DESCRIPTION : `int` = `14`
    Receive only. Not used.
GATEWAY_OPERATION_VOICE_VIDEO_SINK : `int` = `15`
    Receive and send, not used.
GATEWAY_OPERATION_VOICE_FLAGS : `int` = `18`
    Receive only, not used.
GATEWAY_OPERATION_VOICE_PLATFORM : `int` = `20`
    Receive only, not used.
"""
