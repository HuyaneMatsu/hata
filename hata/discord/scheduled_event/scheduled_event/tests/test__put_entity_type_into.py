import vampytest

from ..fields import put_entity_type_into
from ..preinstanced import ScheduledEventEntityType


def test__put_entity_type_into():
    """
    Tests whether ``put_entity_type_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (ScheduledEventEntityType.stage, False, {'entity_type': ScheduledEventEntityType.stage.value}),
    ):
        data = put_entity_type_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
