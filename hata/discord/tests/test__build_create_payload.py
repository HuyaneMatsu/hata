import vampytest

from ..payload_building import build_create_payload


def test__build_create_payload():
    """
    Tests whether ``build_create_payload`` works as intended.
    """
    class TestType:
        def to_data(self, *, defaults = False):
            data = {}
            
            data['aya'] = 'aya'
            data['remi'] = 'lia'
            
            return data
    
    keyword_parameters = {
        'aya' : 'ayaya',
        'sakuya': 'tea',
    }
    
    
    def aya_validator(aya):
        return aya
    
    def aya_putter(aya, data, defaults):
        data['aya'] = aya
    
    def sakuya_validator(sakuya):
        return sakuya
    
    def sakuya_putter(sakuya, data, defaults):
        data['sakuya'] = 'tea'
    
    field_converters = {
        'aya' : (aya_validator, aya_putter),
        'sakuya': (sakuya_validator, sakuya_putter),
    }
    
    for input_entity, input_keyword_parameters, expected_output in (
        (
            TestType(),
            keyword_parameters.copy(),
            {
                **keyword_parameters,
                'remi': 'lia',
            },
        ), (
            TestType(),
            {},
            {
                'aya': 'aya',
                'remi': 'lia',
            }
        ), (
            None,
            keyword_parameters.copy(),
            keyword_parameters.copy(),
        ), (
            None,
            {},
            {},
        ),
    ):
        output = build_create_payload(input_entity, field_converters, input_keyword_parameters)
        vampytest.assert_eq(output, expected_output)
