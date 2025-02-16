__all__ = ()

from ...field_parsers import (
    int_parser_factory, nullable_array_parser_factory, nullable_date_time_parser_factory,
    nullable_entity_array_parser_factory, preinstanced_array_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    int_optional_putter_factory, int_putter_factory, nullable_date_time_optional_putter_factory,
    nullable_entity_array_optional_putter_factory, nullable_value_array_optional_putter_factory,
    preinstanced_array_optional_putter_factory, preinstanced_putter_factory
)
from ...field_validators import (
    int_conditional_validator_factory, nullable_date_time_validator_factory, nullable_entity_array_validator_factory,
    nullable_sorted_int_array_conditional_validator_factory, preinstanced_array_validator_factory,
    preinstanced_validator_factory
)

from ..schedule_nth_weeks_day import ScheduleNthWeeksDay, ScheduleWeeksDay

from .preinstanced import ScheduleFrequency, ScheduleMonth


# by_month_days

parse_by_month_days = nullable_array_parser_factory('by_month_day')
put_by_month_days = nullable_value_array_optional_putter_factory('by_month_day')
validate_by_month_days = nullable_sorted_int_array_conditional_validator_factory(
    'by_month_days',
    (lambda month_day : month_day >= 1 and month_day <= 31),
    '>= 1 and <= 31',
)


# by_months

parse_by_months = preinstanced_array_parser_factory('by_month', ScheduleMonth)
put_by_months = preinstanced_array_optional_putter_factory('by_month')
validate_by_months = preinstanced_array_validator_factory('by_months', ScheduleMonth)


# by_nth_weeks_days

parse_by_nth_weeks_days = nullable_entity_array_parser_factory('by_n_weekday', ScheduleNthWeeksDay)
put_by_nth_weeks_days = nullable_entity_array_optional_putter_factory('by_n_weekday', ScheduleNthWeeksDay)
validate_by_nth_weeks_days = nullable_entity_array_validator_factory('by_nth_weeks_days', ScheduleNthWeeksDay)


# by_weeks_days

parse_by_weeks_days = preinstanced_array_parser_factory('by_weekday', ScheduleWeeksDay)
put_by_weeks_days = preinstanced_array_optional_putter_factory('by_weekday')
validate_by_weeks_days = preinstanced_array_validator_factory('by_weeks_days', ScheduleWeeksDay)


# by_year_days

parse_by_year_days = nullable_array_parser_factory('by_year_day')
put_by_year_days = nullable_value_array_optional_putter_factory('by_year_day')
validate_by_year_days = nullable_sorted_int_array_conditional_validator_factory(
    'by_year_days',
    (lambda year_day : year_day >= 1 and year_day <= 366),
    '>= 1 and <= 366',
)


# end

parse_end = nullable_date_time_parser_factory('end')
put_end = nullable_date_time_optional_putter_factory('end')
validate_end = nullable_date_time_validator_factory('end')


# frequency

parse_frequency = preinstanced_parser_factory('frequency', ScheduleFrequency, ScheduleFrequency.yearly)
put_frequency = preinstanced_putter_factory('frequency')
validate_frequency = preinstanced_validator_factory('frequency', ScheduleFrequency)


# occurrence_count_limit

parse_occurrence_count_limit = int_parser_factory('count', 0)
put_occurrence_count_limit = int_optional_putter_factory('count', 0)
validate_occurrence_count_limit = int_conditional_validator_factory(
    'occurrence_count_limit',
    0,
    (lambda count : count >= 0),
    f'>= 0'
)


# occurrence_spacing

parse_occurrence_spacing = int_parser_factory('interval', 1)
put_occurrence_spacing = int_putter_factory('interval')
validate_occurrence_spacing = int_conditional_validator_factory(
    'occurrence_spacing',
    1,
    (lambda interval : interval >= 1),
    f'>= 1'
)


# start

parse_start = nullable_date_time_parser_factory('start')
put_start = nullable_date_time_optional_putter_factory('start')
validate_start = nullable_date_time_validator_factory('start')
