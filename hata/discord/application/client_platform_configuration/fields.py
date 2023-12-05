__all__ = ()

from ...field_parsers import preinstanced_parser_factory, nullable_date_time_parser_factory
from ...field_putters import preinstanced_putter_factory, nullable_date_time_putter_factory
from ...field_validators import preinstanced_validator_factory, nullable_date_time_validator_factory

from .preinstanced import LabelType, ReleasePhase


# label_type

parse_label_type = preinstanced_parser_factory('label_type', LabelType, LabelType.none)
put_label_type_into = preinstanced_putter_factory('label_type')
validate_label_type = preinstanced_validator_factory('label_type', LabelType)

# labelled_until

parse_labelled_until = nullable_date_time_parser_factory('label_until')
put_labelled_until_into = nullable_date_time_putter_factory('label_until')
validate_labelled_until = nullable_date_time_validator_factory('label_until')

# release_phase

parse_release_phase = preinstanced_parser_factory('release_phase', ReleasePhase, ReleasePhase.global_launch)
put_release_phase_into = preinstanced_putter_factory('release_phase')
validate_release_phase = preinstanced_validator_factory('release_phase', ReleasePhase)
