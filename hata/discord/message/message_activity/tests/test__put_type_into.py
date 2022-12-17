import vampytest

from ..fields import put_type_into
from ..preinstanced import MessageActivityType


def test__put_type_into():
    """
    Tests whether ``put_type_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (MessageActivityType.none, True, {'type': MessageActivityType.none.value}),
        (MessageActivityType.join, False, {'type': MessageActivityType.join.value}),
    ):
        data = put_type_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
