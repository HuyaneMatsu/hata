import vampytest

from ....guild.guild.guild_boost_perks import LEVEL_0

from ..fields import parse_attachment_size_limit


def _iter_options():
    yield {}, LEVEL_0.attachment_size_limit
    yield {'attachment_size_limit': None}, LEVEL_0.attachment_size_limit
    yield {'attachment_size_limit': 1}, 1


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_attachment_size_limit(input_data):
    """
    Tests whether ``parse_attachment_size_limit`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_attachment_size_limit(input_data)
    vampytest.assert_instance(output, int)
    return output
