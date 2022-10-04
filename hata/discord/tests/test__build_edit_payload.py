import vampytest

from ..payload_building import build_edit_payload


def test__build_edit_payload():
    """
    Tests whether ``build_edit_payload`` works as intended.
    """
    class TestType:
        def __init__(self, old):
            self.old = old
        
        def to_data(self, *, defaults = False):
            data = {}
            
            old = self.old
            
            data['aya'] = 'aya'
            data['remi'] = 'lia'
            data['koishi'] = 'komeiji' if old else 'kokoro'
            
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
    
    for input_old_entity, input_new_entity, input_keyword_parameters, expected_output in (
        (
            TestType(True),
            TestType(False),
            keyword_parameters.copy(),
            {
                **keyword_parameters,
                'koishi': 'kokoro',
            },
        ), (
            TestType(True),
            TestType(False),
            {},
            {
                'koishi': 'kokoro',
            }
        ), (
            None,
            None,
            keyword_parameters.copy(),
            keyword_parameters.copy(),
        ), (
            None,
            None,
            {},
            {},
        ), (
            None,
            TestType(False),
            keyword_parameters.copy(),
            {
                **keyword_parameters,
                'remi': 'lia',
                'koishi': 'kokoro',
            },
        ), (
            None,
            TestType(False),
            None,
            {
                'aya': 'aya',
                'remi': 'lia',
                'koishi': 'kokoro',
            },
        )
    ):
        output = build_edit_payload(input_old_entity, input_new_entity, field_converters, input_keyword_parameters)
        vampytest.assert_eq(output, expected_output)
