import vampytest

from ..application_command import APPLICATION_COMMAND_CONVERSIONS


def test__APPLICATION_COMMAND_CONVERSIONS():
    """
    Tests whether `APPLICATION_COMMAND_CONVERSIONS` contains conversion for every expected key.
    """
    vampytest.assert_eq(
        {*APPLICATION_COMMAND_CONVERSIONS.get_converters.keys()},
        set(),
    )

