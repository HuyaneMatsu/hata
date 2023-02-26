__all__ = ()

from ...field_parsers import (
    bool_parser_factory, entity_id_parser_factory, force_string_parser_factory, negated_bool_parser_factory,
    nullable_date_time_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, entity_id_putter_factory, force_bool_putter_factory, force_string_putter_factory,
    negated_bool_optional_putter_factory, nullable_date_time_optional_putter_factory
)
from ...field_validators import (
    bool_validator_factory, entity_id_validator_factory, force_string_validator_factory,
    nullable_date_time_validator_factory
)
from ..user import ClientUserBase

# channel_id

parse_channel_id = entity_id_parser_factory('channel_id')
put_channel_id_into = entity_id_putter_factory('channel_id')
validate_channel_id = entity_id_validator_factory('channel_id', NotImplemented, include = 'Channel')

# deaf

parse_deaf = bool_parser_factory('deaf', False)
put_deaf_into = force_bool_putter_factory('deaf')
validate_deaf = bool_validator_factory('deaf', False)

# guild_id

validate_guild_id = entity_id_validator_factory('guild_id', NotImplemented, include = 'Guild')

# mute

parse_mute = bool_parser_factory('mute', False)
put_mute_into = force_bool_putter_factory('mute')
validate_mute = bool_validator_factory('mute', False)

# requested_to_speak_at

parse_requested_to_speak_at = nullable_date_time_parser_factory('request_to_speak_timestamp')
put_requested_to_speak_at_into = nullable_date_time_optional_putter_factory('request_to_speak_timestamp')
validate_requested_to_speak_at = nullable_date_time_validator_factory('requested_to_speak_at')

# self_deaf

parse_self_deaf = bool_parser_factory('self_deaf', False)
put_self_deaf_into = force_bool_putter_factory('self_deaf')
validate_self_deaf = bool_validator_factory('self_deaf', False)

# self_mute

parse_self_mute = bool_parser_factory('self_mute', False)
put_self_mute_into = force_bool_putter_factory('self_mute')
validate_self_mute = bool_validator_factory('self_mute', False)

# self_stream

parse_self_stream = bool_parser_factory('self_stream', False)
put_self_stream_into = bool_optional_putter_factory('self_stream', False)
validate_self_stream = bool_validator_factory('self_stream', False)

# self_video

parse_self_video = bool_parser_factory('self_video', False)
put_self_video_into = force_bool_putter_factory('self_video')
validate_self_video = bool_validator_factory('self_video', False)

# session_id

parse_session_id = force_string_parser_factory('session_id')
put_session_id_into = force_string_putter_factory('session_id')
validate_session_id = force_string_validator_factory('session_id', 0, 1024)

# speaker

parse_speaker = negated_bool_parser_factory('suppress', False)
put_speaker_into = negated_bool_optional_putter_factory('suppress', False)
validate_speaker = bool_validator_factory('speaker', False)

# user_id

parse_user_id = entity_id_parser_factory('user_id')
put_user_id_into = entity_id_putter_factory('user_id')
validate_user_id = entity_id_validator_factory('user_id', ClientUserBase)
