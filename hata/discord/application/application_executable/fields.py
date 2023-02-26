__all__ = ()

from ...field_parsers import (
    bool_parser_factory, force_string_parser_factory, nullable_string_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, force_string_putter_factory, nullable_string_putter_factory,
    preinstanced_putter_factory
)
from ...field_validators import (
    bool_validator_factory, force_string_validator_factory, nullable_string_validator_factory,
    preinstanced_validator_factory
)

from .preinstanced import OperationSystem

# launcher

parse_launcher = bool_parser_factory('is_launcher', False)
put_launcher_into = bool_optional_putter_factory('is_launcher', False)
validate_launcher = bool_validator_factory('launcher', False)

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', 0, 1024)

# os

parse_os = preinstanced_parser_factory('os', OperationSystem, OperationSystem.none)
put_os_into = preinstanced_putter_factory('os')
validate_os = preinstanced_validator_factory('os', OperationSystem)

# parameters

parse_parameters = nullable_string_parser_factory('parameters')
put_parameters_into = nullable_string_putter_factory('parameters')
validate_parameters = nullable_string_validator_factory('parameters', 0, 1024)
