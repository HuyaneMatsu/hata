import vampytest

from ....oauth2 import Oauth2Scope

from ..fields import put_scopes_into


def test__put_scopes_into():
    """
    Tests whether ``put_scopes_into`` works as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {'scopes': []}),
        ((Oauth2Scope.bot, ), True, {'scopes': [Oauth2Scope.bot.value]}),
    ):
        data = put_scopes_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
