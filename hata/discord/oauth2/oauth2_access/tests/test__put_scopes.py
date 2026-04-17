import vampytest

from ..fields import put_scopes
from ..preinstanced import Oauth2Scope


def test__put_scopes():
    """
    Tests whether ``put_scopes`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {'scope': ''}),
        ((Oauth2Scope.bot, ), True, {'scope': Oauth2Scope.bot.value}),
        (
            (Oauth2Scope.bot, Oauth2Scope.email),
            True,
            {'scope': ' '.join([Oauth2Scope.bot.value, Oauth2Scope.email.value])},
        ),
    ):
        data = put_scopes(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
