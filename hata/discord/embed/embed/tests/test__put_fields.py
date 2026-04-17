import vampytest

from ...embed_field import EmbedField

from ..fields import put_fields


def test__put_fields():
    """
    Tests whether ``put_fields`` works as intended.
    """
    field_0 = EmbedField('komeiji', 'koishi')
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'fields': []}),
        ([field_0], True, {'fields': [field_0.to_data(defaults = True)]}),
    ):
        output = put_fields(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
