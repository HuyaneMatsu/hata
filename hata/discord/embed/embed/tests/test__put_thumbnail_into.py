import vampytest

from ...embed_thumbnail import EmbedThumbnail

from ..fields import put_thumbnail_into


def test__put_thumbnail_into():
    """
    Tests whether ``put_thumbnail_into`` is working as intended.
    """
    thumbnail = EmbedThumbnail(url = 'https://orindance.party/')
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (thumbnail, False, {'thumbnail': thumbnail.to_data()}),
        (thumbnail, True, {'thumbnail': thumbnail.to_data(defaults = True)}),
    ):
        data = put_thumbnail_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
