import vampytest

from ..fields import put_default_sort_order_into
from ..preinstanced import SortOrder


def test__put_default_sort_order_into():
    """
    Tests whether ``put_default_sort_order_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (SortOrder.latest_activity, False, {}),
        (SortOrder.latest_activity, True, {'default_sort_order': SortOrder.latest_activity.value}),
        (SortOrder.creation_date, False, {'default_sort_order': SortOrder.creation_date.value}),
    ):
        data = put_default_sort_order_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
