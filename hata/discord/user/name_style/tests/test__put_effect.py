import vampytest

from ..fields import put_effect
from ..preinstanced import NameStyleEffect


def _iter_options():
    yield (
        NameStyleEffect.none,
        False,
        {
            'effect_id': NameStyleEffect.none.value,
        },
    )
    
    yield (
        NameStyleEffect.none,
        True,
        {
            'effect_id': NameStyleEffect.none.value,
        },
    )
    
    yield (
        NameStyleEffect.pop,
        False,
        {
            'effect_id': NameStyleEffect.pop.value,
        },
    )
    
    yield (
        NameStyleEffect.pop,
        True,
        {
            'effect_id': NameStyleEffect.pop.value,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_effect(input_value, defaults):
    """
    Tests whether ``put_effect`` is working as intended.
    
    Parameters
    ----------
    input_value : ``NameStyleEffect``
        Input value.
    
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_effect(input_value, {}, defaults)
