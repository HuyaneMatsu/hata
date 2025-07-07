import vampytest

from ..fields import put_additional_soundboard_sound_slots


def _iter_options():
    yield (
        0,
        False,
        {
            'additional_sound_slots': 0,
        },
    )
    
    yield (
        0,
        True,
        {
            'additional_sound_slots': 0,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_additional_soundboard_sound_slots(input_value, defaults):
    """
    Tests whether ``put_additional_soundboard_sound_slots`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_additional_soundboard_sound_slots(input_value, {}, defaults)
