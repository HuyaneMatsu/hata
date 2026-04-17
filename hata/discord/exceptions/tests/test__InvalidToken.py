import vampytest

from ..invalid_token import InvalidToken


def test__InvalidToken__new():
    """
    Tests whether ``InvalidToken.__new__`` works as intended.
    """
    exception = InvalidToken()
    vampytest.assert_instance(exception, BaseException)
    vampytest.assert_instance(exception, InvalidToken)
    
    vampytest.assert_eq(len(exception.args), 1)
    vampytest.assert_instance(exception.args[0], str)
