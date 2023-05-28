__all__ = ()

from ...field_parsers import entity_id_parser_factory, nullable_entity_array_parser_factory
from ...field_putters import entity_id_optional_putter_factory, nullable_entity_array_putter_factory
from ...field_validators import entity_id_validator_factory, nullable_entity_array_validator_factory

from ..soundboard_sound import SoundboardSound

# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id_into = entity_id_optional_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', NotImplemented, include = 'Guild')

# sounds

parse_sounds = nullable_entity_array_parser_factory('soundboard_sounds', SoundboardSound)
put_sounds_into = nullable_entity_array_putter_factory(
    'soundboard_sounds', SoundboardSound, force_include_internals = True
)
validate_sounds = nullable_entity_array_validator_factory('sounds', SoundboardSound)
