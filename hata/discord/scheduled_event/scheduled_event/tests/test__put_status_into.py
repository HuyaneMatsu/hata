import vampytest

from ..fields import put_status_into
from ..preinstanced import ScheduledEventStatus


def test__put_status_into():
    """
    Tests whether ``put_status_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (ScheduledEventStatus.none, False, {}),
        (ScheduledEventStatus.none, True, {'status': ScheduledEventStatus.active.none}),
        (ScheduledEventStatus.active, False, {'status': ScheduledEventStatus.active.value}),
    ):
        data = put_status_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
