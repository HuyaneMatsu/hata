import vampytest

from ..utils import normalize_description


def _iter_options():
    yield None, None
    yield '', None
    yield '\n\n\n', None
    
    yield 'I should show up.', 'I should show up.'
    yield 'I should show up.\nMe too', 'I should show up. Me too'
    yield '\nI should show up.\nMe too\n', 'I should show up. Me too'
    yield 'I should show up.    \nMe too', 'I should show up. Me too'
    yield '\n    I should show up.\n    Me too\n    ', 'I should show up. Me too'
    yield '\n    I should show up.\n\n    Me not\n    ', 'I should show up.'
    yield '\n    I should show up.\n    \n    Me not\n    ', 'I should show up.'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__normalize_description(input_value):
    """
    Tests whether ``normalize_description`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Value to test on.
    
    Returns
    -------
    output : `None | str`
    """
    output = normalize_description(input_value)
    vampytest.assert_instance(output, str, nullable = True)
    return output
