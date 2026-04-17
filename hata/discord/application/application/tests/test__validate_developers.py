import vampytest

from ...application_entity import ApplicationEntity

from ..fields import validate_developers


def test__validate_developers__0():
    """
    Tests whether ``validate_developers`` works as intended.
    
    Case: Passing.
    """
    application_entity = ApplicationEntity.precreate(202211270002)
    
    for input_parameter, expected_output in (
        (None, None),
        ([], None),
        ([application_entity], (application_entity, ))
    ):
        output = validate_developers(input_parameter)
        vampytest.assert_eq(output, expected_output)


def test__validate_developers__1():
    """
    Tests whether ``validate_developers`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        2.3,
        [2.3],
    ):
        with vampytest.assert_raises(TypeError):
            validate_developers(input_value)
