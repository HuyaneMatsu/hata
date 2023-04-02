import vampytest

from ...embed_field import EmbedField

from ..constants import EMBED_FIELDS_LENGTH_MAX
from ..fields import validate_fields


def test__validate_fields__0():
    """
    Tests whether ``validate_fields`` works as intended.
    
    Case: passing.
    """
    field = EmbedField('komeiji', 'koishi')
    
    for input_value, expected_output in (
        ([], None),
        ([field], [field]),
        (None, None),
        ([field] * (EMBED_FIELDS_LENGTH_MAX + 1), [field] * (EMBED_FIELDS_LENGTH_MAX + 1)),
    ):
        output = validate_fields(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_fields__1():
    """
    Tests whether ``validate_fields`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.5,
        [12.6,]
    ):
        with vampytest.assert_raises(TypeError):
            validate_fields(input_value)
