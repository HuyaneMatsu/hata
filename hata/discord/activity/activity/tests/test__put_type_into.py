import vampytest

from ..fields import put_type_into
from ..preinstanced import ActivityType


def test__put_type_into():
    """
    Tests whether ``put_type_into`` works as intended.
    """
    for input_, defaults, expected_output in (
        (ActivityType.competing, False, {'type': ActivityType.competing.value}),
    ):
        data = put_type_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
