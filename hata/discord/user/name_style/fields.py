__all__ = ()

from ...color import Color
from ...field_parsers import nullable_functional_array_parser_factory, preinstanced_parser_factory
from ...field_putters import nullable_functional_array_optional_putter_factory, preinstanced_putter_factory
from ...field_validators import nullable_object_array_validator_factory, preinstanced_validator_factory

from .preinstanced import NameStyleEffect, NameStyleFont


# effect

parse_effect = preinstanced_parser_factory('effect_id', NameStyleEffect, NameStyleEffect.none)
put_effect = preinstanced_putter_factory('effect_id')
validate_effect = preinstanced_validator_factory('effect', NameStyleEffect)


# colors

parse_colors = nullable_functional_array_parser_factory('colors', lambda value : Color(value))
put_colors = nullable_functional_array_optional_putter_factory('colors', lambda color : int(color))
validate_colors = nullable_object_array_validator_factory('colors', Color)


# font

parse_font = preinstanced_parser_factory('font_id', NameStyleFont, NameStyleFont.default)
put_font = preinstanced_putter_factory('font_id')
validate_font = preinstanced_validator_factory('font', NameStyleFont)
