import vampytest

from ...core import USERS
from .. import ZEROUSER


def test__ZEROUSER():
    """
    Tests whether zerouser is cached.
    """
    vampytest.assert_in(ZEROUSER.id, USERS)
    vampytest.assert_is(USERS[ZEROUSER.id], ZEROUSER)
