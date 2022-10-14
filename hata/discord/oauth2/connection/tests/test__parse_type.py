import vampytest

from ..fields import parse_type
from ..preinstanced import ConnectionType


def test__parse_type():
    """
    Tests whether ``parse_type`` works as intended.
    """
    for input_data, expected_output in (
        ({'type': ConnectionType.github.value}, ConnectionType.github),
    ):
        output = parse_type(input_data)
        vampytest.assert_eq(output, expected_output)
