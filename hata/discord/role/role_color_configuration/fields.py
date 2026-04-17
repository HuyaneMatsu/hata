__all__ = ()

from ...field_parsers import flag_parser_factory, nullable_flag_parser_factory
from ...field_putters import flag_optional_putter_factory, nullable_flag_optional_putter_factory
from ...field_validators import flag_validator_factory, nullable_flag_validator_factory
from ...color import Color

# primary

parse_color_primary = flag_parser_factory('primary_color', Color)
put_color_primary = flag_optional_putter_factory('primary_color', Color())
validate_color_primary = flag_validator_factory('color_primary', Color)


# secondary

parse_color_secondary = nullable_flag_parser_factory('secondary_color', Color)
put_color_secondary = nullable_flag_optional_putter_factory('secondary_color')
validate_color_secondary = nullable_flag_validator_factory('color_secondary', Color)


# tertiary

parse_color_tertiary = nullable_flag_parser_factory('tertiary_color', Color)
put_color_tertiary = nullable_flag_optional_putter_factory('tertiary_color')
validate_color_tertiary = nullable_flag_validator_factory('color_tertiary', Color)
