import vampytest

from ..preinstance import Preinstance
from ..preinstanced_meta import _pop_items_to_post_instantiate


def _iter_options():
    yield (
        {},
        (
            {},
            [],
        )
    )
    
    yield (
        {
            'hello': 'mister',
            'satori': Preinstance(12, 'sato'),
            'koishi': Preinstance(12, 'koi'),
        },
        (
            {
                'hello': 'mister',
            },
            [
                ('satori', Preinstance(12, 'sato')),
                ('koishi', Preinstance(12, 'koi')),
            ],
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__pop_items_to_post_instantiate(type_attributes):
    """
    Tests whether ``_pop_items_to_post_instantiate`` works as intended.
    
    Parameters
    ----------
    type_attributes : `dict<str, object>`
        The defined attributes of the type.
    
    Returns
    -------
    type_attributes : `dict<str, object>`
    output : `list<(str, Preinstance)>`
    """
    type_attributes = type_attributes.copy()
    output = _pop_items_to_post_instantiate(type_attributes)
    vampytest.assert_instance(output, list)
    return type_attributes, output
