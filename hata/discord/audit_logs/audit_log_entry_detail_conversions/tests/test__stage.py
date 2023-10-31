import vampytest

from ....stage.stage.fields import validate_channel_id

from ...conversion_helpers.converters import get_converter_id, put_converter_id

from ..stage import CHANNEL_ID_CONVERSION, STAGE_CONVERSIONS


def test__STAGE_CONVERSIONS():
    """
    Tests whether `STAGE_CONVERSIONS` contains conversion for every expected key.
    """
    vampytest.assert_eq(
        {*STAGE_CONVERSIONS.get_converters.keys()},
        {'channel_id',}
    )


# ---- channel_id ----

def test__CHANNEL_ID_CONVERSION__generic():
    """
    Tests whether ``CHANNEL_ID_CONVERSION`` works as intended.
    """
    vampytest.assert_is(CHANNEL_ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.validator, validate_channel_id)

