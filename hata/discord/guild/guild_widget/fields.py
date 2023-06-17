__all__ = ()

from ...field_parsers import int_parser_factory, nullable_entity_array_parser_factory, nullable_string_parser_factory
from ...field_putters import int_putter_factory, nullable_entity_array_putter_factory, url_optional_putter_factory
from ...field_validators import (
    int_conditional_validator_factory, nullable_entity_array_validator_factory, url_optional_validator_factory
)

from ..guild.fields import parse_id, parse_name, put_id_into, put_name_into, validate_id, validate_name
from ..guild_widget_channel import GuildWidgetChannel
from ..guild_widget_user import GuildWidgetUser

# approximate_online_count

parse_approximate_online_count = int_parser_factory('presence_count', 0)
put_approximate_online_count_into = int_putter_factory('presence_count')
validate_approximate_online_count = int_conditional_validator_factory(
    'approximate_online_count',
    0,
    lambda approximate_online_count : approximate_online_count >= 0,
    '>= 0',
)

# channels

parse_channels = nullable_entity_array_parser_factory('channels', GuildWidgetChannel)
put_channels_into = nullable_entity_array_putter_factory('channels', GuildWidgetChannel)
validate_channels = nullable_entity_array_validator_factory('channels', GuildWidgetChannel)

# invite_url

parse_invite_url = nullable_string_parser_factory('instant_invite')
put_invite_url_into = url_optional_putter_factory('instant_invite')
validate_invite_url = url_optional_validator_factory('invite_url')

# users

parse_users = nullable_entity_array_parser_factory('members', GuildWidgetUser)
put_users_into = nullable_entity_array_putter_factory('members', GuildWidgetUser)
validate_users = nullable_entity_array_validator_factory('members', GuildWidgetUser)
