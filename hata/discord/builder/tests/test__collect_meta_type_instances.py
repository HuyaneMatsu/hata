import vampytest

from ..builder_base import _collect_meta_type_instances


def _iter_options():
    yield int, (), []
    yield int, ('', ''), []
    yield int, ('', 1), [1]
    yield int, (1, 2), [1, 2]


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__collect_meta_type_instances(meta_type, base_types):
    """
    Tests whether ``_collect_meta_type_instances`` works as intended.
    
    Parameters
    ----------
    meta_type : `type`
        Meta type to match.
    base_types : `tuple<type>`
        Types to filter from.
    
    Returns
    -------
    output : `list<type>`
    """
    return _collect_meta_type_instances(meta_type, base_types)
