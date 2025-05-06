import vampytest

from ..constants import EXPIRE_GRACE_PERIOD_DEFAULT
from ..fields import put_expire_grace_period


def test__put_default_auto_archive_after_into():
    """
    Tests whether ``put_expire_grace_period`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (EXPIRE_GRACE_PERIOD_DEFAULT, False, {}),
        (EXPIRE_GRACE_PERIOD_DEFAULT, True, {'expire_grace_period': EXPIRE_GRACE_PERIOD_DEFAULT}),
        (1, False, {'expire_grace_period': 1}),
    ):
        data = put_expire_grace_period(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
