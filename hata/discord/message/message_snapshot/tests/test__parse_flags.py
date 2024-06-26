import vampytest

from ...message.flags import MessageFlag

from ..fields import parse_flags


def _iter_options():
    yield {}, MessageFlag(0)
    yield {'message': {}}, MessageFlag(0)
    yield {'message': {'flags': 1}}, MessageFlag(1)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_flags(input_data):
    """
    Tests whether ``parse_flags`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse the flags from.
    
    Returns
    -------
    output : ``MessageFlag``
    """
    output = parse_flags(input_data)
    vampytest.assert_instance(output, MessageFlag)
    return output
