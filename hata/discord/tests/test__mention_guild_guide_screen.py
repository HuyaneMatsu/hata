import vampytest

from ..utils import mention_guild_guide_screen


def _iter_options():
    yield (
        '<id:guide>',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__mention_guild_guide_screen():
    """
    Tests whether ``mention_guild_guide_screen`` works as intended.
    
    Returns
    -------
    output : `str`
    """
    output = mention_guild_guide_screen()
    vampytest.assert_instance(output, str)
    return output
