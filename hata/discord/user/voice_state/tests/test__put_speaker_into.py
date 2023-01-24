import vampytest

from ..fields import put_speaker_into


def test__put_speaker_into():
    """
    Tests whether ``put_speaker_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'suppress': True}),
        (True, False, {'suppress': False}),
    ):
        data = put_speaker_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
