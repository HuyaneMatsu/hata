import vampytest

from ....user import User

from ..fields import validate_author_ids


def _iter_options__passing():
    author_id_0 = 202601030010
    author_id_1 = 202601030011
    
    author_0 = User.precreate(author_id_0)
    author_1 = User.precreate(author_id_1)
    
    yield (
        None,
        None,
    )
    
    yield (
        [],
        None,
    )
    
    yield (
        [
            author_id_0,
            author_id_1,
        ],
        (
            author_id_0,
            author_id_1,
        ),
    )
    
    yield (
        [
            author_id_1,
            author_id_0,
        ],
        (
            author_id_0,
            author_id_1,
        ),
    )
    
    yield (
        [
            author_0,
            author_1,
        ],
        (
            author_id_0,
            author_id_1,
        )
    )
    
    yield (
        [
            author_1,
            author_0,
        ],
        (
            author_id_0,
            author_id_1,
        ),
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_author_ids(input_value):
    """
    Tests whether `validate_author_ids` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<int>`
    
    Raises
    ------
    TypeError
    """
    output = validate_author_ids(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, int)
    
    return output
