import vampytest

from ....oauth2 import Oauth2Scope

from ..fields import validate_scopes


def test__validate_scopes__0():
    """
    Tests whether `validate_scopes` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([Oauth2Scope.bot], (Oauth2Scope.bot, )),
        ([Oauth2Scope.bot.value], (Oauth2Scope.bot, )),
    ):
        output = validate_scopes(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_scopes__1():
    """
    Tests whether `validate_scopes` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_scopes(input_value)
