__all__ = ()

from ...fields.field_parsers import nullable_entity_array_parser_factory
from ...fields.field_putters import nullable_entity_array_putter_factory
from ...fields.field_validators import nullable_entity_array_validator_factory
from ...fields.fields_common import parse_guild_id, put_guild_id__optional as put_guild_id, validate_guild_id

from ..soundboard_sound import SoundboardSound

# sounds

parse_sounds = nullable_entity_array_parser_factory('soundboard_sounds', SoundboardSound)
put_sounds = nullable_entity_array_putter_factory(
    'soundboard_sounds', SoundboardSound, force_include_internals = True
)
validate_sounds = nullable_entity_array_validator_factory('sounds', SoundboardSound)
