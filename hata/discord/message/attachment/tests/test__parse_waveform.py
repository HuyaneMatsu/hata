import vampytest

from ..fields import parse_waveform


def test__parse_waveform():
    """
    Tests whether ``parse_waveform`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'waveform': None}, None),
        ({'waveform': ''}, None),
        ({'waveform': 'a'}, 'a'),
    ):
        output = parse_waveform(input_data)
        vampytest.assert_eq(output, expected_output)
