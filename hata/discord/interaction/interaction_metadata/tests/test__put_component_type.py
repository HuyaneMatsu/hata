import vampytest

from ....component import ComponentType

from ..fields import put_component_type


def test__put_component_type():
    """
    Tests whether ``put_component_type`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (ComponentType.none, False, {'component_type': ComponentType.none.value}),
        (ComponentType.button, False, {'component_type': ComponentType.button.value}),
        (ComponentType.button, True, {'component_type': ComponentType.button.value}),
    ):
        data = put_component_type(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
