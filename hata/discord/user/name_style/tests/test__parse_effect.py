import vampytest

from ..fields import parse_effect
from ..preinstanced import NameStyleEffect


def _iter_options():
    yield (
        {},
        NameStyleEffect.none,
    )
    
    yield (
        {
            'effect_id': None,
        },
        NameStyleEffect.none,
    )
    
    yield (
        {
            'effect_id': NameStyleEffect.pop.value
        },
        NameStyleEffect.pop,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_effect(input_data):
    """
    Tests whether ``parse_effect`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``NameStyleEffect``
    """
    output = parse_effect(input_data)
    vampytest.assert_instance(output, NameStyleEffect)
    return output
