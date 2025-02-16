import vampytest

from ..fields import put_tts


def test__put_tts():
    """
    Tests whether ``put_tts`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'tts': False}),
        (True, False, {'tts': True}),
    ):
        data = put_tts(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
