from dotenv import dotenv_values
from hata import Client, wait_for_interruption
from hata.ext.plugin_loader import add_default_plugin_variables, load_all_plugin, register_plugin

config = dotenv_values('.env')

Sakuya = Client(config['TOKEN'],
    extensions = 'commands_v2',
    prefix = '!',
)


@Sakuya.events
async def ready(client):
    print(f'{client:f} is connected!')

# Registered variables to extension loader, show up in each loaded extension file.
add_default_plugin_variables(Sakuya=Sakuya)
# Adds the extensions file or the extensions files recursive in the directory
register_plugin('modules')
# Loads all the added extension files.
load_all_plugin()


Sakuya.start()

wait_for_interruption()
