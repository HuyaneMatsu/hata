__all__ = ()

from ...field_parsers import int_parser_factory, preinstanced_array_parser_factory
from ...field_putters import int_putter_factory, preinstanced_array_putter_factory
from ...field_validators import int_conditional_validator_factory, preinstanced_array_validator_factory
from ...guild import GuildFeature


# additional_emoji_slots

parse_additional_emoji_slots = int_parser_factory('additional_emoji_slots', 0)
put_additional_emoji_slots = int_putter_factory('additional_emoji_slots')
validate_additional_emoji_slots = int_conditional_validator_factory(
    'additional_emoji_slots',
    0,
    (lambda additional_emoji_slots : additional_emoji_slots >= 0),
    '>= 0',
)

# additional_soundboard_sound_slots

parse_additional_soundboard_sound_slots = int_parser_factory('additional_sound_slots', 0)
put_additional_soundboard_sound_slots = int_putter_factory('additional_sound_slots')
validate_additional_soundboard_sound_slots = int_conditional_validator_factory(
    'additional_soundboard_sound_slots',
    0,
    (lambda additional_soundboard_sound_slots : additional_soundboard_sound_slots >= 0),
    '>= 0',
)

# additional_sticker_slots

parse_additional_sticker_slots = int_parser_factory('additional_sticker_slots', 0)
put_additional_sticker_slots = int_putter_factory('additional_sticker_slots')
validate_additional_sticker_slots = int_conditional_validator_factory(
    'additional_sticker_slots',
    0,
    (lambda additional_sticker_slots : additional_sticker_slots >= 0),
    '>= 0',
)

# features

parse_features = preinstanced_array_parser_factory('features', GuildFeature)
put_features = preinstanced_array_putter_factory('features')
validate_features = preinstanced_array_validator_factory('features', GuildFeature)
