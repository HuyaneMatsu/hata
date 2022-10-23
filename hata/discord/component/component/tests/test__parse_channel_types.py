import vampytest

from ....channel import ChannelType

from ..fields import parse_channel_types


def test__parse_channel_types():
    """
    Tests whether ``parse_channel_types`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'channel_types': None}, None),
        ({'channel_types': []}, None),
        ({'channel_types': [ChannelType.private.value]}, (ChannelType.private.value,)),
    ):
        output = parse_channel_types(input_data)
        vampytest.assert_eq(output, expected_output)
