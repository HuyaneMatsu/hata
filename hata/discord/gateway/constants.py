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

GATEWAY_ACTION_KEEP_GOING = 0
GATEWAY_ACTION_CONNECT = 1
GATEWAY_ACTION_RESUME = 2
