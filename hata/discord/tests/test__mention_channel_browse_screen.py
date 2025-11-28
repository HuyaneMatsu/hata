import vampytest

from ..utils import mention_channel_browse_screen


def _iter_options():
    yield (
        '<id:browse>',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__mention_channel_browse_screen():
    """
    Tests whether ``mention_channel_browse_screen`` works as intended.
    
    Returns
    -------
    output : `str`
    """
    output = mention_channel_browse_screen()
    vampytest.assert_instance(output, str)
    return output
