__all__ = ()

from ....field_parsers import entity_id_array_parser_factory
from ....field_putters import entity_id_array_optional_putter_factory
from ....field_validators import entity_id_array_validator_factory

from ...forum_tag import ForumTag

parse_applied_tag_ids = entity_id_array_parser_factory('applied_tags')
put_applied_tag_ids_into = entity_id_array_optional_putter_factory('applied_tags')
validate_applied_tag_ids = entity_id_array_validator_factory('applied_tag_ids', ForumTag)
