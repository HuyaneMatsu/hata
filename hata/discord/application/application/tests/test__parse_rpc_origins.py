import vampytest

from ..fields import parse_rpc_origins


def test__parse_rpc_origins():
    """
    Tests whether ``parse_rpc_origins`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'rpc_origins': None}, None),
        ({'rpc_origins': []}, None),
        ({'rpc_origins': ['https://orindance.party/']}, ('https://orindance.party/', )),
    ):
        output = parse_rpc_origins(input_data)
        vampytest.assert_eq(output, expected_output)
