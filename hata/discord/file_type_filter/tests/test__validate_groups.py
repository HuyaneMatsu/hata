import vampytest

from ..fields import validate_groups
from ..preinstanced import FileTypeFilterGroup


def _iter_options__passing():
    yield (
        None,
        None,
    )
    
    yield (
        [],
        None,
    )
    
    yield (
        FileTypeFilterGroup.audio,
        (FileTypeFilterGroup.audio, ),
    )
    
    yield (
        FileTypeFilterGroup.audio.value,
        (FileTypeFilterGroup.audio, ),
    )
    
    yield (
        [FileTypeFilterGroup.audio],
        (FileTypeFilterGroup.audio, ),
    )
    
    yield (
        [FileTypeFilterGroup.audio.value],
        (FileTypeFilterGroup.audio, ),
    )
    
    yield (
        [FileTypeFilterGroup.audio, FileTypeFilterGroup.image],
        (FileTypeFilterGroup.audio, FileTypeFilterGroup.image,),
    )
    yield (
        [FileTypeFilterGroup.image, FileTypeFilterGroup.audio],
        (FileTypeFilterGroup.audio, FileTypeFilterGroup.image,),
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_groups(input_value):
    """
    Tests whether `validate_groups` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``None | tuple<FileTypeFilterGroup>``
    
    Raises
    ------
    TypeError
    """
    output = validate_groups(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, FileTypeFilterGroup)
    return output
