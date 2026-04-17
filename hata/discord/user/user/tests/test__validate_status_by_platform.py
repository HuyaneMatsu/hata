import vampytest

from ...status_by_platform import Status, StatusByPlatform

from ..fields import validate_status_by_platform


def _iter_options__passing():
    status_by_platform = StatusByPlatform(
        mobile = Status.online,
    )
    
    yield None, None
    yield status_by_platform, status_by_platform


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_status_by_platform(input_value):
    """
    Tests whether `validate_status_by_platform` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``None | StatusByPlatform``
    """
    output = validate_status_by_platform(input_value)
    vampytest.assert_instance(output, StatusByPlatform, nullable = True)
    return output
