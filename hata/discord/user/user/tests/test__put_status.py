import vampytest

from ..fields import put_status
from ..preinstanced import Status


def test__put_status():
    """
    Tests whether ``put_status`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (Status.online, False, {'status': Status.online.value}),
    ):
        data = put_status(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
