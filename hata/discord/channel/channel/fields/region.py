__all__ = ()


from ....field_parsers import preinstanced_parser_factory
from ....field_putters import preinstanced_optional_putter_factory
from ....field_validators import preinstanced_validator_factory

from ..preinstanced import VoiceRegion


parse_region = preinstanced_parser_factory('rtc_region', VoiceRegion, VoiceRegion.unknown)
put_region_into = preinstanced_optional_putter_factory('rtc_region', VoiceRegion.unknown)
validate_region = preinstanced_validator_factory('region', VoiceRegion)
