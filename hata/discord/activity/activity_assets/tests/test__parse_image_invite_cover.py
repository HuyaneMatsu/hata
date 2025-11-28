import vampytest

from ..fields import parse_image_invite_cover


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'invite_cover_image': None,
        },
        None,
    )
    
    yield (
        {
            'invite_cover_image': '',
        },
        None,
    )
    
    yield (
        {
            'invite_cover_image': 'a',
        },
        'a',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_image_invite_cover(input_data):
    """
    Tests whether ``parse_image_invite_cover`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    output = parse_image_invite_cover(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output
