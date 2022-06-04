from dotenv import dotenv_values
from hata import Client, wait_for_interruption
from hata.ext.plugin_loader import add_default_plugin_variables, load_all_plugin, register_plugin


config = dotenv_values('.env')

Sakuya = Client(
    config['TOKEN'],
    extensions = ('slash', 'solarlink'),
)

# Returns True on success, so we check for False.
if not Sakuya.solarlink.add_node('127.0.0.1', 2333, 'youshallnotpass', None):
    raise RuntimeError('Connecting to node unsuccessful.')


add_default_plugin_variables(Sakuya=Sakuya)
register_plugin('modules')
load_all_plugin()


Sakuya.start()

wait_for_interruption()
