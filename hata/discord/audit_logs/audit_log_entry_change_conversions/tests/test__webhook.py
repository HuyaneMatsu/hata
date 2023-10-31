import vampytest

from ....bases import Icon
from ....user.user.fields import validate_name
from ....user.user.user_base import USER_AVATAR
from ....webhook.webhook.fields import validate_channel_id

from ...conversion_helpers.converters import get_converter_id, get_converter_name, put_converter_id, put_converter_name

from ..webhook import AVATAR_CONVERSION, CHANNEL_ID_CONVERSION, NAME_CONVERSION, WEBHOOK_CONVERSIONS


def test__WEBHOOK_CONVERSIONS():
    """
    Tests whether `WEBHOOK_CONVERSIONS` contains conversion for every expected key.
    """
    vampytest.assert_eq(
        {*WEBHOOK_CONVERSIONS.get_converters.keys()},
        {'avatar_hash', 'channel_id', 'name'},
    )


# ---- avatar ----

def test__AVATAR_CONVERSION__generic():
    """
    Tests whether ``AVATAR_CONVERSION`` works as intended.
    """
    vampytest.assert_eq(AVATAR_CONVERSION.get_converter, Icon.from_base_16_hash)
    vampytest.assert_eq(AVATAR_CONVERSION.put_converter, Icon.as_base_16_hash)
    vampytest.assert_eq(AVATAR_CONVERSION.validator, USER_AVATAR.validate_icon)


# ---- channel_id ----

def test__CHANNEL_ID_CONVERSION__generic():
    """
    Tests whether ``CHANNEL_ID_CONVERSION`` works as intended.
    """
    vampytest.assert_is(CHANNEL_ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.validator, validate_channel_id)


# ---- name ----

def test__NAME_CONVERSION__generic():
    """
    Tests whether ``NAME_CONVERSION`` works as intended.
    """
    vampytest.assert_is(NAME_CONVERSION.get_converter, get_converter_name)
    vampytest.assert_is(NAME_CONVERSION.put_converter, put_converter_name)
    vampytest.assert_is(NAME_CONVERSION.validator, validate_name)
