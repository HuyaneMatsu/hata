import vampytest

from ...application_entity import ApplicationEntity

from ..fields import validate_publishers


def test__validate_publishers_0():
    """
    Tests whether ``validate_publishers`` works as intended.
    
    Case: Passing.
    """
    application_entity = ApplicationEntity.precreate(202211270026)
    
    for input_parameter, expected_output in (
        (None, None),
        ([], None),
        ([application_entity], (application_entity, ))
    ):
        output = validate_publishers(input_parameter)
        vampytest.assert_eq(output, expected_output)


def test__validate_publishers__1():
    """
    Tests whether ``validate_publishers`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        2.3,
        [2.3],
    ):
        with vampytest.assert_raises(TypeError):
            validate_publishers(input_value)
