import vampytest

from ...embed_provider import EmbedProvider

from ..fields import validate_provider


def test__validate_provider__0():
    """
    Tests whether `validate_provider` works as intended.
    
    Case: passing.
    """
    provider = EmbedProvider(name = 'hell')
    
    for input_value, expected_output in (
        (None, None),
        (provider, provider),
    ):
        output = validate_provider(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_provider__1():
    """
    Tests whether `validate_provider` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_provider(input_value)
