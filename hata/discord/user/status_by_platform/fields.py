__all__ = ()

from ...field_parsers import preinstanced_parser_factory
from ...field_putters import preinstanced_optional_putter_factory
from ...field_validators import preinstanced_validator_factory

from .preinstanced import SessionPlatformType, Status


# desktop

parse_desktop = preinstanced_parser_factory('desktop', Status, Status.offline)
put_desktop = preinstanced_optional_putter_factory('desktop', Status.offline)
validate_desktop = preinstanced_validator_factory('desktop', Status)


# embedded

parse_embedded = preinstanced_parser_factory('embedded', Status, Status.offline)
put_embedded = preinstanced_optional_putter_factory('embedded', Status.offline)
validate_embedded = preinstanced_validator_factory('embedded', Status)


# mobile

parse_mobile = preinstanced_parser_factory('mobile', Status, Status.offline)
put_mobile = preinstanced_optional_putter_factory('mobile', Status.offline)
validate_mobile = preinstanced_validator_factory('mobile', Status)


# platform

validate_platform = preinstanced_validator_factory('platform', SessionPlatformType)


# web

parse_web = preinstanced_parser_factory('web', Status, Status.offline)
put_web = preinstanced_optional_putter_factory('web', Status.offline)
validate_web = preinstanced_validator_factory('web', Status)
