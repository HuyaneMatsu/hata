import vampytest

from ...embed_provider import EmbedProvider

from ..fields import parse_provider


def test__parse_provider():
    """
    Tests whether ``parse_provider`` works as intended.
    """
    provider = EmbedProvider(name = 'hell')
    
    for input_data, expected_output in (
        ({}, None),
        ({'provider': None}, None),
        ({'provider': provider.to_data()}, provider),
    ):
        output = parse_provider(input_data)
        vampytest.assert_eq(output, expected_output)
