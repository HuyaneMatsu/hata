import vampytest

from ..fields import put_type_into
from ..preinstanced import MessageType


def test__put_type_into():
    """
    Tests whether ``put_type_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (MessageType.call, False, {'type': MessageType.call.value}),
    ):
        data = put_type_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
