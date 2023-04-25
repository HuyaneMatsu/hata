import vampytest

from ..fields import put_waveform_into


def test__put_waveform_into():
    """
    Tests whether ``put_waveform_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'waveform': ''}),
        ('a', False, {'waveform': 'a'}),
    ):
        data = put_waveform_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
