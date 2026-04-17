import vampytest

from ...reaction_mapping_line import ReactionMappingLine

from ..fields import validate_reaction_mapping_line


def _iter_options__passing():
    line = ReactionMappingLine(count = 6)
    
    yield line, line


def _iter_options__type_error():
    yield None
    yield 12



@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_reaction_mapping_line__passing(input_value):
    """
    Tests whether ``validate_reaction_mapping_line`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``ReactionMappingLine``
    
    Raises
    ------
    TypeError
    """
    output = validate_reaction_mapping_line(input_value)
    vampytest.assert_instance(output, ReactionMappingLine)
    return output
