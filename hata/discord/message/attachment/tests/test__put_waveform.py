import vampytest

from ..fields import put_waveform


def test__put_waveform():
    """
    Tests whether ``put_waveform`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'waveform': ''}),
        ('a', False, {'waveform': 'a'}),
    ):
        data = put_waveform(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
