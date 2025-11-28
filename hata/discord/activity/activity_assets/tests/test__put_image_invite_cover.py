import vampytest

from ..fields import put_image_invite_cover


def _iter_options():
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'invite_cover_image': '',
        },
    )
    
    yield (
        'a',
        False,
        {
            'invite_cover_image': 'a',
        },
    )
    
    yield (
        'a',
        True,
        {
            'invite_cover_image': 'a',
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_image_invite_cover(input_value, defaults):
    """
    Tests whether ``put_image_invite_cover`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Value to serialize.
    
    defaults : `bool`
        Whether values of their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_image_invite_cover(input_value, {}, defaults)
