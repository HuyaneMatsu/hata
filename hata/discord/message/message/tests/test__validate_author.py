import vampytest

from ....user import User
from ....webhook import Webhook

from ..fields import validate_author


def test__validate_author__0():
    """
    Tests whether `validate_author` works as intended.
    
    Case: passing.
    """
    user = User.precreate(202304280047, name = 'Keine')
    webhook = Webhook.precreate(202304280048, name = 'Keine')
    
    for input_value, expected_output in (
        (user, user),
        (webhook, webhook),
    ):
        output = validate_author(input_value)
        vampytest.assert_is(output, expected_output)


def test__validate_author__1():
    """
    Tests whether `validate_author` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        'a',
    ):
        with vampytest.assert_raises(TypeError):
            validate_author(input_value)
