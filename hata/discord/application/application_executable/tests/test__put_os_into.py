import vampytest

from ..fields import put_os_into
from ..preinstanced import OperationSystem


def test__put_os_into():
    """
    Tests whether ``put_os_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (OperationSystem.linux, True, {'os': OperationSystem.linux.value}),
    ):
        data = put_os_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
