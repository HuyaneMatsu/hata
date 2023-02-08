import vampytest

from ..fields import parse_type
from ..preinstanced import WebhookType


def test__parse_type():
    """
    Tests whether ``parse_type`` works as intended.
    """
    for input_data, expected_output in (
        ({}, WebhookType.none),
        ({'type': WebhookType.none.value}, WebhookType.none),
        ({'type': WebhookType.server.value}, WebhookType.server),
    ):
        output = parse_type(input_data)
        vampytest.assert_eq(output, expected_output)
