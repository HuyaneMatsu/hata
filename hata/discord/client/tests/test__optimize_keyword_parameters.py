import vampytest

from ..client_wrapper import optimize_keyword_parameters


def _iter_options():
    yield {}, None
    yield {'name': ..., 'value': ...}, None
    yield {'name': ..., 'value': 'satori'}, {'value': 'satori'}
    yield {'name': 'koishi', 'value': ...}, {'name': 'koishi'}
    yield {'name': 'koishi', 'value': 'satori'}, {'name': 'koishi', 'value': 'satori'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__optimize_keyword_parameters(input_value):
    """
    Tests whether ``optimize_keyword_parameters`` works as intended.
    """
    return optimize_keyword_parameters(input_value)
