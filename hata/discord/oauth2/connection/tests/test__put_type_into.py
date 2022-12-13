import vampytest

from ..fields import put_type_into
from ..preinstanced import ConnectionType


def test__put_type_into():
    """
    Tests whether ``put_type_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (ConnectionType.unknown, True, {'type': ConnectionType.unknown.value}),
        (ConnectionType.github, False, {'type': ConnectionType.github.value}),
    ):
        data = put_type_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)