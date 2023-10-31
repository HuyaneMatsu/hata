import vampytest

from ....application_command.application_command.fields import validate_application_id

from ...conversion_helpers.converters import get_converter_id, put_converter_id

from ..application_command import APPLICATION_COMMAND_CONVERSIONS, APPLICATION_ID_CONVERSION


def test__APPLICATION_COMMAND_CONVERSIONS():
    """
    Tests whether `APPLICATION_COMMAND_CONVERSIONS` contains conversion for every expected key.
    """
    vampytest.assert_eq(
        {*APPLICATION_COMMAND_CONVERSIONS.get_converters.keys()},
        {'application_id',},
    )


# ---- application_id ----

def test__APPLICATION_ID_CONVERSION__generic():
    """
    Tests whether ``APPLICATION_ID_CONVERSION`` works as intended.
    """
    vampytest.assert_is(APPLICATION_ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(APPLICATION_ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(APPLICATION_ID_CONVERSION.validator, validate_application_id)
