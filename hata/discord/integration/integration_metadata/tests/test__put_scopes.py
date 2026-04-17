import vampytest

from ....oauth2 import Oauth2Scope

from ..fields import put_scopes


def test__put_scopes():
    """
    Tests whether ``put_scopes`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {'scopes': []}),
        ((Oauth2Scope.bot, ), True, {'scopes': [Oauth2Scope.bot.value]}),
    ):
        data = put_scopes(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
