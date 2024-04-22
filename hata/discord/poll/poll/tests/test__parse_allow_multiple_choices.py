import vampytest

from ..fields import parse_allow_multiple_choices


def _iter_options():
    yield {}, False
    yield {'allow_multiselect': None}, False
    yield {'allow_multiselect': False}, False
    yield {'allow_multiselect': True}, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_allow_multiple_choices(input_data):
    """
    Tests whether ``parse_allow_multiple_choices`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    output = parse_allow_multiple_choices(input_data)
    vampytest.assert_instance(output, bool)
    return output
