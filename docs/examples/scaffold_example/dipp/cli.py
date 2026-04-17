__all__ = ('main',)

def main():
    try:
        from hata.main import execute_command_from_system_parameters
    except ImportError as err:
        raise ImportError(
            'Couldn\'t import hata. '
            'Are you sure it\'s installed and available on your PYTHONPATH environment variable? '
            'Did you forget to activate a virtual environment?'
        ) from err

    from hata.ext.plugin_auto_reloader import start_auto_reloader, warn_auto_reloader_availability
    from hata.ext.plugin_loader import load_all_plugin, frame_filter, register_plugin
    from scarletio import get_event_loop, write_exception_sync

    from . import bots

    register_plugin(f'{__spec__.parent}.plugins')

    try:
        load_all_plugin()
    except BaseException as err:
        write_exception_sync(err, filter = frame_filter)
        get_event_loop().stop()
        raise SystemExit(1) from None

    warn_auto_reloader_availability()
    start_auto_reloader()

    execute_command_from_system_parameters()
