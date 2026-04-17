import vampytest

from ..constants import EXPIRE_GRACE_PERIOD_DEFAULT
from ..fields import parse_expire_grace_period


def test__parse_expire_grace_period():
    """
    Tests whether ``parse_expire_grace_period`` works as intended.
    """
    for input_data, expected_output in (
        ({}, EXPIRE_GRACE_PERIOD_DEFAULT),
        ({'expire_grace_period': None}, EXPIRE_GRACE_PERIOD_DEFAULT),
        ({'expire_grace_period': 1}, 1),
    ):
        output = parse_expire_grace_period(input_data)
        vampytest.assert_eq(output, expected_output)
