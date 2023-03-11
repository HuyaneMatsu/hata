import vampytest

from ..helpers import Oauth2Scope, build_joined_scopes


def test__build_joined_scopes__0():
    """
    Tests whether ``build_joined_scopes`` works as intended.
    
    cases: everything passes.
    """
    for input_value, expected_output in (
        ('bot', 'bot'),
        (Oauth2Scope.bot, 'bot'),
        (['bot'], 'bot'),
        ([Oauth2Scope.bot], 'bot'),
        (['email', Oauth2Scope.bot], 'email bot'),
    ):
        output = build_joined_scopes(input_value)
        vampytest.assert_eq(output, expected_output)


def test__build_joined_scopes__1():
    """
    Tests whether ``build_joined_scopes`` works as intended.
    
    cases: everything fails.
    """
    for input_value in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            build_joined_scopes(input_value)
