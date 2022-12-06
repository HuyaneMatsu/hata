import vampytest

from ..fields import parse_type
from ..preinstanced import ApplicationRoleConnectionMetadataType


def test__parse_type():
    """
    Tests whether ``parse_type`` works as intended.
    """
    for input_data, expected_output in (
        (
            {'type': ApplicationRoleConnectionMetadataType.integer_equal.value},
            ApplicationRoleConnectionMetadataType.integer_equal,
        ),
    ):
        output = parse_type(input_data)
        vampytest.assert_is(output, expected_output)
