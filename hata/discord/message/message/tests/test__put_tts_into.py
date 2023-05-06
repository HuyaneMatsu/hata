import vampytest

from ..fields import put_tts_into


def test__put_tts_into():
    """
    Tests whether ``put_tts_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'tts': False}),
        (True, False, {'tts': True}),
    ):
        data = put_tts_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
