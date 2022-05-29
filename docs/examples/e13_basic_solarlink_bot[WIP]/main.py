from dotenv import dotenv_values
from hata import Client, wait_for_interruption
from hata.ext.plugin_loader import EXTENSION_LOADER


config = dotenv_values('.env')

Sakuya = Client(
    config['TOKEN'],
    extensions = ('slash', 'solarlink'),
)

# Returns True on success, so we check for False.
if not Sakuya.solarlink.add_node('127.0.0.1', 2333, 'youshallnotpass', None):
    raise RuntimeError('Connecting to node unsuccessful.')


EXTENSION_LOADER.add_default_variables(Sakuya=Sakuya)
EXTENSION_LOADER.register('modules')
EXTENSION_LOADER.load_all()


Sakuya.start()

wait_for_interruption()
