import vampytest

from ..utils import mention_channel_and_roles_screen


def _iter_options():
    yield (
        '<id:customize>',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__mention_channel_and_roles_screen():
    """
    Tests whether ``mention_channel_and_roles_screen`` works as intended.
    
    Returns
    -------
    output : `str`
    """
    output = mention_channel_and_roles_screen()
    vampytest.assert_instance(output, str)
    return output
