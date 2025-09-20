__all__ = ()

from ...field_parsers import nullable_string_parser_factory
from ...field_putters import nullable_string_optional_putter_factory
from ...field_validators import nullable_string_validator_factory

# image_large

parse_image_large = nullable_string_parser_factory('large_image')
put_image_large = nullable_string_optional_putter_factory('large_image')
validate_image_large = nullable_string_validator_factory('image_large', 0, 1024)


# image_small

parse_image_small = nullable_string_parser_factory('small_image')
put_image_small = nullable_string_optional_putter_factory('small_image')
validate_image_small = nullable_string_validator_factory('image_small', 0, 1024)


# text_large

parse_text_large = nullable_string_parser_factory('large_text')
put_text_large = nullable_string_optional_putter_factory('large_text')
validate_text_large = nullable_string_validator_factory('text_large', 0, 1024)


# url_large

parse_url_large = nullable_string_parser_factory('large_url')
put_url_large = nullable_string_optional_putter_factory('large_url')
validate_url_large = nullable_string_validator_factory('url_large', 0, 1024)


# text_small

parse_text_small = nullable_string_parser_factory('small_text')
put_text_small = nullable_string_optional_putter_factory('small_text')
validate_text_small = nullable_string_validator_factory('text_small', 0, 1024)


# url_small

parse_url_small = nullable_string_parser_factory('small_url')
put_url_small = nullable_string_optional_putter_factory('small_url')
validate_url_small = nullable_string_validator_factory('url_small', 0, 1024)
