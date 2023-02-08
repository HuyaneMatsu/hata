import vampytest

from ..fields import put_scopes_into
from ..preinstanced import Oauth2Scope


def test__put_scopes_into():
    """
    Tests whether ``put_scopes_into`` works as intended.
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
        data = put_scopes_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
