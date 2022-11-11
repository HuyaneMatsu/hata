import vampytest

from ...interaction_component import InteractionComponent

from ..fields import parse_components


def test__parse_components():
    """
    Tests whether ``parse_components`` works as intended.
    """
    component = InteractionComponent(custom_id = 'requiem')
    
    for input_data, expected_output in (
        ({}, None),
        ({'components': None}, None),
        ({'components': []}, None),
        ({'components': [component.to_data()]}, (component, )),
    ):
        output = parse_components(input_data)
        vampytest.assert_eq(output, expected_output)
