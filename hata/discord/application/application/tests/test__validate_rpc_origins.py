import vampytest

from ..fields import validate_rpc_origins


def test__validate_rpc_origins__0():
    """
    Tests whether `validate_rpc_origins` works as intended.
    
    Case: passing.
    """
    for input_rpc_origins, expected_output in (
        (None, None),
        ([], None),
        ('https://orindance.party/', ('https://orindance.party/',)),
        (['https://orindance.party/'], ('https://orindance.party/', )),
    ):
        output = validate_rpc_origins(input_rpc_origins)
        vampytest.assert_eq(output, expected_output)


def test__validate_rpc_origins__1():
    """
    Tests whether `validate_rpc_origins` works as intended.
    
    Case: `TypeError`.
    """
    for input_rpc_origins in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_rpc_origins(input_rpc_origins)


def test__validate_rpc_origins__2():
    """
    Tests whether `validate_rpc_origins` works as intended.
    
    Case: `ValueError`.
    """
    for input_rpc_origins in (
        '',
    ):
        with vampytest.assert_raises(ValueError):
            validate_rpc_origins(input_rpc_origins)
