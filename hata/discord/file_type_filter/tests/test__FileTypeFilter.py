import vampytest

from ..file_type_filter import (
    FileTypeFilter, file_type_filter_convert_to_data, file_type_filter_create, file_type_filter_create_from_data
)
from ..preinstanced import FileTypeFilterGroup


def assert_file_type_filter_fields_set(file_type_filter):
    """
    Asserts whether every fields are set of the file type.
    
    Parameters
    ----------
    file_type_filter : ``FileTypeFilter``
        The instance to check.
    """
    vampytest.assert_instance(file_type_filter, FileTypeFilter)
    vampytest.assert_instance(file_type_filter.groups, tuple, nullable = True)
    vampytest.assert_instance(file_type_filter.individuals, tuple, nullable = True)
    

def test__FileTypeFilter__repr():
    """
    Tests whether ``FileTypeFilter.__repr__`` works as intended.
    """
    groups = [FileTypeFilterGroup.audio, FileTypeFilterGroup.image]
    individuals = ['rms', 'txt']
    
    file_type_filter = file_type_filter_create(
        groups = groups,
        individuals = individuals,
    )
    
    output = repr(file_type_filter)
    vampytest.assert_instance(output, str)


def test__FileTypeFilter__hash():
    """
    Tests whether ``FileTypeFilter.__hash__`` works as intended.
    """
    groups = [FileTypeFilterGroup.audio, FileTypeFilterGroup.image]
    individuals = ['rms', 'txt']
    
    file_type_filter = file_type_filter_create(
        groups = groups,
        individuals = individuals,
    )
    
    output = hash(file_type_filter)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    groups = [FileTypeFilterGroup.audio, FileTypeFilterGroup.image]
    individuals = ['rms', 'txt']
    
    keyword_parameters = {
        'groups': groups,
        'individuals': individuals,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'groups': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'individuals': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__FileTypeFilter__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``FileTypeFilter.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    guild_profile_0 = file_type_filter_create(**keyword_parameters_0)
    guild_profile_1 = file_type_filter_create(**keyword_parameters_1)
    
    output = guild_profile_0 == guild_profile_1
    vampytest.assert_instance(output, bool)
    return output


def test__file_type_filter_create():
    """
    Tests whether ``file_type_filter_create`` works as intended.
    """
    groups = [FileTypeFilterGroup.audio, FileTypeFilterGroup.image]
    individuals = ['rms', 'txt']
    
    file_type_filter = file_type_filter_create(
        groups = groups,
        individuals = individuals,
    )
    assert_file_type_filter_fields_set(file_type_filter)
    
    vampytest.assert_eq(file_type_filter.groups, tuple(groups))
    vampytest.assert_eq(file_type_filter.individuals, tuple(individuals))


def test__file_type_filter_create_from_data():
    """
    Tests whether ``file_type_filter_create_from_data`` works as intended.
    """
    data = ['.rms', '.txt', FileTypeFilterGroup.audio.value, FileTypeFilterGroup.image.value]
    
    file_type_filter = file_type_filter_create_from_data(data)
    assert_file_type_filter_fields_set(file_type_filter)
    
    vampytest.assert_eq(file_type_filter.groups, (FileTypeFilterGroup.audio, FileTypeFilterGroup.image))
    vampytest.assert_eq(file_type_filter.individuals, ('rms', 'txt'))
    

def test__file_type_filter_convert_to_data():
    """
    Tests whether ``file_type_filter_convert_to_data`` works as intended.
    """
    groups = [FileTypeFilterGroup.audio, FileTypeFilterGroup.image]
    individuals = ['rms', 'txt']
    
    file_type_filter = file_type_filter_create(
        groups = groups,
        individuals = individuals,
    )
    
    output = file_type_filter_convert_to_data(file_type_filter)
    vampytest.assert_eq(
        output,
        ['.rms', '.txt', FileTypeFilterGroup.audio.value, FileTypeFilterGroup.image.value],
    )
