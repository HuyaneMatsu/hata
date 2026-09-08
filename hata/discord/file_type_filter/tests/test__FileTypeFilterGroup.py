import vampytest

from ..preinstanced import FileTypeFilterGroup


@vampytest.call_from(FileTypeFilterGroup.INSTANCES.values())
def test__FileTypeFilterGroup__instances(file_type_filter_group):
    """
    Tests whether ``FileTypeFilterGroup`` instances have the correct structure.
    
    Parameters
    ----------
    file_type_filter_group : ``FileTypeFilterGroup``
        The instance to test.
    """
    vampytest.assert_instance(file_type_filter_group, FileTypeFilterGroup)
    vampytest.assert_instance(file_type_filter_group.name, str)
    vampytest.assert_instance(file_type_filter_group.value, FileTypeFilterGroup.VALUE_TYPE)
    vampytest.assert_instance(file_type_filter_group.members, tuple, nullable = True)
