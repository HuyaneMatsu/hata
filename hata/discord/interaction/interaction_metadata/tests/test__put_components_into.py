import vampytest

from ...interaction_component import InteractionComponent

from ..fields import put_components_into


def test__put_components_into():
    """
    Tests whether ``put_components_into`` is working as intended.
    """
    component = InteractionComponent(custom_id = 'overkill')
    
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'components': []}),
        ((component, ), False, {'components': [component.to_data()]}),
    ):
        data = put_components_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
