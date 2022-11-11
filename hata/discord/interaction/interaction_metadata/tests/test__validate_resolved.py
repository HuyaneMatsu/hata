import vampytest

from ....message import Attachment

from ...resolved import Resolved

from ..fields import validate_resolved


def test__validate_resolved__0():
    """
    Tests whether ``validate_resolved`` works as intended.
    
    Case: Passing.
    """
    entity_id = 202211050043
    resolved = Resolved(attachments = [Attachment.precreate(entity_id)])
    
    for input_value, expected_output in (
        (None, None),
        (resolved, resolved),
    ):
        output = validate_resolved(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_resolved__1():
    """
    Tests whether ``validate_resolved`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_resolved(input_value)
