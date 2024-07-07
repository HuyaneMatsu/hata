import vampytest

from ..helpers import _merge_dictionaries


def _iter_options():
    yield [], None
    yield [None, None], None
    yield [None, {6: 7}], {6: 7}
    yield [{5: 6}, None], {5: 6}
    yield [{5: 6}, {6: 7}], {5: 6, 6: 7}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__merge_dictionaries(input_value):
    """
    Tests whether ``_merge_dictionaries`` works as intended.
    
    Parameters
    ----------
    input_value : `iterable<None | dict>`
        Value to test with.
    
    Returns
    -------
    output : `None | dict`
    """
    output = _merge_dictionaries(input_value)
    vampytest.assert_instance(output, dict, nullable = True)
    return output
