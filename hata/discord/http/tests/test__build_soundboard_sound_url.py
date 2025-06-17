import vampytest

from ..urls import CDN_ENDPOINT, build_soundboard_sound_url


def _iter_options():
    sound_id = 202305240053
    yield (
        sound_id,
        f'{CDN_ENDPOINT}/soundboard-sounds/{sound_id}',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_soundboard_sound_url(sound_id):
    """
    Tests whether ``build_soundboard_sound_url`` works as intended.
    
    Parameters
    ----------
    sound_id : `int`
        Sound identifier to test with.
    
    Returns
    -------
    url : `str`
    """
    output = build_soundboard_sound_url(sound_id)
    vampytest.assert_instance(output, str)
    return output
