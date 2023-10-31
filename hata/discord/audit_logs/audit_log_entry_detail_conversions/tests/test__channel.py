import vampytest

from ....channel.channel_metadata.fields import validate_status

from ...conversion_helpers.converters import get_converter_description, put_converter_description

from ..channel import CHANNEL_CONVERSIONS, STATUS_CONVERSION


def test__CHANNEL_CONVERSIONS():
    """
    Tests whether `CHANNEL_CONVERSIONS` contains conversion for every expected key.
    """
    vampytest.assert_eq(
        {*CHANNEL_CONVERSIONS.get_converters.keys()},
        {'status',}
    )


# ---- status ----

def test__STATUS_CONVERSION__generic():
    """
    Tests whether ``STATUS_CONVERSION`` works as intended.
    """
    vampytest.assert_is(STATUS_CONVERSION.get_converter, get_converter_description)
    vampytest.assert_is(STATUS_CONVERSION.put_converter, put_converter_description)
    vampytest.assert_is(STATUS_CONVERSION.validator, validate_status)
