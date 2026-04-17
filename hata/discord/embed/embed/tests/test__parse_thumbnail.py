import vampytest

from ...embed_thumbnail import EmbedThumbnail

from ..fields import parse_thumbnail


def test__parse_thumbnail():
    """
    Tests whether ``parse_thumbnail`` works as intended.
    """
    thumbnail = EmbedThumbnail(url = 'https://orindance.party/')
    
    for input_data, expected_output in (
        ({}, None),
        ({'thumbnail': None}, None),
        ({'thumbnail': thumbnail.to_data()}, thumbnail),
    ):
        output = parse_thumbnail(input_data)
        vampytest.assert_eq(output, expected_output)
