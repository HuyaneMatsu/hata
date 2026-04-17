import vampytest

from ..payload_building import add_payload_fields_from_keyword_parameters


def test__add_payload_fields_from_keyword_parameters():
    """
    Tests whether ``add_payload_fields_from_keyword_parameters`` works as intended.
    """
    initial_data = {
        'field': 'value',
        'aya': 'ya',
    }
    
    expected_final_data_with_defaults = {
        'field': 'field_value',
        'aya': 'ya',
        'kei': 'nana',
    }
    
    expected_final_data_without_defaults = {
        'field': 'field_value',
        'aya': 'ya',
    }
    
    keyword_parameters = {
        'field': 'field_value',
        'kei': 'na',
    }
    
    def field_validator(field_value):
        return field_value
    
    def field_putter(field_value, data, defaults):
        data['field'] = field_value
    
    def kei_validator(kei):
        return kei * 2
    
    def ke_putter(field_value, data, defaults):
        if defaults:
            data['kei'] = field_value
    
    field_converters = {
        'field': (field_validator, field_putter),
        'kei': (kei_validator, ke_putter),
    }
    
    for expected_output, defaults in (
        (expected_final_data_with_defaults, True),
        (expected_final_data_without_defaults, False),
    ):
        test_data = initial_data.copy()
        add_payload_fields_from_keyword_parameters(field_converters, keyword_parameters.copy(), test_data, defaults)
        
        vampytest.assert_eq(test_data, expected_output)
