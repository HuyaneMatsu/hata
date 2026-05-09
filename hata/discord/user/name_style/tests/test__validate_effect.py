import vampytest

from ..fields import validate_effect
from ..preinstanced import NameStyleEffect


def _iter_options__passing():
    yield None, NameStyleEffect.none
    yield NameStyleEffect.pop, NameStyleEffect.pop
    yield NameStyleEffect.pop.value, NameStyleEffect.pop


def _iter_options__effect_error():
    yield 12.6
    yield 'a'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__effect_error()).raising(TypeError))
def test__validate_effect(input_value):
    """
    Tests whether ``validate_effect`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``NameStyleEffect``
    
    Raises
    ------
    TypeError
    """
    output = validate_effect(input_value)
    vampytest.assert_instance(output, NameStyleEffect)
    return output
