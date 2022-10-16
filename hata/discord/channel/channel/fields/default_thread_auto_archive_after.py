__all__ = ()

from ....field_parsers import int_postprocess_parser_factory
from ....field_putters import int_optional_postprocess_putter_factory
from ....field_validators import int_options_validator_factory

from ..constants import AUTO_ARCHIVE_DEFAULT, AUTO_ARCHIVE_OPTIONS


parse_default_thread_auto_archive_after = int_postprocess_parser_factory(
    'default_auto_archive_duration',
    AUTO_ARCHIVE_DEFAULT,
    (lambda default_thread_auto_archive_after: default_thread_auto_archive_after * 60),
)
put_default_thread_auto_archive_after_into = int_optional_postprocess_putter_factory(
    'default_auto_archive_duration',
    AUTO_ARCHIVE_DEFAULT,
    (lambda default_thread_auto_archive_after: default_thread_auto_archive_after // 60),
)
validate_default_thread_auto_archive_after = int_options_validator_factory(
    'default_thread_auto_archive_after', AUTO_ARCHIVE_OPTIONS
)
