from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_boosts_since


def test__parse_boosts_since():
    """
    Tests whether ``parse_boosts_since`` works as intended.
    """
    boosts_since = DateTime(2016, 5, 14)
    
    for input_value, expected_output in (
        ({}, None),
        ({'premium_since': None}, None),
        ({'premium_since': datetime_to_timestamp(boosts_since)}, boosts_since),
    ):
        output = parse_boosts_since(input_value)
        vampytest.assert_eq(output, expected_output)
