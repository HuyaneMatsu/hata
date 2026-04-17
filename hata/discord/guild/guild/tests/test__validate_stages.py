import vampytest

from ....stage import Stage

from ..fields import validate_stages


def test__validate_stages__0():
    """
    Tests whether ``validate_stages`` works as intended.
    
    Case: passing.
    """
    stage_id = 202306110006
    stage_topic = 'Koishi'
    
    stage = Stage.precreate(
        stage_id,
        topic = stage_topic,
    )
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ({}, None),
        ([stage], {stage_id: stage}),
        ({stage_id: stage}, {stage_id: stage}),
    ):
        output = validate_stages(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_stages__1():
    """
    Tests whether ``validate_stages`` works as intended.
    
    Case: raising.
    """
    for input_value in (
        12.6,
        [12.6],
        {12.6: 12.6},
    ):
        with vampytest.assert_raises(TypeError):
            validate_stages(input_value)
