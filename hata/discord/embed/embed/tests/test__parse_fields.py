import vampytest

from ...embed_field import EmbedField

from ..fields import parse_fields


def test__parse_fields():
    """
    Tests whether ``parse_fields`` works as intended.
    """
    field_0 = EmbedField('komeiji', 'koishi')
    field_1 = EmbedField('komeiji', 'satori')
    
    for input_data, expected_output in (
        ({}, None),
        ({'fields': None}, None),
        ({'fields': []}, None),
        ({'fields': [field_0.to_data()]}, [field_0]),
        ({'fields': [field_0.to_data(), field_1.to_data()]}, [field_0, field_1]),
    ):
        output = parse_fields(input_data)
        vampytest.assert_eq(output, expected_output)
