import vampytest

from ..audio_source import DEFAULT_EXECUTABLE, LocalAudio


def test__LocalAudio__create_process_preprocess__file_does_not_exists():
    """
    Tests whether ``LocalAudio._create_process_preprocess`` raises when the file does not exists.
    
    Case: Raise `source` is not a file.
    """
    source = '/root/stuff'
    
    def is_file(input_path):
        nonlocal source
        vampytest.assert_eq(source, input_path)
        return False
    
    mocked = vampytest.mock_globals(
        LocalAudio._create_process_preprocess.__func__,
        is_file = is_file,
    )
    
    with vampytest.assert_raises(ValueError):
        mocked(LocalAudio, source, DEFAULT_EXECUTABLE, False, None, None)


def test__LocalAudio__create_process_preprocess__passing():
    """
    Tests whether ``LocalAudio._create_process_preprocess`` raises when the file does not exists.
    
    Case: passing.
    """
    source = '/root/stuff'
    
    def is_file(input_path):
        nonlocal source
        vampytest.assert_eq(source, input_path)
        return True
    
    mocked = vampytest.mock_globals(
        LocalAudio._create_process_preprocess.__func__,
        is_file = is_file,
    )
    
    executable, parameters, io = mocked(LocalAudio, source, DEFAULT_EXECUTABLE, False, None, None)
    vampytest.assert_eq(executable, DEFAULT_EXECUTABLE)
    vampytest.assert_eq(
        parameters,
        ['-i', source, '-f', 's16le', '-ar', '48000', '-ac', '2', '-loglevel', 'panic', 'pipe:1'],
    )
    vampytest.assert_is(io, None)
