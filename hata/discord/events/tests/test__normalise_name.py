import vampytest

from ..handling_helpers import normalise_name


def _iter_options():
    yield 'NameCacher', 'name_cacher'
    yield 'NAMECacher', 'name_cacher'
    yield 'name693', 'name_693'
    yield '514koishi', '514_koishi'
    yield 'NYAN_NYAN', 'nyan_nyan'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__normalise_name(name):
    """
    Tests whether ``normalise_name`` works as intended.
    
    Parameters
    ----------
    name : `str`
        The name to normalise.
    
    Returns
    -------
    output : `str`
    """
    output = normalise_name(name)
    vampytest.assert_instance(output, str)
    return output
